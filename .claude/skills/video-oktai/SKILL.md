---
name: video-oktai
description: Build an OktAI pair - Oktay's own channel about building with AI and making money with it - a long-form 16:9 and its vertical Short, read aloud by Oktay himself. Suggest topics, research, write both scripts and the read-aloud page for him, then, once he sends the recordings, check them, build both videos with his voice and the camera box, and hand them over. Use when the user runs /video-oktai, asks for an OktAI video, Short or script, or sends recordings for one. Builds only; publishing is /publish-video. For crypto use video-crypto, for tinnitus video-tinnitus.
---

# OktAI videos

**"OK, AI. Let's build."** Oktay's own channel: what we build with AI and
how it makes money, shown from the inside. **A long form and its Short, as a
pair**, like crypto and tinnitus - with one difference that shapes the whole
run: **Oktay reads the scripts himself.** So the run stops in the middle and
waits for him.

**Repo:** `~/Coding/video-edit-automation`, Python from there with
`PYTHONPATH=.`. **Recordings:** `~/Movies/OktAI/<name>/`.

**No long dashes, ever:** a single `-` in every line, title, description
and caption. The picture is enforced in code (`design.md`).

## What this channel is

Read `docs/oktai-channel-plan.md` before the first run of a session - the
name, the formats, the topic slate, the look, and section 7 (links). Then
`docs/video/projects/oktai.md` for how a build differs from the other two.

- **Every claim is something we did, measured or sourced.** The proof is our
  own: the ledgers, the logs, the repos, the books' `SOURCES.md`. A number we
  cannot point at does not go in. The *Proof of Work* beat - one real number,
  on screen, early - is in every video.
- **It is a person talking.** First person, "I" and "we", the way Oktay
  would say it. Warm, direct, a little dry. Never a pitch.
- **Show the real thing.** Screen recordings and real pages first, drawn
  beats second, stock only where nothing real exists, never a stock face.
- **No watermark, no CTA tail** in the video. Links live in the description.

## Read these

| Step | Read |
| --- | --- |
| The run's shared steps | `docs/video/workflow.md` |
| Before writing a line | `docs/video/narration.md`, `docs/video/projects/oktai.md` |
| The long form / the Short | `docs/video/longform.md`, `docs/video/shorts.md` |
| Drawn graphics | `docs/video/beats.md` |
| Real pages and footage | `docs/video/footage.md` (`screencap`, `window=`) |
| Covers | `docs/video/thumbnails.md` |

## The run

### Part 1 - topic, research, script (then stop)

