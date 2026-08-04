# Content still needed from Team University

The site is built and every page works. These items are placeholders. Nothing
on the site invents a fact about the university: where information was not
available, the page says so and asks the reader to contact the relevant office.
Replace each item below before the site goes live.

## Must have before launch

| Page | What is missing |
|---|---|
| `about.html` | **Leadership.** Names, titles and photographs of the office holders, plus a message from the Vice Chancellor. Currently a notice saying the section awaits content. |
| `faculty-health.html` | **Programme list.** The School of Health Sciences has one placeholder row. Needs the real programmes, codes, awards, and which professional council registers each one. This is the least complete page. |
| `admissions.html` | **Fees structure.** Tuition and functional fees per programme and study mode. The page currently tells applicants to request it from the finance office. Do not publish invented figures. |
| `contact.html` | **Enquiry form destination.** The form has no `action` and cannot send. On PHP hosting point it at a small mail script; otherwise use a form service. Until then the page tells visitors to email instead. |
| `academics.html` | **Academic almanac.** Registration, teaching, examination and recess dates for the year. |

## Should have soon

- **Higher-resolution photographs.** The four photos we hold are about 1020px
  wide, so banners look slightly soft on a large monitor. Their photographer
  will have the originals. Same photos, bigger files, no redesign needed.
- **More photography.** Classrooms, laboratories, the library, students at
  work, staff. Every faculty page currently reuses one of four campus photos.
- **News items** for `news.html`. It carries one real notice (the August 2026
  intake) and is ready for more.
- **Guild leadership** and the student activity calendar for `student-life.html`.
- **Programme detail** for Social Sciences and Applied Sciences: several rows
  say "See faculty" rather than naming each award.

## Verify before launch

- Confirm the **YouTube channel URL** in the footer. It is a best guess
  (`youtube.com/@teamuniversity`) and must be checked.
- Confirm every **programme title and code** against the current prospectus.
- Confirm the **entry requirements** table matches what admissions actually
  applies. It currently states the standard national routes.

## Separate issue, not about this site

The existing WordPress site at teamuniversity.ac.ug is serving injected spam in
German, Bengali, French and Turkish. That is a compromised install. Whoever
runs it should change the WordPress and cPanel passwords regardless of whether
this new site replaces it.
