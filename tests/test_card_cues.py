"""Chapter cards and reels sound the same in every Short - the quiz too."""

from video_automation.crypto.build import card_cues
from video_automation.crypto.shots import Shot


def _shot(start, hold, **kw):
    sh = Shot(**kw)
    sh.start, sh.hold = start, hold
    return sh


def test_a_chapter_card_gets_riser_hit_keys_and_flashback():
    sh = _shot(5.0, 3.0, graphic="chapter", payload=("How many?", None, "band", 1))
    kinds = [k for _, k in card_cues([sh], 20.0)]
    assert {"chapter_riser", "impact", "title_flashback"} <= set(kinds)
    assert any(k.startswith("key") for k in kinds)


def test_a_reel_pans_between_cards_and_ticks_each_label():
    sh = _shot(2.0, 6.0, graphic="reel", payload=([], ""))
    sh.reveals = [2.0, 4.0, 6.0]
    kinds = [k for _, k in card_cues([sh], 20.0)]
    assert kinds.count("pan") == 2 and kinds.count("reveal") == 3


def test_a_post_arrives_and_highlights():
    sh = _shot(1.0, 4.0, graphic="post", payload=("post", {}, ""))
    sh.reveals = [1.0, 2.5]
    assert sorted(k for _, k in card_cues([sh], 20.0)) == ["pan", "reveal"]
