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
the existing JSON, do not call it and clobber the richer one.) Write it back
with `json.dumps(m, indent=2)` plus a newline and nothing else:
`ensure_ascii=False` or another indent re-formats all 25,000 lines, and the
diff hides the twenty entries you added.

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

## A portrait or square photograph must never fill a 16:9 frame

**The sibling of the rule above, and it is about *shape* rather than
resolution.** `PhotoShot` cover-crops to the `aspect` it is given, so a portrait
source in a landscape slot (`aspect=16/9`) keeps the full width and throws away
the height: a 1670x2553 press portrait becomes a **938px band across the face**,
with the top of the head and everything below the chest gone. It upscales
cleanly, nothing raises, and the user's word for it was "zoomed in too close".

So, on any video about a person:

- **Only a landscape source may fill the frame.** Do the check before writing
  the shot, not after: if the source is taller than 16:9, it cannot go in a
  full-frame slot at all.
- **Portrait and square crops go in a beat's `picture=` column**, where `Beat`
  scales the column *down to the picture* instead of cropping it. That is a
  framed inset, it is what the split layout exists for, and it looks
  deliberate — the Ethereum cut puts one beside the pull quote and one beside
  the `stat` whose note names the man.
- **A low-resolution landscape source can be promoted once**, by resizing it to
  the frame and saving that as its own asset. A clean studio shot survives 2x;
  a busy one does not.

## A brand-recoloured logo is a legitimate asset, and often the best one

**Built on the Ethereum cut, where the site library had no usable picture of
the subject at all.** Most of these topics have an official mark on Wikimedia
Commons at 2000px+ under CC BY or CC0. Flattening it against the brand
background and mapping its luminance onto the brand's own gold ramp gives a
full-frame shot that is unmistakable, perfectly on-palette, needs no screening
and can never be off-message.

Two things it buys that stock cannot:

- **The noun, exactly.** A line that says "Ethereum went live" over the Ethereum
  mark needs no label — see the payload rule in `longform.md`.
- **A contrast that carries an argument.** Rendering a second mark in a
  different tone makes a fork visible: Ethereum in gold, Ethereum Classic in
  pewter, the same shape in a lesser metal. That is the whole 2016 split in one
  cut, with no caption.

Keep the licence line in the project's `CREDITS.md` and in `Meta.credits`. Do
**not** do this to a company's logo in a piece that criticises it — a recoloured
mark still reads as that brand.

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

## Label a video clip only when the picture cannot say the noun

**Narrowed 2026-09-06; this section used to read "label your video clips" and
was applied to all of them.** The reasoning was sound as far as it went — stock
was not shot for this script, so a stretch of it under a specific claim says
nothing. But the conclusion was wrong: the cure for a picture that cannot name
the noun is **a different picture**, and only where no such picture exists does
`Shot(clip=..., payload=("", "One line"))` earn its place.

Labelling every clip put a 96px statement on almost every frame of a
four-minute video and the user's verdict was that it was impossible to follow.
The density rule, the three things a payload may still carry, and the
one-per-minute budget live in `longform.md` — see the payload bullet under *The
screen has to say what the voice is saying*.

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

## The cache is pruned to what the cuts use

Screening is what makes the cache grow: a dozen candidates per slot, one cut,
the rest left on disk — and the same Pexels id cached again under every query
slug that returned it (`10241357` sat under four padlock folders). It reached
**26 GB**, 24 GB of it video, which is not a sane thing to carry on a laptop
for footage that is re-fetchable by id.

So the cache now holds **only what a project file on disk actually cuts** -
every `projects/**/*.py`, committed or not:

```bash
.venv/bin/python tools/prune_stock.py            # report
.venv/bin/python tools/prune_stock.py --apply    # delete the rest
```

525 files / 4.2 GB kept, 3375 / 23.5 GB dropped on the first run. Two
consequences for the way you work:

* **Record the verdict here, in the tables below, the same day you screen.**
  That was always the instruction; it is now the *only* copy. A reject whose
  bytes are gone and whose verdict was never written down will be screened
  again from scratch.
* **A missing file is a real error, not a cache miss.** `prune_stock.py`
  exits non-zero and names any path a project cuts that is not on disk. If
  that fires, re-fetch it by id from `manifest.json` — do not quietly swap in
  another clip, because the committed project is the record of what the
  published video was cut from.

Run the prune after a video ships, once the shot list is written into its
project file. Running it *during* a build deletes the pool you are still
screening - the candidates on the contact sheet are not pinned anywhere yet, so
nothing protects them.

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

## Whole query classes come back as the wrong thing — and one class is off-message for crypto

**From the Ruja pair. Three fetches shipped into the first cut and all three
were wrong, none catchable by the luma box:**

| query | what came back |
|---|---|
| `stock market data screen dark`, `code programming screen dark` | live **forex charts with a broker name** (Binance) and a moving price on screen |
| `music festival crowd silhouette dark` | a **bar / lounge** — cocktails, neon, magazine posters, not a crowd |
| `courthouse building`, `red warning flag`, `empty theatre stage` (photos) | all screened **L100+** — a bright subject on a bright ground reads dark on the mean but glares in frame |

Two rules:

- **A no-financial-advice crypto video shows no live price, chart, ticker or
  broker name, ever** — not even blurred behind a beat. Those clips are the
  literal picture of the thing the script is careful never to do. Search
  `server room`, `data center`, `hands typing keyboard`, `dark abstract
  particles` for "a database / a screen" instead; every one of them screened
  L<25 and says "digital" without saying "trade this".
