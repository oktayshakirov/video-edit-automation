# The tests

**They exist because two bugs in one afternoon were found by rendering a video
and looking at it.** `partial()` was called with keyword arguments it does not
take, and the map pin was anchored 34px from the point it marked. Both are the
kind of thing a machine notices instantly and a person notices on the third
viewing, if at all.

So the rule here is narrow: **test what can be checked without rendering a
video.** Nothing in this directory synthesises speech, renders a video or
reaches the network (`test_hdr` encodes a two-frame lavfi clip, which is the
one exception and takes milliseconds). A full build is minutes; the suite is
about half a minute, which is the only reason it will actually get run.

    .venv/bin/python -m pytest tests -q

**It runs off the Mac too** - in CI on every push (`.github/workflows/tests.yml`)
and in a cloud session after `tools/cloud_setup.sh` (`docs/video/cloud.md`).
`conftest.py` installs `core.fontshim`, which answers the missing macOS fonts
with free ones; no test asserts a typeface. What needs the Mac skips with the
reason: the Kokoro weights, the stock cache, the crypto-wiki checkout, a
script that saves a card at import.

What they cover:

| file | what it protects |
| --- | --- |
| `test_beats.py` | every beat in `BEATS` renders, landscape and portrait, on both brands, and `item_count` agrees with it |
| `test_breath.py` | the breathing ring's phases agree, long form and Short, on every pattern |
| `test_card_cues.py` | chapter cards and reels sound the same in every Short, the quiz too |
| `test_chrome.py` | the navigation overlays, and the cue collision rule |
| `test_filmfx.py` | the film surface's per-shot arrangement |
| `test_guard.py` | a render refuses a full disk and aborts on critical memory pressure |
| `test_hdr.py` | SDR-to-HLG keeps colour, and the SDR renderers refuse an HLG clip |
| `test_looks.py` | every session look is a loop that closes |
| `test_meta.py` | a disclaimer becomes the notice card; a routing line asks by kicker |
| `test_narration_cache.py` | the cache key, and the shadowing bug that poisoned it |
| `test_readalong.py` | the read-along picks the scripted gaps, not the voice's own pauses |
| `test_reel.py` | the `reel` beat's dives into and out of a card, and `post`'s highlighter on every frame |
| `test_samples.py` | the tinnitus sound samples: synthesis, placement and the bed dip |
| `test_script_check.py` | `tools/script_check.py` flags what the docs forbid and passes the honest sentence - and every project script still imports |
| `test_search_opener.py` | the Search opener types on the shared rhythm |
| `test_sfx_kits.py` | the per-site sound kits, and the cue set no kit may touch |
| `test_special_cuts.py` | where the glitch and TV-static cuts are placed |
| `test_spotlight_ambience.py` | the spotlight's box fits the content; place-sound stays restrained |
| `test_transitions.py` | `push` stays byte-identical; every mode returns a frame |
| `test_docs.py` | the docs and skills point at files that exist, and this table lists every test |

**What they deliberately do not cover** is whether anything *looks* right.
A beat that renders a legible frame and a beat that renders a grey rectangle
both pass here. Looking at the render is still the job; these only make sure
the things that cannot be seen at a glance stay true.
