# The run

Identical for every project. What changes per project is the source site, the
voice and the safety rules - not these steps. `/video-drone` skips step 1 and
usually builds one format instead of a pair.

**A shared run is not a shared channel.** These are the mechanics - suggest,
script, build, review, hand off - and they are here so the two build skills
cannot drift apart on the parts that were never supposed to differ. Everything
that gives a channel its own voice stays in its own skill and its own project
doc: what the subject *is*, what a picture of it looks like, which beats carry
it, what may never be said, and what the opener is allowed to claim. A
thecrypto.wiki explainer and a tinnitushelp.me explainer should not be
mistakable for each other, and following the same five steps is not what would
make them so.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with
`PYTHONPATH=.`.

## 1. Suggest topics, do not pick one

```bash
python3 tools/topics.py crypto      # or: tinnitus
```

Coverage is derived, never tracked: an article is covered when a script in
`projects/` names it or the site's `videos.json` points a video at it. There is
no list to maintain, so there is nothing to forget to update.

**That list says what has no video yet. It does not say what anyone wants to
watch.** Cross it with the channel's demand map (`demand/tinnitus.md`,
`demand/crypto.md`; the method is `demand/README.md`) before suggesting
anything (2026-10-25, E11).

**Offer three to five candidates**, then stop and wait. Each one carries:

