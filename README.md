# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. Text comes in. Someone's site sends `POST /submit` with `text` and `creator_id` to `app.py::submit`. It makes a `content_id` for it. If the text is missing, empty, or crazy long it sends back a 400 and stops.
2. Signal one, `detector.py::model_signal`. Runs gpt2 on my laptop and checks how predictable the text is. Gives back `model_score`, 0 to 1, higher = more AI.
3. Signal two, `stylometry.py::style_signal`. Doesn't read the text, just looks at its shape: sentence lengths, repeated words, punctuation. Gives back `style_score`, same direction.
4. `scoring.py::combine_signals` squishes the two scores into one `combined_score`.
5. `scoring.py::score_to_label` turns that number into a guess (ai / human / unsure) and the sentence the writer actually sees.
6. `audit.py::log_decision` writes it all to `logs/audit.jsonl` (ids, guess, both scores, combined score, label, status `decided`).
7. The response goes back with `content_id`, guess, confidence, label, and both scores. If the writer thinks it's wrong they hit `POST /appeal` with the `content_id`, and it gets logged and set to `under_review`.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to gpt2 (runs locally). It's perplexity, turned into 0-1 where higher = more AI-ish. Code is `detector.py::model_signal`.

**Why that might differ between human and AI writing:** A model writes by picking the likely next word, so another model finds it easy to guess. People are weirder. Random word choices, sudden turns, specific stuff.

**What it can't see:** Who actually wrote it. It only sees "predictable", and plain writing is predictable too. Someone writing in their second language with safe simple words, a younger writer, or just someone keeping it plain, all look like AI to this thing. Fancy human writing with rare words looks human. It also only reads the first 400 tokens (`DETECTOR_MAX_TOKENS`), so the rest is ignored. And AI text with some weird words stuck in could slip past.

### Signal two — the style signal

**What it measures:** The shape of the text, not what it says. How much sentence length bounces around, how many words are unique vs repeated, and how much punctuation there is. Code is `stylometry.py::style_signal`.

**Why that might differ between human and AI writing:** AI tends to write even, medium sentences and reuse a smaller set of words. Humans are lumpier, like a 3 word sentence right next to a 40 word one.

**What it can't see:** The meaning. It can't read at all. So anything that changes the shape without changing the point fools it: typos, chopping sentences up, pasting a quote in. That's cheap to do on purpose. It's also unfair to real people who just write evenly (formal essays, technical writing, really short pieces where the numbers are basically noise).

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two scores. But if they're really far apart (more than 0.4), don't trust the average either way and squeeze the result into 0.40-0.60, which is the unsure range. Reasoning: two methods that disagree means we don't know. And the thing I'm scared of is signal one calling a plain human writer AI, so I don't want it to be able to decide that alone.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`, `DISAGREEMENT_GAP = 0.40`, `DISAGREEMENT_BAND = (0.40, 0.60)`, all in `config.py`. Thresholds are still `HUMAN_THRESHOLD = 0.35` and `AI_THRESHOLD = 0.65`. Style signal (`stylometry.py::style_signal`) is 0.5 x sentence length spread + 0.3 x punctuation density + 0.2 x vocabulary variety, each scaled to 0-1 and flipped so higher = more AI. Spread counts most because it seemed most reliable, vocabulary least because it still changes with text length and topic.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

My plain human paragraph ("I moved to this city three years ago for work, and the biggest surprise was how quiet the evenings are. People go home early. On weekends the park fills up, though, and everyone seems to know each other."): `model_score` 0.734, `style_score` 0.191. Signal one says AI because the words are all ordinary. Signal two says human because the sentences are different lengths (a 4 word one next to a long one). They're 0.54 apart, over the 0.4 gap, so the combined score is 0.462, unsure. Without the rule it would've been 0.46 anyway here, but the rule matters when one is like 0.95 and the other 0.45.

Calibration table (all four plus the plain one):

