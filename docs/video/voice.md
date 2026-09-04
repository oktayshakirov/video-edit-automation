# Voice and synthesis

How Kokoro actually behaves, and how a written line becomes audio. Shared by
every narrated video on every project - `narration.md` is about *writing* the
line, this is about *speaking* it.

Each project's own roster and approved voice live in its `projects/*.md`; what
is here is true regardless of which voice is selected.

## Backends and profiles

Backends live behind `synth_phrase`, in quality order: **kokoro** (local,
unlimited, Apache 2.0, default), **edge** (Microsoft neural voices, free, no key,
but a network call and throttleable), **say** (macOS legacy, last resort).

Model files: `~/.local/share/kokoro` (~350MB). Installed as **kokoro-onnx**, not
the PyTorch `kokoro` package — that one depends on spacy, which has no Python
3.13 wheels and fails to build, and would add ~2.5GB of torch.

**Always pass the profile explicitly.** `voice=None` still resolves to a
default voice, but the mood defaults independently, so the defaults do not
describe one coherent recipe. `profile_args` is the only call that keeps voice
and chain together — and half a profile is a different voice.

A retired default's chain stays registered even when no profile uses it, because
shipped videos and CHANGELOG entries refer to that sound by name. Drone's
`melancholic` is the example: retired when `leo` was approved, still registered.
Do not delete a chain because nothing currently selects it.

**Every voice lives in `video_automation/core/voices.py`.** A profile is the
whole recipe — voice, Kokoro speed and post chain — because those three are one
decision, not three. Profiles are named after people; the Kokoro voices
underneath are an implementation detail.

```bash
.venv/bin/python -m video_automation voices list        # all profiles
.venv/bin/python -m video_automation voices show leo    # full recipe
.venv/bin/python -m video_automation voices render leo  # sample to Desktop
```

**`status` is not a rating.** `approved` means it shipped in a finished video;
`candidate` means the user shortlisted it by ear and has not decided. Do not
promote one without being told to.

**A voice is a `(510, 1, 256)` style tensor, not a model**, so a weighted sum is
a new speaker identity the model renders as one person — not two voices mixed as
audio. `voice_style()` accepts a name, a `{name: weight}` mapping, or `None`.
`Kokoro.create` takes the resulting array directly.

Why a blend: `am_onyx` was chosen by ear over five alternatives, but the model
card grades it **D on 10–100 minutes of data**, the weakest of the American
males. `am_puck`, `am_michael` and `am_fenrir` are all **C+ with hours**. The
60/40 keeps the onyx character on a steadier base, and was picked over straight
onyx and eight other mixes for sounding more human. Grades are in the model
card's `VOICES.md`; the best English voices overall are `af_heart` (A) and
`af_bella` (A−), both female.

**Kokoro cannot clone a voice.** No training or fine-tuning code has been
released, so blending existing embeddings is the ceiling without leaving Kokoro.
A small CC0 community collection exists at `n33kos/kokoro-voices`.

**Kokoro has no emotion parameter.** Mood comes from three stacked levers, and
the writing carries most of it:

1. **Script construction.** Motivational = short declaratives, hard consonants,
   imperatives, full stops as beats. Melancholic = long vowels, soft consonants,
   no imperatives, clauses that trail rather than land.
2. **Pace** — `KOKORO_MOODS`, roughly 0.80 sad to 0.95 motivational.
3. **Post-processing**, which does more than expected.

## Sentences are synthesised in runs, not one at a time

**The user's note was that the presentation "doesn't sound human" and that the
breaks are unnatural, and the largest cause was architectural rather than the
model.** `build_narration_aligned` used to call the synthesiser once per
sentence and concatenate the results with `anullsrc` silence. Two consequences,
both measured on the proof-of-stake script:

- **Every sentence was a cold start.** Five consecutive lines synthesised alone
  opened at 258, 271, 229, 227 and 246 Hz — every one a fresh sentence-initial
  reset, high in the speaker's range. The same five as one utterance sat at
  199 Hz falling to 193: a calm register with real paragraph declination. A
  script of cold starts is what "reading a list" sounds like.
- **Every pause was digital zero.** Each sentence was also hard-trimmed at both
  ends by `librosa.effects.trim`, so the audio floor dropped to absolute
  silence roughly sixty times in a 3:30 video, with no breath and no decay.

