"""The things that get uploaded alongside the MP4.

The video is the deliverable everyone looks at; these are the ones that decide
whether anybody finds it. The drone channel shipped thirty Shorts with an empty
description and zero tags, which is the failure this module exists to make
impossible — the build produces the metadata whether or not anyone remembers to
write it.

Three artifacts:

* **An SRT.** YouTube indexes uploaded captions, and ours are exact where its
  automatic ones guess. It costs nothing: `build_narration_aligned` already
  returns the caption spans.
* **A description**, with the post link in the first two lines — the only part
  visible before "…more" — then chapters, then attribution.
* **Chapters**, which YouTube parses out of the description and turns into a
  labelled scrubber. Free structure, and the reason `Section` exists.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# YouTube's rules for chapter parsing. All three are silent failures — get one
# wrong and the timestamps render as plain text with no warning anywhere.
MIN_CHAPTERS = 3
MIN_CHAPTER_LEN = 10.0


def plain_dashes(text: str) -> str:
    """Em and en dashes down to a plain hyphen, for anything sent to YouTube.

    **This is a house rule, not a typographic opinion**, and it was being paid
    for by hand: four of the tinnitus channel's five uploads had their dashes
    converted in the upload form, and the fifth shipped with the em dash still
    in it because somebody blinked. A rule enforced by remembering is a rule
    that holds until the first busy day.

    It applies to the description and the tags — the fields this module writes
    — and deliberately **not** to the SRT, where the dash is ordinary prose the
    voice actually reads, nor to the sidecar's own headings.
    """
    return text.replace("—", "-").replace("–", "-")


def timestamp(t: float, srt: bool = False) -> str:
    """`0:00` / `1:23:45` for a description, `00:00:01,500` for an SRT."""
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    if srt:
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def write_srt(captions, out: Path) -> Path:
    """One cue per caption, in the order they were spoken.

    Cues are clamped so none overlaps the next. A caption is deliberately held
    until the next one starts, which is right on screen and wrong in a subtitle
    file — an overlapping cue makes some players stack two lines.
    """
    lines = []
    for i, c in enumerate(captions, 1):
        if not c.text.strip():
            continue
        end = c.end
        if i < len(captions):
            end = min(end, captions[i].start)
        if end <= c.start:
            continue
        lines += [str(i),
                  f"{timestamp(c.start, srt=True)} --> {timestamp(end, srt=True)}",
                  c.text.strip(), ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def check_chapters(chapters: list[tuple[float, str]], total: float) -> list[str]:
    """Return the reasons YouTube would refuse this chapter list, if any."""
    problems = []
    if not chapters:
        return ["no chapters"]
    if abs(chapters[0][0]) > 0.001:
        problems.append(f"first chapter is at {chapters[0][0]:.2f}s, must be 0:00")
    if len(chapters) < MIN_CHAPTERS:
        problems.append(f"{len(chapters)} chapters, YouTube needs {MIN_CHAPTERS}")
    ends = [t for t, _ in chapters[1:]] + [total]
    for (t, name), end in zip(chapters, ends):
        if end - t < MIN_CHAPTER_LEN:
            problems.append(
                f"chapter {name!r} runs {end - t:.1f}s, minimum is "
                f"{MIN_CHAPTER_LEN:.0f}s")
    return problems


@dataclass
class Meta:
    """Everything the upload form needs, and the sidecar that carries it."""

    title: str
    hook: str                          # the first line, before "…more"
    url: str                           # the post this video came from
    summary: str = ""
    tags: list[str] = field(default_factory=list)
    credits: list[str] = field(default_factory=list)
    cta: str = ""

    def description(self, chapters: list[tuple[float, str]],
                    total: float) -> str:
        """The description, with the link where it is actually visible.

        Two lines are shown before the fold. Spending them on a hook and the
        link is the whole game — a link below three paragraphs of boilerplate is
        a link nobody clicks, which is most of why description traffic is as bad
        as it is.
        """
        parts = [self.hook, "", f"Full article: {self.url}", ""]
        if self.summary:
            parts += [self.summary, ""]
        if chapters:
            parts.append("Chapters")
            for t, name in chapters:
                parts.append(f"{timestamp(t)} {name}")
            parts.append("")
        if self.cta:
            parts += [self.cta, ""]
        if self.credits:
            parts.append("Credits")
            parts += self.credits
            parts.append("")
        if self.tags:
            parts.append(" ".join(f"#{t.replace(' ', '')}" for t in self.tags[:5]))
        return plain_dashes("\n".join(parts).strip()) + "\n"

    def write(self, out: Path, chapters: list[tuple[float, str]],
              total: float, video: Path, srt: Path,
              thumb: Path | None = None) -> Path:
        """A single sidecar to work from while filling in the upload form."""
        problems = check_chapters(chapters, total)
        body = [
            f"# {self.title}", "",
            f"- **Video:** `{video}`",
            f"- **Captions:** `{srt}`",
        ]
        if thumb:
            body.append(f"- **Thumbnail:** `{thumb}`")
        body += [
            f"- **Runtime:** {timestamp(total)} ({total:.2f}s)",
            f"- **Tags:** {', '.join(self.tags)}" if self.tags else "",
            "",
        ]
        if problems:
            body += ["## Chapter problems — YouTube will ignore these silently",
                     ""]
            body += [f"- {p}" for p in problems]
            body.append("")
        body += ["## Description", "", "```", self.description(chapters, total),
                 "```", ""]
        out.write_text("\n".join(x for x in body if x is not None),
                       encoding="utf-8")
        return out
