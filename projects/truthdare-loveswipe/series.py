"""What every Love Swipe pick-a-truth Short shares: its title, its outro,
and how it renders. A video script is its rounds and its backdrop.

**Titled "Love Swipe", the app's name, on the user's call (2026-10-27).**
The card shows the name; "pick a truth" and the instruction to pause are
spoken only. The same call asked for a batch of six with a different
background each - the backdrops are `core.backdrop.LOVESWIPE_BACKDROPS` -
uploaded and scheduled by hand on TikTok, so nothing here publishes.
"""

from dataclasses import replace
from pathlib import Path

from video_automation.core.brand import LOVESWIPE
from video_automation.quiz.truthdare import render_truth_dare_short

TITLE = (("Love Swipe", "Love Swipe. Pick a truth, couples edition."),
         ("Grab your partner",
          "Grab your partner, pick one each round, and pause if you need "
          "more time."))

# 870 cards across the app's sixteen decks, counted from the deck files.
OUTRO = ("Which ones did you pick?",
         ("800+ more cards in Love Swipe",
          "Eight hundred more cards in Love Swipe."))


def render(script: str, rounds: list, backdrop: str) -> None:
    """Render one video to the Desktop, named after its script."""
    name = Path(script).stem
    out = Path.home() / f"Desktop/{name}.mp4"
    work = Path.home() / f"Desktop/.{name}-work"
    path, total = render_truth_dare_short(
        rounds, TITLE, OUTRO, out, work,
        brand=replace(LOVESWIPE, backdrop=backdrop))
    print(f"{path}  {total:.1f}s")
