# Teardown: What Is A SEED Phrase?? How It Is Generated
CoinGecko, 54.5k views, 11x its median (2026-10-27 `outliers`), published
2023-09-28. https://youtu.be/lOiVGTuh7dE
Transcript: youtube-audit/research/transcripts/2023-09-28__what-is-a-seed-phrase-how-it-is-generated__lOiVGTuh7dE.md (local only)

Read beside it: CoinGecko "Can Someone Guess My Bitcoin Seed Phrase?"
(18.8k, 2024-11-18, `1Oy0Eeo90qw`), the same channel answering the question
the first video's comments asked.

## The promise
Title and animated cover together: *how* the words are generated, not only
what they are. For someone who already has a phrase and has never wondered
where it came from - problem-aware, not a beginner.

## The opening (promise / proof / plan, with times)
Promise at 0:00 - "have you ever wondered how they really work?" by 0:20.
No proof step (the channel's name is the proof). No plan beyond chapters.
The decode ("a master private key in human-readable format") lands at
0:25, before any mechanism.

## The structure (chapters, points, length, wpm, the turn, the CTA)
3:28, 491 words, 142 wpm, six chapters: intro, why they matter, how they
work, BIP39, the process, conclusion. One turn: the wordlist's four-letter
rule, then the bits-to-words process at 1:38. Ends on the passphrase as an
"advanced" extra and a plug for another video.

## Rewatched and skipped (heatmap)
**Most replayed: 1:38-2:09**, the whole bits-to-words process (1.00 at
1:38, 0.90-0.96 to 2:09). Least: 2:51 onward, the passphrase and the
outro. The mechanism is what people came for; the extras are skipped.

## What satisfied viewers (comments)
The top comment (21 likes) is "This is confusing as hell" - the process was
narrated over an animation without the numbers being shown landing on
words. Then, repeatedly: "can't a hacker just try word combinations from
this list?", "does the generator know the phrases already created?", "how
is it linked to an address?", "why save private keys when the seed is all
of them?". The second video answers the first one's guessing question with
arithmetic and its comments are relief ("took a weight off my shoulders",
"exactly the question I was wondering").

## The failures beside it
From the same search: "Your Seed Phrase Wasn't Stolen - It Was Guessed"
(CRYPTO LADY, 31k, 1.1x) - the fear angle did not stand out. Long
general-purpose explainers (Ledger 17 min, Sovereign Money 23 min) sit
below their channels. The standouts are short and mechanism-first.

## Our version - keep, cannot have, replaced by, rule limits
- **Keep:** the promise (how the words are made), the length class (ours
  ~3:45), the mechanism as the centre, and the guessing question as the turn
  - the two CoinGecko videos together are our one video.
- **Fix what confused them:** draw it. `mnemonic` shows real bits, the
  checksum, the real index and the real BIP39 word per row, so the step the
  top comment could not follow is on screen, not narrated over a cartoon.
  Answer the unanswered comments in order: guessing (the odds chapter), the
  address (`diagram`, words to seed to keys to addresses).
- **Cannot have:** their animation style or wording. Ours is the article's
  facts in our words, drawn in the channel's beats.
- **Replaced by / added:** the article's turn the standouts never make -
  almost every loss is a person, not the math - with its three composite
  thefts as a `grid`. That is the sceptic's payoff and keeps the passphrase
  (their skipped tail) as one short practical chapter instead of a tail.
- **Rule limits:** no wallet or product is recommended, nothing about
  price. The guessing figures are arithmetic on the article's 128 bits,
  said as an order of magnitude, never as a promise of safety ("as long as
  the wallet's randomness is real").
