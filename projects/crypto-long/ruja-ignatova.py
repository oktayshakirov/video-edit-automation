"""Ruja Ignatova — the coin that was never there. Long-form 16:9 for YouTube.

Source: crypto-wiki/content/crypto-ogs/ruja-ignatova.mdx. Built as a pair with
`crypto-short/ruja-ignatova.py`, which keeps the same core fact — no blockchain,
still four billion dollars, still missing — and does only that one move. What
three minutes buys is the mechanism underneath it: the MLM/Ponzi structure, the
regulator warnings that started in year one, the disappearance, and the
convictions of everyone who did not vanish.

**No financial advice, and this topic does not invite it — it is fraud
mechanics.** The script describes how the con worked and how to check a coin. It
names no price level, predicts nothing, rates no real platform, and recommends
buying or selling nothing. The outro asks one question and stops — no "sources
below", no "subscribe".

**"Ruja" is Bulgarian (Ружа) and is said "ROO-zha", not "ROO-ja".** The spoken
half of every name chunk respells it `Roozha`; the caption keeps `Ruja`. Kokoro
puts the stress of "Ignatova" on the wrong syllable and has no stress control,
so the surname is said in full only where it has to be — mostly it is "Roozha"
or "she".

**The photographs are not the site's.** `crypto-wiki/public/images/crypto-ogs/
ruja-ignatova.jpg` is 441x441, far under the floor the landscape Ken Burns shots
need. Her portraits come from Wikimedia Commons — `assets/crypto/ruja-ignatova/
CREDITS.md`. `ruja-glamour.jpg` is CC BY-SA 2.0, which makes this video a
derivative work, so `Meta.credits` carries the attribution block; `ruja-fbi.jpg`
is a public-domain FBI work. `one-coin.jpeg` is the site's own photo of Ruja at
her OneCoin desk — on message, and used once.

**Every still is used once.** There are only three pictures of her (the glamour
crop is used twice, as a deliberate open/close bookend), so the rest of the
frame is carried by dark screened stock and the drawn beats. Site photos and
`GOLD_DUST` appear at most twice, far apart.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/ruja-ignatova.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"
PH = STOCK / "photos"
RUJA = Path(__file__).resolve().parents[2] / "assets/crypto/ruja-ignatova"

A = 16 / 9

# Her, from Wikimedia Commons. glamour and portrait are two crops of the one
# press photo; fbi is the wanted poster.
P_GLAMOUR = RUJA / "ruja-glamour.jpg"
P_PORTRAIT = RUJA / "ruja-portrait.jpg"
P_FBI = RUJA / "ruja-fbi.jpg"

# Stock, screened at 0.5/3/6/9s — trailing comment is the luma/sat range. The
# first fetch's "screen" clips were live forex charts with a broker name on
# them; these replace them. Every clip is used at most twice, far apart.
CROWD_NIGHT = STOCK / "videos/crowd-cheering-hands-raised-night/26744501.mp4"        # 17s L27-32 S15-22
CROWD_CONCERT = STOCK / "videos/concert-crowd-stage-lights-dark/26745109.mp4"        # 11s L5-12 S14-21
AUDIENCE_SEATED = STOCK / "videos/conference-audience-auditorium-dark/7986776.mp4"   # 17s L10 S3
AUDIENCE_2 = STOCK / "videos/conference-audience-auditorium-dark/7988642.mp4"        # 13s L12 S8
SERVER_DARK = STOCK / "videos/server-room-dark-corridor-blue/7598737.mp4"            # 10s L12 S3
DATACENTER = STOCK / "videos/data-center-servers-rack-dark/3130182.mp4"              # 20s L12-13 S6-7
KEYBOARD = STOCK / "videos/hands-typing-keyboard-dark-close-up/5289120.mp4"          # 20s L6-8 S2-4
ABSTRACT = STOCK / "videos/dark-abstract-digital-particles-network/34127955.mp4"     # 20s L7-10 S1
PLANE_WINDOW = STOCK / "videos/airplane-night-flight-window/19229592.mp4"            # 15s L4-7 S2-5
BOARDING_PASS = STOCK / "videos/passport-boarding-pass-hands-table/3701060.mp4"      # 11s L26-32 S12-16
COURTROOM = STOCK / "videos/courtroom-witness-stand-dark/6101343.mp4"                # 11s L32 S5
RAIN_WINDOW = STOCK / "videos/rain-window-dark-night-moody/6237715.mp4"              # 10s L9 S5
SMOKE = STOCK / "videos/black-smoke-abstract-dark-slow/8386263.mp4"                  # 23s L16 S3

# Dark stock photos, 6000px+ so they bleed off the frame. Each used once, except
# GOLD_DUST (twice, far apart).
SILHOUETTE = PH / "silhouette-businesswoman-walking-dark/39040879.jpg"               # L12 S7
SILHOUETTE2 = PH / "silhouette-businesswoman-walking-dark/12291871.jpg"              # L28 S5
SPEAKER = PH / "conference-keynote-speaker-stage-dark/10401263.jpg"                  # L23 S5
GOLD_DUST = PH / "abstract-particles-gold-black/9665182.jpg"                         # L17 S5

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                   # female, af_heart. Candidate, not approved.

URL = "https://thecrypto.wiki/crypto-ogs/ruja-ignatova"


SECTIONS = [
    # --- the hook, first thirty seconds. No card. --------------------------
    Section(
        title="The coin that was never there",
        card=False,
        sentences=[
            ("In twenty sixteen,",
             "a woman filled Wembley Arena",
             "and told a sold-out crowd",
             "her cryptocurrency would bury Bitcoin."),
            (("Her name was Doctor Ruja Ignatova.",
              "Her name was Doctor Roozha Ignahtova."),
             "The cryptocurrency was called OneCoin."),
            ("Investors put in",
             "more than four billion dollars.",
             "Some estimates run far higher."),
            ("There was one problem with OneCoin.",),
            ("It did not exist.",),
            ("There was no blockchain.",
             "No coins were ever mined.",
             "And that was true",
             "from the very first day."),
            ("Stay to the end",
             "and you will know the one check",
             "that would have caught it in a minute."),
        ],
        shots=[
            # Frame one is a clip: the sold-out crowd, already moving.
            Shot(clip=CROWD_NIGHT, clip_at=1.0),
            Shot(image=P_GLAMOUR, zoom=1.09, pan=(0.02, -0.01), aspect=A, bias=0.25),
            Shot(graphic="stat",
                 payload=("$4B+", "TAKEN IN BY ONECOIN",
                          "Across more than 175 countries.", False),
                 backdrop=POSTS / "one-coin.jpeg"),
            Shot(image=SPEAKER, zoom=1.10, pan=(0.02, 0.01), aspect=A, bias=0.4),
            # the title stamp, on the video's own title line.
            Shot(clip=ABSTRACT, clip_at=2.0,
                 payload=("", "IT DID NOT EXIST")),
            Shot(clip=KEYBOARD, clip_at=2.0,
                 payload=("", "No blockchain. No coins. Not on day one.")),
            Shot(clip=DATACENTER, clip_at=2.0,
                 payload=("", "One check. One minute.")),
        ],
        gaps=[0.45, 0.55, 0.60, 0.85, 1.20, 0.45, 0.80],
    ),

    # --- reframe: why anyone believed it ----------------------------------
    Section(
        title="Why would anyone believe this?",
        sentences=[
            (("Ruja Ignatova was not an obvious con artist.",
              "Roozha Ignahtova was not an obvious con artist."),),
            ("She held a law doctorate",
             "from a German university.",
             "She had studied at Oxford.",
             "She had worked at McKinsey."),
            ("That record did the work",
             "a real product could not."),
            ("And OneCoin did not sell a coin.",
             "It sold education packages,",
             "and a commission",
             "for every friend you brought in."),
            ("Money from new members",
             "paid the members who joined before them."),
            ("That is the definition",
             "of a Ponzi scheme."),
            ("So there were two OneCoins.",),
            # `name_columns=True`: the heading is its own revealed item, so the
            # order on screen is the order in the mouth. One caption chunk per
            # reveal - 2 headings + 3 + 3 = 8.
            ("On the slides,",
             "a coin you could mine,",
             "a price that only rose,",
             "an exchange to cash out.",
             "And here is what was real.",
             "A database they could edit,",
             "a price set in an office,",
             "a system with no way out."),
        ],
        shots=[
            Shot(image=P_PORTRAIT, zoom=1.10, pan=(-0.02, 0.01), aspect=A, bias=0.3),
            Shot(image=POSTS / "law.jpg", zoom=1.11, pan=(0.02, -0.01),
                 aspect=A, bias=0.4),
            None,
            Shot(clip=AUDIENCE_SEATED, clip_at=2.0,
                 payload=("", "Not a coin. A recruiting scheme.")),
            None,
            Shot(image=POSTS / "regulators.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
            None,
            Shot(graphic="compare",
                 payload=("ON THE SLIDES",
                          ["A coin you could mine",
                           "A price that only rose",
                           "An exchange to cash out"],
                          "WHAT WAS REAL",
                          ["A database they could edit",
                           "A price set in an office",
                           "A system with no way out"],
                          True)),
        ],
    ),

    # --- the deep dive. This is the video. -------------------------------
    Section(
        title="So what was OneCoin actually?",
        sentences=[
            ("Strip away the events",
             "and the branding,",
             "and OneCoin was three things."),
            ("A private database of balances.",
             "A website that played a mining animation.",
             "An internal exchange",
             "where withdrawals mostly failed."),
            ("No independent blockchain existed.",),
            ("You could not send a OneCoin",
             "to anyone outside the system.",
             "No real exchange ever listed it."),
            ("When members asked to see the blockchain,",
             "the company stalled,",
             "then said it was being rebuilt."),
            ("For a coin sold to millions",
             "as the next Bitcoin,",
             "that is a remarkable thing to be missing."),
        ],
        shots=[
            Shot(clip=SERVER_DARK, clip_at=1.0,
                 payload=("", "Three things, and none of them a blockchain")),
            None,
            Shot(graphic="quote",
                 payload=("There was no blockchain. There was a spreadsheet.",
                          "what OneCoin actually ran on"),
                 picture=POSTS / "digital-technology.jpg"),
            Shot(image=POSTS / "one-coin.jpeg", zoom=1.12, pan=(0.02, -0.01),
                 aspect=A, bias=0.5),
            None,
            Shot(graphic="stat",
                 payload=("0", "PUBLIC BLOCKCHAINS",
                          "For a coin marketed as the next Bitcoin.")),
        ],
    ),

    # --- the twist: the warnings were early and loud ---------------------
    Section(
        title="The warnings started in year one",
        sentences=[
            ("None of this was hidden.",),
            ("Independent experts",
             "flagged OneCoin in its first year."),
            ("By twenty sixteen,",
             "financial regulators in Britain,",
             "Germany, Italy,",
             "and more than a dozen other countries",
             "had issued public warnings."),
            ("And OneCoin kept growing anyway.",),
            ("Here is how the next few years went.",),
            ("Twenty fourteen, OneCoin launches.",
             "Twenty sixteen, regulators warn worldwide.",
             (("October twenty seventeen, Ruja disappears.",
               "October twenty seventeen, Roozha disappears.")),
             "Twenty nineteen, her brother is arrested.",
             "Twenty twenty-two, the FBI Ten Most Wanted list."),
            ("The warnings were loud.",
             "The money was louder."),
        ],
        shots=[
            Shot(image=POSTS / "regulators.jpg", zoom=1.10, pan=(-0.02, 0.01),
                 aspect=A, bias=0.35),
            Shot(clip=AUDIENCE_2, clip_at=1.0,
                 payload=("", "Flagged in the first year")),
            None,
            Shot(clip=CROWD_CONCERT, clip_at=1.0,
                 payload=("", "Warned, and still growing")),
            None,
            Shot(graphic="steps",
                 payload=(["2014 - OneCoin launches",
                           "2016 - regulators warn, worldwide",
                           "Oct 2017 - Ruja boards a flight, vanishes",
                           "2019 - her brother is arrested",
                           "2022 - added to the FBI Ten Most Wanted"],
                          "HOW IT PLAYED OUT")),
            Shot(image=GOLD_DUST, zoom=1.11, pan=(0.02, 0.01), aspect=A, bias=0.5),
        ],
    ),

    # --- the mirror: the check the hook promised -------------------------
    Section(
        title="What would have caught it?",
        sentences=[
            ("Put yourself in twenty sixteen,",
             "at one of those events."),
            ("You do not have to be an expert",
             "to check a cryptocurrency.",
             "You need four questions."),
            ("Can you inspect the blockchain yourself?",
             "Is it listed somewhere you do not control?",
             "Does the product work without recruiting?",
             "Can you withdraw today, without a reason?"),
            ("For OneCoin, every honest answer",
             "was the same.",
             "No. No. No. No."),
            ("Any one of them,",
             "asked out loud in that arena,",
             "ended the pitch."),
        ],
        shots=[
            Shot(clip=CROWD_NIGHT, clip_at=8.0,
                 payload=("", "You are in the room. What do you ask?")),
            None,
            Shot(graphic="checklist",
                 payload=([("Inspect the blockchain yourself", False),
                           ("Listed somewhere you don't control", False),
                           ("Works without recruiting", False),
                           ("Withdraw today, no reason given", False)],
                          "COULD YOU VERIFY ANY OF IT?",
                          True),                       # flow
                 picture=GOLD_DUST),
            None,
            Shot(image=SILHOUETTE2, zoom=1.11, pan=(0.02, 0.01), aspect=A, bias=0.45),
        ],
        gaps=[0.45, 0.60, 0.34, 1.30, 0.80],
    ),

    # --- aftermath: where she went -------------------------------------
    Section(
        title="Where did she go?",
        sentences=[
            ("On the twenty-fifth of October,",
             "twenty seventeen,",
             (("Ruja Ignatova flew from Sofia to Athens.",
               "Roozha Ignahtova flew from Sofia to Athens.")),),
            ("She has not been seen in public since.",),
            ("In twenty twenty-two she became",
             "the first woman",
             "on the FBI's Ten Most Wanted list."),
            ("The reward for information",
             "reached five million dollars."),
            ("The people around her",
             "did not vanish."),
            ("Karl Sebastian Greenwood, co-founder.",
             "Mark Scott, the lawyer who moved the money.",
             "Gilbert Armenta, who laundered hundreds of millions.",
             "Irina Dilkinska, head of legal."),
            ("Her brother Konstantin",
             "pleaded guilty and testified against her."),
            (("Ruja is still missing.",
              "Roozha is still missing."),),
        ],
        shots=[
            Shot(clip=BOARDING_PASS, clip_at=1.0,
                 payload=("", "Sofia to Athens, 25 October 2017")),
            Shot(clip=PLANE_WINDOW, clip_at=2.0),
            Shot(image=P_FBI, zoom=1.09, pan=(0.02, -0.01), aspect=A, bias=0.35),
            Shot(graphic="stat",
                 payload=("$5M", "REWARD FOR INFORMATION",
                          "US State Department, announced 2024.", False)),
            Shot(image=POSTS / "law.jpg", zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="grid",
                 payload=([("Karl Sebastian Greenwood", "co-founder, 20 years"),
                           ("Mark Scott", "laundered ~$400M, 10 years"),
                           ("Gilbert Armenta", "moved the money, 5 years"),
                           ("Irina Dilkinska", "head of legal, 4 years")],
                          "CONVICTED, WHILE SHE STAYED GONE")),
            # No free photo of Konstantin Ignatov exists (not on Wikimedia
            # Commons; DOJ arrest photo not cleanly PD) - a dark courtroom clip
            # labelled with his name instead.
            Shot(clip=COURTROOM, clip_at=1.0,
                 payload=("", "Konstantin Ignatov - testified against her")),
            Shot(image=SILHOUETTE, zoom=1.11, pan=(-0.02, 0.01), aspect=A, bias=0.3),
        ],
    ),

    # --- echo, and the ask. No "below", no "subscribe". -----------------
    Section(
        title="A scam, or a lesson?",
        spoken_title="So what does OneCoin leave behind?",
        sentences=[
            ("Back to that arena",
             "in twenty sixteen."),
            ("OneCoin worked",
             "because a crowd wanted a coin",
             "that only went up,",
             "and someone with the right résumé",
             "told them she had one."),
            ("The technology was never the point.",
             "The check would have taken a minute."),
            ("Nothing in this video is financial advice.",),
            ("So, what do you think?",),
            ("If you had been in that arena,",
             "would you have asked",
             "to see the blockchain?"),
        ],
        shots=[
            Shot(clip=AUDIENCE_SEATED, clip_at=8.0,
                 payload=("", "Back to the arena")),
            Shot(image=P_GLAMOUR, zoom=1.12, pan=(0.02, 0.01), aspect=A, bias=0.25),
            Shot(graphic="stat",
                 payload=("1 minute", "TO CHECK IT",
                          "Four questions. She failed all four.", False)),
            # Disclaimer on screen whenever the line is spoken - user's rule.
            Shot(clip=RAIN_WINDOW, clip_at=1.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=SMOKE, clip_at=2.0),
            Shot(clip=ABSTRACT, clip_at=10.0),
        ],
        gaps=[0.45, 0.55, 0.85, 0.60, 0.45, 2.40],
    ),
]

META = Meta(
    title="How OneCoin Sold $4 Billion of a Coin That Didn't Exist",
    hook="OneCoin took in over $4 billion with no blockchain and no coins. "
         "Here is how the con worked, and the check that would have caught it.",
    url=URL,
    summary="Ruja Ignatova built OneCoin into one of the largest frauds in "
            "history and then vanished. What OneCoin actually was, why people "
            "believed it, and the four questions that broke the pitch.",
    tags=["ruja ignatova", "onecoin", "cryptoqueen", "crypto scams",
          "ponzi scheme"],
    cta=f"Full profile, quick facts and sources: {URL}",
    credits=["Portrait of Ruja Ignatova (\"Dr. Ruja Ignatova\") by OneCoin "
             "Corporation, CC BY-SA 2.0, via Wikimedia Commons. This video is "
             "shared under CC BY-SA 4.0.",
             "FBI Ten Most Wanted poster image: Federal Bureau of "
             "Investigation, public domain.",
             "Additional footage and photographs: Pexels (Pexels licence, no "
             "attribution required).",
             "Music: night-drift, licensed for this channel.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-ruja-ignatova-long.mp4"
    work = Path.home() / "Desktop/.crypto-ruja-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=music.track("night-drift"),
        callouts=None,
        # Punchy two-liner, sized big by the updated `_headline`. States two
        # true facts that together are the hook; answers nothing.
        thumb_headline="The coin that never [existed]",
        thumb_image=P_GLAMOUR,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
