# Long-form strategy — YouTube explainers for thecrypto.wiki and tinnitushelp.me

Plan for `/video-crypto` and `/video-tinnitus`. Written 2026-08-11,
before any of it is built. Grounded in the two sites' own traffic data and in a
count of what pictures actually exist, not in general video advice.

The premise: turn site posts into 2–4 minute 16:9 YouTube videos, link the post
from the description, and embed the video back into the post.

## What the SEO claim is actually worth

Four separate claims travel together under "video helps SEO". They are not
equally true and the plan depends on separating them.

**An embedded video does not raise the post's ranking.** There is no evidence
video embeds are a ranking factor. What people mean by this is usually the video
rich result — the thumbnail beside the blue link. Since Google's August 2023
change those are shown mainly where video is the **main content** of the page. An
article with a supplementary embed generally does not qualify. Add `VideoObject`
markup anyway — it feeds the Video tab, Discover and key moments — but **do not
budget for a search thumbnail**.

**The embed is a live Core Web Vitals risk, and CWV is a ranking input.** A stock
YouTube iframe is roughly 500 KB–1.5 MB across several third-party origins. Put
that on 130 pages naively and it plausibly costs more than the video gains. The
facade is not an optimisation, it is the condition of doing this at all — and the
poster is served from our own `public/` as WebP, so the page makes **zero**
third-party requests until someone clicks.

**The genuine upside is YouTube as its own search engine.** "how to build a
mining rig" and "brown noise vs white noise for tinnitus" are queries people type
into YouTube. A three-minute answer can rank there and reach an audience the site
never touches. That is real incremental discovery. It is not SEO for the site.

**Referral traffic back to the site will be small.** Description links convert
well under 2% of views in most niches; YouTube is built to keep people on
YouTube. The case for this work is a second discovery surface, brand, and — for
tinnitus — app installs, which `/video-tinnitus` already identifies as the
better conversion than blog traffic.

### The risk that outweighs all of it

YouTube's inauthentic-content policy targets mass-produced templated AI-voiced
slideshows precisely. Both short skills already carry *volume is the failure
mode*. Long-form makes that worse, not better: 35 seconds can coast on a good
first line, three minutes cannot. A channel that trips this is suppressed
wholesale, not partially.

**Therefore: 15–20 videos on demand-ranked pages, not one per post.** Decided.

### The only long-form data we have, and why it does not transfer

The drone channel's numbers say long-form loses badly there — five long-form
videos since Jan 2026 took 1,518 views combined while 30 Shorts took 19,566, and
the best long-form film ever made did 727. That is real, and it is **not**
evidence about this format. Those are scenery films competing on browse and
suggested; these are query-answering explainers competing on search. Different
demand, different retention curve. Cite the drone numbers only as a warning that
long-form is not free, never as a forecast for these two channels.

## Demand ranking — where the pilot goes

From each site's own `views.json`, which measures **SEO demand, not video
appeal**. Same caveat the crypto skill already carries: this says what people
search for, not what they will watch.

**Done so far, in ranking order:** `how-to-build-a-mining-rig` (1510),
`understanding-crypto-exchanges` (1038) and, off-ranking,
`crypto-ogs/michael-saylor` and the Satoshi proof post. Next by demand is
`exchanges/cryptocom` (380) — note it is an *exchange* page rather than a post,
so it is the first one that would be a review rather than an explainer, and
that is a format question worth settling before building it. `crypto-ogs/satoshi-nakamoto` (372) is
already covered by the proof video on a different page.

| thecrypto.wiki | views | tinnitushelp.me | views |
|---|---|---|---|
| posts/how-to-build-a-mining-rig | 1510 **done** | blog/celebrities-with-tinnitus | 482 |
| posts/understanding-crypto-exchanges | 1038 **done** | blog/the-gamers-guide-to-preventing-tinnitus | 351 **done** |
| exchanges/cryptocom | 380 | blog/tinnitus-in-history | 279 |
| crypto-ogs/satoshi-nakamoto | 372 | blog/pulsatile-tinnitus-why-you-hear-your-heartbeat | 257 |
| posts/crypto-etfs-explained | 362 | zen/morning-sounds | 256 |
| posts/what-is-proof-of-stake | 317 | blog/your-tinnitus-as-stressometer | 245 |
| exchanges/okx | 304 | blog/airpods-and-tinnitus | 219 |

