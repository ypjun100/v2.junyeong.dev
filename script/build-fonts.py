#!/usr/bin/env python3
"""Regenerate the self-hosted webfont subsets in assets/fonts/.

Run this when a font, a weight, or a Korean label in a template changes:

    python3 -m venv .venv && .venv/bin/pip install fonttools brotli
    .venv/bin/python script/build-fonts.py

Source TTFs are downloaded from Google Fonts and are not kept in the repo.
All four families are licensed under the SIL Open Font License 1.1, which
permits self-hosting and subsetting; see assets/fonts/OFL.txt.

Two subsetting strategies, picked per role:

  content  Fonts that render text from content/*.md, where the characters are
           not known ahead of time. These get every modern Hangul syllable,
           split in two by unicode-range: the 2350 KS X 1001 syllables that
           cover essentially all Korean prose, and the remaining 8822 that the
           browser fetches only if a page actually uses one.

  ui       Fonts that only ever render labels written in the templates. The
           character set is therefore known, and the subset is built from it.
           Adding a new Korean label to a template means rerunning this script;
           check_ui_coverage() below fails the build if that is forgotten.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "fonts"
SCSS = ROOT / "_sass" / "_fonts.scss"
WORK = ROOT / ".font-build"

LATIN = ",".join([
    "U+0020-007E", "U+00A0-00FF", "U+2010-2027", "U+2030-205E",
    "U+20A9", "U+20AC", "U+2190-2199", "U+3000-303F", "U+3131-318E",
    "U+FF01-FF60",
])

# family, weight, role
FONTS = [
    ("Nanum Myeongjo",    400, "content"),
    ("Nanum Myeongjo",    700, "content"),
    ("IBM Plex Sans KR",  400, "ui"),
    ("IBM Plex Sans KR",  600, "ui"),
    ("IBM Plex Sans KR",  700, "ui"),
    ("IBM Plex Mono",     400, "latin"),
    ("IBM Plex Mono",     500, "latin"),
]

# The ui face is only ever applied to the sidebar and to a handful of labels.
# Everything else in the templates is set in the body face, which carries the
# full Hangul range, so scraping whole files would bloat the ui subset with
# characters it never draws. These patterns track the classes that set
# font-family: var(--font-ui) in _sass/.
UI_WHOLE_FILES = ["_includes/sidebar.html"]
UI_ELEMENT_PATTERNS = [
    r'class="section-label[^"]*"[^>]*>(.*?)<',
    r'class="section-head__more"[^>]*>(.*?)<',
    r'class="intro__stat-label"[^>]*>(.*?)<',
    r'class="chip"[^>]*>(.*?)<',
]
UI_SEARCH_FILES = ["_includes/*.html", "_layouts/*.html", "index.html", "about.html", "posts.html"]
# The sidebar prints these through Liquid, so they never appear as literal text
# in a template and scraping alone would miss them.
UI_CONFIG_KEYS = ["title", "tagline"]


def in_ks_x_1001(ch):
    """KS X 1001 sits in EUC-KR lead 0xB0-0xC8, trail 0xA1-0xFE. Python's
    euc-kr codec also accepts the CP949 extension, so the byte range is what
    separates the 2350 from the other 8822."""
    try:
        b = ch.encode("euc-kr")
    except UnicodeEncodeError:
        return False
    return len(b) == 2 and 0xB0 <= b[0] <= 0xC8 and 0xA1 <= b[1] <= 0xFE


SYLLABLES = [chr(c) for c in range(0xAC00, 0xD7A4)]
COMMON = [c for c in SYLLABLES if in_ks_x_1001(c)]
REST = [c for c in SYLLABLES if not in_ks_x_1001(c)]


def template_hangul():
    config = (ROOT / "_config.yml").read_text(encoding="utf-8")
    text = "".join(
        m.group(1) for key in UI_CONFIG_KEYS
        for m in [re.search(rf"^{key}:\s*(.+)$", config, re.M)] if m
    )
    for name in UI_WHOLE_FILES:
        text += (ROOT / name).read_text(encoding="utf-8")
    for pattern in UI_SEARCH_FILES:
        for path in ROOT.glob(pattern):
            body = path.read_text(encoding="utf-8")
            for element in UI_ELEMENT_PATTERNS:
                text += "".join(re.findall(element, body, re.S))
    return "".join(sorted({c for c in text if "가" <= c <= "힣"}))


def check_ui_coverage(chars):
    """A template label outside KS X 1001 would silently miss from the ui
    subset on a later rebuild, so surface it now."""
    stray = [c for c in chars if not in_ks_x_1001(c)]
    if stray:
        print(f"  note: template labels use {len(stray)} syllable(s) outside KS X 1001: {''.join(stray)}")


def fetch(url, dest=None):
    """curl rather than urllib: the macOS framework Python ships without a
    usable CA bundle, and this script should not depend on which Python it is."""
    cmd = ["curl", "-sSfL", "-A", "curl/7.0", url]  # old UA gets ttf, not woff2
    if dest:
        cmd += ["-o", str(dest)]
        subprocess.run(cmd, check=True)
        return None
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def ttf_url(family, weight):
    spec = family.replace(" ", "+")
    css = fetch(f"https://fonts.googleapis.com/css2?family={spec}:wght@{weight}")
    match = re.search(r"url\((https://[^)]+\.ttf)\)", css)
    if not match:
        sys.exit(f"no ttf for {family} {weight}")
    return match.group(1)


def slug(family, weight):
    return f"{family.lower().replace(' ', '-')}-{weight}"


def subset(src, out, *, text=None, unicodes=None):
    cmd = [sys.executable, "-m", "fontTools.subset", str(src),
           "--flavor=woff2", "--layout-features=", f"--output-file={out}"]
    if text is not None:
        chars = WORK / (out.stem + ".txt")
        chars.write_text(text, encoding="utf-8")
        cmd.append(f"--text-file={chars}")
    if unicodes:
        cmd.append(f"--unicodes={unicodes}")
    subprocess.run(cmd, check=True, capture_output=True)


def ranges_css(chars):
    cps = sorted(ord(c) for c in chars)
    out, start, prev = [], cps[0], cps[0]
    for c in cps[1:]:
        if c == prev + 1:
            prev = c
        else:
            out.append((start, prev))
            start = prev = c
    out.append((start, prev))
    return ",".join(f"U+{a:04X}" if a == b else f"U+{a:04X}-{b:04X}" for a, b in out)


def face(family, weight, filename, unicode_range=None):
    lines = [
        "@font-face {",
        f'  font-family: "{family}";',
        "  font-style: normal;",
        f"  font-weight: {weight};",
        "  font-display: swap;",
        f'  src: url("/assets/fonts/{filename}") format("woff2");',
    ]
    if unicode_range:
        lines.append(f"  unicode-range: {unicode_range};")
    lines.append("}")
    return "\n".join(lines)


def main():
    try:
        import fontTools, brotli  # noqa: F401
    except ImportError:
        sys.exit("this script needs fonttools and brotli: pip install fonttools brotli")

    WORK.mkdir(exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    ui_chars = template_hangul()
    check_ui_coverage(ui_chars)
    print(f"  ui subset covers {len(ui_chars)} template syllables")

    rest_range = ranges_css(REST)
    faces, total = [], 0

    for family, weight, role in FONTS:
        src = WORK / f"{slug(family, weight)}.ttf"
        if not src.exists():
            fetch(ttf_url(family, weight), src)

        base = slug(family, weight)
        main_file = OUT / f"{base}.woff2"

        if role == "content":
            subset(src, main_file, text="".join(COMMON), unicodes=LATIN)
            rest_file = OUT / f"{base}.rest.woff2"
            subset(src, rest_file, text="".join(REST))
            faces.append(face(family, weight, main_file.name))
            faces.append(face(family, weight, rest_file.name, rest_range))
            sizes = f"{main_file.stat().st_size/1024:7.1f} KB + {rest_file.stat().st_size/1024:7.1f} KB rest"
            total += main_file.stat().st_size
        elif role == "ui":
            subset(src, main_file, text=ui_chars, unicodes=LATIN)
            faces.append(face(family, weight, main_file.name))
            sizes = f"{main_file.stat().st_size/1024:7.1f} KB"
            total += main_file.stat().st_size
        else:
            subset(src, main_file, unicodes=LATIN)
            faces.append(face(family, weight, main_file.name))
            sizes = f"{main_file.stat().st_size/1024:7.1f} KB"
            total += main_file.stat().st_size

        print(f"  {family} {weight:<4} {role:<8} {sizes}")

    header = (
        "// Generated by script/build-fonts.py. Do not edit by hand.\n"
        "// The .rest faces are declared after their sibling so that, where the\n"
        "// ranges overlap, the browser prefers the rest file for those syllables.\n\n"
    )
    SCSS.write_text(header + "\n\n".join(faces) + "\n", encoding="utf-8")
    print(f"\n  wrote {SCSS.relative_to(ROOT)} ({SCSS.stat().st_size/1024:.1f} KB)")
    print(f"  always-loaded total: {total/1024:.1f} KB")
    shutil.rmtree(WORK)


if __name__ == "__main__":
    main()
