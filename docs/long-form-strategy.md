# Long-form strategy — why these videos exist, and how many

Written 2026-08-11 as the plan for long-form explainers on thecrypto.wiki and
tinnitushelp.me. **What survives here is the reasoning: what the SEO claim is
actually worth, and why the output is capped.**

Everything about *how* to build one has moved to `docs/video/` and is maintained
there - `longform.md` for the format, `footage.md` for the picture, and
`docs/video/README.md` for the map. The build plan, the phase logs and the
format spec that used to live here were completed or superseded, and the pace
figure they carried (2.9 words/sec) was measured wrong; `longform.md` gives the
real one. Which post to make next is `tools/topics.py`, not the ranking this
doc used to hold.

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

## Why the output is capped

**15–20 videos on demand-ranked pages, not one per post. Decided.**

YouTube's inauthentic-content policy targets mass-produced templated AI-voiced
slideshows precisely. Both short formats already carry *volume is the failure
mode*. Long-form makes that worse, not better: 35 seconds can coast on a good
first line, three minutes cannot. A channel that trips this is suppressed
wholesale, not partially.

That cap is the reason `tools/topics.py` suggests and never bulk-generates, and
the reason script generation from MDX is not planned.

## Do not

- Mass-produce. 130 templated explainers is the pattern YouTube suppresses, and
  the reason this plan caps at 15–20.
- Present a video embed as a page-ranking gain, or promise a search thumbnail.
- Ship a raw YouTube iframe. Facade with a local poster, or do not embed.
- Quote `views.json` as evidence about video. It is SEO demand.
- Repost a music-bedded long cut to TikTok or Instagram — the Audio Library
  licence does not cover it.
- Generate scripts automatically across the back catalogue.

The YMYL limits and the voice-approval rule are per project and live in
`docs/video/projects/crypto.md` and `docs/video/projects/tinnitus.md`.
