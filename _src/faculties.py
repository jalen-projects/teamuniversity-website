"""
FACULTY PAGES AND THE FULL PROGRAMME LIST
=========================================
Six faculty pages and one searchable index of all ninety-nine programmes,
generated from `catalogue.py` rather than typed out — so a programme added to
the university's registry reaches the website by re-running the builder, and a
programme that was never on the books cannot appear here at all.

Three of these pages did not exist before: Graduate Studies, Education and
Vocational and Technical Education. Between them that is fifty-nine of the
university's ninety-nine programmes — most of the postgraduate and vocational
offer, missing from the university's own front door.

What each page deliberately does NOT say: fees, and the names of staff. Both
were unavailable, and a university website that invents either is worse than
one that says "ask the office".
"""

import json

import catalogue as cat
from build import APPLY, CTA_BAND, banner, page_body, related, sidenav


def _table(rows):
    """One award level as a table: name, code, how long, who awards it."""
    body = "".join(
        f"<tr><td><strong>{row['name']}</strong></td>"
        f"<td><code>{row['code']}</code></td>"
        f"<td>{cat.duration(row)}</td>"
        f"<td>{cat.BOARD_NAME.get(row['board'], row['board'])}</td></tr>"
        for row in rows)
    return f"""<div class="table-wrap"><table class="prog-table">
  <thead><tr><th>Programme</th><th>Code</th><th>Duration</th><th>Awarded by</th></tr></thead>
  <tbody>{body}</tbody>
</table></div>"""


def faculty_page(code):
    """The whole body for one faculty."""
    page, title, blurb, icon, photo, count = cat.FACULTIES[code] + (cat.count(code),)
    full = cat.faculty_name(code)

    blocks = []
    for label, rows in cat.by_level(code):
        blocks.append(f'<h2 id="{label.lower().replace(" ", "-")}">{label} '
                      f'<span class="count-badge">{len(rows)}</span></h2>')
        blocks.append(_table(rows))

    intro = f"""<p class="lede">{blurb}</p>

<p>The {full} runs <strong>{count} programmes</strong>. Every one of them is
taught on more than one schedule where numbers allow — by day, in the evening,
at weekends, and by distance — so that a job, a business or a family does not
have to be given up to study.</p>

<div class="callout callout--gold">
  <h3>50% scholarships, August 2026 intake</h3>
  <p>Selected programmes in this faculty carry a half-fee scholarship for the
     August intake, awarded on merit and need. Ask the admissions office which
     of the programmes below are covered before you apply.</p>
  <p><a class="btn btn--primary" href="{APPLY}">Apply now</a>
     <a class="btn btn--line" href="contact.html">Ask about scholarships</a></p>
</div>

<h2 id="entry">Getting in</h2>
<p>Entry requirements differ by award. As a general guide: a bachelors degree
   needs a UACE certificate with two principal passes (or a relevant diploma);
   a diploma needs a UCE certificate and the relevant subjects; a certificate
   needs a UCE certificate. Masters and postgraduate programmes need a first
   degree in a related field. The admissions office confirms your own case
   against your documents — send them, and they will tell you where you stand.</p>

<h2 id="fees">Fees</h2>
<p>Tuition and functional fees for this faculty are set each academic year and
   are issued by the finance office. They are not published here because a
   figure that goes out of date on a website costs a family real money.
   <a href="contact.html">Request the current fees structure</a> and it will be
   sent to you with the programme you are asking about.</p>
"""

    others = [(p, t) for c, (p, t, *_rest) in cat.FACULTIES.items() if c != code][:3]
    return page_body(
        banner(full, blurb,
               [("Academics", "academics.html"), (title,)],
               image=photo, alt=f"{full} at Team University"),
        sidenav("Academics", [(p, t, p == page) for p, t, _d in _academics_nav()]),
        intro + "\n" + "\n".join(blocks),
        related(others + [("admissions.html", "How to apply")]),
    ) + "\n\n" + CTA_BAND


def _academics_nav():
    from build import ACADEMICS
    return ACADEMICS


