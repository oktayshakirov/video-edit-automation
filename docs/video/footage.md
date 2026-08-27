# Footage: stock, photos, screening

Choosing, screening and moving the picture. The single largest source of
re-cuts, which is why it is the longest doc here.

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
- **The luma box does not screen a screenshot, and a website screenshot is an
  infographic.** A line about a product should show the product, and the site
  owns two kinds of picture for that. `bitfinex-ui.png` measures L46 and
  `gemini-exchange-trading.jpg` L67 — both comfortably inside the box — and on
  the frame they are bright teal marketing pages with a promo bar and two
  hundred words of unreadable small type. **A UI is dark chrome carrying small
  bright text, so the mean reads dark while the eye reads bright**, and the
  legible content is the same objection the no-infographics rule already makes
  about diagrams. Both shipped into a cut and both had to come out.
  There is also a second problem with a *branded* homepage: a company's own
  page under a line about custody risk is closer to naming a platform than an
  explainer wants to be.
  What works instead is the **app**, unbranded: `portfolio.jpg` is a phone
  showing a coin list and balances, which is what a viewer pictures when they
  hear "your balance". Screen a screenshot by looking at it, not by measuring
  it.
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

## Screen a clip by watching it, not by looking at one frame of it

`woman-sitting-alone-dark-room-thinking/6073058` screened at L13-14 / S8 and
appeared on a labelled contact sheet as a woman alone under a single bulb in
an empty room - the exact subject of the script. It shipped into two cuts.
Played, she is **shaving her head**, which is a specific and arresting act
under a line about quiet rooms, and the user caught it in the first five
seconds of both videos.

The luma/saturation box measures brightness. A contact sheet at one timestamp
measures one four-hundredth of a clip. **Neither can see what is happening in
the shot**, and "what is happening" is the only thing that decides whether the
footage illustrates the line. Sample a few seconds of anything before it goes
in a shot list - this is the same failure as the green apartment block and the
unlabelled water, arriving through the one door those rules left open.

## A photograph bleeds off every edge, or it is not a full-frame shot

The silence cut put the site's `neurons.jpg` (900x599) in a full-frame slot.
Under `max_upscale=1.90` a 900px source cannot reach 1920, so it rendered
**fitted** - a letterboxed panel with a hairline and black bands above and
below - and the user's note at 0:54 was to remove that treatment completely
and show the picture full screen the way the one at 3:27 is.

So the rule is now absolute: **a photograph in a full-frame shot must be large
enough to bleed off all four edges.** Do the arithmetic before writing the shot
(source width x 1.90 must clear the frame width), and when the site's own
library cannot make it - which on both sites is most of the library - either
put the picture in a beat's picture column, where the same file is a
*downscale* at 660px, or use a stock source big enough. The picture column is
what that layout exists for; the fitted panel was never a design, only what
the renderer does when it runs out of pixels.

## Label a contact sheet, or you will pick the wrong clip

A green-lit apartment block shipped into a short under the line "rain, a fan,
or brown noise" because three rain clips were laid out in one sheet and read
back against the wrong filenames. It screened **L15 S17** — comfortably inside
the box — and green is the one hue that cuts hardest against both palettes.

Two things follow. **The luma/saturation box measures brightness, not hue**, and
a dark green passes it easily; hue against the brand is a separate judgement
the numbers will not make for you. And **put the id in the frame** when
building a sheet, or check each pick individually before writing it into a
shot list. The cost of being wrong is a shot nobody notices until it is in a
render.

## Screen the site's own pictures, every time

The library is much brighter than it looks in a browser and it decides the shot
list. Measured for the gaming cut: `gamer` L22, `live-music-show` L27,
`neurons` L24 — and then `headphones-2` **L206**, `research` L195, `relaxing-
woman` L173, `audiologist` L179. Only the first three could take the full frame;
everything else belongs in a beat's picture column where it is downscaled and
small.

**A blurred `backdrop` does not rescue a bright picture, it spreads it.** Two
beats in the first gaming cut used `research.jpg` and `megaphone-noise.jpg`
behind them and both rendered as a grey wall behind the type — the brightest
frames in a near-black video. Dropping the backdrop entirely is usually the
right answer: a flat panel with the drifting grid is what those beats were
designed for.

