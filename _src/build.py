#!/usr/bin/env python3
"""
Team University site builder.

Writes the plain .html files in the project root from one shared shell, so the
navigation, footer and head never drift apart across eleven pages. There is no
framework and nothing to install: run it with any Python 3.

    python _src/build.py

The generated .html files are what you upload. This script does not need to go
on the server.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Where the site is actually served. Link previews (WhatsApp, Facebook) fetch
# the thumbnail from here, so it MUST be the live address: when the site moves
# to teamuniversity.ac.ug, change this one line and rebuild.
SITE = "https://jalen-projects.github.io/teamuniversity-website"
OG_IMAGE = "img/og-share.jpg"   # 1200x630, made by build_share.py; rename it when it changes
import shell
from shell import PORTAL, APPLY, ELEARN, ELIB

# --------------------------------------------------------------------------
# Icon sprite (Phosphor Icons, MIT). Inlined so pages make no outside request.
# --------------------------------------------------------------------------
SPRITE = (ROOT / "_src" / "sprite.svg").read_text(encoding="utf-8")

ACADEMICS = [
    ("academics.html", "All faculties", "Programmes, study modes and the academic year"),
    ("programmes.html", "Every programme", "Search all 99 across the six faculties"),
    ("faculty-graduate.html", "Graduate Studies", "Masters and postgraduate diplomas"),
    ("faculty-business.html", "Management and Humanities", "Business, accounting, procurement, economics"),
    ("faculty-applied.html", "Applied Science and Technology", "Computing, IT, environment, agriculture"),
    ("faculty-health.html", "Health Sciences", "Clinical, nursing and public health"),
    ("faculty-education.html", "Education", "Training teachers for the new curriculum"),
    ("faculty-tvet.html", "Vocational and Technical", "Trades, assessed by the national boards"),
]


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{site}/{page}">
<meta name="theme-color" content="#0b55a6">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Team University">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{site}/{og_image}">
<meta property="og:image:secure_url" content="{site}/{og_image}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Team University crest over graduands celebrating, with the motto Empower for Generations">
<meta property="og:locale" content="en_UG">
<meta property="og:url" content="{site}/{page}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@TeamUniversityU">
<meta name="twitter:image" content="{site}/{og_image}">

<link rel="icon" href="img/crest-160.png" type="image/png">
<link rel="apple-touch-icon" href="img/crest-320.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Team University">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Roboto+Condensed:wght@400;500;700&display=swap">
{preload}<link rel="stylesheet" href="css/main.css">
{styles}
{jsonld}</head>
<body>

<a class="skip" href="#main">Skip to main content</a>

{sprite}

{topbar}

{masthead}

<main id="main">
{body}
</main>

{footer}

{tabbar}
<script src="js/site.js" defer></script>
{scripts}</body>
</html>
"""


def banner(title, lede, crumbs, image="campus", alt=""):
    """Inner-page header: photograph, breadcrumb, title, one line of context."""
    trail = ['<a href="index.html">Home</a>']
    for label, href in crumbs[:-1]:
        trail.append('<svg><use href="#i-chevron"/></svg>')
        trail.append(f'<a href="{href}">{label}</a>')
    trail.append('<svg><use href="#i-chevron"/></svg>')
    trail.append(f'<span aria-current="page">{crumbs[-1][0]}</span>')
    import media
    return f"""<section class="banner">
  {media.picture(image, alt, sizes="100vw", cls="banner-img", eager=True)}
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{''.join(trail)}</nav>
    <h1>{title}</h1>
    <p>{lede}</p>
  </div>
</section>"""


def sidenav(heading, links):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"true\"" if cur else ""}>{t}</a></li>'
        for h, t, cur in links
    )
    return f'<nav class="sidenav" aria-label="{heading}"><h2>{heading}</h2><ul>{items}</ul></nav>'


def related(items):
    li = "".join(
        f'<li><a href="{h}">{t}<svg><use href="#i-arrow"/></svg></a></li>' for h, t in items
    )
    return f'<div class="related"><h2>Where to next</h2><ul>{li}</ul></div>'


def page_body(banner_html, side, content, rel=""):
    return f"""{banner_html}

<div class="page">
  <div class="wrap">
    {side}
    <div>
      <div class="prose">
{content}
      </div>
      {rel}
    </div>
  </div>
</div>"""


# Faculty sub-navigation reused on the five academics pages.
def academics_side(current):
    return sidenav("Academics", [(h, t, h == current) for h, t, _ in ACADEMICS])


CTA_BAND = f"""<section class="cta">
  <div class="wrap">
    <div>
      <h2>Applications are open for the February 2027 intake.</h2>
      <p>Apply online, or collect an application form at the Mengo campus. Our admissions office will walk you through entry requirements, fees and your study schedule.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn--primary" href="{APPLY}">Apply now <svg><use href="#i-arrow"/></svg></a>
      <a class="btn btn--ghost" href="contact.html">Talk to admissions</a>
    </div>
  </div>
</section>"""


# The phone's tab bar. Four destinations, and it is the same four on every
# page so a thumb learns where they are. Rendered for every page rather than
# only the home page, because an app-like bar that disappears on the second
# screen is worse than none at all.
TABBAR = """<nav class="tabbar" aria-label="Quick navigation">
  <a href="index.html"{home}><svg><use href="#i-buildings"/></svg>Home</a>
  <a href="programmes.html"{prog}><svg><use href="#i-search"/></svg>Programmes</a>
  <a class="tab-apply" href="{apply}"><svg><use href="#i-cap"/></svg>Apply</a>
  <a href="contact.html"{contact}><svg><use href="#i-phone"/></svg>Contact</a>
</nav>"""


def tabbar_html(current):
    mark = ' class="is-on"'
    return TABBAR.format(
        home=mark if current == "index.html" else "",
        prog=mark if current == "programmes.html" else "",
        contact=mark if current == "contact.html" else "",
        apply=APPLY)


def render():
    import pages
    written = []
    for name, spec in pages.PAGES.items():
        html = SHELL.format(
            title=spec["title"],
            og_title=spec.get("og_title", spec["title"]),
            description=spec["description"],
            page="" if name == "index.html" else name,
            site=SITE,
            og_image=OG_IMAGE,
            sprite=SPRITE.strip(),
            topbar=shell.topbar(),
            masthead=shell.masthead(name),
            footer=shell.footer(),
            body=spec["body"],
            preload=spec.get("preload", ""),
            jsonld=spec.get("jsonld", ""),
            tabbar=tabbar_html(name),
            styles=spec.get("styles", ""),
            scripts=spec.get("scripts", ""),
        )
        (ROOT / name).write_text(html, encoding="utf-8")
        written.append((name, len(html)))
    return written


if __name__ == "__main__":
    for name, size in render():
        print(f"  {name:26} {size/1024:6.1f} KB")
    print(f"\n{len(pathlib.Path(ROOT).glob('*.html') and list(ROOT.glob('*.html')))} pages written to {ROOT}")
