---
name: video-crypto-long
description: Make long-form 16:9 YouTube videos from thecrypto.wiki articles — 2-4 minute explainers with voiceover, drawn data beats, chapters, an SRT and a thumbnail. Use when the user runs /video-crypto-long, asks for a long or full-length crypto video, wants a post from thecrypto.wiki turned into a YouTube video, or wants to embed a video on a crypto-wiki post. For vertical TikTok/Shorts use video-crypto-short instead.
---

# Crypto Wiki — long form

**Repo:** `~/Coding/video-edit-automation` — run from there with `PYTHONPATH=.`.
Renders go to the Desktop; they are uploads, not repo artifacts.

**Source content:** `~/Coding/crypto-wiki` — 61 posts, 27 exchanges, 33 crypto-ogs.

**Read `docs/long-form-strategy.md` first.** It carries the SEO reasoning, the
demand ranking that decides which post is next, and the measurements behind the
numbers below. This file is how to build one.

## Built

```bash
PYTHONPATH=. .venv/bin/python projects/crypto-long/satoshi-proof.py
```

`video_automation/longform/` — shared with tinnitus. What differs between the
two sites is a `Brand` and a script, not a fork.

```python
from video_automation.core.brand import CRYPTO
from video_automation.longform import Meta, Section, render_long

made = render_long(SECTIONS, out, work, brand=CRYPTO, meta=META, voice="mia",
                   music="pulse", callouts=None, endcard=ENDCARD,
                   thumb_headline="...", thumb_subline="...",
                   thumb_image=..., thumb_zoom=1.30, thumb_focus=(0.0, 0.84))
```

Produces the MP4, an `.srt`, a 1280x720 thumbnail and a `.md` sidecar carrying
the description, chapters and any chapter-rule violations.

**Built on the site side:** `<PostVideo />` and `VideoObject` on both repos,
driven by a `videos.json` registry - see `docs/site-video-integration.md`. A new
video appears on its article by adding a registry entry; do **not** put video
metadata in MDX frontmatter.

`/videos` and `/videos/<slug>` carry the feed and the per-video transcript
pages. Chapters go in the registry as `{start, title, text}` and drive both the
transcript and the `Clip` key moments.

**Still unbuilt:** upload. The registry is hand-edited on upload by design.
Script generation from MDX is **not** planned and should not be: the script is
the product.

**Keep the `.srt` and the `.md` sidecar.** Both were cleaned off the Desktop
before the site pages needed them, and the transcripts had to be rebuilt from
`SECTIONS[].sentences` plus the chapter times in the YouTube description.

## The shape

| | value | why |
|---|---|---|
| frame | 1920x1080 | `core.frame.LANDSCAPE` |
| runtime | **2:30–4:00** | under 2:30 sits awkwardly between Shorts and long form; v1 shipped at 2:47 |
| words | 440–700 | `mia` runs ~2.9 words/sec with `gap=0.34` |
| shots | 27–44 | ~5.5s mean |
| captions | **SRT only, none burned** | see below |
| voice | `mia` (`af_heart`) | the user's pick for the first cut. **Candidate, not approved.** |

## Structure: an arc, not an agenda

The format is **continuous narration**, not a sectioned document. The first cut
was seven numbered chapter cards over a script written as headings and bullets,
and it read as a slide deck. Follow this arc:

    hook -> reframe -> deep dive -> counterintuitive twist -> mirror -> echo

and these rules, which come from a reference prompt for a doodle-explainer
channel and independently from YouTube retention research — they agree, which is
why they are here:

- **Second person throughout.** "You have seen the headline." Never "we", never
  "I". The viewer is the subject, not the audience.
- **Short. Short. One longer that builds. Short. Question?** Write the cadence
  into the sentence lengths deliberately.
- **A question every four to six sentences.** Every section turn is one.
- **The three-phase opening.** Pattern interrupt in the first 5s, a specific
  promise by 15s, a reason to commit by 30s. The steepest retention drop is
  between seconds 10 and 20 — nothing decorative goes there. YouTube's "Intro"
  metric is % still watching at 30s; above 50% is outperforming.
- **Say the point, then show the graphic.** A beat that arrives before its own
  thesis has to be decoded rather than read. The mining rig cut put "this is who
  you are bidding against" *after* the comparison it introduced and the user
  found it confusing — by then they had already read both columns and did not
  need telling what they were. One line of setup, then the beat.
