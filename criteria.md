# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives: at most 1 in 10 of my own writing gets the high-confidence AI label

Take 10 pieces of real human writing (my own essays, emails, and a couple of plain simple ones too, not just the nice ones). Submit each to `/submit`. At most 1 of the 10 comes back with guess `ai`. This has to be true in all three trials, not just one.

**Why this target:**

Wrongly telling someone they cheated is the worst thing this system can do, and they might lose real stuff over it (their account, their reputation). Missing some AI text barely costs anything in comparison. I thought about 0 in 10 but gpt2 is small and plain human writing looks like AI to it, so 0 is probably not honest. 1 in 10 is already a lot though. I'd be annoyed if it was my essay.

---

## 2. Score spread: clearly-AI and clearly-human text land at least 0.3 apart

Take 5 pieces I'm sure are AI (I'll generate them) and 5 I'm sure are human (I wrote them). The average `confidence` of the AI group has to be at least 0.3 higher than the average of the human group. I'm only checking the averages, not every single piece, because gpt2 is too rough for that.

**Why this target:**

If clear cases don't even score apart, the labels are basically random and the rest doesn't matter. 0.3 is big enough that the two groups should end up on different sides of the unsure band (0.35 to 0.65), but I'm not requiring it to be perfect since nothing is. Smaller than that and I wouldn't trust it.

---

## 3. Label coverage: all three labels can be produced by real text

I have to be able to submit text that gets each of the three labels (high-confidence human, unsure, high-confidence AI) through `/submit`, and `scoring.label_ranges()` shouldn't show a gap or overlap. Done once for each label, and I paste the three responses in the README.

**Why this target:**

The config note says that with a weak style signal the combined score gets stuck in a narrow range, so one label can end up impossible to get. A label nobody can reach is basically a fake feature. This one is easy to check, yes and no, so there's no arguing with myself later.

---

## 4. The appeal path: every appeal of a real `content_id` changes status and gets logged, 10 out of 10

Submit 10 pieces of text, appeal each one with its `content_id`. After every appeal, `GET /log` shows an entry for that `content_id` with `"event": "appeal"` and status `under_review`, with the reasoning I sent. Also, appealing a `content_id` that doesn't exist returns a 404 and does not write an appeal entry. 10 out of 10 each trial, no misses.

**Why this target:**

The appeal is the only thing a wrongly accused writer can do. If even 1 in 10 silently vanishes, then for that person there is no appeal at all. So it's all of them, not "most". It's code that is either right or wrong, unlike the detector, so a perfect score is reasonable to ask for.

---

## 5. Bad input: missing, empty, or whitespace-only `text`, or text over the limit, never crashes the service

Send `/submit` these: no `text` field, `text` as `""`, `text` as `"   "`, `text` as a number, a body that isn't JSON, and `text` of 100,000 characters. Every one gets a 400 with an error message (never a 500, never a crash), and none of them write a decision to the log. After all of them, `/ping` and `/health` still answer. 6 out of 6.

**Why this target:**

A malformed request that takes down the service is a really common real failure, and it's one I can fully prevent unlike the detection stuff. The 100,000 characters one matters because gpt2 is slow, so a huge submission could freeze things for everybody. Not logging them keeps junk out of the audit log.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->


---
---

# Capstone criteria (unit 9)

Written before any capstone test run. Extension = the hardening layer on `/submit` (timeout, logged failures, `duration_ms`/`input_chars` fields). Criteria 1-4 are about the extension, 5 is about the original system. Each trial is a fresh run of `capstone_run.py`; the target must hold in all three trials. Runs go through Flask's test client with the real gpt2 model and rate limiting off, model warmed first.

## Capstone 1. Every failed /submit leaves a record: 8 of 8 bad requests produce exactly one `rejected` audit entry

Send 8 bad requests: missing `text`, `text` = "", `text` = "   ", `text` = a number, non-JSON body, JSON list body, 100,000-char text, missing `creator_id`. Each gets a 4xx JSON response, and the log gains exactly one new entry with `event: rejected`, a `reason`, `http_status`, and `duration_ms`. 8 of 8, every trial.

**Why this target:** The whole point of the extension is that a failure must never be an absence. Any miss means some failure type is invisible. It's deterministic code, so it should be 8 of 8, not "most".

## Capstone 2. Timeout: with the timeout shrunk to 0.001 s, 5 of 5 valid submissions return a 504 JSON `detector_timeout` within 1 second, and each is logged

Set `config.DETECTOR_TIMEOUT_S = 0.001`, submit 5 valid texts. Each returns 504 with `error: detector_timeout` in under 1.0 s wall time, and each has a `rejected` entry with `reason: detector_timeout`. 5 of 5 each trial.

**Why this target:** A request that hangs while gpt2 grinds is the failure this layer exists to stop, so the caller must get an answer fast. Under 1 s (not under the timeout exactly) allows for thread start overhead but still fails if the request waits for the model, which takes 1-2 s warm.

## Capstone 3. Recovery: after the timeouts, the next 3 normal submissions all return 200

Restore the timeout to 20 s (after letting background scoring jobs finish), submit 3 valid texts. 3 of 3 return 200 with a real `model_score` and `style_score`, and are logged as decisions.

**Why this target:** Timed-out jobs keep running in the background (Python can't kill a thread). If they poison the model or block later requests, the hardening made things worse. Needs to be 3 of 3 since a one-off failure here would still mean a user got an error for no reason.

## Capstone 4. Warm latency: median `duration_ms` of 10 normal submissions is at most 3000 ms and the slowest is at most 6000 ms

10 valid texts of 80-150 words after the model is loaded, read `duration_ms` from the audit log. Median at most 3000 ms and max at most 6000 ms. Warm requests only; the first request after a cold start is excluded and said so.

**Why this target:** The config comments say a warm request takes "a second or two" on CPU. 3 s median gives room for a slow laptop but would catch a regression to something users would give up on. The max bound catches the occasional stall that a median hides. Stricter (1 s) would just test my CPU, not my system.

## Capstone 5. Logged duration is honest: `duration_ms` is within 25% of the wall-clock time the caller measured, for at least 9 of 10 submissions

For the same 10 submissions, compare the log's `duration_ms` to a `time.perf_counter()` measurement around the client call. 9 of 10 within 25% of the wall time (or within 50 ms for fast ones).

**Why this target:** Latency numbers in the log are only useful for diagnosis if they're true. If the logged time leaves out the model call (the slow part) it would look fine and be useless. 25% allows for Flask overhead outside the handler; 9 of 10 allows one scheduling hiccup.
