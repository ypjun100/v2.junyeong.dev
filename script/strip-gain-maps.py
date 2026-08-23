#!/usr/bin/env python3
"""Cut Apple HDR gain maps out of the photos under imgs/.

An iPhone photo carries a second image after the primary one, linked by an MPF
segment (APP2, "MPF\\0"). On an HDR display iOS Safari applies it to lift
brightness, which is why these blow out on a phone while the page around them
does not. It is data inside the file; no CSS turns it off.

jpegtran -copy none takes the gain map, but it takes EXIF and the ICC profile
with it -- these photos carry Display P3, and at least one relies on an EXIF
Orientation to stand upright. So this removes the MPF segment and the appended
image and nothing else, then checks its own work before writing:

  - the primary image's compressed scan is byte-identical
  - every other marker segment survives, EXIF and ICC included
  - no MPF remains

Standard library only, to keep the no-toolchain rule in AGENTS.md.

    python3 script/strip-gain-maps.py            # report what would change
    python3 script/strip-gain-maps.py --write    # rewrite the files
"""

import argparse
import pathlib
import struct
import sys

# Markers that stand alone -- no length field follows them.
STANDALONE = {0xD8, 0xD9} | set(range(0xD0, 0xD8))


def segments(data):
    """Yield (marker, start, end) for each marker segment before the scan.

    Stops after SOS: what follows is entropy-coded data, not segments.
    """
    i = 2
    while i < len(data) - 1:
        if data[i] != 0xFF:
            raise ValueError(f"expected a marker at {i}, found {data[i]:#04x}")
        marker = data[i + 1]
        if marker in STANDALONE:
            yield marker, i, i + 2
            i += 2
            continue
        length = struct.unpack(">H", data[i + 2 : i + 4])[0]
        yield marker, i, i + 2 + length
        if marker == 0xDA:  # SOS -- the scan starts here
            return
        i += 2 + length


def primary_end(data, scan_start):
    """Offset just past the primary image's EOI.

    Walks the entropy-coded data, stepping over stuffed bytes (FF 00) and
    restart markers, which are not real markers.
    """
    i = scan_start
    while i < len(data) - 1:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker == 0x00 or marker == 0xFF or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        if marker == 0xD9:
            return i + 2
        i += 2
    raise ValueError("no EOI found for the primary image")


def app_tag(data, start, end):
    """The identifier an APPn segment opens with, e.g. b'Exif', b'MPF\\0'."""
    return data[start + 4 : end].split(b"\x00")[0] + b"\x00"


def strip(data):
    """Return the file without its MPF segment and appended image, or None."""
    mpf = None
    scan = None
    for marker, start, end in segments(data):
        if marker == 0xE2 and data[start + 4 : start + 8] == b"MPF\x00":
            mpf = (start, end)
        if marker == 0xDA:
            scan = end
    if mpf is None:
        return None
    return data[: mpf[0]] + data[mpf[1] : primary_end(data, scan)]


def check(before, after):
    """Raise unless `after` is `before` minus the gain map and nothing else."""
    kept = [(m, before[s:e]) for m, s, e in segments(before)]
    got = [(m, after[s:e]) for m, s, e in segments(after)]
    dropped = [(m, b) for m, b in kept if (m, b) not in got]
    if len(dropped) != 1 or dropped[0][0] != 0xE2:
        raise ValueError(f"expected to drop one APP2, dropped {len(dropped)}")
    if not dropped[0][1][4:8] == b"MPF\x00":
        raise ValueError("dropped the wrong APP2")

    scan_before = next(e for m, s, e in segments(before) if m == 0xDA)
    scan_after = next(e for m, s, e in segments(after) if m == 0xDA)
    if before[scan_before : primary_end(before, scan_before)] != after[scan_after:]:
        raise ValueError("the compressed scan changed")

    for marker, start, end in segments(after):
        if marker == 0xE2 and after[start + 4 : start + 8] == b"MPF\x00":
            raise ValueError("MPF still present")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="rewrite the files")
    ap.add_argument("--root", default="imgs", help="directory to walk")
    args = ap.parse_args()

    paths = sorted(
        p
        for ext in ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG")
        for p in pathlib.Path(args.root).rglob(ext)
    )
    hits = saved = 0
    for path in paths:
        before = path.read_bytes()
        try:
            after = strip(before)
        except ValueError as err:
            print(f"  skipped {path}: {err}", file=sys.stderr)
            continue
        if after is None:
            continue
        check(before, after)
        hits += 1
        saved += len(before) - len(after)
        tags = [
            app_tag(after, s, e).rstrip(b"\x00").decode("latin-1")
            for m, s, e in segments(after)
            if 0xE0 <= m <= 0xEF
        ]
        print(f"  {path}  {len(before):,} -> {len(after):,}  keeps {', '.join(tags)}")
        if args.write:
            path.write_bytes(after)

    verb = "stripped" if args.write else "would strip"
    print(f"\n{len(paths)} JPEGs, {verb} {hits}, {saved / 1e6:.1f}MB")
    if hits and not args.write:
        print("Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
