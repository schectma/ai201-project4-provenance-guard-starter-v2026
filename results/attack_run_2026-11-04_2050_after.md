# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 20:50
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `f0852ddfb61f4e1aa9131e78d518a69c` | unsure | 0.460 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `58b104bce56f452b8afa36ee355e0d2a` | unsure | 0.430 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d69efc46fb1d486190fe1cd1d1406c2a` | unsure | 0.541 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `93a80cc06d78406bb789bd7474f391f1` | unsure | 0.670 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `400667033c1e4acea778c8c2e55958be` | human | 0.241 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `a2343b9669d54952b6714f9e3dcb169a` | unsure | 0.433 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e4d7a7e72b694663861ddc763cca803f` | unsure | 0.408 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `6e08e34fe1c84cdea2543953d19cc909` | unsure | 0.477 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `8cbe6b3f9a77450490d065b9b7e3d0e9` | unsure | 0.573 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `60d121e266f547459ad03ed50ed0ad4d` | ai | 0.882 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `812069ccf5f447b68965279e8d61c2f4` | unsure | 0.588 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `a664e3d63e2b4c00af53703891b76571` | ai | 0.783 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `7877df46a0d248b4ab6b945be7422ef9` | ai | 0.751 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `cc865bbe2e7b4e648b817b1c6f5139d6` | ai | 0.744 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `02fc247b06b549b18854ae6ab004e4b2` | ai | 0.858 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `c376e4b5519a461a9c56d15700688895` | unsure | 0.691 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `aecd8fc135a44a529adc9a04a4f728f1` | unsure | 0.686 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `91357d879fff485590eb419c4b7abd15` | unsure | 0.432 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `8ca47a351e7e445a951c8218ff73b008` | unsure | 0.381 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `be441c3413c54ca88f2996627db770c4` | human | 0.234 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `eb596f0cda184e25bec0289361897b51` | unsure | 0.587 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `e50b1ce6bb6a4076a2dc519cc90b7699` | unsure | 0.480 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ddefd403fefc4f94a6800042131e7faa` | unsure | 0.419 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | `f0c4288eec5f4e9ebfe5927c4123de22` | unsure | 0.555 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `5c21bbbae6434aad8278a1c3ed1c4f45` | unsure | 0.400 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `8c69dc02559c4fd58315a334a82f6665` | unsure | 0.400 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `d531c2061731469ca662690210b7deeb` | unsure | 0.600 | HELD |
| MF06 | malformed | text is emoji only | 200 | `cc16c94480e54fe28140024b2376a61a` | ai | 0.799 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `2b36e7aee5164a3caffdc379710c19a0` | ai | 0.754 | BROKE |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a180a0f68309417a9a9d41872e5fef5d` | unsure | 0.400 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `94c677ddccd2419c861561ddceb80565` | unsure | 0.400 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8edf6a9261694493873e732344baa41e` | unsure | 0.400 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `55c553946ef8490ab89415e5b9940e2a` | unsure | 0.400 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f2a2b9f3c298462a9784dc1e03c7fe36` | unsure | 0.400 | HELD |
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
  "content_id": "f0852ddfb61f4e1aa9131e78d518a69c",
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
  "content_id": "58b104bce56f452b8afa36ee355e0d2a",
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
  "content_id": "d69efc46fb1d486190fe1cd1d1406c2a",
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
  "content_id": "93a80cc06d78406bb789bd7474f391f1",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6705,
  "model_score": 0.6114,
  "style_score": 0.7297,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
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
  "content_id": "400667033c1e4acea778c8c2e55958be",
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
  "content_id": "a2343b9669d54952b6714f9e3dcb169a",
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
  "content_id": "e4d7a7e72b694663861ddc763cca803f",
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
  "content_id": "6e08e34fe1c84cdea2543953d19cc909",
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
  "content_id": "8cbe6b3f9a77450490d065b9b7e3d0e9",
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
  "content_id": "60d121e266f547459ad03ed50ed0ad4d",
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
  "content_id": "812069ccf5f447b68965279e8d61c2f4",
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
  "content_id": "a664e3d63e2b4c00af53703891b76571",
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
  "content_id": "7877df46a0d248b4ab6b945be7422ef9",
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
  "content_id": "cc865bbe2e7b4e648b817b1c6f5139d6",
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
  "content_id": "02fc247b06b549b18854ae6ab004e4b2",
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
  "content_id": "c376e4b5519a461a9c56d15700688895",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6914,
  "model_score": 0.8814,
  "style_score": 0.5014,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
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
  "content_id": "aecd8fc135a44a529adc9a04a4f728f1",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.686,
  "model_score": 0.8816,
  "style_score": 0.4903,
  "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.",
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
  "content_id": "91357d879fff485590eb419c4b7abd15",
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
  "content_id": "8ca47a351e7e445a951c8218ff73b008",
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
  "content_id": "be441c3413c54ca88f2996627db770c4",
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
  "content_id": "eb596f0cda184e25bec0289361897b51",
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
  "content_id": "e50b1ce6bb6a4076a2dc519cc90b7699",
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
  "content_id": "ddefd403fefc4f94a6800042131e7faa",
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
  "content_id": "f0c4288eec5f4e9ebfe5927c4123de22",
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
  "content_id": "5c21bbbae6434aad8278a1c3ed1c4f45",
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
  "content_id": "8c69dc02559c4fd58315a334a82f6665",
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
  "content_id": "d531c2061731469ca662690210b7deeb",
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
  "content_id": "cc16c94480e54fe28140024b2376a61a",
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
  "content_id": "2b36e7aee5164a3caffdc379710c19a0",
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
  "content_id": "a180a0f68309417a9a9d41872e5fef5d",
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
  "content_id": "94c677ddccd2419c861561ddceb80565",
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
  "content_id": "8edf6a9261694493873e732344baa41e",
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
  "content_id": "55c553946ef8490ab89415e5b9940e2a",
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
  "content_id": "f2a2b9f3c298462a9784dc1e03c7fe36",
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
