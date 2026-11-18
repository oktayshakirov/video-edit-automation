# Song: the karaoke music video

A finished song from `~/Coding/create-song-automation` (lyrics and render), cut as a lyric video: 16:9 for YouTube
and the **whole song** at 9:16 for Shorts, TikTok and Reels (the user's call
on "Come Back at Five", 2026-11-06 - not a 45-second excerpt). The first one
is `projects/song/come-back-at-five/`; the second `projects/song/gta-flu/` (2026-11-17).
Copy the newer one's scripts for the next.

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
`~/Coding/create-song-automation/.venv`, demucs in
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

## What the second song added (GTA Flu, 2026-11-17)

- **The Short can be its own cut.** The user wanted the Short without the
  middle hook. The audio cut lives in the song repo's tooling; `video.py`
  takes the cut (`CUT_A`, `CUT_LEN`, `CUT_SUNG`) and maps every time across
  it with `T()`. Drop the lines that *start* inside the removed span from
  where the vocal is muted, not from the join: hook 2's first words began
  0.4s before the join and showed up in the Short.
- **A looping Short has no end card.** Its outro call ends on "call ended"
  beeps that lead back into the intro's call; the long one keeps a title card.
- **Lines the take garbles are shown as the take sings them**, timed by hand
  from Whisper over the full mix, when the vocal stem loses a whole section
  (the final hook here). A hand-timed line can be kept out of forced
  alignment (`"keep"` in `EDITS`): the aligner dragged "Or this year" 1.3s
  late, onto the drop.
- **Re-theme by palette, not by copying the subject's look.** An 80s
  Miami-dusk palette and a drawn synthwave sun said "Vice City" without any
  of the game's art, logo or characters (Lucia is a name on a card).
- **Check the layout against the karaoke at both sizes.** Labels under a
  centred prop collided with a two-row lyric in 16:9, and a split-screen in
  9:16 put its lower half's labels under the lyric; both came from stills,
  before the full render (about 3 minutes a format at 30 fps).
- **Round 2 notes from the user (2026-11-18), now the defaults:**
  - *Plain karaoke.* Avenir Next Heavy with a sweep cutting through letters
    "looked bad". SF Pro Bold (`/System/Library/Fonts/SFNS.ttf`, variation
    `Bold`), whole words change colour (sung white, current pink, rest solid
    grey), a thin dark outline, no bounce, no next-line preview.
  - *Say who is talking.* Dialogue lines get a speaker tag above the lyric
    ("ME -> BOSS"), and the people in the scene get name tags.
  - *Real subject imagery, via cutouts.* The user wants the real thing (here
    official GTA VI screenshots) and pointed at `core.vision.cutout` for
    graphics: a character cut out on a card or an end card, a real location
    as a photo, a dim screenshot as a backdrop. Keep the source images out
    of the repo (`~/.cache/video-automation/song/<slug>/`). Rockstar's fan
    policy is non-commercial and excludes music videos, so tell the user the
    claim risk once; it is their call.
- **Nothing on screen for less than a second** (the user, 2026-11-18: "some
  text or emoji pops up half a second before the next frame replaces it",
  a recurring fault). `video.py` enforces it: `render_frame` records the
  scene's start and end, `at(t0)` pulls a prop's start early enough to hold
  `MIN_HOLD` (1.0s) before the scene ends (never before it starts), and
  `shows(t0)` hides anything that still cannot hold it. Ad-lib stickers start
  on the line's last word and are dropped when the next line sings the same
  words ("Or Friday (or this year)" before "Or this year"). Phone-state
  changes ("Call ended") go through `shows()` too.
  **Check:** `video.py long --audit` / `short --audit` samples the video at
  5 fps and lists everything the rule hid, with how long it would have been
  up. Read it before every full render; a hidden punchline gets re-timed, a
  hidden ad-lib can go.
