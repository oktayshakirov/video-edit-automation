---
name: video-glitch
description: Build datamosh glitch transitions - the TikTok "reality glitching" cut where the first shot is smeared into the second shot's shapes by its motion, then the glitch pixels drain away slowly into the clean second shot. Use when the user runs /video-glitch, asks for a datamosh, a glitch or trippy transition, "one video glitching into another", or wants an existing short re-cut with a mosh at one of its cuts. Experimental, builds test renders only; publishing is /publish-video. For plain drone cuts use video-drone.
---

# Glitch transitions (datamosh)

**Experimental.** Renders are tests: silent, uncommitted, unpublished, unless
the user asks otherwise. The engine is `video_automation/core/datamosh.py`;
its docstring is the reference, read it first.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with
`PYTHONPATH=. .venv/bin/python` (system `python3` has no `cv2`).

Not the `glitch` mode in `core/transitions.py`, which is a drawn RGB-split
cut for the article videos. This one breaks the codec.

## How it works

Compressed video only stores a full picture at keyframes; the frames between
are motion vectors applied to the frame before. Drop shot B's keyframe and the
decoder keeps applying B's motion to A's last picture, so A is pushed into
B's shapes. Repeating one P-frame (a *bloom*) re-applies its motion and the
smear grows. Then `heal()` lets the glitch go: B takes over block by block
while the mosh keeps moving underneath, slowing to a stop.

## The signed-off cut

`datamosh.cut()` is the whole thing, and its defaults are the version the user
approved (forest into the rotating Golden Girl top-down):

| frames | what plays |
|---|---|
| `build` 30 | A broken up by B's motion at 4x, bloom of 10 |
| `heal_frames` 75 | B takes over; glitch blocks drain on a long tail while the motion slows 4x to 1x (`motion_ramp()`) |
| the rest | clean B at 1x |

```bash
PYTHONPATH=. .venv/bin/python -m video_automation.core.datamosh A.mp4 B.mp4 ~/Desktop/test.mp4 --a-start 2 --a-dur 3 --b-start 4 --b-dur 5
```

**A cut inside an existing short** - write a variant project script that
imports the approved one's segments and swaps only the incoming segment, as
`projects/drone-short/spree-what-my-drone-sees-mosh.py` does. **Never edit the
approved script**: approved cuts are locked (`docs/video/projects/drone-long.md`).

## The exit is where every round went

The user liked the entry from the first good test; four of the six rounds
were the exit. In order:

| exit | user's verdict |
|---|---|
| 4-frame snap to clean | "it just disappears" |
| 0.8s block heal, each block fading over a linear window | the effect was "stopping too quick" |
| mirrored unwind: B scattered by A's motion, played backwards | "getting further away from the effect" |
| soft eased fade, every block partway at once | not shown - looked like a crossfade in the strip |
| **crisp blocks, clearing on a long tail, motion slowing** | the one to keep |

What the kept one does, and why each part is there:

- **Blocks clear crisply, one by one** (`fade=8` frames each). The glitch
  leaves as *pixels*. Any fade where all blocks go partway together washes the
  glitch out like a dissolve.
- **The clearing times follow a long tail** (`tail=2`): half the blocks are
  gone in the first quarter, so the viewer is on the second video fast, and
  scattered glitch blocks keep dropping out for the remaining ~2s.
- **The motion slows from 4x to 1x across the heal**, so the leftovers drift
  to a stop instead of thrashing until they vanish.
- **Order is B's darkest structure first** with noise (`noise=0.5`), so B's
  shapes come out of the mosh and the leftovers are scattered, not a wipe.

## Lessons from the entry

- **A takes B's shapes because of parallax in B's motion.** Near objects
  moving against the sky give the motion field edges where the buildings are.
  Worked: Vienna sunset into the skyscraper approach; the Spree hyperlapse into
  the Treptowers orbit; the forest into the Golden Girl rotation.
- **A static B does not mosh.** A locked-off hyperlapse gives near-zero
  vectors and reads as a crossfade. **A synthetic push-in is not the fix**
  (`mosh(push_zoom=)`): motion but no edges, so A only zooms - "unrelated".
  Cut *into* a moving shot (orbit, approach, rotation, yaw).
- **Speed up the motion source, not the shot.** At 1x the Golden Girl
  rotation only froze the forest with streaks; at 4x it swirled it. Clean B
  still plays at 1x.
- **Never feed B its own motion to glitch B.** B pushed by its own vectors just
  moves coherently. The glitch is the mismatch between picture and motion.
- **Contrast sells it.** White forest into gold and lilac, warm sunset into
  blue daylight. Two similar shots barely show it. A dark, low-detail B (the
  Sinemorets sea) eats A in noisy dark blocks rather than shaping it.
- **Labels go on after the mosh**, or they smear with it.
- **HDR:** the mosh is 8-bit. HLG segments keep their code values with no
  colour conversion and are tagged HLG again; see the Spree variant. The CLI
  and `cut()` are SDR.

## Music, when a test wants it

There is no trippy track in the library. The phonk take that fit is
`~/Coding/song-automation/projects/glitch-phonk.md` (seed 2208343586, 130 BPM,
drop at 14.921s); `glitch-trip.md` (seed 1412661844) is the psychedelic
alternative, unused. Put the first glitch on the drop. Stop the song engine
when done.

## Hand over

Send the render, say where the break-up starts, where the heal runs and where
B is clean (the CLI prints them), and look at a frame strip yourself first.
Ask before committing anything.
