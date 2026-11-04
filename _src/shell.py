"""
THE SHELL — every page's head, masthead, menus and footer (Nov 2026 redesign)
============================================================================
Laid out the way the established Ugandan university sites are (Kabale
University was the reference the university's own staff pointed to):

* a yellow utility bar — email, phone, socials, quick links;
* a royal-blue masthead with the menu SPLIT around the crest, which sits in a
  round seal that overlaps the photograph below it;
* a phone drawer and a four-tab bar for small screens.

One menu definition (MENU) drives the desktop dropdowns AND the phone drawer,
so the two can never disagree about where a page lives.
"""

PORTAL = "https://team.campusnect.com/portal/login/"
APPLY = "https://team.campusnect.com/apply/"
ELEARN = "https://elearning.teamuniversity.ac.ug"
ELIB = "https://libraris.teamuniversity.ac.ug"

PHONE = "+256 782 752226"
PHONE_TEL = "+256782752226"
EMAIL = "info@teamuniversity.ac.ug"
WHATSAPP = "https://wa.me/256782752226"

SOCIAL = [
    ("https://www.facebook.com/teamuniversitykampala", "i-facebook", "Facebook"),
    ("https://twitter.com/TeamUniversityU", "i-x", "X (Twitter)"),
    ("https://www.youtube.com/@teamuniversity", "i-youtube", "YouTube"),
    (WHATSAPP, "i-whatsapp", "WhatsApp"),
]

# (label, href or None, [children]) — children are (label, href).
# A child list given as a dict of {heading: [...]} renders as a two-column mega menu.
MENU_LEFT = [
    ("Home", "index.html", None),
    ("About Us", "about.html", [
        ("Who we are", "about.html#who"),
        ("Vision and mission", "about.html#vision"),
        ("Our values", "about.html#values"),
        ("Leadership", "about.html#leadership"),
        ("Academic standards", "about.html#quality"),
        ("Contact us", "contact.html"),
    ]),
    ("Admissions", "admissions.html", [
        ("How to apply", "admissions.html#how"),
        ("Entry requirements", "admissions.html#requirements"),
        ("Documents you need", "admissions.html#documents"),
        ("Scholarships", "admissions.html#scholarships"),
        ("Fees structure", "admissions.html#fees"),
        ("Intakes", "admissions.html#intakes"),
        ("Common questions", "admissions.html#faq"),
        ("Apply online", APPLY),
    ]),
    ("Academics", "academics.html", {
        "Faculties and schools": [
            ("Graduate Studies and Research", "faculty-graduate.html"),
            ("Management and Humanities", "faculty-business.html"),
            ("Applied Science and Technology", "faculty-applied.html"),
            ("Health Sciences", "faculty-health.html"),
            ("Education", "faculty-education.html"),
            ("Vocational and Technical Education", "faculty-tvet.html"),
        ],
        "Study at TEAM": [
            ("All programmes", "programmes.html"),
            ("Faculties at a glance", "academics.html"),
            ("Study modes", "academics.html#modes"),
            ("Academic calendar", "academics.html#calendar"),
            ("Teaching and assessment", "academics.html#teaching"),
            ("E-Learning", ELEARN),
        ],
    }),
]

MENU_RIGHT = [
    ("Research", "research.html", [
        ("Research at TEAM", "research.html"),
        ("AI in Education Conference 2026", "research.html#conference"),
        ("Graduate research", "faculty-graduate.html"),
        ("E-Library", ELIB),
    ]),
    ("Students", "student-life.html", [
        ("The campus", "student-life.html#campus"),
        ("Student support", "student-life.html#support"),
        ("Student leadership", "student-life.html#guild"),
        ("Digital services", "student-life.html#digital"),
        ("Accommodation", "student-life.html#accommodation"),
        ("Student portal", PORTAL),
    ]),
    ("News &amp; Events", "news.html", None),
    ("Contacts", "contact.html", None),
]

