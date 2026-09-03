# Long-form engine (16:9)

The 2-4 minute explainer: shape, chapters, timing, the opener and the outro.
Shared by crypto and tinnitus. Drone long form is a different engine entirely -
see `projects/drone-long.md`.

## The shape

| | value | why |
|---|---|---|
| frame | 1920x1080 | `core.frame.LANDSCAPE` |
| runtime | **2:30–4:00**, and see below | under 2:30 sits awkwardly between Shorts and long form; v1 shipped at 2:47 |
| words | 440–700 | **`mia` runs 3.25 words/sec, measured — see below** |

**Estimate the runtime from 3.25 words/sec, not 2.9, and this replaces the
figure this doc used to give.** The 2.9 was an early guess and it is wrong by
enough to matter: the `who-controls-bitcoins-price` script was first drafted at
940 words, which 2.9 predicts as a plausible 5:20 and which would in fact have
run past six minutes. The number to trust is the one the shipped cuts measure -
`crypto-exchanges-long` is **718 words plus 42.2s of written gaps, delivered at
263.21s**, which is 3.25 words/sec with the chapter cards already inside it. So:

    seconds = words / 3.25 + sum(gaps)

Predicted 4:06 for the 656-word bitcoin-price script; it rendered at 4:06.
**Check the arithmetic before rendering, not after** - a long-form render is
twelve minutes and a script that is 40% too long is 40% too long in every one
of them.

**The word count assumes `gap=0.34` everywhere, and you should not be writing
that any more.** Written pauses cost real time: the crypto-exchanges cut went
4:07 -> 4:23 on gaps alone, ~16s across 55 sentences, and the video is better
for every one of them. Budget roughly **0.3s per sentence** on top of the words
when estimating, or write the script at the low end of the range. Do not buy the
runtime target back by removing pauses — a monotone 3:50 is worse than a
well-punctuated 4:20, and the ceiling was never a hard platform limit.
| shots | 27–44 | ~5.5s mean |
| captions | **SRT only, none burned** | see below |
| voice | `mia` (`af_heart`) female, or `otis` (`am_puck`) male | both **candidate, not approved**; see the project docs |

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

## The YouTube title is a search query, not the Short's hook

The `Meta` title (the video's YouTube title - not the chapter cards, not the
on-screen title stamp) must be a phrase a person actually types into YouTube
search: "How to sleep with tinnitus", "Why is tinnitus worse at night", "What
is proof of stake", "proof of stake vs proof of work". It must **not** be the
Short's curiosity or challenge hook reworded onto the long form.

