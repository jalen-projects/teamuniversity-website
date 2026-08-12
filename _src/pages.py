"""
Page content for the Team University site.

Each entry is one .html file. Content marked TODO in a comment is a placeholder
the university must replace with its own material: see TODO.md in the project
root for the full list. Everything not marked TODO is taken from the
university's own published information.
"""

from build import (APPLY, PORTAL, ELEARN, ELIB, CTA_BAND, banner, sidenav,
                   related, page_body, academics_side)
import catalogue as cat
import faculties
import home

# The faculty table is generated from the university's own catalogue, so it
# cannot say "four faculties" while the registry holds six.
def _faculty_rows():
    rows = []
    for code, page, title, _blurb, _icon, _photo, n in cat.all_faculties():
        awards = ", ".join(label for label, _r in cat.by_level(code))
        rows.append(
            f"    <tr><td><a href=\"{page}\">{cat.faculty_name(code)}</a></td>"
            f"<td>{_FIELDS[code]}</td>"
            f"<td>{awards}</td>"
            f"<td style=\"text-align:center\"><strong>{n}</strong></td></tr>")
    return "\n".join(rows)


_FIELDS = {
    "SGSR": "Masters and postgraduate study across management, education, health and public administration",
    "FMH": "Business, accounting, procurement, human resource, economics, social work, public administration, journalism",
    "FAST": "Computer science, information technology, software engineering, environment, agriculture",
    "SHS": "Clinical medicine, nursing, midwifery, public and community health",
    "FED": "Primary and secondary teacher training, early childhood, education management",
    "TVET": "Catering, tailoring, electrical, motor vehicle, building, plumbing and other trades",
}

FACULTY_TABLE = f"""<div class="table-scroll">
<table class="data">
  <caption>Every faculty, what it covers and how many programmes it runs. Confirm the exact award title and entry requirements with the faculty before paying any fees.</caption>
  <thead>
    <tr><th scope="col">Faculty or school</th><th scope="col">Fields covered</th><th scope="col">Awards</th><th scope="col">Programmes</th></tr>
  </thead>
  <tbody>
{_faculty_rows()}
  </tbody>
</table>
</div>

<p><a class="btn btn--primary" href="programmes.html">Search all {cat.count()} programmes</a></p>"""


# ==========================================================================
# HOME
# ==========================================================================

