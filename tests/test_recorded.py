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
