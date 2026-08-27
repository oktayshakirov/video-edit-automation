# The run

Identical for every project. What changes per project is the source site, the
voice and the safety rules - not these steps. `/video-drone` skips step 1 and
usually builds one format instead of a pair.

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

Writing them together is what stops the Short from being a trailer for the long
one. Read `narration.md` before writing a line of either, and the project doc
for what may and may not be said.

## 3. Build

One Python file per video under `projects/<project>-<format>/<name>.py`. Set
`SOURCE_POST = "<article-slug>"` near the top so `tools/topics.py` can see it -
or `SOURCE_POST = None` for an off-site topic.

Run `tools/audit_assets.py` before rendering. Outputs go to the Desktop; they
are uploads, not repo artifacts.

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
   starts.
2. **Write the handoff** to `HANDOFF-PUBLISH.md` at the repo root: what was
   built, the absolute path of every file, the source article slug, and anything
   still undecided. `/publish-video` reads this.
3. **Tell the user to open a fresh session and run `/publish-video`.**

**The build session does not publish.** A build loop burns its context on
renders, re-cuts and screenshots, and publishing is the irreversible half - a
Reel and a Telegram post cannot be un-sent. It gets a clean context by design.
Committing first is what makes the seam safe: the fresh session can read the
repo instead of trusting a summary.
