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

## The run

`/video-oktai` (`.claude/skills/video-oktai/SKILL.md`): topic, research,
both scripts and a Kokoro *draft* render, then `tools/oktai_script.py
<name>` hands Oktay the page to read and the run stops. When the recordings
arrive in `~/Movies/OktAI/<name>/` (`long.*`, `short.*`, optional
`long-cam.*` / `short-cam.*`), `tools/oktai_recording_check.py`
checks them and `video_automation.oktai.build_long` / `build_short` build the
pair with his voice and the camera box.

## The look

The portfolio's (oktayshakirov.com): the `oktai-night` backdrop (near-black
sky, two soft blooms, a few dim twinkling stars - a full starfield behind
type was rejected on tinnitus), the portfolio gold `#ffdb70` as `primary`,
and the "oktAI" wordmark ("okt" white, "AI" gold, Poppins SemiBold).
**No watermark on the videos** (`Brand.watermark=False`, the editor's call
2026-11-21): the marks exist to promote a domain, and this channel is the
person. The wordmark is for covers and cards. Both
assets are drawn by `tools/oktai_brand.py`; the Poppins files are the
portfolio's, in `assets/brand/oktai/fonts`. When the ChatGPT logo arrives,
replace `assets/brand/oktai/wordmark.png` - the brand points at the file.

**The picture rules from the third draft (the editor, 2026-11-23):**

- **Cards show footage, never a text placeholder** - a robot for "the same
  robot voice", a stopwatch for "the first seconds" (`reel` docstring). A
  text card is the exception when nothing else can show it.
- **Text screens are polished**: a hand-set headline is
  `Shot(graphic="chapter", payload=(text, None, "headline", None, None))` -
  typed, no rule over it, no film dust (`filmfx.kind`).
- **The sky is the portfolio's** (`painted.OKTAI_NIGHT`): near-black, a
  three-size starfield, three falling stars a 24 s loop.
- **Yellow subtitles under the long form** (`oktai.SUBTITLES`,
  `render_long(subtitles=)`), 44 px, at the bottom.
- **Every red or green mark has its sound** (`sfx.verdict_wrong` /
  `verdict_right`).
- **Our own videos as they sit on YouTube** - `window=("youtube", title,
  "Channel · N views · age", avatar)`, numbers read with yt-dlp that day -
  instead of a bare clip with a label.
- **Claude Code at work**: `screenplay.claude_chat(prompt, reply, tools)` in
  place of some plain terminals - the prompt said plainly, real files and
  sizes. The channel's point is that a person with AI beats either alone:
  say "Claude made it", not "I made it".
- **Cards are read, not glanced at**: a strip walked on a path travels at
  1.0 s; a list of five is a row of tiles (`logos` with stills,
  `oktai.still`), not a strip; a lone logo is capped (it went soft at full
  size); a stat can show its count as pips (`stat` payload's fifth item).
- **Stock faces only as the marked mistake, and then really stock**: people
  who smile into the lens, where the line says "smiling strangers".
- **Site screens show the videos**: the app and audiobook cards are hidden
  (`PROMOS` in the project), and ad slots collapse everywhere.

**From the third draft's review (2026-11-23):**

- **An example is framed as one.** A picture of an old video, a re-drawn
  sentence, the sound waves "made for this one" sit in a `window=("player",
  ...)` or `("youtube", ...)`; a full-frame graphic is this video's own
  point. Never mix the two looks.
- **The number, problem and fix screens are one card** (`lesson`): red "THE
  PROBLEM", green "THE FIX", gold "WHAT I LEARNED" or a count with pips, on
  the ruled ground, with sounds - not `stat` or a pull quote.
- **The end screen**: "Thanks for watching", big and centred, no channel
  name (`chapter` style `"headline"`), the camera box with it to the end.
- **The camera box is landscape** (3:2, the full camera height, the mic in
  frame, the right side cropped): bottom right in 16:9, bottom centre in
  9:16. Only on a personal aside and the ending - not in the first minute.
- **A card is read before it moves**: a chapter's way in keeps 2.2 s of
  room after its line (`lead_gap`), and a strip's last window gets a pause.
- **Space, not dust**: the sky has no grain and a falling star every 4 s.

**From the fourth review (2026-11-24):**

- **The channel's own bed, soft and low** (his call: "different background
  music for this channel ... something soft"; most creator explainers run a
  quiet lo-fi or ambient bed, some none). `assets/brand/music/oktai-bed.wav`,
  a lo-fi instrumental rendered locally with ACE-Step (ours, MIT), 12 dB under
  the other channels' level since 2026-11-24 (6 before; `oktai.MUSIC_LUFS`), up for the opening and each
  chapter's way in (`render_long(music_swell=True)`, `audio.swell`). The
  examples from the other channels keep their own music.
