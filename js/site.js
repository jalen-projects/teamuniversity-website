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
     Seven seconds a slide, caption changes with the picture, pauses on hover
     and when the tab is hidden, and swipes on a phone. */
  (function slider() {
    var hero = document.getElementById('hero');
    if (!hero) { return; }
    var slides = hero.querySelectorAll('.slide');
    var caps = hero.querySelectorAll('.cap');
    var dots = hero.querySelectorAll('.hero-dots button');
    if (slides.length < 2) { return; }
    var at = 0, timer = null, HOLD = 7000;

    function show(n) {
      at = (n + slides.length) % slides.length;
      for (var i = 0; i < slides.length; i++) {
        slides[i].classList.toggle('is-on', i === at);
        if (caps[i]) { caps[i].classList.toggle('is-on', i === at); }
        if (dots[i]) { dots[i].classList.toggle('is-on', i === at); }
      }
    }
    function start() { if (!reduced && !timer) { timer = setInterval(function () { show(at + 1); }, HOLD); } }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function go(n) { stop(); show(n); start(); }

    hero.querySelector('.hero-arrow--prev').addEventListener('click', function () { go(at - 1); });
    hero.querySelector('.hero-arrow--next').addEventListener('click', function () { go(at + 1); });
    Array.prototype.forEach.call(dots, function (d, i) { d.addEventListener('click', function () { go(i); }); });
    hero.addEventListener('mouseenter', stop);
    hero.addEventListener('mouseleave', start);
    document.addEventListener('visibilitychange', function () { if (document.hidden) { stop(); } else { start(); } });

    var x0 = null;
    hero.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      if (x0 === null) { return; }
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) { go(dx < 0 ? at + 1 : at - 1); }
      x0 = null;
    });
    start();
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
