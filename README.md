# Team University website

The public website for Team University, Kampala (`teamuniversity.ac.ug`).

Plain HTML, CSS and JavaScript. No framework, no build tools to install, no
database. It runs on any hosting that can serve files, which means it works on
shared cPanel hosting and on an nginx server without changes.

## What to upload

Everything except `_src/`, `README.md` and `TODO.md`:

```
*.html      the eleven pages
css/        site.css (base) and pages.css (inner pages)
js/         site.js
img/        photographs, crest, WebP and JPEG variants
fonts/      the Outfit variable font, self-hosted
```

Upload to the web root (usually `public_html`). `index.html` becomes the home
page automatically.

## Editing

Change text directly in the `.html` files if you only need a word or two.

For anything shared across pages, the navigation, the footer or a new page,
edit `_src/pages.py` (the content) or `_src/build.py` (the shell), then run:

```
python _src/build.py
```

That rewrites all eleven `.html` files from one template, so the navigation and
footer can never drift apart. Python 3 with no extra packages.

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `about.html` | About the university |
| `academics.html` | Faculties, study modes, academic year |
| `faculty-business.html` | Faculty of Business and Management |
| `faculty-health.html` | School of Health Sciences |
| `faculty-applied.html` | Faculty of Applied Sciences |
| `faculty-social.html` | Faculty of Social Sciences |
| `admissions.html` | How to apply, requirements, fees, FAQ |
| `student-life.html` | Campus, support, guild, digital services |
| `news.html` | News and events |
| `contact.html` | Contacts, offices, enquiry form, map |

## Notes

- **No outside requests.** Fonts and icons are served from this site, so the
  pages load quickly on Ugandan mobile data and keep working if a third party
  goes down. The only external element is the Google map on the contact page.
- **Images** are served as WebP with a JPEG fallback, at 800px and 1020px.
  `_src/build.py` expects both widths for every photo used in a banner.
- **Icons** are Phosphor Icons (MIT), inlined once per page as an SVG sprite.
- **Type** is Outfit (SIL Open Font License), self-hosted as one variable font.
- Light and dark mode both supported. Motion respects `prefers-reduced-motion`.

## Outstanding content

See `TODO.md`. Several sections are deliberately marked as awaiting information
from the university rather than filled with invented detail.