| input | model | style | combined |
|---|---|---|---|
| clearly AI | 0.908 | 0.841 | 0.875 |
| clearly human (casual) | 0.247 | 0.143 | 0.195 |
| formal human | 0.167 | 0.000 | 0.084 |
| lightly edited AI | 0.574 | 0.363 | 0.468 |
| plain human | 0.734 | 0.191 | 0.462 |

Clear AI and clear human are 0.68 apart. Edited AI ends up in unsure, so it gets through. That's a miss, but I'd rather miss it than accuse someone. I only tested one example of each, so these are not solid numbers.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.65 | We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything. |
| high-confidence AI | 0.65 – 1.00 | This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look. |

**Why I worded the "unsure" one this way:**
I wanted it to say "we don't know" without sounding like "we think you cheated". So it says outright that it doesn't mean there's a problem and that you don't have to do anything. A writer who got this on their own work shouldn't feel like they have to defend themselves. I also kept the word "AI" in there once because otherwise it's too vague to mean anything. The AI label is the scary one, so it admits we can get it wrong (especially for plain writing, which is what the detector is worst at) and points to the appeal.
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables. Finally, it is essential to ensure that the system remains robust and scalable over time.", "creator_id": "ai1"}'
```

```json
{
  "confidence": 0.8747,
  "content_id": "8b5adf7075cc44beb3390fae2733f063",
  "guess": "ai",
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "model_score": 0.908,
  "style_score": 0.8414
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "8b5adf7075cc44beb3390fae2733f063", "reasoning": "I wrote this myself for a class."}'
```

```json
{
  "content_id": "8b5adf7075cc44beb3390fae2733f063",
  "message": "We got your appeal. A person will look at this decision again.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log"
```

Entries for this content_id (the first is the original decision, the second is the appeal after it):

```json
{
  "timestamp": "2026-11-03T01:59:10+00:00",
  "content_id": "8b5adf7075cc44beb3390fae2733f063",
  "creator_id": "ai1",
  "guess": "ai",
  "model_score": 0.908,
  "style_score": 0.8414,
  "combined_score": 0.8747,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "status": "decided"
}
{
  "timestamp": "2026-11-03T01:59:11+00:00",
  "content_id": "8b5adf7075cc44beb3390fae2733f063",
  "creator_id": "ai1",
  "event": "appeal",
  "status": "under_review",
  "reasoning": "I wrote this myself for a class."
}
```

---

## How I Used AI

Straight up: Claude Code did most of the building in this project. I gave it each milestone and it wrote the code, the README sections and the first draft of `criteria.md`, and ran the tests. The two moments below are the ones where what I got was off and something had to change.

**Moment 1**

- *What I asked for:* The Milestone 1 write-up: the path a submission takes, what both signals measure and miss, the false positive trace, and the shape of `/submit` and `/appeal`.
- *What came back:* Correct, but it read like a polished essay. Words like "the substance" and "ornate", numbered bold lead-ins, and a very confident tone about numbers (like a 0.8 `model_score`) that nobody had measured yet.
- *What I changed:* I asked for it to be redone in plain student voice. The rewrite kept the same facts but said the 0.8 was a guess to check in Milestone 3. When I did check, my plain human paragraph scored 0.73 on signal one, so the guess was about right, and that is what the false positive trace was worried about.

**Moment 2**

- *What I asked for:* Milestone 4, the style signal and the combining rule.
- *What came back:* Three measures in `stylometry.py`, a combine rule that averages and then clamps to the unsure band when the two signals are more than 0.4 apart, and a table of the four calibration inputs plus my plain paragraph (model 0.734, style 0.191, so they split). Then the first live `/submit` crashed with `NameError: name 'stylometry' is not defined`, because one of the edits to `app.py` silently didn't apply (the comment it was matching on was different from what it assumed).
- *What I changed:* Added the missing imports in `app.py` and reran, and the response then had both scores and the log had all three numbers. Keep in mind the calibration table is one example per row, so I can't say the numbers are solid, and the criteria numbers in `criteria.md` were drafted by Claude as proposals. I'm the one who has to defend them in unit 8.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-05T02:22:57+00:00", "content_id": "0c31eddbd8374e6aa1ad09837c6e7f31", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.7574, "combined_score": 0.4604, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-05T02:22:57+00:00", "content_id": "0c31eddbd8374e6aa1ad09837c6e7f31", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.7574, "combined_score": 0.4604, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-05T02:22:59+00:00", "content_id": "2c5ae06e2c9247adbebe6fdc4475ecd1", "creator_id": "attacker_EV04", "guess": "ai", "model_score": 0.6114, "style_score": 0.7297, "combined_score": 0.6705, "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.", "status": "decided"}

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**


## Capstone

**What This Extends**

System: Provenance Guard (Project 4). New in this unit: a hardening layer on `/submit` in `app.py`. (1) A scoring timeout (`config.DETECTOR_TIMEOUT_S`, `_run_with_timeout`) so a slow detector returns a 504 instead of hanging the request. (2) Every failed request (bad input, timeout, detector down, unexpected error) now leaves a `rejected` record in `logs/audit.jsonl`. (3) Every record, success or failure, carries `input_chars` and `duration_ms`. (4) Unexpected exceptions in either signal return a JSON 500 instead of a stack trace.

**The Shape**

B, harden against failure. I added the failure handling and the criteria are about the bad path (timeout, rejected input, logging of failures) plus latency.

Out of scope: I'm not changing the detector model, the thresholds or the scoring rule; I'm not adding a third signal; I'm not rebuilding `/appeal` or the rate limiter; I'm not moving to a real queue or process pool to kill timed-out work (a timed-out scoring job still finishes in the background).


**Running It**

Path B (local with logs). Start command `python app.py`; details, environment and clean-checkout steps are in [RUNNING.md](RUNNING.md). I cloned the repo into a fresh folder and brought up the app from the clone (`/health` and `/ping` answered). I did not reinstall the pinned dependencies in a fresh venv, so that part of RUNNING.md is untested.

**Instrumentation**

Each `logs/audit.jsonl` record is one JSON object. Decisions hold `timestamp, content_id, creator_id, guess, model_score, style_score, combined_score, label, status, input_chars, duration_ms`. Failures hold `timestamp, creator_id, event="rejected", status, reason, http_status, input_chars, duration_ms`. `input_chars` is the length of the input (the output is the scores and label). Ten real decision entries (`results/capstone_log_cost.jsonl`, from the cost run):

```
{"timestamp": "2026-11-21T23:42:12+00:00", "content_id": "33ee06de0e774a1d84f8f4bf909d6478", "creator_id": "cost", "guess": "unsure", "model_score": 0.3465, "style_score": 0.6964, "combined_score": 0.5214, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 627, "duration_ms": 194.4}
{"timestamp": "2026-11-21T23:42:12+00:00", "content_id": "58a98bcf93d84edbb3ddf9376da01fa9", "creator_id": "cost", "guess": "unsure", "model_score": 0.3544, "style_score": 0.783, "combined_score": 0.5687, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 637, "duration_ms": 175.9}
{"timestamp": "2026-11-21T23:42:12+00:00", "content_id": "fefeadef94c849a687bd936401070f54", "creator_id": "cost", "guess": "unsure", "model_score": 0.342, "style_score": 0.7957, "combined_score": 0.5688, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 639, "duration_ms": 167.4}
{"timestamp": "2026-11-21T23:42:12+00:00", "content_id": "0499d71511bb4519a3de52f30d8d38d8", "creator_id": "cost", "guess": "unsure", "model_score": 0.4191, "style_score": 0.7724, "combined_score": 0.5958, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 639, "duration_ms": 171.6}
{"timestamp": "2026-11-21T23:42:12+00:00", "content_id": "a76f8f2c835d4cf5903f172e55f50d03", "creator_id": "cost", "guess": "unsure", "model_score": 0.3937, "style_score": 0.7014, "combined_score": 0.5475, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 637, "duration_ms": 173.9}
{"timestamp": "2026-11-21T23:42:12+00:00", "content_id": "d7a37c2f5f4143ac86614ca951cc51d8", "creator_id": "cost", "guess": "unsure", "model_score": 0.2668, "style_score": 0.675, "combined_score": 0.4709, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 634, "duration_ms": 174.6}
{"timestamp": "2026-11-21T23:42:13+00:00", "content_id": "9836eaf2ae70459d9fa8440ecebd421e", "creator_id": "cost", "guess": "unsure", "model_score": 0.2493, "style_score": 0.7614, "combined_score": 0.5053, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 631, "duration_ms": 190.9}
{"timestamp": "2026-11-21T23:42:13+00:00", "content_id": "3790f84279724ceaae1f4ecc019e4188", "creator_id": "cost", "guess": "unsure", "model_score": 0.3702, "style_score": 0.6686, "combined_score": 0.5194, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 628, "duration_ms": 179.0}
{"timestamp": "2026-11-21T23:42:13+00:00", "content_id": "f781bf8c74484387b71e59170e14c21b", "creator_id": "cost", "guess": "unsure", "model_score": 0.2563, "style_score": 0.6627, "combined_score": 0.4595, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 631, "duration_ms": 191.8}
{"timestamp": "2026-11-21T23:42:13+00:00", "content_id": "505a52dd9047498d9906c4866f23569f", "creator_id": "cost", "guess": "unsure", "model_score": 0.3952, "style_score": 0.6863, "combined_score": 0.5408, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 635, "duration_ms": 260.4}
```

Failed runs from the same harness (`results/capstone_log_before_trial1.jsonl`): bad input, and a timeout:

```
{"timestamp": "2026-11-21T23:38:33+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": null, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:38:33+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": 0, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:38:33+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": 3, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:38:33+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "detector_timeout", "http_status": 504, "input_chars": 633, "duration_ms": 17.6}
```

Not covered: 429 rate-limit rejections are logged by the older handler in `app.py` and do not have `duration_ms` or `input_chars`.

**What It Costs**

Measured with `python capstone_run.py --cost`: 10 warm submissions through `/submit`, timed with `time.perf_counter` (wall) and `time.process_time` (CPU, all threads). No API spend; gpt2 runs locally. Per run: mean 0.190 s wall, mean 2.44 s CPU (runs 2.1 to 2.8). CPU is much larger than wall because torch uses several cores at once. Hundred-people-a-day arithmetic: assume 5 submissions each, 100 x 5 = 500 runs/day; 500 x 0.19 s = 95 s of wall time and 500 x 2.44 s = 1,220 CPU-seconds (about 20 minutes of one core's work) per day, which one laptop handles.

**Run Log and Verdicts**

Three trials per criterion, run by `capstone_run.py` (fresh process per label, trials 1 to 3 in one process, model warmed). Criteria are in `criteria.md` (Capstone section), committed in "add capstone criteria" before any results; the first results commit is "capstone: first results (before improvement)". Results file: `results/capstone_before_cpu_2026-11-21_1840.md` (re-run with the CPU metric; the earlier `capstone_before_*.md` from the first run is identical in verdicts).

| Criterion | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|
| 1. Every failed request logged (8 of 8) | 8/8 | 8/8 | 8/8 | MET |
| 2. Timeout -> fast 504, logged (5 of 5) | 5/5 | 5/5 | 5/5 | MET |
| 3. Recovery after timeouts (3 of 3) | 3/3 | 3/3 | 3/3 | MET |
| 4. Warm latency (median<=3000, max<=6000 ms) | median 176ms max 182ms | median 170ms max 180ms | median 174ms max 195ms | MET |
| 5. Logged duration honest (9 of 10) | 10/10 | 10/10 | 10/10 | MET |

All five met. Real output (from `capstone_log_before_trial1.jsonl`, written by `app.py::submit`; the harness is `capstone_run.py::crit1/crit2`): the rejected/timeout/decision lines pasted under Instrumentation above, plus these timings from trial 1 of the first run: timeouts answered in `504 20ms, 15ms, 13ms, 8ms, 20ms`; warm durations `[180, 180, 180, 198, 202, 190, 200, 207, 206, 183]` ms against caller wall times `[183, 182, 182, 201, 204, 193, 202, 209, 208, 186]` ms.

Misses: none, so no diagnosis of a miss. Honest read: my targets were set low. Criterion 4 allowed 3000 ms median and runs came in at about 175 ms, a 17x margin that would not catch a 10x slowdown. Criterion 2's "under 1 s" was met at about 15 ms. The thing the criteria did not see: timed-out requests are answered in about 10 ms but the model keeps running in the background (CPU measurement below).

**The Improvement**

What I changed: `app.py::_run_with_timeout` now sets a cancel flag on timeout, and `detector.py::perplexity` checks it just before the model forward pass and skips the work. Why: the harness's CPU measurement showed 5 timed-out requests burned about 10 CPU-seconds in the background after the client was already told 504 (`orphan_cpu` 10.31 / 12.28 / 10.23 s in the before-run). Stage: the timeout wrapper in `app.py`; mechanism: Python threads cannot be killed, so a timed-out scoring job runs to completion.

Second run log, same format (`results/capstone_after_2026-11-21_1841.md`):

| Criterion | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|
| 1. Every failed request logged (8 of 8) | 8/8 | 8/8 | 8/8 | MET |
| 2. Timeout -> fast 504, logged (5 of 5) | 5/5 | 5/5 | 5/5 | MET |
| 3. Recovery after timeouts (3 of 3) | 3/3 | 3/3 | 3/3 | MET |
| 4. Warm latency (median<=3000, max<=6000 ms) | median 173ms max 192ms | median 174ms max 188ms | median 183ms max 216ms | MET |
| 5. Logged duration honest (9 of 10) | 10/10 | 10/10 | 10/10 | MET |

Orphan CPU after the change: 11.22 / 10.52 / 10.80 s per trial, versus 10.31 / 12.28 / 10.23 before. **It did not help.** I then measured the pieces: one scoring call costs about 1.4 CPU-seconds and 8 idle seconds with the model loaded costs about 1.4 CPU-seconds (torch's thread pool keeps spinning). So the orphan figure is mostly 5 jobs x 1.4 CPU-s plus idle spin, and the cancel check does not stop them because the worker thread has already passed the check (tokenizing takes under a millisecond) by the time the timeout fires. Nothing got worse: criteria 1 to 5 stayed MET. Cancelling mid-forward-pass would need a separate process I can kill, which I did not build.

**What's Still Broken**

Orphaned scoring work after a timeout: I'd run scoring in a worker process (or a bounded single worker queue) so a timed-out job can be killed or at least not piled up. I stopped because it is a bigger change than the unit's 90-minute build limit and all five criteria were already met. The cut: process-based scoring (scope in The Shape).

All five met, so the target to tighten: criterion 4 from "median at most 3000 ms, max at most 6000 ms" to "median at most 400 ms, max at most 1000 ms" (observed about 175 ms and 215 ms, so this still leaves room but would catch a real regression). Also 429 rejections still lack `duration_ms` and `input_chars`.

First thing I'd do next with another unit: process-based scoring with a kill on timeout, because it is the only measured cost (CPU burned after the user already got an error) that my current design cannot remove.

**How I Used AI**

Moment 1: I asked Claude which of my four systems would be easiest to extend for this capstone. It compared them (logging, service layer, test harness already existing) and picked Provenance Guard. I went with it; I changed nothing about the recommendation.

Moment 2: I asked Claude to do the capstone work. It wrote the timeout and logging layer, the criteria, the test harness and the write-up, and ran the three-trial test. Its first improvement (cancel flag) did not reduce the CPU number; Claude measured why and I kept the result as a failed improvement rather than rewording it. Note: I let the AI write the criteria, which the brief says not to do; the criteria and this section were AI-written at my instruction.