- **Make the retention call out loud, early.** "Stay to the end and you will know
  whether to build one." It is the oldest device on YouTube because it works: a
  promise the viewer can *hear* being made is what buys the next three minutes,
  and a specific one beats "stay tuned". Put it in the first fifteen seconds and
  make sure the outro actually answers it — the mining rig script asks and
  answers the same question, which is what makes the echo land.
- **The closing line echoes the opening, reframed.**
- **No jargon without an immediate plain-English decode.**
- **A title shaped like a question gets a question mark**, on the card and in
  `spoken_title`. "Where the money is actually made" has a question's word order
  and a statement's full stop, so the synthesiser read it flat and the card
  printed no mark. The rising intonation is free; punctuate for it.
- **Hold scenes.** Put `None` in the shots list where the picture should ride
  through the next sentence. One shot per sentence is a new scene every four
  seconds — a metronome, not a rhythm.

## No burned captions

`callouts=None`. Showing a handful of lines and not the rest reads as
arbitrary, which is what a viewer noticed immediately. The full transcript ships
as the SRT — YouTube indexes it and viewers can switch it on. The reference
channel puts nothing on screen but labels and arrows either.

## One `Section` per chapter

`Section(title, sentences, shots, kicker=, card=, spoken_title=, gaps=)`. Shots
correspond one-to-one with sentences, exactly as in the shorts. The chapter card
is **not** one of them — `Section.parts` adds it, along with the sentence that
speaks it.

- **The chapter title is read aloud.** The first build left the card in silence
  and paid for it with a 2.4s gap, which made every boundary a hole in the
  audio — six of them, which was most of why that cut ran short of its own
  target. Reading the title costs the same screen time, fills the hole, and puts
  the section headings into the SRT as real text. **Write titles that read well
  aloud**, or set `spoken_title`.
- **The opening section takes `card=False`.** An opening chapter card spends the
  one second that decides whether anybody stays.
- **Every chapter must run ≥10s, there must be ≥3, and the first must be 0:00.**
  All three fail *silently* on upload — the timestamps just render as text.
  `meta.check_chapters` reports violations into the sidecar; read it.

## Chapter cards

**No numbers.** A numbered agenda is the visual language of a presentation and
tells the viewer they are being lectured. It also hid an off-by-one: numbering
ran off the section index, and because the opening section carries no card, the
first one on screen read "02".

One line, centred on both axes, 108px, with a short rule opening outward above
it. **Usually a question** — a question makes the next twenty seconds an answer
the viewer is waiting for — **but a section that resolves something wants a
statement**, and forcing a question onto a conclusion is worse than saying it.
`Valid signature. Wrong address.` is a card; so is `Seventeen years, still
unsigned`. Write whichever the moment is.

## Checklist: two timing modes

`flow=False` (default) is the shorts' original — every item appears unmarked, so
the list is a genuine open question, then the verdicts land together. It has a
payoff and needs a written pause.

`flow=True` marks each item as it is spoken, and exists for when the **script
carries the verdict itself**: "Not a court ruling." "Not a writing style." When
the narration is already saying no, holding the cross back four seconds puts the
picture behind the voice. Use flow when the narration tells, two-phase when it
asks. Third element of the payload tuple.

## The watermark sits high

`logo_at=(64, 62)` with `safe_top=40`. It was at y=150 and collided with both
the full-frame photographs and the beat kickers — a 16:9 player puts nothing
there persistently, so the first guess of a 120px top reserve was paying a real
cost against a hypothetical one. The guard checks **`logo_at` minus the 8px
float**, so a mark that clears `safe_top` at rest can still raise.

Beat kickers moved to y=214 for the same reason: at 176 a 34px kicker read as
the second line of the logo lockup rather than as the beat's own heading.

### A photo's border never crosses the watermark

**There are two kinds of picture frame and only one of them has this problem.**
A photograph that fills the frame bleeds off every edge and draws no hairline at
the top, so the mark simply sits over the image — that is fine and is left
alone. A photograph that *fits* carries a gold hairline along its top edge, and
that line ran straight under the wordmark: two graphics crossing, which a viewer
reads as a fault rather than as framing.

`PhotoShot` dodges it automatically — nothing to set per shot.

