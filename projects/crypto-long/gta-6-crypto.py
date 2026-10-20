"""What is Dacity Coin? The crypto in GTA 6 - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/grand-theft-auto-crypto.mdx (rewritten for
launch, updated 2026-10-20). GTA 6 launches 19 November 2026.

**The angle.** Five years of "GTA 6 will pay you in Bitcoin" headlines, and a
launch trailer that does show a coin. The video sorts the three things that
get called "GTA 6 crypto": the rumor (one reporter, June 2021, called off by
him in February 2026), the joke (Dacity Coin, a made-up brand in the October
15 trailer) and the money (two real tokens trading on the game's name, one of
them a leaker's pump and dump). This is a named-scheme story as much as a
mechanism, so it runs the crypto doc's "several rejected claims, then the one
that holds" device as a `checklist`, and plants the leak-coin loop before its
exit. The close echoes the open: the Bitcoin was a rumor, the coin is a
joke, the scams are real.

**No financial advice.** Nothing here rates, prices or recommends a token.
The two real tokens are named only as unaffiliated with Rockstar, and their
figures are history with dates, never a direction. No shot shows a chart,
ticker or price; the `chart` beat has no y-axis numbers, by design.

**Figures, all from the article and its sources, each said with its date.**
Henderson's tweet June 2021; "I believe this was scrapped years ago",
February 2026; the roleplay ban November 2022; launch trailer 15 October 2026,
the plane at ~0:55; CYBERLEEK launched 15 August 2026, clips from 18 August,
peak ~$25M market cap on 23 August (CoinDesk, Kotaku), an estimated $250,000+
sold on 27 August hours before Rockstar's showcase, roughly halved within a
day; Take-Two's SDNY subpoenas from 20 August, nobody named as of mid-October;
the Dacity copycat token launched 11 October, ~2,900% in the hour after the
trailer, then about half of it gone. The `chart` series is the leak coin's
shape from those points, not a price history.

**Never pronounced:** nothing needs respelling. "meme coin" is written as two
words because `memecoin` phonemizes MEM-i-coin; "N F Ts" is spelled out
because `NFTs` drops its s.

## The beats

Last three crypto long forms: decentralized-ai (replicate / gauge / compare /
grid / checklist), bear-market-in-crypto (bars / diagram / chart / steps /
stat), bitcoin-halving (steps / bars / diagram / compare / timeline).

* `timeline` - how the rumor actually ran, 2021 to the trailer, spaced by real
  time. Months now place within a year (`Timeline._year`, this run), which is
  what lets February and October 2026 sit apart.
* `quote` - Henderson's six words. Not used in the last three.
* `checklist`, `flow=True` - IS IT IN GTA 6? Three crosses, then the one tick,
  with the voice saying each verdict. The only beat shared with the last
  video, and it is the device the genre asks for.
* `diagram`, `loop=True` - how the leak coin fed itself.
* `chart` - the leak coin's climb, with the creator's sale marked.

**Opener: `Stamp`.** Last three long forms opened hook / Search / Counter.
The topic is a belief to overturn, which is what `Stamp` is for; the verdict
RUMOR judges a claim, not an asset. It lands on "rumor" in sentence 1 (a long
form's hook word may, `longform.md` 2026-10-16).

**Footage: the subject's world, no game footage.** Nothing from the trailers
is used: the game's own pictures are Rockstar's. So the world is drawn from
what the game parodies - Miami at night, palm avenues, sports cars,
aerobatic planes trailing smoke for the stunt plane, a pink street flare -
plus the act of the scam: thumbs on phones, hands at a laptop at night,
banknotes counted. Every clip fresh, verdicts in `footage.md`. The one
abstract is the dark surf under the disclaimer.

**Thumbnail:** the user's pick - Rockstar's own key art of Jason and Lucia -
set right, with the title's question in two rows on the left, clear of both
faces.

**Real references (the user's note on the first cut).** All-stock about a
real game was "boring and monotone", so official GTA VI art and in-game
screenshots from rockstargames.com/VI replace stock under the lines about
the game, the launch trailer's real DacityCoin frame sits under the line
that names it, the GTA VI mark rides in the corner of the remaining stock,
and the two real tokens get drawn ticker cards (their logos cannot be tied
to the right contract).

    PYTHONPATH=. .venv/bin/python projects/crypto-long/gta-6-crypto.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Stamp

SOURCE_POST = "grand-theft-auto-crypto"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Every clip fetched fresh for this pair and looked at on a labelled
# three-frame contact sheet (15/50/85% of its length).
SKYLINE = V / "miami-night-neon/19109600.mp4"                  # 22s, L27, Miami towers at night, a blue-lit crown
AERIAL = V / "miami-night-neon/19109601.mp4"                   # 28s, L38, aerial over lit blocks - SKYLINE's shoot, kept apart
AVENUE = V / "palm-trees-neon-night/40175608.mp4"              # 11s, L40, a palm avenue between towers, purple neon
BEACH = V / "palm-trees-neon-night/4441056.mp4"                # 26s, L33, palms against a dark beach
DRIVE = V / "ocean-drive-miami-night/15270404.mp4"             # 26s, L13, an empty highway at night
EVO = V / "sports-car-night-city/13795978.mp4"                 # 32s, L35, a black sports car, headlights on
WRX = V / "sports-car-night-city/13795917.mp4"                 # 9s,  L46, a car rolling at the camera at night
STUNT = V / "airshow-night/13066176.mp4"                       # 22s, L65, stunt planes trailing smoke - the trailer's plane
FLARE = V / "red-flare-smoke-night/34067500.mp4"               # 12s, L46 S62, a pink flare in the street - the trailer's flare
PAD = V / "playing-video-game-controller-dark/16628557.mp4"    # 14s, L52, hands on a gamepad
COUCH = V / "watching-tv-dark-room/6901290.mp4"                # 33s, L30, two people watching a screen in the dark
RIG = V / "gaming-pc-setup-dark/30470983.mp4"                  # 19s, L37, a gaming PC, red fans
GAMER = V / "gaming-pc-setup-dark/10620285.mp4"                # 12s, L28, a player at a PC at night
PHONE = V / "scrolling-phone-dark/13358555.mp4"                # 15s, L14, a hand on a phone, screen unreadable
THUMB = V / "phone-screen-hands-night/14513394.mp4"            # 10s, L46, a thumb scrolling a phone
FEED = V / "phone-screen-hands-night/28828935.mp4"             # 17s, L21, a phone list in two hands, unreadable
LAPTOP = V / "laptop-screen-dark-room/7272375.mp4"             # 20s, L21, hands at a laptop in the dark
DESK = V / "laptop-screen-dark-room/36392511.mp4"              # 9s,  L35, a figure at a desk of screens
CASH = V / "counting-cash-hands-dark/6266425.mp4"              # 10s, L56, banknotes counted at a desk
SURF = V / "ocean-waves-night/40200251.mp4"                    # 34s, L24, dark surf from above - the one abstract

# Real references (the user's note on the first cut: all-stock about a real
# game is monotone). Official GTA VI art and screenshots from
# rockstargames.com/VI, and the launch trailer's DacityCoin frame as
# published by the press - used for commentary, credited in the description.
PRESS = ROOT / "assets/stock/press/gta6"
LOGO = PRESS / "img/poster_logo.0m-7c805zusl7.png"            # GTA VI lockup, RGBA
KEYART = PRESS / "img/an-extended-look.0ijbsha5fo1te.jpg"      # Jason and Lucia, bandanas - the thumbnail
LAUNCH = PRESS / "img/launch-trailer.0_q-sdrgufc.s.jpg"        # the pair at a red car, palms
VICENIGHT = PRESS / "img/desktop.00.5pzu2sm-z4.jpg"            # Vice City at night from the water, in-game
BEACHCAR = PRESS / "img/desktop.0iky3x6.hl8fo.jpg"             # the pair on a green car, beach, in-game
HIGHWAY = PRESS / "img/o3982oa93a23k4.05jwq4z-sjai_.jpg"       # Vice City traffic, in-game
POOL = PRESS / "img/onlyInLeonidaDesktop.15y2n40f3axwo.jpg"    # "Only in Leonida": a man in a pool float
HEIST = PRESS / "img/mediaDesktop.11iioep6d3wsf.jpg"           # the pair in a vault
COVER = PRESS / "img/poster_full.0az_iud2g3y4j.jpg"            # the cover collage
PLANE = PRESS / "news/sg.png"                                  # the DacityCoin plane, launch trailer ~0:55
BUG = (LOGO, "tr", 0.12)                                       # the corner logo on a stock clip

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/grand-theft-auto-crypto"

# The leak coin's shape, from the dated points in the header: launch, the
# first clip, the climb, the 23 August peak, the slide, the 27 August sale,
# the halving after it, and the long fade into October. A shape, not prices.
LEAK = [0.2, 0.6, 3, 8, 14, 20, 25, 22, 20, 19, 14, 7, 5, 3, 1.5]
SALE = 10

# The two real tokens, drawn rather than logo'd: a dozen copycat contracts
# share each name, so no DEX logo can be trusted to be the right one.
from video_automation.longform.overlay import ticker_card  # noqa: E402
CARDS = ROOT / "assets/stock/press/gta6/cards"
CARD_LEAK = ticker_card("cyberleek", "Leak meme coin, Aug 2026",
                        "not affiliated with Rockstar", CRYPTO,
                        CARDS / "cyberleek.png")
CARD_DACITY = ticker_card("dacity", "Copycat meme coin, Oct 2026",
                          "not affiliated with Rockstar", CRYPTO,
                          CARDS / "dacity.png")


SECTIONS = [
    # --- hook. No card. The Stamp lands on "rumor" in sentence 1. ----------
    Section(
        title="GTA 6 and Bitcoin",
        card=False,
        sentences=[
            ("GTA 6 paying you in Bitcoin was only ever a rumor.",),
            ("And the reporter who started it now believes it was scrapped years ago.",),
            ("But the final trailer does show a coin.",),
            ("It is called Dacity Coin, and Rockstar made it up.",),
            ("Within an hour, people were buying a real token with the same name.",),
            ("Stay to the end,",
             "and you will know which GTA 6 coins are real,",
             "and why none of them are Rockstar's."),
        ],
        shots=[
            Shot(clip=PAD, clip_at=1.0),
            Shot(image=VICENIGHT, zoom=1.10, inset=BUG),
            Shot(image=KEYART, zoom=1.08, pan=(0.02, 0.0)),
            None,
            Shot(clip=THUMB, clip_at=1.0),
            Shot(image=LAUNCH, zoom=1.10, pan=(-0.02, 0.0)),
        ],
        gaps=[0.70, 0.90, 0.55, 0.70, 0.80, 0.90],
    ),

    # --- where the rumor came from ------------------------------------------
    Section(
        title="Where did the Bitcoin rumor come from?",
        spoken_title="So where did the Bitcoin rumor come from?",
        sentences=[
            ("In June 2021, a games reporter named Tom Henderson posted",
             "that some GTA 6 missions would pay in Bitcoin instead of cash."),
            # the timeline's own sentence: one chunk per event.
            ("June 2021, the Bitcoin rumor.",
             "November 2022, Rockstar bans crypto on fan-run servers.",
             "February 2026, the rumor is called off.",
             "And October 2026, a coin in the final trailer."),
            ("Asked about it again in February, Henderson answered in seven words.",),
            # the quote's own sentence.
            ("I believe this was scrapped years ago.",),
            ("No leak, trailer or official reveal since",
             "has shown a mission that pays in crypto."),
        ],
        shots=[
            Shot(clip=PHONE, clip_at=1.0, inset=BUG),
            Shot(graphic="timeline", backdrop=BEATGROUND,
                 payload=([("Jun 2021", "Missions paid in Bitcoin?"),
                           ("Nov 2022", "Rockstar bans crypto on fan servers"),
                           ("Feb 2026", "The rumor is called off"),
                           ("Oct 2026", "A coin in the final trailer")],
                          "GTA 6 AND CRYPTO, SO FAR")),
            Shot(clip=LAPTOP, clip_at=1.0),
            Shot(graphic="quote", backdrop=BEATGROUND,
                 payload=("I believe this was scrapped years ago.",
                          "TOM HENDERSON, FEBRUARY 2026")),
            Shot(image=HIGHWAY, zoom=1.10),
        ],
        gaps=[0.80, 1.30, 0.70, 1.10, 0.90],
    ),

    # --- the coin in the trailer ---------------------------------------------
    Section(
        title="What is Dacity Coin?",
        spoken_title="So what is Dacity Coin?",
        sentences=[
            ("Around fifty-five seconds into the launch trailer,",
             "released on October fifteenth, a stunt plane flies past."),
            ("Painted on its side are two names. DacityCoin, and AudaCity.",),
            ("And someone on its wing lights a pink flare.",),
            ("AudaCity is a made-up brand inside the game,",
             "and Dacity Coin is its made-up coin."),
            ("GTA has always done this. GTA Five mocked Facebook with a fake network called LifeInvader,",
             "and ran fake stock markets instead of real ones."),
            ("So a city full of influencers and fast money",
             "was always going to get a meme coin."),
            ("But can you actually earn one, or buy one?",),
            # the checklist's own sentence: the voice says each verdict.
            ("Missions that pay in Bitcoin, scrapped.",
             "N F T cars and houses, never shown.",
             "An official GTA token, there is none.",
             "A made-up coin, for the story. That one is real."),
        ],
        shots=[
            Shot(clip=STUNT, clip_at=0.5, inset=BUG),
            # The real frame: the lettering sits lower left, so the push
            # travels toward it.
            Shot(image=PLANE, zoom=1.16, pan=(-0.04, 0.03),
                 ),
            Shot(clip=FLARE, clip_at=2.0),
            Shot(image=BEACHCAR, zoom=1.10),
            Shot(clip=AERIAL, clip_at=4.0),
            Shot(image=POOL, zoom=1.08, pan=(0.02, 0.0)),
            Shot(clip=EVO, clip_at=2.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Missions paid in Bitcoin", False),
                           ("NFT cars and houses", False),
                           ("An official GTA token", False),
                           ("A made-up coin, as a joke", True)],
                          "IS IT IN GTA 6?", True)),
        ],
        gaps=[0.55, 0.70, 0.60, 0.70, 0.60, 0.80, 0.90, 1.40],
    ),

    # --- why Rockstar stays away ---------------------------------------------
    Section(
        title="Why would Rockstar avoid real crypto?",
        spoken_title="So why would Rockstar stay away from real crypto?",
        sentences=[
            ("Its only official word on crypto is a ban.",),
            ("In November 2022, Rockstar told fan-run GTA roleplay servers",
             "to stop using crypto and N F Ts."),
            ("That was the year gaming N F Ts collapsed,",
             "and players turned on the publishers who tried them."),
            ("And real coins would wreck the game's economy.",
             "A crash would wipe out your progress. A rally would break the balance."),
            ("And anything worth real money turns a game into a financial product,",
             "with different rules in every country."),
            ("A currency that Rockstar controls itself is simpler,",
             "and in GTA Five's online mode, it has already earned billions."),
        ],
        shots=[
            Shot(clip=GAMER, clip_at=7.0, inset=BUG),
            Shot(clip=RIG, clip_at=2.0),
            Shot(clip=DESK, clip_at=1.0),
            Shot(clip=WRX, clip_at=0.5),
            Shot(clip=SKYLINE, clip_at=12.0),
            Shot(image=HEIST, zoom=1.08),
        ],
        gaps=[0.60, 0.60, 0.70, 0.70, 0.60, 0.90],
    ),

    # --- the twist: the real crypto is outside the game ---------------------
    # The turning point, so the card gets the longer silence.
    Section(
        title="Where is the real crypto?",
        spoken_title="So where is the real crypto around GTA 6?",
        card_gap=1.30,
        sentences=[
            ("Outside the game. And it is a trap.",),
            ("In August 2026, an anonymous leaker going by Cyberleek",
             "began posting stolen GTA 6 clips."),
            ("Every clip carried the name of a meme coin,",
             "and a promise: the higher its price, the more leaks."),
            ("That is a loop, and it feeds itself.",),
            # the diagram's own sentence - one chunk per node.
            ("A new leak goes out.",
             "Fans buy the coin.",
             "And the price climbs, so another leak is promised."),
            ("The coin peaked at about twenty-five million dollars, on August twenty-third.",),
            # the chart's own sentence: the line, then the marked sale.
            ("Then, on August twenty-seventh,",
             "hours before Rockstar's own gameplay reveal, wallets linked to the creator sold."),
            ("An estimated two hundred and fifty thousand dollars, or more.",
             "Within a day, the price had roughly halved."),
            ("And on trailer day, a copycat token called Dacity",
             "jumped about twenty-nine hundred percent in an hour,",
             "then gave back half of it. Neither coin is Rockstar's."),
        ],
        shots=[
            Shot(clip=BEACH, clip_at=2.0),
            # A game still on the leaker's screen side: the clips were the game.
            Shot(clip=LAPTOP, clip_at=9.0, inset=(BEACHCAR, "right", 0.34)),
            Shot(clip=FEED, clip_at=4.0),
            None,
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("A new leak", "posted with the coin's name"),
                           ("Fans buy the coin", "hoping for more"),
                           ("The price climbs", "so another leak is promised")],
                          "HOW THE LEAK COIN FED ITSELF", True)),
            Shot(clip=THUMB, clip_at=3.0,
                 note=("~$25M", "the leak coin at its peak, 23 Aug 2026"),
                 inset=(CARD_LEAK, "right", 0.36)),
            Shot(graphic="chart", backdrop=BEATGROUND,
                 payload=(LEAK, "THE LEAK COIN, DRAWN", SALE,
                          "the creator sells")),
            Shot(clip=CASH, clip_at=1.0,
                 note=("$250K+", "sold hours before the reveal, est.")),
            Shot(clip=COUCH, clip_at=2.0,
                 note=("~2,900%", "a copycat Dacity token, in one hour"),
                 inset=(CARD_DACITY, "right", 0.36)),
        ],
        gaps=[0.85, 0.55, 0.70, 0.55, 1.40, 0.70, 1.40, 0.70, 0.90],
    ),

    # --- close: the echo -----------------------------------------------------
    Section(
        title="Will GTA 6 have crypto?",
        spoken_title="So, will GTA 6 have crypto?",
        sentences=[
            ("A joke one, yes. A real one, no.",),
            ("The Bitcoin was a rumor. The coin is a joke.",
             "The scams are real."),
            ("Nothing in this video is financial advice.",),
            ("So, when a coin with GTA in its name shows up in your feed next month,",
             "would you check who is selling it?"),
        ],
        shots=[
            Shot(image=COVER, zoom=1.08),
            Shot(clip=AVENUE, clip_at=6.0, inset=BUG),
            Shot(clip=SURF, clip_at=4.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=DRIVE, clip_at=12.0),
        ],
        gaps=[0.85, 0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Is Dacity Coin? The Crypto in GTA 6, Explained",
    hook="GTA 6 paying you in Bitcoin was only ever a rumor - but the final "
         "trailer does show a coin. Here is what Dacity Coin is, where the "
         "Bitcoin rumor came from and why it was called off, why Rockstar "
         "stays away from real crypto, and the two real tokens trading on "
         "the game's name before its 19 November 2026 launch.",
    url=URL,
    summary="What crypto is actually in GTA 6, a month before its 19 November "
            "2026 launch: Dacity Coin, a made-up coin from the fictional "
            "AudaCity brand painted on a stunt plane in the 15 October 2026 "
            "launch trailer, in the series' tradition of parody brands like "
            "GTA V's LifeInvader; the June 2021 rumor that missions would pay "
            "in Bitcoin, which the reporter who started it said in February "
            "2026 was scrapped years ago; Rockstar's November 2022 ban on "
            "crypto and NFTs on fan-run roleplay servers; why real crypto "
            "would break a game economy and turn a game into a financial "
            "product; and the real tokens outside the game - the CYBERLEEK "
            "leak meme coin, which peaked near $25 million on 23 August 2026 "
            "before its creator sold an estimated $250,000 or more, and a "
            "copycat Dacity token that jumped about 2,900% in the hour after "
            "the trailer. Neither is connected to Rockstar. Nothing here is "
            "financial advice.",
    tags=["gta 6 crypto", "dacity coin", "dacity coin gta 6",
          "gta 6 bitcoin", "will gta 6 have crypto", "gta 6 trailer coin",
          "audacity gta 6", "gta 6 coin scam", "cyberleek",
          "gta 6 leak coin", "gta 6 nft", "gta 6 explained"],
    cta=f"The full guide to GTA 6 and crypto: {URL}",
    credits=["GTA VI artwork and screenshots: Rockstar Games, used for commentary.",
             "Launch-trailer still via The Sunday Guardian.",
             "Not affiliated with Rockstar Games or Take-Two Interactive.",
             "Nothing in this video is financial advice."],
)

# The title's own question; the plate on CRYPTO.
# Four short rows in a narrow left column (the user's call: one row along
# the bottom, then two wide rows, both took too much of the art).
HEADLINE = "Will\nGTA\u00a06\nhave\n[crypto?]"


def thumbs(out: Path) -> Path:
    """The key art the user picked - Jason and Lucia, bandanas, Leonida at
    dusk - cropped to the pair and set against the right edge, with the
    title's question in four short rows on the black it uncovers at the left. The
    300px ramp blends the art into the black, so no seam shows."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(KEYART).convert("RGB")
    crop = src.crop((int(src.width * 0.15), 0, int(src.width * 0.84),
                     src.height))
    pw = int(720 * crop.width / crop.height)
    crop = crop.resize((pw, 720), Image.LANCZOS)
    im = Image.new("RGB", (1280, 720), (0, 0, 0))
    x = 1280 - pw
    im.paste(crop, (x, 0))
    a = np.zeros((1, 1280), np.float32)
    a[0, :x] = 1.0
    a[0, x:x + 300] = np.linspace(1.0, 0.0, 300)
    mask = Image.fromarray((np.repeat(a, 720, 0) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, mask)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 120, 400, 50, fill, ink, max_lines=4,
                leading=1.02, band="middle", margin=40, shadow=11, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/gta-6-crypto-long.mp4"
    work = Path.home() / "Desktop/.gta-6-crypto-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # A belief to overturn, landing in sentence 1. Last three long forms
        # opened hook / Search / Counter.
        opener=Stamp("GTA 6 pays you in Bitcoin", "RUMOR", at_word="rumor"),
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        # A no-break space keeps "GTA 6" on one row: the first render broke
        # the title as "...in GTA / 6, Explained".
        title=META.title.replace("GTA 6", "GTA\u00a06"),
        title_at=8.5, title_hold=5.4,
    )
    # `render_long`'s own thumbnail is replaced by the hand-built one.
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/gta-6-crypto-long-thumb.jpg"))
    else:
        main()
