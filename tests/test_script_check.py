"""`tools/script_check.py` catches what the docs forbid, and nothing it should not.

Each case is a line a script could really carry. The pass cases matter as much
as the flags: a checker that cries wolf on "there is no cure" - the honest
sentence the tinnitus doc asks for - gets ignored, and then it catches
nothing. They were calibrated against every script in `projects/`
(2026-11-05): 330 raw hits, 15 after the negation, history and date rules,
and the 15 are real.

The last test imports every committed project script. An engine change that
renames a `Shot` field or drops a beat breaks an approved script at import,
and nothing else would say so until that video is re-cut.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "script_check", REPO / "tools/script_check.py")
sc = importlib.util.module_from_spec(spec)
sys.modules["script_check"] = sc
spec.loader.exec_module(sc)


def script(channel: str, fmt: str, sentences=(), sections=None, title=None,
           questions=None, **attrs) -> "sc.Script":
    """A Script as `load` would build it, without a file or git."""
    d = f"quiz-{channel}" if fmt == "quiz" else f"{channel}-{fmt}"
    mod = SimpleNamespace(SOURCE_POST="x", DEMAND=None, **attrs)
    if sentences:
        mod.SENTENCES = list(sentences)
    if sections is not None:
        mod.SECTIONS = sections
    if questions is not None:
        mod.QUESTIONS = questions
    s = sc.Script(Path(f"projects/{d}/t.py"), channel, fmt, mod)
    for sec in sections or []:
        if sec.card:
            s.lines.append(sc.Line(f"card {sec.title!r}", sec.title, sec.title))
            s.titles.append((f"chapter {sec.title!r}", sec.title))
        for i, x in enumerate(sec.sentences, 1):
            s.lines.append(sc.as_line(f"s{i}", x))
    for i, x in enumerate(sentences, 1):
        s.lines.append(sc.as_line(f"s{i}", x))
    for qi, q in enumerate(questions or [], 1):
        s.lines.append(sc.Line(f"q{qi} answer", q.answer, q.answer))
    if title:
        s.titles.insert(0, ("Meta.title", title))
    return s


def rules(s) -> list[str]:
    return [f.rule for f in sc.check(s)]


def sec(title, sentences, kicker="", card=True):
    return SimpleNamespace(title=title, sentences=sentences, kicker=kicker,
                           card=card)


# --- the two rules that outrank everything --------------------------------

@pytest.mark.parametrize("line", [
    "You should buy before the next halving.",
    "This coin is going to moon.",
    "Bitcoin will hit $200,000 by next year.",
    "It is the best exchange to start with.",
    "Guaranteed returns, every month.",
])
def test_a_direction_is_flagged_on_crypto(line):
    assert "financial-advice" in rules(script("crypto", "short", [(line,)]))


@pytest.mark.parametrize("line", [
    "Nobody can tell you the best time to buy.",
    "Bitcoin hit sixty-nine thousand dollars in 2021.",
    "A rug pull is sold as guaranteed returns.",
])
def test_a_mechanism_is_not(line):
    assert "financial-advice" not in rules(script("crypto", "long", [(line,)]))


@pytest.mark.parametrize("line", [
    "Sound therapy can help.",
    "This is how you get rid of the ringing.",
    "Magnesium cures it for some people.",
    "Here is how to stop your tinnitus tonight.",
])
def test_a_promise_is_flagged_on_tinnitus(line):
    assert "relief-promise" in rules(script("tinnitus", "short", [(line,)]))


@pytest.mark.parametrize("line", [
    "There is no cure that works for everyone.",
    "Almost every old cure went wrong.",
    "Sound therapy makes it less noticeable.",
    "It is not a fix, and nothing here claims to relieve it.",
])
def test_the_honest_sentence_is_not(line):
    assert "relief-promise" not in rules(script("tinnitus", "long", [(line,)]))


def test_the_crypto_rule_stays_on_its_channel():
    assert "relief-promise" not in rules(script("crypto", "long", [("A cure.",)]))
    assert "financial-advice" not in rules(
        script("tinnitus", "long", [("You should buy earplugs.",)]))


# --- phonemes read the spoken half only ------------------------------------

def test_a_spoken_initialism_is_flagged():
    assert "phoneme" in rules(script("tinnitus", "long", [("Ask about CBT.",)]))


def test_a_respelled_one_is_not():
    s = script("tinnitus", "long", [(("Ask about CBT.", "Ask about talking therapy."),)])
    assert "phoneme" not in rules(s)


def test_ent_inside_a_word_is_not_an_initialism():
    s = script("tinnitus", "long", [("The ENTIRE room went quiet, gently.",)])
    assert "phoneme" not in rules(s)


# --- narration and format rules -------------------------------------------

def test_the_banned_windup():
    s = script("crypto", "long", [("Here is the question almost nobody asks about it.",)])
    assert rules(s).count("windup") == 2


def test_a_long_form_outro_does_not_ask_for_a_subscribe():
    s = script("crypto", "long", [("A line.",), ("If that was useful, subscribe.",)])
    assert "outro-cta" in rules(s)


def test_a_subscribe_mid_script_is_not_the_outro():
    s = script("crypto", "long", [("Subscribe models are a thing.",), ("A.",), ("B?",)])
    assert "outro-cta" not in rules(s)


def test_a_short_never_carries_the_disclaimer():
    s = script("crypto", "short", [("A line.",), ("This is not financial advice.",)])
    assert "short-disclaimer" in rules(s)
    long = script("crypto", "long", [("A line.",), ("This is not financial advice.",)])
    assert "short-disclaimer" not in rules(long)


@pytest.mark.parametrize("title,flagged", [
    ("Does Tinnitus Go Away", True),
    ("What Is Market Cap in Crypto", True),
    ("How Long Does Tinnitus Last", True),
    ("Does Tinnitus Go Away? The Honest Answer", False),
    ("What Is a Seed Phrase? How 12 Words Control Your Crypto", False),
    ("How North Korea Stole $6.36 Billion", False),
    ("How to Manage a Tinnitus Spike", False),
    ("Crypto Exchanges: What Are They", True),
])
def test_a_question_gets_its_mark(title, flagged):
    s = script("tinnitus", "long", [("A.",)], title=title)
    assert ("title-question-mark" in rules(s)) is flagged


def test_every_carded_chapter_needs_a_kicker():
    s = script("crypto", "long", sections=[
        sec("Is it just a password?", [("A.",)], kicker="THE CATCH"),
        sec("How are the words made?", [("B.",)]),
        sec("No card", [("C.",)], card=False),
    ])
    found = [f for f in sc.check(s) if f.rule == "kicker"]
    assert [f.where for f in found] == ["chapter 'How are the words made?'"]


def test_a_quiz_answer_never_names_its_letter():
    q = SimpleNamespace(answer="The answer is B. Quiet rooms remove the cover.")
    assert "answer-letter" in rules(script("tinnitus", "quiz", questions=[q]))
    ok = SimpleNamespace(answer="Quiet rooms remove the sound that covered it.")
    assert "answer-letter" not in rules(script("tinnitus", "quiz", questions=[ok]))


def test_missing_bookkeeping_is_flagged():
    s = script("crypto", "long", [("A.",)])
    del s.mod.SOURCE_POST, s.mod.DEMAND
    s.path = REPO / "tests/test_script_check.py"   # has no /posts/ URL in it
    assert {"source-post", "demand"} <= set(rules(s))


# --- the back catalogue ----------------------------------------------------

SCRIPTS = sorted(p for d in ("crypto-long", "crypto-short", "tinnitus-long",
                             "tinnitus-short", "quiz-crypto", "quiz-tinnitus",
                             "drone-short")
                 for p in (REPO / "projects" / d).glob("*.py"))


class WritesAtImport(Exception):
    pass


@pytest.mark.parametrize("path", SCRIPTS, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_project_script_still_imports(path, monkeypatch):
    """**Importing a script must not write anything.** Three drew their
    ticker cards at module level and saved them into `assets/` - and the
    first version of this test, run under the font shim, overwrote the
    committed `squid.png` with a stand-in face. They draw in `cards()` from
    `main()` now (`workflow.md` step 3), so a save at import is a failure.
    The shim stays off for the import and the save is refused either way:
    this test never writes, even when it fails.
    """
    from PIL import Image
    from video_automation.core import fontshim

    def refuse(self, fp, *a, **k):
        raise WritesAtImport(str(fp))

    fontshim.uninstall()
    monkeypatch.setattr(Image.Image, "save", refuse)
    try:
        sc.load(path)
    except WritesAtImport as e:
        pytest.fail(f"{path.name} saves {e} at import - draw it in a function "
                    f"main() calls (workflow.md step 3)")
    except Exception as e:
        if sc.environmental(e):
            pytest.skip(f"needs the build Mac: {type(e).__name__}: {e}")
        raise
    finally:
        fontshim.install()


def test_a_stand_in_font_never_reaches_a_card(tmp_path, monkeypatch):
    """`ticker_card` refuses to write once this process has drawn with a
    stand-in font - the second guard behind the import rule."""
    from video_automation.core import fontshim
    from video_automation.core.brand import CRYPTO
    from video_automation.longform.overlay import ticker_card
    monkeypatch.setattr(fontshim, "_used", {"/System/Library/Fonts/x.ttf": "dejavu"})
    out = tmp_path / "card.png"
    with pytest.raises(RuntimeError, match="stand-in fonts"):
        ticker_card("squid", "a line", "a sub", CRYPTO, out)
    assert not out.exists()