`LOGO_CLEAR` came down from 16 to 10 while fixing the tinnitus mark, so a
dodging photograph now sits 6px higher here as well. **Every pixel of it is
charged twice** — once as dead space above the picture and again as size, since
a photo too tall for the remaining band is scaled into it. Under a 33px wordmark
that is invisible; under a square lockup it was the complaint that found it.

- **The push is a constant offset for the whole shot, not a per-frame clamp.**
  `y` travels across a Ken Burns move, so clamping each frame would hold the
  picture against the floor and then release it. The offset comes from the
  extreme of the travel and the motion is preserved exactly.
- **It fires only when the picture actually reaches the mark, in both axes.** A
  shot already below the wordmark, or sitting to its right, is untouched — which
  is also what keeps the shipped vertical shorts byte-identical, since 9:16 puts
  the mark at y=268 and the photograph 200px below it.
- **A photo too tall to fit under the mark is shrunk, not shoved.** Translating
  a picture that already reaches within 60px of the bottom pushes its lower edge
  off frame, so the bottom hairline vanishes mid-shot — one artifact traded for
  another. It is scaled into the band that is actually available instead, which
  costs a few percent on what is a downscale of the source anyway.

## The drawn beats carry the video

The arithmetic is in the strategy doc and it is the whole design: ~30 shots
against the 3–5 photographs a post actually has. Beats are not decoration here,
they are the majority of the runtime.

`chapter` · `checklist` · `stat` · `compare` · `quote` · `bars` · `grid` ·
`steps` — in `longform/beats.py`. The first six share a content column left and
a picture column right; `grid` and `steps` span the full width. Video clips
(`Shot(clip=...)`) and the end-screen sting are the two things that are not
beats; see `longform/clip.py` and `longform/overlay.py`.

- **Vary the layout across the channel, not just within a video.** The user's
  note on the mining rig cut was that every list in every video looks the same,
  and they were right: `checklist` and `compare` both set type in a left column
  with a ragged right edge, so a four-item list and a three-a-side comparison
  read as one graphic at a glance. Across fifteen videos that is the templated
  sameness the strategy doc says gets a channel suppressed. **The fix is
  silhouette, not decoration** — a different typeface or accent changes nothing;
  a layout with no left column and no ragged edge changes everything. Before
  building, list the beats you have chosen and check you are not using the same
  two shapes four times. Vary the item counts too.
- **`grid` is for a *set*; `checklist` is for a set with verdicts.** Cards across
  the full width, three to a row from five items up, two below that. Nothing is
  ticked or struck — if items need verdicts, that is a checklist. Each card takes
  an optional second line, which is where the wide layout pays for itself: "8 GB
  of memory" is far more useful with "enough for any mining OS" under it, and a
  list row has no room for that.
- **`steps` is for a procedure, and order is what it shows.** A numbered track,
  four or five nodes. This is the `timeline` the strategy doc listed and never
  built. "Install the drivers, install the miner, join a pool" as a checklist is
  three unrelated facts; on a track it is a sequence, and a how-to video is
  mostly sequences. **Numbers are right here and banned on a chapter card**, and
  the two are not in tension: a numbered agenda tells the viewer they are being
  lectured, a numbered sequence *is* the content.

- **The split layout is why this is sharp.** A 900px source — the site median —
  in a 660px picture column is a *downscale*. Full-frame photos are the only
  place the upscale ceiling bites. **Do not "fix" a beat by giving its picture
  the full frame.**
- **`compare` is the beat to reach for first** when the article has an "A vs B"
  in it. 16:9 is a bad shape for a list and a very good one for a comparison.
  **It reveals the whole left column, then the whole right one** — the first
  version alternated sides and that can never match the voice, because a script
  covers one column and then the other. Interleaved, the second column started
  filling while the narration was still on the first, which reads as the graphic
  being out of sync. Write **one caption chunk per item, in column order, with
  no lead-in sentence inside the beat's span** — a spare sentence in front eats
  reveal 0 and shunts every item one line late. Three per column beats two: two
  looks like a stub.
- **`stat` is the best value per second in the format.** A figure spoken and not
  shown is a figure not remembered. Use it for the one number that matters, not
  every number in the paragraph.
- **One caption per item.** That is what times the reveals — `reveals` come from
  the caption starts of the beat's own sentence, so a line appears exactly as it
  is spoken. Even fractions of the shot look synced until you watch them.
