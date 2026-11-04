"""
THE HOME PAGE (Nov 2026 redesign)
=================================
Built in the order Ugandan university home pages are read — the order the
university's own staff pointed to on kab.ac.ug:

  1. photo slider with a caption plate        (what is happening at TEAM now)
  2. programme finder  +  notice board        (the two things visitors come for)
  3. faculties band                           (what can I study)
  4. what makes TEAM unique + figures         (why here)
  5. university news                          (proof of life)
  6. upcoming events                          (what is next)
  7. study modes                              (how — day / evening / weekend / ODeL)
  8. gallery                                  (campus life)
  9. regulators and partners                  (trust)

EVERY FACT HERE HAS A SOURCE. Notices, news and events come from the
university's own material: the 15th graduation book (Nov 2025), the
convocation and conference pages of teamuniversity.ac.ug (2026), and the
registry catalogue. The live site the university replaced carried invented
stories (a Lancet paper, a hackathon, a hospital partnership); none of those
are repeated here. Keep it that way — a notice board that lies is worse than
an empty one.

All photographs are the university's own, from the teamuniversity.ac.ug media
library (2560px originals; see build_media.py).
"""

import json

import catalogue as cat
import media
from shell import APPLY, PORTAL, ELEARN, ELIB


def pic(stem, alt, sizes="100vw", eager=False):
    return media.picture(stem, alt, sizes=sizes, eager=eager)


# ---------------------------------------------------------------- 1. HERO --
SLIDES = [
    ("hero-graduands", "Team University graduands celebrating on graduation day",
     "Congratulations to our graduands &mdash; the 16th Graduation Ceremony, held under the theme "
     "&ldquo;Competency-Based Education and Training for Transformative Education.&rdquo;",
     "news.html#graduation-16", "Read more"),
    ("building-sky", "The Team University building at Wood House, Mengo, under a blue sky",
     "Our campus at Wood House, Mengo &mdash; on Kabaka A&rsquo;njagala Road, a short ride from Kampala city centre.",
     "contact.html#find", "Find us"),
    ("ceremony-mace", "The university mace carried in the graduation procession",
     "Applications are open for the February 2027 intake &mdash; study by day, in the evening, at weekends or by distance.",
     APPLY, "Apply Online"),
    ("grads-walk", "Four Team University graduates walking together in their gowns",
     "Twenty-five years of TEAM &mdash; the Silver Jubilee and the launch of the Team University Alumni Association.",
     "news.html#jubilee", "Read the story"),
    ("procession", "Guests and academic staff in procession at a Team University ceremony",
     "International Conference on AI and the Transformation of Education Systems &mdash; 10 and 11 December 2026.",
     "research.html#conference", "Conference details"),
]


TONES = ["blue", "green", "navy"]   # the caption plate changes colour with each photo


def hero():
    slides = "".join(
        f'<div class="slide{" is-on" if i == 0 else ""}">{pic(stem, alt, eager=(i == 0))}</div>'
        for i, (stem, alt, *_r) in enumerate(SLIDES))
    caps = "".join(
        f'<p class="cap{" is-on" if i == 0 else ""}">{text} <a href="{href}">{link}</a></p>'
        for i, (_s, _a, text, href, link) in enumerate(SLIDES))
    dots = "".join(
        f'<button type="button" aria-label="Show slide {i + 1}"{" class=\"is-on\"" if i == 0 else ""}></button>'
        for i in range(len(SLIDES)))
    total = f"{len(SLIDES):02d}"
    return f"""<section class="hero" id="hero" data-tone="{TONES[0]}" aria-roledescription="carousel" aria-label="Team University highlights">
  <div class="hero-track">{slides}
    <div class="hero-wipe" aria-hidden="true"><i></i><i></i><i></i></div>
  </div>
  <button class="hero-arrow hero-arrow--prev" type="button" aria-label="Previous slide"><svg><use href="#i-chevron"/></svg></button>
  <button class="hero-arrow hero-arrow--next" type="button" aria-label="Next slide"><svg><use href="#i-chevron"/></svg></button>
  <div class="hero-nav"><span class="hero-count"><b id="heroNow">01</b> / {total}</span><div class="hero-dots">{dots}</div></div>
  <div class="hero-cap" aria-live="polite">{caps}</div>
  <div class="hero-ribbon" aria-hidden="true"><i></i></div>
</section>"""


