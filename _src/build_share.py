"""
THE LINK-PREVIEW CARD — img/og-share.jpg (1200 x 630)
=====================================================
What WhatsApp, Facebook, X and LinkedIn show when somebody pastes a link to
the site. Everything important sits in the middle third, because WhatsApp
sometimes crops the card to a centred square. It is kept under 300 KB:
WhatsApp silently drops larger preview images.

    python build_share.py <photo.jpg> <RobotoCondensed[wght].ttf> <Poppins-Medium.ttf>

If you change the card, change OG_IMAGE's file name in build.py too, or
WhatsApp keeps showing the old one from its cache.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 630
BLUE, GOLD, GREEN, NAVY = (11, 85, 166), (246, 192, 33), (0, 132, 61), (5, 42, 87)


def cover(img, w, h, focus_y=0.4):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = int((img.height - h) * focus_y)
    return img.crop((x, y, x + w, y + h))


def main(photo, rc_path, pop_path):
    card = cover(Image.open(photo).convert("RGB"), W, H)

    # Navy wash: light at the top so the photo reads, deep at the bottom for text.
    wash = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(wash)
    for y in range(H):
        t = y / H
        a = int(70 + 175 * max(0, t - 0.25) / 0.75)
        d.line([(0, y), (W, y)], fill=NAVY + (min(a, 235),))
    card = Image.alpha_composite(card.convert("RGBA"), wash)

    # The crest seal: white disc, gold border, soft gold glow.
    cx, cy, r = W // 2, 168, 112
    glow = Image.new("RGBA", (W, H))
    ImageDraw.Draw(glow).ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), fill=(255, 210, 80, 150))
    card = Image.alpha_composite(card, glow.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(card)
    d.ellipse((cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10), outline=GOLD + (255,), width=5)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255), outline=GOLD + (255,), width=6)
    crest = Image.open(os.path.join(ROOT, "img", "crest-320.png")).convert("RGBA")
    ch = 160
    crest = crest.resize((round(crest.width * ch / crest.height), ch), Image.LANCZOS)
    card.alpha_composite(crest, (cx - crest.width // 2, cy - ch // 2 - 2))

    def font(path, size, var=None):
        f = ImageFont.truetype(path, size)
        if var:
            f.set_variation_by_name(var)
        return f

    def centred(text, f, y, fill, spacing=0):
        if spacing:
            widths = [d.textlength(c, font=f) for c in text]
            total = sum(widths) + spacing * (len(text) - 1)
            x = (W - total) / 2
            for c, w in zip(text, widths):
                d.text((x, y), c, font=f, fill=fill)
                x += w + spacing
        else:
            d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)

    d = ImageDraw.Draw(card)
    centred("TEAM UNIVERSITY", font(rc_path, 86, b"Bold"), 300, (255, 255, 255), spacing=3)
    centred("EMPOWER FOR GENERATIONS", font(rc_path, 30, b"SemiBold"), 400, (255, 205, 79), spacing=6)
    centred("Mengo, Kampala  ·  Six faculties and schools  ·  Day, evening, weekend and distance",
            font(pop_path, 23), 463, (235, 241, 250))
    centred("Applications open for the February 2027 intake",
            font(rc_path, 30, b"Bold"), 514, (255, 255, 255))

    # The ribbon along the bottom edge, in the crest colours.
    rib = Image.new("RGBA", (W + 60, 22), (255, 255, 255, 255))
    rd = ImageDraw.Draw(rib)
    x, k = -40, 0
    while x < W + 60:
        col = (BLUE, GOLD, GREEN)[k % 3]
        rd.polygon([(x + 15, 0), (x + 23, 0), (x + 8, 22), (x, 22)], fill=col + (255,))
        x += 11
        k += 1
    card.alpha_composite(rib.crop((0, 0, W, 22)), (0, H - 22))

    out = os.path.join(ROOT, "img", "og-share.jpg")
    card.convert("RGB").save(out, "JPEG", quality=84, optimize=True, progressive=True)
    print(out, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    main(*sys.argv[1:4])