- **the demand evidence** - a standout from the map (title, channel, views,
  ratio to that channel's median), one of our own standouts, or a brand-new
  search term with few answers yet (E8). Mark it **"no evidence"** when there
  is none, and say so plainly; it may still be picked, but not by default.
  When the map has nothing on the subject, search it on YouTube now (one
  branch, `demand/README.md`) and add what you find to the map;
- **the bridge**, when the article's subject is a mechanism with no demand of
  its own: the outcome the viewer already searches, and the format that ties
  them ("If you don't understand X, you don't understand Y");
- **the title format** to borrow, from the map's formats table, with *why*
  it works and its fit verdict for this channel - never a format marked "no";
- what the article gives the video - a counterintuitive honest answer, a table
  that earns a `bars` beat, a real thing to show.

A list of slugs with no reasoning is not a suggestion, and neither is a list
with no demand column.

**A covered article is not used up when its video missed the demanded
angle.** `topics.py` hides it, so check the map for it too. When the map
shows the subject wins on a different promise from the one our video made,
offer a **re-angle**: a new pair from the same article, on the promise that
wins. The first case: "Why Does Tinnitus Spike?" (26 views) against five
channels standing out on *what to do during a spike*, from an article that
already has that section (`demand/teardowns/manage-a-tinnitus-spike.md`).

**Once one is picked, and its `DEMAND` names a standout, write its teardown
before the script** (`demand/README.md`, "Teardown"), unless one is already
in `demand/teardowns/`. The script takes its shape - promise, opening order,
number of points, kind of proof - and none of its words.

**Do not start building until the user has picked one.**

An off-site topic - one with no article - is a fine thing to build when the user
asks for it, and is never offered from `topics.py`. **A subject the demand map
proves (2+ channels with standouts) that no article covers** may be offered,
labelled *article first*: the article is written and published through
`/publish-content-tinnitus` or `/publish-content-crypto`, and the pair is
built from it afterwards. The site stays the place the video sends people.

## 2. Script the pair together

For crypto and tinnitus, **the long and the Short come from one article and are
written in one pass.** They are not the same video at two lengths:

- The **long form** walks the mechanism and earns its conclusion. See
  `longform.md`.
- The **Short** does the single move the long form spends three chapters setting
  up, and opens by asking its own title question. See `shorts.md` - and its
  2026-10-13 section for when the move needs setup the viewer does not have.
- The **long-form YouTube title must be a phrase people type into YouTube
  search** - "how to X", "why does X", "what is X", "X vs Y" where both are
  searched. Never the Short's curiosity hook reworded. The Short is pushed by
  the Shorts feed and keeps its teasing title question (`shorts.md`); a
  brand-new long-form earns almost no browse or suggested impressions and is
  found by search or not at all, so its title has to *be* the search. Pick a
  different query angle from the Short. See `longform.md`.

Writing them together is what stops the Short from being a trailer for the long
one. Read `narration.md` before writing a line of either, and the project doc
for what may and may not be said.

**Write the opening as one unit, first.** The title question (sentence 1), the
redacted `hook="... [word] ..."` on screen, and sentence 2 - a partial answer
that *says the hidden word*, so it is revealed on the beat. Both the Short and
the long form take `hook=`. See `shorts.md`, "The opening hook: a redacted
headline", and `narration.md`, "Revised 2026-09-21".

**The hidden word is never the answer to the title question.** Sentence 2
has to say it, so if `[Hal Finney]` is hidden, "Hal Finney." is sentence 2
and the viewer has what they came for at five seconds. The same goes for an
opener's `at_word=`. See `narration.md`, "Confirmed 2026-10-11".

**And the hidden word has to be worth revealing (2026-10-22).** A
placeholder - `[one source]`, `[two things]` - is not the answer, and it is
not a payoff either: the pill lands and the viewer has learned nothing. When
the only safe word to hide is a placeholder, do not redact: use the pair's
long-form opener, a `Counter`/`Stamp`, or the hook in statement mode. See
`shorts.md`, "A hidden word must be worth revealing".

**Gate: run the opening check on the Short before preflight or build, and
put its output in the script handover.**

```bash
PYTHONPATH=. .venv/bin/python tools/opening_check.py projects/<project>-short/<name>.py
```

It prints the title question, sentence 2, the opener and the word it lands
on, and flags the shapes that cliffed every time they shipped. It also
prints the last line and flags one that asks (gated 2026-11-03: a Short
shipped ending on a question after the 09-11 rule). Then answer
its last question in one line in the handover: *can the title question be
answered from sentences 1-2, and if so, is that answer a plain reversal with
the next question already open?* If the answer is "yes, and it confirms" or
"yes, plainly", rewrite sentence 2 before building - not after a re-cut.
The rule lived in `narration.md` for ten days and four Shorts still broke
it, because it was checked from memory rather than against the file.

**Gate: run the script check on both scripts of the pair, with the opening
check (2026-11-05).** It reads what each script will show and say and flags
the shapes the docs already forbid: a direction on crypto, a promise of
relief on tinnitus, a spoken `CBT` / `ENT` / `TMJ`, the banned windup, a
long form's outro asking for a subscribe, a Short carrying the disclaimer, a
question title with no question mark, a carded chapter with no kicker, no
`SOURCE_POST` or `DEMAND`.

```bash
PYTHONPATH=. .venv/bin/python tools/script_check.py \
    projects/<project>-long/<name>.py projects/<project>-short/<name>.py
```

A flag is a prompt to look, the same as the opening check: answer each one
in the handover in a line, or rewrite. `--rules` lists every rule and the
doc it comes from. Run against the back catalogue on 2026-11-05 it found the
banned windup in `vitalik-ethereum`, a "subscribe" outro in
`pulsatile-tinnitus` after that rule, and a spoken "CBT" plus "can help" in
the tinnitus myths quiz - each shipped after the rule it breaks.

**Pick the opener deliberately.** The redacted `hook=` is the default and the
control; `longform.openers` has Counter / Stamp / Split / Search / Flash for a
number, a belief, a comparison, a search phrase or a picture payoff. Choose by
the *shape of the topic*, not by taste. Read the last three scripts on that
channel and do not use the same opener three times running (`shorts.md`,
"Choosing the opener"). **What a given opener is allowed to assert is the
channel's business** - a verdict stamp means something different on a market
explainer than on a health video - so check the project doc before reaching
for one.

## 3. Build

One Python file per video under `projects/<project>-<format>/<name>.py`. Set
`SOURCE_POST = "<article-slug>"` near the top so `tools/topics.py` can see it -
or `SOURCE_POST = None` for an off-site topic.

Under it, set `DEMAND` to the evidence the topic was picked on, as one line -
`DEMAND = "Treble Health 'Does Tinnitus Cause Dementia?' 5.5k, ratio ?"`, or
`DEMAND = None` when it had none. `video-performance-review` tags every video
from this line, and E11 cannot be judged without it.

**The description's link is the next useful step, not "read more".** Write
the `cta` as what the article gives that the video could not: the full
table, every source, the checklist, the sessions on Spotify. The question to
ask of it: would an unbiased expert point the viewer there because it makes
the lesson more useful? If not, it is a plug, and a plug is skipped.

Run `tools/audit_assets.py` before rendering. Outputs go to the Desktop; they
are uploads, not repo artifacts.

**A script draws its generated files in a function `main()` calls, never at
module level** - a `ticker_card`, a slide, anything saved to disk. Every gate
imports the script (`opening_check`, `script_check`, preflight), and three
scripts that drew their cards on import rewrote them each time; under the
test font shim one import overwrote the committed `squid.png` in the wrong
typeface (2026-11-05). Keep the path as a constant for the shot list and do
the drawing in `cards()`; `test_every_project_script_still_imports` fails a
script that saves on import, and `ticker_card` refuses to write in a process
that drew with stand-in fonts.

**Preflight a long form before you render it.** `clip.py` raises on the
*first* shot whose footage cannot fill its slot, and it raises from inside
`render_long` - after the narration has been synthesised. A cut with four
tight slots therefore costs four full runs to find four problems, each of
them knowable the moment the timeline existed. Preflight walks the timeline
once and reports **every** slot, plus the runtime and the chapter list:

```bash
PYTHONPATH=. .venv/bin/python -m video_automation.longform.preflight \
    projects/tinnitus-long/<name>.py
```

Read the `margin` column, not the shortfall: `clip.py` reports `want / src_len`
against the clip's *whole* length and ignores `clip_at`, so a shot 9 seconds
into an 11 second clip claims it needs "0.93x slow motion" when what it has is
2.2 seconds for a 10.4 second slot. The number looks survivable and is not.

It shares the narration cache with the render, so the build that follows a
preflight does not synthesise the script a second time.

Each video produces:

| File | Needed by |
| --- | --- |
| the MP4 | publish |
| the thumbnail | publish |
| the `.srt` | publish, long form only |
| the `.md` sidecar | publish - it carries the title, description and chapters |

The `.md` is not for the user to read. It exists so the publish step is not
re-deriving a description from memory, which is how nine Shorts went live with a
dead "read more" line and no URL.

## 4. Review, and expect to go round again

Hand over the render and say what to look at. The user watches it and either
approves or asks for changes; **re-cut as many times as it takes.** This loop is
the normal case, not a failure - most rules in these docs came out of it.

**Include the feed check for the long form in the handover.** Search the
long-form's `Meta` title on YouTube in the built-in browser, read the top
results, and put our thumbnail next to the top three at 320px (`sips -Z
320`). Report three things in one line each: whether the query returns
videos with real views (it is a search people make), whether ours makes a
different promise from the top result or the same one with less proof, and
whether ours is the one the eye lands on. A thumbnail or title that loses
this check is re-cut here, before publishing, where it is cheap.
`demand/README.md`, "Packaging".

When something turns out to be a bug or a missing capability rather than a
choice, fix the code, then record the lesson under the policy in `README.md` -
narrowest doc, no cross-posting, same commit.

## 5. Approve, commit, hand off

Only once the user says they are happy:

1. **Commit everything** - the project scripts, any engine changes, and any doc
   updates the run produced. The working tree must be clean before publishing
   starts. Run `.venv/bin/python -m pytest tests -q` if the run touched the
   engine; it is about five seconds and it covers the things that cannot be
   seen by watching the render.
2. **Write the handoff** to `HANDOFF-PUBLISH.md` at the repo root: what was
   built, the absolute path of every file, the source article slug, and anything
   still undecided. `/publish-video` reads this.
3. **Tell the user to open a fresh session and run `/publish-video`.**

**The build session does not publish.** A build loop burns its context on
renders, re-cuts and screenshots, and publishing is the irreversible half - a
Reel and a Telegram post cannot be un-sent. It gets a clean context by design.
Committing first is what makes the seam safe: the fresh session can read the
repo instead of trusting a summary.

**And it does not describe publishing either.** Which file goes to which
platform, the metadata pass, the site registry entry, the social posts and
their order are all `/publish-video`'s, and it is the only copy. That sequence
used to be duplicated into every build skill; the copies drifted, disagreed
about what a Short gets, and cost a registry entry that had to be reverted and
a social post that could not be un-sent. Do not restate those steps, pre-empt
them, or re-derive them from memory.

## What every article build draws by default (2026-10-21)

For the two article channels, long form and Short. These are on without
asking - a script only supplies the words. Detail in `longform.md` and
`audio.md`. (Moved here from `/video-crypto` and `/video-tinnitus`
2026-11-05, where it was the same 56 lines twice and every engine change
had to edit both copies.)

- **Chapter cards are the band card**, long form and Short: the title typed
  into a band of the brand colour on key clicks, the riser into it and the
  cinematic flashback out of it. **Write a `Section(kicker=)` for every
  carded section** - two or three words naming the stake ("THE REJECTION",
  "THE CATCH"). Without one the long form shows "CHAPTER n" and a Short
  shows no label.
- **The opening title is the glitch slate** (`title_at=`, default since
  2026-11-04): the title split at its colon / question mark / dash, the
  search phrase big in DIN Condensed, the promise under it in the brand
  colour, glitching in and out on the title intro sound. Keep its hold
  clear of the first chapter card. `title_style="cinematic"` brings back
  the old card.
- **A disclaimer `payload` becomes the notice card** on the notification
  chime - no flag needed.
- **The video ends on the band end card** - THANKS FOR WATCHING, retyped as
  LIKE & COMMENT - **and switches off like a TV.** `endcard=` turns the card
  on; the TV-off is always there.
- **The old-film surface is arranged, not blanketed** (`core/filmfx.py`):
  the first shot clean, a section's first clip full, the rest rotating
  grain-only / clean / dust-only / full, nothing on drawn beats. `film=False`
  turns it off for one video, a number scales it.
- **A few cuts become glitch or TV static on their own**
  (`transitions.plan_special`): a glitch into a sentence that turns ("But…"),
  static or glitch alternating into chapter cards, static on a jump in time -
  about one per 45 seconds. **Open a turning sentence with "But" or
  "Actually" when it really turns**; that is what places the glitch. A
  transition set by hand on a shot always wins.
- **`reel` is the beat for a sequence the viewer should feel move** - days,
  versions, dates, steps: a strip of cards (clips, photos or text) the camera
  travels along, one card per sentence (a Short: one phrase per card, ~2s
  each). It can **dive into its last card and continue as that clip**, or
  open out of the previous clip (`enter` / `emerge`) - use it where the
  script moves from an overview into one example. `docs/video/beats.md`.
- **`post` puts what someone actually wrote on screen** - a post, a news
  headline, a transaction - and highlights the `[bracketed]` line as it is
  read. Real, sourced wording only; write its sentence as two phrases, the
  lead-in and the quote. `docs/video/beats.md`, "`post`".
- **`emphasis=[...]` punches the word a sentence hinges on onto the screen**
  as it is spoken, long form only, once or twice a minute. Pick one word or
  short phrase per minute that the whole sentence turns on.
- **`spotlight` directs a still**: the camera glides into the part of a
  photo the voice names (a line of a document, one face), one region per
  sentence; the ring snaps to the content, so regions can be rough.
  `docs/video/beats.md`, "`spotlight`".
- **Footage of a place gets a quiet bed of it** (city, rain, office,
  servers) automatically, only on clips of 3s or more - nothing to write.
  Pick clips whose folder names the place when the sound would help.
- **The title and chapter sounds are files** in `assets/brand/sfx/`, kept out
  of git. On a machine without them the build falls back to synthesized
  stand-ins - copy them over before a build that ships.
