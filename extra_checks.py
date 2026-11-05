#!/usr/bin/env python3
"""
The two checks run_eval.py can't do (Unit 8, Milestone 3).

    python extra_checks.py --label before --trials 3

Criterion 4 (appeal path): submit 10 texts, appeal each content_id, then look in
GET /log for an appeal entry for each one. Then appeal a made-up content_id and
check for a 404 and NO appeal entry.

Criterion 5 (the part scenarios.py can't say): a body that isn't JSON, then
/ping and /health still answer, and the number of *decision* entries in the log
did not go up because of the bad requests.

This only sends requests and counts. It doesn't change the service.
"""

import argparse
import datetime as dt
import json
import time
import uuid

import requests

import config
import scenarios

URL = f"http://{config.HOST}:{config.PORT}"


def log_entries():
    return requests.get(f"{URL}/log", timeout=30).json()["entries"]


def appeal_check(trial):
    texts = scenarios.MY_WRITING  # 10 texts
    run = uuid.uuid4().hex[:6]
    ok = 0
    detail = []
    for i, text in enumerate(texts, 1):
        # new creator each time so the rate limit never gets in the way
        sub = requests.post(f"{URL}/submit", timeout=90,
                            json={"text": text, "creator_id": f"appeal_{run}_{i}"})
        if sub.status_code != 200:
            detail.append({"i": i, "submit_status": sub.status_code})
            continue
        cid = sub.json()["content_id"]
        reasoning = f"I wrote this myself, trial {trial} piece {i}."
        ap = requests.post(f"{URL}/appeal", timeout=30,
                           json={"content_id": cid, "reasoning": reasoning})
        entries = [e for e in log_entries() if e.get("content_id") == cid]
        logged = any(e.get("event") == "appeal" and e.get("status") == "under_review"
                     and e.get("reasoning") == reasoning for e in entries)
        passed = ap.status_code == 200 and ap.json().get("status") == "under_review" and logged
        ok += passed
        detail.append({"i": i, "appeal_status": ap.status_code,
                       "response_status": ap.json().get("status"), "logged": logged})

    fake = "does-not-exist-" + uuid.uuid4().hex
    before = len([e for e in log_entries() if e.get("event") == "appeal"])
    r404 = requests.post(f"{URL}/appeal", timeout=30,
                         json={"content_id": fake, "reasoning": "should not work"})
    after = len([e for e in log_entries() if e.get("event") == "appeal"])
    unknown_ok = r404.status_code == 404 and after == before
    return {"appeals_ok": ok, "of": len(texts), "unknown_id_status": r404.status_code,
            "unknown_id_wrote_appeal": after != before, "unknown_ok": unknown_ok,
            "pass": ok == len(texts) and unknown_ok, "detail": detail}


def bad_input_extra():
    decisions_before = len([e for e in log_entries() if "event" not in e])
    results = {}
    # a body that isn't JSON at all. creator_id can't be read so this counts
    # against the IP; that is fine, it is one request.
    r = requests.post(f"{URL}/submit", data="this is not json {{{", timeout=30,
                      headers={"Content-Type": "application/json"})
    results["not_json_status"] = r.status_code
    decisions_after = len([e for e in log_entries() if "event" not in e])
    results["decision_entries_added"] = decisions_after - decisions_before
    results["ping"] = requests.post(f"{URL}/ping", json={"message": "x"}, timeout=10).status_code
    results["health"] = requests.get(f"{URL}/health", timeout=10).status_code
    results["pass"] = (r.status_code == 400 and results["decision_entries_added"] == 0
                       and results["ping"] == 200 and results["health"] == 200)
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--trials", type=int, default=3)
    p.add_argument("--label", default="")
    args = p.parse_args()

    out = {"produced_by": "extra_checks.py", "when": dt.datetime.now().isoformat(timespec="seconds"),
           "label": args.label, "trials": []}
    for t in range(1, args.trials + 1):
        trial = {"trial": t, "criterion_4_appeal": appeal_check(t),
                 "criterion_5_extra": bad_input_extra()}
        out["trials"].append(trial)
        print(f"trial {t}: appeals {trial['criterion_4_appeal']['appeals_ok']}/"
              f"{trial['criterion_4_appeal']['of']}, unknown id "
              f"{trial['criterion_4_appeal']['unknown_id_status']}, "
              f"not-json {trial['criterion_5_extra']['not_json_status']}, "
              f"ping/health {trial['criterion_5_extra']['ping']}/{trial['criterion_5_extra']['health']}")
        time.sleep(1)

    config.RESULTS_DIR.mkdir(exist_ok=True)
    name = f"extra_checks_{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}" + (f"_{args.label}" if args.label else "") + ".json"
    path = config.RESULTS_DIR / name
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
