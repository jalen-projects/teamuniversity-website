"""
BUILD THE SITE'S MEDIA
======================
Takes the university's own photographs and video out of the Desktop working
folders and produces what a web page should actually be served: several widths
of each image, WebP beside JPEG, and nothing larger than it needs to be.

Run from the site root:

    python _src/build_media.py

Why widths rather than one big file: a phone on Ugandan mobile data should
fetch the 640px copy, not the 1600px one meant for a desktop banner. The
`srcset` in the HTML does the choosing; this script provides the choices.

Why WebP *beside* JPEG rather than instead of it: WebP is a third of the size
and every current browser reads it, but the JPEG costs little to keep and is
what an old handset falls back to. `<picture>` serves whichever the browser
says it can read.

The video is copied, not transcoded — there is no ffmpeg on this machine. Only
clips small enough to serve honestly are copied at all; the rest are listed at
the end so somebody can compress them properly before they go anywhere near a
home page.
"""

import os
import shutil
import sys

from PIL import Image, ImageFilter

SOURCE = r"C:\Users\MBABAZI VERONICA\Desktop\DESIGNS"
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(SITE, "img")
VIDEO = os.path.join(SITE, "video")

# The widths the layout actually asks for: a phone, a tablet, a laptop, and a
# wide banner. More than four is bytes nobody downloads.
WIDTHS = [640, 1000, 1400, 1920]

# (source file, output stem, how it is used)
PHOTOS = [
    (r"TEAM\team1.jpg", "campus-life", "students on campus"),
    (r"TEAM\team 2.jpg", "campus-walk", "the walkway"),
    (r"TEAM\team 3.jpg", "campus-group", "students together"),
    (r"TEAM\team 4.jpg", "campus-study", "study"),
    (r"Graduation 1.png", "graduation-1", "graduation"),
    (r"Graduation 2.png", "graduation-2", "graduation"),
    (r"Graduation 3.png", "graduation-3", "graduation"),
    (r"cloud image.jpg", "technology", "computing and technology"),
]

# Only what is small enough to autoplay behind a hero without costing a
# visitor their bundle. A 65 MB clip is not a background, it is a download.
VIDEOS = [
    # The hero. Students with books in a quiet setting, which is what a
    # university home page should be showing — the graduation reel that was
    # here first is cut fast and reads as an advert. It is 5.2 MB, which is
    # more than one wants; CSS keeps it off phones entirely, and if anyone
    # ever gets ffmpeg onto a machine, re-encoding this at a lower bitrate is
    # the single best performance win the site has left.
    (r"students  standing with some books.mp4", "students.mp4", 8),
]


def ensure(path):
    os.makedirs(path, exist_ok=True)


def process_photo(source, stem, note):
    """One photograph at every width the page can ask for, JPEG and WebP."""
    if not os.path.exists(source):
        return f"  ! missing: {source}"
    with Image.open(source) as original:
        original = original.convert("RGB")
        made = []
        for width in WIDTHS:
            # Never upscale. Blowing a 1000px photo up to 1920 adds bytes and
            # softness and not one pixel of detail.
            if original.width < width and width != WIDTHS[0]:
                continue
            height = round(original.height * width / original.width)
            resized = original.resize((width, height), Image.LANCZOS)
            resized.save(os.path.join(IMG, f"{stem}-{width}.jpg"),
                         "JPEG", quality=82, optimize=True, progressive=True)
            resized.save(os.path.join(IMG, f"{stem}-{width}.webp"),
                         "WEBP", quality=80, method=6)
            made.append(width)

        # A tiny blurred copy, inlined as the background of the image's own
        # box, so a slow connection shows the shape of the photograph rather
        # than a grey rectangle while the real one arrives.
        thumb = original.resize((20, max(round(20 * original.height / original.width), 1)))
        thumb = thumb.filter(ImageFilter.GaussianBlur(1))
        thumb.save(os.path.join(IMG, f"{stem}-blur.jpg"), "JPEG", quality=40)
        return f"  {stem}: {', '.join(str(w) for w in made)}  ({note})"


def process_video(source, name, budget_mb):
    if not os.path.exists(source):
        return f"  ! missing: {source}"
    size = os.path.getsize(source) / (1024 * 1024)
    if size > budget_mb:
        return (f"  ! {name} is {size:.1f} MB, over the {budget_mb} MB budget — "
                f"compress it before using it")
    shutil.copy2(source, os.path.join(VIDEO, name))
    return f"  {name}: {size:.1f} MB"


def main():
    ensure(IMG)
    ensure(VIDEO)
    print("Photographs")
    for relative, stem, note in PHOTOS:
        print(process_photo(os.path.join(SOURCE, relative), stem, note))
    print("Video")
    for relative, name, budget in VIDEOS:
        print(process_video(os.path.join(SOURCE, relative), name, budget))
    print("\nDone. Anything marked ! was skipped and is not on the site.")


if __name__ == "__main__":
    sys.exit(main())
