"""
WHICH WIDTHS ACTUALLY EXIST
===========================
The site had two generations of photograph in it — the originals at 800/1020
and the new ones at 640/1000 — and every helper that wrote a `srcset` guessed
the widths. Thirty broken images, none of them visible on the machine that
built the page, because a missing `srcset` candidate simply falls back to
another one until they all fail.

So nothing guesses any more. This reads the img/ folder and reports the widths
that are really on disk for a given stem. A photograph that only exists at
640px gets a srcset with one entry, which is correct; a stem with no files at
all raises, which is a great deal better than a page shipping a broken image.
"""

import pathlib
import re

IMG = pathlib.Path(__file__).resolve().parent.parent / "img"

_cache = {}


def widths(stem):
    """[640, 1000] — every width this photograph exists at, smallest first."""
    if stem in _cache:
        return _cache[stem]
    found = set()
    for path in IMG.glob(f"{stem}-*.jpg"):
        match = re.fullmatch(rf"{re.escape(stem)}-(\d+)", path.stem)
        if match:
            found.add(int(match.group(1)))
    out = sorted(found)
    _cache[stem] = out
    return out


def has(stem):
    return bool(widths(stem))


def picture(stem, alt, sizes="100vw", cls="", loading="lazy", eager=False):
    """A responsive <picture> built from the files that are actually there.

    WebP is only offered where the .webp really exists beside the .jpg, so a
    photograph converted by hand and never re-run through build_media does not
    silently serve a 404 to every modern browser.
    """
    sizes_list = widths(stem)
    if not sizes_list:
        raise ValueError(
            f"No image files for '{stem}'. Run _src/build_media.py, or check "
            f"the name against the files in img/.")

    jpg = ", ".join(f"img/{stem}-{w}.jpg {w}w" for w in sizes_list)
    webp = [w for w in sizes_list if (IMG / f"{stem}-{w}.webp").exists()]
    source = ""
    if webp:
        srcset = ", ".join(f"img/{stem}-{w}.webp {w}w" for w in webp)
        source = f'<source type="image/webp" srcset="{srcset}" sizes="{sizes}">'

    biggest = sizes_list[-1]
    attrs = f'class="{cls}" ' if cls else ""
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f"<picture>{source}"
            f'<img {attrs}src="img/{stem}-{sizes_list[0]}.jpg" srcset="{jpg}" '
            f'sizes="{sizes}" alt="{alt}" {load} decoding="async"></picture>')
