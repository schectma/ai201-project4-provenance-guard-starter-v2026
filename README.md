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

I ran `python run_attacks.py --set attack_set --label before` against my service with nothing changed since Milestone 1. That's 56 attacks: 32 from `attacks.csv` and 24 from `attacks_malformed_requests.csv` (12 bad requests and 12 flood requests). The script auto-marked 0 as broke because nothing crashed or gave a 500, so every held/broke mark below is mine. The full output is in `results/attack_run_2026-11-04_2039_before.md` (made by `run_attacks.py::main`).

**How I decided held or broke.** I had to make up rules and I'm not totally sure they're fair, but here they are:
- Evasion and prompt injection (AI text dressed up): HELD only if it still got the `ai` guess. If it got `unsure` or `human` it BROKE, because the AI text got away without being flagged.
- False positive (real human writing): HELD if it did NOT get `ai`. BROKE if a real person got accused.
- Malformed: HELD if the service answered correctly and didn't crash. BROKE if it did something weird, like calling emoji "AI" or answering a bad request with the wrong status.
- Flood: HELD if the limiter cut it off.

**Score: 22 BROKE, 34 HELD, out of 56.**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 2 (EV04, EV10) | 8 |
| false_positive | 8 | 2 (FP01, FP08) | 6 |
| prompt_injection | 6 | 2 (PI04, PI06) | 4 |
| malformed (MF + RQ) | 20 | 16 | 4 (MF06, MF07, RQ10, RQ11) |
| flood_same_creator | 12 | 12 | 0 |

Full table with my marks:

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c31526d59d16439e848d1dede98d0025` | unsure | 0.460 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `ca9812bf39a2471ba1c98cc0458d67ba` | unsure | 0.430 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `900cbb7f849d49f9851d29ce7f2e8e9b` | unsure | 0.541 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `7dc7a40c5daa412791efd7565eb865db` | ai | 0.670 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `b2591902f5c9401ebe6a5b35c22e263a` | human | 0.241 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `930eeb67a641489f83c31cba81157ed6` | unsure | 0.433 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `d191d7a1b9d848e0b9fa58a3a11946d3` | unsure | 0.408 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `a324eccf68f7422293495e522d597e26` | unsure | 0.477 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `f014bc33b38449c49cdfc034ad13264d` | unsure | 0.573 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `ca68b82e913440cea6288b4d18c7836b` | ai | 0.882 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `259ee332d8fa46baa34ba613e6769a6d` | unsure | 0.588 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `2bf7b83bc7e14c25ba67d238e04820d7` | ai | 0.783 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `8f518060e8e249ffbc4a1747f7aa12b0` | ai | 0.751 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `38e96a7dce8e46ad9836b83a45c7abc4` | ai | 0.744 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `51e26ab444524dec97df4382f93a8c98` | ai | 0.858 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `60e8b4d94a174cdab23e15c3fbdfac61` | ai | 0.691 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `426a36d600e54fb9ba8097ce08c3b815` | ai | 0.686 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `a5f348d5277f47d0981f91bb3b671ba9` | unsure | 0.432 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `11551a28a7d54afb82b309fd11f519a4` | unsure | 0.381 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b67b72a4b1384642a501fe170b4e93f3` | human | 0.234 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `dfc644d03d8d4e01a0ea1a85afd3ada5` | unsure | 0.587 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f97b868ada454b5d8c96c405413a73c6` | unsure | 0.480 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ecc1e83a39484e5dab225618cafe9f5c` | unsure | 0.419 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | `a242a23b37a44b9b9d6e7daab76ddf98` | unsure | 0.555 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `162c3d3fb7ef487aa083768ba7e29277` | unsure | 0.400 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `fe6985ef7c8a4dcb918e699b33f92267` | unsure | 0.400 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `0a950a64811143709d853d09d86b2b94` | unsure | 0.600 | HELD |
| MF06 | malformed | text is emoji only | 200 | `35010545138444e09391d40f8bfbf07d` | ai | 0.799 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `62f5a3dbc4f94532b650841ec14a6252` | ai | 0.754 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | BROKE |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | BROKE |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b54c1ff921eb430c9a50af7f42d6d138` | unsure | 0.400 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `101e17b1290b4014965af14922ac2a73` | unsure | 0.400 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6756e4b84b774ab3bd92e980939663c2` | unsure | 0.400 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `23c2f47d6b24487297d46cd77cb0f313` | unsure | 0.400 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `de77175d65bc42b8a5f213c4eb24f3c6` | unsure | 0.400 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**What I noticed in the results** (diagnosing them properly is Milestone 4):
- 6 of the 8 `false_positive` pieces, which are all real human writing, got the `ai` guess. The worst ones were FP05 (technical docs, 0.858) and FP02 (formal register, 0.783). That's a bad result for a system whose whole point is to not accuse people.
- Most of the evasions worked just by landing in `unsure`. EV02, EV06 and EV07 all pushed `style_score` down to 0.23 to 0.29 while `model_score` stayed at 0.57 to 0.59, and the combining rule averaged them into 0.41 to 0.43.
- PI02 (a fake "SYSTEM:" line stuck on the AI essay) came back `human` at 0.234. My service has no LLM reading the text, so it didn't *obey* the line. The extra words just changed what the two signals measured. Same effect though.
- RQ10 (form-encoded body) and RQ11 (JSON claiming to be plain text) came back **429** instead of 400. Those requests don't have a usable `creator_id`, so `rate_limit_key` falls back to the IP address, and the earlier junk requests from the same IP (RQ02, RQ07, RQ08, RQ09) used up the 5 per minute. So I never actually saw how my validation treats those two. They count as a break because a real writer on the same IP would be locked out by garbage someone else sent.
- MF06 (emoji only, 0.799) and MF07 (right-to-left script, 0.754) got the `ai` guess even though there is no English text to judge. MF03 and MF04 (control characters, only punctuation) got `unsure` at exactly 0.400, so they were still logged as decisions.

