# Handoff — `first-bitcoin-transaction`, ready to publish (2026-10-02)

Built and re-cut across a build session. **Open a fresh session and run
`/publish-video`** — that skill owns the sequence, the platform split and the
site registry entry, and this file does not restate any of it.

**Read "One thing still open" at the bottom before you upload anything.**

## What was built

The OG-bio explainer pair for thecrypto.wiki, long form and Short, from one
page.

**Source:** the crypto-og bio `hal-finney`
(`~/Coding/crypto-wiki/content/crypto-ogs/hal-finney.mdx`)
→ https://thecrypto.wiki/crypto-ogs/hal-finney

There is **no `posts/` article** behind this pair, so both scripts set
`SOURCE_POST = None` and `SOURCE_OG = "hal-finney"`. `tools/topics.py` only
scans `posts/`, so it will never show this page as covered — that is expected
and not a bug to chase.

**Build scripts, committed (`6fd0909`):**

- `projects/crypto-long/first-bitcoin-transaction.py`
- `projects/crypto-short/first-bitcoin-transaction.py`

### Long form — 3:53 (233.99s), 16:9

| | |
|---|---|
| video | `/Users/oktayshakirov/Desktop/first-bitcoin-transaction-long.mp4` |
| thumbnail | `/Users/oktayshakirov/Desktop/first-bitcoin-transaction-long-thumb.jpg` |
| captions | `/Users/oktayshakirov/Desktop/first-bitcoin-transaction-long.srt` |
| metadata | `/Users/oktayshakirov/Desktop/first-bitcoin-transaction-long.md` |

YouTube title: **What Was the First Bitcoin Transaction?** — a phrase people
type, and a different query angle from the Short. Six chapters, all well over
10s with the first at 0:00; the timestamps, the description, the tags and the
credits block are all in the `.md`. **Read the `.md` rather than re-deriving
any of it** — it carries an attribution line the licence needs (below).

### Short — 47s (46.65s), 9:16

| | |
|---|---|
| video | `/Users/oktayshakirov/Desktop/first-bitcoin-transaction-short.mp4` |
| cover | `/Users/oktayshakirov/Desktop/first-bitcoin-transaction-short-thumb.jpg` |

The cover is 1080x1920, one file, same photograph and same headline as the
long form's. There is no `.md` sidecar for a Short.

## Things the publish session should know

- **The angle is a mechanism, not the Satoshi question.** `satoshi-nakamoto`
  already names Hal Finney three times and runs him as a struck item in its
  candidates checklist, so the "was he Satoshi?" video exists. This pair
  argues the thing only he can carry: in 2004 he built reusable proof of work,
  whose token ownership sat on **one trusted server**, and five years later he
  received the first Bitcoin payment — the same sequence with that machine
  removed. If any platform copy summarises the video, summarise *that*, not
  the Satoshi rumour.
- **Attribution is required in the description and is already in the `.md`.**
  The photograph is a 1972 Daily News-Post staff photo (public domain, via
  Wikimedia Commons) and the trusted-server fact is sourced to Finney's own
  RPOW pages via the Nakamoto Institute, because the bio does not state it.
  Keep both lines wherever the description goes. Details and the rejected
  candidates are in `assets/crypto/finney/CREDITS.md`.
- **There is no photograph of adult Hal Finney anywhere.** Wikidata's image
  property points at the 1972 shot and nothing else; the only adult portrait
  is a fair-use 268x370 upload on English Wikipedia, which is not usable on a
  monetised thumbnail. **Do not go looking for a better one and do not
  substitute the fair-use file.** He appears in the two beats that have a
  picture column (2:52 and 3:38) and on both thumbnails, which is the ceiling.
- **Opener, for the fortnightly ledger:** both cuts open on a **redacted
  hook** whose hidden phrase is his name — "The first bitcoin ever sent went
  to [Hal Finney]". Tag it as redacted-mode, not statement-mode; the two are
  separate cohorts in the E1 ledger.
- **No financial advice, and the topic is structurally safe.** No price, no
  level, no prediction, no platform rated, nothing recommended — the whole
  argument is that the first payment was worth nothing. No live price, chart,
  ticker or broker name appears in any shot; three stills were rejected during
  the build for having a candlestick chart or the word TRADING in frame. The
  compliance line is spoken at 3:44 over rain and is in the description.
- **The navigation chrome is off**, as it now is by default — no ticked
  chapter rule along the bottom. The gold border around clip shots is
  `clip.py`'s own hairline and is on every crypto long form; it is not a
  defect.

## One thing still open

**Neither cut has been explicitly approved.** Every change the user asked for
is in and was verified on the rendered frames, but they have not said the cuts
are finished. **Confirm before uploading.** A Reel and a Telegram post cannot
be un-sent.

## Two things the user settled during the build

**The pronunciation.** `Finney` phonemizes to `fˈɪni` - which reads correctly
on paper and was wrong in the mouth. Four variants were synthesised and the
user picked the respelling: the spoken half now says **`Finnee`** (`fˈɪniː`,
a clear long vowel on the last syllable) everywhere his name is read aloud,
including the chapter card's `spoken_title`. **The caption half, the SRT, the
on-screen cards, the thumbnails and the description all still read "Finney"** -
the respelling exists only for the synthesiser. If any platform copy is typed
by hand, it is "Finney".

**The ALS glitch.** `He dies of A.L.S.` phonemized to
`hiː dˈaɪz əvə dˈɑːt ˌɛlˈɛs` - espeak reads the full stops aloud as the word
"dot" once an initialism sits inside a sentence. The spoken half now says the
disease's full name; the timeline card still reads "Dies of ALS".

## Also on the Desktop, and not part of this handoff

`~/Desktop/.fbt-backup/` holds the previous long-form render, kept only in
case the re-render for the `BLOCK 170` overflow had to be rolled back. It is
superseded. **Delete it rather than publishing from it.**
