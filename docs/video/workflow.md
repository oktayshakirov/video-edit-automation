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

**Offer three to five candidates with a reason each**, then stop and wait. The
reason is the part that matters - a title that is already a question, an honest
answer that is counterintuitive, a table of figures that earns a `bars` beat, a
query people actually type into YouTube. A list of slugs with no reasoning is
not a suggestion.

**Do not start building until the user has picked one.**

An off-site topic - one with no article - is a fine thing to build when the user
asks for it, and is never offered from this list.

## 2. Script the pair together

For crypto and tinnitus, **the long and the Short come from one article and are
written in one pass.** They are not the same video at two lengths:

- The **long form** walks the mechanism and earns its conclusion. See
  `longform.md`.
- The **Short** does the single move the long form spends three chapters setting
  up, and opens by asking its own title question. See `shorts.md`.
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

Run `tools/audit_assets.py` before rendering. Outputs go to the Desktop; they
are uploads, not repo artifacts.

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
