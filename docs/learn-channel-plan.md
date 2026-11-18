# The learning channel - plan (draft, 2026-11-17)

A third channel, next to Tinnitus Help and Crypto Wiki, but with one big
difference: **it belongs to Oktay, not to a site.** It teaches what we actually
built, measured and got wrong - the audiobooks, the video pipeline, the job
search, the apps - and shows the receipts on screen. **Oktay reads every
script himself from day one**, and appears now and then in a small camera box
in the corner. A Kokoro voice is kept only as a backup.

Status: plan only. Nothing is built, no channel or handle is registered.

---

## 1. Name

### Recommended: **Oktay Builds**

- Handle `@oktaybuilds` on YouTube and TikTok (check both are free before
  anything else - one name on every platform matters more than the name).
- Tagline: **"I build it with AI. Then I show you what worked."**
- Why it wins:
  - **It is attached to the person**, which is the brief - and with Oktay's
    own voice and face box from the first video, the name matches what the
    viewer hears and sees.
  - **It says the format.** Every video is something that was built: a
    pipeline, a book, a search, an app. "Builds" also covers money (apps), jobs
    (a search we built) and crypto safety (a vault we built).
  - **It is not tied to one tool.** No "Claude", "AI" or "faceless" in the
    name - tools change, and a trademark in a channel name is a takedown risk.
  - Short, searchable, says itself out loud.

### Recurring segment name: **Proof of Work**

Every video carries one real number from our own logs, on screen, early -
"587 postings, 4 worth applying to". That beat is called *Proof of Work*
(and the crypto pun is a free bonus). It is the channel's promise in one
device: nothing here is theory.

### Alternatives, if the handle is taken or it does not feel right

| Name | For | Against |
| --- | --- | --- |
| **Oktay Figures It Out** | humble, "learn with me" tone, very personal | long; weaker as a handle |
| **Proof of Work** (as the channel) | strong promise, memorable | generic phrase, crowded in crypto search, not attached to the person |
| **Learned It the Hard Way** | great hook energy for mistake videos | negative frame for 100 videos; not personal |
| **Built, Then Taught** | describes the format exactly | sounds like a course, not a channel |

---

## 2. What the channel is

**One sentence:** a builder using AI for real work, showing what worked, what
did not, and the numbers - so you skip the mistakes.

**Who it is for:** people who want to *use* AI to make something - a channel,
an app, a side income, a job search - and are tired of hype. Mostly 20-40,
technical-curious, not necessarily developers.

**What makes it different from the other two channels**

| | Tinnitus Help / Crypto Wiki | Oktay Builds |
| --- | --- | --- |
| Owner | a site | a person |
| Source | an article | something we built or measured |
| Voice | Kokoro, "here is the fact" | Oktay himself, "here is what happened when I did it" |
| Face | none | a small camera box in the corner, at chosen moments |
| Picture | drawn beats, stock, site pages | screen recordings, real tools, real numbers, drawn graphics |
| Stock | up to half the shots | rare - only where nothing real exists |
| Goal | traffic to the site | trust in Oktay; books, apps, portfolio, work offers |

**The rules (from day one)**

1. **Every claim is something we did, measured or sourced.** Numbers come
   from the ledgers, logs, analytics and the books' `SOURCES.md` - never
   invented, never rounded up. If we did not do it, we do not teach it.
2. **Show, do not tell.** The real tool on screen beats a drawn icon of it;
   a drawn graphic beats stock; stock is the last resort.
3. **A real person, a real voice.** Oktay reads every script. Built with AI,
   presented by a human: on a channel that teaches people to avoid AI slop,
   that is the brand. An accent and the odd imperfect take are fine - they
   prove it is a person. If a backup Kokoro voice is ever used, the
   description says so and YouTube's altered/synthetic content flag is set.
4. **The same house rules as the other channels:** no long dashes in any copy
   or picture, no default stock portraits (hands, screens, graphics instead),
   Shorts tell the story in order (who/what and stake first, twist last),
   no licence/tool credit lines, captions without a CTA tail.