# ------------------------------------------------ 2. FINDER + NOTICE BOARD --
NOTICES = [
    # (day, month, open?, category, new?, title, href, audience)
    ("OPEN", "", True, "Admissions", True,
     "Applications are open for the February 2027 intake",
     "admissions.html#intakes", "Prospective students &bull; Parents and guardians"),
    ("01", "Oct 26", False, "Call for papers", False,
     "International Conference on AI and the Transformation of Education Systems, 10&ndash;11 December 2026",
     "research.html#conference", "Researchers &bull; Academic staff &bull; Graduate students"),
    ("30", "May 26", False, "Graduation", False,
     "The 16th Graduation Ceremony of Team University",
     "news.html#graduation-16", "Graduands &bull; Parents and guardians"),
    ("21", "Nov 25", False, "Alumni", False,
     "Silver Jubilee: launch of the Team University Alumni Association",
     "news.html#jubilee", "Alumni &bull; Convocation"),
]


def notice_board():
    rows = []
    for day, mon, is_open, catg, new, title, href, who in NOTICES:
        date = (f'<div class="date date--open"><b>{day}</b><span>now</span></div>' if is_open
                else f'<div class="date"><b>{day}</b><span>{mon}</span></div>')
        tag = ' <span class="tag">New</span>' if new else ""
        rows.append(f"""<article class="notice">
        {date}
        <div>
          <div class="n-cat">{catg}{tag}</div>
          <h3><a href="{href}">{title}</a></h3>
          <p class="n-for"><svg><use href="#i-users"/></svg><b>For:</b> {who}</p>
          <a class="n-read" href="{href}">Read notice <svg><use href="#i-arrow"/></svg></a>
        </div>
      </article>""")
    return "\n      ".join(rows)


def finder_and_board():
    levels = "".join(f'<option value="{label}">{label}</option>' for _c, label in cat.LEVELS)
    quick = [
        ("i-cap", "Apply online", "Start your application", APPLY),
        ("i-laptop", "Student portal", "Results, fees, registration", PORTAL),
        ("i-books", "E-Library", "Journals and past papers", ELIB),
        ("i-globe", "E-Learning", "Course materials online", ELEARN),
        ("i-money", "Fees structure", "Ask for the current fees", "admissions.html#fees"),
        ("i-calendar", "Academic calendar", "Semesters and intakes", "academics.html#calendar"),
    ]
    tiles = "".join(
        f'<a href="{h}"><svg><use href="#{i}"/></svg><span>{t}<br><small>{d}</small></span></a>'
        for i, t, d, h in quick)
    return f"""<section class="sec">
  <div class="wrap fn">
    <div>
      <div class="finder">
        <h2>Course and programme finder</h2>
        <div class="finder-grid">
          <div>
            <h3>Programmes by pathway</h3>
            <ul>
              <li><a href="faculty-graduate.html">Masters and Postgraduate Diplomas</a></li>
              <li><a href="faculty-tvet.html">UVTAB Vocational Programmes</a></li>
              <li><a href="faculty-health.html">Health Sciences Programmes</a></li>
              <li><a href="academics.html#modes">Open Distance and e-Learning (ODeL)</a></li>
              <li><a href="admissions.html#scholarships">Scholarships and bursaries</a></li>
            </ul>
          </div>
          <form action="programmes.html" method="get" role="search">
            <label class="sr" for="fLevel">Study level</label>
            <select id="fLevel" name="level">
              <option value="">- Study Level -</option>
              {levels}
            </select>
            <label class="sr" for="fQ">Programme title or keyword</label>
            <input id="fQ" name="q" type="search" placeholder="Enter Programme title or Keyword">
            <button type="submit">Search</button>
          </form>
        </div>
      </div>
      <div class="quick">{tiles}</div>
    </div>

    <div>
      <div class="kicker">Latest updates</div>
      <div class="nb-head">
        <div>
          <h2 class="title">University Notice Board</h2>
          <p>Official announcements, opportunities and academic updates from Team University.</p>
        </div>
        <a class="btn-out" href="news.html">View All Notices <svg><use href="#i-arrow"/></svg></a>
      </div>
      <div class="board">
      {notice_board()}
      </div>
    </div>
  </div>
</section>"""


# ------------------------------------------------------ 3. FACULTIES BAND --
def faculties_band():
    links = "".join(
        f'<li><a href="{page}">{title}</a></li>'
        for _c, page, title, _b, _i, _ph, _n in cat.all_faculties())
    return f"""<section class="areas">
  <div class="areas-text">
    {pic("fss-tent", "", sizes="50vw")}
    <div class="areas-inner">
      <h2>Six Faculties and Schools to Explore Your Interests</h2>
      <ul class="area-links">{links}</ul>
      <div class="btns">
        <a class="btn btn--gold" href="programmes.html">Our Programmes</a>
        <a class="btn btn--green" href="faculty-graduate.html">Graduate Studies</a>
      </div>
    </div>
  </div>
  <div class="areas-photo">{pic("building-front", "The terracotta-and-gold Team University building and its lawn", sizes="(max-width: 960px) 100vw, 50vw")}</div>
</section>"""