## Label your video clips

`Shot(clip=..., payload=("KICKER", "One line"))`. Stock footage is wallpaper by
construction — it was not shot for this script and cannot say anything
specific, so a stretch of it with nothing on top is the dullest thing in the
video. A kicker and one line in the same lockup the drawn beats use turns
wallpaper into a titled shot.

## A clip is over-used long before it is used twice

**Every note the user gave on the myths cut's footage was one of three
faults, and they compound.** The rules now:

- **No clip plays more than twice, and never twice inside a minute.** That
  cut ran `stressed-man.../6415592` three times and two more clips twice, and
  the note was that it "looks very repetitive". A second use is fine as a
  deliberate echo — the myths re-cut re-opens on its own opening face at the
  close — and a third is not.
- **No clip holds longer than about eight seconds.** Two slots ran 14.7s and
  10.4s and the user flagged the first one by timestamp. **The fix is usually
  not a longer clip, it is splitting the sentence**: both offenders were a
  single `Section` sentence with four or five caption chunks, which is one
  span and therefore one picture. Splitting "See a doctor if it is new, will
  not settle, sits in one ear only, or comes with hearing loss" into two
  sentences turned one 14.7s hold into two shots without touching a word.
- **Cast a clip against the line it sits under, then check the list for
  clips that are only atmosphere.** The skill already says a concert line
  gets a concert; the corollary is that a slot with no obvious subject is
  where a wrong clip hides.

**Adjacent Pexels ids are the same shoot, and nothing in the pipeline knows
that.** Searching for a replacement for `6415592` returned `6415611`,
`6415649` and `6415877` — all screened at L13-18, all perfect on the numbers,
and all *the same bearded man in the same black studio*. Using one would have
made the repetition worse while looking like a fix. **Treat a candidate whose
id is within a few hundred of a clip already in the cut as the same clip
until a contact sheet proves otherwise.**

## A clip already in the cache has *not* been screened. Sheet everything.

**This is the rule the myths re-cut broke while writing the rule above it.**
The second pass carefully contact-sheeted every *newly fetched* clip and then
reused a dozen cached ones on the strength of their folder names — and four
of those were wrong in ways no measurement could see:

| clip | folder name says | what it actually is |
|---|---|---|
| `man-sitting-alone.../7280519` | man alone, dark apartment | head in hands with **a row of beer bottles** on the floor — reads as drinking |
| `tired-woman-hands-on-face/7676117` | tired woman, studio | woman in a **surgical mask and black leather gloves** |
| `tired-woman-hands-on-face/7676122` | tired woman, studio | hair completely covering her face — horror-adjacent |
| `quiet-library-reading-dark/10480415` | quiet library | a **red-lit antique treasure map** and a magnifying glass |

The beer-bottle one shipped into a rendered Short under "it does not just
fade, it can last for years" and was only caught by looking at the finished
frames. **A folder name is the search query somebody typed, not a description
of the footage** — Pexels returned it, the luma box passed it, and nothing
between those two facts looked at the picture.

So: **build one labelled contact sheet of every clip in the shot list, cached
or fetched, before the first render.** Three timestamps across each clip, id
burned into the frame. It costs about a minute for a whole cut and it is the
only step that catches subject faults, which are the only faults the user
ever notices.

## Screening for brightness is not screening for who is in the shot

**The hook's two replacement faces repeated the exact fault they replaced.**
The first cut's opener was called out and swapped for two new clips; both
landed as Black actors, and with `TEMPLES` — also Black — as the very next
shot, the hook opened on three Black faces in a row. Nobody chose that
deliberately either time. It is a structural side effect of screening stock
purely on `luma`: a pale face against a dark backdrop is *brighter* by
definition than a dark face against the same backdrop, so the `MAX_LUMA`
ceiling this whole pipeline screens on rejects lighter-skinned candidates
more often. Every query tried afterwards — "caucasian woman", "man portrait
dark moody european", explicit ethnicity terms in the search string — kept
returning the same small set of darker-skinned actors, because the Pexels
tags on a clip are not reliable and the luma filter is doing the real
selecting underneath the query.

