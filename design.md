# Provenance Guard - Milestone 1 notes

Written before building anything.

## The path

It's in the README under "What This Does". Basically: text comes in and gets checked, both signals run, they get combined, a label gets picked, it's logged, and the answer goes back. Appeals are separate. They just look up the `content_id` in the log.

## The two signals

**Signal one (`detector.py`)** asks how predictable the text is to gpt2. Blind spot: it can't tell "written by AI" from "written plainly". Simple human writing looks like AI to it, and fancy or edited AI writing can look human. It also only reads about the first 400 tokens.

**Signal two (`stylometry.py`)** looks at shape: sentence length spread, unique word ratio, punctuation. Blind spot: it has no idea what the text means. Typos, chopped up sentences, or a pasted quote change the numbers without changing anything real.

They break in different ways (one on word choice, one on shape), so a trick that fools one usually doesn't fool the other. That's probably why we need two.

## The false positive

Say a non-native English speaker writes a plain 250 word essay. Short sentences, simple words they're sure about. They wrote all of it themselves.

1. It hits `/submit`, text is fine, so it goes through.
2. Signal one thinks it's very predictable. I'd guess `model_score` is high, like 0.8+, but I haven't tested it yet so that's a guess. I need to check in Milestone 3.
3. Signal two sees even sentences and a small vocabulary, so `style_score` is probably high too. The annoying part is both signals are wrong for the same reason, so they agree and nothing catches it.
4. `combine_signals` gives a high score, probably over `AI_THRESHOLD` (0.65).
5. The writer gets the high-confidence AI label. Basically being told they cheated when they didn't.
6. It's logged as `decided`.
7. Their only option is `POST /appeal` with the `content_id` and their reasoning. It goes to `under_review` and they get a confirmation. Nothing re-checks it automatically, so a person has to actually read it.

What this means for Milestone 4: the two signals agreeing doesn't mean they're right, since they share the same weakness. So I should keep `AI_THRESHOLD` high, make the "unsure" band wide, and word the AI label so the writer can still argue back.

## Endpoints

### `POST /submit`

Goes in (JSON):

| Field | Type | Required | Notes |
|---|---|---|---|
| `text` | string | yes | Can't be empty (after trimming). Max length goes in `config.py`, I'll pick it in Milestone 3. |
| `creator_id` | string | yes | Can't be empty. Just used for logging. |

Comes out on success (200):

| Field | Type | What it is |
|---|---|---|
| `content_id` | string | Unique id. `/appeal` needs it. |
| `guess` | string | `"ai"`, `"human"` or `"unsure"` |
| `confidence` | number 0-1 | The combined score. Higher = more likely AI. Careful, it is NOT "how sure we are about the guess". |
| `label` | string | The full sentence the writer sees |
| `model_score` | number 0-1 | Signal one, higher = more AI |
| `style_score` | number 0-1 | Signal two, higher = more AI |

Errors (400) look like `{"error": "bad_request", "message": "..."}`. That happens when the body isn't a JSON object, `text` or `creator_id` is missing / not a string / empty, or `text` is too long.

### `POST /appeal`

Goes in:

| Field | Type | Required | Notes |
|---|---|---|---|
| `content_id` | string | yes | Has to already be in the log |
| `reasoning` | string | yes | Can't be empty |

Comes out on success (200):

| Field | Type | What it is |
|---|---|---|
| `content_id` | string | Same id back |
| `status` | string | Always `"under_review"` |
| `message` | string | Plain confirmation for the writer |

Errors: 400 `{"error": "bad_request", ...}` if a field is missing or empty. 404 `{"error": "not_found", ...}` if the `content_id` isn't in the log. An unknown id should never give a 200.

### Could someone else build from this?

I think mostly yes. The things I would've had to ask myself were what `confidence` means (combined score, higher = AI), what happens with a bad id (404), and what statuses exist (`decided`, `under_review`). Still not decided: the max text length. That's a Milestone 3 thing.
