| Criterion | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|
| 1. Every failed request logged (8 of 8) | 8/8 | 8/8 | 8/8 | MET |
| 2. Timeout -> fast 504, logged (5 of 5) | 5/5 | 5/5 | 5/5 | MET |
| 3. Recovery after timeouts (3 of 3) | 3/3 | 3/3 | 3/3 | MET |
| 4. Warm latency (median<=3000, max<=6000 ms) | median 176ms max 182ms | median 170ms max 180ms | median 174ms max 195ms | MET |
| 5. Logged duration honest (9 of 10) | 10/10 | 10/10 | 10/10 | MET |

```
trial 1: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 21ms', '504 12ms', '504 12ms', '504 9ms', '504 9ms'] | c3 ['orphan_cpu=10.31s', '200 194ms', '200 187ms', '200 186ms'] | durations [173, 173, 181, 181, 176, 174, 173, 177, 175, 182] walls [176, 175, 184, 183, 178, 176, 175, 180, 177, 184]
trial 2: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 7ms', '504 19ms', '504 12ms', '504 12ms', '504 8ms'] | c3 ['orphan_cpu=12.28s', '200 195ms', '200 172ms', '200 178ms'] | durations [168, 164, 167, 159, 168, 175, 171, 173, 174, 180] walls [170, 166, 170, 162, 171, 177, 174, 175, 176, 183]
trial 3: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 7ms', '504 17ms', '504 8ms', '504 7ms', '504 20ms'] | c3 ['orphan_cpu=10.23s', '200 181ms', '200 191ms', '200 163ms'] | durations [172, 170, 174, 177, 181, 195, 182, 170, 173, 172] walls [175, 172, 177, 179, 184, 197, 185, 172, 175, 174]
```

Sample log lines (trial 1):
```
{"timestamp": "2026-11-21T23:39:44+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": null, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:39:44+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": 0, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:39:44+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": 3, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:39:52+00:00", "content_id": "ce50da7d8cf0408693dddea3def8db7c", "creator_id": "t", "guess": "unsure", "model_score": 0.2336, "style_score": 0.7651, "combined_score": 0.4994, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 636, "duration_ms": 191.1}
{"timestamp": "2026-11-21T23:39:52+00:00", "content_id": "7b785b30a425421cbb4f9d6bc3b45d3b", "creator_id": "t", "guess": "unsure", "model_score": 0.2625, "style_score": 0.6627, "combined_score": 0.4626, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 627, "duration_ms": 185.1}
{"timestamp": "2026-11-21T23:39:52+00:00", "content_id": "287c324009a54db485424dfdbc6ec7fe", "creator_id": "t", "guess": "unsure", "model_score": 0.295, "style_score": 0.6948, "combined_score": 0.4949, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 630, "duration_ms": 183.4}
```