# -------------------------------------------------------------- 4. UNIQUE --
def unique():
    ticks = "".join(
        f'<li><svg><use href="#i-check"/></svg>{t}</li>'
        for t in ["Masters Degrees", "Bachelors Degrees", "Postgraduate Diplomas",
                  "Diplomas", "Certificates", "Vocational Awards"])
    return f"""<section class="sec unique">
  <div class="wrap">
    <div>
      <div class="u-card">{pic("graduand-carpet", "A Team University graduand on the red carpet at graduation", sizes="260px")}</div>
      <a class="link-arrow" href="programmes.html">View all programmes <svg><use href="#i-arrow"/></svg></a>
    </div>
    <div class="u-tall">{pic("student-speaker", "A Team University student addressing guests from the lectern", sizes="(max-width: 640px) 100vw, 380px")}</div>
    <div class="u-text">
      <h2>What makes TEAM Unique?</h2>
      <div class="bar bar--left"></div>
      <p>Twenty-five years of professional education in the heart of Kampala &mdash; from Team
         Business College to a university licensed by the National Council for Higher
         Education. We teach the way working people can study: by day, in the evening, at
         weekends and by distance.</p>
      <ul class="ticks">{ticks}</ul>
      <div class="counts">
        <div><strong data-count="{cat.count()}">{cat.count()}</strong><span>Programmes</span></div>
        <div><strong data-count="25">25</strong><span>Years of TEAM</span></div>
      </div>
      <a class="btn btn--gold" href="{APPLY}">Apply Online</a>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- 5. NEWS --
NEWS = [
    ("graduands-smile", "Two Team University graduates smiling in their gowns",
     "Team University holds its 16th Graduation Ceremony under the theme of competency-based education",
     "30 May 2026", "news.html#graduation-16"),
    ("conf-ai", "Call for papers poster for the AI in Education conference",
     "Call for papers: International Conference on AI and the Transformation of Education Systems",
     "1 October 2026", "research.html#conference"),
    ("grads-walk", "Graduates walking together at Team University",
     "Twenty-five years of TEAM, and the launch of the university's first Alumni Association",
     "21 November 2025", "news.html#jubilee"),
    ("students-building", "Students gathered outside the Team University building",
     "Studying with Team University in South Sudan, through Destiny University College, Juba",
     "Partnerships", "news.html#juba"),
    ("students-audience", "Students listening during an event at Team University",
     "Applications open for the February 2027 intake across all six faculties",
     "November 2026", "news.html#intake"),
]


def news():
    stem, alt, title, when, href = NEWS[0]
    minis = "".join(
        f"""<a class="mini" href="{h}">{pic(s, a, sizes="(max-width: 640px) 120px, 280px")}
        <div><h3>{t}</h3><time>{w}</time></div></a>"""
        for s, a, t, w, h in NEWS[1:])
    return f"""<section class="sec sec--sky">
  <div class="wrap">
    <h2 class="title title--center" style="color:var(--ink)">University News</h2>
    <p class="sub">Stories about people, research and life across the University</p>
    <div class="bar"></div>
    <div class="news-grid">
      <a class="feature" href="{href}">{pic(stem, alt, sizes="(max-width: 960px) 100vw, 600px")}
        <div class="feature-body"><h3>{title}</h3><time>{when}</time></div></a>
      <div class="minis">{minis}</div>
    </div>
    <div class="more"><a class="btn btn--gold" href="news.html">More University News</a></div>
  </div>
