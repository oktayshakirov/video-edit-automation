# Project: thecrypto.wiki

Source site `~/Coding/crypto-wiki`. Long form and a Short are built as a pair
from one article.

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
driven by a `videos.json` registry - see `docs/site-video-integration.md`.
`/videos` and `/videos/<slug>` carry the feed and the per-video transcript
pages, and chapters drive both the transcript and the `Clip` key moments.

That is context for what the build produces, **not** an instruction: writing
the registry entry is `/publish-video`'s job, not the build's. What matters
here is that the chapter list and the `.md` sidecar are build outputs the
publish step will need, so they have to be correct before the hand-off.

**Still unbuilt:** upload. The registry is hand-edited on upload by design.
Script generation from MDX is **not** planned and should not be: the script is
the product.

**Keep the `.srt` and the `.md` sidecar.** Both were cleaned off the Desktop
before the site pages needed them, and the transcripts had to be rebuilt from
`SECTIONS[].sentences` plus the chapter times in the YouTube description.

## What the site gives you

**Images:** `crypto-wiki/public/images/{posts,crypto-ogs,exchanges}`. Already
licensed, already on brand, already attached to the post. Start here — but do
**not** finish here, and that is a reversal, see below.

**The one exception is a short about a person.** The site's OG portraits are the
smallest images it has and most are under the ~750px floor — Saylor's are 700x348
and 500x472, so a piece about the man had no usable picture of him. Pull those
from **Wikimedia Commons**, which is licensed, attributable, and where the
photographs are 2000-8000px, i.e. the only images in the format that never
upscale at all. `assets/crypto/<person>/` holds them with a `CREDITS.md`, and the
CC BY-SA ones make the video a derivative work — **the attribution block goes in
the description of anything published**. This is not a licence to reach for
stock: it is a portrait of a named individual or it does not apply.

**Structured data, and it is built:** `video_automation/crypto/facts.py` reads
the frontmatter of all 27 exchange files and 32 OG files and hands
`quickFacts` straight to the beats. This is the one place the setup scales
without hitting the mass-production failure mode, because the *data* is the
script — numbers the site already publishes, fact-checks and keeps updated —
rather than a model's guess at one.

```python
from video_automation.crypto import facts as F

picked = [F.load("exchanges", s) for s in ("coinbase", "binance", "kraken", "uniswap")]
rows = F.compare(picked, "custody", F.contains("non-custodial"))
# -> [("Coinbase", False), ("Binance", False), ("Kraken", False), ("Uniswap", True)]
Shot(graphic="checklist", payload=(rows, "Who holds your keys?"))

F.facts_grid(F.load("exchanges", "kraken"))   # -> [(label, value), ...] for `grid`
```

- **Run `F.coverage(F.load_all("exchanges"))` before choosing what to compare
  on.** Four keys are on all 27 — `founded`, `type`, `custody`, `availability`
  — and only those support a comparison across the whole set. `headquarters`
  covers 24, `token` 19, `founder` 15. The gaps are not random: `token` is
  missing exactly from the exchanges that have no token, so a beat built on it
  silently drops the interesting cases.
- **`custody` is the first comparison worth making.** 21 of 27 are flatly
  "Custodial", 3 are non-custodial, 3 are custodial with a self-custody wallet
  alongside. That is a real answer to a real question, it is a judged list
  rather than a table, and the judgement is the site's rather than this repo's.
- **Pick the handful the script argues about, never the whole set.** `compare`
  raises past six rows, because a checklist reveals one item per caption and
  every row has to be spoken. 27 rows is not a graphic, it is a table. Pass
  `strict=False` to survey while choosing an angle.
- **It also raises on a row too wide for the line.** An over-long item draws
  straight off the right edge — nothing clips it and nothing raised before, the
  same bug class as marks scheduled past the last frame. `with_value=True` is
  usually what triggers it; the values are prose.
- **This is a payload generator, not a script generator.** The angle, the
  verdict and the wording stay hand-written. The script is the product.
- `Entry.image` resolves the frontmatter path into `public/images` and returns
  None when the asset is missing, rather than handing a shot list a path that
  fails at render time. The ~750px floor and the no-infographics rule apply to
  anything it returns exactly as they do to a hand-picked file.
