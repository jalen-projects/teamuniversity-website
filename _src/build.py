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

SITE = "https://teamuniversity.ac.ug"
PORTAL = "https://team.campusnect.com/portal/login/"
APPLY = "https://team.campusnect.com/apply/"
ELEARN = "https://elearning.teamuniversity.ac.ug"
ELIB = "https://libraris.teamuniversity.ac.ug"

# --------------------------------------------------------------------------
# Icon sprite (Phosphor Icons, MIT). Inlined so pages make no outside request.
# --------------------------------------------------------------------------
SPRITE = (ROOT / "_src" / "sprite.svg").read_text(encoding="utf-8")

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("__academics__", "Academics"),
    ("admissions.html", "Admissions"),
    ("student-life.html", "Student Life"),
    ("news.html", "News"),
    ("contact.html", "Contact"),
]

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


def nav_html(current):
    out = []
    for href, label in NAV:
        if href == "__academics__":
            # Marks the section as current WITHOUT opening the menu on load.
            here = " is-section" if current in [p for p, _, _ in ACADEMICS] else ""
            items = "".join(
                f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}'
                f"<small>{d}</small></a>"
                for h, t, d in ACADEMICS
            )
            out.append(
                f'<div class="nav-item{here}" data-dropdown>'
                f'<button type="button" aria-expanded="false">Academics'
                f'<svg><use href="#i-caret"/></svg></button>'
                f'<div class="submenu">{items}</div></div>'
            )
        else:
            cur = ' aria-current="page"' if href == current else ""
            out.append(f'<a href="{href}"{cur}>{label}</a>')
    out.append(f'<a class="btn btn--primary" href="{APPLY}">Apply now</a>')
    return "\n      ".join(out)


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{site}/{page}">
<meta name="theme-color" content="#0b3350">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Team University">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{site}/img/grad-1020.jpg">
<meta property="og:url" content="{site}/{page}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@TeamUniversityU">

<link rel="icon" href="img/crest.png" type="image/png">
<link rel="apple-touch-icon" href="img/crest.png">
<link rel="preload" href="fonts/outfit-var-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="css/site.css">
<link rel="stylesheet" href="css/pages.css">
{styles}
{jsonld}</head>
<body>

<a class="skip" href="#main">Skip to main content</a>

{sprite}

<div class="utility">
  <div class="wrap">
    <div class="utility-contacts">
      <span><svg><use href="#i-phone"/></svg> +256 782 752226</span>
      <span><svg><use href="#i-mail"/></svg> info@teamuniversity.ac.ug</span>
    </div>
    <nav class="utility-links" aria-label="Quick links">
      <a href="{elib}">E-Library</a>
      <a href="{elearn}">E-Learning</a>
      <a href="{portal}">Student Portal</a>
    </nav>
  </div>
</div>

<header class="masthead" id="masthead">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="img/crest-96.png" alt="Team University crest" width="42" height="42">
      <span>
        <span class="brand-name">Team University</span>
        <span class="brand-sub">Kampala, Uganda</span>
      </span>
    </a>

    <nav class="nav" id="nav" aria-label="Main">
      {nav}
    </nav>

    <div class="masthead-actions">
      <a class="btn btn--primary" href="{apply}">Apply now</a>
      <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="nav" aria-label="Open menu">
        <svg id="navIcon"><use href="#i-menu"/></svg>
      </button>
    </div>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="foot" id="contact-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="foot-brand">
          <img src="img/crest-96.png" alt="" width="48" height="48">
          <span>
            <strong>Team University</strong>
            <span>Empower For Generations</span>
          </span>
        </div>
        <p style="max-width:34ch">A Kampala university offering 99 programmes across six faculties — day, evening, weekend and distance.</p>
        <div class="socials">
          <a href="https://www.facebook.com/teamuniversitykampala" aria-label="Team University on Facebook"><svg><use href="#i-facebook"/></svg></a>
          <a href="https://twitter.com/TeamUniversityU" aria-label="Team University on X"><svg><use href="#i-x"/></svg></a>
          <a href="https://www.youtube.com/@teamuniversity" aria-label="Team University on YouTube"><svg><use href="#i-youtube"/></svg></a>
        </div>
      </div>

      <div>
        <h3>Study</h3>
        <ul>
          <li><a href="academics.html">Faculties and programmes</a></li>
          <li><a href="programmes.html">Every programme</a></li>
          <li><a href="admissions.html">How to apply</a></li>
          <li><a href="admissions.html#requirements">Entry requirements</a></li>
          <li><a href="academics.html#modes">Study modes</a></li>
        </ul>
      </div>

      <div>
        <h3>Campus</h3>
        <ul>
          <li><a href="{portal}">Student Portal</a></li>
          <li><a href="{elearn}">E-Learning</a></li>
          <li><a href="{elib}">E-Library</a></li>
          <li><a href="student-life.html">Student life</a></li>
          <li><a href="news.html">News and events</a></li>
        </ul>
      </div>

      <div>
        <h3>Contact</h3>
        <ul class="foot-contact">
          <li><svg><use href="#i-pin"/></svg><span>Wood House Mengo, Plot 446<br>Kabaka A'njagala Road<br>Mengo-Rubaga, Kampala</span></li>
          <li><svg><use href="#i-phone"/></svg><span><a href="tel:+256782752226">+256 782 752226</a><br><a href="tel:+256704310224">+256 704 310224</a></span></li>
          <li><svg><use href="#i-mail"/></svg><a href="mailto:info@teamuniversity.ac.ug">info@teamuniversity.ac.ug</a></li>
        </ul>
      </div>
    </div>

    <div class="foot-base">
      <span>&copy; <span id="year">2026</span> Team University, Kampala. All rights reserved.</span>
      <span>Student system powered by CampusNect</span>
    </div>
  </div>
</footer>

<script src="js/site.js" defer></script>
{scripts}</body>
</html>
"""


def banner(title, lede, crumbs, image="campus", alt=""):
    """Inner-page header: photograph, breadcrumb, title, one line of context."""
    trail = ['<a href="index.html">Home</a>']
    for label, href in crumbs[:-1]:
        trail.append('<svg><use href="#i-caret"/></svg>')
        trail.append(f'<a href="{href}">{label}</a>')
    trail.append('<svg><use href="#i-caret"/></svg>')
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
      <h2>The August 2026 intake is open.</h2>
      <p>Apply online, or collect an application form at the Mengo campus. Our admissions office will walk you through entry requirements, fees and your study schedule.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn--primary" href="{APPLY}">Apply now <svg><use href="#i-arrow"/></svg></a>
      <a class="btn btn--ghost" href="contact.html">Talk to admissions</a>
    </div>
  </div>
</section>"""


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
            sprite=SPRITE.strip(),
            nav=nav_html(name),
            body=spec["body"],
            preload=spec.get("preload", ""),
            jsonld=spec.get("jsonld", ""),
            styles=spec.get("styles", ""),
            scripts=spec.get("scripts", ""),
            apply=APPLY,
            portal=PORTAL,
            elearn=ELEARN,
            elib=ELIB,
        )
        (ROOT / name).write_text(html, encoding="utf-8")
        written.append((name, len(html)))
    return written


if __name__ == "__main__":
    for name, size in render():
        print(f"  {name:26} {size/1024:6.1f} KB")
    print(f"\n{len(pathlib.Path(ROOT).glob('*.html') and list(ROOT.glob('*.html')))} pages written to {ROOT}")
