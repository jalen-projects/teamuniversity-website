# Content still needed from Team University

The site is built and every page works. Nothing on it invents a fact about the
university: where information was not available, the page says so and asks the
reader to contact the relevant office. Replace each item below before it goes
to print anywhere.

## Must have before launch

| Page | What is missing |
|---|---|
| `about.html` | **Leadership.** Names, titles and photographs of the office holders, plus a message from the Vice Chancellor. Currently a notice saying the section awaits content. This is the biggest remaining gap: every university site the reference points to leads with its VC. |
| `admissions.html` | **Fees structure.** Tuition and functional fees per programme and study mode. The page tells applicants to request it from the finance office. Do not publish invented figures. |
| `admissions.html` | **Which programmes carry the 50% scholarship**, and the closing date for it. The page says to ask admissions, which is honest but weaker than a list. |
| `contact.html` | **Enquiry form destination.** The form has no `action` and cannot send. On PHP hosting point it at a small mail script; otherwise use a form service. Until then the page tells visitors to email instead. |
| `academics.html` | **Academic almanac.** Registration, teaching, examination and recess dates for the year. |

## Should have soon

- **Higher-resolution photographs.** Everything we hold is 550–1000px wide.
  That is why the hero is video and the photographs are used in cards and a
  mosaic rather than as full-width banners — they would go soft. Their
  photographer will have the originals. Same photos, bigger files, no redesign
  needed: drop them in `Desktop/DESIGNS/TEAM/` and re-run
  `python _src/build_media.py`.
- **More photography.** Classrooms, laboratories, the library, students at
  work, staff, each faculty in its own setting. Faculty pages currently share a
  small pool of campus photographs.
- **More video.** The graduation clip carries the hero. Anything else in
  `Desktop/DESIGNS` is 5 MB and up and needs compressing before it goes near a
  page — there is no ffmpeg on the build machine, so that has to be done
  elsewhere.
- **News items** for `news.html`. It carries three real notices now (the
  scholarship, the August intake, the programme index) and is ready for more.
- **Guild leadership** and the student activity calendar for `student-life.html`.

## Done since the first build

- Six faculties, not four. Graduate Studies, Education and Vocational and
  Technical Education were missing entirely — 59 of the 99 programmes.
- Every programme page is generated from the university's own catalogue
  (`_src/catalogue.py`), the same list the student system is seeded from, so
  the site and the registry cannot drift apart.
- A programme finder on the home page and at `programmes.html`.
- Video hero, with the poster served instead below 700px.
- The 50% August scholarship on the home page, the admissions page, all six
  faculty pages and the news page.
- `_src/check.py` — broken links, missing images, duplicate ids, dead anchors,
  images with no alt. Run it before every deploy; it exits non-zero on failure.

## How to work on this site

```
python _src/build_media.py     # photographs and video -> img/ and video/
python _src/build.py           # _src/*.py -> the .html files in the root
python _src/check.py           # verify before uploading
```

Only the built `.html`, `css/`, `js/`, `img/`, `video/` and `fonts/` need to go
on the server. `_src/` is the source and does not.