# Which pages count as "inside" each top-level item, for the highlight.
SECTION_OF = {
    "about.html": "About Us", "admissions.html": "Admissions",
    "academics.html": "Academics", "programmes.html": "Academics",
    "research.html": "Research", "student-life.html": "Students",
    "news.html": "News &amp; Events", "contact.html": "Contacts",
    "index.html": "Home",
}


def _children(kids):
    if isinstance(kids, dict):
        return [k for group in kids.values() for k in group]
    return kids or []


def _section(page):
    if page.startswith("faculty-"):
        return "Academics"
    return SECTION_OF.get(page, "")


def _desktop(items, current):
    out = []
    here = _section(current)
    caret = '<svg class="caret"><use href="#i-caret"/></svg>'
    for label, href, kids in items:
        cls = "ni is-here" if label == here else "ni"
        if not kids:
            cur = ' aria-current="page"' if href == current else ""
            out.append(f'<div class="{cls}"><a href="{href}"{cur}>{label}</a></div>')
            continue
        if isinstance(kids, dict):
            cols = "".join(
                "<div><h4>" + head + "</h4>" + "".join(
                    f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>'
                    for t, h in group) + "</div>"
                for head, group in kids.items())
            panel = f'<div class="dd dd--mega">{cols}</div>'
        else:
            panel = '<div class="dd">' + "".join(
                f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>'
                for t, h in kids) + "</div>"
        out.append(f'<div class="{cls}"><a href="{href}" aria-haspopup="true">{label}{caret}</a>{panel}</div>')
    return "".join(out)


def _drawer(current):
    out = []
    for label, href, kids in MENU_LEFT + MENU_RIGHT:
        kids = _children(kids)
        if not kids:
            out.append(f'<a href="{href}">{label}</a>')
        else:
            inner = f'<a href="{href}">{label} &mdash; overview</a>' + "".join(
                f'<a href="{h}">{t}</a>' for t, h in kids if h != href)
            opened = " open" if _section(current) == label else ""
            out.append(f"<details{opened}><summary>{label}</summary>{inner}</details>")
    return "".join(out)


SEAL = """<a class="seal" href="index.html" aria-label="Team University home">
      <svg class="seal-ring" viewBox="0 0 176 176" aria-hidden="true">
        <defs>
          <path id="sealTop" d="M 25 88 A 63 63 0 0 1 151 88"/>
          <path id="sealBot" d="M 22 92 A 66 66 0 0 0 154 92"/>
        </defs>
        <text><textPath href="#sealTop" startOffset="50%" text-anchor="middle">Team University</textPath></text>
        <text class="lo"><textPath href="#sealBot" startOffset="50%" text-anchor="middle">&#9733; Empower for Generations &#9733;</textPath></text>
      </svg>
      <img src="img/crest-160.png" alt="Team University crest" width="123" height="160">
    </a>"""


def topbar():
    socials = "".join(
        f'<a href="{u}" aria-label="Team University on {n}" rel="noopener"><svg><use href="#{i}"/></svg></a>'
        for u, i, n in SOCIAL)
    return f"""<div class="topbar">
  <div class="wrap">
    <div class="topbar-contacts">
      <a href="mailto:{EMAIL}"><svg><use href="#i-mail"/></svg>{EMAIL}</a>
      <a href="tel:{PHONE_TEL}"><svg><use href="#i-phone"/></svg>{PHONE}</a>
    </div>
    <div class="topbar-right">
      <div class="topbar-social">{socials}</div>
      <nav class="topbar-links" aria-label="Quick links">
        <a href="{PORTAL}">Student Portal</a>
        <a href="{ELEARN}">E-Learning</a>
        <a href="{ELIB}">E-Library</a>
        <a href="{APPLY}">Apply Online</a>
      </nav>
    </div>
  </div>
</div>"""