HOME_BODY = f"""<section class="hero">
  <div class="hero-media">
    <picture>
      <source type="image/webp" srcset="img/grad-800.webp 800w, img/grad-1020.webp 1020w" sizes="100vw">
      <img src="img/grad-1020.jpg" alt="Team University graduands walking in procession in academic gowns on graduation day" width="1020" height="476" fetchpriority="high" decoding="async">
    </picture>
  </div>

  <div class="wrap">
    <div class="hero-inner">
      <span class="hero-eyebrow"><svg><use href="#i-cap"/></svg> Empower For Generations</span>
      <h1 class="h-display">Study in Kampala, on <span class="accent">your own schedule</span>.</h1>
      <p class="hero-lede">Day, evening, weekend and distance programmes across six faculties, built for students who are already building a career.</p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="{APPLY}">Apply now <svg><use href="#i-arrow"/></svg></a>
        <a class="btn btn--ghost" href="academics.html">Explore programmes</a>
      </div>
    </div>
  </div>
</section>

<div class="intake">
  <div class="wrap">
    <span>The August 2026 intake is open for registration.</span>
    <a href="admissions.html">See how to apply</a>
  </div>
</div>

<section class="section vision">
  <div class="wrap">
    <div class="reveal">
      <p class="vision-statement">Team University exists to turn ambition into <em>qualified, employable expertise</em> for the people who keep East Africa working.</p>
    </div>
    <div class="vision-body reveal reveal-d1">
      <div class="vision-block">
        <h3>Our vision</h3>
        <p>To be a hub of professional excellency through continued innovations in business, management and other disciplines, research and entrepreneurship in the East African region.</p>
      </div>
      <div class="vision-block">
        <h3>Our mission</h3>
        <p>To provide a transformative education experience for students, with intent to foster productive careers, meaningful livelihood, and responsible citizenry.</p>
      </div>
      <div class="vision-block">
        <h3>Where we are</h3>
        <p>Wood House Mengo, Plot 446 Kabaka A'njagala Road, Mengo-Rubaga, Kampala. <a href="contact.html">Find us and get in touch</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="faculties">
  <div class="wrap">
    <div class="faculties-head reveal">
      <p class="eyebrow">Faculties and schools</p>
      <h2 class="h-section">Six faculties, one campus.</h2>
      <p class="lede">Each faculty runs its own admissions and academic advising, so you deal with people who know your field.</p>
    </div>

    <div class="bento">
      <a class="fac fac--media reveal" href="faculty-business.html">
        <picture>
          <source type="image/webp" srcset="img/campus-998.webp">
          <img src="img/campus-998.jpg" alt="The Team University campus building in Mengo, Kampala" width="998" height="459" loading="lazy" decoding="async">
        </picture>
        <span class="fac-icon"><svg><use href="#i-briefcase"/></svg></span>
        <h3>Faculty of Business and Management</h3>
        <p>Accounting and finance, business administration, procurement and logistics, from certificate through to postgraduate study.</p>
        <span class="fac-more">View programmes <svg><use href="#i-caret"/></svg></span>
      </a>

      <a class="fac fac--navy reveal reveal-d1" href="faculty-health.html">
        <span class="fac-icon"><svg><use href="#i-cap"/></svg></span>
        <h3>School of Health Sciences</h3>
        <p>Clinical and community health training with supervised practical placements.</p>
        <span class="fac-more">View programmes <svg><use href="#i-caret"/></svg></span>
      </a>

      <a class="fac fac--blue reveal reveal-d2" href="faculty-applied.html">
        <span class="fac-icon"><svg><use href="#i-laptop"/></svg></span>
        <h3>Faculty of Applied Sciences</h3>
        <p>Computing, information technology and the applied sciences that employers are hiring for now.</p>
        <span class="fac-more">View programmes <svg><use href="#i-caret"/></svg></span>
      </a>

      <a class="fac fac--media reveal reveal-d3" href="faculty-social.html">
        <picture>
          <source type="image/webp" srcset="img/gate-800.webp 800w, img/gate-1020.webp 1020w" sizes="(min-width: 1060px) 60vw, 100vw">
          <img src="img/gate-1020.jpg" alt="The main gate and entrance of Team University on Kabaka A'njagala Road" width="1020" height="476" loading="lazy" decoding="async">
        </picture>
        <span class="fac-icon"><svg><use href="#i-globe"/></svg></span>
        <h3>Faculty of Social Sciences</h3>
        <p>Social work, public administration and development studies for careers in government, NGOs and community organisations.</p>
        <span class="fac-more">View programmes <svg><use href="#i-caret"/></svg></span>
      </a>
    </div>
  </div>
</section>

<section class="section modes">
  <div class="wrap">
    <div class="modes-head reveal">
      <h2 class="h-section">Four ways to study.</h2>
      <p class="lede">Most of our students work. Choose the schedule that fits the life you already have, and change it between semesters if your circumstances change.</p>
    </div>

    <div class="rail">
      <article class="mode reveal">
        <span class="mode-icon"><svg><use href="#i-clock"/></svg></span>
        <h3>Day</h3>
        <p>Weekday timetable for full-time students, with lectures and practicals scheduled across the working week.</p>
      </article>
      <article class="mode reveal reveal-d1">
        <span class="mode-icon"><svg><use href="#i-buildings"/></svg></span>
        <h3>Evening</h3>
        <p>Lectures after office hours for students in full-time employment in and around Kampala.</p>
      </article>
      <article class="mode reveal reveal-d2">
        <span class="mode-icon"><svg><use href="#i-briefcase"/></svg></span>
        <h3>Weekend</h3>
        <p>Concentrated Saturday and Sunday sessions for professionals who cannot attend during the week.</p>
      </article>
      <article class="mode reveal reveal-d3">
        <span class="mode-icon"><svg><use href="#i-globe"/></svg></span>
        <h3>Distance and online</h3>
        <p>Open Distance and e-Learning, so you can study from anywhere in the region and come in for assessments.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--dark digital">
  <div class="wrap">
    <div class="reveal">
      <p class="eyebrow">Digital campus</p>
      <h2 class="h-section">Your records, results and materials in one place.</h2>
      <p class="lede" style="margin-top:1rem">Registration, coursework, results and fee statements run on the university's own student system. You do not queue for a printout.</p>
    </div>

    <div class="digital-list reveal reveal-d1">
      <a class="dcard" href="{PORTAL}">
        <span class="dcard-icon"><svg><use href="#i-cap"/></svg></span>
        <span>
          <h3>Student Portal</h3>
          <p>Register for courses, track your results and CGPA, download your fee statement and admission documents.</p>
        </span>
      </a>
      <a class="dcard" href="{ELEARN}">
        <span class="dcard-icon"><svg><use href="#i-laptop"/></svg></span>
        <span>
          <h3>E-Learning</h3>
          <p>Lecture materials, assignments and submissions for every unit you are registered for.</p>
        </span>
      </a>
      <a class="dcard" href="{ELIB}">
        <span class="dcard-icon"><svg><use href="#i-books"/></svg></span>
        <span>
          <h3>E-Library</h3>
          <p>Journals, past papers and reference texts, searchable from your phone.</p>
        </span>
      </a>
    </div>
  </div>
</section>

{CTA_BAND}"""


# ==========================================================================
# ABOUT
# ==========================================================================

ABOUT = page_body(
    banner("About Team University",
           "A Kampala university built around working students, professional practice and the qualifications employers in the region actually ask for.",
           [("About", "about.html")], image="campus",
           alt="The Team University campus building in Mengo, Kampala"),
    sidenav("On this page", [
        ("#who", "Who we are", True),
        ("#vision", "Vision and mission", False),
        ("#values", "Our values", False),
        ("#leadership", "Leadership", False),
        ("#quality", "Academic standards", False),
    ]),
    """<h2 id="who">Who we are</h2>
<p>Team University is a private university in Mengo, Kampala, offering programmes in business and management, health sciences, applied sciences and social sciences. Our students range from school leavers taking their first degree to working professionals returning for a postgraduate qualification.</p>
<p>What shapes the university is who studies here. Most of our students hold a job, support a family, or both. That is why teaching runs on four schedules rather than one, why our campus sits inside the city rather than outside it, and why registration, results and fee statements are handled online instead of at a counter.</p>

<figure class="lead-figure">
  <picture>
    <source type="image/webp" srcset="img/gate-1020.webp">
    <img src="img/gate-1020.jpg" alt="Students and traffic at the Team University main gate on Kabaka A'njagala Road" width="1020" height="476" loading="lazy">
  </picture>
  <figcaption>The main gate on Kabaka A'njagala Road, Mengo-Rubaga.</figcaption>
</figure>

<h2 id="vision">Vision and mission</h2>
<h3>Vision</h3>
<p>To be a hub of professional excellency through continued innovations in business, management and other disciplines, research and entrepreneurship in the East African region.</p>
<h3>Mission</h3>
<p>To provide a transformative education experience for students, with intent to foster productive careers, meaningful livelihood, and responsible citizenry.</p>
<h3>Motto</h3>
<p><strong>Empower For Generations.</strong> The measure of a degree is not the ceremony at the end of it. It is what a graduate is able to do afterwards, and what that changes for the people around them.</p>

<h2 id="values">Our values</h2>
<ul class="bullets">
  <li><strong>Professional practice.</strong> Programmes are built around the work our graduates will actually do, and taught by people who have done it.</li>
  <li><strong>Access.</strong> A qualification should not be reserved for people who can stop working for three years.</li>
  <li><strong>Integrity.</strong> Assessment is the university's word on what a graduate knows. We protect it.</li>
  <li><strong>Responsibility.</strong> Graduates who understand the communities they serve, not only the sector they are employed in.</li>
</ul>

<h2 id="leadership">Leadership</h2>
<!-- TODO: Replace with the real office holders, their photographs and a short
     message from the Vice Chancellor. Nothing here should be published until
     the university confirms the names and titles. -->
<div class="callout">
  <h3>This section is awaiting content from the university</h3>
  <p>Names, titles, photographs and a message from the Vice Chancellor need to be supplied by the administration before this page goes live. The layout below is ready for them.</p>
</div>

<h2 id="quality">Academic standards</h2>
<p>Team University's programmes follow Ugandan higher-education practice: semester-based study, continuous assessment carried alongside end-of-semester examinations, and classification on the standard degree bands. Coursework and examination weightings are set per course unit and published to students at the start of each semester.</p>
<p>Results are approved by the faculty before release, and every registered student can see their own marks, grade points and cumulative average in the <a href="%PORTAL%">student portal</a> as soon as they are approved.</p>
""".replace("%PORTAL%", PORTAL),
    related([
        ("academics.html", "Faculties and programmes"),
        ("admissions.html", "How to apply"),
        ("contact.html", "Contact the university"),
    ]),
)


