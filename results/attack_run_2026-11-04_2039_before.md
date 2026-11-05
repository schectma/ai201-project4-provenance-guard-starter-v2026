# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 20:39
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

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

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c31526d59d16439e848d1dede98d0025",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4604,
  "model_score": 0.1635,
  "style_score": 0.7574,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "ca9812bf39a2471ba1c98cc0458d67ba",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4297,
  "model_score": 0.5943,
  "style_score": 0.2651,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "900cbb7f849d49f9851d29ce7f2e8e9b",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5411,
  "model_score": 0.6662,
  "style_score": 0.4159,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "7dc7a40c5daa412791efd7565eb865db",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6705,
  "model_score": 0.6114,
  "style_score": 0.7297,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "b2591902f5c9401ebe6a5b35c22e263a",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2414,
  "model_score": 0.3212,
  "style_score": 0.1616,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "930eeb67a641489f83c31cba81157ed6",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4331,
  "model_score": 0.5727,
  "style_score": 0.2935,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "d191d7a1b9d848e0b9fa58a3a11946d3",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4082,
  "model_score": 0.5862,
  "style_score": 0.2302,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "a324eccf68f7422293495e522d597e26",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4766,
  "model_score": 0.2452,
  "style_score": 0.708,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "f014bc33b38449c49cdfc034ad13264d",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5734,
  "model_score": 0.7042,
  "style_score": 0.4426,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "ca68b82e913440cea6288b4d18c7836b",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8819,
  "model_score": 0.9792,
  "style_score": 0.7846,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "259ee332d8fa46baa34ba613e6769a6d",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5884,
  "model_score": 0.6175,
  "style_score": 0.5592,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "2bf7b83bc7e14c25ba67d238e04820d7",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.783,
  "model_score": 0.7387,
  "style_score": 0.8272,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "8f518060e8e249ffbc4a1747f7aa12b0",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7513,
  "model_score": 0.8051,
  "style_score": 0.6976,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "38e96a7dce8e46ad9836b83a45c7abc4",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7439,
  "model_score": 0.8329,
  "style_score": 0.6548,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "51e26ab444524dec97df4382f93a8c98",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8576,
  "model_score": 0.8005,
  "style_score": 0.9146,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "60e8b4d94a174cdab23e15c3fbdfac61",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6914,
  "model_score": 0.8814,
  "style_score": 0.5014,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "426a36d600e54fb9ba8097ce08c3b815",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.686,
  "model_score": 0.8816,
  "style_score": 0.4903,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "a5f348d5277f47d0981f91bb3b671ba9",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4317,
  "model_score": 0.3223,
  "style_score": 0.5411,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "11551a28a7d54afb82b309fd11f519a4",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3812,
  "model_score": 0.4625,
  "style_score": 0.3,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "b67b72a4b1384642a501fe170b4e93f3",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2342,
  "model_score": 0.2044,
  "style_score": 0.2639,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "dfc644d03d8d4e01a0ea1a85afd3ada5",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.587,
  "model_score": 0.5943,
  "style_score": 0.5797,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "f97b868ada454b5d8c96c405413a73c6",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4801,
  "model_score": 0.4998,
  "style_score": 0.4604,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "ecc1e83a39484e5dab225618cafe9f5c",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4193,
  "model_score": 0.6401,
  "style_score": 0.1984,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "a242a23b37a44b9b9d6e7daab76ddf98",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5548,
  "model_score": 0.5583,
  "style_score": 0.5513,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "162c3d3fb7ef487aa083768ba7e29277",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0,
  "style_score": 0.5222,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "fe6985ef7c8a4dcb918e699b33f92267",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0112,
  "style_score": 0.6022,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "0a950a64811143709d853d09d86b2b94",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9976,
  "style_score": 0.5222,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "35010545138444e09391d40f8bfbf07d",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.7995,
  "model_score": 0.9969,
  "style_score": 0.6022,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "62f5a3dbc4f94532b650841ec14a6252",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7543,
  "model_score": 0.9064,
  "style_score": 0.6022,
  "label": "This might have been written with AI, but we can get this wrong, especially with plain, simple writing. If you wrote it yourself, you can ask for a person to take another look.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "b54c1ff921eb430c9a50af7f42d6d138",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.5222,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "101e17b1290b4014965af14922ac2a73",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.5222,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "6756e4b84b774ab3bd92e980939663c2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.5222,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "23c2f47d6b24487297d46cd77cb0f313",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.5222,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "de77175d65bc42b8a5f213c4eb24f3c6",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.5222,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