def all_programmes_page():
    """Every programme in the university, searchable, on one page."""
    index = json.dumps(cat.search_index(), separators=(",", ":"), ensure_ascii=False)
    levels = "".join(
        f'<button type="button" class="chip" data-level="{label}">{label}</button>'
        for _code, label in cat.LEVELS)
    faculty_options = "".join(
        f'<option value="{title}">{title}</option>'
        for _c, _p, title, _b, _i, _ph, _n in cat.all_faculties())

    counts = "".join(
        f'<a class="tally" href="{page}"><strong>{n}</strong><span>{title}</span></a>'
        for _c, page, title, _b, _i, _ph, n in cat.all_faculties())

    body = f"""<p class="lede">Every programme Team University runs — {cat.count()} of
them, across {len(cat.FACULTIES)} faculties. Search by subject, or filter by the
award you are after.</p>

<div class="tallies">{counts}</div>

<div class="finder-controls">
  <div class="finder-search">
    <svg><use href="#i-search"/></svg>
    <input type="search" id="progSearch" placeholder="Search all programmes…"
           autocomplete="off" aria-label="Search programmes">
  </div>
  <select id="progFaculty" aria-label="Filter by faculty">
    <option value="">All faculties</option>
    {faculty_options}
  </select>
</div>

<div class="chips" id="progLevels" role="group" aria-label="Filter by award">
  <button type="button" class="chip is-on" data-level="">All awards</button>
  {levels}
</div>

<p class="finder-count" id="progCount" aria-live="polite"></p>
<div class="finder-results finder-results--page" id="progResults"></div>

<h2>What the award means</h2>
<p>Most programmes are awarded by Team University itself. Where a programme is
   assessed by a national board — UVTAB for the vocational trades, UHPAB for
   health — the board is named in the results above, because a nationally
   assessed certificate is a different thing from a university award and you
   should know which you are signing up for.</p>

<script id="progData" type="application/json">{index}</script>"""

    return page_body(
        banner("Every programme",
               f"All {cat.count()} programmes across {len(cat.FACULTIES)} faculties.",
               [("Academics", "academics.html"), ("Every programme",)],
               image="campus-group", alt="Team University students on campus"),
        sidenav("Academics", [(p, t, p == "programmes.html") for p, t, _d in _academics_nav()]),
        body,
        related([("admissions.html", "How to apply"),
                 ("academics.html", "Faculties and study modes"),
                 ("contact.html", "Talk to admissions")]),
    ) + "\n\n" + CTA_BAND


def specs():
    """The page entries for PAGES, one per faculty plus the full list."""
    out = {}
    for code, (page, title, blurb, _icon, _photo) in cat.FACULTIES.items():
        full = cat.faculty_name(code)
        out[page] = dict(
            title=f"{full} | Team University Kampala",
            og_title=full,
            description=f"{blurb} {cat.count(code)} programmes at Team University, "
                        f"Kampala — day, evening, weekend and distance.",
            body=faculty_page(code),
            styles='<link rel="stylesheet" href="css/home.css">',
        )
    # The old Social Sciences page keeps its address rather than 404ing —
    # anything already linking to it (a Facebook post, a printed flyer) still
    # lands somewhere useful. Its programmes are now inside Management and
    # Humanities, which is where the registry actually keeps them.
    out["faculty-social.html"] = dict(
        title="Social Sciences | Team University Kampala",
        og_title="Social sciences at Team University",
        description="Social work, development studies and public administration "
                    "at Team University are taught in the Faculty of Management "
                    "and Humanities.",
        body=page_body(
            banner("Social sciences at Team",
                   "Social work, development studies and public administration.",
                   [("Academics", "academics.html"), ("Social sciences",)],
                   image="campus-group", alt="Team University students on campus"),
            sidenav("Academics", [(p, t, False) for p, t, _d in _academics_nav()]),
            """<p class="lede">These programmes are taught in the
<a href="faculty-business.html">Faculty of Management and Humanities</a>.</p>

<p>Team University groups the social sciences with management and the
humanities in a single faculty, which is how the university's own registry
holds them. Social Work and Social Administration, Development Studies, Public
Administration and Management, International Relations and Diplomacy, and
Journalism and Media Studies are all listed there, together with their
diplomas and postgraduate awards.</p>

<p><a class="btn btn--primary" href="faculty-business.html">Go to Management and
Humanities</a> <a class="btn btn--line" href="programmes.html">Search all
programmes</a></p>""",
            related([("faculty-business.html", "Management and Humanities"),
                     ("programmes.html", "Every programme"),
                     ("admissions.html", "How to apply")]),
        ) + "\n\n" + CTA_BAND,
        styles='<link rel="stylesheet" href="css/home.css">',
    )
    out["programmes.html"] = dict(
        title=f"All {cat.count()} programmes | Team University Kampala",
        og_title="Every programme at Team University",
        description=f"Search all {cat.count()} Team University programmes across "
                    f"{len(cat.FACULTIES)} faculties — masters, bachelors, diplomas "
                    f"and national certificates.",
        body=all_programmes_page(),
        styles='<link rel="stylesheet" href="css/home.css">',
        scripts='<script src="js/home.js" defer></script>\n',
    )
    return out
