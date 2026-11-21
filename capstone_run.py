#!/usr/bin/env python3
"""
Capstone test runner. Three trials of the five criteria in criteria.md
(Capstone section), through Flask's test client with the real model.

    python capstone_run.py --label before
    python capstone_run.py --label after
    python capstone_run.py --cost          # cost of one run, 10 runs averaged

Rate limiting is turned off here (it would 429 the 10-submission batches).
Audit entries go to results/capstone_log_<label>_trialN.jsonl, not the main log.
"""
import argparse
import datetime as dt
import random
import statistics
import sys
import time

import config

config.RATE_LIMITING_ENABLED = False
import audit  # noqa: E402
import detector  # noqa: E402
from app import app  # noqa: E402

RES = config.RESULTS_DIR
LABEL = "run"

SENT = [
    "I walked to the market this morning and the baker had run out of rye again.",
    "My brother says the bridge will never reopen, but he said that last year too.",
    "The report covers three areas: cost, schedule, and risk, in that order.",
    "Honestly the movie dragged in the middle, though the ending almost made up for it.",
    "We measured each sample twice because the first readings looked suspiciously high.",
    "Rain kept the dog inside, so she chewed through two pairs of my good socks.",
    "It is important to note that several factors contribute to the overall outcome.",
    "After the meeting Dana asked whether anyone had actually read the contract.",
    "The garden needs water, but the hose split in half on Tuesday and nobody fixed it.",
    "Prices rose sharply in March, then flattened out once the new supplier arrived.",
    "Moreover, the system provides a comprehensive solution to a wide range of problems.",
    "I never learned to whistle, which my grandfather considered a personal failing.",
]
WARM = "Warm up the model with one ordinary sentence of text here, please."


def make_texts(n, seed):
    rnd = random.Random(seed)
    return [" ".join(rnd.sample(SENT, 8)) for _ in range(n)]


def post(c, body=None, raw=None):
    t = time.perf_counter()
    if raw is not None:
        r = c.post("/submit", data=raw, content_type="text/plain")
    else:
        r = c.post("/submit", json=body)
    return r, (time.perf_counter() - t) * 1000


def count():
    return len(audit.read_entries())


def crit1(c, seed):
    cases = [
        {"creator_id": "t"}, {"text": "", "creator_id": "t"}, {"text": "   ", "creator_id": "t"},
        {"text": 12345, "creator_id": "t"}, "RAW", [1, 2, 3],
        {"text": "a" * 100_000, "creator_id": "t"}, {"text": make_texts(1, seed)[0]},
    ]
    ok, detail = 0, []
    for case in cases:
        before = count()
        r, _ = post(c, raw="not json at all") if case == "RAW" else post(c, body=case)
        new = audit.read_entries()[before:]
        good = (400 <= r.status_code < 500 and r.is_json and len(new) == 1
                and new[0].get("event") == "rejected" and new[0].get("reason")
                and new[0].get("http_status") and new[0].get("duration_ms") is not None)
        ok += bool(good)
        detail.append(f"{r.status_code}/{len(new)} entries")
    return ok, len(cases), detail


def crit2(c, seed):
    config.DETECTOR_TIMEOUT_S = 0.001
    ok, detail = 0, []
    for t in make_texts(5, seed):
        before = count()
        r, ms = post(c, {"text": t, "creator_id": "t"})
        new = audit.read_entries()[before:]
        good = (r.status_code == 504 and (r.get_json() or {}).get("error") == "detector_timeout"
                and ms < 1000 and len(new) == 1 and new[0].get("reason") == "detector_timeout")
        ok += bool(good)
        detail.append(f"{r.status_code} {ms:.0f}ms")
    config.DETECTOR_TIMEOUT_S = 20
    return ok, 5, detail


def crit3(c, seed):
    time.sleep(8)  # let background jobs finish
    ok, detail = 0, []
    for t in make_texts(3, seed + 1):
        r, ms = post(c, {"text": t, "creator_id": "t"})
        j = r.get_json() or {}
        good = r.status_code == 200 and j.get("model_score") is not None and j.get("style_score") is not None
        ok += bool(good)
        detail.append(f"{r.status_code} {ms:.0f}ms")
    return ok, 3, detail