Sentences now go to the model in **runs**, and a run breaks where the *script*
asks for a real pause (`RUN_BREAK_GAP`, 1.0s) — a checklist's verdict silence
or a statement card is a written beat and the silence is the point, so joining
across it would smooth away what the gap was buying. Inside a run the model's
own breaths are kept and `_pad_pause` tops them up to the scripted `gap` by
inserting into the **quietest point** of the existing pause, so the decay
before and the onset after survive. Measured on the same seven lines: internal
absolute-silence gaps went 7 → 3.

**What this does not fix.** Kokoro is an 82M model with no prosody control and
no emotion parameter. The register and the joins are much better; the ceiling
is unchanged. Anything beyond it is an engine change, and the options
researched — ElevenLabs (word-level timestamps, `<break>` tags, an IPA
pronunciation dictionary; needs a paid tier for monetised video), Chatterbox
(MIT, but CPU-only on Apple Silicon) and Orpheus (Apache, needs a GGUF/LM
Studio path) — are a decision the user takes by ear, not a default to change.
`synth_phrase` remains the only place an engine is named, so the swap stays
cheap whenever they want it.

## A one-word sentence has nothing to fall from

**"Money." was flagged as sounding like a question rather than a statement.**
Measured on the shipped audio, the pitch runs 211 → 255 → **274** → 200 → 206
Hz: it peaks mid-word and ends roughly *level*. A contour that does not resolve
downward is heard as unfinished, which is heard as a question.

This is the same failure this doc already records for "Do not." — a fragment
cannot cash the pause the gap table buys it — arriving on a one-word *answer*
rather than a one-word imperative. Run-based synthesis helps, because the line
now falls out of the sentence before it instead of starting cold. But the rule
generalises: **a one-word sentence is a rhetorical device on the page and a
liability in the mouth.** Keep it only where the preceding line hands it real
momentum, and never as the first line of a run.

## Check every proper noun with espeak, not just the risky-looking ones

`Ethereum` shipped mispronounced. It phonemizes to `ˌiːθɚɹˈiːəm` —
"ee-thuh-REE-um", stress on the wrong syllable — where `Etheerium` returns the
correct `iːθˈɪɹiəm`. The phoneme rule was being applied only to words that
*looked* risky: initialisms, tickers, invented brand names. **A proper noun
that looks like an ordinary English word is exactly where this hides.** Respell
in the spoken half of a `(caption, spoken)` pair.

## Ethereum, and checking a brand name you think you know

`Ethereum` phonemizes to `ˌiːθɚɹˈiːəm` — "ee-thuh-REE-um", stress on the wrong
syllable and a schwa where the vowel wants to be `ɪɹ`. It shipped, and the user
caught it.

    espeak-ng -v en-us -q --ipa "Ethereum"    # ˌiːθɚɹˈiːəm   wrong
    espeak-ng -v en-us -q --ipa "Etheerium"   # iːθˈɪɹiəm     right

The respell goes in the **spoken** half of a `(caption, spoken)` pair, exactly
as `Binance`/`Bynanse` already does. The wider lesson is that this doc's
phoneme rule was being applied only to words that *looked* risky — initialisms,
tickers, invented brand names. **`Ethereum` looks like an ordinary English
word and is not one.** Check every proper noun in the script, not the ones that
feel like they need it.

## Hold a word by writing a pause, not by respelling the vowel

The outro's "So - would you rather..." was asked to sound like a drawn-out
"soo would you rather", for a more human close. **Respelling does not work:**
espeak reads `Soo` as `sˈuː` ("sue") and `Sooo` as `sˈuːoʊ`, both the wrong
vowel, and Kokoro has no per-phoneme duration control.

What does work is punctuation, measured in the engine rather than guessed:

| written | pause after "So" |
|---|---|
| `So -` | **none** — it runs straight through |
| `So,` | ~150ms |
| `So...` | ~170ms, vowel intact |

So the hold is a *pause*, not a longer vowel. The ellipsis goes in the **spoken**
half of a `(caption, spoken)` pair so the caption keeps its hyphen, per this
file's own "only a hyphen goes on screen" rule.

## Do not write a two-word imperative for a synthesiser to read