5. **Privacy on screen:** no API keys, tokens, emails, inbox, account
   balances or other people's data in a recording. Real revenue numbers only
   when Oktay decides to show them.

---

## 3. Formats

### A. The Short (9:16, 30-50 s) - the main engine

One lesson, one number, one twist.

1. **0-3 s:** the stake as a full question or claim, with the *Proof of Work*
   number on screen. *"I let AI apply to 587 jobs for me. Four were worth it."*
2. **3-25 s:** what happened, in order, on screen - the recording, the result.
3. **Last 5-10 s:** the twist / the lesson, ending on a line that loops back.

### B. The Build Log (16:9, 6-10 min)

One playbook, built in front of you. Chapters, real screen recordings, the
numbers before and after. Each long form makes 2-4 Shorts from its beats.
Source material: the books' chapters (each book is 12-14 ready-made
episodes, already researched and cited) and our skills/pipelines.

### C. Later formats (once A and B work)

- **The Number** (Short): one metric from our analytics and what it taught.
- **Mistake of the Week** (Short): one thing that cost us a re-cut, a
  rejection or a day.
- **Live build** (long): a recording of one Claude Code session start to
  finish, sped up, with narration over the key moments.

---

## 4. Look and sound

### Visual identity (must look different from Tinnitus and Crypto at a glance)

- **The desk:** a dark workspace backdrop; content sits in macOS-style
  windows (`core/window.py` already does this) - browser, terminal, editor,
  chat, analytics.
- **One signature colour** that neither existing channel uses (proposal:
  electric amber or lime on near-black), plus a monospace accent face for
  terminal/prompt text next to the main sans.
- **The camera box** - Oktay's face in a small rounded box in one corner
  (bottom-right in 16:9, above the captions in 9:16), with a thin brand-colour
  border. It is a trust device, not a talking head, so it comes and goes:
  - **on:** the first 2-3 seconds (a person says the hook), the moment of the
    twist or lesson, a personal aside ("this one cost me a week"), and the
    last line;
  - **off:** while the viewer has to read a screen, a page or a number - the
    box would sit on top of the evidence;
  - roughly 15-25% of a video's runtime; it slides in and out, never cuts.
- **A drawn monogram for Oktay** - a simple vector mark that stands in the
  camera box's spot in videos without face footage, and on the end card and
  avatar, so the layout is the same either way.
- **Motion vocabulary:** typed-out prompts (`core/typewriter.py`), cursor
  highlight and auto-zoom on clicks, terminal output scrolling, code diffs
  that animate in, before/after splits, counters that run up to the real
  number, drawn arrows and rings on the thing being read (`spotlight`).
- **Thumbnails:** the real screen or the real number, big, plus Oktay's face
  cut out from the recording (or the monogram). Never a stock face.

### What goes on screen, in order of preference

1. **Screen recordings** of the real work: Claude Code sessions, the render
   pipeline, n8n, YouTube Studio graphs (blurred where private), the job
   search shortlist, the audiobook pipeline, App Store / Play listings.
2. **Website captures** via `screencap` (public pages only, as in
   `docs/video/footage.md`).
3. **Drawn graphics and vectors**: the existing beat library
   (`docs/video/beats.md`) restyled to the new brand, plus a few new beats
   (below).
4. **Stock**: only where nothing real exists (a city, an office, a phone in a
   hand), never a portrait, never more than a handful of shots per long form.

### Voice: Oktay reads the script

**Why own voice first:** the channel is attached to a person, it teaches
against AI slop, and the books themselves say the AI voice is one of the four
tells. A human voice removes that tell on day one. It costs ~15-30 minutes of
recording per Short batch and per long form.

**Recording setup (cheap is fine):**

- A USB or lavalier mic, ~15-20 cm from the mouth, in a soft room (clothes,
  curtains, a bed nearby). No laptop mic.
- Read the script as written, one sentence per breath; re-read a sentence on
  a mistake rather than stopping the take - the edit removes the bad one.