def crit45(c, seed):
    durs, walls = [], []
    for t in make_texts(10, seed + 2):
        before = count()
        r, ms = post(c, {"text": t, "creator_id": "t"})
        new = audit.read_entries()[before:]
        durs.append(new[0]["duration_ms"] if r.status_code == 200 and new else float("nan"))
        walls.append(ms)
    med, mx = statistics.median(durs), max(durs)
    ok4 = med <= 3000 and mx <= 6000
    ok5 = sum(1 for d, w in zip(durs, walls) if abs(d - w) <= max(0.25 * w, 50))
    return ok4, ok5, med, mx, durs, walls


def trial(i):
    config.AUDIT_LOG = RES / f"capstone_log_{LABEL}_trial{i}.jsonl"
    if config.AUDIT_LOG.exists():
        config.AUDIT_LOG.unlink()
    c = app.test_client()
    seed = 100 * i
    detector.model_signal(WARM)
    return crit1(c, seed), crit2(c, seed), crit3(c, seed), crit45(c, seed)


def cost(n=10):
    config.AUDIT_LOG = RES / "capstone_log_cost.jsonl"
    if config.AUDIT_LOG.exists():
        config.AUDIT_LOG.unlink()
    c = app.test_client()
    detector.model_signal(WARM)
    cpu, wall = [], []
    for t in make_texts(n, 7):
        p0, w0 = time.process_time(), time.perf_counter()
        r, _ = post(c, {"text": t, "creator_id": "cost"})
        cpu.append(time.process_time() - p0)
        wall.append(time.perf_counter() - w0)
        assert r.status_code == 200
    out = (f"wall seconds per run: mean {statistics.mean(wall):.3f}, runs {[round(x, 3) for x in wall]}\n"
           f"cpu seconds per run (time.process_time, all threads): mean {statistics.mean(cpu):.3f}, "
           f"runs {[round(x, 3) for x in cpu]}\n")
    (RES / f"cost_{dt.date.today()}.md").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="run")
    ap.add_argument("--cost", action="store_true")
    a = ap.parse_args()
    LABEL = a.label
    if a.cost:
        cost()
        sys.exit()
    rows = {k: [] for k in range(1, 6)}
    passes, notes = [], []
    for i in (1, 2, 3):
        c1, c2, c3, (ok4, ok5, med, mx, durs, walls) = trial(i)
        rows[1].append(f"{c1[0]}/{c1[1]}")
        rows[2].append(f"{c2[0]}/{c2[1]}")
        rows[3].append(f"{c3[0]}/{c3[1]}")
        rows[4].append(f"median {med:.0f}ms max {mx:.0f}ms")
        rows[5].append(f"{ok5}/10")
        notes.append(f"trial {i}: c1 {c1[2]} | c2 {c2[2]} | c3 {c3[2]} | "
                     f"durations {[round(x) for x in durs]} walls {[round(x) for x in walls]}")
        passes.append((c1[0] == c1[1], c2[0] == c2[1], c3[0] == c3[1], ok4, ok5 >= 9))
    names = ["1. Every failed request logged (8 of 8)", "2. Timeout -> fast 504, logged (5 of 5)",
             "3. Recovery after timeouts (3 of 3)", "4. Warm latency (median<=3000, max<=6000 ms)",
             "5. Logged duration honest (9 of 10)"]
    out = ["| Criterion | Run 1 | Run 2 | Run 3 | Verdict |", "|---|---|---|---|---|"]
    for k in range(5):
        v = "MET" if all(p[k] for p in passes) else "MISSED"
        out.append(f"| {names[k]} | {rows[k + 1][0]} | {rows[k + 1][1]} | {rows[k + 1][2]} | {v} |")
    out += ["", "```", *notes, "```", "", "Sample log lines (trial 1):", "```"]
    log = (RES / f"capstone_log_{LABEL}_trial1.jsonl").read_text(encoding="utf-8").splitlines()
    out += [x for x in log if '"rejected"' in x][:3] + [x for x in log if '"decided"' in x][:3] + ["```"]
    f = RES / f"capstone_{LABEL}_{dt.datetime.now():%Y-%m-%d_%H%M}.md"
    f.write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    print("->", f)