**So casting is a thing to look at on the finished contact sheet, not just
infer from a search query.** After screening a batch for brightness, look at
who is actually in it before writing the shot list, and count how many
people of the same appearance land in a row — the same discipline this doc
already applies to subject matter and to over-used clips, extended to who is
on screen rather than what they are doing.

**Two closeup faces back to back is the practical ceiling; three reads as a
wall of faces regardless of who they are.** The fix here was not "swap two
more faces for two different ones" — it was also removing the third shot
entirely and giving it to an abstract instead, so the hook is two people and
then a change of register, not three portraits in the same "studio, dark
background" setup.

**A shoot rejected for being over-used stops being over-used once nothing
from it ships.** `man-serious-portrait-dark-studio-black-background/6415611`
and its siblings were flagged on an earlier cut as "the same man as the
clip already over-used." By the time this fault was found, that whole shoot
had been removed from the video — so a single clip from it was a legitimate,
first-time use, not a repeat of anything. Re-check whether an old rejection
still applies before re-applying it; a stale "cannot use this" is as much a
bug as a stale "safe to reuse."

## An asset used in another video is not available to this one

**The user's rejection of the proof-of-stake cut, and it is a channel-level
rule, not a note about one video.** That cut was built entirely from assets
already shipped elsewhere — reasoning, wrongly, that "screen the cache first"
meant "prefer the cache". An inventory across all six crypto projects found
the channel recycling a pool of about fifteen files:

| asset | videos |
|---|---|
| `security-combination-lock.jpg` | **9** |
| `digital-technology.jpg` | 8 |
| `analysis.jpg`, `laptop-trading.jpg`, `futuristic-crypto-exchange.jpg` | 7 each |
| `server-room-data-center`, `digital-code-stream-dark`, `abstract-dark-waves-motion` | 7 each |

That is precisely the templated sameness `docs/long-form-strategy.md` says
gets a channel suppressed, and it arrived through the back door of a rule
written for a different purpose. **The cache exists so a rejected clip is not
re-fetched and so a build is reproducible — not as the shot list's shopping
list.**

So, before writing a shot list: **inventory what the other videos already
use, and treat those files as unavailable.** One command does it — grep
`STOCK / "videos/...` and `POSTS / "...` out of every project file and count.
A handful of genuinely brand-level assets are exempt (the `subscribe` sting,
the backdrop, the music track); everything else is per-video.

**Corollary, measured: the site's own image library is exhausted for
thecrypto.wiki.** Of 147 post images, only fifteen unused ones pass the dark
box at all, and every one is disqualified on grounds already in this doc —
brand logos (`kucoin-logo`, `binance-banner`, `ethereum-2`), platform
screenshots (`bitfinex-ui`, `gemini-exchange-trading`), the labelled
`proof-of-stake.jpg` infographic, and the two off-message files
(`ftx-collapse`, `one-coin`). **The strategy doc's "site images lead,
stock supports" has quietly stopped being achievable here**, and pretending
otherwise is what produced nine uses of one photograph. Budget for a real
stock fetch on every video, and say so rather than reaching for the cache.

