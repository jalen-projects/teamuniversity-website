/* ==========================================================================
   TEAM UNIVERSITY — every page
   Phone drawer, touch-friendly dropdowns, the hero slider and the counters.
   Every block checks its own elements exist, so this file is safe anywhere,
   and nothing here is load-bearing: with JavaScript off the first slide and
   its caption still show and every menu item is still a working link.
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var year = document.getElementById('year');
  if (year) { year.textContent = new Date().getFullYear(); }

  /* --- Phone drawer ------------------------------------------------------ */
  var toggle = document.getElementById('navToggle');
  var drawer = document.getElementById('drawer');
  function setDrawer(open) {
    if (!drawer) { return; }
    drawer.classList.toggle('is-open', open);
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
    if (toggle) { toggle.setAttribute('aria-expanded', open ? 'true' : 'false'); }
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (toggle && drawer) {
    toggle.addEventListener('click', function () { setDrawer(true); });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('[data-close]') || e.target.closest('nav a') || e.target.closest('.drawer-apply')) {
        setDrawer(false);
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) { setDrawer(false); toggle.focus(); }
    });
    window.matchMedia('(min-width: 961px)').addEventListener('change', function (e) {
      if (e.matches) { setDrawer(false); }
    });
  }

  /* --- Desktop dropdowns on touch screens --------------------------------
     Hover opens them with a mouse. A tablet has no hover, so the first tap on
     a parent opens its menu and the second tap follows the link. */
  var parents = document.querySelectorAll('.mainnav .ni > a[aria-haspopup]');
  Array.prototype.forEach.call(parents, function (a) {
    a.addEventListener('touchend', function (e) {
      var item = a.parentNode;
      if (!item.classList.contains('is-open')) {
        e.preventDefault();
        Array.prototype.forEach.call(document.querySelectorAll('.mainnav .ni.is-open'), function (o) { o.classList.remove('is-open'); });
        item.classList.add('is-open');
      }
    });
  });
  document.addEventListener('touchstart', function (e) {
    if (!e.target.closest('.mainnav')) {
      Array.prototype.forEach.call(document.querySelectorAll('.mainnav .ni.is-open'), function (o) { o.classList.remove('is-open'); });
    }
  }, { passive: true });

  /* --- Hero slider ---------------------------------------------------------
     The ribbon under the photo is the clock: its light runs left to right for
     seven seconds, and when it reaches the end three bands in the crest
     colours sweep across the photo and bring in the next one. The caption
     plate changes colour with it. Hover, a hidden tab or a finger on the
     photo pauses the clock where it is; swipe or the arrows go either way. */
  (function slider() {
    var hero = document.getElementById('hero');
    if (!hero) { return; }
    var slides = hero.querySelectorAll('.slide');
    var caps = hero.querySelectorAll('.cap');
    var dots = hero.querySelectorAll('.hero-dots button');
    var bands = hero.querySelectorAll('.hero-wipe i');
    var ribbon = hero.querySelector('.hero-ribbon');
    var now = document.getElementById('heroNow');
    if (slides.length < 2) { return; }
    var TONES = ['blue', 'green', 'navy'];
    var COLOURS = ['#0b55a6', '#f6c021', '#00843d'];
    var at = 0, busy = false, fallback = null;

    function pad(n) { return (n < 9 ? '0' : '') + (n + 1); }

    function mark(to) {
      for (var i = 0; i < slides.length; i++) {
        if (caps[i]) { caps[i].classList.toggle('is-on', i === to); }
        if (dots[i]) { dots[i].classList.toggle('is-on', i === to); }
      }
      hero.setAttribute('data-tone', TONES[to % TONES.length]);
      if (now) { now.textContent = pad(to); }
    }

    /* Restarting a CSS animation needs the class off, a reflow, then on. */
    function clock() {
      if (reduced) { return; }
      if (!ribbon) { clearTimeout(fallback); fallback = setTimeout(function () { show(at + 1, 1); }, 7000); return; }
      ribbon.classList.remove('is-timing');
      void ribbon.offsetWidth;
      ribbon.classList.add('is-timing');
    }

    function show(n, dir) {
      var to = (n + slides.length) % slides.length;
      if (to === at || busy) { return; }
      var from = at;
      at = to;
      mark(to);
      if (reduced) {
        slides[from].classList.remove('is-on');
        slides[to].classList.add('is-on');
        return;
      }
      busy = true;
      /* The bands lead with a different crest colour each time. */
      for (var k = 0; k < bands.length; k++) { bands[k].style.background = COLOURS[(to + k) % COLOURS.length]; }
      hero.classList.toggle('is-back', dir < 0);
      slides[to].classList.add('is-in');
      hero.classList.remove('is-wiping');
      void hero.offsetWidth;
      hero.classList.add('is-wiping');
      if (ribbon) { ribbon.classList.add('is-rolling'); }
      setTimeout(function () {
        slides[from].classList.remove('is-on');
        slides[to].classList.add('is-on');
        slides[to].classList.remove('is-in');
        hero.classList.remove('is-wiping');
        if (ribbon) { ribbon.classList.remove('is-rolling'); }
        busy = false;
      }, 1500);
      clock();
    }

    if (ribbon) {
      ribbon.addEventListener('animationend', function (e) {
        if (e.animationName === 'ribbonTime') { show(at + 1, 1); }
      });
    }

    function pause() { hero.classList.add('is-paused'); }
    function resume() { hero.classList.remove('is-paused'); }

    hero.querySelector('.hero-arrow--prev').addEventListener('click', function () { show(at - 1, -1); });
    hero.querySelector('.hero-arrow--next').addEventListener('click', function () { show(at + 1, 1); });
    Array.prototype.forEach.call(dots, function (d, i) {
      d.addEventListener('click', function () { show(i, i < at ? -1 : 1); });
    });
    hero.addEventListener('mouseenter', pause);
    hero.addEventListener('mouseleave', resume);
    hero.addEventListener('focusin', pause);
    hero.addEventListener('focusout', resume);
    document.addEventListener('visibilitychange', function () { if (document.hidden) { pause(); } else { resume(); } });

    var x0 = null;
    hero.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; pause(); }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      resume();
      if (x0 === null) { return; }
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) { show(dx < 0 ? at + 1 : at - 1, dx < 0 ? 1 : -1); }
      x0 = null;
    });
    clock();
  })();

  /* --- Counting figures ----------------------------------------------------- */
  (function counters() {
    var nums = document.querySelectorAll('[data-count]');
    if (!nums.length || reduced || !('IntersectionObserver' in window)) { return; }
    function run(el) {
      var end = parseInt(el.getAttribute('data-count'), 10), t0 = null;
      function step(now) {
        if (!t0) { t0 = now; }
        var p = Math.min((now - t0) / 1400, 1);
        el.innerHTML = Math.round(end * (1 - Math.pow(1 - p, 3))) + '<sup>+</sup>';
        if (p < 1) { requestAnimationFrame(step); }
      }
      requestAnimationFrame(step);
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { run(en.target); io.unobserve(en.target); } });
    }, { threshold: 0.5 });
    Array.prototype.forEach.call(nums, function (el) { io.observe(el); });
  })();
})();
