| Criterion | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|
| 1. Every failed request logged (8 of 8) | 8/8 | 8/8 | 8/8 | MET |
| 2. Timeout -> fast 504, logged (5 of 5) | 5/5 | 5/5 | 5/5 | MET |
| 3. Recovery after timeouts (3 of 3) | 3/3 | 3/3 | 3/3 | MET |
| 4. Warm latency (median<=3000, max<=6000 ms) | median 173ms max 192ms | median 174ms max 188ms | median 183ms max 216ms | MET |
| 5. Logged duration honest (9 of 10) | 10/10 | 10/10 | 10/10 | MET |

```
trial 1: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 22ms', '504 13ms', '504 17ms', '504 6ms', '504 11ms'] | c3 ['orphan_cpu=11.22s', '200 185ms', '200 173ms', '200 179ms'] | durations [181, 172, 168, 173, 173, 173, 192, 167, 174, 174] walls [184, 174, 170, 175, 176, 175, 195, 170, 177, 176]
trial 2: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 8ms', '504 16ms', '504 13ms', '504 7ms', '504 23ms'] | c3 ['orphan_cpu=10.52s', '200 183ms', '200 186ms', '200 199ms'] | durations [174, 183, 174, 169, 172, 173, 178, 188, 174, 174] walls [176, 185, 176, 171, 175, 175, 180, 190, 176, 177]
trial 3: c1 ['400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries', '400/1 entries'] | c2 ['504 4ms', '504 19ms', '504 13ms', '504 7ms', '504 10ms'] | c3 ['orphan_cpu=10.80s', '200 184ms', '200 185ms', '200 177ms'] | durations [212, 178, 176, 198, 189, 216, 187, 176, 178, 175] walls [215, 180, 178, 201, 191, 218, 189, 179, 181, 178]
```

Sample log lines (trial 1):
```
{"timestamp": "2026-11-21T23:40:50+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": null, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:40:50+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": 0, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:40:50+00:00", "creator_id": "t", "event": "rejected", "status": "rejected", "reason": "bad_request", "http_status": 400, "input_chars": 3, "duration_ms": 0.1}
{"timestamp": "2026-11-21T23:40:58+00:00", "content_id": "34fba143ecba4e8db76c9fce147b9fa0", "creator_id": "t", "guess": "unsure", "model_score": 0.2336, "style_score": 0.7651, "combined_score": 0.4994, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 636, "duration_ms": 182.4}
{"timestamp": "2026-11-21T23:40:59+00:00", "content_id": "2b21525255c24808b05c8a0f6ddcb590", "creator_id": "t", "guess": "unsure", "model_score": 0.2625, "style_score": 0.6627, "combined_score": 0.4626, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 627, "duration_ms": 170.3}
{"timestamp": "2026-11-21T23:40:59+00:00", "content_id": "ac29222e7bd24f40a40deb21763d6628", "creator_id": "t", "guess": "unsure", "model_score": 0.295, "style_score": 0.6948, "combined_score": 0.4949, "label": "We can't tell whether this was written by a person or by AI. That doesn't mean there's a problem, and you don't need to do anything.", "status": "decided", "input_chars": 630, "duration_ms": 176.7}
```