- PyYAML is a dependency now. A hand parser was the first plan and is wrong
  here — the site's own values carry quoted colons ("Nasdaq: COIN") and
  semicolon-separated clauses, which is where naive splitting breaks. `head()`
  takes the clause before the semicolon, which is what fits on a card; the
  qualifier after it is the honest part and belongs in the narration.

**Palette** is `config/theme.json`: gold `#e5c200` on `#171717` / `#2f2f2f`.

**Demand data** is `json/views.json` — site pageviews, so it measures SEO demand,
**not** short-form appeal. Do not present it as evidence about video. Top pages:
`how-to-build-a-mining-rig` 1510, `understanding-crypto-exchanges` 1038,
`exchanges/cryptocom` 380, `crypto-ogs/satoshi-nakamoto` 372,
`crypto-etfs-explained` 362, `what-is-proof-of-stake` 317, `exchanges/okx` 304.

## Voice

**`mia` is the default** for both formats — every shipped crypto long+short
pair uses it. `max` is the roster's alternate for this project, carried over
from drone and not yet tuned for an explainer script; see `voice.md` and
`docs/video/projects/tinnitus.md` for the shared roster and the reasoning.
Both remain `candidate`, not `approved`, until the user says otherwise.

```bash
.venv/bin/python -m video_automation voices list
.venv/bin/python -m video_automation voices show mia
```

The roster was trimmed from a larger shortlist (`sam`, `theo`, `mia-calm`) on
2026-08-28, once `mia` had settled in as the working default across every
project script.

**Pace: use `words / 3.25 + sum(gaps)`, not 2.9.** Measured on shipped cuts:
`bitcoin-price-short` is 141 words plus 12.24s of gaps, and 3.25 predicts
55.6s against a **54.2s** render — inside a second and a half. The old 2.9
figure predicts 61s, which is enough error to push a Short past the window
without noticing. `longform.md` carries the same correction for long form.

## Copy

**Captions go under the photograph, not over it.** Every source image is
landscape, so even cropped it leaves a band of blurred backdrop below, and that
band is where the type belongs — over the photo it covers the thing it is
describing, and it wasted the empty space.

**One caption line for the whole piece, not one per shot.** `caption_line()`
takes the lowest line any shot needs — `photo_box(0.5)` plus 96px, clamped to
0.80 — and every caption in the video sits there. Measuring per shot was shipped
once and was wrong: captions are held until the next one starts and shots
dissolve over `XFADE`, so the outgoing sentence's last caption is still on
screen while the incoming photograph is already visible, and the type jumped
mid-dissolve — on the shots whose photos sit lowest, jumping *into* the incoming
picture. Solving the worst case solves all of them. The tightest shots get a
little more air under the photo than they need, which nobody notices; the jump,
everybody did. `y_frac=0.70` is only the floor.

**Watch the shot that sets the line.** It is whichever photo runs lowest, and if
its bottom lands within ~10px of 1536 the type has no air. Widen that shot's
`aspect` rather than lowering the clamp — 0.80 comes from the safe box.

**Captions are composited in Python, in `render_shots`, not burned by ffmpeg.**
They used to be full-frame PNG overlays gated with `enable='between(t,..)'`,
which is a hard on and a hard off — against a voice with a real sentence contour
that snap is the one part of the piece that still reads as generated. Every
frame is already drawn in Python, so `CaptionSprite` costs nothing and buys a
per-frame entrance: fade up over 0.13s while rising 12px and settling from 94%
**with a slight overshoot**. The overshoot is the trick — a linear scale-in
reads as a zoom, one that passes its mark and comes back reads as being
*placed*. Captions also cross-dissolve into each other, which is what stops a
four-caption sentence looking like four separate cards. It also deletes a
thirty-stream ffmpeg filter chain; the final pass is now just a mux.

Futura Medium 46px, stroke 4, `max_w=CAPTION_MAX_W`.

**Emoji** via `core.vertical.add_caption_emoji` — shared with the tinnitus format.
One or two per script, where they add something: a padlock on "those coins have
never moved", a down-arrow on the closing question. More than that reads as
decoration.

`gap=0.34`, tighter than the drone quotes' 0.65. A quote wants air between lines;
a thirty-second explainer does not, and the pauses are what a viewer scrolls away
during.

