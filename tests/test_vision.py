"""The vision layer and what it drives: depth parallax, isolation, pop, the
`behind` beat's placement and the thumbnail's subject in front.

**No model is needed here.** `vision.depth` and `vision.matte` are replaced
with maps whose answer is known - the left half near, an ellipse for a
person - so each test checks the behaviour, not the network weights: near
moves more than far, the room dims and the subject does not, the head crosses
the frame's edge. One test runs the real models, and skips without them.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from PIL import Image, ImageDraw

from video_automation.core import vision
from video_automation.core.frame import LANDSCAPE, VERTICAL
from video_automation.crypto.shots import PhotoShot

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def photo(tmp_path):
    """A textured landscape picture, so any warp shows up as a pixel change."""
    rng = np.random.default_rng(7)
    px = rng.integers(40, 215, (900, 1500, 3), dtype=np.uint8)
    px = np.asarray(Image.fromarray(px).resize((1500, 900), Image.NEAREST))
    p = tmp_path / "photo.png"
    Image.fromarray(px).save(p)
    return p


def ellipse(shape, box=(0.38, 0.12, 0.62, 1.15)):
    h, w = shape[:2]
    a = Image.new("L", (w, h), 0)
    ImageDraw.Draw(a).ellipse([w * box[0], h * box[1], w * box[2], h * box[3]],
                              fill=255)
    return np.asarray(a, np.float32) / 255.0


@pytest.fixture
def fake_maps(monkeypatch):
    """Depth: the left half near, the right half far. Matte: an ellipse."""
    def depth(img):
        rgb = vision.as_rgb(img)
        d = np.zeros(rgb.shape[:2], np.float32)
        d[:, : rgb.shape[1] // 2] = 1.0
        return d
    monkeypatch.setattr(vision, "depth", depth)
    monkeypatch.setattr(vision, "matte", lambda img: ellipse(vision.as_rgb(img).shape))


# --- the vision core ----------------------------------------------------------

def test_a_missing_model_says_how_to_fetch_it(monkeypatch, tmp_path):
    monkeypatch.setattr(vision, "MODELS_DIR", tmp_path)
    monkeypatch.setattr(vision, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(vision, "_sessions", {})
    with pytest.raises(vision.MissingModel, match="vision fetch"):
        vision.depth(np.zeros((32, 32, 3), np.uint8))


def test_the_cache_key_is_every_pixel_and_the_model():
    a = np.zeros((8, 8, 3), np.uint8)
    b = a.copy()
    b[3, 3, 1] = 1
    assert vision.cache_key("depth", a) == vision.cache_key("depth", a.copy())
    assert vision.cache_key("depth", a) != vision.cache_key("depth", b)
    assert vision.cache_key("depth", a) != vision.cache_key("matte", a)


def test_a_cached_picture_never_runs_the_model_twice(monkeypatch, tmp_path):
    runs = []

    class Session:
        def get_inputs(self):
            return [type("I", (), {"name": "x"})()]

        def run(self, _, feed):
            runs.append(1)
            return [np.ones((1, 518, 518), np.float32)]

    monkeypatch.setattr(vision, "CACHE", tmp_path)
    monkeypatch.setattr(vision, "_session", lambda name: Session())
    img = np.full((40, 60, 3), 90, np.uint8)
    vision._raw("depth", img)
    vision._raw("depth", img)
    assert len(runs) == 1


def test_a_drawn_matte_is_used_as_given():
    im = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    im.putpixel((5, 5), (255, 255, 255, 255))
    a = vision.alpha_of(im)
    assert a is not None and a[5, 5] == 1.0 and a[0, 0] == 0.0
    assert vision.alpha_of(Image.new("RGB", (4, 4))) is None


# --- PhotoShot ----------------------------------------------------------------

def test_the_default_shot_never_touches_a_model(photo, monkeypatch):
    def boom(_):
        raise AssertionError("a plain still ran a model")
    monkeypatch.setattr(vision, "depth", boom)
    monkeypatch.setattr(vision, "matte", boom)
    ps = PhotoShot(photo, 1.12, (0.0, 0.0), 1.78, frame=LANDSCAPE)
    assert ps._fx is False
    ps.draw(0.5)


def test_parallax_moves_the_near_half_more_than_the_far(photo, fake_maps):
    flat = PhotoShot(photo, 1.12, (0.0, 0.0), 1.78, frame=LANDSCAPE)
    deep = PhotoShot(photo, 1.12, (0.0, 0.0), 1.78, frame=LANDSCAPE, parallax=1.0)
    a = np.asarray(flat.draw(1.0), np.int16)
    b = np.asarray(deep.draw(1.0), np.int16)
    W = LANDSCAPE.w
    # Away from the seam, where the dilated near plane spills over.
    near = np.abs(a[:, : W // 2 - 120] - b[:, : W // 2 - 120]).mean()
    far = np.abs(a[:, W // 2 + 120:] - b[:, W // 2 + 120:]).mean()
    assert near > 2 * far, (near, far)


def test_isolate_dims_the_room_and_leaves_the_subject(photo, fake_maps):
    flat = PhotoShot(photo, 1.12, (0.0, 0.0), 1.78, frame=LANDSCAPE)
    iso = PhotoShot(photo, 1.12, (0.0, 0.0), 1.78, frame=LANDSCAPE, isolate=1.0)
    a = np.asarray(flat.draw(1.0), np.float32)
    b = np.asarray(iso.draw(1.0), np.float32)
    W, H = LANDSCAPE.size
    subject = (slice(int(H * 0.55), int(H * 0.75)), slice(int(W * 0.47), int(W * 0.53)))
    room = (slice(int(H * 0.3), int(H * 0.7)), slice(int(W * 0.05), int(W * 0.2)))
    assert abs(a[subject].mean() - b[subject].mean()) < 3
    assert b[room].mean() < a[room].mean() * 0.7
    # ...and it arrives: nothing at the first frame.
    assert np.abs(np.asarray(iso.draw(0.0), np.float32)
                  - np.asarray(flat.draw(0.0), np.float32)).mean() < 0.5


def test_pop_puts_the_head_over_the_frames_top_edge(photo, fake_maps):
    ps = PhotoShot(photo, 1.06, (0.0, 0.0), 1.15, frame=VERTICAL, pop=True)
    assert ps.pop_cut > 0
    x, y, w, h = ps.photo_box(0.5)
    out = np.asarray(ps.draw(0.5), np.int16)
    plain = PhotoShot(photo, 1.06, (0.0, 0.0), 1.15, frame=VERTICAL, pop=True)
    plain.pop_layer = None                      # the same shot, no head
    base = np.asarray(plain.draw(0.5), np.int16)
    cx = int(x + w / 2)
    above = (slice(int(y) - 40, int(y) - 5), slice(cx - 20, cx + 20))
    side = (slice(int(y) - 40, int(y) - 5), slice(max(5, int(x) + 5), max(40, int(x) + 40)))
    assert np.abs(out[above] - base[above]).mean() > 10      # the head is there
    assert np.abs(out[side] - base[side]).mean() < 1         # the room is not


def test_pop_and_parallax_refuse_to_share_a_shot(photo, fake_maps):
    with pytest.raises(ValueError, match="pop= and parallax="):
        PhotoShot(photo, 1.12, (0.0, 0.0), 1.15, frame=VERTICAL, pop=True,
                  parallax=1.0)


# --- the cover and the beat ------------------------------------------------------

def test_subject_front_puts_the_subject_over_the_type(monkeypatch):
    from video_automation.longform import thumb
    before = Image.new("RGB", (200, 100), (30, 30, 30))
    im = Image.new("RGB", (200, 100), (230, 200, 0))       # "the headline"
    a = np.zeros((100, 200), np.float32)
    a[:, 80:120] = 1.0
    monkeypatch.setattr(vision, "matte", lambda img: a)
    out = np.asarray(thumb.subject_front(im, before))
    assert tuple(out[50, 100]) == (30, 30, 30)     # the subject, in front
    assert tuple(out[50, 20]) == (230, 200, 0)     # the type, elsewhere


def test_behind_never_hides_more_of_the_word_than_it_allows():
    import test_beats
    from video_automation.core.brand import CRYPTO
    from video_automation.longform.beats import BEATS
    b = BEATS["behind"](test_beats.CUTOUT, "ETHEREUM", brand=CRYPTO,
                        frame=LANDSCAPE, start=0.0, hold=4.0, reveals=[0.2])
    assert b.cover <= b.MAX_COVER
    assert b.text_y >= b.head_y - b.size        # never up under the watermark
    # The subject is in front: the middle of the ellipse shows the photo,
    # not the brand gold, wherever the word runs behind it.
    pic = np.asarray(b.draw(1.0), np.int16)
    W = LANDSCAPE.w
    mid = pic[b.text_y + b.size // 2, W // 2]
    assert np.abs(mid - np.array(CRYPTO.primary)).sum() > 120


@pytest.mark.skipif(not (vision.model_path("depth").exists()
                         and vision.model_path("matte").exists()),
                    reason="vision models not installed (`vision fetch`)")
def test_the_real_models_answer_on_a_real_photo():
    img = REPO / "assets/crypto/vitalik-buterin/vitalik-techcrunch-square.jpg"
    rgb = vision.as_rgb(img)
    d, a = vision.depth(rgb), vision.matte(rgb)
    assert d.shape == a.shape == rgb.shape[:2]
    h, w = a.shape
    assert a[h // 2, w // 2] > 0.5         # a portrait: the middle is the person
    assert a[2, 2] < 0.5                   # ...and the corner is not