- Camera recorded **at the same time** as the voice (phone or webcam at eye
  level, window light from the front), so lips and voice match whenever the
  box is on.
- Export: one WAV for the voice, one video file for the face, same take.

**What the pipeline needs for it** (today it only speaks synthesised lines,
and captions are timed from the synthesis):

- **`voice_import`** - take the recorded WAV plus the script, cut out the
  re-reads and long pauses, level it (loudness, light de-noise, de-ess) and
  find where each sentence starts and ends (forced alignment, e.g. a local
  Whisper model), so captions and beats sync exactly as they do with Kokoro.
- **`facecam`** - take the face video, crop it to the box, match it to the
  voice timing, and place it on the cues marked in the script
  (`face=on` / `face=off` per line).

### Backup: a Kokoro profile for this channel

For days without recording, or a quick test. The voice must differ from
`mia` (crypto/tinnitus) and from `leo`/`max` (drone). Male-only blends - the
drone notes say a female blend reads androgynous on a real script. Not slowed
down: the *Stop Making AI Slop* book says it outright, a slowed voice is the
robotic one.

Audition shortlist (only if a backup is wanted; Oktay picks by ear):

| # | Blend | Speed | Expected character |
| --- | --- | --- | --- |
| 1 | `am_michael` 60 + `am_fenrir` 40 | 1.10 | warm, steady, conversational |
| 2 | `am_puck` 50 + `am_michael` 50 | 1.10 | younger, more energy |
| 3 | `am_fenrir` 60 + `am_onyx` 40 | 1.05 | deeper, calmer, "explainer" |
| 4 | `bm_george` 50 + `am_michael` 50 | 1.10 | mid-Atlantic, stands apart from every other channel |
| 5 | `am_eric` 60 + `am_puck` 40 | 1.12 | bright, quick, Shorts-first |

The winner gets a profile in `video_automation/core/voices.py` under a new
`learn` project, named after a person like the others, status `candidate`
until it ships. **Never mix the two voices in one video** - a viewer hears
the switch.

---

## 5. First videos (pilot slate)

All from material we already have. Bracketed numbers must be read from the
ledger, logs or books before scripting - none are to be guessed.

| # | Format | Working title | Source | Proof of Work |
| --- | --- | --- | --- | --- |
| 1 | Short + long | **I made [N] AI videos. Most lost viewers in seven seconds.** | *Stop Making AI Slop* ch. 3, `retention.md` curves | our measured drop-off second |
| 2 | Short | **My AI voice sounded robotic because I slowed it down** | *Slop* ch. 7, `voice.md` | the same line at 0.9 vs 1.1 speed, A/B on screen - and the twist: "so on this channel, I read it myself" |
| 3 | Short | **587 job postings in one week. Four worth applying to.** | *Job Hunting in the Age of AI* intro, job-search shortlists | 587 → 4 counter |
| 4 | Long | **I let AI build my YouTube videos. This is the whole pipeline.** | this repo, the skills, screen recordings | article → script → voice → render → publish, timed |
| 5 | Short | **The four things that give an AI video away** | *Slop* ch. 6-9 | one real before/after of ours per tell |
| 6 | Short | **Nobody rejected you at two in the morning. A filter did.** | *Job Hunting* ch. 3 | screen of a real ATS flow (public demo) |
| 7 | Short | **The stock clip said something my voice did not** | *Slop* ch. 8, `footage.md` | a shot we had to cut, and why |
| 8 | Long | **I wrote and narrated a one-hour audiobook with AI. What it took.** | audio-book-automation, the four books | hours, chapters, cost, the store rejection we fixed |
| 9 | Short | **You are not applying to jobs. You are choosing companies.** | *Job Hunting* ch. 10 | the filter rules, on screen |
| 10 | Short | **The friendliest crypto message is the scam** | *Stop Losing Money in Crypto* ch. 5 | real public scam examples via `screencap` |
| 11 | Long | **[N] apps in the stores. What actually makes money.** | portfolio `projects.json`, store consoles | only numbers Oktay chooses to show |
| 12 | Short | **Faceless channel, month one: the real numbers** | `videos-performance` snapshots | views, retention, what we changed |

