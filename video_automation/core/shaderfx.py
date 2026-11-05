"""GPU effects on a shot: bloom, light leak, chromatic aberration, vignette.

`Shot(shader="bloom")`, `Shot(shader=("leak", 0.7))` or a list of either,
chained in order. The effect runs on that shot's own frames - picture or
drawn beat - before the crossfade, captions and watermark go on, so type the
viewer reads is never smeared. Off by default; a shot without `shader` never
creates a GL context.

| effect | what it does | where it earns its place |
| --- | --- | --- |
| `bloom` | bright parts glow into their surroundings | gold type on black, a lit screen, a city at night |
| `leak` | warm light drifts across, screen-blended, tinted with the brand colour | an opener, a chapter's first shot, a memory |
| `aberration` | colour fringes at the edges, kicked hard at the cut then settling | glitch cuts, a "something is wrong" line |
| `vignette` | the corners fall away | a still that should feel looked at, a session |

GLSL 330, which the Mac's OpenGL 4.1 runs, through ModernGL (MIT): a
standalone context on the Mac, EGL headless on Linux. Bloom samples the
frame's own mipmaps, so it is a handful of texture reads a pixel rather
than a blur loop. Effects are deterministic on one machine; GPUs differ in
the last bit, so a render on another machine is not byte-identical.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

from .brand import CRYPTO, Brand

VERTEX = """
#version 330
in vec2 pos;
out vec2 uv;
void main() { uv = pos * 0.5 + 0.5; gl_Position = vec4(pos, 0.0, 1.0); }
"""

HEADER = """
#version 330
uniform sampler2D tex;
uniform vec2 res;
uniform float time;
uniform float amount;
uniform vec3 tint;
in vec2 uv;
out vec4 color;
float luma(vec3 c) { return dot(c, vec3(0.2126, 0.7152, 0.0722)); }
"""

EFFECTS = {
    # Two passes (see `apply`): "bright" keeps only what is bright, at full
    # resolution, then "bloom" adds that pass's blurrier mip levels back on
    # top of the frame. Thresholding *after* the blur - the first version -
    # averaged thin white type into its black ground and nothing glowed.
    "bright": """
void main() {
    vec3 c = texture(tex, uv).rgb;
    color = vec4(c * smoothstep(0.50, 0.90, luma(c)), 1.0);
}""",
    "bloom": """
uniform sampler2D glowtex;
void main() {
    vec3 base = texture(tex, uv).rgb;
    vec3 glow = vec3(0.0);
    float w = 0.0;
    for (int i = 1; i <= 6; i++) {
        float wi = 1.0 / float(i);
        glow += textureLod(glowtex, uv, float(i)).rgb * wi;
        w += wi;
    }
    color = vec4(base + glow / w * amount * 2.2, 1.0);
}""",
    # Two soft light sources drifting, screen-blended: never darkens.
    "leak": """
void main() {
    vec3 base = texture(tex, uv).rgb;
    float ar = res.x / res.y;
    float t = time * 0.18;
    vec2 c1 = vec2(0.12 + 0.30 * sin(t * 1.3), 0.30 + 0.22 * cos(t * 0.9));
    vec2 c2 = vec2(0.88 + 0.12 * cos(t * 1.1 + 1.0), 0.72 + 0.18 * sin(t * 0.7));
    vec2 d1 = (uv - c1) * vec2(ar, 1.0);
    vec2 d2 = (uv - c2) * vec2(ar, 1.0);
    float a1 = exp(-dot(d1, d1) * 3.2);
    float a2 = exp(-dot(d2, d2) * 5.0);
    vec3 warm = vec3(1.0, 0.42, 0.12);
    vec3 leak = mix(warm, tint, 0.45) * a1 * 0.85 + vec3(1.0, 0.72, 0.38) * a2 * 0.55;
    leak = clamp(leak * amount, 0.0, 1.0);
    color = vec4(1.0 - (1.0 - base) * (1.0 - leak), 1.0);
}""",
    # Red out, blue in, from the centre: a kick at the cut that settles.
    "aberration": """
void main() {
    vec2 d = uv - 0.5;
    float k = amount * 0.004 * (1.0 + 3.0 * exp(-time * 5.0)) * (0.3 + 2.0 * dot(d, d) * 4.0);
    float r = texture(tex, 0.5 + d * (1.0 + k)).r;
    float g = texture(tex, uv).g;
    float b = texture(tex, 0.5 + d * (1.0 - k)).b;
    color = vec4(r, g, b, 1.0);
}""",
    "vignette": """
