# OktAI - channel plan (draft, 2026-11-17, name chosen 2026-11-21)

A third channel, next to Tinnitus Help and Crypto Wiki, but with one big
difference: **it belongs to Oktay, not to a site.** It teaches what we actually
built, measured and got wrong - the audiobooks, the video pipeline, the job
search, the apps - and shows the receipts on screen. **Oktay reads every
script himself from day one**, and appears now and then in a small camera box
in the corner. A Kokoro voice is kept only as a backup.

Status: plan only. Nothing is built, no channel or handle is registered.

---

## 1. Name: **OktAI** (chosen 2026-11-21)

- **OktAI** - Oktay, spelled so the name ends in **AI**, and read as
  **"OK, AI"**: the start of every task the videos show.
- **Tagline:** **"OK, AI. Let's build."**
- **Wordmark:** "okt" in white, "AI" in the portfolio's gold gradient.
- **Handle:** `@oktai`; if taken, `@shakirov.oktay` or similar - the handle
  matters less than the content.
- **Home:** oktayshakirov.com (no new domain for now). The "What I use"
  links page lives there.
- **Mascot (idea):** an octopus - "okt" sounds like *octo* - eight arms, one
  per pipeline. Logo and banner to be made in ChatGPT from the prompts in
  `docs/oktai-brand-prompts.md`.
- **Recurring beat:** *Proof of Work* - one real number from our own logs,
  on screen, early.
- **Focus:** AI - building with it and making money with it.

---

## 2. What the channel is

**One sentence:** a builder using AI for real work, showing what worked, what
did not, and the numbers - so you skip the mistakes.

**Who it is for:** people who want to *use* AI to make something - a channel,
an app, a side income, a job search - and are tired of hype. Mostly 20-40,
technical-curious, not necessarily developers.

**What makes it different from the other two channels**

| | Tinnitus Help / Crypto Wiki | OktAI |
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

**Every topic ships as a pair: one long form and its Short**, the same way
Crypto Wiki and Tinnitus Help do. Both scripts are written together and
recorded in one sitting (voice and camera), so one session gives a week's
pair.

### A. The Short (9:16, 30-50 s)

One lesson, one number, one twist - the strongest beat of its long form,
told on its own.

1. **0-3 s:** the stake as a full question or claim, with the *Proof of Work*
   number on screen. *"I let AI apply to 587 jobs for me. Four were worth it."*
2. **3-25 s:** what happened, in order, on screen - the recording, the result.
3. **Last 5-10 s:** the twist / the lesson, ending on a line that loops back.

### B. The Build Log (16:9, 6-10 min)

One playbook, built in front of you. Chapters, real screen recordings, the
numbers before and after. It is the parent of the pair's Short.
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
- **Dark, like the portfolio (oktayshakirov.com):** a near-black night sky
  (`#050507` to `#0a0a0f`) with slow twinkling stars, tinted glass panels
  (`hsl(240 2% 12%)` at 40%), light grey body type (`#d6d6d6`), and the
  portfolio's gold gradient (`#ffdb70` to `#ffc05c`) as the one accent.
  Poppins for type, a monospace face for terminal and prompt text. Crypto
  Wiki is gold too, but a deeper, flatter gold on black water in Futura -
  the sky, the softer gold and Poppins keep the two apart.
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

1. **Scripted screens** of the real work (`core/screenplay.py`, played and
   recorded by the build - Oktay never records his screen, 2026-11-21):
   Claude Code sessions as `Terminal` takes with the real output, public
   tools and our own sites as `Browser` takes. A logged-in view (YouTube
   Studio, n8n) is a `screencap` still of a page we export, or a drawn beat
   of its numbers.
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

- **`voice_import`** - transcribe the recording word by word with
  timestamps (local Whisper on MLX, `whisper-large-v3-turbo` - already
  installed in `create-song-automation/.venv` and the model is cached, so it
  runs offline on the M2 Pro), match the words to the script, keep the best
  take of each sentence and cut the re-reads and long pauses, then level it
  (loudness, light de-noise, de-ess). The word timings drive captions and
  beats exactly as Kokoro's timings do now, and a diff of transcript vs
  script shows every changed, skipped or stumbled word before the build.
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

**Pilot = three pairs (long + Short each): #1, #3 and #4.** They cover three
pillars (AI content, jobs, building with AI) and each has a number we
already own. A row marked "Short" above becomes the Short of the pair whose
long form covers it, or gets its own long form.

### Behind the scenes: how we make everything (one pair each)