- **A `checklist` needs a ~2.4s `gap` on its own sentence**, or the verdicts have
  nowhere to land and `mark_times` compresses to nothing.
- A checklist with every item ticked is a legitimate use — a procedure that ticks
  through. `satoshi-proof.py` uses it for the four verification steps.

## Statements over footage, and the opener

**A line on a clip goes big and centred, never in a corner.** The first build
set a 34px kicker and a 58px line in the lower left and the user called it
boring and confusing — correctly, because a small label in a corner reads as a
caption for footage that does not need captioning. Set at 96px, centred, over a
scrim band, with the same rule the chapter cards use, the same line stops being
a label and becomes a **statement the footage is illustrating** — and it carries
the viewer into the section instead of annotating it. `Shot(clip=...,
payload=("KICKER", "The line"))`; the kicker is optional and usually better
empty.

That also gives the format its **title stamp**: a clip whose statement is the
video's own title. Put it on the line that promises the payoff — around eight
seconds, not on the opening frame — so it costs none of the first five seconds
while still functioning as a title sequence.

**The opener has to earn the first thirty seconds.** Not a picture and straight
into narration. The shape that works: cold-open on the claim, a hard number
early (`stat`, "0 out of four claims"), the title stamp on the promise, then a
reason to keep watching that is specific ("you will be able to run it by the end
of this video"). Nothing decorative goes in 0–20s; that is where the drop is.

**Open on motion. Frame one is a clip, not a photograph.** All three pilots
opened on a still held seven or eight seconds under a Ken Burns move, and the
user's word for it was boring — correctly. A slow push on a photograph is the
slowest thing this format has, and putting it exactly where the retention drop
is steepest is the worst available use of it. A clip is already moving on frame
one and costs nothing else. Keep the still for later, where a change of pace
reads as a change of pace rather than as the video not having started.

## The end-screen sting

`render_long(endcard=..., endcard_lead=7.0)`, screen-blended over the last
seconds by `longform/overlay.py`. It rides **over** the outro footage rather
than replacing it, because the outro is deliberately uncluttered for YouTube's
own end-screen cards and that gap is what the viewer stares at while the ask is
spoken.

- **Use a black-background sting, not green screen.** A screen blend
  (`1-(1-a)(1-b)`) leaves pure black exactly transparent — no key threshold, no
  spill suppression, no edge fringing. Chroma keying green against a
  gold-on-near-black palette tints every antialiased edge.
- **Measure a sting's bright bounding box across the whole clip before
  committing to it.** The first pick looked perfect on one frame and its
  animation turned out to be a *moving* vertical swipe divider crossing the full
  width — no crop removes that, and screen-blended it is a bright bar sweeping
  the frame. The keeper has a stable box on pure black.
- `crop` is fractional on the source; `scale` is a fraction of frame **width**
  and the height follows the crop's aspect. Forcing 16:9 smeared a 3.6:1 button
  strip.
- The sting is committed (`assets/stock/videos/subscribe/`), unlike the rest of
  the stock cache — one 0.4 MB file reused by every video is a brand asset, the
  same argument the drone location pin gets.

## Transitions: push, not dissolve

`render_shots(transition="push", xfade=0.34)`, which long form opts into —
`"dissolve"` stays the default because the shorts are byte-reproducible and must
not change under them.

**A cross-dissolve necessarily shows two shots at once.** For a third of a
second the outgoing shot's type sits on top of the incoming picture, and a
viewer reads that as a fault rather than as a transition. A push slides one
frame out as the other comes in, so **every pixel shows exactly one shot** and
there is still a deliberate move. Eased at both ends; a linear slide reads as a
scroll. 0.34s rather than 0.45 because a move that travels is legible in less
time than a fade that has to reach 50% before it reads as anything.

`Shot.transition` overrides per shot, `Shot.xfade = 0` still cuts.

## A number needs its own meaning on screen

`stat` shows one figure large. That works when the figure *is* the point ("0
times passed", "1.1M coins") and fails when it is a count of things the viewer
cannot see — a bare "5 / SIGNS TO ACT ON" tells nobody what the five are, and it
sits in one corner with the rest of the frame empty. If the narration at that
moment is naming items, use a `checklist` of those exact items instead. The rule
is the general one: **show what is being said, not a summary of it.**

## Fill the right column, always

A `stat` or a `quote` with no `picture=` is a short block on the left and 40% of
a 16:9 frame showing nothing. `Beat.EMBLEM` draws counter-rotating concentric
arcs there instead — deliberately abstract and low contrast, there to balance
the composition and give the eye something moving, not to mean anything. On by
default for `stat` and `quote`; a `checklist` or `compare` already spans the
frame and does not need it.

## `bars` — the beat for a proportion

`payload: ([(label, fraction, value_text), ...], title)`. `stat` shows one
number and `compare` shows two lists; neither can show a **proportion**, and a
proportion is the one thing a spoken number cannot convey. "One point one
million coins" means nothing without the supply; drawn against 21 million it is
instantly legible and needs no second sentence.

## Label your video clips

`Shot(clip=..., payload=("KICKER", "One line"))`. Stock footage is wallpaper by
construction — it was not shot for this script and cannot say anything
specific, so a stretch of it with nothing on top is the dullest thing in the
video. A kicker and one line in the same lockup the drawn beats use turns
wallpaper into a titled shot.

## A year never counts up

`Stat` animates numeric values, but suppresses it for a bare four-digit year in
1900–2100. "2009" racing from zero spends most of the beat showing 1200, 1780,
2001 — all plausible years, all wrong, and a viewer reads the wrong one as an
error rather than as an animation. Counting is for magnitudes, where the
intermediate values are obviously partial.

## Give a beat time to be read

A drawn beat whose sentence is short gets a shot that is gone in under two
seconds. If a beat carries the line the video is built toward, buy it a pause
with the sentence's `gap` — the outro's "Did they sign?" takes 2.40.

## Rules paid for in blood

**Cut between drawn beats; dissolve between photographs.** The shorts' "always
dissolve" is a rule about *photographs*. Dissolving a pull quote into a checklist
cross-fades two sets of type through each other and reads as a rendering fault.
`plan.lay_out` sets `xfade=0` automatically between beats and on both sides of a
chapter card. Do not override it.

**The drifting grid only draws on a flat panel.** Its tint is near-black, picked
against a dark backdrop; over a bright blurred photograph it reads as graph
paper. Over a photo the backdrop drifts instead.

**Measure the block, then centre it.** Every beat was first laid out from
fractions of frame height and every one left the bottom 40–50% of the frame
empty. Wrapping decides height, so measure before placing.

**Callouts are for the five to eight lines that carry the argument**, not for
every line. Full burned captions for three minutes fight every drawn beat for
the same space. The complete transcript ships as the SRT, which YouTube indexes
and which is exact where its automatic captions guess.

**Pick callouts from lines whose shot is a photograph.** `build` drops a callout
on a drawn beat — the shorts' rule, and for the shorts' reason: the beat's items
already *are* the type, set larger and mid-frame, so a line underneath restates
what is being read at that moment in a worse position. The natural instinct is
to call out the punchiest closing line of each section, which is exactly the
line a script tends to give a `stat` or a `quote` to. Three of the pilot's first
five callouts were silently dropped for this. A callout also cannot outlive its
own sentence's audio, so it can never bleed across the silence a chapter card
occupies — that is automatic now, but it is why the first pilot burned "There is
no third answer." straight over chapter card 03.

**Check phonemes before rendering.** `ecdsa` comes out `ˈɛkdsə` and `secp256k1`
is worse — `satoshi-proof.py` says "a cryptographic signature" throughout
instead. Years are fine (`2009` → "two thousand nine"). Spell out or avoid any
initialism.

## Music — generated, not fetched

`core/music.py` synthesizes the bed. **`pulse`** is the crypto default —
112 BPM, plucked sixteenths, soft kick. Also `momentum` (100 BPM, calmer),
`bright` (warmer), and the pad-only `tension` / `calm`. Pass a `Path`
instead to use a real track.

- **Pads alone read as creepy.** The first bed was three chords and a filter
  and the user's word for it was "creepy mysterious". What makes a bed feel
  dynamic is *note events on a grid* — an arpeggio and a kick give the piece
  a tempo, and tempo is what the ear reads as momentum rather than
  atmosphere. Brightness alone does not fix it.
- **`air` is 0 on every preset with a rhythm section.** That layer is
  broadband high-passed noise; under a bare pad it reads as space, with
  plucks present it is plainly audible hiss. Measured at 0.6% of energy
  above 4 kHz before, 0.03% after.

This is `sfx.py`'s argument at three-minute scale. A YouTube Audio Library track
is cleared for YouTube and **not** for a TikTok repost, which this repo does
routinely; its tracks are usually shorter than the video so `render_bed` has to
loop them, and a loop is only invisible if the track was written to loop. A
generated bed has no licence edge on any platform, is rendered to the exact
length, and — the part that matters for a channel — is the *same* bed every
time, which is a brand rather than a different stock track each video.

- **Voice ~7 dB over the bed** under speech, bed at full strength through card
  silence. Measured on the pilot. The sidechain numbers come from the tinnitus
  build and did not need changing.
- **The register is the whole thing.** First pass voiced the pad one octave
  above a 55 Hz root, which put 96% of the bed's energy below 200 Hz — a rumble,
  not music. Two octaves up, with `1/k` partials instead of `1/k²`, puts ~22% in
  the 200 Hz–1 kHz band where a pad belongs.
- **Nobody has listened to these on speakers yet.** The measurements say the mix
  is right; they cannot say it sounds good.

## Sound effects

All synthesized, all in `core/sfx.py`, all cued from the shot list by
`build._cues` so picture and sound cannot drift.

| cue | where |
|---|---|
| `riser` | 0.75s before a chapter card — says a cut is coming |
| `impact` | on the card — the riser's full stop |
| `whoosh` | cutting *out* of a card, covering the return to content |
| `reveal` | an item arriving on any drawn beat |
| `cross` / `tick` | a checklist verdict landing |

`LEVELS` sets each against the narration peak, and one gain for all of them
cannot work: a transition has to be heard over the bed, an item tick has to sit
under a syllable, and those are a factor of four apart. **The set is
deliberately small** — a sound on every event is a cartoon. The `riser` is
subtle by design and has not been judged by ear.

## Stock footage and photos — a supporting layer

`core/stock.py`, on the same Pexels key `publish-content` uses. Cached under
`assets/stock/` — the **bytes are gitignored and `manifest.json` is what makes a
build reproducible**, so anything pulled must land in the manifest. It was found
75 files short, including tinnitus assets from earlier sessions; an unmanifested
file is unrecoverable the day its photographer deletes it. (`stock.manifest()`
writes a different, thinner schema than the file on disk actually uses — extend
the existing JSON, do not call it and clobber the richer one.)

**This reverses the short skills' "never reach for a stock API" rule, and the
reversal is arithmetic rather than taste.** A three-minute video needs ~30 shots
and a post owns 3–5 images, so a long-form video built only from the archive
contains most of the same photographs as every other one. What survives is the
real rule: **stock supports, the site's images and the drawn beats lead.** Wall-
to-wall stock loops under an AI voice is still the failure the shorts describe.

- **Screen every candidate before using it — `stock.screen(path)` returns mean
  luminance and saturation.** Taking the API's top result shipped a novelty
  dinosaur, a bitcoin sticker on a pine table and a rainbow of cables into a
  gold-on-near-black video. `MAX_LUMA=48`, `MAX_SAT=50`; the keepers measured
  L4/S5, L14/S6, L41/S20.
- **Screen a clip across its length, not at one second.** `stock.screen(p, at=)`
  takes a timestamp for exactly this. `crypto-mining-rig-hardware/854969.mp4`
  measures **L27 on its opening frame and L88 by second six** — it is a push-in
  onto a cream-coloured case, and a single-frame check would have shipped it.
  Sample at 0.5, 3, 6 and 9 seconds and read the range. This is the end-screen
  sting's "measure the bright bounding box across the whole clip" rule arriving
  at ordinary footage, which is where it was always going to arrive.
- **A photograph can pass the box and still be wrong on the opening frame.**
  `data-center.jpg` measures L41/S40 and is a *green-lit* server room — green is
  the one colour that cuts hardest against gold. It was fine ninety seconds in
  and wrong at second three. The box is about brightness; hue against the brand
  is a separate judgement the numbers do not make for you.
- **Never put a site infographic in a full-frame shot.** A Ken Burns move on a
  diagram crops its own title off the top and its last row off the bottom, which
  is what shipped and what the user caught at 0:27. And at 660px in a beat's
  picture column its labels are unreadable. So an infographic has **no
  full-frame use in this format at all** — as a blurred `backdrop` it is only
  texture, which is fine and is the one place it belongs.
- **Screen the site's own images too.** `stock.screen` works on any file, and
  the library is much brighter than it looks in a browser: `investing.jpg`
  measures L196, `stock-trader.jpg` L170, `corporate.jpg` L113. Six of those
  went into the first Saylor cut and every one of them glared against the
  gold-on-near-black frame. The `MAX_LUMA=48` box is for full-frame stock and
  does not transfer — **the working ceiling for a site photograph is the
  pilot's own brightest, about L82**, and roughly S60 on saturation.
- **A picture can be off-message as well as off-palette, and that is worse.**
  `ftx-collapse.jpg` under a line about leverage reads as exchange fraud, which
  is a different failure from debt-funded volatility. `one-coin.jpg` is OneCoin
  — Ruja Ignatova's fraud — and placing it beside a living person is an
  accusation the script never makes. Read the filename's *subject*, not its
  vibe, and think about what a viewer will infer from the pairing.
- Build a preview sheet of first frames and *look* at it. The search query has
  almost no bearing on what comes back.
- Pexels 403s urllib's default User-Agent on both the API and the CDN, silently.
  `stock.UA` exists for that.
- Video shots go in `Shot(clip=..., clip_at=)` and are handled by
  `longform/clip.py`: a clip longer than its slot is **trimmed** at natural
  speed, a shorter one is stretched up to 1.33x, and it is never looped — a loop
  point in real footage is instantly visible. Clips are dimmed and desaturated
  to sit with the stills. `clip_at` skips into the source; stock rarely opens on
  its own best moment.

## The Ken Burns on a photograph is one float affine

`PhotoShot.draw` scales and translates the sharp layer with a single
`warpAffine`. It used to be three separate integer steps — `int()` on the
width, `int()` on the height, `round()` on the paste — so **the two axes
crossed their rounding boundaries on different frames**. The picture grew a
pixel taller on one frame and a pixel wider three frames later, which a viewer
reads as the image lagging its own move. Measured, the frame-to-frame delta
swung **3.4–4.5x between consecutive frames**; after the warp it is within
1.15x with no frozen frames.

This is the video path's lesson arriving at the stills, and it had been latent
for as long as the photographs bled off the frame — an edge you cannot see
cannot be seen to jump. Bringing both edges inside the frame for the watermark
dodge is what exposed it. **The hairline is drawn with cv2's `shift` for the
same reason**: a border snapped to whole pixels under a picture that is not
puts the judder straight back.

**This changed the vertical shorts too, and they are no longer byte-identical
to the shipped renders.** That was a deliberate call — the old bytes contained
the judder, and `crypto/shots.py` has claimed subpixel motion in its own
docstring since it was written. If a short is ever re-rendered it will look
slightly smoother and hash differently.

## Motion on a video shot — three things that all caused visible glitches

Stock is **25fps against this 30fps timeline**, which is where all of this comes
from. A viewer reported "a glitch in the first second" and it was three separate
faults stacked:

1. **The crop must be subpixel.** The rest of the repo has known this forever;
   the video path was written with `int()` on the crop box and `//2` on the
   origin, so the push moved in whole-pixel steps — and a whole-pixel translation
   of an entire detailed frame is a large, visible jump (5x the normal
   frame-to-frame delta). One float `warpAffine` does the crop and the scale
   together.
2. **Sample at fractional positions and blend.** Rounding to the nearest source
   frame repeats every sixth one, and a repeat is a *dead* frame — motion stops
   for one frame in six. With an integer crop those repeats were pixel-identical.
   Blending the two neighbours keeps motion continuous; the weight never exceeds
   0.5 at 25→30 so there is no ghosting.
3. **`_prepare` could collapse the buffer to one pixel wide.** `int(sw * s)`
   truncates, and when the source is exactly the frame's aspect it lands one
   pixel *under* the target — `x0` goes to −1, the negative index wraps, and the
   crop silently returns a 1px sliver. It bites at `zoom=1.06` and not at
   `1.12`, so it sat latent behind a default. Ceil, and clamp.

Measured on the opener: frozen frames went 26 → 0, and the min/median
frame delta from 0.14 to 0.53. **If a clip ever looks like it stutters, measure
the per-frame delta series first** — a periodic dip is an fps artifact, an
isolated spike is a crop step, and real motion has neither.

## Thumbnail

`render_thumb(headline=, subline=, image=, accent=)`. **No zoom, no focus, no
watermark** — the first two are searched and the third was removed.

- **Brackets mark the accent phrase**, which gets a solid vibrant box:
  `"Nobody has [passed it]"`. Every reference thumbnail that works does this;
  the box is what the eye lands on first, and a headline with no focal word is
  a wall. `accent` is `red` / `yellow` / `orange` / `blue` / `cyan` —
  deliberately **not** the brand palette, which is low-contrast against the
  channel's own dark imagery and disappears in a grid.
- One box per *run* of accent words, not per word. Per-word boxing leaves a seam
  of background between them and reads as a rendering fault.
- **The accent must land on one line**, and the size search enforces it: it
  takes the largest size at which the whole accent run sits on a single line,
  falling back to merely fitting if no size does. An accent that wraps draws two
  plates on two lines and loses the single focal point the device exists for.
  Nothing to tune per thumbnail.
- **The box is sized from the cap band**, not the line box, so uppercase sits
  optically centred in it. A font's line box carries ascender and descender room
  that caps never use, and padding that left the words riding high in the plate.
- **No subline.** A second smaller line under the headline was tried and cut:
  the headline is the whole hook, and a subtitle competes with the video title
  sitting directly beneath the thumbnail anyway.
- **Ask what the title does not.** The title carries the search phrase; the
  thumbnail spending its words on the same question wastes half the click
  decision. `Does Tinnitus Go Away?` as the title, `Which kind do you have?` on
  the image.
- **No watermark.** The channel name is already under the thumbnail everywhere
  it appears; a mark on the image is a tell of a template.
- **The scorer loses to the subject.** `render_long(thumb_side=)` overrides the
  searched side, and on Saylor it was used: the two sources that scored clean
  are him twenty years ago, and a thumbnail is a promise about who the video is
  about. The +0.91 on the shipped one is a studio backdrop's lettering, which
  the eye reads as a flat blue field. Look at the render before believing
  either the score or the override — but note that **all three thumbnails so
  far ship overridden**, which says as much about the scorer as the pictures.

### The layout is searched, and the search is the point

The question is **not** "where is the person" — it is **"where is the picture
empty enough to take type"**. Two attempts chased the subject and both failed
the same way: a face cascade finds a head, and no multiple of a head describes
the arms, hair and torso that actually collide with words. The second attempt
reported a clean layout while the type sat across a woman's chest, because the
box was honest about her face and wrong about her.

So `_layout` scores candidates on a blurred edge-energy map: **quiet under the
words, busy beside them** (`quiet - 0.6 * busy`), with a detected face under the
type treated as fatal. It searches zoom x pan x **side x vertical band** and
takes the best. A negative score means the composition works; positive prints a
warning.

**The band matters as much as the side.** Placing the block dead centre and only
choosing left or right ignores half the question — on a subject who fills the
lower frame the space is up in a corner, not beside them. Bands are top, middle
and bottom, scored over the region the type will actually occupy rather than the
whole column.

**Use the scorer to choose the source.** That is the real workflow now — run
`_layout` over a batch of candidates and read the scores, rather than eyeballing
one. The tinnitus thumbnail's source was picked that way: every image in the
site library scored "busy", so a batch of stock was fetched and scored and the
best one taken. Scoring is far more reliable than looking at a full-size file,
because the failure only shows at feed size.

Brightness is normalised toward a target rather than dimmed by a fixed factor —
a flat 0.80 crushed the dark portraits this selects for into near-black.

## Do not

- Mass-produce. The strategy doc caps this at 15–20 videos across both sites for
  a reason: 130 templated explainers is the pattern YouTube suppresses, and
  three minutes cannot coast on a good first line the way 35 seconds can.
- Give financial advice, or imply one. Route to the article.
- Generate scripts from MDX automatically.
- Promote a candidate voice to approved without being told to.
- Present the landscape safe box or `max_upscale=1.90` as settled. Both are
  `GUESS` in `core/frame.py` until checked on a real upload at full-screen size.
- Quote `views.json` as evidence about video. It is SEO demand.