# ==========================================================================
# ACADEMICS
# ==========================================================================

ACADEMICS_PAGE = page_body(
    banner("Academics",
           "Six faculties, four ways to study, and one academic calendar. Choose a faculty to see its programmes and entry routes.",
           [("Academics", "academics.html")], image="grad",
           alt="Team University graduands in academic gowns on graduation day"),
    academics_side("academics.html"),
    """<h2>Faculties and schools</h2>
<p>Each faculty admits its own students, advises on programme choice and supervises teaching. If you know the field you want, start with the faculty; if you are still deciding, the admissions office will talk you through the options.</p>

""" + FACULTY_TABLE + """

<h2 id="modes">Study modes</h2>
<p>Every faculty teaches on more than one schedule. You choose your mode when you register, and you can change it between semesters if your circumstances change.</p>

<div class="table-scroll">
<table class="data">
  <thead>
    <tr><th scope="col">Mode</th><th scope="col">When you attend</th><th scope="col">Suits</th></tr>
  </thead>
  <tbody>
    <tr><td>Day</td><td>Weekdays, working hours</td><td>Full-time students, mostly school leavers</td></tr>
    <tr><td>Evening</td><td>Weekday evenings, after office hours</td><td>Students in full-time employment in Kampala</td></tr>
    <tr><td>Weekend</td><td>Saturday and Sunday sessions</td><td>Professionals who cannot attend on weekdays</td></tr>
    <tr><td>Distance and online</td><td>Study remotely, attend for assessment</td><td>Students outside Kampala or travelling for work</td></tr>
  </tbody>
</table>
</div>

<h2 id="calendar">The academic year</h2>
<p>Teaching runs in semesters, with recess terms used for field attachment, retakes and practical work depending on the programme. The August 2026 intake is open for registration now.</p>
<!-- TODO: Replace with the university's published almanac dates once the
     registrar confirms them for the year. -->
<div class="callout">
  <h3>Semester dates</h3>
  <p>The full academic almanac with registration, teaching, examination and recess dates is issued by the Academic Registrar each year. Contact the registrar's office for the current dates.</p>
  <a class="btn btn--line" href="contact.html">Contact the registrar</a>
</div>

<h2 id="teaching">How you are taught and assessed</h2>
<p>Courses combine lectures, tutorials and practical or field work depending on the discipline. Assessment is split between continuous assessment carried through the semester and an end-of-semester examination, with the weighting set per course unit and published to students at the start of the semester.</p>
<p>Registered students access their materials, assignments and results through the <a href="%ELEARN%">e-learning platform</a> and the <a href="%PORTAL%">student portal</a>.</p>
""".replace("%ELEARN%", ELEARN).replace("%PORTAL%", PORTAL),
    related([
        ("admissions.html", "Entry requirements"),
        ("student-life.html", "Life on campus"),
        ("contact.html", "Ask a question"),
    ]),
)


# ==========================================================================
# FACULTY PAGES
# ==========================================================================