Note both lists contain pages that are **already the answer to a YouTube query**,
which is the filter that matters more than the pageview number: a mining rig
build, a pulsatile tinnitus explanation, a proof-of-stake definition.

**One video goes on one post: its own. Decided 2026-08-16, against the earlier
recommendation here.** The idea was that eight to ten videos, each spread to
three or four neighbouring posts, buys the same page coverage at a quarter of
the production. The user's call is that it does not, and the reasoning holds up:
the coverage it buys is fake. A mining rig explainer under an article about
proof-of-work is a video that does not answer the page's question, so it earns
a worse click-through *and* a worse impression of the site than no video at all
— and the page-coverage number it improves was never a real metric, because an
embed is not a ranking factor (see the top of this document, which says so
plainly two sections earlier). Spreading optimises the one thing we already
established is worthless.

The registry's `alsoOn` field stays in place and stays empty. It is one line in
`lib/videos.js` and costs nothing; ripping it out would only make the decision
harder to reverse if a video ever genuinely does answer two pages.

## The constraint that decides the format

Counted, not assumed:

| | posts | images on the site | distinct images **per post** |
|---|---|---|---|
| crypto | 61 posts, 27 exchanges, 33 OGs | 147 post images, 26 exchange logos | 3–5 |
| tinnitus | 69 posts, 10 zen albums | 110 | **2–3** |

At the measured pace (2.9–3.1 words/sec with `gap=0.34`) a 2:30 video is ~440
words and a 4:00 video is ~700. At a 5.5s mean shot that is **27 to 44 shots**
against 2–5 available photographs.

**So 85–95% of the picture cannot come from the post's own images.** This is the
whole design problem, and it is a statement about *pictures*, not about scripts:
a long version is free to reuse a short's angle and material — that angle is
usually the best one the article has — but it cannot reuse its picture budget.
`ChecklistShot` carries one beat in a ten-shot short; here the drawn beats have
to carry roughly half the runtime.

Two things make that tractable rather than grim:

- **The structured frontmatter is already there.** `quickFacts` and `faqs` on all
  27 exchange and 33 OG files; `faq` and `sources` blocks on the tinnitus posts.
  The crypto skill already flagged this as where the format scales — comparison
  and quote beats become a data problem instead of a design one.
- **Tinnitus has `nebula_canvas`** — infinite, on-brand, zero-licence procedural
  picture, already built and already measured for subpixel drift.

