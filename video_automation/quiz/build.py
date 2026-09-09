"""Assemble a quiz short: questions in, one MP4 out.

The script is not written as sentences and shots here — it is written as
*questions*, and this module turns each one into the sentences and shots the
engine wants. That is the whole reason the module exists. A quiz written by
hand as a shot list is a list of numbers that all have to agree with each
other: the countdown gap has to match the ring, the ring has to match the
ticks, the verdict has to land on the cut. Written as a `Question`, none of
those is a number anyone types.

Everything downstream — narration, captions, karaoke, the watermark, the
sidechained bed, the encode — is `render_crypto_short`, unchanged, exactly as
the tinnitus article shorts use it. This file adds a beat and its arithmetic
and nothing else.

**A question is seven shots, not one**, and the number is a consequence
rather than a design: every scripted silence needs a sentence boundary to sit
on, and `plan_shots` wants one `Shot` per sentence. So the question, each of
the four cards, and the two halves of the reveal are seven one-chunk
sentences — and therefore seven `Shot`s. All of them are `QuizShot`s built
from the *same* absolute timings (`reveals`, `countdown_at`, `mark_at`), so
the picture is one continuous drawing sliced across six hard cuts rather than
seven different pictures. A cut between two frames computed identically at
the boundary is invisible; that is what makes this cheap.

**Several review rounds shaped the pacing, and more than one overturned the
previous fix's assumption — see `LETTER_WITH_OPTION` for the fullest
account.** In short: `gap` is only ever silence *between sentences*, so a
question carrying its options as caption chunks had nothing separating them;
a scripted gap under `RUN_BREAK_GAP` is not even a guarantee, so every gap
here sits at or above `RUN_BREAK`, which this module lowers to 0.30 through
`render_crypto_short`'s `run_break`; and a card's letter is never split from
its answer at synthesis time — five different ways of doing that were tried
and four were shipped and sent back sounding wrong, so the letter and the
answer are always synthesised together as one utterance. A short pause
between them is still possible, spliced into that same audio afterward
(`synth_option_paused`) where the audio itself shows room for one; the
format-wide pause between cards (`CARD_GAP`) costs nothing either way.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..core.brand import CRYPTO, Brand
from ..core.frame import VERTICAL, Frame
from ..core.voiceover import profile_args, synth_option_paused
from ..crypto.build import _short_factory, render_crypto_short
from ..crypto.shots import Shot
from .cards import LETTERS, QuizShot

# The default wait. Started at eight seconds and came down to six on the
# user's call (2026-09-08) once the format had shipped and the eight-second
# version had actually been watched — still long enough on a phone that the
# viewer either answers or leaves, which is the trade the format is making.
COUNTDOWN = 6.0

# --- pacing, all of it real silence bought from `build_narration_aligned` ---
#
# **These are guaranteed silences, and getting there took two attempts.** The
# first fix split the ask into nine sentences and set gaps of 0.15-0.45 on
# them, on the assumption that a scripted gap is a scripted gap. It is not: a
# gap *below* `RUN_BREAK_GAP` is inserted into the model's own pause by
# `_pad_pause`, which needs a real pause at that boundary to insert into, and
# Kokoro does not leave one after a bare letter. Measured on the shipped
# render: a run that asked for 2.45s of internal gaps got none of it, and the
# options came back exactly as run-together as before.
#
# Nor is there a punctuation trick. "A. It has no effect.", "A... It has no
# effect.", "A, it has no effect." and "Option A." were all synthesised and
# measured: not one leaves a quiet stretch after the letter that clears
# `PAUSE_FLOOR` for `MIN_PAUSE`. The letter is absorbed into the phrase every
# time.
#
# So every gap here is at or above `RUN_BREAK`, which makes each sentence its
# own run and each gap a real silence file in the concat. That is the only
# mechanism in this engine that always happens. The cost is that each item is
# synthesised without the one before it for context — the cold-start prosody
# the run machinery exists to avoid — and for a quiz that is *correct*: four
# lettered options are a list of discrete items, not a paragraph, and reading
# them item by item is what the format wants anyway.
RUN_BREAK = 0.30         # at or above this, a gap is guaranteed rather than hoped for

QUESTION_GAP = 0.65      # after the question, before the first card
CARD_GAP = 0.70          # between one card and the next
ANSWER_LEAD_GAP = 0.40   # after "The correct answer is B.", before the why
NEXT_Q_GAP = 1.00        # after the answer line, before the next question
INTRO_GAP = 1.00         # after the intro card, before the first question
TITLE_GAP = 1.00         # after the series/edition card, before the intro

# **A letter is never spoken apart from its answer, and this is measured
# rather than a preference — five different attempts at separating them were
# built (four of them shipped) and every one sent back sounding wrong, each
# for a different reason.**
#
# *Attempt 1: the letter as its own one-word sentence, read with no context at
# all.* Guarantees a gap through `run_break`, same as every other gap here,
# but changes how the model reads the letter: measured on the pitch track,
# "A." spoken with nothing around it runs flat (127 -> 127 Hz) where the same
# letter *in context* — as the opening of "A. It has no effect." — opens with
# a real rise. Reported back as "weird," "unnatural," "very weird and
# glitchy." A bare one-word utterance also gets the same trailing lengthening
# Kokoro gives the *end* of a real sentence, so the isolated letter runs
# noticeably longer than its natural length in context — the flatness is the
# actual defect, not the length.
#
# *Attempt 2: letter and answer kept as one sentence, split into two chunks,
# with the engine forcing a splice between them after synthesis
# (`chunk_pad`/`_force_pad` in `core/voiceover.py`).* Keeps the natural
# contour — the model still reads the whole sentence as one phrase — but
# requires finding *where* to cut inside continuous, coarticulated audio that
# has no real boundary to find. Not solvable reliably: checked against four
# real cards, no single energy heuristic found the true boundary on all four,
# and `align_chunks`' own DTW estimate, meant to anchor the search, was off by
# -0.06s to +0.14s with no consistent direction. Reported back, again, as
# "weird cut" and "letters sound weird" — some cards were genuinely cut
# mid-word.
#
# *Attempt 3: synthesise the letter in its real answer's context — so the
# model still gives it a real onset — then throw the answer's audio away
# instead of trying to keep or precisely bound it.* Measured clean on every
# check available at the time — no click, no bleed into the next word, a fade
# that survives the compression chain — and still came back "the letters are
# not spoken properly and sound like are cut in the middle." The check that
# was missing: how much of the letter Kokoro actually voices once it can see
# an answer coming. Traced frame-by-frame, "C." in "C. Loud noise is the only
# cause" carries real content for only ~60-90ms before "Loud" begins — the
# cut-finder was landing on a real, correct boundary, not a wrong one; the
# true boundary genuinely sits that early. Kokoro rushes the letter itself
# given somewhere to go; no cut point downstream of that synthesis can
# recover content that was never voiced.
#
# *Attempt 4: isolate the letter again, exactly as Attempt 1 did, but trim it
# far harder.* Shipped once, briefly, and sent back with nearly Attempt 1's
# own words — "weird and unnatural," "lengthened," "glitchy." Trimming only
# ever touches length; the actual defect was always the flat or falling pitch
# a letter gets with nothing to lead into, and no trim setting touches pitch.
#
# *Attempt 5: keep the combined read exactly as it already sounds, and splice
# a short pause into whatever quiet point already exists between letter and
# answer — nothing isolated, nothing discarded.* Applied to every card, this
# fails the same way: the quiet point is not at a consistent acoustic
# distance from the letter across different cards. A slow letter ("A.", "D.")
# leaves a real 100-200ms lull before the answer starts. A fast one ("C.")
# barely leaves any — Kokoro is already rising into the answer within
# 60-90ms of the letter's own peak, the same rushing Attempt 3 measured — and
# a splice forced there lands on the shoulder of the answer's own onset, a
# real waveform discontinuity.
#
# **What shipped is Attempt 5 gated rather than unconditional: the pause is
# only spliced in where the audio itself shows a genuinely quiet moment to
# put it in, and every other card keeps the plain, already-accepted read.**
# `synth_option_paused` (`core/voiceover.py`) measures how quiet the
# candidate splice point is relative to the letter's own peak and refuses to
# use it below a confidence floor — checked against the same twelve real
# option lines the unconditional version was tested on, that gate accepts
# about half of them and rejects the rest, every "C." card among them
# consistently, because the fast-letter problem is systematic to that letter
# rather than occasional. The letter's pronunciation itself is untouched
# either way — `synth_option_paused` synthesises exactly the same text
# `LETTER_WITH_OPTION` always has, and only ever splices *after* that
# synthesis, into audio that already exists.
#
# **What the first four attempts share, and what Attempt 5 avoids by being
# gated rather than unconditional: forcing a silence onto every card is what
# made the earlier attempts trade the letter's own naturalness away to get
# it.** `LETTER_WITH_OPTION`: the letter travels with its answer as one
# spoken utterance (`option_line` below); the format-wide pause still lives
# between cards (`CARD_GAP`), where it always costs nothing; and a per-card
# pause after the letter is added only where measurement says it is safe,
# never at the cost of how the letter itself sounds.
LETTER_WITH_OPTION = True

# `chunk_pad`/`_force_pad` stay in `core/voiceover.py` as general capability
# for a case where the *kept* side of a cut is the one that matters — this
# format does not use them for the letter/answer pause, and should not.

# The countdown ring used to start the instant the model's own audio ended —
# mathematically correct and still read as the video cutting the last option
# off mid-word, because there was no daylight between "the last syllable" and
# "the timer appears". `LEAD` buys that daylight; `TAIL` buys the matching
# beat of stillness *after* the ring's last tick, before the cut to the marked
# cards. Both are added to the requested silence, not carved out of the wait
# itself — the ring itself still runs for exactly `countdown`.
LEAD = 0.25
TAIL = 0.25

# `whoosh` is 0.62s and swells to its peak in the middle. Cued this far ahead
# of a question, it has finished before the voice starts — the transition
# announces the question rather than talking over its first word. It needs the
# gap in front of the question to be at least this long, which is what
# `NEXT_Q_GAP` and `INTRO_GAP` are sized for.
WHOOSH_LEAD = 0.70

# **Very low, and `music_gain` is the wrong knob for it.** `render_bed`
# applies `volume=gain` and then `loudnorm=I=BED_LUFS`, which normalises the
# result straight back and undoes most of the gain. The loudness target is
# what actually moves a bed, so this is passed as `music_lufs`. -32 against
# the default -23 puts the bed roughly a ninth of the power under the voice:
# present under the countdown's silence, which is the whole reason a quiz
# wants one, and not competing with the read.
MUSIC_LUFS = -32

# Silence between the two full-frame cards and the rest.
GAP = 0.40

MARK_LAG = QuizShot.MARK_LAG    # the tick follows the crosses by this long


@dataclass
class Question:
    """One question, as a writer writes it.

    `options` is four answers in the order they are read; `correct` indexes
    the one that is right.

    **`answer` is the *because* only — never "the answer is B".** Naming the
    right option is the format's job, not the writer's: the reveal speaks
    "The correct answer is B." on its own, takes a beat, and then reads this
    line. So write the reason and nothing else ("Quiet rooms remove the sound
    that was covering it."), with no letter on the front — `answer_line`
    puts one there for the card. This is the only place the article's actual
    content lands, and it is what stops a viewer who got it wrong from
    feeling caught out.

    `spoken` overrides how a chunk is said without changing what is shown, for
    Kokoro's spelling — the same `(caption, spoken)` pair the rest of the repo
    uses, keyed by the string it replaces (the question, an option's plain
    text, or the answer — never the lettered form, which this file builds).
    """
    question: str
    options: tuple[str, str, str, str]
    correct: int
    answer: str
    countdown: float = COUNTDOWN
    spoken: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if len(self.options) != 4:
            raise ValueError(f"{self.question!r}: a quiz card grid is four "
                             f"options, got {len(self.options)}")
        if not 0 <= self.correct < 4:
            raise ValueError(f"{self.question!r}: correct={self.correct} "
                             f"indexes nothing")

    def _say(self, text: str, terminate: bool = True
             ) -> "str | tuple[str, str]":
        """The `(caption, spoken)` pair for one chunk.

        **The spoken half gets a full stop the caption does not**, and that is
        not cosmetic. An option is written "It has no effect" because a card
        does not carry a full stop, and the first build handed that string
        straight to the synthesiser — so the last sentence of every run ended
        with no terminal punctuation, Kokoro gave it no sentence-final fall,
        and `librosa.effects.trim` then cut into the word itself. Measured:
        the same run text ends at 0.047 RMS without the stop and 0.006 with
        it, and the audible symptom was the D option's last words missing.
        """
        spoken = self.spoken.get(text, text)
        if terminate and spoken and spoken[-1] not in ".!?…:,":
            spoken += "."
        return text if spoken == text else (text, spoken)

    def option_line(self, i: int) -> "str | tuple[str, str]":
        """One card, letter and answer together, as one spoken utterance.

        The letter is not separable — see `LETTER_WITH_OPTION`. `spoken` is
        keyed by the option as written, so a writer respelling a word does not
        have to know the engine says "B. " in front of it.
        """
        opt = self.options[i]
        said = self.spoken.get(opt, opt)
        if said and said[-1] not in ".!?…:,":
            said += "."
        caption = f"{LETTERS[i]}. {opt}"
        spoken = f"{LETTERS[i]}. {said}"
        return caption if caption == spoken else (caption, spoken)

    def lead_line(self) -> str:
        """"The correct answer is B." — spoken alone, then a beat, then why.

        A full sentence rather than a bare letter, which is what makes it
        safe to synthesise on its own: the complaint that killed the isolated
        letter was a flat one-syllable utterance, and this is a clause with a
        real contour of its own.
        """
        return f"The correct answer is {LETTERS[self.correct]}."

    def answer_line(self) -> str:
        """What the reveal band shows: the letter, then the reason."""
        return f"{LETTERS[self.correct]}. {self.answer}"


def _check_fits(questions: list[Question], frame: Frame, brand: Brand) -> None:
    """Raise on any answer too long for its card, before anything renders.

    `QuizShot` clips an option at three lines. Clipping quietly is the one
    thing a card must not do — the answer would be *wrong on screen* rather
    than merely ugly, and a truncated D option is exactly the kind of fault
    that survives a review because the reviewer already knows what it says.
    Measured with the real font at the real width, so the message names the
    option and the number of lines it actually needs.

    Questions are checked the same way against their own three-line budget.
    """
    from PIL import Image, ImageDraw

    from ..core.draw import wrap

    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    for q in questions:
        shot = QuizShot(list(q.options), question=q.question,
                        correct=q.correct, frame=frame, brand=brand)
        w = shot.card_w - 2 * shot.pad
        for i, opt in enumerate(q.options):
            n = len(wrap(probe, opt, shot.a_font, w))
            if n > 3:
                raise ValueError(
                    f"option {LETTERS[i]} of {q.question!r} needs {n} lines "
                    f"and a card holds 3: {opt!r}. Shorten the answer — an "
                    f"option that long is being read for five seconds and is "
                    f"a script problem, not a layout one.")
        n = len(wrap(probe, q.question, shot.q_font,
                     frame.w - int(160 * shot.k)))
        if n > 3:
            raise ValueError(
                f"question needs {n} lines and the header holds 3: "
                f"{q.question!r}")

        # The answer line is *shown* as well as spoken — it sets in the band
        # the countdown vacates, and that band holds two lines.
        n = len(wrap(probe, q.answer_line(), shot.ans_font,
                     frame.w - int(160 * shot.k)))
        if n > 2:
            raise ValueError(
                f"answer needs {n} lines and the reveal band holds 2: "
                f"{q.answer_line()!r}. It is read over the marked cards in "
                f"about three seconds — if it does not fit, it is too long "
                f"to land.")


@dataclass
class _Group:
    """The seven shots that make up one question.

    One for the question, one per card (letter and answer together), then two
    for the reveal — the spoken "The correct answer is B." and the reason
    after it. Seven because every scripted silence needs a sentence boundary
    to sit on and `plan_shots` wants one `Shot` per sentence.

    Kept as object references rather than looked up again later — by the time
    `plan_graphics` runs, `plan_shots` has already set `.start`/`.hold` on
    every shot in this group, so the group's own timings can be read straight
    off them instead of re-deriving anything from captions.
    """
    q: Question
    question_shot: Shot
    option_shots: list   # 4 Shots, one per card (letter and answer together)
    reveal_lead: Shot    # "The correct answer is B."
    reveal_body: Shot    # the reason


def render_quiz_short(questions: list[Question], outro: tuple,
                      out: Path, workdir: Path,
                      title: "str | tuple[str, str] | None" = None,
                      title_number: "int | None" = None,
                      intro: "tuple | None" = None,
                      voice: str = "otis",
                      brand: Brand = CRYPTO,
                      frame: Frame = VERTICAL,
                      gap: float = GAP,
                      **kw) -> tuple[Path, float]:
    """One quiz short, end to end.

    `title` opens the video — the series card, a full-frame `chapter` beat:
    "Tinnitus Quiz: Myths Edition" and so on. **No number by default, on the
    user's call (2026-09-08).** The format tried a large numeral above the
    title for exactly one video — `title_number`, `ChapterCard`'s own field
    for "a script that is genuinely counting something the narration also
    counts out loud" — before it was dropped; the parameter still works if a
    later run wants it back. Nothing in this format writes the number into
    `title`'s own text either way: Kokoro reads a bare "#1" as "hash one"
    (checked), reason enough on its own never to put a numeral in the caption
    string.

    `intro` is optional and off by default. The first video carried a second
    card between the title and the first question, stating the stake ("Three
    tinnitus myths. Most people believe at least one.") — the user cut it as
    redundant with the title (2026-09-08). Pass it to bring a stake-setting
    card back for a quiz where the title alone does not carry enough context.

    `outro` is required and always renders, unlike `intro`.

    **The outro just asks the question** — "How many did you get?" and stop.
    It used to add "Tell me in the comments", and the user cut it: a quiz that
    has just scored the viewer generates comments on its own, and spelling the
    ask out loud is the one line in the format that sounds like a channel
    asking for engagement rather than a quiz ending.

    `voice` defaults to **`otis`** (bare `am_puck` on the ENERGETIC chain) —
    the male article reader for both channels. An earlier build read the quiz
    in a second, reserved-for-this-format voice, on the reasoning that a
    distinct reader is what stops a quiz sounding like the explainers with a
    gimmick. That reasoning lost to the user's ear: the cut was rejected as
    weird and glitchy (2026-09-07), the alternate profile was retired from the
    roster, and the format has read in `otis` since. Sounding like the channel
    beats sounding distinct from it.

    **The pacing this buys is not free.** Every card and every question
    boundary is a real scripted silence rather than a punctuation mark, and
    each one is paid for in runtime. Three questions run well past the
    original 60s estimate; that is the cost of the breaks actually being
    audible rather than the cost of a mistake. The countdown is the largest
    single item in the budget (three times `countdown`), so it is the first
    thing to trade if a run has to come back down. `_check_fits` still guards
    the part of the budget that was never negotiable — nothing on a card gets
    clipped.

    Every other keyword goes straight through to `render_crypto_short`.
    """
    if not questions:
        raise ValueError("a quiz with no questions is a chapter card")

    _check_fits(questions, frame, brand)

    sentences: list[tuple] = []
    shots: list[Shot] = []
    gaps: list[float] = []
    # A card's letter+answer is synthesised once here rather than left to
    # `build_narration_aligned`'s own pass, so `synth_option_paused` can
    # splice its short pause in where the audio shows room for one — see
    # `LETTER_WITH_OPTION`. Keyed by sentence index, which `precomputed` only
    # ever honours for a sentence alone in its own run — true of every card
    # here, since every gap in this format sits at or above `RUN_BREAK`.
    precomputed: dict[int, object] = {}
    voice_pa = profile_args(voice)

    def add(chunks: tuple) -> None:
        sentences.append(chunks)

    def card(text: "str | tuple[str, str]") -> Shot:
        """A full-frame `chapter` beat — the title, the intro, the outro."""
        display = text if isinstance(text, str) else text[0]
        return Shot(graphic="chapter", payload=(display,))

    if title is not None:
        add((title,))
        display = title if isinstance(title, str) else title[0]
        shots.append(Shot(graphic="chapter", payload=(display, title_number)))
        # Whichever of title/intro is last has to hold the first question's
        # whoosh — `TITLE_GAP` and `INTRO_GAP` are both 1.00s for exactly
        # that reason, not because the two cards need different silences.
        gaps.append(TITLE_GAP)

    if intro is not None:
        add(tuple(intro))
        shots.append(card(" ".join(c if isinstance(c, str) else c[0]
                                   for c in intro)))
        gaps.append(INTRO_GAP)

    if not shots:
        raise ValueError("a quiz needs at least a title or an intro to open "
                         "on — the first question's whoosh has nothing to "
                         "sit inside otherwise")

    groups: list[_Group] = []
    # `whoosh` marks the cut into a new question — including the first, off
    # the intro card. `state[id(shot)]` is how a shot carries its quiz data to
    # `factory`; it is not on `Shot` because `Shot` is the crypto format's
    # dataclass, and adding a dozen quiz-only fields to it for one format is
    # how a shared dataclass turns into a union of every format's needs.
    state: dict[int, dict] = {}

    for q in questions:
        options = list(q.options)

        def quiz_shot() -> Shot:
            sh = Shot(graphic="quiz", payload=(options,))
            # Every internal edge is a cut. The ask and the reveal are the
            # same picture apart from the verdicts, so a cross-dissolve
            # between them plays the mark animation through a fade of
            # itself — the badges arrive at half opacity over a ghost of the
            # unmarked card, which reads as a rendering fault rather than a
            # reveal. Between two ask shots a dissolve would blend two frames
            # that are computed identically at the boundary, which costs a
            # render pass to produce exactly what a cut gives for free.
            sh.xfade = 0.0
            return sh

        question_shot = quiz_shot()
        add((q._say(q.question),))
        shots.append(question_shot)
        gaps.append(QUESTION_GAP)

        option_shots = []
        for i in range(len(q.options)):
            os_ = quiz_shot()
            # Letter and answer in one utterance — the letter is not spoken
            # alone. See `LETTER_WITH_OPTION`. The same text is pre-synthesised
            # here (rather than left to the engine's own pass) so a short
            # pause can be spliced in after the letter where the audio shows
            # room for one — see `synth_option_paused`.
            line = q.option_line(i)
            spoken = line[1] if isinstance(line, tuple) else line
            precomputed[len(sentences)] = synth_option_paused(
                spoken, voice_pa["voice"], voice_pa.get("mood"))
            add((line,))
            shots.append(os_)
            # The last card's gap is what the countdown is built from —
            # `LEAD` seconds of runway past its real speech end, the ring's
            # own `countdown`, then `TAIL` seconds of stillness before the
            # cut to the marked cards.
            gaps.append(CARD_GAP if i < 3 else LEAD + q.countdown + TAIL)
            option_shots.append(os_)

        reveal_lead = quiz_shot()
        add((q.lead_line(),))
        shots.append(reveal_lead)
        gaps.append(ANSWER_LEAD_GAP)

        reveal_body = quiz_shot()
        add((q._say(q.answer),))
        shots.append(reveal_body)
        gaps.append(NEXT_Q_GAP)

        grp = _Group(q, question_shot, option_shots, reveal_lead, reveal_body)
        groups.append(grp)
        for sh in [question_shot, *option_shots, reveal_lead, reveal_body]:
            state[id(sh)] = {"options": options, "question": q.question,
                             "correct": q.correct, "countdown": q.countdown}

    add(tuple(outro))
    shots.append(card(" ".join(c if isinstance(c, str) else c[0]
                               for c in outro)))
    gaps.append(gap)

    quiz_cues: list[tuple[float, str]] = []

    def plan(planned: list[Shot], sents: list, captions: list) -> None:
        """Fill in every group's reveals, ring and verdict, and the sound.

        Runs after `plan_shots`, so every shot in `groups` already carries its
        real `.start`/`.hold` — read straight off the objects rather than
        re-derived from `captions`, which is what the one-sentence-per-card
        design needed and this one does not.
        """
        for grp in groups:
            # A card pops in as its own line starts being read.
            reveals = [os_.start for os_ in grp.option_shots]
            countdown_at = grp.reveal_lead.start - TAIL - grp.q.countdown
            # The verdict lands on the cut into "The correct answer is B." —
            # the marks and the sentence naming the answer arrive together.
            mark_at = grp.reveal_lead.start

            for sh in [grp.question_shot, *grp.option_shots[:-1]]:
                state[id(sh)].update(reveals=reveals)
            # Only the last card carries the countdown: its `.hold` has
            # already been extended (by the engine's own gap-closing pass)
            # all the way to `reveal_lead.start`, so the ring's window fits
            # inside it.
            state[id(grp.option_shots[-1])].update(reveals=reveals,
                                                    countdown_at=countdown_at)
            # Both reveal shots carry the same absolute `mark_at`, so the
            # verdicts stay drawn across the cut between them, and the same
            # band text, so the reason stays on screen while it is read.
            for sh in [grp.reveal_lead, grp.reveal_body]:
                state[id(sh)].update(
                    reveals=[grp.reveal_lead.start - 0.01] * 4,
                    mark_at=mark_at, answer=grp.q.answer_line())

            # Ahead of the question, not on top of it. The cue used to sit
            # on the shot start, which put a 0.62s swell over the first word
            # of the question; `WHOOSH_LEAD` moves it into the silence in
            # front so it has finished by the time the voice arrives.
            quiz_cues.append((max(0.0, grp.question_shot.start - WHOOSH_LEAD),
                              "whoosh"))
            n = int(round(grp.q.countdown))
            for i in range(n):
                t = countdown_at + i
                quiz_cues.append((t, "clock_final" if i == n - 1 else "clock"))
            quiz_cues.append((mark_at, "cross"))
            quiz_cues.append((mark_at + MARK_LAG, "tick"))

    def factory(sh: Shot, fr: Frame):
        st = state.get(id(sh))
        if st is None:
            return _short_factory(sh, fr, brand)
        return QuizShot(st["options"], question=st.get("question", ""),
                        correct=st["correct"], reveals=st.get("reveals"),
                        countdown_at=st.get("countdown_at"),
                        countdown=st["countdown"], mark_at=st.get("mark_at"),
                        answer=st.get("answer"), start=sh.start, hold=sh.hold,
                        frame=fr, brand=brand)

    def cue_list(planned: list[Shot]) -> list[tuple[float, str]]:
        """Every tick, verdict and transition — computed once, in `plan`.

        Not derived by asking each prepared shot for its own cues: a group's
        shots share one `countdown_at` and one `mark_at`, and asking each of
        them would mix the same eight ticks seven times over. `plan` is the
        one place that already knows which shot owns which timing, so it is
        the one source.
        """
        return sorted(quiz_cues)

    kw.setdefault("music_lufs", MUSIC_LUFS)
    return render_crypto_short(
        sentences, shots, out, workdir, voice=voice, frame=frame, brand=brand,
        mark=brand.mark(int(frame.logo_w * brand.mark_scale)),
        gap=gaps, run_break=RUN_BREAK, precomputed=precomputed,
        factory=factory, plan_graphics=plan, cues=cue_list, **kw)
