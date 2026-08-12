"""
THE UNIVERSITY'S OWN CATALOGUE
==============================
Six faculties and ninety-nine programmes, taken from the same list the
university's student system is seeded from (`seed_team_catalogue`), so the
website and the registry cannot drift apart. Nothing here is invented: if a
programme is on this page it is on the university's books.

The website previously showed four faculties. Team has six — Graduate Studies,
Education and TVET were missing entirely, which is most of the postgraduate
and vocational offer left off the university's own front door.
"""

import json
import pathlib

DATA = json.loads(
    (pathlib.Path(__file__).resolve().parent / "programmes.json").read_text(encoding="utf-8"))

# code -> (page, short title, blurb, icon, photo stem)
FACULTIES = {
    "SGSR": ("faculty-graduate.html", "Graduate Studies and Research",
             "Masters and postgraduate diplomas for people already working, "
             "taught in the evening and at weekends.",
             "i-cap", "graduation-2"),
    "FMH": ("faculty-business.html", "Management and Humanities",
            "Business, accounting, procurement, human resource, economics and "
            "the humanities — the faculty most of Kampala studies in.",
            "i-briefcase", "campus-group"),
    "FAST": ("faculty-applied.html", "Applied Science and Technology",
             "Computer science, information technology, software engineering, "
             "environmental science and agriculture.",
             "i-cpu", "technology"),
    "SHS": ("faculty-health.html", "Health Sciences",
            "Clinical, nursing and public-health training for Uganda's health "
            "service.",
            "i-heart", "campus-study"),
    "FED": ("faculty-education.html", "Education",
            "Training the teachers of the new lower-secondary curriculum, in "
            "arts, sciences and early childhood.",
            "i-book", "campus-life"),
    "TVET": ("faculty-tvet.html", "Vocational and Technical Education",
             "Hands-on certificates and diplomas that put a trade in your "
             "hands — catering, tailoring, electrical, motor vehicle and more.",
             "i-wrench", "campus-walk"),
}

LEVELS = [
    ("MASTERS", "Masters"),
    ("POSTGRAD_DIPLOMA", "Postgraduate Diploma"),
    ("BACHELOR", "Bachelors"),
    ("DIPLOMA", "Diploma"),
    ("CERTIFICATE", "Certificate"),
]
LEVEL_NAME = dict(LEVELS)

# Which examinations board awards it. A UBTEB or UNMEB award is a different
# thing from a university degree and an applicant deserves to see which.
BOARD_NAME = {
    "UNIVERSITY": "Team University",
    "UVTAB": "UVTAB",      # Uganda Vocational and Technical Assessment Board
    "UHPAB": "UHPAB",      # Uganda Health Professionals Assessment Board
    "HEC": "HEC",          # Higher Education Certificate
}


def programmes(faculty=None, level=None):
    rows = DATA["programmes"]
    if faculty:
        rows = [r for r in rows if r["faculty"] == faculty]
    if level:
        rows = [r for r in rows if r["level"] == level]
    order = [code for code, _label in LEVELS]
    return sorted(rows, key=lambda r: (order.index(r["level"])
                                       if r["level"] in order else 9, r["name"]))


def by_level(faculty):
    """[(level label, [programmes])] for one faculty, biggest award first."""
    out = []
    for code, label in LEVELS:
        rows = programmes(faculty, code)
        if rows:
            out.append((label, rows))
    return out


def count(faculty=None):
    return len(programmes(faculty))


def faculty_name(code):
    return DATA["faculties"][code]


def all_faculties():
    """[(code, page, short title, blurb, icon, photo, programme count)]"""
    return [(code, *FACULTIES[code], count(code)) for code in FACULTIES]


def duration(row):
    years = row["years"]
    if row["level"] == "CERTIFICATE" and years <= 1:
        return "1 year"
    return f"{years} year{'s' if years != 1 else ''}"


def search_index():
    """Every programme as one flat row for the finder's JSON payload."""
    return [
        {
            "n": row["name"],
            "c": row["code"],
            "f": FACULTIES[row["faculty"]][1],
            "p": FACULTIES[row["faculty"]][0],
            "l": LEVEL_NAME.get(row["level"], row["level"]),
            "d": duration(row),
            "b": BOARD_NAME.get(row["board"], row["board"]),
        }
        for row in programmes()
    ]