</section>"""


# -------------------------------------------------------------- 6. EVENTS --
EVENTS = [
    ("International Conference on AI and the Transformation of Education Systems",
     "Two days of research, practice and policy on how AI is reshaping teaching, learning and the governance of education. Hybrid; papers in English or French.",
     "10&ndash;11 December 2026", "Two days", "Team University, Kampala &middot; and online",
     "research.html#conference"),
    ("Campus visits for applicants",
     "Thinking of joining in February? Come and see the campus, meet the admissions office and talk through programmes, entry requirements and fees.",
     "Monday to Friday", "Office hours", "Admissions Office, Wood House Mengo",
     "contact.html"),
    ("17th Graduation Ceremony",
     "Graduation notices, clearance deadlines and the graduation list will be published on the notice board as soon as the date is confirmed.",
     "Date to be announced", "", "Team University, Kampala",
     "news.html"),
]


def events():
    cards = "".join(f"""<article class="ev">
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="ev-meta"><span><svg><use href="#i-calendar"/></svg>{when}</span>{('<span><svg><use href="#i-clock"/></svg>' + time + '</span>') if time else ''}</div>
        <div class="ev-where"><svg><use href="#i-pin"/></svg>{where}</div>
        <a class="btn btn--blue" href="{href}">Learn More</a>
      </article>""" for t, d, when, time, where, href in EVENTS)
    return f"""<section class="events">
  {pic("academic-procession", "", sizes="100vw")}
  <div class="wrap">
    <h2 class="title">Upcoming Events</h2>
    <p class="sub">Opportunities to engage with people, ideas and education across the University.</p>
    <div class="ev-grid">{cards}</div>
  </div>
</section>"""


# --------------------------------------------------------------- 7. MODES --
def modes():
    items = [
        ("i-sun", "Day", "Monday to Friday", "Full-time study on the Mengo campus, for school leavers and anyone free in the day."),
        ("i-moon", "Evening", "After work", "Keep your job and study in the evening on the same programmes and the same campus."),
        ("i-calendar", "Weekend", "Saturday and Sunday", "Popular with working professionals and students travelling in from outside Kampala."),
        ("i-globe", "ODeL", "Open Distance and e-Learning", "Study from anywhere, with materials and assessment online through the e-Learning platform."),
    ]
    cards = "".join(
        f'<div class="mode"><div class="mode-ico"><svg><use href="#{i}"/></svg></div>'
        f'<h3>{t}</h3><em>{s}</em><p>{d}</p></div>' for i, t, s, d in items)
    return f"""<section class="sec">
  <div class="wrap">
    <h2 class="title title--center">Study Your Way</h2>
    <p class="sub">Four ways to study at TEAM &mdash; choose the one that fits your life.</p>
    <div class="bar"></div>
    <div class="modes">{cards}</div>
  </div>
</section>"""


# ------------------------------------------------------------- 8. GALLERY --
def gallery():
    shots = [
        ("graduates-line", "Graduates and staff lined up in their gowns", "Graduation"),
        ("library-study", "Students studying together in the library", "Library"),
        ("student-speaker", "A student speaking at a university event", "Student voice"),
        ("fbm-tent", "Graduands of the Faculty of Business and Management", "Faculties"),
        ("dignitaries", "Guests of honour and university leaders at a ceremony", "Ceremonies"),
    ]
    tiles = "".join(
        f'<a href="student-life.html">{pic(s, a, sizes="(max-width: 640px) 50vw, 33vw")}<span>{l}</span></a>'
        for s, a, l in shots)
    return f"""<section class="sec sec--sky">
  <div class="wrap">
    <h2 class="title title--center">Life at TEAM</h2>
    <p class="sub">Graduations, lectures, the library and the people who make the university.</p>
    <div class="bar"></div>
    <div class="gallery">{tiles}</div>
    <div class="more"><a class="btn btn--blue" href="https://www.youtube.com/@teamuniversity" rel="noopener"><svg><use href="#i-play"/></svg> Watch on YouTube</a></div>
  </div>
</section>"""


# ------------------------------------------------------------ 9. PARTNERS --
def partners():
    items = [
        ("NCHE", "National Council for Higher Education &mdash; university licence", "https://unche.or.ug"),
        ("UVTAB", "Uganda Vocational and Technical Assessment Board", "faculty-tvet.html"),
        ("UHPAB", "Health professions assessment, Uganda", "faculty-health.html"),
        ("CEDIMES", "Paris &mdash; partner, AI in Education Conference 2026", "research.html#conference"),
        ("DUC", "Destiny University College, Juba &mdash; collaboration", "news.html#juba"),
        ("+", "Partner with Team University", "contact.html"),
    ]
    tiles = "".join(
        f'<a class="partner" href="{h}"><span><b>{n}</b><small>{d}</small></span></a>' for n, d, h in items)
    return f"""<section class="sec">
  <div class="wrap">
    <h2 class="title title--center">Regulators, Partners and Collaborators</h2>
    <p class="sub">The bodies that license and examine our programmes, and the institutions we work with.</p>
    <div class="bar"></div>
    <div class="partners">{tiles}</div>
  </div>
</section>"""


def body():
    from build import CTA_BAND
    return "\n\n".join([
        hero(), finder_and_board(), faculties_band(), unique(), news(),
        events(), modes(), gallery(), partners(), CTA_BAND,
    ])