void main() {
    vec3 base = texture(tex, uv).rgb;
    vec2 d = (uv - 0.5) * vec2(res.x / res.y, 1.0);
    float v = smoothstep(1.05, 0.30, length(d));
    color = vec4(base * mix(1.0, v, clamp(amount, 0.0, 1.5) * 0.65), 1.0);
}""",
}

# What a script may ask for; "bright" is bloom's own first pass.
NAMES = ("bloom", "leak", "aberration", "vignette")

_gl: dict = {}


def context():
    """One GL context for the process: the platform's own, else EGL."""
    if "ctx" in _gl:
        return _gl["ctx"]
    import moderngl
    errors = []
    for kw in ({}, {"backend": "egl"}):
        try:
            _gl["ctx"] = moderngl.create_context(standalone=True, require=330, **kw)
            return _gl["ctx"]
        except Exception as e:      # noqa: BLE001 - every backend may fail
            errors.append(f"{kw or 'default'}: {e}")
    raise RuntimeError("no OpenGL 3.3 context for shader effects - "
                       + "; ".join(errors))


def _program(name: str):
    key = ("prog", name)
    if key not in _gl:
        ctx = context()
        prog = ctx.program(vertex_shader=VERTEX,
                           fragment_shader=HEADER + EFFECTS[name])
        quad = ctx.buffer(np.array([-1, -1, 3, -1, -1, 3], np.float32).tobytes())
        _gl[key] = (prog, ctx.vertex_array(prog, [(quad, "2f", "pos")]))
    return _gl[key]


def _targets(w: int, h: int):
    """Three textures with framebuffers: ping-pong, plus bloom's bright pass."""
    key = ("fbo", w, h)
    if key not in _gl:
        ctx = context()
        pair = []
        for _ in range(3):
            t = ctx.texture((w, h), 3)
            t.filter = (ctx.LINEAR_MIPMAP_LINEAR, ctx.LINEAR)
            t.repeat_x = t.repeat_y = False
            pair.append((t, ctx.framebuffer(color_attachments=[t])))
        _gl[key] = pair
    return _gl[key]


def parse(spec) -> list[tuple[str, float]]:
    """`"bloom"`, `("bloom", 0.6)` or a list of either -> [(name, amount)]."""
    if spec is None:
        return []
    if isinstance(spec, str):
        return [(spec, 1.0)]
    if (isinstance(spec, tuple) and len(spec) == 2
            and isinstance(spec[0], str) and isinstance(spec[1], (int, float))):
        return [(spec[0], float(spec[1]))]
    return [p for item in spec for p in parse(item)]


def apply(img, spec, t: float, brand: Brand = CRYPTO) -> Image.Image:
    """Run the effect chain `spec` over one frame at shot-local time `t`."""
    chain = parse(spec)
    rgb = np.ascontiguousarray(np.asarray(img.convert("RGB") if isinstance(
        img, Image.Image) else img, np.uint8))
    if not chain:
        return Image.fromarray(rgb)
    h, w = rgb.shape[:2]
    ctx = context()
    (ta, fa), (tb, fb), spare = _targets(w, h)
    ta.write(rgb.tobytes())
    src, dst = (ta, fa), (tb, fb)
    tint = tuple(c / 255.0 for c in brand.primary)

    def run(name, read, write, amount, glow=None):
        prog, vao = _program(name)
        write[1].use()
        read[0].use(location=0)
        prog["tex"].value = 0
        if glow is not None:
            glow[0].build_mipmaps()
            glow[0].use(location=1)
            prog["glowtex"].value = 1
        for u, v in (("res", (float(w), float(h))), ("time", float(t)),
                     ("amount", float(amount)), ("tint", tint)):
            if u in prog:
                prog[u].value = v
        vao.render()

    for name, amount in chain:
        if name not in EFFECTS or name == "bright":
            raise ValueError(f"unknown shader {name!r} - known: {', '.join(NAMES)}")
        src[0].build_mipmaps()
        if name == "bloom":
            run("bright", src, spare, amount)
            run("bloom", src, dst, amount, glow=spare)
        else:
            run(name, src, dst, amount)
        src, dst = dst, src
    out = np.frombuffer(src[1].read(components=3, alignment=1), np.uint8)
    ctx.finish()
    return Image.fromarray(out.reshape(h, w, 3))


class ShaderShot:
    """A prepared shot with `Shot(shader=...)` applied to every frame it draws.

    Everything else - `release`, `photo_box`, whatever `render_shots` asks
    of the shot inside - passes straight through.
    """

    def __init__(self, inner, spec, hold: float, brand: Brand = CRYPTO):
        for name, _ in parse(spec):     # an unknown name fails at build time
            if name not in NAMES:
                raise ValueError(f"unknown shader {name!r} - known: "
                                 f"{', '.join(NAMES)}")
        self.inner, self.spec, self.hold, self.brand = inner, spec, hold, brand

    def draw(self, f: float) -> Image.Image:
        return apply(self.inner.draw(f), self.spec, f * self.hold, self.brand)

    def __getattr__(self, name):
        return getattr(self.inner, name)
