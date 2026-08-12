"""
THE HOME PAGE
=============
Rebuilt to carry the whole university rather than a quarter of it.

What a Ugandan applicant actually does on a university home page, in order:
work out whether the course they want is taught here, work out what it costs
and when the intake closes, and then find the button that starts an
application. Everything above the fold serves those three, and the programme
finder is deliberately the first thing after the hero — 99 programmes is a
strength only if a visitor can get to theirs in one search.

Design notes, since the brief was "better than KIU and King Ceasor":

*  **The hero is video, and that is a decision about the photographs.** The
   university's own stills are 550–1000px — fine in a card, soft blown up to a
   2000px banner. The graduation footage is the one asset that fills a screen
   without falling apart, so it carries the hero and the photographs are used
   where they stay sharp.
*  **The scholarship is a band, not a badge.** A 50% scholarship is the single
   most persuasive fact the university has this August, and burying it in a
   news list wastes it.
*  **Counts are real or absent.** 99 programmes, 6 faculties, 3 intakes, 4
   study modes — every one of those is checkable against the registry. No
   invented student numbers, no invented founding year, no testimonials from
   students who never said anything.
"""

import json

import catalogue as cat
from build import APPLY, PORTAL, ELEARN, ELIB


import media


def _picture(stem, alt, widths=None, sizes="(max-width:800px) 100vw, 33vw",
             cls="", loading="lazy"):
    """A responsive photograph, built from the widths that exist on disk.

    `widths` is ignored and kept only so old call sites do not break: guessing
    widths is precisely what put thirty broken images on the site.
    """
    return media.picture(stem, alt, sizes=sizes, cls=cls)


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

HERO = f"""<section class="hero hero--video">
  <div class="hero-media">
    {{comment}}
    <video class="hero-video" autoplay muted loop playsinline preload="metadata"
           poster="img/graduation-1-640.jpg"
           aria-hidden="true" tabindex="-1">
      <source src="video/graduation.mp4" type="video/mp4">
    </video>
    <div class="hero-scrim"></div>
  </div>

  <div class="wrap">
    <div class="hero-inner">
      <span class="hero-eyebrow"><svg><use href="#i-cap"/></svg> Empower For Generations</span>
      <h1 class="h-display">Your degree, on <span class="accent">your own schedule</span>.</h1>
      <p class="hero-lede">
        {cat.count()} programmes across {len(cat.FACULTIES)} faculties — taught by day,
        in the evening, at weekends and by distance, in the middle of Kampala.
      </p>
      <div class="hero-actions">
        <a class="btn btn--primary btn--lg" href="{APPLY}">Apply for August <svg><use href="#i-arrow"/></svg></a>
        <a class="btn btn--glass btn--lg" href="#finder">Find your programme</a>
      </div>
      <p class="hero-note">
        <svg><use href="#i-spark"/></svg>
        <strong>50% scholarships</strong> available on selected programmes this August intake.
      </p>
    </div>
  </div>

  <a class="hero-scroll" href="#quick" aria-label="Scroll to the next section">
    <span></span>
  </a>
</section>"""

HERO = HERO.format(comment="""<!-- Muted and looping so it may autoplay at all, and
         preload="metadata" because preload="none" leaves some browsers
         refusing to start it. CSS hides the video below 700px and shows the
         poster instead, so a phone on mobile data never fetches 2.4 MB of
         decoration it did not ask for. -->""")


# ---------------------------------------------------------------------------
# Quick links — the five things people come here to do
# ---------------------------------------------------------------------------

QUICK_ITEMS = [
    ("i-cap", "Apply online", "August intake open", APPLY),
    ("i-search", "Programme finder", f"All {cat.count()} programmes", "#finder"),
    ("i-money", "Fees and funding", "Scholarships and payment", "admissions.html#fees"),
    ("i-laptop", "Student portal", "Results, registration", PORTAL),
    ("i-books", "E-Library", "Journals and books", ELIB),
]