Every pipeline we run is a long form, and its best moment is the Short.
Real recordings of the real runs; the link column is what goes in the
description (section 7).

| # | Long form | The Short | On screen | Links |
| --- | --- | --- | --- | --- |
| B1 | **How we make AI videos: explainers, quiz Shorts, drone montages** | "One article in, a long video and a Short out" | `/video-crypto` run from article to render, the quiz build, the FCPXML drone cut | MacBook, drone, our free prompt repo |
| B2 | **How we automate content for our websites** | "This article wrote, checked and published itself" (and what a human still checks) | `/publish-content-*` run, staging, deploy | hosting / domain referrals |
| B3 | **How we publish one video to five platforms** | "Five platforms, one command - and the one that still fails" (TikTok drafts / the Instagram-only Reel) | `/publish-video`, n8n, the access log | n8n, the publish checklist repo |
| B4 | **How we make audiobooks with AI** | "A one-hour audiobook, and the store that rejected it" (the subtitle mismatch) | manuscript, Kokoro render, the store upload | the four books, distributor referrals |
| B5 | **How we make sound-therapy albums** | "We sell albums of noise. Here is how they are made." | `/create-zen`: noise colours, notched noise, DistroKid | DistroKid, headphones |
| B6 | **How we make AI songs locally** | "This song never touched a studio" | `/create-song`: lyrics, ACE-Step render, a fixed section | DistroKid, MacBook |
| B7 | **How we read our channel analytics** | "Half our viewers leave at second [N]. Here is why." | `/videos-performance`: retention curves, the ledger, a rule that changed | our audit prompt repo |
| B8 | **Making money with drone footage** | "What one drone clip earns on stock sites" (real numbers only) | the drone library, the stock upload | Adobe Stock, the drone, SD cards |
| B9 | **How our job search finds 4 jobs in 587** | the 587 → 4 counter | `/job-search` run, the filter rules | the job audiobook |

### Problems we solved (Shorts, or a long form when there are three of a kind)

Each one is a real fault we hit and fixed - the "what went wrong" story is
the hook. Mined from the CHANGELOG, the memory notes and the troubleshooting
docs, so there is a long backlog.

- The AI voice sounded robotic - each sentence was a cold start.
- The publish tunnel died mid-upload at the time limit.
- TikTok said "sent to inbox" and the draft never arrived.
- Facebook kept posting a Reel we meant for Instagram only (still unsolved -
  a "we have not fixed this yet" video is honest and rare).
- A site build failed on the font loader until we self-hosted the font.
- The Mac disk filled up with build caches - what was safe to delete.
- Long dashes kept sneaking into on-screen text, so the code now forbids them.
- Stock portraits made every video look the same, so faces are banned.

**Rule for every topic:** before the script, list which tools appear on
screen and look each up in `links.json`; a tool without a program gets no
pitch, a tool with one gets its one line.

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

1. Name chosen: OktAI. Check `@oktai` (fallback `@shakirov.oktay`) on YouTube and
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

**Built 2026-11-21** (how to use them: `docs/video/projects/oktai.md`):

- The `OKTAI` brand - portfolio gold, the `oktai-night` backdrop, the
  "oktAI" wordmark (`tools/oktai_brand.py`).
- **The recorded voice** (`video_automation/core/recorded.py`, section 4's
  `voice_import`): Whisper word timings, last good take per sentence, room
  tone in the cuts, -14 LUFS, a report of every changed word. Works for the
  long form and the Short: `voice=Recording(file)`.
- **The camera box** (`video_automation/core/facecam.py`): cut with the
  voice's edit so the lips match, face found automatically, slides in on
  the hook, the last line and any phrase named.
- **Scripted screens** (`core/screenplay.py` + `core/screenrec.py`,
  2026-11-21): a browser or terminal take played in headless Chromium and
  recorded with its own event log, then re-cut offline - idle sped up,
  auto-zoom to clicks, typing and arriving results, a drawn cursor, gold
  click ripples, mosaic blur, framed in the wide `window=`.

Still to build:

- Poppins in captions and drawn beats (they use the engine's global fonts).
- **New beats:** `terminal` (typed command + scrolling output), `prompt`
  (a chat bubble typing out, with the reply arriving), `diff` (code lines
  going red/green), `receipt` (the Proof of Work counter), `split`
  (before/after on one frame).
- `docs/video/projects/learn.md` - voice, copy, sources, privacy list.
- `/video-learn` skill - the build order, like `/video-crypto`.

### Phase 2 - pilot (2-3 weeks)

- Build and publish the pilot (3 pairs). TikTok gets the Shorts.
- New YouTube and TikTok credentials for `publish-video` (new channel = new
  OAuth token and new n8n workflow rows; Instagram/Facebook can wait).
- After 14 days, read the numbers with `video-audit` and add the
  channel to `videos-performance`.

### Phase 3 - cadence

- Pairs, like the other channels: one long form and its Short per topic,
  1-2 pairs a week to start, one recording session per pair.
- Every video logged in the video ledger, same as the other channels.

### Phase 4 - more of Oktay, if the numbers say so

Compare retention on videos with more vs less camera-box time. If the face
holds viewers, try full on-camera intros and a few talking-head Shorts;
if not, keep the box small and rare. Decide from the curves, not before.

---

## 7. How it earns

Every video teaches something we really use, so the tool in the video is
the natural link in the description. Nothing is recommended that we have
not used ourselves.

### Referrals and affiliates - mapped to the videos they belong in

| Program | Fits videos about | What it is |
| --- | --- | --- |
| **DistroKid** referral | AI songs, sound-therapy albums, making money with AI music | the distributor we put the zen albums on |
| **Adobe Stock** (contributor / affiliate) | making money with drone footage, stock footage | where drone clips can be sold |
| **Amazon Associates** | the gear: MacBook, drone, mic, camera, SSDs | the things on the desk in every video |
| Tools we use that have a referral program (hosting, domains, audiobook distributors, n8n cloud, etc.) | the video where that tool is on screen | checked per tool before the script |
| Our own: the four audiobooks, the apps, the sites | the matching topic | own products, no program needed |

Before the first link goes live, join each program and **read its terms**:
what has to be disclosed, where links may be posted, and what keeps the
account active (Amazon, for example, closes accounts with no sales in the
first months). Pick Amazon.com or Amazon.de Associates by where the audience
turns out to be - the analytics will say.

### How the links appear

- **In the long form's script:** one spoken line, **at the moment the tool
  is on screen**, said as part of the story - *"the album went out through
  DistroKid - my link is in the description if you want to try it."* Once
  per tool, never a list, never in the first 30 seconds.
- **In the Short's script:** no spoken pitch (the Short stays a story that
  loops, as on the other channels); the link goes in the description and
  the pinned comment.
- **Description block,** same order every time: the video's tools with
  links, the gear, the related audiobook, then the disclosure line:
  *"Some links are affiliate links: if you buy through them I earn a small
  commission, at no extra cost to you."* Plus each program's own required
  wording (Amazon's "As an Amazon Associate I earn from qualifying
  purchases").
- **A "What I use" page** on oktayshakirov.com (`/uses`): every tool and
  piece of gear with its link. TikTok descriptions cannot hold clickable
  links, so the TikTok bio points there; YouTube descriptions can also link
  to it instead of listing everything.
- The build writes the description block from a links file
  (`projects/learn/links.json`: tool → URL, program, required wording), and
  the script check flags a long form that names a tool without its line.

### Sharing our skills - the free taste, the paid kit

The skills and pipelines are what make the videos credible. Share the
*method*, keep the *engine*.

| Share (free, GitHub) | Sell (small paid kit, Gumroad or Lemon Squeezy) | Keep private |
| --- | --- | --- |
| A trimmed skill or prompt per video: the retention checklist, the narration rules, the audit questions, the publish checklist | The full prompt pack for one workflow (e.g. "the faceless Short kit": script prompts, checks, the build order) with a template project | The render engine, beat library, voice blends, n8n workflows, every token, key and account detail |

- A free repo per topic (`oktai/ai-video-prompts` etc.) is the lead:
  link it from the video, the paid kit is linked from the repo's README.
- **Before anything is published:** a secret scan (tokens, keys, emails,
  local paths, private URLs) and a read-through. Nothing leaves the machine
  without that.

### Also

- YouTube Partner Program once eligible.
- The portfolio - the channel is a public work sample, so freelance and job
  offers are part of the return.

---

## 8. Open decisions for Oktay

1. ~~The name~~ - **OktAI**, chosen 2026-11-21. Check `@oktai` on YouTube and TikTok.
2. Mic and camera you already have (decides whether anything needs buying).
3. Which programs to join first (DistroKid, Adobe Stock, Amazon .com or .de).
4. Which skills go into the free repo, and whether a paid kit is wanted.
5. Which real numbers may appear on screen: app revenue, book sales,
   channel earnings - yes, no, or later.
6. Language: English only (recommended - the books, the voice and the other
   channels are English).
