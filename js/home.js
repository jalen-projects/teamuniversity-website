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
   * THE HERO FOOTAGE, SLOWED
   * The graduation clip is cut fast — good for a highlights reel, wrong
   * behind a headline somebody is trying to read. Half speed turns the same
   * footage into something calm without needing different footage, and the
   * browser resamples it smoothly.
   * ------------------------------------------------------------------ */
  (function calmHero() {
    var video = document.querySelector('.hero-video');
    if (!video) return;
    function slow() { try { video.playbackRate = 0.5; } catch (e) {} }
    slow();
    // Some browsers reset the rate when the source loads or the loop wraps.
    video.addEventListener('loadedmetadata', slow);
    video.addEventListener('play', slow);
    video.addEventListener('seeked', slow);
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