QUICK = """<section class="quick" id="quick">
  <div class="wrap">
    <div class="quick-grid">
      {items}
    </div>
  </div>
</section>""".format(items="\n      ".join(
    f'<a class="quick-card" href="{href}">'
    f'<span class="quick-ico"><svg><use href="#{icon}"/></svg></span>'
    f'<span><strong>{title}</strong><small>{note}</small></span>'
    f'<svg class="quick-arrow"><use href="#i-arrow"/></svg></a>'
    for icon, title, note, href in QUICK_ITEMS))


# ---------------------------------------------------------------------------
# The scholarship campaign
# ---------------------------------------------------------------------------

SCHOLARSHIP = f"""<section class="scholar">
  <div class="wrap">
    <div class="scholar-body">
      <span class="pill pill--gold"><svg><use href="#i-spark"/></svg> August 2026 intake</span>
      <h2>Up to <span class="big">50%</span> scholarship on selected programmes.</h2>
      <p>
        Team University is offering half-fee scholarships on selected programmes for
        the August 2026 intake. Places are limited and awarded on academic merit and
        need. Talk to the admissions office about which programmes are covered and
        what your application needs to show.
      </p>
      <div class="scholar-actions">
        <a class="btn btn--gold btn--lg" href="{APPLY}">Start an application</a>
        <a class="btn btn--outline" href="contact.html">Ask about the scholarship</a>
      </div>
    </div>
    <div class="scholar-art" aria-hidden="true">
      <div class="scholar-ring"><span>50<small>%</small></span></div>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Programme finder — the whole catalogue, searchable
# ---------------------------------------------------------------------------

def finder():
    index = json.dumps(cat.search_index(), separators=(",", ":"), ensure_ascii=False)
    levels = "".join(
        f'<button type="button" class="chip" data-level="{label}">{label}</button>'
        for _code, label in cat.LEVELS)
    faculties = "".join(
        f'<option value="{title}">{title}</option>'
        for _c, _p, title, _b, _i, _ph, _n in cat.all_faculties())
    return f"""<section class="finder" id="finder">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow"><svg><use href="#i-search"/></svg> Programme finder</span>
      <h2>Every one of our {cat.count()} programmes, in one search.</h2>
      <p>Type a subject — accounting, nursing, software, tailoring — or filter by
         the award you want. Results are the university's own catalogue.</p>
    </div>

    <div class="finder-controls">
      <div class="finder-search">
        <svg><use href="#i-search"/></svg>
        <input type="search" id="progSearch" placeholder="Search programmes…"
               autocomplete="off" aria-label="Search programmes">
      </div>
      <select id="progFaculty" aria-label="Filter by faculty">
        <option value="">All faculties</option>
        {faculties}
      </select>
    </div>

    <div class="chips" id="progLevels" role="group" aria-label="Filter by award">
      <button type="button" class="chip is-on" data-level="">All awards</button>
      {levels}
    </div>

    <p class="finder-count" id="progCount" aria-live="polite"></p>
    <div class="finder-results" id="progResults"></div>
    <p class="finder-more">
      Not sure which to choose? <a href="contact.html">Talk to an admissions officer</a>
      — they will match your grades and your schedule to a programme.
    </p>
  </div>
</section>

<script id="progData" type="application/json">{index}</script>"""


# ---------------------------------------------------------------------------
# Faculties
# ---------------------------------------------------------------------------

def faculties():
    cards = []
    for _code, page, title, blurb, icon, photo, n in cat.all_faculties():
        cards.append(f"""<a class="fac-card" href="{page}">
        <div class="fac-photo">{_picture(photo, "", cls="", loading="lazy")}
          <span class="fac-ico"><svg><use href="#{icon}"/></svg></span>
        </div>
        <div class="fac-body">
          <span class="fac-count">{n} programmes</span>
          <h3>{title}</h3>
          <p>{blurb}</p>
          <span class="fac-link">Explore the faculty <svg><use href="#i-arrow"/></svg></span>
        </div>
      </a>""")
    return f"""<section class="faculties" id="faculties">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow"><svg><use href="#i-buildings"/></svg> Faculties</span>
        <h2>Six faculties. One campus in Mengo.</h2>
      </div>
      <a class="btn btn--outline" href="academics.html">All academics <svg><use href="#i-arrow"/></svg></a>
    </div>
    <div class="fac-grid">
      {"".join(cards)}
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# The numbers — every one checkable
# ---------------------------------------------------------------------------

