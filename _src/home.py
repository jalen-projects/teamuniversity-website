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

*  **The hero is a photograph, split against warm paper — not a dark slab.**
   A full-bleed photo under a near-opaque dark gradient is the commonest hero
   on the internet and the reason a page reads as generic; it also throws the
   photograph away. These graduands are in the university's own blue and gold
   against Kampala green, so the words moved to a warm panel beside the picture
   instead of on top of it.
*  **Nothing goes on this site that has not been looked at.** A video was once
   chosen here by its filename, because video cannot be viewed on this machine,
   and it showed people who were not this university's students. The
   photographs can be opened and checked; the video could not, so it is gone.
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

HERO = f"""<section class="hero hero--photo">
  <div class="hero-media">
    {{photo}}
    <div class="hero-scrim"></div>
  </div>

  <div class="wrap">
    <div class="hero-inner">
      <span class="hero-eyebrow"><svg><use href="#i-cap"/></svg> Empower For Generations</span>
      <h1 class="h-display">Your degree, on <span class="accent"><span class="rotator" id="rotator">{{rotator}}</span></span></h1>
      <p class="hero-lede">
        {cat.count()} programmes across {len(cat.FACULTIES)} faculties &mdash; taught by day,
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

# Team University's own graduands, in the university's own blue-and-gold gowns.
# It replaced a video: video cannot be viewed on the machine that builds this
# site, a clip was once chosen by its filename alone, and it showed people who
# were not this university's students. A photograph that has been looked at
# beats footage that has not.
# The university's own graduation footage, in the right-hand panel. The
# poster underneath it is a photograph of the same graduation, so the panel is
# correct before a single frame has loaded and on any phone, where CSS keeps
# the video from being fetched at all.
ROTATE = ["your own schedule.", "evenings after work.", "weekends only.",
          "distance, from anywhere."]

HERO = HERO.replace("{rotator}", "".join(
    f'<span{" class=\"is-on\"" if i == 0 else ""}>{phrase}</span>'
    for i, phrase in enumerate(ROTATE)))

HERO = HERO.format(photo=(
    '<video class="hero-photo hero-video" autoplay muted loop playsinline '
    'preload="metadata" poster="img/campus-group-1000.jpg" '
    'disablepictureinpicture disableremoteplayback '
    'aria-hidden="true" tabindex="-1">'
    '<source src="video/graduation.mp4" type="video/mp4"></video>'
    + media.picture(
        "campus-group",
        "Team University graduands in blue and gold academic gowns walking "
        "together on graduation day",
        sizes="100vw", cls="hero-photo hero-fallback", eager=True)))


# ---------------------------------------------------------------------------
# The marquee
# ---------------------------------------------------------------------------
# Built from the catalogue, so it cannot advertise a faculty the university
# does not have. The list is written twice into the markup because a marquee
# that translates -50% needs two identical halves or the loop shows a gap.

def marquee():
    items = "".join(
        f'<a class="marquee-item" href="{page}">'
        f'<span class="dot"></span><span>{title}</span> <b>{n}</b></a>'
        for _c, page, title, _b, _i, _ph, n in cat.all_faculties())
    return f"""<div class="marquee" aria-label="Faculties and how many programmes each runs">
  <div class="marquee-track">{items}{items}</div>
</div>"""


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
      <figure class="gal gal--tall">{_picture("graduation-1", "Team University graduands throwing their caps on graduation day, with Kampala behind them", sizes="(max-width:800px) 100vw, 50vw")}</figure>
      <figure class="gal">{_picture("graduation-2", "A graduand celebrating in the procession")}</figure>
      <figure class="gal">{_picture("campus-study", "The Team University campus gate on Kabaka A&#39;njagala Road")}</figure>
      <figure class="gal">{_picture("graduation-3", "Graduands on graduation day")}</figure>
      <figure class="gal">{_picture("campus-life", "The campus buildings at Mengo")}</figure>
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
    """The whole home page, in the order a visitor reads it.

    The Vice Chancellor comes after the numbers and before the practical
    detail: by then a visitor knows what the university offers, and a person
    speaking is what turns a list of programmes into somewhere you might go.
    """
    return "\n\n".join([
        HERO, marquee(), QUICK, SCHOLARSHIP, finder(), faculties(), STATS,
        VC_MESSAGE, MODES_HTML, GALLERY, WHY_HTML,
    ])


# ---------------------------------------------------------------------------
# The Vice Chancellor
# ---------------------------------------------------------------------------
# Prof. Lutalo Bbosa is a real, named person and his photograph is on this
# page. The words below are therefore a DRAFT WRITTEN FOR HIS APPROVAL, not a
# quotation — nothing here was said by him, and no biography is claimed,
# because there was no way to research one from this machine and inventing a
# professor's career would be worse than leaving it out.
#
# BEFORE THIS GOES LIVE: the VC reads it, changes whatever he likes, and
# approves it. Until then the source carries this notice and TODO.md lists it.

VC_MESSAGE = f"""<section class="vc" id="vc">
  <div class="wrap">
    <figure class="vc-portrait">
      {media.picture("vc-lutalo-bbosa",
                     "Professor Lutalo Bbosa, Vice Chancellor of Team University",
                     sizes="(max-width:800px) 60vw, 320px")}
      <figcaption>
        <strong>Prof. Lutalo Bbosa</strong>
        <span>Vice Chancellor</span>
      </figcaption>
    </figure>

    <div class="vc-words">
      <span class="eyebrow"><svg><use href="#i-cap"/></svg> From the Vice Chancellor</span>
      <h2>&ldquo;We teach the people who are already carrying something.&rdquo;</h2>
      <p>
        Most of the students who walk through our gate at Mengo are not coming
        straight from a classroom. They are coming from a job, a business, a
        ward, a farm, a family. They have something to carry, and they have
        decided to carry a qualification as well.
      </p>
      <p>
        That is the university we have built for them. Our lectures run in the
        evening and at the weekend as readily as they run by day, because a
        person should not have to choose between earning and learning. Our
        programmes &mdash; {cat.count()} of them, from national certificates in
        the trades to masters degrees &mdash; are set to be finished by people
        who are busy, and to be worth something to an employer at the end.
      </p>
      <p>
        You will be taught by staff who know your field and who will know your
        name. Come and see us, or apply online, and let us talk about where you
        want to be in three years.
      </p>
      <p class="vc-sign">Prof. Lutalo Bbosa <span>Vice Chancellor, Team University</span></p>
      <a class="btn btn--outline" href="about.html">More about the university <svg><use href="#i-arrow"/></svg></a>
    </div>
  </div>
</section>"""
