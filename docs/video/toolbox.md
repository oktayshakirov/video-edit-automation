# The shared toolbox

Every tool here is general code in `video_automation/`; a channel's look
is in how it uses them, not in which it has. **A tool or fix made for one
channel is available to all three the same day** (the editor, 2026-11-25:
"general tools we implement and problems we solve should be implemented in
all ... without ruining the style of each channel"). Read this table at
"Write the picture first" (`workflow.md`) for every video, and pick by the
channel's column - a blank cell is a choice, not a gap.

Channels: **C** thecrypto.wiki (gold on black, explainer, Kokoro voice),
**T** tinnitushelp.me (peach on near-black, calm, an audience with
hyperacusis - no slams, no sustained tones), **O** OktAI (Oktay's own voice
and face, first person, "show the real thing").

## Picture

| Tool | Where | C | T | O |
| --- | --- | --- | --- | --- |
| Verdict marks: red cross / green tick on a shot | `Shot(verdict=)`, `core/verdict.py` | a myth, a scam screen | a myth vs the evidence | every mistake shown |
| Strip of cards the camera travels (`reel`): per-stop `lead`, `travel`, labels `"over"` the footage, chapter windows that `open` on their own card | `beats/reel.py` | a list of coins, exchanges | a list of triggers | the roadmap, slop, chapters |
| Scripted screen takes - a real page or terminal played headless, no hands | `core/screenplay.py`, `oktai.screen` / `screenplay.shot` | a block explorer, an exchange page | a guideline, a study page | Claude Code chats, his channels |
| Highlighter drawn across a line of a real page, the camera holding on it | `screenplay.mark(text, color)` | the clause in a ToS or a hack report | the sentence in a study | the policy line |
| Setup before filming, a slow scroll, no pointer | `Browser(before=, cookies=)`, `screenplay.glide` | sort a list before showing it | | channel grids |
| A page's dark theme, a consent page declined | `screenplay.YOUTUBE_DARK`, `_decline` | any YouTube screen | any YouTube screen | channel grids |
| Cut-out subject: `isolate`, `pop`, `parallax`, `behind` on a still; the `cutout` cover - **at least one per long form** (the editor, 2026-11-25: "we dont use that tool much but looks good"; `script_check` `cutout`) | `core/vision.py`, `thumbnails.md` | a person in the story (never stock); give a 3:4 portrait a wide copy first (`bernie-madoff-wide.jpg`) or the head hides the word | a real photo of the subject | **his own photo and face** - covers, the hook; **and screens built from cut-outs on the video's topic** - objects, logos, people of the story, animated (the editor, 2026-11-25: "recommended to create interesting screens and animations on the video topics, like the ones we tried for crypto wiki"; to be experimented with and shared from the next video) |
| Money through a middle, then nobody in it (`ponzi`) | `beats/ponzi.py` | a Ponzi against a market | | |
| Coins moving wallet to wallet, no centre (`peers`) | `beats/peers.py` | a closing line about Bitcoin, in place of cash | | |
| Animated emoji in drawn beats | on by default (`animated_emoji=`) | 🔥🔒 where they animate | sparing - motion is calm | lesson counts, steps |
| Lesson cards: problem / fix / "what I learned", counts as pips | `beats/lesson.py` | a "the rule" card closing a section | a gentle "the takeaway" card | every chapter's rule |
| Logos lineup, `numbered` "#1"-"#5" | `beats/wide.Logos` | exchanges ranked | | tools, the roadmap |
| Bars with a quote and a note beside it | `beats/scale.Bars` `(label, note)` | quotes with sources | a study's arms | Shorts' hooks |
| Voice / waveform comparison, with a `footnote` | `beats/voice.py` | | sound samples A/B | AI voice vs his |
| Wall of real beats, phones of real Shorts | `beats/wall.py`, `beats/phones.py` | past explainers | past sessions | "what I made" |
| REC dot over a shot | `Shot(rec=True)`, `core/rec.py` | | | his script page |
| Closing card after the TV-off: a line + arrow to the description | `render_long(coda=(line, small))`, `overlay.Coda` | the free guide / app | the free audiobook sample | the free prompt |

## Sound

| Tool | Where | C | T | O |
| --- | --- | --- | --- | --- |
| Place-sound under footage, named per shot (`"digital"` bit chirps) | `core/ambience.py`, `Shot(ambience=)` | data and servers: `"digital"` | quiet beds only, `KIT_GAIN` | `"digital"` |
| Sound examples that play out in their own pause, never under the voice | `Shot(samples=)`, gaps `_after(clip)` | | the sound samples | music, voices |
| A recorded voice: pins, drops, pickups matched to the take, splits at the quiet after an "s", `Pause(0.3)` | `core/recorded.py` | if he ever records | if he ever records | every video |
| De-reverb for a live room | `recorded.dereverb` | | | ready, unused (his pick) |

## Checking

| Tool | Use on every channel |
| --- | --- |
| `tools/hear_check.py VIDEO` | the built video transcribed against its own subtitles; a flag is checked on the line alone before it is called a fault |
| `tools/frame_sheet.py VIDEO OUT T...` | frames at the editor's timestamps, 16:9 or 9:16 |
| `tools/oktai_preview.py` | OktAI: one stretch rendered at the full video's speed |
| `tools/visual_check.py`, `tools/script_check.py` | before any draft |
| `tools/short_cover_check.py COVER...` | every Short cover, before any TikTok upload: type and plates must sit inside the 3:4 band TikTok's grid keeps (`thumb.SAFE_TOP`-`SAFE_BOTTOM`, y 240-1680) |

When a new tool lands, add its row here with all three columns, and say in
the channel skill's own doc which way that channel uses it.
