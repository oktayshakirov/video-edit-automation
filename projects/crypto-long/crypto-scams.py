"""How to avoid crypto scams - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/how-to-avoid-crypto-scams.mdx.

**The angle.** The article lists nine scam types. The video does not: it
argues that almost every one ends by asking for the same two things - your
seed phrase, or coins sent first - and walks why crypto makes that ask so
costly (no reversal), the four stories it arrives in, phishing, the one
attack that needs no story (clipper malware), and what to do after. The
close is the rule the whole video built.

**No financial advice.** It describes how scams work. It names no platform
as safe or unsafe, no coin and no price.

## The beats

Last three crypto long-forms: satoshi (quote / steps / split / checklist /
stat), rwa (split / diagram / steps / compare / grid), miners-ai (grid /
bars / stat / compare / checklist).

* `compare` - a bank transfer vs a crypto transfer
* `grid` - the four stories
* `quote` - the seed-phrase line from the article
* `diagram` - how a clipper swaps the address
* `checklist` (all ticked) - what to do if it already happened

Clips are hands, phones, keyboards and a baited hook, fetched fresh for this
pair. Nobody is cast as a victim.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/crypto-scams.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "how-to-avoid-crypto-scams"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

SCAMKEYS = V / "hacker-hands-keyboard-dark-hoodie/6964023.mp4"            # 14s, a hand holding keycaps that spell SCAM
HACKER = V / "hacker-hands-keyboard-dark-hoodie/5240933.mp4"              # 18s, hooded figure typing at monitors, from behind
WRITING = V / "hand-writing-on-paper-desk-lamp-night/8631662.mp4"         # 13s, a hand writing under a lamp
ROMANCE = V / "smartphone-text-message-notification-dark-night/6414244.mp4"  # 15s, a phone lighting up with a face on it
CHAT = V / "hands-typing-smartphone-chat-dark/39494892.mp4"               # 26s, a hand typing into a chat
HOODLAP = V / "laptop-login-password-screen-dark/36036810.mp4"            # 12s, a hooded figure at a laptop
CALL = V / "man-on-phone-call-night-dark-worried/7698902.mp4"             # 17s, a woman takes a phone call at night
KEYBOARD = V / "copy-paste-laptop-keyboard-shortcut-dark/36036748.mp4"    # 11s, a lit laptop keyboard
HOOK = V / "fishing-hook-bait-dark-water/6739545.mp4"                     # 21s, a baited hook dropping into dark water
PHONE = V / "phone-vibrating-on-table-dark/6611950.mp4"                   # 23s, two hands on a phone, blank glow
FEED = V / "thumb-scrolling-phone-feed-dark/38410500.mp4"                 # 30s, a thumb scrolling a social feed
TYPING = V / "hands-typing-keyboard-dark-close-up/946146.mp4"           # 38s, two hands typing on a laptop
FRIENDS = V / "man-reading-phone-screen-night-bedroom-dark/7987508.mp4"   # 12s, two people looking at one phone
RAIN = V / "rain-drops-window-glass-night-slow/29992735.mp4"              # 14s, rain on glass, city lights

THUMB = ROOT / "assets/crypto/scams/scam-keycaps.jpg"                     # frame 5s of SCAMKEYS
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/how-to-avoid-crypto-scams"


SECTIONS = [
    # --- hook. No card. ------------------------------------------------------
    Section(
        title="Crypto scams need your help",
        card=False,
        sentences=[
            ("Most crypto scams never break into anything.",),
            ("They need your help - and they ask for it politely.",),
            ("You hand over your seed phrase,",
             "or you send the coins yourself."),
            ("And once a crypto transaction confirms,",
             "nobody can reverse it."),
            ("Stay to the end,",
             "and you will know the four stories scammers use -",
             "and the one rule that beats every one of them."),
        ],
        shots=[
            Shot(clip=SCAMKEYS, clip_at=0.5),
            Shot(clip=CHAT, clip_at=1.0),
            None,
            Shot(clip=PHONE, clip_at=1.0),
            None,
        ],
        gaps=[0.70, 0.90, 0.60, 0.95, 0.85],
    ),

    # --- why crypto ----------------------------------------------------------
    Section(
        title="Why is crypto such an easy target?",
        spoken_title="So why is crypto such an easy target?",
        sentences=[
            ("Because the safety nets you are used to are missing.",),
            # the compare's own sentence - heading, three items, heading, three.
            ("Take a bank transfer.",
             "It can be frozen.",
             "It can be reversed.",
             "And there is a name on the other end.",
             "Now compare that with a crypto transfer.",
             "Nobody can freeze it.",
             "Nobody can reverse it.",
             "And the other end is just an address."),
            ("That is the whole appeal for a scammer.",
             "Get the coins moving once, and they are gone for good."),
        ],
        shots=[
            Shot(clip=TYPING, clip_at=2.0),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("BANK TRANSFER",
                          ["Can be frozen",
                           "Can be reversed",
                           "A name on the end"],
                          "CRYPTO TRANSFER",
                          ["Cannot be frozen",
                           "Cannot be reversed",
                           "Just an address"],
                          True)),
            Shot(clip=ROMANCE, clip_at=5.0),
        ],
        gaps=[0.60, 1.30, 0.90],
    ),

    # --- the four stories ----------------------------------------------------
    Section(
        title="What do crypto scams look like?",
        spoken_title="So what do these scams actually look like?",
        sentences=[
            ("The story changes. The ending does not.",),
            ("There are four you will see again and again.",),
            # the grid's own sentence - one chunk per card.
            ("A support agent who messages you first.",
             "A giveaway that promises to double your coins.",
             "An investment that pays a fixed daily profit.",
             "And a new friend online, with a platform to show you."),
            ("Real support never messages you first,",
             "and never asks for your seed phrase."),
            ("A real giveaway never asks you to send anything.",),
            ("And no honest investment guarantees a daily return.",),
        ],
        shots=[
            Shot(clip=FEED, clip_at=1.0),
            Shot(clip=FRIENDS, clip_at=1.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("Fake support", "messages you first", "🎧"),
                           ("Fake giveaway", "send one, get two back", "🎁"),
                           ("Fake investment", "a guaranteed daily profit", "📈"),
                           ("Fake friend", "a platform to show you", "💬")],
                          "FOUR STORIES, ONE ENDING")),
            Shot(clip=CALL, clip_at=2.0),
            None,
            Shot(clip=KEYBOARD, clip_at=0.5),
        ],
        gaps=[0.70, 0.45, 1.20, 0.60, 0.55, 0.90],
    ),

    # --- phishing ------------------------------------------------------------
    Section(
        title="How does a fake website steal a wallet?",
        spoken_title="So how does a fake website get into your wallet?",
        sentences=[
            ("Phishing works because the copy looks exactly like the original.",),
            ("A sponsored search result, a link in an email,",
             "one letter different in the address."),
            ("You log in, or type your seed phrase to restore a wallet -",
             "and the person behind the copy now has it too."),
            ("So remember this line.",),
            # the quote's own sentence
            ("No real wallet, exchange or support team",
             "will ever ask for your seed phrase."),
            ("Bookmark the sites you use,",
             "and only ever log in from the bookmark."),
        ],
        shots=[
            Shot(clip=HOOK, clip_at=1.0),
            None,
            Shot(clip=HOODLAP, clip_at=0.5),
            None,
            Shot(graphic="quote", backdrop=BEATGROUND,
                 payload=("No legitimate service will ever ask for your seed phrase.",
                          "thecrypto.wiki - how to avoid crypto scams")),
            Shot(clip=TYPING, clip_at=20.0),
        ],
        gaps=[0.60, 0.70, 0.85, 0.45, 1.20, 0.90],
    ),

    # --- the clipper ---------------------------------------------------------
    Section(
        title="Can malware change the address you paste?",
        spoken_title="And can malware change an address after you paste it?",
        sentences=[
            ("Yes - and this one needs no story at all.",),
            ("It is called a clipper, and it hides on your computer.",
             "Here is what it does."),
            # the diagram's own sentence - one chunk per node.
            ("You copy a friend's wallet address.",
             "The clipper swaps it for the scammer's address.",
             "You paste it, and send.",
             "And the coins go to the scammer."),
            ("The fix takes five seconds.",),
            ("After you paste, check the first and last six characters",
             "against the original, before you confirm."),
        ],
        shots=[
            Shot(clip=HACKER, clip_at=1.0),
            None,
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("You copy an address", "your friend's wallet", "📋"),
                           ("Malware swaps it", "for the scammer's", "🦠"),
                           ("You paste and send", "without checking", "📤"),
                           ("The coins are gone", "no way back", "🚫")],
                          "HOW A CLIPPER WORKS")),
            Shot(clip=KEYBOARD, clip_at=3.0),
            None,
        ],
        gaps=[0.70, 0.45, 1.10, 0.55, 0.90],
    ),

    # --- afterwards ----------------------------------------------------------
    Section(
        title="What if it already happened?",
        spoken_title="So what do you do if it has already happened?",
        sentences=[
            ("Stop, and send nothing more.",
             "Then work through this, in order."),
            # the checklist's own sentence - one chunk per row, all ticked.
            ("Move whatever is left to a brand new wallet.",
             "Report the address to the exchange or platform.",
             "File a report with the police, or the FBI's internet crime center.",
             "And ignore anyone offering to recover it for a fee."),
            ("That last one matters most.",
             "A recovery offer is almost always a second scam."),
        ],
        shots=[
            Shot(clip=CALL, clip_at=8.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Move what is left", True),
                           ("Report the address", True),
                           ("Report it to the police", True),
                           ("Ignore recovery offers", True)],
                          "IF IT ALREADY HAPPENED")),
            Shot(clip=HOOK, clip_at=12.0),
        ],
        gaps=[0.60, 2.40, 0.90],
    ),

    # --- the rule, the echo, the ask -----------------------------------------
    Section(
        title="What is the one rule?",
        spoken_title="So what is the one rule that beats all of them?",
        sentences=[
            ("Every story in this video ended the same way.",),
            ("Somebody asked for your seed phrase,",
             "or asked you to send first."),
            ("So if anyone asks for either one,",
             "you already know what it is."),
            ("Nothing in this video is financial advice.",),
            ("A scam needs your help to work.",
             "So the next time a stranger asks for it - would you notice?"),
        ],
        shots=[
            Shot(clip=WRITING, clip_at=1.0),
            None,
            Shot(clip=ROMANCE, clip_at=1.0),
            Shot(clip=RAIN, clip_at=1.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=FRIENDS, clip_at=4.0),
        ],
        gaps=[0.60, 0.85, 1.00, 1.10, 2.30],
    ),
]

META = Meta(
    title="How to Avoid Crypto Scams: The Two Things Every Scam Asks For",
    hook="Most crypto scams never hack anything - they ask you to hand over "
         "your seed phrase or send the coins yourself. Here is why crypto "
         "makes that so costly, the four stories scams arrive in, how "
         "phishing and clipper malware work, and what to do if it already "
         "happened.",
    url=URL,
    summary="How to spot and avoid crypto scams: why a crypto transfer cannot "
            "be frozen or reversed, the four common stories (fake support, "
            "fake giveaways, guaranteed-profit investments and online "
            "friends with a platform), how phishing sites copy a real one, "
            "how clipper malware swaps a pasted wallet address, and the steps "
            "to take after a scam, including why recovery offers are usually "
            "a second scam. Nothing here is financial advice.",
    tags=["crypto scams", "how to avoid crypto scams", "crypto scam",
          "how to spot a crypto scam", "seed phrase scam", "phishing crypto",
          "clipper malware", "crypto giveaway scam", "crypto romance scam",
          "crypto security"],
    cta=f"The full guide to spotting and avoiding crypto scams: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-scams-long.mp4"
    work = Path.home() / "Desktop/.crypto-scams-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        hook="Most crypto scams need [your help]",
        # Two forced rows, centred vertically; the picture slides left so all
        # four keycaps sit clear of the type.
        thumb_headline="How to spot\na [crypto scam]",
        thumb_image=THUMB,
        thumb_accent="yellow",
        thumb_side="right", thumb_crop_at=(0.5, 0.5),
        thumb_crop_band="middle", thumb_shift=0.2,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
