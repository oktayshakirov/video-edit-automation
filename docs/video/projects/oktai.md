# OktAI - Oktay's own channel

**"OK, AI. Let's build."** The channel teaches what we build with AI and how
it makes money, shown from the inside. The plan, the video slate, links and
affiliates are in `docs/oktai-channel-plan.md`; the ChatGPT prompts for the
logo and banner in `docs/oktai-brand-prompts.md`. This page is only how a
build differs from the crypto and tinnitus pairs - everything else
(`workflow.md`, `longform.md`, `shorts.md`, `beats.md`) applies as written.

## What is different

| | Crypto / Tinnitus | OktAI |
| --- | --- | --- |
| Voice | Kokoro (`mia`) | **Oktay's recording** (`core/recorded.py`) |
| Face | none | **the camera box** at chosen moments (`core/facecam.py`) |
| Brand | `CRYPTO` / `TINNITUS` | `OKTAI` in `core/brand.py` |
| Source | an article | something we built, measured or sourced |
| Pair | long + Short | long + Short, both read in one sitting |

## The look

The portfolio's (oktayshakirov.com): the `oktai-night` backdrop (near-black
sky, two soft blooms, a few dim twinkling stars - a full starfield behind
type was rejected on tinnitus), the portfolio gold `#ffdb70` as `primary`,
and the "oktAI" wordmark ("okt" white, "AI" gold, Poppins SemiBold). Both
assets are drawn by `tools/oktai_brand.py`; the Poppins files are the
portfolio's, in `assets/brand/oktai/fonts`. When the ChatGPT logo arrives,
replace `assets/brand/oktai/wordmark.png` - the brand points at the file.

**Not yet per brand:** captions and beat type are still the engine's global
Futura / Avenir. Poppins in the drawn beats is a follow-up.

## Recording

What Oktay sends: **one file per script** (the long form and the Short each
get their own), voice and face in the same take when possible.

- Read the script as written, a sentence per breath. **On a mistake, say the
  whole sentence again** - the last good take of each sentence is kept, and
  false starts, re-reads and asides between takes are cut.
- Mic 15-20 cm away, soft room. Camera at eye level, light from the front.
- Voice on a separate mic is fine: pass `Recording(audio, video=camera_file)`
  and the face is synced to the voice by cross-correlating the camera's own
  sound (`facecam.sync_offset`).

## Building with a recording

```python
from video_automation.core.brand import OKTAI
from video_automation.core.recorded import Recording, sidecar
from video_automation.core import facecam

REC = Recording(Path("~/Movies/oktai/job-search-long.mov"))
made = render_long(SECTIONS, out, work, brand=OKTAI, voice=REC, ...)
```

`voice=` takes a `Recording` anywhere it takes a profile name, the Short
(`render_crypto_short(..., voice=REC, brand=OKTAI)`) included. A chapter
card's spoken title is a sentence too, so it has to be in the recording.

What happens, in `core/recorded.py`'s docstring: Whisper (large v3 turbo, on
MLX, offline, run from `create-song-automation`'s venv, cached by file hash)
transcribes every word with its time; each sentence is matched to its takes;
the kept takes are cut and joined with the real pauses (capped) or the
recording's own room tone; then a light clean-up and `loudnorm` to -14 LUFS,
where the Kokoro reads sit. Captions are timed by the words actually spoken.

**Read the report before the review.** `NAME.<hash>.report.txt` next to the
recording lists, per sentence, the take used and every word said that the
script does not have (or the reverse). A changed word is in the voice and not
in the captions until the script is edited to match. A sentence that was
never said stops the build with the list to re-record.

## The camera box

After the render, on the finished MP4:

```python
facecam.apply(made["video"], out.with_name(out.stem + "-cam.mp4"),
              sidecar(REC, [list(s) for s in sentences], "edl.json"),
              on=[("this one cost me a week", 4.0)])
```

On by default for the hook (first ~3 s) and the last line; `on=` adds a
phrase (as its caption starts) and how long to stay; `cue_list=` gives exact
seconds. The face is cut with the voice's own edit file, so the lips match;
a gap filled with room tone shows a still frame. 16:9: bottom right, 320 px,
above the control bar. 9:16: top right, 300 px, left of the right rail.
**Off while a screen or a number has to be read** - the box would cover the
evidence (`docs/oktai-channel-plan.md`, "The camera box").

## Links in scripts

A long form names a tool when it is on screen and says the referral line
once there; the Short does not pitch. The description carries the links and
the disclosure. The rules are in `docs/oktai-channel-plan.md`, section 7.
