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

**My limits:** 5 per minute, 100 per day

**Why those numbers and not others:**
A real writer submits maybe a few things an hour, and even if they fix a typo and resubmit, 5 a minute is plenty. 100 a day is way more than a person would do. A script trying to map my thresholds needs hundreds of variations, so 5 a minute slows it to a crawl and 100 a day caps it. I picked these kind of by feel, not from any data. One thing I noticed is each submission takes a second or two on gpt2 anyway, so a flood is also expensive for me, which is another reason to keep it low.
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** The `creator_id` in the request body. If there isn't a usable one (missing, empty, or the body isn't a JSON object) it falls back to the caller's IP address. That's what the starter's `rate_limit_key` already does. The downside is that someone can dodge the limit by just changing `creator_id` every request, since I never check it's a real account. Counting by address would stop that but would lump a whole household or school together.

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 15
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
10 of 15 were rate limited.
```

First 5 got through, the other 10 got a 429. Full output is in `results/flood_2026-11-02_2107.md`. `GET /health` shows `"rate_limiting": true`, and the log has a rejection entry for each 429, for example:

```json
{"creator_id": "flood_tester", "event": "rejected", "limit": "5 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-03T02:07:06+00:00"}
```

I also changed `app.py` so my own 400s (missing text and so on) get written to the log as `rejected` entries too, using `audit.log_rejection`. Before this they left no trace. Unknown `content_id` appeals get logged the same way.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

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
