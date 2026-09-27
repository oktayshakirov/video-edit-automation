"""Every beat renders, and `item_count` tells the truth about it.

The bug this is really aimed at: `Chart` and `Spectrum` called `partial()`
with `fill=` and `width=`, which that helper does not take. It raised on the
first frame of the first render - after the narration had been synthesised -
and cost a full build to find. A smoke render at three values of `f` catches
that class of mistake in under a second.

The payloads below are deliberately *minimal but real*. A beat that only ever
sees a one-item list will not exercise its wrapping, so each one carries the
shape a script would actually pass.
"""

from __future__ import annotations

import pytest
from PIL import Image
from pathlib import Path

from video_automation.core.brand import CRYPTO, TINNITUS
from video_automation.core.frame import LANDSCAPE, VERTICAL
from video_automation.longform.beats import BEATS, item_count

# One payload per beat, in `BEATS` order. Keep this exhaustive: the coverage
# test below fails when a beat is added without one, which is the point - a
# new beat with no payload here is a new beat with no test.
PAYLOADS = {
    "chapter": ("A dated axis", "timeline"),
    "checklist": ([("An individual holder", True),
                   ("An exchange or custodian", False)], "ARE THEY THEIR OWN?"),
    "stat": ("1.1M", "coins", "never moved"),
    "compare": ("COINS IN", ["Getting ready to sell", "A fund rebalancing"],
                "COINS OUT", ["Going to cold storage", "Nothing at all"], True),
    "quote": ("The chain records the movement, never the reason.", "A trader"),
    # rows are (label, fraction, value_text) - the value is printed, the
    # fraction draws the bar. Read off `bitcoin-price`.
    "bars": ([("2009", 1.0, "50 BTC"), ("2024", 0.0625, "3.125 BTC")],
             "THE HALVING"),
    "grid": ([("Bitcoin", "a whale from 1,000 coins"),
              ("Ethereum", "the line sits near 10,000")], "THE WORD IS RELATIVE"),
    "steps": ([("Install the drivers", None), ("Join a pool", None)], "THE ORDER"),
    "logos": ([("binance", "Binance", True)], "NAMED IN THE SCRIPT"),
    # (value, frac, label, threshold, threshold_label, title) - from
    # `brown-noise-vs-white-noise-for-tinnitus`.
    "gauge": ("BURIED", 0.80, "the ringing is gone", 0.44,
              "partial masking - aim here", "HOW LOUD SHOULD IT BE?"),
    # (bands, value, label, title); a band is (name, upper_frac, colour).
    # `value=None` is the legal "scale with no needle" case, which is why
    # `item_count` branches on it - covered separately below.
    "dial": ([("Extreme fear", 0.25, "#f85032"), ("Neutral", 0.55, "#f2c94c"),
              ("Extreme greed", 1.00, "#56ab2f")], 0.5, "Neutral",
             "A SCORE FROM 0 TO 100"),
    # (photo, items, title). The photo must exist - `Callout` raises rather
    # than drawing an empty frame - so the fixture below supplies a real one.
    "callout": ("<photo>", [("The monitor", 0.72, 0.3),
                            ("The shoulders", 0.3, 0.55)], "WHERE IT STARTS"),
    # (nodes, title, loop); a node is text, or (text, note, icon).
    "diagram": ([("You copy an address", "your friend's wallet", "\U0001F4CB"),
                 ("Malware swaps it", "for the scammer's", "\U0001F9A0")],
                "HOW IT HAPPENS", True),
    "split": ("ONE ADDRESS", "past every threshold",
              "CUSTOMER CLAIMS", "none of its own", "WHOSE COINS?"),
    "timeline": ([("2009", "The first block is mined"),
                  ("2024", "Spot funds list in the US")], "WHY GAPS MATTER"),
    "chart": ([12, 26, 58, 77, 64], "THE SHAPE", 3, "the turn"),
    "map": ([("Switzerland", 0.5, 0.34), ("Singapore", 0.76, 0.62)],
            "WHERE THE RULES ARE"),
    "anatomy": ([("The cochlea", 0.48, 0.52, "r"),
                 ("The hair cells", 0.3, 0.66, "l")], "WHERE SOUND IS MADE"),
    "spectrum": ((3400, 5200), "NOTCHED AUDIO", "cut around your tone", "notch"),
}


def test_every_beat_has_a_payload():
    """A beat added without a test payload fails here rather than silently."""
    assert set(PAYLOADS) == set(BEATS), (
        f"missing: {sorted(set(BEATS) - set(PAYLOADS))}, "
        f"stale: {sorted(set(PAYLOADS) - set(BEATS))}")


# `Callout` is the one beat that needs a file on disk. Any real image will
# do - it is cropped and dimmed - so the brand's own beat ground stands in
# rather than the test writing a temporary PNG.
PHOTO = Path(__file__).resolve().parents[1] / "assets/brand/beat-ground-crypto.jpg"


def _payload(name):
    return tuple(PHOTO if v == "<photo>" else v for v in PAYLOADS[name])


