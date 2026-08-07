---
name: video-tinnitus-short
description: Make vertical short-form videos for TikTok, YouTube Shorts and Instagram Reels for tinnitushelp.me — article shorts with voiceover and synced captions, plus ASMR sound-therapy shorts. Use when the user runs /video-tinnitus-short, asks for a tinnitus short or Reel, wants a post from tinnitushelp.me turned into a video, wants sound therapy or masking or notched-audio content, or wants to pick or tune the tinnitus voice. For drone footage shorts use video-drone-short instead.
---

# Tinnitus Help — short form

**STATUS: not built.** The voice candidates are saved and reproducible; nothing
else is. Say so plainly rather than improvising a pipeline.

**Repo:** `~/Coding/video-edit-automation` — run from there with `PYTHONPATH=.`.
`video_automation/tinnitus/` is a stub package.

**Source content:** `~/Coding/tinnitus-blog/content` (75 posts).
**There is also an app** — `~/Coding/tinnitus-app`.

## Two formats, and they are not the same job

1. **Article shorts** — structurally identical to crypto's. Not built.
2. **ASMR / sound-therapy shorts** — generated tones, notched audio, masking
   noise. Needs audio synthesis the repo does not have. **This is the format
   with a real reason to exist on these platforms**: tone-matching ("which
   frequency matches yours?") is genuinely useful and natively engaging, rather
   than a talking-head summary competing with a million others.

## What exists

Five shortlisted voices, all reproducing their audition WAVs sample-for-sample:

```bash
.venv/bin/python -m video_automation voices list
.venv/bin/python -m video_automation voices show caspar
.venv/bin/python -m video_automation voices render felix
```

| profile | recipe | note |
|---|---|---|
| `luna` | female, `af_nicole` 1.10, energetic | the only breathy voice Kokoro has, and the base for the four below |
| `elias` | 12% down, time restored | |
| `felix` | 16% down, time restored | |
| `jonas` | 12% down, slowdown kept | no time-stretch artifacts |
| `caspar` | 16% down, slowdown kept, aspiration boost | most processed of the set |

**None is approved.** All five were shortlisted by ear and are waiting on a
decision.

elias, felix, jonas and caspar are all luna pitched down. They exist because **Kokoro has no male breathy voice** — this was
measured, not assumed. All twelve male voices ran 11.7–16.2s where `af_nicole`
ran 23.3s on the same script. Cross-gender style blends were tried and lose the
character: the blends came in *shorter* at a slower speed setting. Pitching
luna down keeps 100% of the breath by construction, which is why that is
the surviving approach. Kokoro has released no fine-tuning code, so blending
and DSP are the whole ceiling.

**Open risk:** a pitch-shifted female voice can read as "a processed woman"
rather than "a man" — formants shift correctly but phrasing and breath stay
feminine. No measurement settles that; only the user's ear does.

## Do not

- Present this as working. Nothing past the voices has been built.
- Promote a candidate voice to approved without being told to.
- Make medical claims. This is a health topic and a YMYL niche — keep claims
  conservative, and never imply a cure.
- Default to driving traffic to the blog. **App install is the far better
  conversion from short-form**, and it is the only path here with a plausible
  route to revenue.
