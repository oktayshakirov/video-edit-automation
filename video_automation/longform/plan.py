"""Sections, and the timeline they lay out.

A short is one argument and needs no structure above the sentence. Three minutes
does, and the structure has to be a real one rather than a decoration: the
sections here become the chapter timestamps in the description, which is the
single cheapest thing this format gets — a viewer can see what is coming, and
YouTube gets a labelled map of the video for free.

**The chapter title is spoken.** The first build left the card in silence and
paid for it with a widened gap, which worked but made every boundary a two-and-
a-half-second hole in the audio — six of them in a two-minute video, which is
most of the reason that cut ran short of its own target. Reading the title costs
the same screen time, fills the hole, and gives the SRT and YouTube's own
transcript the section headings as real text.

So a card is now an ordinary `(sentence, shot)` pair at the head of its section,
not an insertion into a gap. Everything downstream — reveal timing, the callout
rules, the cut-don't-dissolve rule — treats it like any other beat.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..crypto.shots import Shot

CARD_GAP = 1.10         # silence after a spoken title, so the card holds a beat
GAP = 0.34              # the shorts' value: an explainer wants no air


@dataclass
class Section:
    """One chapter: its sentences, the shots that illustrate them, its title.

    `shots` must correspond one-to-one with `sentences`. The chapter card is not
    one of them — `parts` adds it, along with the sentence that speaks it.

    `spoken_title` overrides what the voice says when the on-screen title would
    read badly aloud. Same escape hatch the narration builder's `(caption,
    spoken)` pairs give every other line.
    """
    title: str
    sentences: list
    shots: list[Shot]
    kicker: str = ""
    card: bool = True
    spoken_title: str | None = None
    gaps: list[float] | None = None     # per-sentence override
    gap: float = GAP
    card_gap: float = CARD_GAP

    def __post_init__(self):
        if len(self.shots) != len(self.sentences):
            raise ValueError(
                f"section {self.title!r}: {len(self.shots)} shots for "
                f"{len(self.sentences)} sentences — they must correspond "
                f"(use None to hold the previous shot across a sentence)")
        if self.shots and self.shots[0] is None:
            raise ValueError(
                f"section {self.title!r}: first shot is None — there is no "
                f"previous shot for it to continue")
        if self.gaps is not None and len(self.gaps) != len(self.sentences):
            raise ValueError(
                f"section {self.title!r}: {len(self.gaps)} gaps for "
                f"{len(self.sentences)} sentences")

    def parts(self) -> tuple[list, list[Shot], list[float]]:
        """Sentences, shots and gaps for this section, card included."""
        sents = list(self.sentences)
        shots = list(self.shots)
        gaps = (list(self.gaps) if self.gaps is not None
                else [self.gap] * len(self.sentences))
        if self.card:
            spoken = self.spoken_title or self.title
            # The caption is the title as written; the spoken half may differ.
            sents.insert(0, ((self.title, spoken),))
            shots.insert(0, Shot(graphic="chapter", payload=(self.title,)))
            gaps.insert(0, self.card_gap)
        return sents, shots, gaps


def flatten(sections: list[Section]) -> tuple[list, list[Shot], list[float]]:
    """The flat sentence, shot and gap lists everything downstream works from."""
    sentences: list = []
    shots: list[Shot] = []
    gaps: list[float] = []
    for sec in sections:
        s, sh, g = sec.parts()
        sentences += s
        shots += sh
        gaps += g
    return sentences, shots, gaps


def lay_out(sections: list[Section], shots: list[Shot],
            spans: list[tuple[float, float]], total: float
            ) -> tuple[list[Shot], list[list[int]], list[tuple[float, str]]]:
    """Give every shot its span; compact the holds; list the chapters.

    Returns `(shots, groups, chapters)` where `groups[i]` is the sentence
    indices shot `i` covers, and chapters is `[(seconds, title), ...]`.

    **A `None` in the shots list means "keep the previous shot running".** The
    engine's original rule was one shot per sentence, which at this pace is a
    new scene every four or five seconds — exactly what the reference material
    warns against ("do not generate a brand new scene every 5 seconds"). Holding
    a shot across two or three sentences is what makes an edit feel like it has
    a rhythm rather than a metronome, and it costs nothing but letting the span
    run on.

    The first chapter is forced to 0:00 — YouTube ignores a chapter list whose
    first entry is not, and silently, which is the worst way to find out.
    """
    if len(shots) != len(spans):
        raise ValueError(f"{len(shots)} shots, {len(spans)} spans")

    kept: list[Shot] = []
    groups: list[list[int]] = []
    for i, (sh, (a, b)) in enumerate(zip(shots, spans)):
        if sh is None:
            kept[-1].hold = b - kept[-1].start
            groups[-1].append(i)
            continue
        sh.start, sh.hold = a, b - a
        kept.append(sh)
        groups.append([i])
    shots = kept

    # Close the inter-sentence gaps: a shot's span ends at its last caption, so
    # the silence after it belonged to no shot and the renderer fell through to
    # the next one at f=0.
    for a, b in zip(shots, shots[1:]):
        a.hold = max(a.hold, b.start - a.start)
    shots[-1].hold = max(shots[-1].hold, total - shots[-1].start)

    # **Cut between drawn beats, dissolve between photographs.** Two type layers
    # cross-fading through each other reads as a rendering fault rather than a
    # transition — plainly visible on the first build, where a pull quote
    # dissolved into a checklist and both were legible at once. A chapter card
    # cuts on both sides regardless: it is punctuation, and the hard reset is
    # the whole reason it is worth its screen time.
    for a, b in zip(shots, shots[1:]):
        if a.xfade is None and a.graphic and b.graphic:
            a.xfade = 0.0
        if b.graphic == "chapter" or a.graphic == "chapter":
            a.xfade = 0.0

    # Chapters key off the first *sentence* of each section, then map through
    # `groups` to whichever shot is carrying it — a section's opening sentence
    # may share a held shot with the one before it.
    starts, i = [], 0
    for sec in sections:
        starts.append(i)
        i += len(sec.sentences) + (1 if sec.card else 0)
    chapters = [(spans[s][0], sec.title) for s, sec in zip(starts, sections)]
    chapters[0] = (0.0, chapters[0][1])
    return shots, groups, chapters


def reveal_times(shot: Shot, starts: list[float], count: int) -> None:
    """Fill a beat's `reveals` from the caption starts of its own sentence.

    Even fractions of the shot look synced until you watch it, and then every
    item is a beat early or late. Write the sentence with one caption per item
    and this needs no tuning — the rule the shorts' checklist established.
    """
    if shot.reveals is None:
        shot.reveals = (starts + [starts[-1]] * count)[:count]


SPEAK_LAST = 0.95       # room left for the final item to actually be read
MARK_TAIL = 0.30        # the last verdict is on screen this long before the cut
MARK_STEP = 0.30


def mark_times(last_start: float, end: float, n: int) -> list[float]:
    """When each verdict lands, inside the pause the beat bought itself.

    Anchored on the **start** of the last item's caption, never its end: a
    sentence's final caption is stretched to where the next sentence begins, so
    its end is already the end of the shot. Anchoring there schedules every mark
    past the last frame and draws nothing at all — a bug that is invisible
    unless you look at the frames.
    """
    first = last_start + SPEAK_LAST
    room = (end - MARK_TAIL) - first
    step = MARK_STEP if n < 2 else min(MARK_STEP, max(0.10, room / (n - 1 + 0.7)))
    times = [first + i * step for i in range(n - 1)]
    return times + [(times[-1] if times else first) + step * 1.7]
