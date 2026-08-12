"""
CHECK THE BUILT SITE
====================
Not a validator — a list of the things that actually break a static site once
it is on a server, each of which is invisible on the machine that built it:

  * a link to a page that was renamed or never existed
  * an <img>, <source> or poster pointing at a file that is not in img/
  * a video the repository does not contain
  * an id="" that two elements share, which breaks every #anchor to it
  * an <a href="#thing"> where nothing on the page has that id
  * an <img> with no alt attribute

    python _src/check.py

Exits non-zero if anything is wrong, so it can gate a deploy.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:")


def attrs(html, tag, attribute):
    return re.findall(rf'<{tag}\b[^>]*?\b{attribute}="([^"]+)"', html, re.I)


def check(page):
    html = page.read_text(encoding="utf-8")
    problems = []
    name = page.name

    # --- internal links ---------------------------------------------------
    for href in attrs(html, "a", "href"):
        if href.startswith(SKIP_SCHEMES) or href.startswith("#"):
            continue
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        if not (ROOT / target).exists():
            problems.append(f"link to missing page: {href}")

    # --- images, sources, posters, videos ---------------------------------
    assets = []
    assets += [(src, "img src") for src in attrs(html, "img", "src")]
    assets += [(src, "video poster") for src in attrs(html, "video", "poster")]
    assets += [(src, "source src") for src in attrs(html, "source", "src")]
    for value in attrs(html, "source", "srcset") + attrs(html, "img", "srcset"):
        for piece in value.split(","):
            url = piece.strip().split(" ")[0]
            if url:
                assets.append((url, "srcset"))
    for url, where in assets:
        if url.startswith(SKIP_SCHEMES):
            continue
        if not (ROOT / url).exists():
            problems.append(f"missing file ({where}): {url}")

    # --- stylesheets and scripts ------------------------------------------
    for href in attrs(html, "link", "href"):
        if href.startswith(SKIP_SCHEMES):
            continue
        if not (ROOT / href).exists():
            problems.append(f"missing stylesheet: {href}")
    for src in attrs(html, "script", "src"):
        if not src.startswith(SKIP_SCHEMES) and not (ROOT / src).exists():
            problems.append(f"missing script: {src}")

    # --- duplicate ids ----------------------------------------------------
    ids = re.findall(r'\bid="([^"]+)"', html)
    seen, dupes = set(), set()
    for one in ids:
        (dupes if one in seen else seen).add(one)
    for one in sorted(dupes):
        problems.append(f"duplicate id: {one}")

    # --- anchors that go nowhere ------------------------------------------
    for href in attrs(html, "a", "href"):
        if href.startswith("#") and len(href) > 1:
            if href[1:] not in seen:
                problems.append(f"anchor with no target: {href}")

    # --- images without alt ------------------------------------------------
    for tag in re.findall(r"<img\b[^>]*>", html, re.I):
        if not re.search(r'\balt="', tag):
            problems.append(f"img without alt: {tag[:70]}…")

    # --- the finder's payload has to be real JSON --------------------------
    payload = re.search(r'<script id="progData"[^>]*>(.*?)</script>', html, re.S)
    if payload:
        try:
            rows = json.loads(payload.group(1))
            if not rows:
                problems.append("programme data is empty")
        except Exception as error:
            problems.append(f"programme data is not valid JSON: {error}")

    return name, problems


def main():
    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        print("No built pages found. Run _src/build.py first.")
        return 1
    total = 0
    for page in pages:
        name, problems = check(page)
        if problems:
            total += len(problems)
            print(f"\n{name}")
            for problem in problems:
                print(f"  - {problem}")
    print(f"\n{len(pages)} pages checked, {total} problem(s).")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
