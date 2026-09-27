# Elon Musk photographs — Wikimedia Commons

Pulled for the `musk-effect` long/short pair. **This is the only sanctioned
source for a portrait of a named individual on this channel** (see
`docs/video/projects/crypto.md`): licensed, attributable, and at a resolution
that never upscales. Pexels has no licensed footage of a real public figure,
and the site's own `crypto-ogs/elon-musk.png` is 800x532 at L76 — under the
~750px working floor once cropped, and too bright for the palette.

**The two CC BY 2.0 files make any video using them a derivative work, so the
attribution block below goes in the description of anything published.** The
public-domain files need no attribution; they are credited anyway so that the
provenance of every frame is recoverable.

**Three files are kept, and they are exactly the three the scripts use.** The
screened-and-rejected candidates were deleted rather than left in the folder:
an unused asset sitting next to the used ones is how a rejected picture gets
pointed at by name a second time.

| file | px | licence | credit | used by |
| --- | --- | --- | --- | --- |
| `elon-musk-colorado-2022.jpg` | 4534x3018 | Public domain | via Wikimedia Commons | long form, opening and closing bookend |
| `elon-musk-33377877458.jpg` | 4318x2879 | **CC BY 2.0** | Daniel Oberhaus, via Wikimedia Commons | long form "the Musk effect" + title card; Short, the line that names him |
| `elon-musk-april-2022.jpg` | 2428x2636 | Public domain | via Wikimedia Commons | both thumbnails; the `stat` picture column |

## The attribution line to publish

> Photographs of Elon Musk: Daniel Oberhaus (CC BY 2.0) and public-domain
> images, via Wikimedia Commons.

It is carried in `Meta.credits` on the long form, so the `.md` sidecar emits it
into the description automatically. **A Short has no description block of its
own in this pipeline**, so if a Short using these ships anywhere that supports a
caption, the line goes there by hand — that is a `/publish-video` step.

## Screened, and what was rejected

Measured with `stock.screen`, then looked at:

| file | why not |
| --- | --- |
| `elon-musk-2021.jpg` | L132 — a white studio wall, the brightest thing in a near-black video |
| `happy-elon-musk-52005460639.jpg` | L52 on a purple stage, and r1.06 — too square to fill a 16:9 frame, and nothing left to put it in |
| `elon-musk-presenting-the-neuralink-master-plan` | L140, a white stage |
| `elon-musk-and-the-neuralink-future.jpg` | a surgical robot and blue curtains — off-message under a crypto script |
| `usafa-hosts-elon-musk-image-1-of-17.jpg` | L92, a cluttered crowd, he is incidental in it |
| every Trump / Modi / Herzog frame in the Commons categories | a political reading this video does not make |

**No usable video of him exists at this resolution.** Commons' only
non-political clips are the two RAeS talk files, which are **500x374** — a 3.8x
upscale to fill a 1920 frame, against a repo floor of ~750px for a still. The
motion in this pair is therefore a Ken Burns move on the stills, which is what
`PhotoShot` is for.
