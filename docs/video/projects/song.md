# Song: the karaoke music video

A finished song from `~/Coding/create-song-automation` (lyrics) and
`~/Coding/song-automation` (render), cut as a lyric video: 16:9 for YouTube
and the **whole song** at 9:16 for Shorts, TikTok and Reels (the user's call
on "Come Back at Five", 2026-11-06 - not a 45-second excerpt). The first one
is `projects/song/come-back-at-five/`; copy its two scripts for the next.

No skill drives this yet. The pieces:

| file | does |
| --- | --- |
| `timing.py` | every sung word's start and end in the final mix, written to `timing.json` (committed) |
| `video.py` | one drawn scene per lyric line, the karaoke on top; `long` or `short`, `--still S` for a frame |

Output goes to `~/Desktop/songs/video/`.

## Timing the words

Whisper over the full mix mishears through the 808s, so `timing.py`
separates the vocal first (demucs `htdemucs`), transcribes that with word
timestamps, then **aligns Whisper's words to the sheet's words** - the
screen shows the lyric, not "Limit reach" or "like a Jedi".

- **Align globally, not greedily** (2026-11-06). `difflib`'s longest-match
  paired the first hook with the second chorus and skipped the 50 seconds of
  verse between them. A Needleman-Wunsch alignment cannot, because every
  token on both sides is placed in order.
- **A line Whisper drops on the stem is often there on the mix.** Two lines
  had no words on the vocal stem; a Whisper pass over the mix for that window
  found both. They go in `EDITS` by hand, with the reason.
- **Show what the take sings** (the user's note, 2026-11-06: "only show the
  lyrics"). Where the take drops words ("refactor everything"), merges two
  sheet lines, or sings a line twice, `EDITS` puts the sung words on screen
  in the sheet's spelling, and the user's ear wins over the sheet ("B-Bye").
  **A repeat is its own line**: one line spanning both passes sat half-lit
  waiting for the second.
- **Whisper places lines, forced alignment times words.** Whisper's word
  times ran late and stretched - the sweep lagged the voice and lines left
  unlit. wav2vec2 (`torchaudio` `WAV2VEC2_ASR_BASE_960H`, `forced_align`)
  fits the known words to the vocal stem. **Align a run of lines in one
  pass, ad-libs included**: aligned one line per window, first and last
  words reached into the neighbours and lines overlapped by ~0.3s.
- **The sweep:** each word from its own start to the next word's start,
  0.08s ahead of the voice; a line comes in 0.3s early but never before the
  previous one is fully sung, and leaves as the next comes in.

The helpers live outside this repo's venv on purpose: Whisper in
`~/Coding/song-automation/.venv`, demucs in
`~/.local/share/song-automation/sepvenv` (it borrows the ACE-Step engine's
torch). **Not in the session scratchpad** - it is wiped between days, and the
first set of venvs went with it.

## The look (decided with the user, 2026-11-06)

- **Neutral, no watermark.** A song is not a crypto or tinnitus video. The
  scripts build their own `Brand` and register it in `BRANDS` at runtime, so
  the beats that look a brand up by name still work, with no logo.
- **No product logo, nothing copied from the product's interface.** The chat
  is a generic window that names the product in our own type. The song repo's
  `docs/originality.md` forbids the logo and anything that reads as official,
  and a recreated interface would read exactly that way.
- **Karaoke:** the line in heavy type, sung words white, the word being sung
  swept in the accent, the rest dimmed; ad-libs as a sticker once the line is
  sung; the next line small underneath in 16:9 only. A dark band sits under it
  so it reads over photos. **No drop shadow** on the type (the user: it looks
  bad). In 9:16 it may take three rows.
- **The Short is centred on the frame**, not on the safe box left of the
  button rail (the user's note, 2026-11-06: it read as pushed left). The
  vertical limits still hold.
- **It ends like the channels' Shorts**: `overlay.TvOff` over the last
  0.55s and `sfx.tv_off` mixed into the soundtrack under it.

## What each tool was good for

- **Animated emoji carry most scenes.** Check every one first
  (`python -m video_automation emoji check ...`): 🐴 🔄 📅 💨 👔 🕔 do not
  animate; 🐎 does.
- **`behind` needs a subject whose head leaves the word room.** "GRASS" over
  the sky above a man lying in grass, and "OUTSIDE" across a sunflower field,
  read whole. "FIX?" and then "THE FIX" behind a manager whose head and
  shoulders filled the top third were never read - that shot became the photo
  pushing in with a stamped "WHERE'S THE FIX?".
- **Draw a moving shape at 3x and reduce it.** The clock drawn straight onto
  the frame was aliased and its 808 swell stepped whole pixels; on its own
  3x tile, reduced with Lanczos, it is crisp. Anything that scales per frame
  needs the same.
- **Give every icon its own spot.** Flames over the laptop, emoji touching the
  clock's rim and a brain over its label all read as clutter; side by side
  with a gap they read as a sentence.
- **A terminal shrinks its font to its longest row** - the 16:9 window cut a
  command in half at 0:33.
- **Avenir and Menlo lack symbols.** ⚠ ↻ and the braille spinner ⠋ draw as
  boxes. Use the emoji (⚠️ 🔄) or plain ASCII in a terminal.
- **`shaderfx` aberration on the hits** (the drop, the weekly-limit banner)
  with a short camera shake; bloom and leak on "the graphics are insane".