**Fetching fresh is also how the palette finally got fixed.** Searching for
the channel's own colour — `abstract gold particles`, `geometric network grid
gold`, `dominoes falling dark` — returned gold-on-black footage that matches
the brand, where the recycled pool was blue server rooms dimmed toward it.
Search the palette, not just the subject.

## Two more ways the luma box lies

Both found fetching for proof-of-stake, both would have shipped on the numbers:

- **A nearly empty frame passes by being empty, not by being dark.**
  `hands-locking-padlock-dark/10241357` measured L0-1 and is a tiny padlock
  drifting in a vast black frame. Nothing is wrong with its brightness; there
  is simply almost no picture in it, and in 9:16 the subject leaves the crop
  entirely. **Check that a clip has a subject at all, not just that its mean
  is low.**
- **A folder name is a search query, and it stays wrong at any brightness.**
  `safe-deposit-box-vault-dark-interior/6406107` is a **van interior**.
  `gold-bars-dark-background/3752109` is **bottle caps**.
  `molecular-structure-rotating-dark-abstract/35967934` is a **DNA double
  helix** and reads as biology under a crypto script. This file already says
  it; it keeps being true, and the fix is always the contact sheet.

## An abstract is a backdrop. It cannot carry a shot.

**The correction to the "fetch fresh, search the palette" rule above, and it is
the more important half.** Told to stop recycling assets and to search the
channel's own colour, the next cut came back almost entirely gold-on-black
*abstraction* — gold dust, drifting smoke, particle spheres, geometric solids,
light trails — and the user's note was that these "feel more like a background
than main footage" and lose attention across a long video. That is exactly
right, and it is the same failure as wall-to-wall stock, wearing a better
palette.

**On-palette is a constraint, not a subject.** An abstract passes every check
this doc has — it is dark, it is on-brand, it is unused elsewhere, it has no
off-message reading — and still says nothing, because there is nothing in it to
look at. The screening pipeline cannot catch this: brightness, saturation,
duration and reuse are all fine.

So: **budget abstraction like seasoning.** One or two slots in a three-minute
video — the outro, where an uncluttered frame is wanted, and perhaps one change
of register. Everything else wants a subject a viewer can name: a person at a
screen, hardware, an object, a place. On the re-cut those were
`man-working-computer-dark-office-night`, `programmer-coding-screen-dark-night`
(hands on a keyboard, code on the monitor), `graphics-card-gpu-dark-background`
and a mining farm — all still inside the luma box, none of them wallpaper.

**Write the shot list's subjects out as a list before building** and count how
many name a thing. If more than a couple read as "texture", the video is
wallpaper with a voice over it.

## Say the noun the narration says

Three faults on the same cut, all the same shape — the picture showed a
neighbour of the word instead of the word:

- **"Money." over Ethereum coins.** The line is deliberately generic — proof of
  stake spends *money* — and the screen showed the one specific cryptocurrency
  the sentence has not got to yet. Banknotes are the picture of that word.
  Fiat is hard to screen (paper is pale; the darkest usable candidate measured
  L67 against a L48 stock ceiling) but a slightly bright *correct* picture
  beats a perfectly graded wrong one.
- **"Proof of work spends electricity" over gold dust.** The thing that spends
  it is a graphics card, and the channel had never once shown one.
- **"The miners did not need saving" over drifting smoke.** The miners were
  available as a photograph the whole time.

The rule this doc already had — *say the whole name of a thing* — was about
the script. This is its other half: **the picture has to name the same noun the
voice does.** Read the shot list against the sentence list once, out loud, and
check every pair.

## Show the thing the line is about

**A concert line gets a concert.** The AirPods cut ran an empty night street
under "a concert is loud, and then you go home" and the user's note was to use
something relevant. Stock searched for atmosphere ("city traffic night") comes
back as atmosphere, and atmosphere under a specific noun is a shot that
illustrates nothing — the same failure as the sleep cut's unlabelled water,
arriving through a different door.

Concert footage screens well for these palettes, which is not obvious: a gig is
mostly dark with coloured stage light, so `concert-crowd-night-stage-lights`
measured L20-32 and a crowd with raised hands L27-32. **Check the hue, not just
the box** — two clips in the same batch were green-lit and green is the one
colour that cuts hardest against both brands.

## Open on a face, moving

The first cut opened on a still of a worried woman and the note back was that it
is not an engaging way in. A **clip** of someone visibly dealing with it reads
instantly, needs no caption, and costs nothing — `headache-stress-tired-woman-dark`
screened at L46/S22. For a health topic the opening frame should be a person, not
a concept.

## A site image's filename is a promise its photograph does not keep

**`young-tinnitus.jpg` is a bright classroom with a child in a VR headset.**
It went into the myths cut's closing `checklist` as the picture column on the
strength of its name — the beat busts "only elderly people get it", so a file
called *young-tinnitus* is the obvious pick. The actual photograph says
nothing about age, ears or hearing, and at L172 it was the brightest thing in
the frame.

Same class of error as trusting a stock folder name, and this library is full
of it: `silence.jpg` is a teal studio "shh" shot, `tinnitus-myths-reality.jpg`
is a desk with a laptop and a textbook. **Open the file before writing it into
a beat.** The replacement here — `kid-and-dad-with-headphones.jpg`, L71, a
child and a parent both wearing headphones — is the picture the line was
actually about, and it is a hundred luma darker.

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

## An infographic is banned from a Ken Burns shot, not from the video

**The ban above is about the move, not the picture, and the proof-of-stake cut
is where that distinction finally mattered.** `posts/proof-of-stake.jpg` is the
site's own architecture diagram — new transaction, mempool, validators stake,
random selection, propose, attest, reward — and the user asked for it to carry
the section that describes exactly that. The existing rule reads as a flat "no
infographics", which would have refused a picture that is better than anything
stock could supply.

What the rule actually protects against is a **zoom and pan cropping the
diagram's own title off the top and its last row off the bottom**. Remove the
move and the objection goes with it:

```python
Shot(image=DIAGRAM, zoom=1.0, pan=(0.0, 0.0), aspect=1.5, bias=0.5)
```

`aspect` set to the source's own ratio means no crop; `zoom=1.0` with no pan
means no travel; and a 1000x667 file cannot cover 1920x1080 under
`max_upscale`, so it renders **fitted** — the whole diagram on black, hairline
and all, like a slide. Fitted is a fault for a photograph and the correct
treatment for a diagram, which is the part this doc had conflated.

**In 9:16 use `ImageOverlay` instead** and keep the footage moving underneath —
see the short's skill.

## Run `tools/audit_assets.py` before every render

**Two builds died on clip arithmetic, and both were answerable without
synthesising a word.** `server-racks-blue-light-dark` (9.2s, called six times
with `clip_at` up to 12.0) and then `dominoes-falling-dark` (10.0s at
`clip_at=7.5` for a 3.8s shot). `VideoShot` correctly refuses rather than
freezing or looping — but it refuses **twelve minutes into the render**, after
the whole narration has been synthesised.

```bash
.venv/bin/python tools/audit_assets.py proof-of-stake   # one video
.venv/bin/python tools/audit_assets.py                  # whole channel
```

It checks three things statically: **<=2 uses per clip**, **>=8s of headroom
after `clip_at`**, and **repeats at least five slots apart** — plus, with no
argument, prints every asset shared by more than one video. It caught four real
faults in this pair the first time it was run, including two that would each
have cost a render.

**A 10-second clip is a one-use clip in this format**, which is the arithmetic
that keeps getting missed. Shots run to ~4s, the stretch limit is 1.33x, so a
usable position needs ~8s left after `clip_at`: a 10s source has exactly one
(two would be `0.5` and `2.0`, which look identical anyway). **Filter a stock
fetch for `duration >= 14` before screening anything** if the shot list needs
clips more than once — the first proof-of-stake fetch returned eight clips that
could not fill 21 slots under the reuse rule no matter how they were arranged,
which cost a second fetch and a second contact sheet.

A long/short pair built from the same post is **one** video for the reuse rule
and is expected to share its roster; the tool treats it that way.

## Adjacent Pexels ids are the same shoot

**Adjacent Pexels ids are the same shoot.** Searching for a replacement for
an over-used clip returned three ids within 300 of it, all screening
perfectly on luma, all the same man in the same studio. Treat a candidate
whose id is close to one already in the cut as the same clip until a contact
sheet says otherwise.

## Clip hygiene, stated as numbers

**Clip hygiene, stated as numbers:** no clip more than twice, never twice
inside a minute, nothing held past about eight seconds. **A long hold is
usually a script problem, not a footage problem** — a `Section` sentence with
five caption chunks is one span and therefore one picture, so splitting the
sentence fixes it without touching a word.

## A ping-pong background must not fold at frame zero

**A ping-pong background must not fold at frame zero.** `pingpong` now drops one
frame from each end of the reversed half and `Backdrop.at` samples from a
quarter of the loop in, because a palindrome's turnaround is the one moment
motion stops and every video was opening on one. Only the crypto water was
affected — the aurora is generated on closed circular paths and has no fold —
but re-measure any new footage background the same way: step series over the
whole loop including the wrap, minimum must not land at a fold.
