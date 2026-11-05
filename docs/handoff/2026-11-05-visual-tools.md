# Handoff: a cloud session added visual tools and a script gate (2026-11-05)

For the local Claude Code agent on the build Mac. A cloud session (Linux, no
macOS fonts, no stock bytes, no credentials) built these, tested them there,
and merged them into `main` through
[PR #1](https://github.com/oktayshakirov/video-edit-automation/pull/1).
**Your job:** install what is new, verify it on the Mac with the real fonts,
learn where each thing is documented, and report back to the editor
anything that looks wrong. Nothing here has been seen on the Mac yet.

## 1. Install (once)

```bash
git checkout main && git pull
.venv/bin/python -m pip install -r requirements.txt
```

New pins, all *additions*; in the cloud venv the install changed no existing
package: `playwright==1.63.0`, `pymunk==7.3.1`, `moderngl==5.13.0` (with
`glcontext`, `greenlet`, `pyee`). **Check the voice pins did not move**, then
check the voice itself - every shipped video's narration depends on it:

```bash
.venv/bin/python -m pip freeze | grep -iE "kokoro|onnxruntime|phonemizer"
# expect kokoro-onnx==0.5.0, onnxruntime==1.28.0, phonemizer-fork==3.3.2
.venv/bin/python -m video_automation voices verify
```

Then the three downloads:

```bash
.venv/bin/python -m video_automation vision fetch     # ~320MB, SHA-256 checked
.venv/bin/python -m playwright install chromium       # ~150MB, the capture browser
.venv/bin/python -m video_automation emoji check 🔥 🔒 🔑   # fetches what animates
```

## 2. Verify

```bash
.venv/bin/python -m pytest tests -q
```

In the cloud: 818 passed, 16 skipped. On the Mac expect *more* to run (real
fonts, CGL for the shader tests, the real-model test after `vision fetch`).
Expected skips on the Mac: the tests that need a clip in the local Pexels
cache when it is not there, and the two read-along sample scripts that need
the `audiobook_automation` sibling package. Anything else skipping is worth
a look.

Then look at everything new with the real fonts - this is the part the
cloud could not do:

```bash
PYTHONPATH=. .venv/bin/python tools/visual_demo.py
open ~/Desktop/visual-demo
```

It renders 14 short clips (~3 min). What to check in them:

- **behind-16x9 / behind-9x16**: the word sits across the top of the head,
  readable. The 38% cover cap was measured with a stand-in font; DIN
  Condensed is narrower, so the word comes out bigger and the cover may
  differ. If the word lands across a face, note the cover the beat chose
  (`Behind(...).cover`) for the editor.
- **parallax-vs-flat**: right half moves in depth, no tearing at tower edges.
- **pile-***: coins stack, the trapdoors swing and the pile pours out.
- **emoji-grid**: fire and lock animate (Noto style), the key stays Apple.
- **shader-***: bloom, leak, aberration, vignette, each visible but not loud.
- **screencap-***: the camera glides and rings two passages of the
  seed-phrase article (rendered locally from `~/Coding/crypto-wiki`).

**Byte-identity, if you have time.** The cloud checked that a still with
none of the new options renders exactly as before (36 frames, both
formats). On the Mac, the stronger check is to re-render one approved Short
at the merge's parent and at `main` and compare frames - any difference
there is a regression to report, not to fix silently.

## 3. What is new, and where it is documented

Every rule lives in one doc; read the section before using the tool.

| Tool | How a script uses it | Doc |
| --- | --- | --- |
| Depth parallax on a still | `Shot(image=..., parallax=1.0)` | `footage.md`, "A still can move in depth" |
| Room dims, subject stays | `Shot(image=..., isolate=1.0)` | same |
| Head breaks the photo frame | `Shot(image=..., pop=True)` (not with parallax) | same |
| Word behind the subject | `Shot(graphic="behind", payload=(photo, word, line))` | `beats.md`, "`behind`" |
| Subject in front of a cover headline | `im = T.subject_front(im, before)` | `thumbnails.md`, "The subject in front of the headline" |
| Coins pour in / drain out | `Shot(graphic="pile", payload=(drops, title, drain))` | `beats.md`, "`pile`" |
| Animated emoji icons | `render_long(..., animated_emoji=True)` | `beats.md`, "Animated emoji icons" |
| GPU effects on a shot | `Shot(shader="bloom" / ("leak", 0.6) / [...])` | `design.md`, "GPU effects on a shot" |
| A real web page on screen | `video_automation screencap grab / clip` | `footage.md`, "A real page" |
| Script rule gate | `tools/script_check.py long.py short.py` | `workflow.md` step 2 |

Code: `core/vision.py` (models, cache), `core/stillfx.py` (depth move,
isolate, pop), `crypto/shots.py` (`PhotoShot._draw_fx`; the original
`draw` path is untouched), `longform/beats/behind.py`, `beats/pile.py`,
`core/emoji_anim.py`, `core/shaderfx.py`, `core/screencap.py`,
`longform/thumb.py` (`subject_front`), `tools/script_check.py`,
`tools/visual_demo.py`. Test-only: `core/fontshim.py` + `tests/conftest.py`
(answers missing macOS fonts so the suite runs on Linux; a no-op on the Mac).

Also changed: the 56-line "What every build draws by default" block moved
from both article skills into `workflow.md` (one copy); the build skills
point at the new tools; `docs/video/README.md` and `tests/README.md` list
what really exists, and `tests/test_docs.py` keeps them true.

## 4. Decisions for the editor (not taken here)

- **Licences to confirm on the source pages**: Noto Emoji Animation is
  believed CC BY 4.0 (the credit line is added automatically); Depth
  Anything V2 is Apache-2.0 for the *Small* model only - never swap in
  Base/Large/Giant (CC-BY-NC).
- **`script_check --all` flagged three shipped scripts** that broke a rule
  already written when they were made: `crypto-long/vitalik-ethereum.py`
  ("So, here is the question."), `tinnitus-long/pulsatile-tinnitus.py` (a
  "subscribe" outro), `quiz-tinnitus/tinnitus-myths-vs-reality.py` (speaks
  "CBT"; an option says "can help"). Shipped videos are not re-cut by this;
  the editor decides whether the scripts change for future copies.
- Whether to commit fetched emoji WebPs (CC BY, ~200KB each) for
  reproducibility, or leave them in `~/.local/share/video-automation/emoji`.
- First real uses: none of the new tools is in a shipped script yet. The
  first pair that uses one should be looked at with that tool in mind.

## 5. Known limits

- `screencap` was only ever run against local pages: external sites were
  blocked from the cloud session. The first real capture should be watched.
- *(Fixed in a follow-up the same day.)* Three scripts - both
  `gta-6-crypto` scripts and `crypto-long/what-are-memecoins` - drew and
  saved their ticker cards on import, so every gate that imported them
  rewrote the files; under the test font shim one import overwrote the
  committed `squid.png` with a stand-in face (restored). They now draw in a
  `cards()` function that `main()` calls, with the same `ticker_card` calls
  and arguments, so the cards are unchanged; the import test fails any
  script that saves on import, and `ticker_card` refuses to write in a
  process that used stand-in fonts. Rule: `workflow.md` step 3. **Check on
  the Mac:** render one of the three (or just call its `cards()`) and
  confirm `git status` shows `squid.png` unchanged.
- Animated emoji only cover some emoji; the rest stay Apple's style. Caption
  emoji in Shorts are not animated (they are pre-rendered PNGs).
- GPU effects are deterministic on one machine but not across GPUs.
- `pop=` and `parallax=` refuse to share a shot.

## 6. When you are done

Tell the editor what passed, what looked wrong in the demo clips (with the
clip name and second), and anything you had to change. Record lessons in the
narrowest doc per `docs/video/README.md`, in the same commit as any fix.
This file can be deleted once the review is done - its content lives in the
docs above.