Budget to aim for: ~30% site photographs, ~50% drawn beats, ~20% procedural or
Commons-sourced (people only, per the crypto skill's rule).

## Motion — where the other 85% of the picture comes from

The user's instruction is to use anything that makes these more engaging:
footage, graphics, sound. The shot-count arithmetic above says the same thing
from the other direction. So the sources, ranked by how well each survives the
question *"is this stock-footage-with-narration?"*:

1. **The site's own photographs**, in the framed-card treatment above. Already
   licensed, already attached to the post. 2–5 per video.
2. **Drawn data beats** — `checklist` today, plus `compare`, `stat`, `timeline`,
   `quote`, `bars`, `chapter`. **This is the differentiator and it should carry
   the largest single share of runtime.** It shows the argument rather than
   illustrating it, it is native 1920 so it never upscales, and it is built from
   the frontmatter the sites already carry.
3. **Procedural backdrops.** `nebula_canvas` already exists for tinnitus and is
   infinite, on-brand and licence-free by construction. Crypto has no equivalent
   yet; the drifting gold grid inside `ChecklistShot` is the seed of one.
4. **Licensed stock video** — Pexels and Pixabay both offer a free API,
   commercial use, no attribution required. Real motion, 1080p and 4K, which is
   the one thing none of the sources above provide.
5. **Public-domain archive** — NASA for the tinnitus space motif, Wikimedia
   Commons, Internet Archive. Free, and unlike stock it is often *specific*.
6. **Synthesized SFX.** `core/sfx.py` generates rather than sources, and its two
   marks are one parameterised instrument. Extend the same way: a whoosh on a
   chapter card, a riser into a reveal, a soft landing under a `stat`.

**The rule that keeps this out of the pattern both platforms suppress:** stock
is texture *under* the argument, not the argument itself. A stock loop blurred
and dimmed behind a data graphic is a backdrop. Thirty stock loops in a row
under an AI voice is the thing the crypto skill already bans, and adding
narration does not change what it is. If a video's runtime is mostly items 4 and
5, it has failed, regardless of how good the individual clips are.

This is a deliberate widening of the shorts' "do not reach for a stock API"
rule, made on the user's instruction and scoped to long form. The reasoning
behind the original rule is not wrong — it is that generic stock cannot carry a
piece. It still cannot. It can support one.

## What Phase 2 settled

Built: `core/brand.py`, `core/draw.py`, and `video_automation/longform/`
(`beats`, `plan`, `audio`, `meta`, `thumb`, `build`). Five drawn beats —
`chapter`, `checklist`, `stat`, `compare`, `quote`. What the frames taught:

**The split layout inverts the resolution problem.** Content in a left column,
the post's photograph in a ~660px right column. A 900px source in a 660px column
is a *downscale*, so the more runtime the drawn beats carry, the sharper the
whole video gets. The arithmetic already wanted them to carry most of it; this
means there is no quality cost for doing so. Do not "fix" a beat by giving its
photograph the full frame.

**Cut between drawn beats, dissolve between photographs.** The shorts' rule —
always dissolve, because the piece is one continuous argument — is a rule about
*photographs*. Dissolving a pull quote into a checklist cross-fades two sets of
type through each other and reads as a rendering fault, not a transition. Both
were legible at once on the first build. Chapter cards cut on both sides
regardless: the hard reset is why they are worth their two seconds.

**The drifting grid only belongs on a flat panel.** Its tint is a near-black
picked against the shorts' dark backdrop; over a bright blurred photograph the
same lines are plainly visible and the beat reads as graph paper. The grid
exists to stop a flat panel looking like the video has stopped, which is not a
problem a photograph has. Over a photo the backdrop drifts instead — better
motion, one less thing drawn.

**Measure the block, then centre it.** Every beat was first laid out from fixed
fractions of frame height, and every one of them left the bottom 40–50% of a
16:9 frame empty. Wrapping decides how tall the content is, so the content has
to be measured before it can be placed.

**A chapter card gets zero room if you compute it the obvious way, and fails
silently.** `build_narration_aligned` holds every caption until the next one
starts (`voiceover.py:488`), so a sentence's last caption *ends where the next
sentence begins* and `sentence_spans` comes back perfectly contiguous — the
silence a section boundary bought is already inside the previous span.
`next_start - prev_end` is therefore exactly zero, always. The first build
emitted no cards at all while still reporting three chapters, which is the worst
kind of bug: the log looked right. The silence is recoverable only because we
know how long it is — sentence `i`'s true audio end is its span end minus
`gaps[i]` — which is why `lay_out` takes the gap list and is not optional.

**The chapter validator earns its place immediately.** It caught the smoke
test's own opening chapter running 5.7s against YouTube's 10s minimum. All three
chapter rules fail silently on upload: get one wrong and the timestamps render
as plain text with no warning anywhere.

**Audio measured, with a caveat.** The bed loops correctly (a 12s track under a
31s video) and lands the exact duration. Through the chapter-card silence the
bed sits at full strength (−25.0 dB); under speech the voice runs ~9.5 dB over
it, against the 3 dB the tinnitus build found unintelligible. **These numbers
come from a sine tone, not music** — the sidechain only moved the bed ~1.8 dB,
and a real track with transients will behave differently. Re-check the ducking
depth on the first actual Audio Library track.

## What Phase 3 settled

Skills `/video-crypto` and `/video-tinnitus`, symlinked into
`~/.claude/skills/`. First pilot built: `projects/crypto-long/satoshi-proof.py`,
from the same post as the `crypto-satoshi-proof` short, reusing its angle and
going deeper — three minutes has room for the verification procedure and the
2019 "valid signature, wrong address" case study, which the 35-second version had
to drop.

**`crypto-satoshi-proof-long` — 2:13, 1920x1080, seven chapters, `mia`, −14.4
LUFS, −1.4 dBTP.** All seven chapters clear YouTube's 10s minimum. Renders in
about ten minutes.

**2:13 is under the 2:30–4:00 target and the script is why.** ~450 words against
the 440–700 the spec calls for, and the seven chapter cards give back 14s of the
runtime rather than adding to it. Not a fault in the engine; the next script
should carry two or three more beats per section.

**Callouts have two rules, and both were found on real frames.** A callout on a
drawn beat is dropped — the shorts' rule, which should have been carried over
from the start, because the beat's items already *are* the type. And a callout
cannot outlive its own sentence's audio, or it burns straight across the silence
the next chapter card lives in. Four of the pilot's first five callouts did
exactly that. The trap is that the natural callout line is each section's
punchiest closer, which is the line a script also tends to give a `stat` or
`quote` to — so three of five were silently dropped once the first rule landed.
**Pick callouts from lines whose shot is a photograph.**

## What the first review changed

The pilot was watched and came back with seven notes. All seven are built; the
three that taught something general:

**Stock has to be screened, not searched.** Taking Pexels' top result for
"bitcoin blockchain abstract" put a novelty dinosaur, a sticker on a pine table
and a rainbow of cables into a gold-on-near-black video. `stock.screen()`
measures mean luminance and saturation, and `MAX_LUMA=48 / MAX_SAT=50` is the
box both sites' palettes need. The keepers measured L4/S5, L14/S6 and L41/S20 —
the rejects L86/S44, L91/S62, L36/S94. Build a preview sheet and look at it: the
query has almost no bearing on what comes back.

**The stock rule is reversed for long form, and the reversal is arithmetic.**
Both short skills say never reach for a stock API. That still holds for a
thirty-second short built from three pictures. At thirty shots against a post's
three to five images, building only from the archive means every video on the
channel contains the same photographs — which is its own sameness. What survives
is the real rule: **stock supports, the site's images and the drawn beats lead.**

**Speaking the chapter titles paid for itself twice.** The card used to sit in
2.4s of silence, six times over — most of why the first cut ran short of its own
target. Reading the title fills the hole at no extra screen cost and puts the
section headings into the SRT and YouTube's transcript as real text.

Also: the watermark moved from y=150 to y=62 (it was colliding with the pictures
and the beat kickers, and a 16:9 player puts nothing there), beat kickers moved
to y=214 for the same reason, the music bed is now generated by `core/music.py`
rather than fetched, chapter transitions carry riser/impact/whoosh, drawn beats
tick as items arrive, numeric `stat` values count up, and the outro's URL came
off the card and went into the voice — the watermark already carries it.

## Format spec

| | short (built) | long (this plan) |
|---|---|---|
| frame | 1080×1920 | **1920×1080** |
| runtime | 30–60 s | **2:30–4:00** |
| words | 105–175 | **440–700** |
| shots | ~10 | **27–44** |
| captions | every line burned | **SRT + key-line callouts** |
| structure | one angle | **sections → YouTube chapters** |
| audio | voice + synth SFX | **voice + music bed, sidechain-ducked** |
| deliverables | one MP4 | MP4, SRT, 1280×720 thumbnail, metadata sidecar |

**16:9 is *not* kinder to these images — corrected during Phase 1.** The first
draft of this document claimed a landscape source drops into a landscape frame
for free, reasoning from height. The binding constraint is width, and measuring
the libraries settles it:

| library | n | min | median | max | ≥1920 wide |
|---|---|---|---|---|---|
| crypto/posts | 147 | 660 | **900** | 1920 | 1 |
| crypto/exchanges | 27 | 350 | 900 | 2000 | 2 |
| crypto/crypto-ogs | 32 | 334 | **500** | 1057 | 0 |
| tinnitus | 108 | 600 | **750** | 1000 | 0 |

Reaching 1920 wide asks 2.1× of a median crypto image and 2.6× of a median
tinnitus one. At the shorts' `MAX_UPSCALE = 1.45` the photograph occupies **65%
of frame width and floats in blur** — the exact failure the crypto skill records
for sources under 750px.

What actually changes between the two formats is **how large the frame is
drawn**. A 9:16 short fills a phone's height, so its picture is displayed at
close to 1:1 and 1.45 is honest. A 16:9 video is a ~390px-wide card in the feed
or ~844px full-screen on the same phone — roughly half the linear resolution for
the same source. So the ceiling can rise for landscape without the softness
showing, and `max_upscale` now lives on the `Frame`.

Compared on real frames at 1.45 / 1.90 / 2.15 and **1.90 taken** (85% of frame
width). 2.15 reaches 96% but leaves a sliver of backdrop that reads as an
accident rather than a border, and is softer for it. At 1.90 the residual blur
band plus the existing gold hairline read as a deliberate framed card. Marked
`GUESS` until it is checked on a real upload at full-screen desktop size, which
is the harshest case and the one none of this reasoning covers.

**A one-off super-resolution pass over both libraries would remove the
constraint entirely** and would improve the vertical shorts too — it is the
obvious follow-up, not a Phase 1 concern.

**The safe area changes completely.** The 9:16 union box (`SAFE_TOP=230`,
`SAFE_BOTTOM=1440`, clear of `x>860`) is about TikTok and Reels chrome and means
nothing here. What matters on YouTube is the bottom band the progress bar and
title occupy on hover, and the four end-screen zones in the final 20 seconds.
Anything drawn must clear both, and `render_shots` should raise rather than ship
outside them — same discipline, new numbers.

**Captions: SRT plus key-line callouts.** Decided. Full burned captions for three
minutes fight every drawn beat for the same space, and the drawn beats are what
buy the runtime. Instead: an uploaded `.srt` (YouTube indexes uploaded captions,
and ours are exact where auto-captions guess), plus a burned lower-third on the
five to eight lines that carry the argument. The `Caption` objects
`build_narration_aligned` already returns are the SRT, so this costs almost
nothing to produce.

**Music: YouTube Audio Library.** Decided. Free, cleared for use in YouTube
videos, which covers the site embed too because the embed *is* the YouTube
player. Two things to respect: some tracks require attribution — check per track
and put it in the description — and **the clearance does not extend to reposting
the same cut to TikTok or Instagram**. If a long cut is ever repurposed for
another platform, the bed has to be stripped or replaced.

The ducking is already solved and measured in `asmr.py`: bed at
`loudnorm=I=-23` with `sidechaincompress threshold=0.03:ratio=8`. Reuse it rather
than re-deriving it. A static mix was tried there and left 3 dB over the
narration, which is not intelligible.

**End on the post, not on a question.** The shorts end on a question because
comments are the cheapest engagement signal a 35-second piece can earn. Long-form
has an end screen: reserve a 15–20 s outro card, point at the article, and give
the end-screen elements somewhere to sit.

## Build plan

### Phase 1 — make the engine frame-agnostic

`OUT_W, OUT_H` are module globals in `core/vertical.py` with 42 references across
`vertical.py`, `crypto/shots.py` and `tinnitus/asmr.py`. Introduce
`core/frame.py` with `LANDSCAPE` (1920×1080) and `VERTICAL` (1080×1920) and
thread a frame through `PhotoShot`, `render_shots`, `ChecklistShot` and the
caption sprites.

Not a rewrite — mostly two files — but it touches shipped code, so: **change one
thing per round**, and re-render `crypto-saylor-treasury` afterwards to confirm
the vertical output is unchanged frame for frame.

### Phase 2 — `video_automation/longform/`

- **`Section`**, one level above `Shot`: a title, its sentences, its shots. This
  is what generates chapter timestamps, and it is the reason sections exist at
  all rather than one flat list.
- **New graphic beats**, alongside `checklist`: `compare` (two columns — brown vs
  white noise, spot vs futures ETF), `stat` (one number, held), `timeline`,
  `quote` (straight out of the tinnitus `sources` frontmatter, with attribution),
  `chapter` (the section card), and `bars` (frequency content, genuinely on-topic
  for tinnitus rather than decorative).
- **Music bed** — port `render_bed` and the sidechain chain from `asmr.py`.
- **SRT writer** off the existing `Caption` list.
- **Thumbnail**, 1280×720, from the post hero plus large type in the site palette
  (crypto gold `#e5c200` on `#171717`; tinnitus `#5B3964`/`#ffdab9`). For
  long-form the thumbnail outweighs almost everything else in the pipeline.
- **Metadata sidecar** — title, description with the post link in the first two
  lines, chapter timestamps, tags, and any required attribution (Commons
  portraits, Audio Library tracks). YouTube's chapter rules: first chapter at
  `0:00`, minimum three, each at least 10 seconds.

Watch render time. Every frame is drawn in Python; 4:00 at 30fps is 7,200 frames
against ~1,800 for a one-minute short. Expect roughly 8–12 minutes a build and
consider caching prepared layers per shot.

### Phase 3 — the two skills

`/video-crypto` and `/video-tinnitus`, symlinked into `~/.claude/skills/`
like the others, plus per-video scripts in `projects/crypto-long/<slug>.py` and
`projects/tinnitus-long/<slug>.py`.

**Keep the hand-written script.** Both short skills say it and it is more true
here: the script is the product, and automated script generation across 130 posts
is the failure mode by another route.

### Phase 4 — the site side

**crypto-wiki** (Next.js, `next-mdx-remote`): add `layouts/components/PostVideo.js`,
register it in the `mdxComponents` map used by `layouts/PostSingle.js`, and emit
`VideoObject` through the `jsonLd` prop `layouts/Baseof.js` already accepts.

**tinnitus-blog** (Next.js + TypeScript): add `src/components/MDX/YouTube/`,
register it in the `components` map in `src/components/MDX/index.tsx`, and use the
existing `JsonLd` component.

Both: frontmatter `video: { id, title, uploadDate, duration }`; facade embed with a
locally served WebP poster (the `/webp` skill already exists for this); and a video
sitemap entry alongside the existing `next-sitemap` config — which does not do
video extensions natively, so it needs an explicit path.

`VideoObject` needs `name`, `description`, `thumbnailUrl`, `uploadDate`; add
`duration` (ISO 8601), `contentUrl` and `embedUrl`. `uploadDate` must be truthful.

### Phase 5 — pilot and measure

Two videos, one per site, on the top-demand page. Then **stop** and measure with
`/youtube-audit` after 30 days before building the other eighteen.

Both channels are new and Shorts-only today, so there is no long-form baseline on
either. The audit skill already refuses to rank below five videos with data — that
rule applies here too. Two videos will show whether anyone watches past 30
seconds; it will not show a pattern.

What to actually look at: retention at 0:30 and at 50%, whether YouTube search is
a traffic source in the analytics at all, and site referrals from YouTube in the
site analytics. The last one will be small — see above — and a small number is not
a failure of the format.

## Do not

- Mass-produce. 130 templated explainers is the pattern YouTube suppresses, and
  the reason this plan caps at 15–20.
- Present a video embed as a page-ranking gain, or promise a search thumbnail.
- Ship a raw YouTube iframe. Facade with a local poster, or do not embed.
- Give financial advice in a crypto script or make a medical claim in a tinnitus
  one. Same YMYL rules the short skills already carry.
- Quote `views.json` as evidence about video. It is SEO demand.
- Repost a music-bedded long cut to TikTok or Instagram — the Audio Library
  licence does not cover it.
- Generate scripts automatically across the back catalogue.
- Promote a candidate voice to approved without being told to. Still unsettled on
  both channels.
