/* Team University - site behaviour.
   No dependencies. No scroll event listeners: everything observable is done
   with IntersectionObserver so scrolling stays smooth on low-end phones. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Current year in the footer -------------------------------------- */
  var year = document.getElementById('year');
  if (year) { year.textContent = new Date().getFullYear(); }

  /* --- Mobile navigation ------------------------------------------------ */
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  var navIcon = document.getElementById('navIcon');
  var masthead = document.getElementById('masthead');

  function setNav(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    navIcon.innerHTML = '<use href="#' + (open ? 'i-close' : 'i-menu') + '"/>';
    document.body.style.overflow = open ? 'hidden' : '';
  }

  if (toggle && nav) {
    /* The drawer opens below the whole header stack, so measure it rather
       than hard-coding a height that breaks when the utility bar wraps. */
    function placeDrawer() {
      var rect = masthead.getBoundingClientRect();
      nav.style.setProperty('--nav-top', Math.max(0, rect.bottom) + 'px');
    }
    placeDrawer();
    window.addEventListener('resize', placeDrawer);

    toggle.addEventListener('click', function () {
      placeDrawer();
      setNav(!nav.classList.contains('is-open'));
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { setNav(false); }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setNav(false);
        toggle.focus();
      }
    });

    /* Leaving mobile width with the drawer open would trap the scroll lock. */
    window.matchMedia('(min-width: 1025px)').addEventListener('change', function (e) {
      if (e.matches) { setNav(false); }
    });
  }

  /* --- Academics dropdown ------------------------------------------------
     Click to open on desktop (hover-only menus are unusable on touch), and an
     accordion inside the mobile drawer. */
  var dropdowns = Array.prototype.slice.call(document.querySelectorAll('[data-dropdown]'));

  dropdowns.forEach(function (dd) {
    var btn = dd.querySelector('button');
    if (!btn) { return; }
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = dd.classList.contains('is-open');
      dropdowns.forEach(function (o) {
        o.classList.remove('is-open');
        o.querySelector('button').setAttribute('aria-expanded', 'false');
      });
      if (!open) {
        dd.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  if (dropdowns.length) {
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-dropdown]')) { return; }
      dropdowns.forEach(function (dd) {
        /* Inside the mobile drawer the section stays expanded: collapsing it
           on any outside tap would fight the user. */
        if (window.innerWidth <= 1024) { return; }
        dd.classList.remove('is-open');
        dd.querySelector('button').setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') { return; }
      dropdowns.forEach(function (dd) {
        if (!dd.classList.contains('is-open')) { return; }
        dd.classList.remove('is-open');
        var b = dd.querySelector('button');
        b.setAttribute('aria-expanded', 'false');
        b.focus();
      });
    });
  }

  /* --- Header shadow once the page has moved ---------------------------- */
  if (masthead && 'IntersectionObserver' in window) {
    var sentinel = document.createElement('div');
    sentinel.setAttribute('aria-hidden', 'true');
    sentinel.style.cssText = 'position:absolute;top:0;height:1px;width:1px';
    document.body.prepend(sentinel);
    new IntersectionObserver(function (entries) {
      masthead.classList.toggle('is-stuck', !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(sentinel);
  }

  /* --- Reveal on scroll -------------------------------------------------
     Motion here has one job: let each section land as its own moment rather
     than arriving pre-assembled. Anything already on screen at load stays
     visible, and users who ask for less motion get none. */
  var revealables = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealables.forEach(function (el) { io.observe(el); });
  }
})();