"Do not." was written as its own sentence with a 0.90 after it, straight out
of this doc's own advice about imperatives landing in silence. On the page it
is the strongest line in the section; read by Kokoro it is **two syllables and
then nothing**, and the user's note was that it loses the human sound of the
voiceover. A person saying "Do not." carries it with emphasis and a falling
pitch, and there is no emphasis to give.

**Write the full sentence and let the gap do the work.** "Do not make that
mistake." is the same beat, still lands on its own, and gives the synthesiser
enough to read as speech. The gap table is unchanged - what changed is that a
fragment cannot cash the pause the table buys it. This does not retire the
imperative rule; it bounds it: **an imperative needs a subject and a verb.**

## Utterance-final words get dragged, and it sounds like a glitch

Measured on the approved voice, the word "sky" in one line, only its position
and punctuation changed:

| position | duration |
|---|---|
| mid-sentence, no punctuation | **0.459s** |
| before a comma | 1.067s |
| ending its own sentence | 0.624s |

The user heard the comma version as "skyy" and flagged it as a glitch in the
voice. It is not a glitch — Kokoro applies phrase-final lengthening, and on an
open diphthong like `skˈaɪ` it stretches into something that sounds broken.
Long vowels are exactly what a melancholic script is full of, so this will
recur.

**The fix is the word's position, not the audio chain.** Kokoro is
deterministic, so re-rendering the same text reproduces the same drag exactly.
Move the word off the boundary: drop the comma, or add a word after it. A
second instance in the same script measured 0.747s before an `and`; changing
"look at the same sky" to "look **up** at the same sky" brought it to 0.520s.

Check any long-vowel word landing before a comma or a full stop:

```python
words = text.split()
ends = align_chunks(_synth_raw(text, voice, mood), words, voice, mood)
```

Anything over ~0.6s on a one-syllable word is the drag. Captions are free to
keep the comma — this only ever concerns the spoken half.

## Punctuation in the spoken half

Tested against measured audio, three finished renders compared by ear, and
**settled: keep writing with plain commas.** Do not re-run this.

Punctuation only affects the `spoken` half of a `(caption, spoken)` pair, so
none of it ever reaches the screen. Longest internal pause, one voice, one
line, only the mark changed:

| mark | pause | vs comma |
|---|---|---|
| nothing | 0.213s | — |
| comma | 0.235s | baseline |
| em dash `—` | 0.256s | +0.02s |
| ellipsis `...` | 0.299s | +0.06s |
| period | 0.341s | +0.11s |

**The ordering is real but the magnitude is not.** Em dashes and ellipses pause
longer than a comma by amounts too small to hear: a full render written with
them came out 10.46s against the comma baseline's 10.55s — *shorter*. They buy
nothing. The user compared all three and chose the plain-comma version.

**The period is the only mark that moves anything**, at 2–3× a comma. It costs
what it buys: a period makes Kokoro treat the clause as a sentence and give it
a terminal falling contour, which is exactly the robotic per-fragment delivery
that `sentences=` exists to avoid. Reach for it only when a line genuinely
needs a full stop.

**`--` is silently dropped.** Only the real `—` survives into the phoneme
string. Nothing warns you; you just get no pause.

**`!` buys a pause, not excitement.** It measured the same as an ellipsis.
Kokoro has no emotion parameter, so intensity comes from the writing, the pace
and the post chain — never from a mark.

**`gap` is the real lever.** At 0.65s between sentences it is roughly double
what any punctuation mark buys, and it is exact rather than inferred. If a line
needs a beat, split it into another sentence entry instead of decorating it.

None of these marks are ever spoken aloud — they stay punctuation in the
phonemes. ALL CAPS and bracketed emotion tags were not tested; keep avoiding
them.

**ALL CAPS is now tested, on a two-letter word, and it fails.** A `chapter`
beat's on-screen card is naturally capitals, and when the same string is also
the spoken half of its sentence, a bare capitalised `IT` phonemizes as the
initialism: `espeak-ng -v en-us -q --ipa "keeps IT honest"` returns
`kˈiːps ˌaɪtˈiː ˈɑːnɪst` — "keeps I.T. honest" — where the lower-case version
returns the correct `ɪɾ`. This shipped audibly on the `perpetual-futures`
short at 0:34 and the user caught it by ear. **A chapter card's `payload` (the
on-screen text) and its narration sentence are two different strings, not
one** — write the sentence chunk as a `(caption, spoken)` pair, caps on
screen, a normal sentence spoken: `(("NO EXPIRY. JUST A FEE THAT KEEPS IT
HONEST.", "No expiry. Just a fee that keeps it honest."),)`. Check every
short all-caps word this way, not just two-letter ones — `IT`, `OR`, `AM` and
`ARE` are all real words with real capitalised siblings that mean something
else to espeak.

