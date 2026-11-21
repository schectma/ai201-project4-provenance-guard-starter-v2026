| Criterion | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|
| 1. Every failed request logged (8 of 8) | 8/8 | 8/8 | 8/8 | MET |
| 2. Timeout -> fast 504, logged (5 of 5) | 5/5 | 5/5 | 5/5 | MET |
| 3. Recovery after timeouts (3 of 3) | 3/3 | 3/3 | 3/3 | MET |
| 4. Warm latency (median<=3000, max<=6000 ms) | median 194ms max 207ms | median 188ms max 199ms | median 190ms max 231ms | MET |
| 5. Logged duration honest (9 of 10) | 10/10 | 10/10 | 10/10 | MET |

```
trial 1: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 20ms', '504 15ms', '504 13ms', '504 8ms', '504 20ms'] | c3 ['200 204ms', '200 195ms', '200 186ms'] | durations [180, 180, 180, 198, 202, 190, 200, 207, 206, 183] walls [183, 182, 182, 201, 204, 193, 202, 209, 208, 186]
trial 2: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 14ms', '504 12ms', '504 13ms', '504 21ms', '504 23ms'] | c3 ['200 191ms', '200 192ms', '200 195ms'] | durations [186, 188, 190, 192, 199, 174, 177, 196, 188, 183] walls [189, 191, 192, 195, 201, 176, 180, 198, 190, 186]
trial 3: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 9ms', '504 14ms', '504 8ms', '504 23ms', '504 14ms'] | c3 ['200 173ms', '200 184ms', '200 184ms'] | durations [180, 174, 231, 181, 170, 190, 201, 224, 190, 194] walls [182, 176, 234, 183, 173, 193, 203, 226, 193, 196]
```

Sample log lines (trial 1):
```
{"timestamp": "2026-11-21T23:38:33+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": null, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:38:33+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": 0, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:38:33+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": 3, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:38:41+00:00", "content_id": "c5301f9b163348639de74e78c853d5b2", "creator_id": "t", "guess": "unsure", "model_score": 0.2336, "style_score": 0.7651, "combined_score": 0.4994, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 636, "duration_ms": 201.6}
{"timestamp": "2026-11-21T23:38:42+00:00", "content_id": "df6c11abcac649d0ab187e2e8e339b36", "creator_id": "t", "guess": "unsure", "model_score": 0.2625, "style_score": 0.6627, "combined_score": 0.4626, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 627, "duration_ms": 193.0}
{"timestamp": "2026-11-21T23:38:42+00:00", "content_id": "02c08aa092524761a75451b8f54cd5f4", "creator_id": "t", "guess": "unsure", "model_score": 0.295, "style_score": 0.6948, "combined_score": 0.4949, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 630, "duration_ms": 183.7}
```