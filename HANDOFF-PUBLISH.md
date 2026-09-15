# Handoff → /publish-video

**Built:** `crypto-exchanges-quiz` — thecrypto.wiki's **first quiz Short**
(`/video-quiz crypto`, quiz #1 for the channel). Vertical only, no long form —
the quiz format never has one.
**Source article:** `understanding-crypto-exchanges` (already has its own
long+short explainer pair — the article that taught the audience the
mechanism this quiz tests).
**Date:** 2026-09-15
**Voice:** `otis` (bare `am_puck`, ENERGETIC chain) — the quiz format's fixed
reader on both channels, not project-specific.
**Approved by the user.** Built and shipped on the first render — no re-cut
needed this session.

## Files (Desktop)

| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/quiz-crypto-exchanges.mp4` |

Runtime **89.9s** (ffprobe-checked), 1080x1920, h264/aac.

**No thumbnail, no SRT, no `.md` sidecar** — all three are format conventions,
not omissions:
- No thumbnail render: the quiz format's own picture is already four drawn
  cards, so a generated headline plate would just restate the hook. Pull the
  Reel cover from a frame of the finished render instead, same as every
  other quiz Short (`docs/video/projects/quiz.md`, `docs/publish/instagram-facebook.md`).
- No SRT: long-form only.
- No `.md` metadata sidecar: also long-form only — the quiz has no chapters
  to carry. Title/description material below is raw material, not
  pre-written copy.

## What this is

Three questions on CEX vs. DEX mechanics, each testing the same confusion
from a different angle — who holds a deposit, how a trade gets matched, what
happens when a CEX is hacked. Every wrong option is a real fact about the
*other* kind of exchange, taken straight from the source article (order book,
KYC and an intermediary are true CEX facts, offered as wrong answers to the
DEX question; self-custody via smart contract is a true DEX fact, offered as
a wrong answer to the CEX question) — so a viewer who half-remembers the
article picks the wrong mechanism, not a made-up distractor.

**No exchange is named anywhere in the script**, and no option has a
direction — every question asks about mechanism ("what does custodial mean",
"how does a trade clear with no company in the middle"), never which
exchange to use or which is safer. This is the crypto channel's standing
safety line (`docs/video/projects/crypto.md`, `docs/video/projects/quiz.md`),
and it is easier to break in this format than in an explainer, so it is
worth a second look before this goes out.

**Outro is "How many did you get?" and stops** — no "tell me in the
comments", per the format's standing rule.

**Suggested title:** "Crypto Exchanges Quiz: CEX vs. DEX" or "How Well Do You
Know Crypto Exchanges?" — Shorts titles are a curiosity hook, not a search
query, so lean on whichever reads better in the Shorts feed. The on-screen
title card itself says "Crypto Quiz: Exchanges Edition" and is not meant to
double as the YouTube title.

**Description material:** the quiz is drawn from **[Crypto Exchanges
Explained](https://thecrypto.wiki/posts/understanding-crypto-exchanges)** —
link it. No financial-advice disclaimer is spoken in the video (the quiz
format never carries one, no long form to inherit it from either), so if the
channel's standard compliance line belongs in the description text, that is
a judgement call for this step, not something scripted into the narration.

## Engine fix shipped with this build (commit below)

**`video_automation/crypto/build.py`'s `render_crypto_short` crashed on
every quiz render, unconditionally**, with `ValueError: unknown beat 'quiz'`.
Cause: the previous commit (`2f76089`, the fear-greed-index/`dial` build)
replaced the old `n = len(sh.payload[0])` reveal-count shortcut with
`item_count(sh.graphic, sh.payload)` for every shot carrying a `.graphic` —
correct for every real beat, but the quiz format's shots carry
`graphic="quiz"` as its own sentinel, not a beat `item_count` knows about,
and its reveals/marks/cues are always precomputed in `quiz.build`'s own
`plan()` closure before this code ever runs. `item_count` doesn't need to be
taught a `"quiz"` case — this loop never needed to touch a quiz shot at all,
so it now skips `sh.graphic == "quiz"` explicitly. This is the first time
the quiz format has been rendered since that commit landed, so nothing
shipped before this was affected — only this build hit it.

No doc change: the fix removes the trap rather than describing it
(`docs/video/README.md`'s own rule — a fixed bug is not documentation).

## Repo state

Committing now: the quiz project script, the `item_count` fix, and this
handoff. Everything will be pushed to `origin/main` before this session
ends.

Nothing has been uploaded or posted anywhere yet.