**Pilot = #1, #2, #3 as Shorts and #4 as the first long form.** They cover
three pillars (AI content, jobs, building with AI) and each has a number we
already own.

### Content pillars (the long-run mix)

1. **Making content with AI** - faceless channels, voices, retention, slop
   (*Stop Making AI Slop*, this repo). ~35%
2. **Building with Claude / automation** - pipelines, skills, n8n, agents. ~25%
3. **Work in the AI age** - job search, portfolio, skills that still pay
   (*Job Hunting in the Age of AI*). ~20%
4. **Money** - apps, stores, ads, books, and not losing it to crypto scams
   (*Stop Losing Money in Crypto*). ~20%

---

## 6. Build plan

### Phase 0 - identity (this week)

1. Pick the name; check `@oktaybuilds` (or the chosen handle) on YouTube and
   TikTok; register both.
2. Recording test: Oktay reads the script of Short #3 (about 40 s) with mic
   and camera at once. We check the sound, the light and the framing of the
   camera box before writing more scripts.
3. Brand kit: signature colour, fonts, monogram, camera-box frame, channel
   banner, avatar, end card. Registered as a new `Brand` in `core/brand.py`.
4. Optional: the Kokoro backup audition.

### Phase 1 - tooling (reuse first)

Reused as is: the long-form and Short engines, captions, `screencap`,
`window`, `typewriter`, beats, thumbnails, `retention_check`, `script_check`.

New:

- `video_automation/learn/` - the project module (build script like
  `crypto/build.py`), brand and voice wired in.
- **`voice_import`** and **`facecam`** (section 4) - the recorded voice
  aligned to the script, and the camera box placed on its cues. Needed before
  the first video.
- **`screenrec`** - record a region of the Mac screen (ffmpeg avfoundation),
  log clicks and keystrokes, then re-render offline with auto-zoom to the
  cursor, click ripples, the brand frame and a privacy blur list. The single
  most important new tool for this channel.
- **New beats:** `terminal` (typed command + scrolling output), `prompt`
  (a chat bubble typing out, with the reply arriving), `diff` (code lines
  going red/green), `receipt` (the Proof of Work counter), `split`
  (before/after on one frame).
- `docs/video/projects/learn.md` - voice, copy, sources, privacy list.
- `/video-learn` skill - the build order, like `/video-crypto`.

### Phase 2 - pilot (2-3 weeks)

- Build and publish the pilot (3 Shorts + 1 long). TikTok gets the Shorts.
- New YouTube and TikTok credentials for `publish-video` (new channel = new
  OAuth token and new n8n workflow rows; Instagram/Facebook can wait).
- After 14 days, read the numbers with `videos-audit` and add the
  channel to `videos-performance`.

### Phase 3 - cadence

- 3 Shorts a week, 1 long form every 2 weeks (each long form feeds 2-4 of
  the Shorts).
- Every video logged in the video ledger, same as the other channels.

### Phase 4 - more of Oktay, if the numbers say so

Compare retention on videos with more vs less camera-box time. If the face
holds viewers, try full on-camera intros and a few talking-head Shorts;
if not, keep the box small and rare. Decide from the curves, not before.

---

## 7. How it earns (no CTA in the video, links in the description)

- The four audiobooks - each video points to the one it came from.
- The apps and sites (Tinnitus Help, Crypto Wiki, Love Swipe, Muscle Pal ...)
  as real examples, never as ads.
- The portfolio (oktayshakirov.com) - this channel is also a public
  work sample.
- YouTube Partner Program once eligible.

---

## 8. Open decisions for Oktay

1. The name (recommended: **Oktay Builds**), and whether the handle is free.
2. Mic and camera you already have (decides whether anything needs buying).
3. Which real numbers may appear on screen: app revenue, book sales,
   channel earnings - yes, no, or later.
4. Language: English only (recommended - the books, the voice and the other
   channels are English).