def faculty_page(slug, title, lede, image, alt, intro, programmes, careers,
                 facts, note=""):
    rows = "".join(
        f"<tr><td>{name}</td><td>{code}</td><td>{award}</td></tr>"
        for name, code, award in programmes
    )
    fact_html = "".join(f"<div class=\"fact\"><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)
    career_items = "".join(f"<li>{c}</li>" for c in careers)
    return page_body(
        banner(title, lede, [("Academics", "academics.html"), (title, slug)],
               image=image, alt=alt),
        academics_side(slug),
        f"""<h2>About the faculty</h2>
{intro}

<dl class="facts">{fact_html}</dl>

<h2 id="programmes">Programmes</h2>
<div class="table-scroll">
<table class="data">
  <caption>Programme titles and codes follow the current prospectus. Confirm the exact award and entry requirements with the faculty before you pay any fees.</caption>
  <thead>
    <tr><th scope="col">Programme</th><th scope="col">Code</th><th scope="col">Award</th></tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
</div>
{note}

<h2 id="careers">Where graduates go</h2>
<ul class="bullets">{career_items}</ul>

<h2 id="apply">Applying to this faculty</h2>
<p>Applications are handled centrally by the admissions office, which passes your file to this faculty for the academic decision. The <a href="admissions.html">admissions page</a> sets out entry requirements, the documents you need and the steps to follow.</p>
<div class="callout">
  <h3>Not sure this is the right programme?</h3>
  <p>The faculty advises prospective students before they apply. Call the admissions office and ask to speak to this faculty, or send your question and someone will call you back.</p>
  <a class="btn btn--solid" href="contact.html">Ask the faculty</a>
</div>
""",
        related([
            ("admissions.html", "Entry requirements"),
            ("academics.html", "All faculties"),
            ("%APPLY%", "Start an application"),
        ]).replace("%APPLY%", APPLY),
    )


BUSINESS = faculty_page(
    "faculty-business.html",
    "Faculty of Business and Management",
    "Accounting, finance, business administration, procurement and logistics, taught from certificate level through to postgraduate study.",
    "campus", "The Team University campus building in Mengo, Kampala",
    """<p>Business and Management is the largest faculty at Team University and the one most of our evening and weekend students join. Teaching is built around professional practice: the accounting a finance officer actually files, the procurement rules a public entity actually applies, the reporting a manager is actually asked for.</p>
<p>The faculty runs a full ladder of awards. A student can enter at certificate or diploma level, work while studying, and progress to a bachelor's degree and then postgraduate study without leaving employment.</p>""",
    [("Bachelor of Science in Accounting and Finance", "BSAF", "Bachelor"),
     ("Bachelor of Business Administration", "BBA", "Bachelor"),
     ("Diploma in Accounting and Finance", "DAF", "Diploma"),
     ("Diploma in Business Administration", "DBA", "Diploma"),
     ("Diploma in Procurement and Logistics Management", "DPLM", "Diploma"),
     ("Master of Business Administration", "MBA", "Postgraduate"),
     ("Postgraduate Diploma in Management", "PGDM", "Postgraduate")],
    ["Accounts and finance departments in private firms, NGOs and government",
     "Procurement and supply chain roles in public entities and manufacturing",
     "Banking, microfinance and savings and credit cooperatives",
     "Audit and consultancy practice, often alongside professional accountancy papers",
     "Running and growing their own businesses"],
    [("Awards", "Certificate to postgraduate"), ("Study modes", "Day, evening, weekend, distance"),
     ("Applications", "Through the admissions office")],
    note="""<p>Students preparing for professional accountancy papers often take a diploma here alongside their professional study. Talk to the faculty about how the two fit together before you register.</p>""",
)

HEALTH = faculty_page(
    "faculty-health.html",
    "School of Health Sciences",
    "Clinical and community health training, with supervised practical placements in health facilities.",
    "gate", "The entrance to Team University on Kabaka A'njagala Road",
    """<p>The School of Health Sciences trains health workers for clinical and community practice. Health programmes carry a supervised practical component, so students divide their time between classroom teaching at Mengo and placements in health facilities.</p>
<p>Because placements are scheduled, health programmes are less flexible than the rest of the university. Prospective students should discuss the timetable with the school before choosing a study mode.</p>""",
    [("Health sciences programmes", "See faculty", "Certificate, diploma, bachelor")],
    ["Health facilities in the public and private sector",
     "Community and public health programmes run by NGOs",
     "Health administration and records",
     "Further clinical training and specialisation"],
    [("Practical component", "Supervised placements"), ("Study modes", "Discuss with the school"),
     ("Regulation", "Professional council requirements apply")],
    note="""<!-- TODO: Replace the single placeholder row above with the school's
     actual programme list, codes and awards, and confirm which professional
     council registers each award. This is the least complete page on the site. -->
<div class="callout">
  <h3>Programme list to be confirmed</h3>
  <p>The full list of health programmes, their codes and the professional council registering each award is being confirmed with the school. Contact the admissions office for the current list.</p>
  <a class="btn btn--line" href="contact.html">Ask the admissions office</a>
</div>""",
)

APPLIED = faculty_page(
    "faculty-applied.html",
    "Faculty of Applied Sciences",
    "Computing, information technology and the applied sciences, with practical work at the centre of every programme.",
    "street", "The street outside Team University in Mengo, Kampala",
    """<p>Applied Sciences covers computing and information technology alongside the applied sciences. Teaching is practical: students spend their time building, configuring and troubleshooting rather than only reading about it.</p>
<p>IT programmes suit both school leavers and people already working in a technical role who need the qualification to match what they already do.</p>""",
    [("Bachelor of Information Technology", "BIT", "Bachelor"),
     ("Diploma in Information Technology", "DIT", "Diploma"),
     ("Computer applications and office IT", "Short course", "Certificate")],
    ["Systems and network administration",
     "Software development and support",
     "ICT support inside banks, NGOs, schools and government",
     "Data and records management",
     "Self-employment in ICT services"],
    [("Emphasis", "Practical and laboratory work"), ("Study modes", "Day, evening, weekend, distance"),
     ("Awards", "Certificate to bachelor")],
)

SOCIAL = faculty_page(
    "faculty-social.html",
    "Faculty of Social Sciences",
    "Social work, public administration and development studies, for careers in government, NGOs and community organisations.",
    "grad", "Team University graduands on graduation day",
    """<p>Social Sciences prepares students for work in government, non-governmental organisations and community bodies. The faculty's programmes combine social theory with the administrative and field skills the sector actually recruits for: case work, community entry, programme administration and reporting to funders.</p>
<p>Many students in this faculty already work in the sector and study in the evening or at weekends while continuing in post.</p>""",
    [("Bachelor of Social Work and Social Administration", "BSWSA", "Bachelor"),
     ("Development studies and public administration programmes", "See faculty", "Diploma, bachelor")],
    ["Social work and probation services",
     "Programme and project officers in NGOs",
     "Local government administration",
     "Community development and mobilisation",
     "Monitoring, evaluation and reporting roles"],
    [("Field component", "Community placement"), ("Study modes", "Day, evening, weekend, distance"),
     ("Awards", "Diploma and bachelor")],
)


# ==========================================================================
# ADMISSIONS
# ==========================================================================

ADMISSIONS = page_body(
    banner("Admissions",
           "The August 2026 intake is open. Here is what you need, what it costs you in time, and exactly how to apply.",
           [("Admissions", "admissions.html")], image="grad",
           alt="Team University graduands celebrating on graduation day"),
    sidenav("On this page", [
        ("#how", "How to apply", True),
        ("#requirements", "Entry requirements", False),
        ("#documents", "Documents you need", False),
        ("#fees", "Fees", False),
        ("#intakes", "Intakes", False),
        ("#faq", "Common questions", False),
    ]),
    """<h2 id="how">How to apply</h2>
<p>You can apply online from anywhere, or in person at the Mengo campus. Applying online is faster and you can track the outcome yourself.</p>

<ol class="steps">
  <li><strong>Choose your programme and study mode</strong>
  Decide which award you want and whether you will study on the day, evening, weekend or distance schedule. If you are unsure, call the admissions office first; changing programme after registration wastes a semester.</li>
  <li><strong>Complete the application</strong>
  Fill in the online form with your personal details, academic history and the programme you want. There is no account to create first, and you do not pay anything to apply.</li>
  <li><strong>Upload or deliver your documents</strong>
  Attach scans of your certificates and results slips, or bring the originals to the admissions office if you are applying in person.</li>
  <li><strong>Wait for the admission decision</strong>
  Your file goes to the relevant faculty for the academic decision. You will be emailed the outcome, and successful applicants receive an admission letter as a PDF.</li>
  <li><strong>Accept, pay and register</strong>
  Report by the date on your admission letter, pay the required portion of your fees and register for your course units. Your student portal login is created for you at admission.</li>
</ol>

<div class="callout">
  <h3>Ready to start?</h3>
  <p>The online application takes about fifteen minutes if you have your results to hand.</p>
  <a class="btn btn--primary" href="%APPLY%">Apply now <svg><use href="#i-arrow"/></svg></a>
</div>

<h2 id="requirements">Entry requirements</h2>
<p>Team University applies the standard Ugandan higher-education entry routes. The table below is the general position. Some programmes, particularly in health sciences, carry additional subject requirements set by their professional council, so always confirm with the faculty before you apply.</p>

<div class="table-scroll">
<table class="data">
  <caption>General entry routes. Programme-specific requirements may be higher.</caption>
  <thead>
    <tr><th scope="col">Award</th><th scope="col">Usual entry route</th></tr>
  </thead>
  <tbody>
    <tr><td>Certificate</td><td>Uganda Certificate of Education (UCE) with passes, or equivalent</td></tr>
    <tr><td>Diploma</td><td>UACE with at least one principal pass and two subsidiaries, or a relevant certificate</td></tr>
    <tr><td>Bachelor's degree</td><td>UACE with at least two principal passes obtained at the same sitting, or a relevant diploma for direct entry</td></tr>
    <tr><td>Postgraduate</td><td>A recognised bachelor's degree in a relevant field</td></tr>
    <tr><td>Mature age</td><td>Mature age entry examination for applicants aged 25 and above who do not hold the usual qualifications</td></tr>
  </tbody>
</table>
</div>

<h2 id="documents">Documents you need</h2>
<ul class="bullets">
  <li>Your UCE and UACE result slips or certificates, or their equivalents</li>
  <li>Certificates and transcripts for any diploma or degree you are using to enter</li>
  <li>A national identity card or passport</li>
  <li>A passport photograph</li>
  <li>For postgraduate applicants, a transcript of your first degree</li>
</ul>
<p>Scans or clear photographs are accepted for the application itself. Originals are verified when you report to campus, and an admission stays provisional until the university has seen them.</p>

<h2 id="scholarships">Scholarships</h2>
<div class="callout callout--gold">
  <h3>50% scholarships &mdash; August 2026 intake</h3>
  <p>Team University is offering <strong>half-fee scholarships on selected
     programmes</strong> for the August 2026 intake. Places are limited, and
     awards are made on academic merit and demonstrated need.</p>
  <p>Which programmes are covered changes with each intake, so ask the
     admissions office before you apply &mdash; they will tell you whether the
     programme you want is on this round's list and what your application needs
     to show. Applying for a scholarship does not delay your admission: you
     apply for the programme in the normal way and raise the scholarship with
     admissions at the same time.</p>
  <p><a class="btn btn--primary" href="%APPLY%">Apply now</a>
     <a class="btn btn--line" href="contact.html">Ask about the scholarship</a></p>
</div>

<h2 id="fees">Fees</h2>
<!-- TODO: Replace with the current fees structure per programme and study mode
     once the bursar confirms the figures. Do not publish invented amounts. -->
<div class="callout">
  <h3>Current fees structure</h3>
  <p>Tuition and functional fees vary by programme and study mode, and are set each academic year. The fees structure is issued with your admission letter, and the finance office will send it to you on request before you apply.</p>
  <a class="btn btn--line" href="contact.html">Request the fees structure</a>
</div>
<p>Once you are registered, your fee statement, payments and outstanding balance are visible any time in the <a href="%PORTAL%">student portal</a>. You do not need to visit the finance office for a statement.</p>

<h2 id="intakes">Intakes</h2>
<p>The <strong>August 2026 intake is open for registration now</strong>, and it
   is the intake carrying the 50% scholarships above.</p>
<p>Team University admits students <strong>three times a year</strong> &mdash; in
   February, in May and in August. Not every programme takes students at every
   intake, so if the one you want is not admitting this round, ask the
   admissions office which intake it next opens for rather than waiting a
   whole year on an assumption.</p>

<h2 id="faq">Common questions</h2>
<div class="faq">
  <details>
    <summary>Do I need an account before I can apply?</summary>
    <p>No. You complete the application form without creating an account. A student portal login is created for you automatically if you are admitted, and the details are emailed to you with your admission letter.</p>
  </details>
  <details>
    <summary>Can I work while studying?</summary>
    <p>Yes, and most of our students do. The evening, weekend and distance schedules exist for exactly this reason. Health programmes with supervised placements are the main exception, because placement times are fixed.</p>
  </details>
  <details>
    <summary>Can I change my study mode later?</summary>
    <p>Yes. You choose your mode at registration and can change it between semesters if your work or family circumstances change. Speak to your faculty before the registration window closes.</p>
  </details>
  <details>
    <summary>I have a diploma. Can I enter a degree directly?</summary>
    <p>Usually yes, where the diploma is in a relevant field. Direct entry is decided by the faculty on the strength of your transcript, so send it with your application.</p>
  </details>
  <details>
    <summary>I finished school a long time ago and do not have the usual passes.</summary>
    <p>Mature age entry exists for applicants aged 25 and above. You sit a mature age entry examination instead of presenting UACE results. Contact the admissions office for the next sitting.</p>
  </details>
  <details>
    <summary>Do you admit students from outside Uganda?</summary>
    <p>Yes. Applicants with qualifications from outside Uganda need an equating certificate from the Uganda National Examinations Board, and the admissions office will tell you what else is required for your country.</p>
  </details>
</div>
""".replace("%APPLY%", APPLY).replace("%PORTAL%", PORTAL),
    related([
        ("academics.html", "Browse programmes"),
        ("student-life.html", "Life on campus"),
        ("contact.html", "Talk to admissions"),
    ]),
)


# ==========================================================================
# STUDENT LIFE
# ==========================================================================

STUDENT_LIFE = page_body(
    banner("Student life",
           "A city campus, a student body that mostly works, and the support services that make studying alongside a job possible.",
           [("Student Life", "student-life.html")], image="street",
           alt="The street outside Team University in Mengo, Kampala"),
    sidenav("On this page", [
        ("#campus", "The campus", True),
        ("#support", "Student support", False),
        ("#guild", "Student leadership", False),
        ("#digital", "Digital services", False),
        ("#accommodation", "Accommodation", False),
    ]),
    """<h2 id="campus">The campus</h2>
<p>Team University sits at Wood House Mengo on Kabaka A'njagala Road, inside Kampala rather than out on the edge of it. That matters more than it sounds: an evening student can leave an office in the city centre and be in a lecture without a long commute, and a weekend student travelling in from outside Kampala can reach the campus on the main Rubaga routes.</p>

<figure class="lead-figure">
  <picture>
    <source type="image/webp" srcset="img/campus-998.webp">
    <img src="img/campus-998.jpg" alt="The Team University campus buildings seen from the road in Mengo" width="998" height="459" loading="lazy">
  </picture>
  <figcaption>The campus at Wood House Mengo, a short distance from the city centre.</figcaption>
</figure>

<h2 id="support">Student support</h2>
<p>The Dean of Students' office is the first place to go with anything that is not strictly academic: welfare, personal difficulty, disputes, or simply not knowing who to ask. Academic questions belong with your faculty and your lecturers, and anything to do with registration, results or transcripts belongs with the Academic Registrar.</p>
<ul class="bullets">
  <li><strong>Dean of Students.</strong> Welfare, personal support and student affairs.</li>
  <li><strong>Faculty offices.</strong> Programme advice, course unit choice, academic difficulty.</li>
  <li><strong>Academic Registrar.</strong> Registration, examinations, results and transcripts.</li>
  <li><strong>Finance office.</strong> Fees, payment arrangements and statements.</li>
</ul>

<h2 id="guild">Student leadership</h2>
<p>Students elect a guild leadership that represents them to the university administration and organises student activities across the year. The guild is the formal route for raising a concern that affects students as a group rather than one individual.</p>
<!-- TODO: Add the current Guild President, the guild cabinet and the year's
     activity calendar once the guild office supplies them. -->

<h2 id="digital">Digital services</h2>
<p>Most university business is done online, which for a working student is the difference between a task and a lost afternoon.</p>
<ul class="bullets">
  <li><a href="%PORTAL%">Student portal</a> for registration, results, CGPA, fee statements and your admission documents.</li>
  <li><a href="%ELEARN%">E-learning</a> for lecture materials, assignments and submissions.</li>
  <li><a href="%ELIB%">E-library</a> for journals, reference texts and past papers.</li>
</ul>
<p>Your portal login is created for you when you are admitted and emailed with your admission letter. A one-time code is sent to your email at sign-in, so keep the address you applied with active.</p>

<h2 id="accommodation">Accommodation</h2>
<p>Team University is a city campus and most students live in the surrounding areas of Mengo, Rubaga and Kampala generally. The Dean of Students' office can point new students towards hostels and rentals near the campus.</p>
<div class="callout">
  <h3>Arriving from outside Kampala?</h3>
  <p>Ask the Dean of Students' office about accommodation before you report, particularly if you are joining the day programme and will be on campus during the week.</p>
  <a class="btn btn--line" href="contact.html">Contact the university</a>
</div>
""".replace("%PORTAL%", PORTAL).replace("%ELEARN%", ELEARN).replace("%ELIB%", ELIB),
    related([
        ("admissions.html", "How to apply"),
        ("academics.html", "Programmes"),
        ("contact.html", "Contact us"),
    ]),
)


# ==========================================================================
# NEWS
# ==========================================================================

NEWS = page_body(
    banner("News and events",
           "Announcements from the university, intake notices and events from around the campus.",
           [("News", "news.html")], image="grad",
           alt="Graduation day at Team University"),
    sidenav("News", [
        ("news.html", "All news", True),
        ("admissions.html", "Admissions notices", False),
        ("academics.html", "Academic calendar", False),
    ]),
    """<h2>Latest</h2>
<!-- TODO: This page currently carries one real notice. Replace and extend it
     with the university's own news as it is published. Each item follows the
     same markup: date, heading, one paragraph, optional photograph. -->

<div class="news-list">
  <article class="news-item">
    <picture>
      <source type="image/webp" srcset="img/graduation-2-640.webp">
      <img src="img/graduation-2-640.jpg" alt="Graduands at Team University" width="640" height="630" loading="lazy">
    </picture>
    <div>
      <p class="news-date">Scholarships &middot; August 2026 intake</p>
      <h3>50% scholarships offered on selected programmes</h3>
      <p>Team University is offering half-fee scholarships on selected programmes
         for the August 2026 intake, awarded on academic merit and demonstrated
         need. Places are limited. Which programmes are covered changes with each
         intake, so ask the admissions office before you apply.</p>
      <p><a href="admissions.html#scholarships">See what the scholarship covers</a></p>
    </div>
  </article>

  <article class="news-item">
    <picture>
      <source type="image/webp" srcset="img/grad-800.webp">
      <img src="img/grad-800.jpg" alt="Graduands in procession at Team University" width="800" height="373" loading="lazy">
    </picture>
    <div>
      <p class="news-date">Admissions notice</p>
      <h3>August 2026 intake open for registration</h3>
      <p>Applications are open for the August 2026 intake across all six faculties, on the day, evening, weekend and distance schedules. Applicants can apply online or collect a form at the Mengo campus.</p>
      <p><a href="admissions.html">Read how to apply</a></p>
    </div>
  </article>

  <article class="news-item">
    <picture>
      <source type="image/webp" srcset="img/campus-group-640.webp">
      <img src="img/campus-group-640.jpg" alt="Students on the Team University campus" width="640" height="360" loading="lazy">
    </picture>
    <div>
      <p class="news-date">Academics</p>
      <h3>All 99 programmes now searchable online</h3>
      <p>Every programme the university runs &mdash; across Graduate Studies,
         Management and Humanities, Applied Science and Technology, Health
         Sciences, Education, and Vocational and Technical Education &mdash; can
         now be searched on one page, with the award, its duration and the board
         that assesses it.</p>
      <p><a href="programmes.html">Search the programmes</a></p>
    </div>
  </article>
</div>

<div class="callout">
  <h3>More news as it is published</h3>
  <p>Graduation notices, events, research and press items go here. Each item
     takes a date, a heading, a short summary and an optional photograph &mdash;
     send them to the communications office and they will be added.</p>
</div>
""",
    related([
        ("admissions.html", "Admissions"),
        ("about.html", "About the university"),
        ("contact.html", "Media enquiries"),
    ]),
)


# ==========================================================================
# CONTACT
# ==========================================================================

CONTACT = page_body(
    banner("Contact us",
           "Find the campus, reach the right office, or send a question and someone will come back to you.",
           [("Contact", "contact.html")], image="gate",
           alt="The main gate of Team University on Kabaka A'njagala Road"),
    sidenav("On this page", [
        ("#reach", "How to reach us", True),
        ("#offices", "Which office to ask", False),
        ("#enquiry", "Send an enquiry", False),
        ("#find", "Finding the campus", False),
    ]),
    """<h2 id="reach">How to reach us</h2>

<div class="contact-block">
  <div class="contact-row">
    <svg><use href="#i-pin"/></svg>
    <div>
      <h3>Campus</h3>
      <p>Wood House Mengo, Plot 446 Kabaka A'njagala Road, Mengo-Rubaga, Kampala, Uganda</p>
    </div>
  </div>
  <div class="contact-row">
    <svg><use href="#i-phone"/></svg>
    <div>
      <h3>Telephone</h3>
      <p><a href="tel:+256782752226">+256 782 752226</a> &nbsp; <a href="tel:+256704310224">+256 704 310224</a></p>
    </div>
  </div>
  <div class="contact-row">
    <svg><use href="#i-mail"/></svg>
    <div>
      <h3>Email</h3>
      <p><a href="mailto:info@teamuniversity.ac.ug">info@teamuniversity.ac.ug</a></p>
    </div>
  </div>
</div>

<h2 id="offices">Which office to ask</h2>
<p>Sending your question to the right office is the fastest way to get an answer.</p>
<div class="table-scroll">
<table class="data">
  <thead><tr><th scope="col">If your question is about</th><th scope="col">Ask</th></tr></thead>
  <tbody>
    <tr><td>Applying, entry requirements, admission letters</td><td>Admissions office</td></tr>
    <tr><td>Registration, results, transcripts, certificates</td><td>Academic Registrar</td></tr>
    <tr><td>Fees, payments and statements</td><td>Finance office</td></tr>
    <tr><td>Programme choice, course units, academic difficulty</td><td>Your faculty</td></tr>
    <tr><td>Welfare, personal matters, student affairs</td><td>Dean of Students</td></tr>
    <tr><td>Portal or e-learning access</td><td>ICT support, through your faculty</td></tr>
  </tbody>
</table>
</div>

<h2 id="enquiry">Send an enquiry</h2>
<p>Fill this in and the relevant office will come back to you. If you are ready to apply, use the <a href="%APPLY%">application form</a> instead.</p>

<!-- TODO: This form needs a destination before it will send anything. On PHP
     hosting, point action at a small mail script; otherwise use a form service.
     Until then it is inert and the note below tells visitors to email. -->
<form class="enquiry" method="post" action="#" novalidate>
  <div class="field">
    <label for="f-name">Your name</label>
    <input type="text" id="f-name" name="name" autocomplete="name" required>
  </div>
  <div class="field">
    <label for="f-email">Email address</label>
    <input type="email" id="f-email" name="email" autocomplete="email" required>
    <span class="hint">We reply to this address, so please check it is correct.</span>
  </div>
  <div class="field">
    <label for="f-phone">Telephone</label>
    <input type="tel" id="f-phone" name="phone" autocomplete="tel">
  </div>
  <div class="field">
    <label for="f-topic">What is your question about?</label>
    <select id="f-topic" name="topic">
      <option>Applying and admissions</option>
      <option>Programmes and study modes</option>
      <option>Fees and payments</option>
      <option>Registration and results</option>
      <option>Something else</option>
    </select>
  </div>
  <div class="field">
    <label for="f-message">Your question</label>
    <textarea id="f-message" name="message" required></textarea>
  </div>
  <button class="btn btn--solid" type="submit">Send enquiry <svg><use href="#i-arrow"/></svg></button>
  <p class="hint" style="margin-top:.9rem">You can also email <a href="mailto:info@teamuniversity.ac.ug">info@teamuniversity.ac.ug</a> directly.</p>
</form>

<h2 id="find">Finding the campus</h2>
<p>The campus is on Kabaka A'njagala Road in Mengo-Rubaga, served by the main Rubaga routes and a short distance from the city centre. Look for the gate marked Team University.</p>
<div class="map">
  <iframe title="Map showing Team University, Mengo-Rubaga, Kampala" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Kabaka+Anjagala+Road+Mengo+Rubaga+Kampala&output=embed"></iframe>
</div>
""".replace("%APPLY%", APPLY),
    related([
        ("admissions.html", "How to apply"),
        ("academics.html", "Programmes"),
        ("about.html", "About the university"),
    ]),
)


# ==========================================================================
# Registry: filename -> (title, description, body, extra head)
# ==========================================================================

JSONLD_HOME = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollegeOrUniversity",
  "name": "Team University",
  "alternateName": "Team University Kampala",
  "slogan": "Empower For Generations",
  "url": "https://teamuniversity.ac.ug/",
  "logo": "https://teamuniversity.ac.ug/img/crest.png",
  "email": "info@teamuniversity.ac.ug",
  "telephone": "+256782752226",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Wood House Mengo, Plot 446, Kabaka A'njagala Road, Mengo-Rubaga",
    "addressLocality": "Kampala",
    "addressCountry": "UG"
  },
  "sameAs": [
    "https://www.facebook.com/teamuniversitykampala",
    "https://twitter.com/TeamUniversityU"
  ]
}
</script>
"""

PAGES = {
    "index.html": dict(
        title="Team University Kampala | 99 Programmes, Day, Evening, Weekend and Distance",
        og_title="Team University Kampala",
        description="Team University is a Kampala university offering 99 programmes across six faculties on day, evening, weekend and distance schedules. The August 2026 intake is open, with 50% scholarships on selected programmes.",
        body=home.body(),
        preload='<link rel="preload" as="image" href="img/graduation-1-640.jpg">\n',
        jsonld=JSONLD_HOME,
        scripts='<script src="js/home.js" defer></script>\n',
    ),
    "about.html": dict(
        title="About | Team University Kampala",
        og_title="About Team University",
        description="Who we are, our vision and mission, our values and how Team University maintains academic standards.",
        body=ABOUT,
    ),
    "academics.html": dict(
        title="Academics | Team University Kampala",
        og_title="Academics at Team University",
        description="Six faculties, 99 programmes, four study modes and the academic year at Team University Kampala. Browse programmes by faculty.",
        body=ACADEMICS_PAGE,
    ),
    "faculty-business.html": dict(
        title="Faculty of Business and Management | Team University",
        og_title="Faculty of Business and Management",
        description="Accounting and finance, business administration, procurement and logistics at Team University Kampala, from certificate to postgraduate.",
        body=BUSINESS,
    ),
    "faculty-health.html": dict(
        title="School of Health Sciences | Team University",
        og_title="School of Health Sciences",
        description="Clinical and community health training with supervised practical placements at Team University Kampala.",
        body=HEALTH,
    ),
    "faculty-applied.html": dict(
        title="Faculty of Applied Sciences | Team University",
        og_title="Faculty of Applied Sciences",
        description="Computing, information technology and applied sciences programmes at Team University Kampala.",
        body=APPLIED,
    ),
    "faculty-social.html": dict(
        title="Faculty of Social Sciences | Team University",
        og_title="Faculty of Social Sciences",
        description="Social work, public administration and development studies at Team University Kampala.",
        body=SOCIAL,
    ),
    "admissions.html": dict(
        title="Admissions | Team University Kampala",
        og_title="Admissions at Team University",
        description="How to apply to Team University Kampala, entry requirements, the documents you need and the August 2026 intake.",
        body=ADMISSIONS,
    ),
    "student-life.html": dict(
        title="Student life | Team University Kampala",
        og_title="Student life at Team University",
        description="The campus at Mengo, student support, guild leadership, digital services and accommodation at Team University Kampala.",
        body=STUDENT_LIFE,
    ),
    "news.html": dict(
        title="News and events | Team University Kampala",
        og_title="News and events",
        description="Announcements, intake notices and events from Team University Kampala.",
        body=NEWS,
    ),
    "contact.html": dict(
        title="Contact us | Team University Kampala",
        og_title="Contact Team University",
        description="Reach Team University Kampala: campus address at Mengo, telephone, email, which office to ask and how to find us.",
        body=CONTACT,
    ),
}

# The six faculty pages and the full programme list are generated from the
# university%s own catalogue, so they cannot drift from the registry.
PAGES.update(faculties.specs())