- **"Screen" and "crowd" and "stage" queries are unreliable enough to sheet
  before writing the shot list, not after.** A `data center` query returns an
  orange data-viz animation as often as a server room; a `crowd` query returns
  a bar. Pull a frame from each candidate the moment it downloads.

## A video about one person with almost no free photos

**The crypto-og content type: the subject often has one press photo and a
mugshot, nothing more.** Ruja Ignatova has exactly the OneCoin publicity
portrait (CC BY-SA, on Wikimedia Commons) and the FBI wanted poster (public
domain). Her brother Konstantin, a named figure in the story, has **no free
image at all** — not on Commons, and the DOJ arrest photo is not cleanly PD.

What works:

- **The one portrait, cropped wide and cropped tight, is used as open/close
  bookends** — the same move the shared thumbnail makes. Two crops of one photo
  spaced three minutes apart read as a punch-in, not a repeat. Never adjacent.
- **A named person with no photo gets a labelled stock clip**, not a silhouette
  left to the viewer's imagination: a dark courtroom clip with `payload=("",
  "Konstantin Ignatov - testified against her")` says who and what. The label
  carries the identity the picture cannot.
- **Everything else is dark screened stock and the drawn beats.** Budget for a
  real stock fetch of ~15 distinct dark clips and ~6 dark photos per video —
  the site library cannot carry a bio piece.

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

## When the subject *is* a photographable object, every shot has it in frame

**The counterweight to the rule below, and the noise-canceling cut is where
it was needed.** That file's whole subject is a *device*. Unlike gain,
habituation or a spike, headphones can simply be photographed — and the first
cut still came back with an airplane cabin, a woman in a dark bedroom, an old
man in a chair and a pair of hands on a laptop. Every one of them was dark,
on-palette, unused elsewhere and screened; every one was rejected, by
timestamp, as irrelevant. The luma box cannot catch this any more than it
catches a wrong-subject clip.

So the brief for a device topic is one line: **headphones in every frame.**
People wearing them, the object itself, the product in its case. The roster
that shipped is six clips of people wearing headphones plus five stills, two
of which are wireless earbuds lit on black — one of those in the brand's own
peach, which is the closest this channel has come to a stock asset that looks
commissioned.

Two things that fell out of it and generalise:

- **Ask what the noun of this video is before searching.** If it has a
  photographable referent, "atmosphere that matches the mood" is not a
  supporting layer, it is padding — and the user reads it as padding. If it
  does not (a number, a loop, a phantom sound), the section below applies
  instead and the answer is to *draw* it.
- **One themed shot is a shot; three are a theme nobody asked for.** The
  airplane cabin survived the re-cut precisely once, under the sentence that
  says "the drone of a plane", for one sentence. The first cut had three
  airplane shots and a long one, which is why it read as a video about
  flying.

## Shoot an abstract topic through hands, screens and crowds — not faces

**This is the fix for the casting problem above, and it arrived from the
other direction: as a note about relevance.** The first cut of
`fear-greed-index` was rejected for stock that had nothing to do with the
script — a fireworks festival under "plenty of people check it", a woman
celebrating under string lights under the greed line, a metronome and three
portraits under claims about *a number*. Every one of those clips was dark,
on-palette, unused elsewhere and passed `audit_assets.py`. Screening was
never going to catch it.

**The fault is upstream of screening: some topics have no photographic
referent at all.** The nouns in that script were "a number", "a score", "a
scale" and "a feedback loop". A stock library has no picture of any of them,
so a shot list built from stock will always drift to *mood* — somebody
looking worried, somebody celebrating — because mood is the only thing stock
has for an abstraction. This file's own "say the noun the narration says"
cannot be satisfied by searching harder. It can only be satisfied by
**drawing the noun** — which means the drawn-beat share has to go up, not the
search budget. That cut went to eight graphics in twenty-six shots against
the format's usual four to nine, and the thing that made it possible was
building the one beat that could draw its subject (`dial`, see `beats.md`).

**And the clips that remain should be the act, not the emotion.** What
"checking a sentiment index" actually looks like is a hand on a lit phone, a
thumb on a feed, a carriage full of people each on their own screen. Those
are literal, they are on-palette almost by definition (a screen in the dark
is a dark frame with one bright rectangle), and they need no face.

**But check what is *on* the prop's screen, because that is a noun too.** The
best-composed clip in that roster — a hand holding a lit phone against pure
black — was pulled from the opening shot of both cuts once the frames were
looked at: the phone is running a **photo editor**, sliders and a filmstrip
and all, legible at full size. Under "one number claims to know the crypto
market's mood" the brightest object in the frame was saying *photo app*. This
is the same failure as the branded exchange homepage already documented above,
arriving through a prop rather than through a screenshot: a screen in shot is
read, not merely seen, and it either says the noun or contradicts it. **Prefer
a clip whose screen is an indistinct glow** — a thumb over the edge of a
phone, a feed scrolling too fast to identify — over a better composition whose
screen says something else.

**Which quietly solves the casting problem this file already documented.**
The section above records that screening on `MAX_LUMA` against dark backdrops
selects for darker-skinned actors structurally, and that every attempt to
steer it with search terms failed — the filter does the casting, not the
query. **The user's standing instruction is that the channel should not keep
returning the same casting, and the reliable way to honour it is to stop
casting at all in most slots.** A hand, a screen, a silhouette and a crowd
carry an explainer perfectly well; they are usually the better picture for an
abstract claim anyway. So:

- **Default an abstract topic's clip roster to hands, screens, objects and
  crowds.** Reach for a face only where the sentence is genuinely about a
  person feeling something, and then cast it deliberately.
- **Count the faces before writing the shot list**, the same way this file
  already says to count the clips that are only atmosphere. If most of the
  roster is portraits and the script is about a mechanism, the roster is
  wrong regardless of who is in it.
- **Look at the cast on the finished contact sheet.** That check stands from
  the section above and is not replaced by this one — it is just needed far
  less often once the roster is mostly hands and screens.

### The hands and screens have to be the *subject's* hands and screens (2026-10-02)

**The rule above is right and it has a hole, and `first-bitcoin-transaction`
fell straight through it.** That cut's nouns are a computer, software, code, a
ledger, a register, a machine and a payment — all abstractions by the test in
the section above — so the roster was built as "dark texture that is not a
face": candles, embers, fog, star trails, the moon, a spider web, a
lighthouse, snow. Every clip screened inside the luma box, every clip was
unused elsewhere, every clip was on-palette, `audit_assets.py` passed, and the
user's verdict was that the footage is irrelevant to the topic. It was.

**"Not a face" is not the same instruction as "not the subject".** A
candle is as generic under "one machine keeps the register" as a stock
portrait would be — it is mood footage that happens to have no person in it,
which is the original failure wearing a different coat. What the rule actually
wants is **the act, in the subject's own world**: for a computing topic that
is source code scrolling, a processor, a terminal mid-computation, hands on a
keyboard, a screen reflected in somebody's glasses, a reel of tape. Those are
literal, they need no face, and they are usually darker than a candle anyway.

- **Name the subject's domain before writing a single query**, and search
  inside it. "Dark night texture" is not a domain; computing, medicine,
  hardware, street are.
- **Relevance outranks palette.** This file already says a slightly bright
  *correct* picture beats a perfectly graded wrong one; that was written about
  one slot and it governs the whole roster. The re-cut kept a teal-ish
  programmer's desk and a slightly bright tape deck, and both read better than
  the perfectly-graded candle they replaced.
- **The palette rejects still stand where they are about legibility**, not
  about mood: rainbow RGB keycaps, Matrix rain, a green-lit UI with a legible
  brand, and the hooded Guy Fawkes "hacker" are all out on their own merits.
- **The test, and it takes one pass:** read the shot list beside the sentence
  list and ask of each pair *what is this a picture of?* If the honest answer
  is "night" rather than the sentence's noun, the roster is wrong however well
  it screened.

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
written for a different purpose. **The cache exists so a build is reproducible
and so a rejected clip is not re-screened — not as the shot list's shopping
list.** Note the wording: *re-screened*, not *re-fetched*. The bytes of a
reject are no longer kept (see "The cache is pruned" below); the verdict in
this doc is what saves the work.

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

**And it must name the noun in *its own* sentence, not the one after it.** The
Ethereum short opened on the founder's portrait while the voice asked "who is in
charge of *Ethereum*?", then cut to the Ethereum mark while the voice said
"*Vitalik Buterin* created it". Both pictures were in the video and both were
right — they were one slot apart, and the user caught it immediately. An
off-by-one is harder to spot than a wrong picture, because every shot looks
correct in isolation and only the *pairing* is wrong. Reading the two lists
side by side as pairs catches it; reading the shot list alone never will.

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

**Every still image is used once.** The user's rule, from the Ruja cut where
`regulators.jpg` appeared five times: a photograph the viewer has already seen
reads as the video running out of pictures. Clips may run twice (the audit
allows it, and there are fewer of them); a still runs once. The exceptions,
each deliberate: the one portrait of the subject as an open/close bookend, and
a genuinely textural backdrop behind a drawn beat — but default to no backdrop
(the brand background) rather than repeating a photo. Write the asset list out
before building and count.

## Pexels has no ASIC mining farm (2026-09-16)

Fetched for `miners-ai`: "bitcoin mining farm", "cryptocurrency mining machines
rows", "asic miner fans", "crypto mining warehouse" returned coins on a table,
sticker piles, a whiteboard, a warehouse, a football crowd and a stairwell.
Not one row of ASICs. **Draw the mining site** (`grid`, `compare`) and shoot
the power around it - pylons, substations, night build sites - rather than
fetching again. Two more folder names that lie:
`hand-plugging-server-cable/4820377` is a **laptop** being plugged in, and
`electrical-substation-night/7960548` grades to black under `VideoShot`'s dim.

### A metaphor for the noun is not the noun, again - and do not drown a crypto video in coins (2026-10-06)

`market-cap` repeated the Finney fault: a rusted chain, a padlocked door and
warehouse crates for "locked supply", all cut by the user. It also ran ten coin
clips in one video, and a coin under every line stopped saying anything. Cap
coin footage at a handful of shots, each under a line that is about a coin.
What replaced them: **a concrete analogy the narration actually says** (a
pizza cut into more slices for price vs market cap), money changing hands
where a trade sets the price, and the people and paperwork behind a vesting
schedule. If the script has no analogy, write one; it is cheaper than a
third fetch.

## Real people: Commons photos, and the article's claims are checked first (2026-10-09)

`celebrities-with-tinnitus` was the first tinnitus pair built on named people,
at the user's request for real names and real photos. The route is the Ruja
one (`assets/crypto/ruja-ignatova/CREDITS.md`): Wikimedia Commons, public
domain or CC BY / BY-SA, one `CREDITS.md` per subject folder and the
attribution block in `Meta.credits`. 1960s network publicity stills (NBC's
*Star Trek* portraits) are public domain on Commons and are the strongest
picture this channel has had - instantly recognisable, on the noun.

- **Check every claim about a person before scripting it.** The article
  hedged half its own entries ("reportedly", "if accurate"), and one was
  plainly wrong against the sources (Streisand "around age seven"; Walters
  interview and memoir say nine / sixth grade). Unverifiable entries are cut,
  not softened. The checked list lives in that video's `CREDITS.md`.
- **A portrait still in a 16:9 slot is a picture-column photo**, exactly as
  "A portrait or square photograph must never fill a 16:9 frame" says; crop a
  wide copy (`kirk-spock-1968-wide.jpg`) for the `callout` and the `Flash`.
- **On a video about named people, the default picture is the person.** The
  first cut filled the Shatner and Streisand sections with stock mood (a
  phone, a man in headphones, a woman at a window, a child at a desk) and the
  user cut all of it as irrelevant. Commons had four more landscape photos of
  the two of them; a real photograph beats a clip that is only near the line.
- **A stranger's face under a line about a named person reads as that
  person.** The headphones close-up under "he found sound therapy" was swapped
  for a record spinning in the Short, where the face filled the frame.

Verdicts from the same fetch, so they are not re-screened:

| clip | verdict |
| --- | --- |
| `special-effects-explosion-film-set/17807763` | a fireball on black for ~3s, then smoke, then **black** - give it a short sentence only |
| `special-effects-explosion-film-set/38630739`, `7901284`, `pyrotechnics-explosion-night/*` | fireworks, not an explosion |
| `old-film-projector-dark/3223854` | a frame of film in the gate; reads as a flat brown rectangle at 16:9 |
| `child-classroom-window/*` | every result L118-203, a bright empty classroom; `old-school-desk-dark/11025486` (a child writing, from above) is the dark answer |
| `banjo-playing-close-up/*` | no banjo: an electric guitar, a bass, a mandolin, two people on a balcony |
| `acoustic-guitar-playing-dark/15348445`, `15348446` | the same shoot as the musicians cut's `15348443` |
| `paparazzi-camera-flashes-red-carpet/12987890` | a white flare, no subject |
| `hands-holding-phone-dark-room/6414098` | a legible messaging app |
| `hands-holding-phone-dark-room/6611941` | **cut on review**: the "glow" is a blank white rectangle at full frame, and it says nothing. "Prefer an indistinct glow" (above) is not a licence for a white screen |
| `person-putting-on-headphones-night/7047263` | **cut on review**: reads as a gamer, not as anybody's sound therapy |
| `woman-looking-out-window-night/5976560` | **cut on review**: mood, under a line about a named man |
| `old-school-desk-dark/11025486` | **cut on review**: a child at a desk does not read as Streisand's classroom - a photograph of her did the job |
| `therapist-counseling-session-hands/*` | every result L90-151; `7200765` (hands and a notebook) is the least bright and was used once, for the word "counselling" |

## The halving fetch: verdicts (2026-10-10)

`bitcoin-halving` was the first crypto pair since the cache prune to find
**every** cached clip already cut by another video - the whole roster was
fetched fresh. The sheet's own `USED` flag is not enough to trust: it missed
`7140928` (a server rack in five projects) because the id sits under four
query folders. **`grep -rl <id> projects/` each pick before writing it in.**

| clip | verdict |
| --- | --- |
| `wall-calendar-pages-flipping/*` | none is a calendar: an animated icon, two books, a page edge |
| `marking-date-on-calendar/9057559`, `9057678` | **kept**: a red marker circling a date. L155-169 and the noun; same shoot, so a minute apart |
| `gold-nuggets-in-hand/7667296`, `7684711` | **cannabis**, not gold |
| `gold-panning-river/*` | every pan is bright green plastic |
| `wooden-blocks-stacking/*` | bright nurseries and children - not "a block" |
| `graphics-card-mining-rig/5466792` | a branded RGB card (GALAX, GEFORCE RTX) |
| `gold-bars-stack/38963084`, `39562740` | a live candlestick chart behind the coins (same fault as `38905685`) |
| `knife-cutting-in-half/*` | fruit on a bright board - "half" as a cooking clip reads as a joke |
| `command-line-terminal-screen/35071678` | a Windows "Command Prompt" banner, legible |
| `computer-screen-code-close-up-dark/6346228`, `command-line-terminal-screen/6804121` | green-tinted code, Matrix-adjacent |
| `rain-on-window-night/34977302` | a teal-lit building, green cast |
| `mining-machines-warehouse/*`, `gold-ore-rock/*` | open-cast mines in daylight, L95-150, a blue sky in every frame |
| `gold-mine-tunnel/31752063`, `gold-mine-miner-digging/38994407` | kept for the first cut, **cut on review**: physical mining reads as ore, not bitcoin - see below |
| `power-plant-at-night/7628844` | **kept**: stacks and steam at night, L37-39 |

**Physical mining is not bitcoin mining (2026-10-11).** The first halving cut
put a tunnel excavator and a man digging rock under the "gold mine" analogy
and the 10.5M line, and the user cut both: a viewer reads them as the video
being about mining ore. A mining *analogy* still needs bitcoin-mining
footage under it, so the line became "a pay cut every four years, however
good the miner's machines get" over an open rig. The re-fetch confirmed the
2026-09-16 finding above: `bitcoin mining rig`, `asic miner`, `cryptocurrency
mining farm` and `bitcoin miner machine` returned whiteboards
(`8370038`, `8370150`), sticker piles (`8370044`), an oil pump (`26172739`),
quarries and bucket-wheel excavators (`27676678`, `30911532`-`3`,
`35650007`, `9310130`), branded RGB cards (`5467289`) and an Ethereum coin
over Matrix rain (`10243081`). What survived: `mining-rig-fans/5467579`
(inside an open rig, L65-71) and `bitcoin-miner-machine/8369987` (bitcoin
stacks of falling height, L73).

**A crowd is not "the claim you hear" (2026-10-11).** `crowd-of-people-night-city/36899602`
(a packed street market) ran under "It is the claim you hear most, every
four years" and the user cut it as a random street, unrelated. The line's
noun is a claim being *read*, so it became `man-reading-newspaper-dark/9564066`
(a newspaper turned in a dark bar, L47-55). Rejected in the same fetch:
`10238038` and `6279142` (a legible Instagram feed), `35888104` (a legible
Spanish news article), `7263305` / `6602246` (bright), `6414098` (a messaging
app, already on record).

## The bear-market fetch: verdicts (2026-10-12)

**On a market topic, every market query returns a live chart.** `bull and
bear statue`, `stock exchange building night`, `stock exchange trading
floor`, `bitcoin dark` and `trader at night` came back as candlestick
screens or a stock heatmap in all but a handful of results - 25 of 30
clips, and the rest bright. The no-chart rule above therefore decides the
roster before screening does. What says "the stock market" without a price
on it is the exchange's own facade (`new-york-stock-exchange/4319342`,
bright, one use); what says "crypto" is a coin.

| clip | verdict |
| --- | --- |
| `bull-and-bear-statue/*`, `stock-exchange-*/*`, `bitcoin-dark/*`, `trader-at-night/*`, `new-york-stock-exchange/38267971`, `38711950`, `39083610` | live candlestick charts or a heatmap - every one |
| `bitcoin-coin-rotating/38858929` | a bitcoin in front of a blurred red-green chart (same fault as `38905685`) |
| `new-york-stock-exchange/7580271` | a tablet held up reading "STOCK MARKET" - slideware |
| `wall-street-sign/*` | a dog mural, a one-way sign, graffiti, a voting sign; `39104013` (Trinity / Liberty) is 5s |
| `dominoes-falling-slow-motion/*` | popcorn, a tennis ball, nuts - no dominoes |
| `dominoes-falling-chain/8102758`, `8102761`, `8102764` | white dominoes on a white table, L146-202 |
| `dominoes-falling/9760001` | **kept**: a hand tips a row of dominoes on a dark table, L50-56; `9760002` is the same shoot (setting them up) |
| `dominoes-falling/5921005` | **kept**: red dominoes fall toward the lens with a man blurred behind - from ~11s his face is out of focus |
| `circuit-breaker-electrical-panel/*` | L80-114, cluttered panels; `6520278` is the halving's `6520448` shoot |
| `red-emergency-stop-button/4285873` | **kept**: STOP pressed on a tape deck, L54-65, 7s |
| `calculator-hands-close-up/*`, `signing-contract-pen-close-up/*` | white desks, L91-207 - except `8439245` (a hand signing a form, L78-100, **kept**) |
| `counting-dollar-bills-hands/*`, `money-falling-slow-motion/*` | bright wood or saturated, L78-204 - except `4524511` (hands counting bills on black, L51-58, **kept**); `hundred-dollar-bills-close-up/5651774`, `5651780` are the `5651771` shoot |
| `people-on-subway-using-phones/*` | bright carriages L63-122; `7251007` is L44-50 until ~20s, then L113 |
| `credit-card-in-hand-dark/7534262`, `7534264` | the `7534328` / `7534329` shoot (rwa, whale) |
| `gold-coin-spinning-dark/19428465` | a plain coin, not a bitcoin |
| `laptop-screen-glow-dark-room/4565731` | a green-screen laptop |
| `rain-on-window-night/5930874` | L42 at the start, L105 by mid-clip |
| `climbing-stairs-at-night/*` | bright or magenta-lit - except `15814666` (worn stone steps, L49-54, **kept**) |
| `treadmill-running-dark-gym/15112689` | **kept**: feet running on a treadmill in a dark gym, L34 |
| `photos/brown-bear-dark-background/33037033` | **kept** for the thumbnail: a bear's head out of pure black, 9504px, L22 |
| `bitcoin-coin-rotating/7450203` | **cut after the first render**: a silver bitcoin in macro on a white sweep. L76-87 on the mean, but the 9:16 crop is all coin face and white ground and it glared off the frame |
| `bitcoin-coin-rotating/7634144` | **kept**: a bitcoin spinning down flat. Before ~3s it is a grey blur crossing the 9:16 crop; from 4s it is a gold coin in focus, low in the frame |
| `gold-bitcoin-black-background/8370146` | **kept**: one gold bitcoin standing on a dark table, centred, L23-38 - the 9:16 crop keeps all of it |
| `gold-bitcoin-black-background/8369965` | **kept**: a heap of coins on dark blue, a bitcoin under a magnifying glass, L63-68 |
| `gold-bitcoin-black-background/8369977`, `bitcoin-coin-on-dark-table/*` | the same bitcoin-on-wood shoot as the halving's `8369987`, bright wood, L75-133 |

## The stress-meter fetch: verdicts (2026-10-12)

`your-tinnitus-as-stressometer` found the tinnitus cache in the same state the
halving pair found crypto's: **every cached clip is cut by another video**, so
the whole roster was fetched fresh (122 clips over three rounds). The subject
cannot be photographed, so the queries were for the act around it - a hand at
a keyboard, a pen in a journal, a meter's needle, a walk - and the meter itself
is the drawn `dial`.

| clip | verdict |
| --- | --- |
| `megaphone-dark/*` | every result bright: a teal studio with flowers, a man in a mask, a woman cheering. The article's megaphone line was rewritten rather than refetched |
| `clenched-fist-hand-tension/*`, `hand-clenching-fist-dark-background/*` | grey studio hand signs (OK, peace, a black glove) - no tension in any of them |
| `fingers-tapping-desk-nervous/*`, `office-meeting-tense-dark/*` | bright desks; an interrogation scene with a tattooed man; a green murk |
| `smoke-alarm-ceiling/*`, `smoke-detector-beeping/*` | an emergency-exit sign, a woman stretching in bed, incense, UV-lit banknotes. No smoke alarm. `burnt-toast-toaster-smoke/4571351` (toast pops smoking at ~7.5s) carries the metaphor instead |
| `vu-meter-needle-analog-audio/14232785` | **kept**: two amber VU meters on a rack, L25 - but **4.1s**, one slot only. `3958754` is a saturated orange close-up (S171), `2442236` a white meter (L178), `30921165` green LED bars |
| `pressure-gauge-needle/5637839` | **kept**: a gauge in a hand, needle swinging. `barometer-needle/*` is a pine tree, a record player and a Cyrillic-lettered scale |
| `person-writing-journal-night-lamp/39425735`, `39425736` | **kept**: a hand writing by a warm lamp. Same shoot as the magnesium pair's `39425737`, which is a close face - nothing in these frames repeats it |
| `hands-typing-laptop-keyboard-night-dark/15872811` | **kept**, 7.1s: a hand at a purple-lit keyboard. **In 9:16 only `clip_ax=0.20` works** - 0.30 is keyboard bokeh, 0.0 the back of a hand. `6346224` is green-lit; `34771070` is the shoot of `34771078`, in six projects |
| `hand-holding-phone-dark-night/15763477` | hands holding a phone **in rubble**, war-like footage on the screen |
| `hands-on-belly-deep-breathing/9465177` | a sheened midriff - reads as a stomach ache or a fitness ad. `8795165` (a man breathing, hand on chest) **kept** |
| `person-sleeping-peacefully-bed-dark/6941199` | **kept** for the opposite of its query: at 4-7s she is awake beside a clock reading 1:28 |
| `deer-alert-ears-forest/*` | a deer with its ears up is the literal picture of "on alert", but green and bright, and it needs an analogy the article does not make |
| `hand-writing-in-notebook-pen-dark/11025442` | **kept** for "give it a number": figures going into an exercise book. Reads a little like homework |
| `red-warning-light-flashing-dark/3882891` | **kept**: a level crossing's red lights. `3350820` is police blue-and-red; `3134591` a legible EXIT sign |
| `candle-flame-dark-close/7033615` | **kept**: one flame on black, the quiet ground for the red-flag label |

## The decentralized-AI fetch: verdicts (2026-10-16)

The noun is computation, so every query went inside computing. **Most of
the obvious server footage is already cut** - `7140928`, `7140931`,
`1085656` (also S121, a blue cable wall), `5028622`, `7140937`, `8212370`,
`34771078`, `6755170`, `6754818`, `6754824` all sit in other projects, and
`34279733` is the shoot of the halving's `34279721`.

| clip | verdict |
| --- | --- |
| `graphics-card-close-up-dark/5466792`, `5467289` | GALAX / GEFORCE RTX branding, RGB (on record) |
| `graphics-card-close-up-dark/3147349` | **kept**: a GPU fan in a lit case, L48 but S60 purple - the noun, so relevance won |
| `graphics-card-installing-computer/34821018` | a white RGB showcase build, L104-122 |
| `hands-typing-keyboard-dark/5495784`, `5495845` | **kept**: hands at a laptop in the dark (L17) and from above (L48) - one shoot, kept apart |
| `rows-of-computers-office-night/36036749` | **kept**: a backlit keyboard, L7-11 |
| `rows-of-computers-office-night/6258096` | a legible shopping site |
| `circuit-board-close-up-dark/6755158` | **kept**: one processor die on dark stone, L19-36 |
| `circuit-board-close-up-dark/6754820` | **kept**: a gold-orange board, L71 |
| `computer-chip-macro/7609195`, `6208729`, `6754822` | bright teal / green boards, L78-88, an Arduino logo |
| `cpu-processor-installing/11537353` | **kept**: fingers seating a CPU, L89-94 |
| `cpu-processor-installing/12611453` | an AMD-branded chip in a hand |
| `motherboard-assembling/9373207` | **kept**: hands on a motherboard, teal-lit, L100-109 |
| `supercomputer/32386520` | **kept**: a corridor between racks, L44-54 - the only fresh rack shot |
| `supercomputer/34719182` | a saturated blue voxel animation, S72-82 |
| `data-center-aisle/*` | every result a warehouse or a supermarket |
| `data-center-corridor-servers/38496190`, `server-rack-lights-dark/38496193`, `gpu-server-installing/38496192` | **kept** (two of them): a hand at drive enclosures, L61-101 - "storage" |
| `neural-network-visualization/37101560` | **kept**: a gold fibre network, L30-73 - "the model" |
| `neural-network-visualization/34992913`, `34994032` | **kept**: red/white ball-and-stick nodes, L21 - one look, so far apart |
| `neural-network-visualization/37104472`, `34996641` | magenta / saturated blue |
| `stopwatch-close-up/9944842` | **kept**: a red LED digit counting down to 0, L29 - a challenge window |
| `stopwatch-close-up/*` others, `hourglass-sand-dark/*` | a chess clock on white, a collage animation, teal-pink hourglasses L71-141 |
| `stack-of-coins-dark/5253412` | **kept**: coins across a dark table, L25-41 |
| `coin-slot-dropping-coin/5305003` | **kept**: coins dropping and scattering on stone, L90 |
| `bank-vault-door/39060937` | **kept**: a key turned in a steel locker, L42-47 after 2s |
| `bank-vault-door/5849613`, `5849641` | cartoon "DEPOSIT" / "SAVINGS" animations |
| `padlock-closing-dark/4889026` | **kept**: a shackle close up, L43 |
| `ink-drop-in-water-dark/7565451` | **kept**: teal ink clouding dark water, L20-34 - "poisoned" |
| `ink-drop-in-water-dark/7565969`, `18333375` | the same on white, L128-210 |
| `smartphone-typing-message-night/39494839` | **kept**: a thumb on a phone keyboard, L31-38, no legible message |
| `artificial-intelligence-chatbot-typing/*`, `robot-hand/*` | toy robots and prosthetic hands on white - "AI" as a cliché, not the act |
| `judge-gavel/6101367`, `6101337` | the `6101343` shoot (bitcoin-price, ruja) |
| `magnifying-glass-document/*`, `signing-contract-pen/*`, `stamp-approved-document/*`, `inspector-checking-quality/*`, `calculator-hands-dark/*`, `abacus-close-up/*` | bright desks, stamp albums, toddlers, hi-vis inspectors - L70-210 |
| `graphics-card-fan-spinning-black/33830775` | **kept**: a slow particle vortex, L10 - the one abstract |

## The GTA 6 fetch: verdicts (2026-10-20)

**No game footage, ever.** The trailers are Rockstar's pictures, so the
world is what the game parodies - Miami at night, palms, cars, planes - and
the act of the scam (phones, a laptop at night, cash). Every plane query
comes back bright sky: L115-176 for `aerobatic plane smoke`, `small plane
flying`, `stunt plane`, `plane flying dusk`, `skydiver sunset`. The one
usable stunt clip is grey-sky L65, kept because it is the noun.

| clip | verdict |
| --- | --- |
| `miami-night-neon/19109600`, `6345160`, `19109601` | **kept**: towers at night, the skyline over the bay, an aerial - one shoot for the first and last, kept apart |
| `miami-night-neon/36032432` | a legible DINER sign, 5s |
| `palm-trees-neon-night/40175608`, `29139475`, `4441056` | **kept**: a purple palm avenue (the thumbnail), a palm street from above, palms on a dark beach |
| `palm-trees-neon-night/40305028` | a funfair carousel |
| `ocean-drive-miami-night/15270404` | **kept**: an empty highway at night, L13 |
| `ocean-drive-miami-night/3770584`, `8554258` | L114-138 daylight |
| `sports-car-night-city/13795978`, `13795917` | **kept**: headlights at night, badges too small to read |
| `sports-car-night-city/14228183` | a BMW i8 roundel, front and centre |
| `airshow-night/13066176` | **kept**: three stunt planes trailing smoke, L65 - the trailer's plane |
| `stunt-plane/33698741` | a national display team in tricolour smoke on blue, L115 |
| `airplane-flying-sunset-silhouette/7196522` | **kept**: a tiny plane over a red sunset, L41 |
| `airplane-flying-sunset-silhouette/10675969` | a wing from a window - an airliner, not a stunt plane |
| `airshow-night/34398861` | fireworks, desaturated grey |
| `red-flare-smoke-night/34067500` | **kept**: a pink flare in a street crowd, S62 - the trailer's flare, so relevance won |
| `red-flare-smoke-night/34067369` | the same crowd, more smoke than subject |
| `playing-video-game-controller-dark/16628557` | **kept**: hands on a gamepad, close |
| `playing-video-game-controller-dark/7667876` | a retro console on a desk, no hands |
| `hands-gamepad-close-up/8127818` | **kept**: a gamepad in blue light |
| `hands-gamepad-close-up/7988047` | a red retro pad on green |
| `watching-tv-dark-room/6901290` | **kept**: two people laughing at a screen in the dark |
| `watching-tv-dark-room/6951594` | a woman in a bed, bright warm room |
| `scrolling-phone-dark/13358555` | **kept**: a hand on a phone against black, screen unreadable |
| `phone-screen-hands-night/14513394`, `28828935` | **kept**: a thumb scrolling; a list in two hands, unreadable |
| `phone-screen-hands-night/5617952` | a legible chat keyboard |
| `laptop-screen-dark-room/7272375`, `36392511` | **kept**: hands at a laptop in the dark; a figure at a desk of screens |
| `counting-cash-hands-dark/6266425` | **kept**: dollars counted at a desk, L56 |
| `counting-cash-hands-dark/34579096` | already cut twice elsewhere |
| `gaming-pc-setup-dark/30470983`, `10620285` | **kept**: a red-fan gaming PC; a player at a PC at night |
| `gaming-pc-setup-dark/7914801`, `gaming-headset-dark-room/10620277` | RGB keyboard, 6s; `10620285`'s shoot |
| `ocean-waves-night/40200251` | **kept**: dark purple surf from above - the one abstract |
| `rain-on-window-night/34977302` | teal window, nothing in it |
| `courthouse-night/28388728`, `legal-documents-dark/*` | 4s; bright desks L78-150 |
| `influencer-filming-phone-ring-light/*`, `hand-turning-off-tv/*` | L95-190; S103-139 |
| `nightclub-lights-miami/*`, `neon-sign-city-night/*` | a disco ball; a legible ROOMS sign |

## When the subject is a real thing, its real pictures lead (2026-10-20)

**The user's note on the first GTA 6 cut, and a standing rule for both
channels:** a video whose subject is a real, named thing - a game, a
product, a company, an event, a scam coin - must show that thing, not only
stock that resembles its world. Twenty-four well-screened stock clips of
Miami, planes and phones read as "boring and monotone", because nothing on
screen was GTA VI. Fair use for commentary covers the subject's own press
material; the description credits it (`Meta.credits`).

**Where to get them, in this order:**

1. **The owner's own press or official site.** `rockstargames.com/VI` serves
   4K key art, in-game screenshots and the logo as an RGBA PNG under
   `/VI/_next/static/media/` - `curl` the page and grep the paths. Official
   art is the most trustworthy source and the only one with no third-party
   watermark.
2. **A press outlet's lead image, for a moment the owner did not publish as
   a still** - the trailer's DacityCoin plane came from a news article's
   `og:image`. Look at it before using it: half of crypto-news lead images
   are AI composites carrying the outlet's own logo (`coingabbar`), which
   is neither real nor theirs to lend.
3. **Never a logo you cannot tie to the thing.** A scam token exists under a
   dozen copycat contracts, so a DEX logo may be the wrong coin, and showing
   it points viewers at a live scam. Draw a `ticker_card` from the verified
   name and date instead.

**How they go in:**

- **`Shot(image=)` for a still that is the line's noun** - full-bleed in 16:9
  when the source clears `1920 / 1.90`, a framed card in 9:16. Official 4K
  art always clears it.
- **`Shot(inset=(path, where, scale))` to put the real thing over stock** -
  the logo in the corner (`"tr"`, 0.12 in 16:9, 0.22 in 9:16), a game still
  beside a leaker's laptop, a ticker card on the phone shot. See
  `overlay.InsetOverlay`.
- **Budget it:** on the GTA pair, about a third of the clip slots became real
  stills and another quarter carry an inset. Stock still carries the act
  (hands, phones, cash); the real pictures carry the nouns.
- **The thumbnail is the subject's own key art** when there is one; the
  user picked it over the drawn and stock options.

Assets live in `assets/stock/press/<topic>/` with a committed `SOURCES.md`;
the bytes are gitignored like the rest of the stock cache.

## The meme coins fetch: verdicts (2026-10-22)

**Every Shiba Inu clip is bright** (L90-157): Pexels shoots dogs in daylight
and white rooms. Relevance won for the Doge noun - three kept, never two in
a row. **Commons had the real things**: a physical Dogecoin on black (CC
BY-SA), Kabosu herself with her owner (CC0), and a 2023 Musk photo unused by
the musk-effect pair. `Kabosu.jpg` on Commons is the citrus fruit - look at
every file a name search returns. Credits in `assets/crypto/memecoins/`.

| clip | verdict |
| --- | --- |
| `shiba-inu-dog/20378106`, `20660963`, `16436887` | **kept**: a grinning close-up (the opening face), one lying down, one on a lead |
| `shiba-inu-dog-close-up/5728459`, `-evening/5921464` | warm-orange interior S90; autumn forest S66 |
| `scrolling-social-media-phone-night/6279142`, `17586685` | **kept**: a feed in two hands by a lamp; a hand on a phone, screen away |
| `scrolling-social-media-phone-night/10238038` | a legible chat, L81-98 |
| `laughing-at-phone-dark/5281602` | **kept**: a face lit by a screen |
| `laughing-at-phone-dark/7986753` | L7, nothing readable |
| `crowd-holding-phones/8088612`, `38471324` | **kept**: a crowd each on a phone; a night square of raised phones |
| `typing-code-laptop-night/13522186`, `5495781` | **kept**: code on a laptop; hands typing |
| `programmer-monitor-code-dark/34160292` | **kept**: a monitor of code, red light |
| `crypto-app-phone-hands/35124446` | **kept**: a candle chart on a phone, no name or ticker |
| `crypto-app-phone-hands/35886692` | **cut after the first render**: the screen says "Apple Inc / AAPL" with prices, legible in 9:16 - a named stock under a meme coin line. The contact-sheet thumbnail hid it |
| `television-studio-audience/14367163` | **kept**: a TV studio floor in silhouette - SNL |
| `padlock-chain-dark/4889026`, `hands-empty-wallet/16747050` | **kept**: an old padlock; an empty wallet opened |
| `stack-of-cash-dark/6266652` | **kept**: a briefcase of cash in red light |
| `person-checking-phone-worried-night/7280528`, `8376635` | **kept**: head in hand over a phone; a glow under a blanket |
| `dark-ocean-waves-night/5678004` | **kept**: dark water - the one abstract |
| `money-banknotes-dark-table/345790xx` | the shoot of `34579096`, already cut twice |
| `magnifying-glass-document-dark/6979937` | the shoot of `6979933`, already used |
| `hourglass-sand-dark/*`, `hand-taking-money-from-table/*`, `people-laughing-at-phone-together/*` | L110-170 daylight |
