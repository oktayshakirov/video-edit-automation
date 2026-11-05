#!/usr/bin/env bash
# Set up a Linux machine that is not the build Mac - a Claude Code cloud
# session or a CI runner - for the work that can be done there.
#
#     bash tools/cloud_setup.sh            # venv + pins + the two site repos
#     bash tools/cloud_setup.sh --kokoro   # ...and the ~350MB Kokoro model
#
# What that buys, and what it does not, is in docs/video/cloud.md. In short:
# tests, script drafting and every static check, topic suggestions, frames of
# a beat to look at, and (with --kokoro) narration synthesis, so preflight can
# report a draft's runtime and chapters. Not a shippable render: the stock
# bytes, the brand sfx, the macOS fonts and the credentials stay on the Mac.
#
# Safe to rerun. It never touches a site checkout it did not create, and it
# refuses to run on macOS, where ~/Coding holds the real working copies.

set -euo pipefail

if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "cloud_setup.sh is for cloud sessions and CI, not the build Mac." >&2
    exit 1
fi

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODING="${HOME}/Coding"
KOKORO=0
for arg in "$@"; do
    case "$arg" in
        --kokoro) KOKORO=1 ;;
        *) echo "unknown option: $arg" >&2; exit 2 ;;
    esac
done

# 1. The venv, from the exact pins. The three TTS pins are the voice; see
#    requirements.txt before changing anything here.
if [[ ! -x "$REPO/.venv/bin/python" ]]; then
    python3 -m venv "$REPO/.venv"
fi
"$REPO/.venv/bin/python" -m pip install -q --disable-pip-version-check \
    -r "$REPO/requirements.txt"

# 2. The two sites, sparse and shallow, where the engine expects them
#    (~/Coding/<repo>). Only the parts a build or a check reads: the posts,
#    the video registry and the images. `topics.py`, `crypto/facts.py` and the
#    `logos` beat all resolve against these paths.
clone_site() {
    local repo="$1"; shift
    if [[ -e "$CODING/$repo" ]]; then
        echo "  $CODING/$repo exists - left as it is"
        return
    fi
    mkdir -p "$CODING"
    git clone -q --depth 1 --filter=blob:none --sparse \
        "https://github.com/oktayshakirov/$repo.git" "$CODING/$repo"
    git -C "$CODING/$repo" sparse-checkout set "$@"
    echo "  cloned $repo ($*)"
}
echo "sites:"
clone_site crypto-wiki content json public/images
clone_site tinnitus-blog content src/data public

# 3. Optionally, the Kokoro weights the narration is synthesised with. Same
#    files, same directory as on the Mac (core/voiceover.py, KOKORO_DIR).
if [[ "$KOKORO" == 1 ]]; then
    dir="$HOME/.local/share/kokoro"
    base="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
    mkdir -p "$dir"
    for f in kokoro-v1.0.onnx voices-v1.0.bin; do
        if [[ -s "$dir/$f" ]]; then
            echo "  $f present"
        else
            curl -fsSL --retry 4 -o "$dir/$f.part" "$base/$f"
            mv "$dir/$f.part" "$dir/$f"
            echo "  fetched $f"
        fi
    done
fi

echo "ready. run: .venv/bin/python -m pytest tests -q"
