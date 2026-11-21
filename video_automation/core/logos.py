"""Round logo badges for the tools and platforms a video names
(2026-11-21: "when talking about TikTok, Instagram or other software, show
the logos").

    PYTHONPATH=. .venv/bin/python tools/oktai_logos.py      # all of them
    logos.path("claude")                                    # in a script

Writes `assets/brand/logos/<slug>.png`, 512 px, transparent outside the
circle, so a `logos` beat (`Shot(graphic="logos", payload=([LOGO("claude"),
...], "TITLE"))`) can line them up. Three sources, in this order:

* **The portfolio's own badges** (`~/Coding/portfolio/assets/images`):
  Claude, n8n, OpenAI (Whisper), GitHub, Docker, Node, Next.js, Figma.
* **Ionicons** (MIT, vendored in the portfolio): TikTok and Instagram glyphs,
  set on their brand colours here.
* **Drawn here** where no file exists on this machine: YouTube's play
  button, Facebook's "f", and plain name badges for Python, FFmpeg, Pexels,
  Playwright and Kokoro. A name badge is honest - it says the name in the
  brand's colour, it does not imitate a mark. Swap in an official file by
  saving it under the same slug.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "assets/brand/logos"
PORTFOLIO = Path.home() / "Coding/portfolio/assets"
IONICONS = PORTFOLIO / "vendor/ionicons/svg"

COPY = {"claude": "claude", "n8n": "n8n", "openai": "openai", "github": "git",
        "docker": "docker", "node": "node", "nextjs": "next", "figma": "figma"}


def _svg_path(name: str) -> str:
    s = (IONICONS / f"logo-{name}.svg").read_text()
    return s[s.index("<path"):s.rindex("</svg>")]


def _badges() -> dict[str, str]:
    """slug -> HTML of the badge's inner circle (512x512)."""
    tik = _svg_path("tiktok").replace("<path", "<path fill='{c}'")
    ig = _svg_path("instagram")
    return {
        "tiktok": f"""<div class=c style="background:#000">
          <svg viewBox="0 0 512 512" style="position:absolute;width:56%;left:23%;top:22%">
          <g transform="translate(-9,-7)">{tik.format(c='#25F4EE')}</g>
          <g transform="translate(9,7)">{tik.format(c='#FE2C55')}</g>
          {tik.format(c='#fff')}</svg></div>""",
        "instagram": f"""<div class=c style="background:radial-gradient(circle at 30% 107%,
          #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%)">
          <svg viewBox="0 0 512 512" style="position:absolute;width:58%;left:21%;top:21%;
          fill:#fff">{ig}</svg></div>""",
        "youtube": """<div class=c style="background:#fff">
          <div style="position:absolute;left:21%;top:31%;width:58%;height:40%;
          background:#FF0000;border-radius:22%"></div>
          <div style="position:absolute;left:44%;top:40%;width:0;height:0;
          border-left:68px solid #fff;border-top:40px solid transparent;
          border-bottom:40px solid transparent"></div></div>""",
        "facebook": """<div class=c style="background:#1877F2">
          <span style="position:absolute;left:0;right:0;bottom:-12%;text-align:center;
          font:800 400px 'Helvetica Neue',Arial;color:#fff">f</span></div>""",
        "python": """<div class=c style="background:#1e1e24">
          <span class=w style="color:#FFD43B">py<b style="color:#4B8BBE">thon</b></span></div>""",
        "ffmpeg": """<div class=c style="background:#0f1a0f">
          <span class=w style="color:#5cb85c">FFmpeg</span></div>""",
        "pexels": """<div class=c style="background:#05A081">
          <span class=w style="color:#fff">Pexels</span></div>""",
        "playwright": """<div class=c style="background:#1e1e24">
          <span class=w style="color:#2EAD33;font-size:86px">Playwright</span></div>""",
        "kokoro": """<div class=c style="background:#14141a;border:10px solid #ffdb70;box-sizing:border-box">
          <span class=w style="color:#ffdb70">Kokoro</span></div>""",
    }


PAGE = """<!doctype html><html><head><meta charset=utf-8><style>
html,body{{margin:0;background:transparent}}
.c{{position:relative;width:512px;height:512px;border-radius:50%;overflow:hidden}}
.w{{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;
   font:700 108px 'Helvetica Neue',Arial;letter-spacing:-2px}}
.w b{{font-weight:700}}
</style></head><body>{inner}</body></html>"""


def build() -> list[Path]:
    from PIL import Image
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for slug, src in COPY.items():
        p = PORTFOLIO / "images" / f"{src}.webp"
        if p.exists():
            im = Image.open(p).convert("RGBA").resize((512, 512), Image.LANCZOS)
            im.save(OUT / f"{slug}.png")
            made.append(OUT / f"{slug}.png")
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page(viewport={"width": 512, "height": 512})
        for slug, inner in _badges().items():
            page.set_content(PAGE.format(inner=inner))
            out = OUT / f"{slug}.png"
            page.locator(".c").screenshot(path=str(out), omit_background=True)
            made.append(out)
        b.close()
    return made


def path(slug: str) -> Path:
    """The badge file for a project's `logos` payload."""
    p = OUT / f"{slug}.png"
    if not p.exists():
        build()
    return p

