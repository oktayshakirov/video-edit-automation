"""thecrypto.wiki shorts.

Built: a photo-driven short assembled from the site's own image library —
`shots.py` prepares the picture (blurred-fill Ken Burns, drawn data graphics,
watermark) and `build.py` cuts it to measured narration and burns captions.

Not built: script generation from MDX, upload, and the on-site embed. The script
stays hand-written for now, which is the right way round — it is the product,
and 60 posts of generated scripts is the failure mode rather than the goal.

No stock API. Every image comes from `crypto-wiki/public/images`, which is
already licensed and on brand, and avoids the AI-voice-over-stock-loops pattern
both platforms suppress.
"""
