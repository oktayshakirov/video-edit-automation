---
name: video-crypto-short
description: Make vertical short-form videos for TikTok, YouTube Shorts and Instagram Reels from thecrypto.wiki articles — voiceover with synced captions over stock b-roll and data graphics. Use when the user runs /video-crypto-short, asks for a crypto short or Reel, wants a post from thecrypto.wiki turned into a video, or wants to pick or tune the crypto voice. For drone footage shorts use video-drone-short instead.
---

# Crypto Wiki — short form

**STATUS: not built.** The voice candidates are saved and reproducible; nothing
else is. Say so plainly rather than improvising a pipeline and presenting the
result as the format.

**Repo:** `~/Coding/video-edit-automation` — run from there with `PYTHONPATH=.`.
Shared with the drone and tinnitus projects. `video_automation/crypto/` is a
stub package.

**Source content:** `~/Coding/crypto-wiki/content/posts/*.mdx` (129 posts).

## What exists

Five shortlisted voices, all reproducing their audition WAVs sample-for-sample:

```bash
.venv/bin/python -m video_automation voices list
.venv/bin/python -m video_automation voices show mia
.venv/bin/python -m video_automation voices render mia
```

| profile | voice | note |
|---|---|---|
| `mia` | female, `af_heart` 1.10 | graded A, the strongest English voice in Kokoro |
| `mia-calm` | female, `af_heart` 1.00 | the same speaker as mia, unhurried — a suffix, not a new name |
| `ivy` | female, `bf_emma` 1.10 | British — an audience choice as much as a voice one |
| `sam` | male, `am_puck` 1.10 | C+ with hours of data, steadiest American male |
| `theo` | male, `am_adam` 1.10 | lowest grade on the list, shortlisted by ear anyway |

Profiles are named after people; the Kokoro voice underneath is an
implementation detail.

**None is approved.** The user shortlisted all five and has not chosen.

All five use the `ENERGETIC` chain — dry and close, ~3% pitch up, compressed to
carry on a phone speaker, 3.5k presence lift, −14 LUFS for the platform target.
**That chain has not been approved either**, only auditioned through.

## What is not built

Script generation from MDX, b-roll sourcing, data graphics, assembly, upload,
and the MDX embed. All of it. The n8n `publish-content` workflow is the natural
place for the script step but is not wired to this.

## Decisions already taken

**Render headless with ffmpeg, not FCPXML.** The drone long-form pipeline writes
XML to finish by hand because there the footage *is* the product. Here it is
filler and the script is the product — with 129 posts, a human step in the loop
means it never runs.

**Do not commit MP4s to the site repo.** Publish to YouTube Shorts and embed a
lazy-loaded facade, so the site carries no video bandwidth and gains a
`VideoObject` schema — which is the SEO win that lands whether or not the
short-form channels work.

**The visual layer does not transfer from drone.** `pick_crop` still applies to
stock clips, but `drone.analysis`, the move-type table and the zoom heuristics
are about drone moves and mean nothing here.

## Do not

- Present this as working. Nothing past the voices has been built.
- Promote a candidate voice to approved without being told to.
- Mass-produce. Both platforms suppress the AI-script-plus-stock-footage
  pattern by policy; volume is the failure mode, not the goal.
- Give financial advice in a script, or imply one. Route to the site's exchange
  pages, which is where the affiliate revenue actually is.