def _build(name, brand, frame):
    n = item_count(name, _payload(name))
    hold = 9.0
    # Reveals spaced the way a real narration would land them, which is what
    # `due`, `span_p` and `marked` all read.
    reveals = [0.9 + i * 1.5 for i in range(n)] or None
    marks = [r + 0.6 for r in reveals] if reveals else None
    return BEATS[name](*_payload(name), brand=brand, frame=frame,
                       reveals=reveals, marks=marks, start=0.0, hold=hold)


@pytest.mark.parametrize("name", sorted(PAYLOADS))
@pytest.mark.parametrize("f", [0.0, 0.5, 1.0])
def test_beat_renders_landscape(name, f):
    """The smoke test. Three values of `f` cover the entrance, the middle and
    the settled state - most timing bugs land in exactly one of them."""
    pic = _build(name, CRYPTO, LANDSCAPE).draw(f)
    assert isinstance(pic, Image.Image)
    assert pic.size == LANDSCAPE.size
    assert pic.mode == "RGB"


@pytest.mark.parametrize("name", sorted(PAYLOADS))
def test_beat_renders_on_both_brands(name):
    """A beat that reads `brand.primary` but hard-codes anything else shows up
    here: tinnitushelp.me's palette is a different shape from thecrypto.wiki's
    (a light accent on plum, not gold on near-black)."""
    assert _build(name, TINNITUS, LANDSCAPE).draw(0.7).size == LANDSCAPE.size


# The portrait layouts are a separate code path in several beats - `steps`
# turns its track ninety degrees, `logos` lays a 2x2 - and that path has no
# coverage at all from the landscape cases above.
PORTRAIT = ["chapter", "checklist", "stat", "quote", "grid", "steps", "logos",
            "timeline", "chart", "map", "spectrum"]


@pytest.mark.parametrize("name", PORTRAIT)
def test_beat_renders_vertical(name):
    assert _build(name, CRYPTO, VERTICAL).draw(0.6).size == VERTICAL.size


@pytest.mark.parametrize("name", sorted(PAYLOADS))
def test_item_count_is_stable(name):
    """`item_count` sizes the `reveals` list `build` hands the beat. If it
    disagrees with what the beat actually reveals, items land on the wrong
    words - silently, because nothing raises."""
    n = item_count(name, _payload(name))
    assert isinstance(n, int) and n >= 0


def test_item_count_rejects_an_unknown_beat():
    with pytest.raises(ValueError, match="unknown beat"):
        item_count("nonesuch", ())


def test_chart_marker_changes_the_reveal_count():
    """The one `item_count` rule with a branch in it: a chart with no marked
    moment is one reveal, not two, and a script that got two would have its
    caption timing shunted a line late."""
    assert item_count("chart", ([1, 2, 3], "t", 1, "n")) == 2
    assert item_count("chart", ([1, 2, 3], "t", None, "")) == 1


# --- the package surface ---------------------------------------------------
#
# `beats` was one 3,124-line module until 2026-09-27. Splitting it into
# families changed no pixel, but it did turn one import site into seven, and
# the way that breaks later is quiet: a beat gets added to a family module and
# never reaches `BEATS`, or a helper stops being re-exported and some caller
# three modules away fails at render time rather than at import.

def test_every_beat_class_is_registered():
    """A class defined in a family module but missing from `BEATS` is a beat
    nobody can reach from a shot list."""
    import importlib
    import inspect

    from video_automation.longform import beats as pkg
    from video_automation.longform.beats.base import Beat

    defined = set()
    for fam in ("column", "wide", "scale", "plot", "annotate"):
        mod = importlib.import_module(f"video_automation.longform.beats.{fam}")
        for obj in vars(mod).values():
            # `obj.__module__` filters out the names each family imports from
            # a sibling's parent - only classes actually defined here count.
            if (inspect.isclass(obj) and issubclass(obj, Beat)
                    and obj is not Beat and obj.__module__ == mod.__name__):
                defined.add(obj)

    missing = defined - set(pkg.BEATS.values())
    assert not missing, ("defined but not in BEATS: "
                         f"{sorted(c.__name__ for c in missing)}")
    # And the other way: a registry entry pointing at nothing real.
    assert set(pkg.BEATS.values()) == defined


@pytest.mark.parametrize("name", [
    # what the rest of the repo imports from here, by name. Each one was a
    # working import before the split and has to stay one.
    "Beat", "BEATS", "item_count", "make_beat", "Checklist",
    "DRAW", "POP", "RISE", "_font", "_display", "_mark_bottom",
    "_round_corners", "_smooth", "_unit", "_hex",
])
def test_the_old_module_surface_is_still_importable(name):
    from video_automation.longform import beats as pkg
    assert hasattr(pkg, name), f"{name} is no longer importable from beats"


def test_no_family_module_imports_another():
    """The families are siblings; shared code goes in `base`. A family
    importing a family is the first step back to one 3,000-line file."""
    from pathlib import Path

    import video_automation.longform.beats as pkg

    fams = ["column", "wide", "scale", "plot", "annotate"]
    root = Path(pkg.__file__).parent
    for fam in fams:
        src = (root / f"{fam}.py").read_text()
        for other in fams:
            if other != fam:
                assert f"from .{other} import" not in src, \
                    f"{fam}.py imports {other}.py - put the shared part in base.py"