**Ten audit log entries from the run** (pulled from `GET /log?limit=200`, 11 shown, 3 of them rejections):

```json
{"combined_score": 0.2414, "content_id": "b2591902f5c9401ebe6a5b35c22e263a", "creator_id": "attacker_EV05", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.3212, "status": "decided", "style_score": 0.1616, "timestamp": "2026-11-05T01:39:52+00:00"}
{"combined_score": 0.2342, "content_id": "b67b72a4b1384642a501fe170b4e93f3", "creator_id": "attacker_PI02", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.2044, "status": "decided", "style_score": 0.2639, "timestamp": "2026-11-05T01:39:55+00:00"}
{"combined_score": 0.7513, "content_id": "8f518060e8e249ffbc4a1747f7aa12b0", "creator_id": "attacker_FP03", "guess": "ai", "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.", "model_score": 0.8051, "status": "decided", "style_score": 0.6976, "timestamp": "2026-11-05T01:39:54+00:00"}
{"combined_score": 0.8576, "content_id": "51e26ab444524dec97df4382f93a8c98", "creator_id": "attacker_FP05", "guess": "ai", "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.", "model_score": 0.8005, "status": "decided", "style_score": 0.9146, "timestamp": "2026-11-05T01:39:54+00:00"}
{"combined_score": 0.7995, "content_id": "35010545138444e09391d40f8bfbf07d", "creator_id": "attacker_MF06", "guess": "ai", "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.", "model_score": 0.9969, "status": "decided", "style_score": 0.6022, "timestamp": "2026-11-05T01:39:58+00:00"}
{"combined_score": 0.7543, "content_id": "62f5a3dbc4f94532b650841ec14a6252", "creator_id": "attacker_MF07", "guess": "ai", "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.", "model_score": 0.9064, "status": "decided", "style_score": 0.6022, "timestamp": "2026-11-05T01:39:58+00:00"}
{"combined_score": 0.6705, "content_id": "7dc7a40c5daa412791efd7565eb865db", "creator_id": "attacker_EV04", "guess": "ai", "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.", "model_score": 0.6114, "status": "decided", "style_score": 0.7297, "timestamp": "2026-11-05T01:39:52+00:00"}
{"combined_score": 0.8819, "content_id": "ca68b82e913440cea6288b4d18c7836b", "creator_id": "attacker_EV10", "guess": "ai", "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.", "model_score": 0.9792, "status": "decided", "style_score": 0.7846, "timestamp": "2026-11-05T01:39:53+00:00"}
{"creator_id": "unknown", "event": "rejected", "limit": "5 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-05T01:39:58+00:00"}
{"creator_id": "attacker_flood", "event": "rejected", "limit": "5 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-05T01:39:59+00:00"}
{"creator_id": "attacker_RQ12", "detail": "Send a non-empty string in \"text\".", "event": "rejected", "reason": "bad_request", "route": "/submit", "status": "rejected", "timestamp": "2026-11-05T01:39:58+00:00"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03, "a non-native English speaker writing carefully". It's real human writing and the service said `ai` with `confidence` 0.7513 (`model_score` 0.8051, `style_score` 0.6976, content_id `8f518060e8e249ffbc4a1747f7aa12b0`). The label the person would see is "This might have been written with AI..." Both signals agreed, so nothing in my combining rule pulled it back toward `unsure`. This is the exact person I wrote about in `design.md`, a careful writer using simple words, and the service accuses them. FP05 scored even higher (0.8576) but FP03 is the one I'd hate to explain, because the writer did everything right and the system punished them for writing plainly.

---

## Run Log and Verdicts

I wrote `scenarios.py` for my five criteria and ran `python run_eval.py --label before` (3 trials). Criteria 1, 2, 3 and 5 are in `scenarios.py`. The `bodies` format can't say "this body isn't JSON" and can't do a submit-then-appeal, so criterion 4 and the non-JSON part of criterion 5 are in a new file, `extra_checks.py` (run 3 times, `--label before`). Files: `results/run_2026-11-04_2043_before.md` (from `run_eval.py::main`) and `results/extra_checks_2026-11-04_2044_before.json` (from `extra_checks.py::main`).

One honest thing: the 10 "my own writing" pieces in `scenarios.py` are written in the style of my own plain writing but were drafted with Claude's help, not copied from my actual essays. The 5 AI pieces are AI generated. The 5 human pieces are also plain student style writing.

Another thing I noticed: all three trials came back with *identical* numbers, to four decimals. gpt2 on CPU with no sampling is deterministic, so the "three trials" idea of the model giving different answers did not show up for me. That does not make it a free pass, it just means the three runs say the same thing.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | at most 1 of 10 of my own pieces gets `ai`, every trial | 2 of 10 `ai` (pieces 5 and 8, 0.682 and 0.665) | 2 of 10 `ai` (same two) | 2 of 10 `ai` (same two) |  |
| 2. Score spread | avg `confidence` of AI group at least 0.3 above human group | AI avg 0.7282, human avg 0.4218, gap 0.3064 | gap 0.3064 | gap 0.3064 |  |
| 3. Label coverage | `human`, `unsure` and `ai` can each be produced | human, unsure, ai | human, unsure, ai | human, unsure, ai |  |
| 4. Appeal path | 10/10 appeals change status and get logged, unknown id gives 404 and no appeal entry | 10/10, 404, no entry | 10/10, 404, no entry | 10/10, 404, no entry |  |
| 5. Bad input | 6/6 bad bodies get 400, no decision logged, /ping and /health still answer | 6/6, 0 decisions added, 200/200 | 6/6, 0 decisions added, 200/200 | 6/6, 0 decisions added, 200/200 |  |

(Criterion 1: the other 8 pieces all came back `unsure`, with `confidence` between 0.530 and 0.616. None of them got `human`. Criterion 2: the 5 AI texts scored 0.8747, 0.6683, 0.7436, 0.6805, 0.6738; the 5 human texts scored 0.5036, 0.5364, 0.3954, 0.3701, 0.3034. Only one of the 5 human texts got the `human` label. The Verdict column gets filled in Milestone 4.)

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

From `results/run_2026-11-04_2043_before.md`, written by `run_eval.py::main`. This is trial 1 of "my own writing", the two pieces that got `ai` plus piece 1 for comparison (I cut the `label` text off so it fits):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6822,
    "model_score": 0.688,
    "style_score": 0.6764,
    "sent": "I think the main thing I learned from this class is that I am bad at e"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6654,
    "model_score": 0.6545,
    "style_score": 0.6764,
    "sent": "We got to the lake around noon and the parking was full, so Dad droppe"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6079,
    "model_score": 0.5186,
    "style_score": 0.6972,
    "sent": "hey, i cant make it to the group meeting thursday because my shift got"
  }
]
```

Bad input, trial 1 (same file, `run_eval.py::main`, the "bad input" scenario). All five bodies got 400:

```json
[
  {
    "status": 400,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "sent": "   "
  },
  {
    "status": 400,
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"
  },
  {
    "status": 400,
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

Appeal path and the non-JSON check, trial 1, from `results/extra_checks_2026-11-04_2044_before.json`, written by `extra_checks.py::main` (I cut the per-appeal detail down to two of the ten):

```json
{
  "trial": 1,
  "criterion_4_appeal": {
    "appeals_ok": 10,
    "of": 10,
    "unknown_id_status": 404,
    "unknown_id_wrote_appeal": false,
    "unknown_ok": true,
    "pass": true,
    "detail": [
      {
        "i": 1,
        "appeal_status": 200,
        "response_status": "under_review",
        "logged": true
      },
      {
        "i": 2,
        "appeal_status": 200,
        "response_status": "under_review",
        "logged": true
      }
    ]
  },
  "criterion_5_extra": {
    "not_json_status": 400,
    "decision_entries_added": 0,
    "ping": 200,
    "health": 200,
    "pass": true
  }
}
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