STATS = f"""<section class="stats">
  <div class="wrap">
    <div class="stat"><span class="stat-n" data-count="{cat.count()}">0</span><span class="stat-l">Programmes on offer</span></div>
    <div class="stat"><span class="stat-n" data-count="{len(cat.FACULTIES)}">0</span><span class="stat-l">Faculties and schools</span></div>
    <div class="stat"><span class="stat-n" data-count="4">0</span><span class="stat-l">Study modes</span></div>
    <div class="stat"><span class="stat-n" data-count="3">0</span><span class="stat-l">Intakes a year</span></div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Study modes
# ---------------------------------------------------------------------------

MODES = [
    ("i-clock", "Day", "Weekday classes for full-time students straight from A-level or a diploma."),
    ("i-buildings", "Evening", "After-work classes in town, for people holding down a job."),
    ("i-calendar", "Weekend", "Friday to Sunday, so a working week stays intact."),
    ("i-globe", "Distance", "Study from anywhere in Uganda, with materials and support online."),
]

MODES_HTML = """<section class="modes" id="modes">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow"><svg><use href="#i-clock"/></svg> Study modes</span>
      <h2>Built for people who are already busy.</h2>
      <p>Most of our students are working, raising families, or both. Every faculty
         runs more than one schedule so that a job is not a reason to stop studying.</p>
    </div>
    <div class="mode-grid">
      {items}
    </div>
  </div>
</section>""".format(items="\n      ".join(
    f'<div class="mode-card"><span class="mode-ico"><svg><use href="#{icon}"/></svg></span>'
    f'<h3>{title}</h3><p>{text}</p></div>'
    for icon, title, text in MODES))


# ---------------------------------------------------------------------------
# Campus life — the photographs, where they stay sharp
# ---------------------------------------------------------------------------

GALLERY = f"""<section class="gallery">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow"><svg><use href="#i-buildings"/></svg> Campus life</span>
        <h2>Mengo, Kampala — five minutes from the city.</h2>
      </div>
      <a class="btn btn--outline" href="student-life.html">Student life <svg><use href="#i-arrow"/></svg></a>
    </div>
    <div class="gal-grid">
      <figure class="gal gal--tall">{_picture("campus-life", "Team University students on campus", sizes="(max-width:800px) 100vw, 50vw")}</figure>
      <figure class="gal">{_picture("campus-group", "Students together between lectures")}</figure>
      <figure class="gal">{_picture("graduation-3", "Graduands on graduation day")}</figure>
      <figure class="gal">{_picture("campus-study", "Students studying")}</figure>
      <figure class="gal">{_picture("technology", "Computing and technology at Team University")}</figure>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Why Team
# ---------------------------------------------------------------------------

WHY = [
    ("i-check", "Recognised awards",
     "Degrees and diplomas awarded by Team University, and vocational awards "
     "assessed by the national boards — so what you earn is registered where "
     "it counts."),
    ("i-laptop", "A student portal that works",
     "Registration, results, transcripts and fees statements online, with your "
     "own login from the day you are admitted."),
    ("i-clock", "A schedule that fits your job",
     "Day, evening, weekend and distance — and you can ask to change mode "
     "between semesters if your work changes."),
    ("i-pin", "In the middle of Kampala",
     "Wood House Mengo, on Kabaka A'njagala Road — reachable from anywhere in "
     "the city, and close to where our students already live and work."),
]

WHY_HTML = """<section class="why">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow"><svg><use href="#i-spark"/></svg> Why Team</span>
      <h2>What you get, beyond the certificate.</h2>
    </div>
    <div class="why-grid">
      {items}
    </div>
  </div>
</section>""".format(items="\n      ".join(
    f'<div class="why-card"><span class="why-ico"><svg><use href="#{icon}"/></svg></span>'
    f'<h3>{title}</h3><p>{text}</p></div>'
    for icon, title, text in WHY))


def body():
    """The whole home page, in the order a visitor reads it."""
    return "\n\n".join([
        HERO, QUICK, SCHOLARSHIP, finder(), faculties(), STATS,
        MODES_HTML, GALLERY, WHY_HTML,
    ])