def masthead(current):
    return f"""<header class="masthead" id="masthead">
  <div class="wrap">
    <nav class="mainnav mainnav--left" aria-label="Main, first half">{_desktop(MENU_LEFT, current)}</nav>
    {SEAL}
    <a class="brand-m" href="index.html" style="display:none"><strong>Team University</strong><span>Empower for Generations</span></a>
    <nav class="mainnav mainnav--right" aria-label="Main, second half">{_desktop(MENU_RIGHT, current)}<div class="ni"><a class="search-btn" href="programmes.html" aria-label="Search programmes"><svg><use href="#i-search"/></svg></a></div></nav>
    <button class="nav-toggle" id="navToggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu"><svg><use href="#i-menu"/></svg></button>
  </div>
</header>

<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-bg" data-close></div>
  <div class="drawer-panel" role="dialog" aria-label="Menu">
    <div class="drawer-head">Menu <button type="button" data-close aria-label="Close menu"><svg><use href="#i-close"/></svg></button></div>
    <nav>{_drawer(current)}</nav>
    <a class="btn btn--gold drawer-apply" href="{APPLY}">Apply online</a>
  </div>
</div>"""


def footer():
    socials = "".join(
        f'<a href="{u}" aria-label="Team University on {n}" rel="noopener"><svg><use href="#{i}"/></svg></a>'
        for u, i, n in SOCIAL)
    return f"""<footer class="foot">
  <div class="ribbon ribbon--thin"></div>
  <div class="foot-top">
    <div class="wrap foot-grid">
      <div>
        <div class="foot-brand">
          <img src="img/crest-160.png" alt="" width="52" height="68">
          <div><strong>Team University</strong><span>Empower for Generations</span></div>
        </div>
        <p>A private university in Mengo, Kampala, licensed by the National Council for Higher Education. Day, evening, weekend and distance study across six faculties and schools.</p>
        <div class="socials">{socials}</div>
      </div>
      <div>
        <h3>Study</h3>
        <ul>
          <li><a href="programmes.html">All programmes</a></li>
          <li><a href="academics.html">Faculties and schools</a></li>
          <li><a href="faculty-graduate.html">Graduate studies</a></li>
          <li><a href="academics.html#modes">Study modes</a></li>
          <li><a href="academics.html#calendar">Academic calendar</a></li>
        </ul>
      </div>
      <div>
        <h3>Admissions</h3>
        <ul>
          <li><a href="{APPLY}">Apply online</a></li>
          <li><a href="admissions.html#requirements">Entry requirements</a></li>
          <li><a href="admissions.html#scholarships">Scholarships</a></li>
          <li><a href="admissions.html#fees">Fees structure</a></li>
          <li><a href="admissions.html#faq">Common questions</a></li>
        </ul>
      </div>
      <div>
        <h3>Quick links</h3>
        <ul>
          <li><a href="{PORTAL}">Student portal</a></li>
          <li><a href="{ELEARN}">E-Learning</a></li>
          <li><a href="{ELIB}">E-Library</a></li>
          <li><a href="research.html">Research</a></li>
          <li><a href="news.html">News and events</a></li>
        </ul>
      </div>
      <div>
        <h3>Contact us</h3>
        <ul class="foot-contact">
          <li><svg><use href="#i-pin"/></svg><span>Wood House Mengo, Plot 446<br>Kabaka A'njagala Road<br>Mengo-Rubaga, Kampala</span></li>
          <li><svg><use href="#i-phone"/></svg><span><a href="tel:+256782752226">+256 782 752226</a><br><a href="tel:+256704310224">+256 704 310224</a></span></li>
          <li><svg><use href="#i-mail"/></svg><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot-base">
    <div class="wrap">
      <span>&copy; <span id="year">2026</span> Team University, Kampala. All rights reserved.</span>
      <span>Licensed by the National Council for Higher Education (NCHE)</span>
    </div>
  </div>
</footer>"""
