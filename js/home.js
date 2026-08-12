/* ==========================================================================
   TEAM UNIVERSITY — HOME
   Three small things: the programme finder, the counting statistics, and the
   reveal-on-scroll. No framework, no dependency, and every one of them checks
   that its own element exists first, so this file is safe to load anywhere.
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------ *
   * THE ROTATING PHRASE
   * Four study modes, one at a time, in the headline. The first is already
   * marked is-on in the HTML, so if this file never loads the sentence still
   * reads correctly — it just stops moving.
   * ------------------------------------------------------------------ */
  (function rotator() {
    var wrap = document.getElementById('rotator');
    if (!wrap || reduced) return;
    var items = wrap.querySelectorAll('span');
    if (items.length < 2) return;
    var at = 0;
    setInterval(function () {
      items[at].classList.remove('is-on');
      at = (at + 1) % items.length;
      items[at].classList.add('is-on');
    }, 2900);
  })();

  /* ------------------------------------------------------------------ *
   * THE HERO SLIDESHOW
   * Four of the university's own photographs, crossfading. Seven seconds a
   * slide, which is long: the complaint about the video it replaced was that
   * it moved too fast. The first slide is already visible from the markup, so
   * if this never runs the hero is a correct still photograph rather than an
   * empty panel.
   * ------------------------------------------------------------------ */
  (function slideshow() {
    var slides = document.querySelectorAll('.hero-media .slide');
    var dots = document.getElementById('heroDots');
    if (slides.length < 2) return;

    var at = 0, timer = null;

    function show(next) {
      slides[at].classList.remove('is-on');
      at = (next + slides.length) % slides.length;
      slides[at].classList.add('is-on');
      if (dots) {
        var buttons = dots.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
          buttons[i].classList.toggle('is-on', i === at);
          buttons[i].setAttribute('aria-selected', i === at ? 'true' : 'false');
        }
      }
    }

    function start() {
      if (reduced) return;                 // one photograph, held, is fine
      stop();
      timer = setInterval(function () { show(at + 1); }, 7000);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    if (dots) {
      for (var i = 0; i < slides.length; i++) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.setAttribute('role', 'tab');
        dot.setAttribute('aria-label', 'Picture ' + (i + 1));
        if (i === 0) { dot.className = 'is-on'; dot.setAttribute('aria-selected', 'true'); }
        (function (index) {
          dot.addEventListener('click', function () { show(index); start(); });
        })(i);
        dots.appendChild(dot);
      }
    }

    // Nothing runs while the tab is in the background: a slideshow ticking
    // over in a tab nobody is looking at is battery spent for no reason.
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { stop(); } else { start(); }
    });
    start();
  })();

  /* ------------------------------------------------------------------ *
   * PROGRAMME FINDER
   * The whole catalogue is already in the page as JSON, so searching is
   * instant and works with no network at all — which matters on a phone
   * holding one bar in a Kampala hostel.
   * ------------------------------------------------------------------ */
  (function finder() {
    var data = document.getElementById('progData');
    var box = document.getElementById('progSearch');
    var out = document.getElementById('progResults');
    if (!data || !box || !out) return;

    var rows;
    try { rows = JSON.parse(data.textContent); } catch (e) { return; }

    var facultySelect = document.getElementById('progFaculty');
    var levelWrap = document.getElementById('progLevels');
    var countEl = document.getElementById('progCount');
    var level = '';

    function escape(text) {
      return String(text).replace(/[&<>"']/g, function (ch) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch];
      });
    }

    function draw() {
      var term = box.value.trim().toLowerCase();
      var faculty = facultySelect ? facultySelect.value : '';
      var hits = rows.filter(function (row) {
        if (level && row.l !== level) return false;
        if (faculty && row.f !== faculty) return false;
        if (!term) return true;
        return (row.n + ' ' + row.c + ' ' + row.f).toLowerCase().indexOf(term) > -1;
      });

      countEl.textContent = hits.length === rows.length
        ? 'Showing all ' + rows.length + ' programmes'
        : hits.length + (hits.length === 1 ? ' programme' : ' programmes') + ' found';

      if (!hits.length) {
        out.innerHTML = '<p class="finder-empty">Nothing matched that. Try a shorter ' +
          'word — "nurs", "account", "tailor" — or clear the filters. If the ' +
          'programme you want is not listed, ask admissions: it may run under ' +
          'another name.</p>';
        return;
      }

      // Built as one string and written once. Appending 99 nodes one at a time
      // is 99 layouts, and it is visible on an older phone.
      var html = hits.map(function (row) {
        return '<a class="prog" href="' + escape(row.p) + '">' +
          '<span class="prog-code">' + escape(row.c) + '</span>' +
          '<span><b>' + escape(row.n) + '</b>' +
          '<span class="prog-meta">' + escape(row.l) + ' &middot; ' +
          escape(row.d) + ' &middot; ' + escape(row.f) +
          (row.b && row.b !== 'Team University' ? ' &middot; ' + escape(row.b) + ' award' : '') +
          '</span></span></a>';
      }).join('');
      out.innerHTML = html;
    }

    var timer;
    box.addEventListener('input', function () {
      // A keystroke should not redraw 99 cards; a pause of a breath should.
      clearTimeout(timer);
      timer = setTimeout(draw, 120);
    });
    if (facultySelect) facultySelect.addEventListener('change', draw);
    if (levelWrap) {
      levelWrap.addEventListener('click', function (event) {
        var chip = event.target.closest('.chip');
        if (!chip) return;
        level = chip.getAttribute('data-level') || '';
        Array.prototype.forEach.call(levelWrap.querySelectorAll('.chip'), function (one) {
          one.classList.toggle('is-on', one === chip);
        });
        draw();
      });
    }
    draw();
  })();

  /* ------------------------------------------------------------------ *
   * COUNTING STATISTICS
   * Counts up once, when the row is actually on screen. Anyone who has
   * asked for reduced motion simply gets the number.
   * ------------------------------------------------------------------ */
  (function counters() {
    var nums = document.querySelectorAll('[data-count]');
    if (!nums.length) return;

    function run(el) {
      var target = parseInt(el.getAttribute('data-count'), 10) || 0;
      if (reduced || !window.requestAnimationFrame) { el.textContent = target; return; }
      var started = null;
      var span = 1100;
      function step(now) {
        if (started === null) started = now;
        var progress = Math.min((now - started) / span, 1);
        // Ease out, so it arrives at the number rather than slamming into it.
        el.textContent = Math.round(target * (1 - Math.pow(1 - progress, 3)));
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    if (!('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(nums, run);
      return;
    }
    var watcher = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        run(entry.target);
        watcher.unobserve(entry.target);
      });
    }, { threshold: .4 });
    Array.prototype.forEach.call(nums, function (el) { watcher.observe(el); });
  })();

  /* ------------------------------------------------------------------ *
   * REVEAL ON SCROLL
   * Classes are added by script, never in the HTML: if this file fails to
   * load, every section is simply visible rather than permanently blank.
   * ------------------------------------------------------------------ */
  (function reveal() {
    if (reduced || !('IntersectionObserver' in window)) return;
    var targets = document.querySelectorAll(
      '.quick-card, .fac-card, .mode-card, .why-card, .gal, .section-head, .scholar-body');
    if (!targets.length) return;

    var watcher = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        watcher.unobserve(entry.target);
      });
    }, { threshold: .12, rootMargin: '0px 0px -40px' });

    Array.prototype.forEach.call(targets, function (el, index) {
      el.classList.add('reveal');
      // A short stagger inside a row, capped so a long grid does not crawl.
      el.style.transitionDelay = Math.min(index % 6, 5) * 60 + 'ms';
      watcher.observe(el);
    });
  })();
})();
