"""The recorded voice keeps the right take of every sentence.

No Whisper here: the transcript is written by hand, the way Whisper returns
it (digits for numbers, punctuation on the words), with the two things a
real read has - a false start, and a sentence read twice.
"""

from video_automation.core.recorded import align, norm, number_words


def words(text: str, start: float = 0.0, step: float = 0.3):
    out, t = [], start
    for w in text.split():
        out.append({"w": " " + w, "s": round(t, 2), "e": round(t + step * 0.8, 2)})
        t += step
    return out


def test_numbers_read_the_same_either_way():
    assert number_words(587) == "five hundred eighty seven".split()
    assert norm("587 job postings") == norm("five hundred and eighty-seven job postings")
    assert norm("1,816 BTC") == norm("one thousand eight hundred sixteen BTC")
    assert norm("10%") == ["ten", "percent"]


def test_false_start_and_retake_are_cut():
    script = [norm("I let AI read 587 job postings in one week."),
              norm("Only four were worth applying to."),
              norm("The rest were fake, stale, or wanted ten years of experience."),
              norm("It is the pile.")]
    heard = words(
        "I let AI read 500 and... Sorry. "                       # 0-6: false start
        "I let AI read 587 job postings in one week. "           # 7-16
        "Only 4 were worth applying to. "                        # 17-22
        "The rest were fake, old, or asked for 10 years of experience. "  # 23-34: first read
        "Um, let me say that again. "                            # 35-40
        "The rest were fake, stale, or wanted 10 years of experience. "   # 41-51: kept
        "It is the pile.")
    takes = align(script, heard)
    assert [(t.first, t.last) for t in takes] == [(7, 16), (17, 22), (41, 51), (52, 55)]
    assert all(t.score == 1.0 for t in takes)


def test_a_missing_sentence_stops_the_build():
    import pytest
    script = [norm("Only four were worth applying to."),
              norm("This line was never read aloud at all.")]
    with pytest.raises(ValueError, match="never read aloud"):
        align(script, words("Only 4 were worth applying to."))


def test_the_read_aloud_script_says_what_the_build_looks_for():
    """`tools/oktai_script.py` prints spoken halves and the chapter titles."""
    import importlib.util
    from pathlib import Path
    from video_automation.crypto.shots import Shot
    from video_automation.longform import Section
    from video_automation.oktai import reading_order
    spec = importlib.util.spec_from_file_location(
        "oktai_script", Path(__file__).resolve().parents[1] / "tools/oktai_script.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    secs = [Section(title="Why nobody answers", sentences=[
        (("587 postings", "five hundred and eighty seven postings"), "in a week."),
        ("Four were real.",)], shots=[Shot(graphic="stat", payload=("587",)), None])]
    lines = [mod._spoken(s) for s in reading_order(sections=secs)]
    assert lines == ["Why nobody answers",
                     "five hundred and eighty seven postings in a week.",
                     "Four were real."]
    assert mod._face_marks(lines, [("in a week", 3.0)]) == {0, 1, 2}


def test_a_long_scripted_gap_is_silence_even_inside_one_take():
    """A sound example plays in a gap of 1s or more: Oktay's own short pause
    there would put the clip on his next line, so the gap is written."""
    import numpy as np
    from video_automation.core import recorded as rc
    words = [{"s": 0.0, "e": 0.4}, {"s": 0.5, "e": 0.9},     # sentence 1
             {"s": 1.1, "e": 1.5}, {"s": 1.6, "e": 2.0}]     # sentence 2, 0.2s later
    takes = [rc.Take(0, 0, 1, 1.0, {}, 0), rc.Take(1, 2, 3, 1.0, {}, 0)]
    audio = np.zeros(int(2.5 * rc.SR))
    _, joined = rc._bounds(takes, words, audio, [0.5, 0.5], max_pause=0.8)
    assert joined == [False, True]                 # a short gap: his own pause
    _, joined = rc._bounds(takes, words, audio, [6.0, 0.5], max_pause=0.8)
    assert joined == [False, False]                # a long one: room tone, 6s
