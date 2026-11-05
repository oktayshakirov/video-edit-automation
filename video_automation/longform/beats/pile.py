"""`pile` - coins pour into a container and settle; the floor can open.

Drawn bars say how much. This says it the way a viewer feels it: a batch of
coins falls in on every reveal, bounces and stacks the way real ones do, and
a pile that is visibly bigger is a number nobody has to read. With `drain`,
the floor opens on the last reveal and the pile pours out - a rug pull, a
hack, a liquidation, money leaving.

**The physics runs once, at build time, with a fixed seed** (`pymunk`, MIT).
Every coin's position is recorded at 120Hz for the whole beat; `draw(f)` only
looks it up. So a re-render is the same frame for frame, a preview matches
the render, and the frame rate cannot change the motion.

payload: (drops, title="", drain="") where drops is
[(count, label) | (count, label, glyph), ...] - one batch per reveal - and
`drain`, if set, is the label for the floor opening (one more reveal).
"""

from __future__ import annotations

import math
import random

import numpy as np
from PIL import Image, ImageDraw

from .base import Beat, _display, _font, _smooth

RATE = 120                  # recorded samples a second
SUBSTEPS = 2                # physics steps per sample


class Pile(Beat):
    """payload: (drops, title="", drain="")."""

    POUR = 0.9              # seconds one batch takes to pour in
    LABEL_IN = 0.30
    OPEN = 0.55             # the trapdoors swinging down, on a drain

    def __init__(self, drops, title="", drain="", **kw):
        super().__init__(**kw)
        self.drops = [tuple(d) for d in drops]
        self.title, self.drain = title, drain
        W, H = self.frame.size
        p = self.portrait
        self.cw = W * (0.62 if p else 0.30)
        self.ch = H * (0.36 if p else 0.50)
        self.cx = W / 2
        self.bottom = H * (0.80 if p else 0.88)
        self.top = self.bottom - self.ch
        total = sum(int(d[0]) for d in self.drops)
        # As big as the container allows for this many coins, never bigger
        # than a ninth of its width.
        fill = self.cw * self.ch * 0.50 / (math.pi * max(total, 1))
        self.r = max(6.0, min(self.cw / 18, math.sqrt(fill)))
        self.wall = max(4, int(W * 0.004))
        self.times = self._times()
        self._simulate(total)
        self._sprites()

    # --- timing -----------------------------------------------------------

    def _times(self):
        n = len(self.drops) + (1 if self.drain else 0)
        rv = list(self.reveals or [])
        return [(rv[i] if i < len(rv) else
                 self.start + self.hold * (0.08 + 0.75 * i / max(n, 1)))
                - self.start for i in range(n)]

    # --- physics ----------------------------------------------------------

    def _simulate(self, total):
        import pymunk

        W, H = self.frame.size
        space = pymunk.Space()
        space.gravity = (0, H * 2.4)            # y down, like the frame
        space.iterations = 24
        space.damping = 0.92
        x0, x1 = self.cx - self.cw / 2, self.cx + self.cw / 2
        seg = self.wall / 2
        walls = [pymunk.Segment(space.static_body, (x0, self.top - self.r * 2),
                                (x0, self.bottom), seg),
                 pymunk.Segment(space.static_body, (x1, self.top - self.r * 2),
                                (x1, self.bottom), seg)]
        # The floor is two trapdoors hinged at the walls. Kinematic, so on a
        # drain they swing down and *push* the pile out through a widening
        # gap - a floor that simply vanished emptied the container in half a
        # second, too fast to see (the first demo).
        flaps = []
        for hinge, sign in ((x0, 1.0), (x1, -1.0)):
            b = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            b.position = (hinge, self.bottom)
            sg = pymunk.Segment(b, (0, 0), (sign * self.cw / 2, 0), seg)
            sg.elasticity, sg.friction = 0.2, 0.8
            space.add(b, sg)
            flaps.append((b, sign))
        for s in walls:
            s.elasticity, s.friction = 0.2, 0.8
        space.add(*walls)

        rng = random.Random(1729)
        # Coins drop in lanes, and never in the lane the last one used: two
        # spawned overlapping are pushed apart by the solver hard enough to
        # leave the container (a test with every coin due at once flung one
        # off the frame). Times are clamped to the beat for the same reason.
        lane_w = self.r * 2.3
        lanes = max(2, int(self.cw * 0.80 / lane_w))
        left = self.cx - lanes * lane_w / 2
        order, lane = [], -1
        spawns = []                              # (time, x, y, spin)
        for (count, *_), t0 in zip(self.drops, self.times):
            count = int(count)
            dur = min(self.POUR, 0.25 + 0.025 * count)
            for k in range(count):
                if not order:
                    order = list(range(lanes))
                    rng.shuffle(order)
                    if order[0] == lane:
                        order.append(order.pop(0))
                lane = order.pop(0)
                spawns.append((max(0.0, t0) + dur * k / max(count, 1),
                               left + (lane + 0.5 + rng.uniform(-0.15, 0.15)) * lane_w,
                               -self.r * 1.6, rng.uniform(-6, 6)))
        spawns.sort()
        self.n = len(spawns)
        drain_t = self.times[-1] if self.drain else None

        n_samples = int(math.ceil(self.hold * RATE)) + 2
        self.pos = np.full((n_samples, self.n, 2), np.nan, np.float32)
        self.ang = np.zeros((n_samples, self.n), np.float32)
        bodies, nxt = [], 0
        dt = 1.0 / (RATE * SUBSTEPS)
        for i in range(n_samples):
            t = i / RATE
            while nxt < self.n and spawns[nxt][0] <= t:
                _, x, y, spin = spawns[nxt]
                b = pymunk.Body(1.0, pymunk.moment_for_circle(1.0, 0, self.r))
                b.position, b.angular_velocity = (x, y), spin
                c = pymunk.Circle(b, self.r)
                c.elasticity, c.friction = 0.25, 0.7
                space.add(b, c)
                bodies.append(b)
                nxt += 1
            if drain_t is not None:
                ang = self.flap_angle(t - drain_t)
                for b, sign in flaps:
                    target = sign * ang
                    b.angular_velocity = (target - b.angle) * RATE
            for b_i, b in enumerate(bodies):
                self.pos[i, b_i] = b.position
                self.ang[i, b_i] = b.angle
            for _ in range(SUBSTEPS):
                space.step(dt)

    def flap_angle(self, since: float) -> float:
        """How far each trapdoor has swung down, `since` the drain began."""
        return 0.0 if since <= 0 else (math.pi / 2) * _smooth(min(1.0, since / self.OPEN))

    # --- drawing ----------------------------------------------------------

    def _sprites(self):
        """One coin, rendered at 4x and scaled down, at 24 rotations."""
        br = self.brand
        d = int(math.ceil(self.r * 2)) + 2
        big = 4 * d
        im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        g = ImageDraw.Draw(im)
        rim = tuple(int(c * 0.72) for c in br.primary)
        g.ellipse([4, 4, big - 5, big - 5], fill=(*rim, 255))
        g.ellipse([big * 0.11, big * 0.11, big * 0.89, big * 0.89],
                  fill=(*br.primary, 255))
        g.arc([big * 0.18, big * 0.18, big * 0.82, big * 0.82], 200, 300,
              fill=(255, 255, 255, 120), width=max(2, big // 28))
        glyphs = {d_[2] for d_ in self.drops if len(d_) > 2 and d_[2]}
        self.sprites = {}
        for glyph in glyphs | {""}:
            base = im.copy()
            if glyph:
                f = _display(int(big * 0.42))
                b = ImageDraw.Draw(base).textbbox((0, 0), glyph, font=f)
                ImageDraw.Draw(base).text(
                    ((big - (b[2] - b[0])) / 2 - b[0], (big - (b[3] - b[1])) / 2 - b[1]),
                    glyph, font=f, fill=(*br.band_ink, 230))
            small = base.resize((d, d), Image.LANCZOS)
            self.sprites[glyph] = [small.rotate(-15 * k, resample=Image.BICUBIC)
                                   for k in range(24)] if glyph else [small]
        # Which glyph each coin carries, in spawn order.
        self.coin_glyph = []
        for count, *rest in self.drops:
            glyph = rest[1] if len(rest) > 1 and rest[1] else ""
            self.coin_glyph += [glyph] * int(count)
        self.coin_glyph = [g for g in self.coin_glyph][: self.n]

    def _sample(self, t):
        x = min(max(t, 0.0) * RATE, self.pos.shape[0] - 1.001)
        i = int(x)
        a = x - i
        p = self.pos[i] * (1 - a) + self.pos[i + 1] * a
        return p, self.ang[i] * (1 - a) + self.ang[i + 1] * a

    def _pill(self, d, text, y, fill, ink, q):
        f = _font(int(self.frame.w * (0.040 if self.portrait else 0.022)))
        text = text.upper()
        b = d.textbbox((0, 0), text, font=f)
        tw, th = b[2] - b[0], b[3] - b[1]
        pw, ph = tw + f.size * 1.2, th + f.size * 0.8
        x = self.cx - pw / 2
        y = y - ph - (1 - q) * 12
        a = int(255 * q)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=int(ph * 0.22),
                            fill=(*fill, a))
        d.text((x + (pw - tw) / 2 - b[0], y + (ph - th) / 2 - b[1]), text,
               font=f, fill=(*ink, a))

    def content(self, out: Image.Image, f: float) -> None:
        t = self.at(f) - self.start
        br = self.brand
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)

        # The container draws on as the beat opens.
        e = _smooth(min(1.0, t / 0.5))
        x0, x1 = self.cx - self.cw / 2, self.cx + self.cw / 2
        ink = (*br.ink, int(230 * e))
        rise = self.ch * e
        d.line([(x0, self.bottom), (x0, self.bottom - rise)], fill=ink, width=self.wall)
        d.line([(x1, self.bottom), (x1, self.bottom - rise)], fill=ink, width=self.wall)
        ang = self.flap_angle(t - self.times[-1]) if self.drain else 0.0
        half = self.cw / 2
        for hinge, sign in ((x0, 1.0), (x1, -1.0)):
            end = (hinge + sign * half * math.cos(ang),
                   self.bottom + half * math.sin(ang))
            d.line([(hinge, self.bottom), end], fill=ink, width=self.wall)

        pos, ang = self._sample(t)
        W, H = self.frame.size
        for k in range(self.n):
            x, y = pos[k]
            if np.isnan(x) or y > H + self.r * 2:
                continue
            sprites = self.sprites[self.coin_glyph[k] if k < len(self.coin_glyph) else ""]
            sp = sprites[int(round(math.degrees(ang[k]) / 15)) % len(sprites)]
            layer.alpha_composite(sp, (int(round(x - sp.width / 2)),
                                       int(round(y - sp.height / 2))))

        # The label of the batch now pouring, above the rim; the drain's, red.
        label_y = self.top - self.r * 2.6
        cur = None
        for i, t0 in enumerate(self.times):
            if t >= t0:
                cur = i
        if cur is not None:
            q = _smooth(min(1.0, (t - self.times[cur]) / self.LABEL_IN))
            if self.drain and cur == len(self.times) - 1:
                self._pill(d, self.drain, label_y, br.negative, (255, 255, 255), q)
            else:
                text = self.drops[cur][1]
                if text:
                    fill = br.band or br.primary
                    self._pill(d, text, label_y, fill, br.band_ink, q)
        out.paste(layer, (0, 0), layer)
        # **The heading goes on last, over the coins, with a dark edge.**
        # Coins spawn above the frame and, in 9:16, fall straight through the
        # kicker's row: drawn first, a coin covered "EY" of "WHERE THE MONEY
        # GOES" in the Mac demo (2026-11-05). Drawn last it was still gone -
        # gold type on a gold coin face - so it gets a dark stroke here, the
        # same colour as the coin's own "$". Local to `pile`: the shared
        # `heading` is in every approved cut and stays as it is.
        if self.title:
            ImageDraw.Draw(out).text(
                (self.col[0], self.head_y), self.title.upper(), font=_font(34),
                fill=br.primary, stroke_width=3, stroke_fill=(20, 20, 20))
        self.heading(out, self.title, f)