## Caption sync

**Use `sentences=`, not `phrases=`, for narrated quotes.** This reversed an
earlier decision, on real output.

Per-phrase synthesis (`phrases=`) gives exact sync by construction, but the
engine sees each fragment with no context, so every chunk lands with a terminal
falling contour and its own pause. The user's verdict on the City 1 cut was
"very robotic, especially the word 'years' and 'ordinary'" — and the finer the
captions, the worse it got, which is backwards. **Caption chunking and delivery
speed must not be the same knob.**

`sentences=` is a list of sentences, each a list of caption chunks. The sentence
is spoken *whole*, so the contour is a real sentence, and the chunk boundaries
are recovered afterwards by DTW-aligning it against throwaway solo renders of
each chunk on log-mel. No aligner model, no Whisper, no download — same engine
and voice on both sides, so the warp absorbs only the prosody that context added.

- **Boundaries land within ~0.19s** of a syllable-count expectation, and where
  they differ the alignment is the more credible one — it gives a pre-comma word
  its real length, which syllable counting cannot know. Chunks show for ~1s, so
  that error is invisible.
- **Trim the padding first.** Kokoro pads each solo render with silence; leaving
  it in shifted a boundary a full word early in testing.
- **Punctuation in the spoken half is the delivery.** Keep the comma on
  "tuesday," and the engine takes the breath. This is now the only way to get a
  pause inside a sentence — `gap` no longer applies there.
- **`gap` is between sentences only.**
- Captions are held until the next one starts, so an inter-sentence gap does not
  play over an empty frame.

`phrases=` is still right when the captions really are separate utterances.

Phrases under three words are merged forward by `split_phrases`; splitting on
every comma produced fragments that flashed past unread ("lost here," measured
0.65s).

**A natural read is much shorter than a chunked one** — the same script went
from 20.4s to 11.1s, because roughly 9s of it had been inter-phrase silence.
That is a real gain, not a shortfall: 10–19s is the channel's strongest bucket.
Do not pad silence to reach a number; write more quote instead.

**Pass `phrases=` for written verse.** `split_phrases` counts words, so a
nine-word line becomes "the things you'll miss are never" / "the things you
planned" — broken in the one place it must not be. Verse already carries its own
line breaks, and those are the right caption *and* speech boundaries.

**Heteronyms are spoken wrong and you will not hear it unless you check.**
espeak phonemizes from spelling, not context: `read` is `/ɹiːd/` in every
sentence, so "i read a quote that said" is delivered in the present tense. A
`phrases` entry may be `(caption, spoken)` — screen keeps `read`, engine gets
`red`. Same trap waits on *lead, live, wind, tear, close, bow, wound, minute*.

Check before rendering rather than after:

```python
_kokoro().tokenizer.phonemize("i read a quote that said", lang="en-us")
```

**`gap` is the honest runtime lever.** Speech length is fixed by the script, and
trimming words to hit a number is the wrong trade. Silence between phrases is
not: at melancholic pace ~1.0s reads as deliberate where the 0.18s default reads
as a list. Hills Monument is 13.4s of speech + 5×1.02s + 1.5s tail = 20.0s.

**The tail is real silence on the audio track**, not just a longer last caption.
The render maps the narration with `-shortest`, so a track shorter than the
reported total silently truncates the video — this shipped once, reporting
20.01s for a file that was 18.51s. Always ffprobe the output and report *that*.

**Keep the tail to 1–2s.** A short loops, and every second after the last word
is a second before it comes back around. `tail=1.2` is the working value; 2.2
was tried and the user cut it for exactly this reason. This is not in tension
with "do not shorten a pause to avoid silence" — that rule is about *dead air*,
and a fast loop is a different reason with a different answer.

**No fade to black.** Removed from `render_short`, `render_narrated` and
`render_narrated_cuts`; the chain now ends `null[vout]`. A fade spends the last
half-second telling the viewer it is over, which is the opposite of what a
looping short wants — the loop point should land on picture.
