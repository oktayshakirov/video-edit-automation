# The tests

**They exist because two bugs in one afternoon were found by rendering a video
and looking at it.** `partial()` was called with keyword arguments it does not
take, and the map pin was anchored 34px from the point it marked. Both are the
kind of thing a machine notices instantly and a person notices on the third
viewing, if at all.

So the rule here is narrow: **test what can be checked without rendering a
video.** Nothing in this directory synthesises speech, encodes an MP4 or
reaches the network. A full build is minutes; these are under a second, which
is the only reason they will actually get run.

    .venv/bin/python -m pytest tests -q

What they cover:

| file | what it protects |
| --- | --- |
| `test_beats.py` | every beat in `BEATS` renders, and `item_count` agrees with it |
| `test_transitions.py` | `push` stays byte-identical; every mode returns a frame |
| `test_narration_cache.py` | the cache key, and the shadowing bug that poisoned it |
| `test_chrome.py` | the navigation overlays, and the cue collision rule |

**What they deliberately do not cover** is whether anything *looks* right.
A beat that renders a legible frame and a beat that renders a grey rectangle
both pass here. Looking at the render is still the job; these only make sure
the things that cannot be seen at a glance stay true.