- **His error sound on every red mark** (`assets/brand/sfx/verdict-wrong.mp3`).
- **A card is read before it moves on**: more items than captions arrive one
  by one, never one-then-the-rest (`plan.reveal_times`, both engines); a
  chapter window already passed is blurred with a check and no label; a
  strip can wait on a card (`path=[0, 1, 2, 2, 3]`); a wall of counting
  numbers gets a pause after it.
- **Claude Code chats play whole**: `screen(..., zoom=1.0, idle=1.0)` - no
  zoom onto a corner, no idle sped up - under two sentences.
- **An example is never from this video** - "Money." as an older video's
  chapter title, in a player.
- **The camera box is gone before the TV-off** at the end, with half a
  second of the end screen alone between them (`TV_OFF_CLEAR` 1.4 s; at
  0.9 s the two read as one motion).
- ~~In a Short, the examples play under the voice~~ - reversed the same
  day, see below.

**From the fifth review (2026-11-24), the recorded cut with pickups:**

- **An example plays out before the next line, in a Short too** ("the
  shorts still overlap the music example or AI voice example with my voice
  over, we don't wait for it to finish"): `build_short` no longer sets
  `samples_under`; the line before an example gets `_after(clip)`, and a
  chapter Short keeps every pause the long form wrote.
- **A list on a strip is read in written pauses** ("add a gap on the voice
  before 'the same template' so there is time to see the stock clips"):
  each named card its own sentence with a gap of 1.0 s or more (shorter
  pauses are capped at `max_pause`), and a stop after a pause travels *in*
  it - `reel` option `lead` per stop - so the card lands on its words.
- **A chapter opens on its own window** ("no need to show the transition,
  just zoom out a bit to see the check on the previous one"): `reel` option
  `open=0.78`, no glide from the last window (`chapter_window`).
- **Numbers over an ordered lineup**: the roadmap's tiles carry "#1"-"#5"
  (`logos` payload `numbered`).
- **Show a mistake the way it was made**: the overcorrection's labels are
  plain type on the footage (`reel` option `labels="over"`), not a card's
  title - "like the real example".
- **An example appears once**: the opener's slop and the picture chapter's
  quantum cut were the same video; the opener shows the price explainer.
- **The prompt is the line to read**: a Claude Code chat types its prompt
  under a yellow highlighter (`claude_chat(mark=True)`, the default).
- **A wall of animations gets 2-3 s after its line** (the graphics wall
  3.0 s, the "same layout" wall 2.7 s): its tiles play for 4.5 s.
- **The giveaway in short quotes**: a bar of "gave it away" names what was
  said, paraphrased and generic ("It was Hal Finney."), not the full line.
- **A comparison says what is the same**: under the two AI voices, "*Both
  are text-to-speech voices reading the same script." (`voice` payload
  `footnote`). It does not say "the same model": the first is macOS `say`.
- **He is the judge, in his own face**: "The judging" is his avatar
  (`assets/brand/oktai/oktay-badge.png`), not Kokoro.
- **A page he reads from is cropped to the script and recording**: the
  script page hides its header, instructions and Start button and carries a
  REC dot (`screen(..., rec=True)`, `core/rec.py`).
- **No camera box from a pickup**, none on the end screen: a pickup's room
  and light differ from the take's. A pickup line whose voice does not match
  can go - "English isn't my first language" did.
- **Sound under data is data**: a shot can name its place-sound
  (`Shot(ambience="digital")`, bit chirps) where its stock folder's name
  would give a server room's fans.
- **The pickups are matched to the take** (`recorded.match_pickups`): the
  take's spectrum and level, before the chain; and the chain's EQ moves the
  voice 70 % of the way to the channel voice, 5 dB a band at most (was 60 %,
  4 dB) - clearer at 3-8 kHz. The level range was already 3.5 LU, so still
  no compressor.
- **Stock picked by hand is fetched by id**: `core.stock.video(id, slug)`.

**The sound (2026-11-24 evening), from his reference video and four
samples - "new tone sounds the best, better than the original":**

- **The voice is aimed at a creator's voice, not the AI voice.** Toward
  `noah` (bright, synthetic) his read came out 8-11 dB hot at 3-5 kHz -
  "very punchy, maybe even loud". `recorded.TARGET_LTASS` is now his
  reference video's spectrum, matched 80 %, 6 dB a band at most.
- **The close mic's boom is cut hard**: 24 dB an octave under 100 Hz and
  -3 dB around 200 Hz (`clean_chain`). His take sits 23-26 dB over 1 kHz at
  100-126 Hz.
- **No real compressor**: one 2.5:1 catcher 10.5 dB over the speech, for
  plosives. Compression lifts the room's tail (11 -> 9 dB down after a word).
- **The bed 12 dB under the other channels' (`MUSIC_LUFS` -35)**: ~17 dB
  under his voice; mixing guides put music 18-20 dB under narration.
- **De-reverb is ready, not on** (`recorded.dereverb`): his room's tail is
  11 dB down 20-50 ms after a word, a treated creator's 26; at two
  strengths it reached 21 and 23 dB with words heard as well. He preferred
  the sample without it.
- **Pickups are cleaned, then matched** (`match_pickups` after
  `clean_gaps`): matched first, a final "s" read as a breath and was cut.
- **A split line keeps its own words' times**: where `_split` moves a
  boundary past Whisper's start of the next word, that word's caption is
  clamped into its own line - it came up 1.8 s early, before the written
  pause, and the reel's card travelled with it (the first render, caught
  before it shipped).
- **A highlight holds the screen camera**: `screenplay.mark` logs where it
  is drawn (`focus` events) and `screenrec` holds the zoom there as on a
  click, without a ripple; drawn in the idle zoom-out it was unreadable.
  Red on the policy page: yellow vanished on Google's pale-yellow notice.

**From the last reviews (2026-11-25):**

- **Our channels, not our sites**: a "my videos" screen is the YouTube
  channel itself - dark (`screenplay.YOUTUBE_DARK`, YouTube ignores the
  browser's scheme signed out), the EU consent page declined before
  filming (`_decline`), header, tabs and side menu hidden, **Popular**
  picked before filming (`Browser(before=...)`), one slow scroll
  (`screenplay.glide`), no zoom (`screen(..., zoom=1.0)`), no pointer. "It's
  hard to focus ... we do too much": one thing per screen.
- **Hide what is not the point, in code**: Tinnitus Help's popular uploads
  are sound-therapy sessions, not slop; any grid item whose title ends in a
  duration ("(20 Minutes)") is removed as it renders.
- **A pause under 1.0 s is written as `recorded.Pause(0.3)`**; plain gaps
  under 1.0 fall back to his natural pause (max 0.4). The slop list went
  1.0 / 1.8 -> natural / 0.3 ("too slow", then "reduce it more").
- **His voice at 215 words a minute** (`oktai.TARGET_WPM`, 190 until
  2026-11-25): he tried 200, 224, 220, 218 and settled on 7.5% over 200.
  Pitch kept; captions, cuts and the camera box follow the same edit.
- **A take that never touches the mouse shows no pointer** (no resting
  hand), and the mouse is parked after a setup click - it hovered the first
  video card. A screen render is reused while its take's digest holds:
  change the recorder, delete the capture.

**Recording (2026-11-24, from the take's own numbers):** peaks at -16 dBFS
and speech at -34 dBFS leave 10 dB unused - gain up until the loudest words
peak near -10 dBFS. The room is quiet (-71 dBFS) but live: closer to the mic
(10-15 cm, or 5-10 for a dynamic mic) gives the voice 6 dB over the echo for
every halving of distance; aim it at the mouth from slightly to the side;
something soft behind the mic and on the desk. Pickups in the same place,
distance and gain as the take - his were another room, 3 dB boomier.

## Shorts from the long form (2026-11-23)

He reads one script; the long form is built first, then a Short per chapter
is cut from it - "use some of the content for Shorts, like the other
projects". `oktai.from_long(SECTIONS, keys, extra)` picks lines by their
opening words with their pictures and pauses; `build_short(..., window=None,
tag=chapter)` finds every line in the same take, so nothing new is recorded.
Each opens on the slop cards, "I know, because I made almost ninety of
them", "Here is what I learned" and "Mistake N of five: ..." over that
chapter's window ("People call it AI slop" only in the two about how slop
looks), tells the chapter in order, ends on its rule and "That's one of five
mistakes. The other four are on my channel." (his notes, 2026-11-24). Screens
recorded 16:9 are taken again `vertical=True`; a line the long form held a
picture over needs its own first picture. The worked example is
`projects/oktai-short/why-ai-videos-feel-fake-chapters.py`.

**Not yet per brand:** captions and beat type are still the engine's global
Futura / Avenir. Poppins in the drawn beats is a follow-up.

## Recording

What Oktay sends: **one file per script** (the long form and the Short each
get their own), voice and face in the same take when possible - **or one
file for both**, read top to bottom off the script page (the first
recording, 2026-11-22): save it as `recording.*`, and each project passes
`window=(start, end)` in seconds to `build_long` / `build_short`. The Short
repeats the long form's opening lines, so without the window the last take
of those lines would come from the wrong script.

- Read the script as written, a sentence per breath. **On a mistake, say the
  whole sentence again** - the last good take of each sentence is kept, and
  false starts, re-reads and asides between takes are cut.
- Mic 15-20 cm away, soft room. Camera at eye level, light from the front.
- **Not too close (the first recording, 2026-11-22: "very quiet but loud,
  as if I'm too close to the mic").** That take had the dynamic mic just
  under his chin: 3-6 dB of extra boom below 400 Hz, breaths as loud as
  words, and clipped peaks while the read itself sat at -22 LUFS. A hand's
  width (10-15 cm) for a dynamic mic, aimed at the corner of the mouth
  rather than straight at it, the gain down until the loudest word peaks
  near -10 dBFS, and a normal speaking voice, as to someone across a table.
  Run `tools/oktai_recording_check.py` on a 30-second test first.
- Voice on a separate mic is fine: pass `Recording(audio, video=camera_file)`
  and the face is synced to the voice by cross-correlating the camera's own
  sound (`facecam.sync_offset`).

## Building with a recording

```python
from video_automation.core.brand import OKTAI
from video_automation.core.recorded import Recording, sidecar
from video_automation.core import facecam

REC = Recording(Path("~/Movies/OktAI/job-search/long.mov"))
made = render_long(SECTIONS, out, work, brand=OKTAI, voice=REC, ...)
```

A project normally does not call this itself: `oktai.build_long(SECTIONS,
NAME, face=FACE, ...)` finds the recording by name, falls back to a Kokoro
draft when there is none yet, and adds the camera box.

`voice=` takes a `Recording` anywhere it takes a profile name, the Short
(`render_crypto_short(..., voice=REC, brand=OKTAI)`) included. A chapter
card's spoken title is a sentence too, so it has to be in the recording.

What happens, in `core/recorded.py`'s docstring: Whisper (large v3 turbo, on
MLX, offline, run from `create-song-automation`'s venv, cached by file hash)
transcribes every word with its time; each sentence is matched to its takes;
the kept takes are cut and joined with the real pauses (capped) or the
recording's own room tone; then a light clean-up and `loudnorm` to -14 LUFS,
where the Kokoro reads sit. Captions are timed by the words actually spoken.

**What the first real recording taught (2026-11-22, 11 minutes, both
scripts in one file):**

- **Whisper skips on a long file.** Fed all of it at once it dropped a full
  retake and the outro. It now gets pieces of 16-26 s cut at pauses, and any
  loud stretch it left without words - or hid under one word stretched over
  seconds - is read again (`_pieces`, `_WHISPER`).
- **Stumbles inside a sentence** ("AI tools love... AI tools love stock
  footage") lose their first copy (`restarts`). Whole-sentence retakes are
  still `align`'s: the last good one wins.
- **A misheard first word stays in the take** ("Claude" heard as "Cloud",
  "Thanks" as "Short"; `_edges`), and a title is never taken from inside a
  longer line ("the first ten seconds" holds "the first seconds").
- **Pacing**, his note: "structured and not too slow". A pause inside a
  sentence over 0.45 s is cut to 0.28 s (`_tighten`); between sentences the
  cap is 0.55 s for OktAI.
- **The clean-up follows the room** (`clean_chain`): the old fixed de-noiser
  took 5-9 dB off everything above 4 kHz in a room that was already quiet.
- **Matched, not compressed**, his notes on the renders: "too loud, doesn't
  fit", then "quiet but loud, as if I'm too close to the mic". `match_eq`
  moves the voice toward `noah`'s tone, a low shelf takes the proximity
  boom, breaths are lowered, and the level is one gain to -18 LUFS - no
  compressor.
- **The second recording (2026-11-22): "make sure you clean the vocals ...
  better cut everything between sentences or even words if it's messy".**
  Three things now run on every recording:
  - *Room tone between words* (`clean_gaps`): each gap, trimmed to the
    words' real tails and onsets, becomes the room's own tone - breaths,
    clicks, creaks gone. Something as loud as speech and longer than a click
    stays, in case it is a word Whisper missed.
  - *Stumbles inside a sentence are spliced out* (`_trim` keeps both parts
    of a read broken by a stumble, `_junk` cuts what is between): "stock
    footage and *it was love stock food* and stock footage loves".
  - *The cut is listened to* (`_extra_words`, `_choose_cut`): the assembled
    voice is transcribed; a phrase of two or more words the script lacks is
    a stumble Whisper hid on the whole file. Each way of cutting it - the
    later copy, the earlier one, none - is built and transcribed with the
    sentences around it, and the one that reads most like the script wins.
    "So the rule became... so the rule became simple" kept the second copy;
    "And now / the voice" lost its stray "And now".
  `restarts` (drop the first copy of a phrase said twice) is no longer
  applied: it kept "love stock food" over the clean first read.
- **Sped up, pitch kept**: "speed up my voice with about 1.25 or 1.5 ... I
  read slower because I'm not native". `target_wpm=190` (`oktai.TARGET_WPM`)
  picks the speed per recording within 1-1.5x (`_speed_up`, `atempo`); the
  sound examples' gaps keep their length and the camera box plays the face
  at the same rate. His first read: 148 wpm, so 1.29x; 6:43 became 5:25.

- **Word edges are found in the hiss band too (the third recording,
  2026-11-23: "the s of graphics is cut", "minutes", "seconds", "sentence",
  "FFmpeg" heard as "FMPEG").** A final "s" or a starting "f" is all hiss
  and little level; on a quiet take it sat under the gap clean-up's level
  line and became room tone. A word's tail and onset now run while either
  the whole band or the 3.5-11 kHz band is speech (`_hiss_db`), up to 0.35 s
  past Whisper's time, over dips of 30 ms. The voice's gate sits just over
  the room (not +26 dB), and the music ducks 80 ms ahead of each word
  (`audio.LOOKAHEAD`) - "AI" after a pause had lost its "A" to the bed.
- **A final stop keeps its release (the pickups build, 2026-11-24: "Claude
  made it with the code" heard as "...the Colt").** A "d", "t" or "k" at
  the end of a word is a tenth of a second of silence and then a short
  burst of hiss. The gap clean-up stopped at the silence and painted the
  burst over with room tone. Now a tail bridges up to 0.16 s of closure to a
  burst that is over within 0.2 s (`_bridge`; a longer one is a breath and
  stays room tone), and a sentence's end edge does the same (`_release`).
- **Check a word with the build's own timeline.** `ffmpeg -ss` on the
  joined recording lands about 0.14 s off the full decode the build uses;
  cut a doubtful word out of `load_audio(...)` instead, or the "missing"
  sound is just outside the cut.
- **Pins and drops - the editor's pick of the take.** `pins={"line": (a,
  b)}` uses those seconds for a line the matching spliced from two reads
  ("AI tools love... AI tools love stock footage"); `drops=[(a, b)]` cuts a
  word he said that the video should not ("hands"), the line keeping it as
  its spoken half so it still matches.
- **Pauses**: a recording's pauses are capped at `max_pause` (0.40 s for
  OktAI) unless written as a beat (1 s and up: a sound example, a chapter's
  way in).
- **Single leftover words at a sentence's edge (his review of the second
  cut, 2026-11-23: "we let some parts of the sound which are not part of
  the sentence in between").** "stops *begin*, and one track every time",
  "*paragraph.* And here, the whole paragraph": one word of the failed
  attempt just before a retake. At a sentence's edge one extra word is now
  enough for `_choose_cut` to listen (`_extra_words(bounds=)`); and a cut's
  onset search that finds nothing quiet stops at the quietest point, never
  back inside the word before (`_edge`, `_refine`).

## Writing for him (2026-11-23)

His review of the second recorded cut: "it needs to be easier for viewers to
follow ... very engaging, flowing easily, and clear about what we discuss
next". The rules, checked against three videos on the same topic
(Kurzgesagt, ThioJoe, Kevis Unfiltered, transcribed for the opener):

- **One message, said in the first 30 seconds, proved by every chapter**
  (2026-11-23, his review of the third cut: "I'm getting confused what the
  main message is"). The opener mixed three of the plan's slate - the
  lessons, the pipeline, the tells. A video is one of them; the others are
  a beat at most. Each chapter: what the AI did by default, what I noticed,
  the fix shown working, and one rule the viewer can use ("If you make AI
  videos, ..."). Title and cover say the same message.
- **Problem first, then the stake, then a counted promise.** The slop the
  viewer has seen; "I made a lot of it"; "here are the five mistakes that
  mattered most". Each chapter counts out loud: "the second mistake was the
  music".
- **No title read on its own.** A chapter is named inside a sentence
  (`Section(lead=("The second mistake", "was the music."))`); the title comes
  up on the word. A read title followed by "And now the voice" was a repeat
  with a pause either side.
- **Every example is introduced**: "here's one example", "here's what that
  looked like", "here's the first track I made". Nothing shown cold.
- **"I", never "we"** - one person, no team. **Short plain sentences** - he
  reads in his second language; "a bed feels alive because of rhythm, not
  brightness" was the example of what not to write.
- **Nothing the viewer cannot use**: an unprovable number ("I can't prove the
  template was the reason") and asides ("some of these get a video of their
  own soon") went.
- **The roadmap is a strip of windows** (`reel` with a `path`): the opener
  walks all five as they are named; each chapter's lead starts on the window
  before, travels to its own on the word and dives in. It also replaced the
  run of labelled clips he called a slideshow.

**Pickups (2026-11-23).** Lines added after a take go in the project's
`PICKUPS`; the script page lists them first ("Record these") and marks them
NEW in place. He reads only those into `pickups.mov` next to the recording;
`oktai.recording` joins it onto the take's end (`recording+pickups.mov`), so
every time already in the project - pins, drops, the window - still holds,
and a window grows a second range for the pickups. A line read in the
pickups wins wherever its line sits (`align(free_from=)`, 2026-11-24): the
pickups are read out of script order, so they are matched first and only
the lines left over need to run in order through the take. Once a build
has used them, empty `PICKUPS` so the next script page asks for nothing.

Read the report's `!` lines for what Whisper heard differently: most are
Whisper ("unexplainer" for "an explainer"); a word he really changed goes
into the script so the captions match. A line flagged **"lasts 1.5s: a
stumble may hide in it"** is the one a transcript cannot catch: Whisper
folded a false start into one long word ("Here is", a throat-clear, then
the whole line again came back as a 1.5 s "what", 2026-11-24), and the cut
kept all of it. Find the clean read in the levels and pin it.

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

**A box leaves with its sentence** (2026-11-23, his note: "it stays there
even when I'm already reading the next sentence and don't look in the
camera"): `build_long` / `build_short` pass the sentences' times and every
cue ends 0.25 s after its sentence's last word, whatever `on=` asked for.

On by default for the hook (first ~3 s) and the last line; `on=` adds a
phrase (as its caption starts) and how long to stay; `cue_list=` gives exact
seconds. The face is cut with the voice's own edit file, so the lips match;
a gap filled with room tone shows a still frame. 16:9: bottom right, 320 px,
above the control bar. 9:16: top right, 300 px, left of the right rail.
**Off while a screen or a number has to be read** - the box would cover the
evidence (`docs/oktai-channel-plan.md`, "The camera box").

**Lip sync (2026-11-22, "the part where I'm shown is not matching the
read"):** a QuickTime `.mov` starts its sound 0.24 s after its picture, and
the edit is in sound time - the face is cut `stream_lead` later, and each
piece is a whole number of frames counted from the cue's start, so many
short pieces cannot drift. Check it on the render, not by ear: lay out the
box's mouth frames around an m, b or p (`me`, `because`, `person`) - the
lips close on the sound's own frame. Faces are found on frames ffmpeg
grabs: OpenCV's seek returns nothing in a long `.mov`, and the box fell back
to the whole room. In 9:16 the box sits at the top right over a `voice`
beat's first row: keep that row's note short ("a computer voice").

## Screens

**Oktay records the voice, never the screen** (the editor's note,
2026-11-21). A screen shot is `oktai.screen(NAME, FILE, take)` (ad slots collapse on every page -
`screenplay.ADS`, 2026-11-23: "make sure there is no gap from ads"), where the
take is a `core/screenplay.py` script - a `Browser` (go, click, type,
scroll) or a `Terminal` (command, output, thinking). `build_long` /
`build_short` play it, record it to `screens/<file>.mp4` and cut it zoomed
to the work, drafts included. How it works and what may go on screen:
`footage.md`, "Our own screen".

## Sound examples

`oktai.examples.make(folder, {name: (maker, arg, {kwargs})})` renders each
clip once, keyed by its recipe. Voices (the editor, 2026-11-21: the male
explainer voice for the AI examples, the first one deliberately worse):
`oldest` (macOS `say`, Daniel, line by line with dead silence - a
dramatization, said so in the script's sources), `one_at_a_time` and
`today` (`noah`, line by line against one run - the fault `voice.md`
measured), `phrase` (one line). Music: `bed("calm")` (pads alone, the creepy
one) and `track("night-drift")`. `samples.register(path, level=, bed=)`
makes each a sample; `bed=0.0` stops the music bed under a music example,
the editor's "it needs to be paused for this part". The `voice` beat plays
them; the opener of `why-ai-videos-feel-fake` is the worked example.

## Our own videos and the logos

`oktai.own(NAME, youtube_id)` is where one of our published videos lives
for the `phones` beat; `fetch_own(NAME, [ids])` downloads them with yt-dlp
(our own uploads - only when the editor has said yes). `core/logos.py`
builds round badges for the tools and platforms a script names (the
portfolio's own badges first), rebuilt on demand and kept out of git.

## Links in scripts

A long form names a tool when it is on screen and says the referral line
once there; the Short does not pitch. The description carries the links and
the disclosure. The rules are in `docs/oktai-channel-plan.md`, section 7.