1. **Suggest, do not pick.** Three to five candidates from the plan's slate
   (`docs/oktai-channel-plan.md`, sections 5 and "Behind the scenes") and
   from anything new we built since. For each: the demand evidence (pull
   the search's top results with `yt-dlp --flat-playlist
   "ytsearch12:<query>"` and give their views, or say "no evidence"), the
   *Proof of Work* number we own, and which referral fits (section 7).
   Read `.claude/skills/videos-performance/videos.md` first once OktAI rows
   exist.
2. **Research.** Our own material first: the repo and its docs, git log,
   the video ledger, `~/Coding/audio-book-automation/projects/*/book/`
   (each book's `SOURCES.md` is already cited), the job-search shortlists,
   the app and site repos. Then outside sources for anything general, each
   cited in the project file's docstring with its date. **Anything about
   Oktay's own life, money or numbers that the files do not prove is marked
   `[CHECK]` in the script** and asked about before he reads it.
3. **Write both scripts together** - `projects/oktai-long/<name>.py` and
   `projects/oktai-short/<name>.py`, the same shapes as crypto's
   (`SECTIONS` of `Section`s; `SENTENCES` + `SHOTS`). Plus, in each:
   - `TITLE`, `FACE` - the phrases where the camera box comes in (the hook
     and the last line are automatic): a personal aside, the twist. Never on
     a line where the viewer reads a screen.
   - **Screens are takes, never recordings he makes** (the editor's note,
     2026-11-21: he records the voice only). A shot is
     `oktai.screen(NAME, "file", take)` with a `core/screenplay.py`
     `Browser(url, steps)` or `Terminal(steps)`: the build plays it in
     headless Chromium, records it and cuts it (`footage.md`, "Our own
     screen"). A terminal's output is the real output of a run you did -
     run it, paste it, never invent it. Write the take to the length of
     the lines over it (the render's report gives `seconds_out`).
   - `LINKS` - the tools named on screen that have a referral.
   **Written to be read aloud by a person:** one thought per sentence, a
   breath's length; numbers as he would say them ("five hundred and
   eighty seven" or "587" both match); no tongue-twisters or stacked
   consonants; contractions are fine. Long form 6-10 minutes; the Short
   30-50 s, telling the story in order, ending on a plain sentence. In the
   long form the referral line is said once, when the tool is on screen;
   the Short never pitches.
4. **Write the picture first** (`workflow.md`, "Write the picture
   first"): one line per sentence, what the viewer sees. For this channel:
   the real screen (his recording, `screencap` of a public page), then a
   beat, then stock. A new beat when the library cannot draw the subject is
   part of the run.
5. **Check, then draft.** `tools/script_check.py`, `tools/opening_check.py`
   and `tools/retention_check.py` on both files; fix or explain every flag.
   Then a **draft render** of both (`build_long(..., draft=True)` /
   `build_short(..., draft=True)` from `video_automation.oktai`): a Kokoro
   voice reads it, so the picture and the timing can be checked before
   anyone records. Look at frames; drafts are never shipped.
6. **Hand him the script.** `tools/oktai_script.py <name>` writes
   `~/Movies/OktAI/<name>/script.html` (dark, numbered, CAM marks, a
   teleprompter on P) and `script.txt`. Send `script.html` with
   SendUserFile, list any `[CHECK]` questions, say where to save the files
   (`long.mov`, `short.mov`, or `long.m4a` + `long-cam.mov` for a separate
   mic), and **stop**. Nothing else is his to record. The next part starts when the
   recordings arrive.

### Part 2 - the recordings arrive

7. **Put them in place** - copy what he sends into `~/Movies/OktAI/<name>/`
   under the names above. **Check the voice recordings first**:
   `tools/oktai_recording_check.py <file>`. A clipping peak, a noisy room
   or a missing face is cheaper to re-record now than to hide later; say
   exactly what to change.
8. **Build both** - the project files' `main()` call `build_long` /
   `build_short` without `draft`, which finds the recordings, transcribes
   them locally, keeps the last good take of each line, cuts the rest, and
   adds the camera box (`docs/video/projects/oktai.md`).
9. **Read the reports** - `<file>.<hash>.report.txt` next to each
   recording. A line he said differently: if it is as good, **change the
   script to what he said** and rebuild (the captions follow the script);
   if it is wrong, give him the line numbers to re-read - a re-read of
   only those lines, in a new file, is enough to splice in later.
10. **Look before handing over**: frames at every cut the report flagged,
    every camera-box entry and exit, the first eight seconds, the last line.
    Covers per `thumbnails.md`, his face cut out where it helps (never a
    stock face). The description: links from `LINKS` with each program's
    disclosure (plan, section 7); a missing referral URL is a placeholder
    he is told about, never invented.
11. **Hand over, re-cut, then commit and log** - `workflow.md` steps 4-5,
    `tools/video_log.py` on the pair. Publishing is `/publish-video`; the
    OktAI accounts are not connected yet - say so instead of trying.
12. **Leave the skill better.** Every note becomes a dated rule in the
    narrowest doc (`projects/oktai.md` for this channel), a check in code
    when it can be one, and an edit to this file when the run itself missed
    a step. Tell him what was learned and where it went.
