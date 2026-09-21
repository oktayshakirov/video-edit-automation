"""What do Bitcoin miners have that AI wants? ~42s crypto short.

Source: crypto-wiki/content/posts/why-wall-street-is-betting-big-on-bitcoin-miners-for-ai.mdx
- the same post as the `miners-ai` long-form, written in the same pass.

**The single move.** The long form walks the four assets, the timeline, the
halving, the income comparison, the retrofit gap and the risk. The Short does
the one thing all of that sets up: AI's bottleneck is connected power, a new
build waits years for it, and a mining site already has it. Then it stops, on
a statement card that answers its own opening question - no question at the
end, no disclaimer (the long form carries it).

No company, fund, ticker, price or direction is named.

**Beats:** `bars` (time to power), `grid` (three things on day one), `chapter`
to close. Clips are all from the long form's roster, each used there once.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/miners-ai.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb

SOURCE_POST = "why-wall-street-is-betting-big-on-bitcoin-miners-for-ai"

V = STOCK / "videos"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

PYLONS = V / "high-voltage-power-lines-night/854741.mp4"
PYLON_WIN = V / "electricity-pylon-power-lines-dusk/36669029.mp4"
SUBSTATION = V / "electrical-substation-night/30264077.mp4"
BUILD = V / "construction-site-crane-night/35039490.mp4"
CRANE = V / "construction-site-crane-night/7317317.mp4"
TOWERS = V / "power-plant-cooling-towers-night/4188245.mp4"
TRADE3 = V / "stock-market-screen-dark/38783512.mp4"
TRADE1 = V / "stock-market-screen-dark/37962424.mp4"
CITY = V / "data-center-night-exterior/5744341.mp4"

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
THUMB = BRAND / "graphics/miners-ai-pylons.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question.
    ("What do Bitcoin miners have",
     "that AI companies want?"),
    # The payoff, sentence two.
    ("Power -",
     "megawatts already plugged into the grid."),
    ("Not the chips.",
     "The electricity to run them."),
    # Hinge into the bars, its own sentence.
    ("And a brand-new data center waits a long time to get it.",),
    # The bars' own sentence - one chunk per row.
    ("A new build, two to three years.",
     "A mining site retooled for AI, three to nine months."),
    ("The substation is built.",
     "The permits already exist."),
    # Hinge into the grid.
    ("So a mining site hands AI three things on day one.",),
    # The grid's own sentence - one chunk per card.
    ("Power at scale,",
     "a live grid connection,",
     "and cooling built for hot machines."),
    ("That is why investors started treating mining companies",
     "as AI infrastructure."),
    ("AI can order chips in months.",),
    # Cold close, answering the opening question.
    (("POWER TAKES YEARS. MINERS ALREADY HAVE IT.",
      "Power takes years. Miners already have it."),),
]

SHOTS = [
    Shot(clip=PYLONS, clip_at=1.0),
    Shot(clip=PYLON_WIN, clip_at=5.0),
    Shot(clip=SUBSTATION, clip_at=6.0),
    Shot(clip=BUILD, clip_at=8.0),
    Shot(graphic="bars", backdrop=BEATGROUND,
         payload=([("New data center", 1.00, "24-36 months"),
                   ("Retooled mining site", 0.25, "3-9 months")],
                  "TIME TO POWER")),
    Shot(clip=CRANE, clip_at=12.0),
    Shot(clip=TOWERS, clip_at=10.0),
    Shot(graphic="grid", backdrop=BEATGROUND,
         payload=([("Power at scale", "50 to 500 MW on one site"),
                   ("A live grid connection", "substation already built"),
                   ("Cooling", "built for hot, dense machines")],
                  "DAY ONE")),
    Shot(clip=TRADE1, clip_at=12.0),
    Shot(clip=CITY, clip_at=12.0),
    Shot(graphic="chapter",
         payload=("POWER TAKES YEARS. MINERS ALREADY HAVE IT.",)),
]

GAPS = [0.70, 0.60, 0.55, 0.60, 1.10, 0.60, 0.55, 1.00, 0.60, 0.60, 1.30]


def main() -> None:
    out = Path.home() / "Desktop/crypto-miners-ai-short.mp4"
    work = Path.home() / "Desktop/.crypto-miners-ai-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
        karaoke_box=False, karaoke_upper=False,  # approved before box became default
                                     voice=VOICE, gap=GAPS,
                                     music=MUSIC, music_gain=0.85)
    # Same headline as the long form - a pair shares its thumbnail.
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO,
        "Why AI wants Bitcoin [miners]",
        image=THUMB, accent="yellow", band="top")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