The reason is distribution, not style. YouTube runs Shorts and long-form on
separate ranking systems and evaluates per video, so the Short is not holding
the long-form back - but a new long-form gets almost no browse or suggested
traffic and is found by search or not at all. The one long-form on either
channel that has beaten its own Short ("How to Sleep With Tinnitus", 95 views
to 36) has a title matching a real high-volume evergreen search; the ones stuck
at 0-12 views have titles nobody searches ("Who Controls Bitcoin's Price? Not
Who You Think", "Quantum Computers vs. Crypto: What Actually Breaks").

Pick a different query angle from the Short, so the two are not competing for
one search-results page (YouTube rarely shows two videos from one channel
back-to-back on a single query). Full reasoning in the `youtube-audit` skill.

## The screen has to say what the voice is saying

**The user's standing note, from the quantum-computers cut, where they flagged
three separate spots by timestamp: "we need to make sure the visuals and the
voice over match and the whole video is easy to follow and easy to understand —
this is the main idea, all topics should be easy to understand".** An explainer
whose pictures do not track its words is a voice memo over wallpaper, and an
abstract topic (cryptography, keys, a mechanism) cannot be followed without the
screen reinforcing each beat. Three rules come out of it:

- **Every clip carries a `payload` line.** `Shot(clip=..., payload=("", "one
  short line"))` — the big centred statement, stating the point of *that*
  sentence. A stretch of generic stock playing silent under a specific claim is
  the failure the user notices every time. This is `footage.md`'s "label your
  video clips" promoted to a hard rule for anything abstract: the countdown clip
  says "No credible date before the 2030s", the archive clip says "Now it is on
  the record, forever". The kicker half stays empty; one line is the whole job.
- **Match the noun.** The picture names the same thing the sentence does, or it
  is labelled so it does. An image the user calls "not fitting" gets replaced,
  not defended — `footage.md`'s "say the noun the narration says", enforced.
- **Drawn beats and labelled clips lead; unlabelled photos are connective
  texture only.** A `PhotoShot` cannot take the centred statement without it
  fighting the Ken Burns, so a photo under a mechanism line has to be carried by
  the beat or the clip on either side of it. If a section is mostly unlabelled
  photos under specific claims, it will read as hard to follow.

## Choose the beats before writing the script

`does-tinnitus-go-away` shipped with four `checklist`s and they read as one
graphic four times — the crypto skill's silhouette rule, arriving here exactly
as it said it would. **List the beats first and check no two share an outline.**
The gaming cut uses each shape once: `quote`, `grid`, `bars`, `stat`, `compare`,
`steps`, one `checklist`.

`bars` is the beat this site's posts keep earning. Half of them carry a table of
figures against a limit — decibels against safe exposure time, one album's
energy against another's — and a proportion is the one thing narration cannot
say. Two notes from building one: the value text travels with the end of its
bar, so a full-width top row pushes its own label off frame (scale the whole set
by one factor and the proportions stay exact); and a `stat` for the same number
is weaker, because a figure with no scale behind it is just a figure.

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

## `Section.number` puts a big numeral on a chapter card — for a counted series only

**`ChapterCard`'s own docstring bans a numeral before every title, and that
rule is unchanged.** A numbered agenda tells the viewer they are being
lectured. `number` is the one deliberate exception: a script that is
genuinely enumerating something and *says the number out loud* ("myth one",
"myth two") gets it on screen too, because the viewer is already tracking the
count — the user's note on the myths cut was exactly this, that the count
should show when the narration says it.

Pass `Section(number=1)` only on sections where `spoken_title` (or the
narration right after the card) actually says that number. A numeral with no
matching word is right back to being a slide deck; that is the whole
distinction between this and the agenda pattern the beat refuses to draw by
default. It draws above the card's rule, sized off the title (`NUM_SCALE`,
`NUM_GAP` on `ChapterCard`), and the whole group re-centres around one
vertical middle rather than pushing the title down.

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

## No burned captions

`callouts=None`. Showing a handful of lines and not the rest reads as
arbitrary, which is what a viewer noticed immediately. The full transcript ships
as the SRT — YouTube indexes it and viewers can switch it on. The reference
channel puts nothing on screen but labels and arrows either.

## Two things that put the silence cut 25% over its ceiling

Both found on `can-silence-make-tinnitus-worse`, which preflighted at **5:10
against a 4:00 ceiling** on its first complete draft. Neither was fixed by
shaving gaps, and trying that first wasted a pass.

**A chapter's `spoken_title` is already the beat's hinge - do not write a
lead-in sentence as well.** The `grid` section opened with
`spoken_title="And there are three of these stacking up together."` and then a
first sentence reading "Three different problems, with three different fixes."
That is the same sentence twice, 3.5s apart, and the second one exists only
because "say the point, then show the graphic" was applied without noticing
the card had already said it. Deleting it improved the writing and bought back
more time than every gap in the section put together. **Check every beat whose
section is carded**: if the spoken title hands off to the graphic, the beat's
own first chunk is the next thing that should be heard.

**Cast clips by duration before writing them into the shot list.** Eight of
thirty-four slots failed preflight on the first pass, all the same way: a 6.0s
traffic clip under a 9.4s sentence, an 8.4s clip under a 10.4s one. The slot
length is not knowable until the narration is measured, but the **clip
lengths are knowable immediately** - `ffprobe` the whole folder once and keep
the long ones (20s+) for the paragraphs and the short ones for the one-line
sentences. A clip that is short can still be used twice at different
`clip_at`; a clip that is short in the wrong slot is a re-render.
