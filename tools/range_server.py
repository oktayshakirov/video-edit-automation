"""Serve a folder on 127.0.0.1 with HTTP Range support.

The resumable Publish Facebook Video workflow pulls the render in the byte
ranges Facebook asks for (`Range: bytes=a-b`), and the stdlib `http.server`
ignores Range and always sends the whole file. Everything else - plain GETs
for the Reel tunnel, HEAD for the size - behaves like `http.server`, so this
can stand in for it on port 8765 in every publish run.

    python3 tools/range_server.py --directory <folder> [--port 8765]
"""

from __future__ import annotations

import argparse
import functools
import os
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

RANGE = re.compile(r"bytes=(\d*)-(\d*)$")


class RangeHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        header = self.headers.get("Range")
        path = self.translate_path(self.path)
        if not header or not os.path.isfile(path):
            return super().send_head()
        m = RANGE.match(header.strip())
        size = os.path.getsize(path)
        if not m or (not m[1] and not m[2]):
            self.send_error(416, "Unsupported Range")
            return None
        if m[1]:
            start = int(m[1])
            end = min(int(m[2]), size - 1) if m[2] else size - 1
        else:  # suffix range: the last N bytes
            start, end = max(size - int(m[2]), 0), size - 1
        if start > end or start >= size:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None
        f = open(path, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._remaining = end - start + 1
        return f

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_remaining", None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        while remaining > 0:
            buf = source.read(min(1 << 20, remaining))
            if not buf:
                break
            outputfile.write(buf)
            remaining -= len(buf)
        self._remaining = None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", required=True)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--bind", default="127.0.0.1")
    a = ap.parse_args()
    handler = functools.partial(RangeHandler, directory=a.directory)
    with ThreadingHTTPServer((a.bind, a.port), handler) as httpd:
        print(f"serving {a.directory} on http://{a.bind}:{a.port} (Range enabled)", flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
