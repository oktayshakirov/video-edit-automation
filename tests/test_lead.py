"""A chapter named inside a sentence (`Section.lead`, `Shot.cue`).

The editor's note on the first recorded OktAI cut (2026-11-23): a chapter
title read on its own, followed by a sentence that says it again, is a
break in the flow. The title comes up on the word instead.
"""

from video_automation.crypto.shots import Shot
from video_automation.longform.plan import Section


def test_the_lead_replaces_the_spoken_title_and_the_card_waits_for_the_word():
    sec = Section(title="The music", lead=("The second mistake", "was the music."),
                  sentences=[("Here's the first track.",)], shots=[Shot(graphic="stat")])
    sents, shots, gaps = sec.parts()
    assert sents[0] == ("The second mistake", "was the music.")
    assert shots[0].graphic == "chapter" and shots[0].cue == 1
    assert gaps[0] == sec.lead_gap


def test_a_lead_shot_replaces_the_card():
    reel = Shot(graphic="reel", payload=([(None, "A")], ""))
    sec = Section(title="The voice", lead=("And the last mistake", "was the voice."),
                  lead_shot=reel, sentences=[("Listen.",)], shots=[Shot(graphic="stat")])
    assert sec.parts()[1][0] is reel


def test_the_cue_is_the_caption_holding_the_title():
    sec = Section(title="The first seconds",
                  lead=("The third mistake", "was in the first seconds", "of a Short."),
                  sentences=[("x",)], shots=[Shot(graphic="stat")])
    assert sec.cue() == 1


def test_without_a_lead_the_title_is_still_spoken():
    sec = Section(title="The tools", sentences=[("x",)], shots=[Shot(graphic="stat")])
    assert sec.parts()[0][0] == (("The tools", "The tools"),)
