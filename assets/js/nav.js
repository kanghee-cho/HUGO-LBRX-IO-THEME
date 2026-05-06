/**
 * nav.js — Hamburger menu toggle for mobile navigation [#169]
 *
 * Selectors (data attributes):
 *   [data-nav-toggle]     — hamburger button
 *   [data-nav-menu]       — mobile dropdown panel
 *   [data-nav-icon-open]  — hamburger icon (3 lines)
 *   [data-nav-icon-close] — X icon
 */
(function () {
  'use strict';

  const toggle = document.querySelector('[data-nav-toggle]');
  const menu = document.querySelector('[data-nav-menu]');
  if (!toggle || !menu) return;

  const iconOpen = toggle.querySelector('[data-nav-icon-open]');
  const iconClose = toggle.querySelector('[data-nav-icon-close]');

  function isOpen() {
    return !menu.hidden;
  }

  function openMenu() {
    menu.hidden = false;
    toggle.setAttribute('aria-expanded', 'true');
    iconOpen.classList.add('hidden');
    iconClose.classList.remove('hidden');
    // Trap focus in menu on next frame
    requestAnimationFrame(() => {
      const firstLink = menu.querySelector('a');
      if (firstLink) firstLink.focus();
    });
  }

  function closeMenu() {
    menu.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
    iconOpen.classList.remove('hidden');
    iconClose.classList.add('hidden');
  }

  // Hamburger button click
  toggle.addEventListener('click', () => {
    isOpen() ? closeMenu() : openMenu();
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen()) {
      closeMenu();
      toggle.focus();
    }
  });

  // Close on click outside
  document.addEventListener('click', (e) => {
    if (isOpen() && !menu.contains(e.target) && !toggle.contains(e.target)) {
      closeMenu();
    }
  });

  // Close and reset when viewport expands to md+ (768px)
  const mq = window.matchMedia('(min-width: 768px)');
  mq.addEventListener('change', (e) => {
    if (e.matches) closeMenu();
  });
})();