**End on a question — unless the video is a how-to, and then end on the rule and
a save.** The question exists to earn a comment, which is the cheapest signal a
35-second explainer can ask for. But it has to be a question the viewer can
actually answer from what they just watched: the mining rig short closed on
"would you have caught that before switching it on?" and the user cut it as
confusing, correctly — "that" had three possible referents by then, and it asked
the viewer to audit a build they have not made.

What replaced it: the rule restated as an echo of the opening line (`Cheap
adapter, expensive mistake.`) and then `Save this before you build one.` with a
🔖. **A save is a stronger signal than a comment on instructional content**, and
unlike "what do you think?" it is something the viewer has a concrete reason to
do. Match the ask to the video: a question for an argument, a save for a
procedure.

**The angle has to be in the first line.** The first cut is
`crypto-satoshi-proof` — "every few years someone claims they're satoshi, and
there is one test that settles it" — built from
`posts/what-it-actually-takes-to-prove-someone-is-satoshi-nakamoto.mdx`. It works
because the answer is concrete, surprising, and needs no financial advice.

**Check phonemes with espeak rather than guessing** — Kokoro phonemizes through
espeak-ng, so `espeak-ng -v en-us -q --ipa "Binance"` is the whole check. It
returns `baɪnˈæns` (bye-NANCE), which is wrong for the brand and shipped once;
`Bynanse` returns `bˈaɪnæns`, which is right. Respell in the **spoken** half of
a `(caption, spoken)` pair so the caption still reads correctly.

**Check phonemes before rendering.** Years are fine (`2009` → "two thousand
nine"), names are fine (`satoshi nakamoto`), but `ecdsa` comes out `ˈɛkdsə` —
spell out or avoid any initialism.

## Decisions already taken

**Render headless with ffmpeg, not FCPXML.** Drone long-form writes XML to finish
by hand because there the footage *is* the product. Here it is support and the
script is the product; a human step in the loop means it never runs.

**Do not commit MP4s to the site repo.** Renders go to the Desktop and the site
never carries video bandwidth; a hosted video is referenced, never checked in.
Where a Short is referenced from - if anywhere - is `/publish-video`'s call, not
this doc's.

**Evergreen before news.** News needs a live data dependency the repo does not
have, cannot be embedded as evergreen `VideoObject` content, carries per-video
accuracy risk in a YMYL niche, and is the shape the platforms suppress hardest.
News becomes a variant once the pipeline is proven, not the proving ground.

## An abstract is a backdrop. It cannot carry a shot.

Cross-posted from the long form, where the full write-up lives. Told to fetch
fresh assets and search the channel's palette, a cut came back almost entirely
gold-on-black *abstraction* — dust, smoke, particles, geometry — and it reads
as wallpaper with a voice over it. **On-palette is a constraint, not a
subject**, and no screening check catches this because brightness, saturation,
duration and reuse are all fine.

It bites harder in a short: there are only a dozen slots and the viewer decides
in one second. Budget **one** abstract, the outro, where an uncluttered frame
is wanted for the ask. Every other slot wants a thing a viewer can name.

## Do not

**Either format:**

- Mass-produce. Volume is the failure mode, not the goal - both platforms
  suppress the AI-script-plus-stock-footage pattern by policy, and the cap is in
  `docs/long-form-strategy.md`.
- Give financial advice, or imply one. Route to the article, or to the site's
  exchange pages, which is where the affiliate revenue actually is.
- Promote a candidate voice to approved without being told to.
- Quote `views.json` as evidence about video performance. It is SEO demand.
- Generate scripts from MDX automatically.

**Long form only:**

- Present the landscape safe box or `max_upscale=1.90` as settled. Both are
  `GUESS` in `core/frame.py` until checked on a real upload at full-screen size.

**The Short only:**

- **Build a piece that is mostly stock.** Stock is permitted; a stock slideshow
  is not. If the site's images and the drawn beat are not carrying the argument,
  the reversal has been misread.
- Open on a still.
- Use an image under ~750px wide, or an infographic at any size.
- Ship a Commons-sourced portrait without its `CREDITS.md` block in the
  description. Two of the four Saylor photographs are share-alike.
