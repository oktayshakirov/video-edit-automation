"""What every Love Swipe pick-a-truth Short shares: its title, its outro,
and how it renders. A video script is its rounds and its backdrop.

**Titled "Love Swipe", the app's name, on the editor's call (2026-10-27).**
The card shows the name; "pick a truth" and the instruction to pause are
spoken only. The same call asked for a batch of six with a different
background each - the backdrops are `core.backdrop.LOVESWIPE_BACKDROPS` -
uploaded and scheduled by hand on TikTok, so nothing here publishes.

**Batch two (07-12, 2026-11-07): a very quick intro, straight to the cards.**
The first batch spoke an ~8s title before a card arrived. Batch two splits
two ways so the numbers can say which wins:

* `"flash"` - the "Love Swipe" card with one spoken line, "Couples, pick
  one.", and a quarter-second gap: the first card lands at ~1.5s.
* `"cold"` - no title at all; the first card lands on frame zero.

It also tries colours: each video has a `LOOKS` entry setting the ground, the
two card neons, the card panel and the header colour together.

**Batch three (13-21, 2026-11-19), built on batch two's TikTok numbers.**
Views barely moved (746-842); likes split:

| # | intro | ground | first card | views | likes |
|---|---|---|---|---|---|
| 07 | cold | ember | who cracks first in an interrogation | 842 | 16 |
| 09 | cold | blush | who's the bigger baby when sick | 789 | 13 |
| 10 | flash | noir | who texts first after an argument | 791 | 12 |
| 11 | cold | grove | who'd win a "who left this here?" case | 761 | 5 |
| 08 | flash | lagoon | your most irrational fear | 749 | 1 |
| 12 | flash | electric | who goes through bathroom drawers | 746 | 1 |

So every batch-three video is a cold open, sits on a warm or dark ground
(three repeats of the winners, six new looks in the same family), and opens
on a judge-your-partner card ("you or your partner", "which of you"). One
video per look, so this is still a small sample: read it as a direction.
"""

from dataclasses import replace
from pathlib import Path

from video_automation.core.brand import LOVESWIPE
from video_automation.quiz.truthdare import CARD_COLORS, render_truth_dare_short

TITLE = (("Love Swipe", "Love Swipe. Pick a truth, couples edition."),
         ("Grab your partner",
          "Grab your partner, pick one each round, and pause if you need "
          "more time."))

FLASH_TITLE = (("Love Swipe", "Couples, pick one."),)
FLASH_GAP = 0.25

# 870 cards across the app's sixteen decks, counted from the deck files.
OUTRO = ("Which ones did you pick?",
         ("800+ more cards in Love Swipe",
          "Eight hundred more cards in Love Swipe."))

# title/outro band, ground, header colour, card panel, (first card neon,
# second card neon). The band is per look because the brand's magenta band
# clashed on the teal and amber grounds in the first test renders.
LOOKS = {
    "ember": dict(band=(176, 62, 22), backdrop="loveswipe-ember", primary=(255, 196, 70),
                  panel=(38, 14, 12),
                  cards=((255, 196, 70), (255, 80, 130))),
    "lagoon": dict(band=(14, 118, 104), backdrop="loveswipe-lagoon", primary=(90, 240, 200),
                   panel=(10, 26, 34),
                   cards=((90, 240, 200), (190, 130, 255))),
    "blush": dict(band=(178, 74, 98), backdrop="loveswipe-blush", primary=(255, 180, 130),
                  panel=(38, 16, 24),
                  cards=((255, 175, 120), (255, 105, 160))),
    # The control: the first batch's own neons on a near-black ground.
    "noir": dict(band=(170, 50, 150), backdrop="loveswipe-noir", primary=(255, 110, 199),
                 panel=(24, 14, 30), cards=CARD_COLORS),
    "grove": dict(band=(36, 108, 46), backdrop="loveswipe-grove", primary=(255, 205, 70),
                  panel=(12, 30, 18),
                  cards=((170, 240, 90), (255, 200, 60))),
    # Batch three (13-21): warm and dark grounds, and the second card always
    # pink or rose - the one thing batch two's three best-liked videos
    # (ember, blush, noir) shared on the cards.
    "wine": dict(band=(150, 30, 70), backdrop="loveswipe-wine",
                 primary=(255, 196, 70), panel=(34, 10, 18),
                 cards=((255, 196, 70), (255, 90, 150))),
    "rosegold": dict(band=(170, 80, 90), backdrop="loveswipe-rosegold",
                     primary=(255, 214, 150), panel=(36, 18, 20),
                     cards=((255, 214, 150), (255, 105, 160))),
    "crimson": dict(band=(180, 30, 40), backdrop="loveswipe-crimson",
                    primary=(255, 225, 190), panel=(34, 8, 12),
                    cards=((80, 210, 255), (255, 90, 170))),
    "velvet": dict(band=(150, 40, 130), backdrop="loveswipe-velvet",
                   primary=(255, 175, 120), panel=(30, 12, 34),
                   cards=((255, 175, 120), (255, 90, 170))),
    "copper": dict(band=(170, 80, 30), backdrop="loveswipe-copper",
                   primary=(255, 200, 120), panel=(34, 16, 10),
                   cards=((255, 230, 180), (255, 100, 150))),
    "noirgold": dict(band=(130, 70, 20), backdrop="loveswipe-noirgold",
                     primary=(255, 196, 70), panel=(22, 16, 12),
                     cards=((255, 196, 70), (255, 90, 170))),
    "electric": dict(band=(58, 70, 200),backdrop="loveswipe-electric", primary=(255, 130, 100),
                     panel=(16, 14, 46),
                     cards=((80, 165, 255), (255, 125, 95))),
}


def _out(script: str) -> tuple[Path, Path]:
    name = Path(script).stem
    return (Path.home() / f"Desktop/{name}.mp4",
            Path.home() / f"Desktop/.{name}-work")


def render(script: str, rounds: list, backdrop: str) -> None:
    """Render one first-batch video to the Desktop, named after its script."""
    out, work = _out(script)
    path, total = render_truth_dare_short(
        rounds, TITLE, OUTRO, out, work,
        brand=replace(LOVESWIPE, backdrop=backdrop))
    print(f"{path}  {total:.1f}s")


def render_look(script: str, rounds: list, look: str, intro: str) -> None:
    """Render one batch-two video: a `LOOKS` entry and a `"flash"` or
    `"cold"` intro."""
    lk = LOOKS[look]
    if intro not in ("flash", "cold"):
        raise ValueError(f"intro is 'flash' or 'cold', not {intro!r}")
    out, work = _out(script)
    path, total = render_truth_dare_short(
        rounds, FLASH_TITLE if intro == "flash" else None, OUTRO, out, work,
        brand=replace(LOVESWIPE, backdrop=lk["backdrop"],
                      primary=lk["primary"], panel=lk["panel"],
                      band=lk["band"]),
        title_gap=FLASH_GAP, card_colors=lk["cards"])
    print(f"{path}  {total:.1f}s")
