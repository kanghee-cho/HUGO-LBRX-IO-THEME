/**
 * theme-toggle.js
 * Handles dark/light mode toggle persistence and Cmd+K search modal.
 * FOUC prevention is handled inline in partials/head.html.
 */
(function () {
  var THEME_KEY = 'lbrx-theme';

  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem(THEME_KEY, theme);
  }

  function toggleTheme() {
    var isDark = document.documentElement.classList.contains('dark');
    applyTheme(isDark ? 'light' : 'dark');
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Dark mode toggle button
    var toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleTheme);
    }

    // Search modal: open button
    var openBtn = document.getElementById('search-open');
    var modal = document.getElementById('search-modal');
    var backdrop = document.getElementById('search-backdrop');

    function openModal() {
      if (!modal) return;
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      if (!modal) return;
      modal.classList.add('hidden');
      document.body.style.overflow = '';
    }

    if (openBtn) {
      openBtn.addEventListener('click', openModal);
    }

    if (backdrop) {
      backdrop.addEventListener('click', closeModal);
    }

    // Keyboard shortcuts: Cmd+K (open) and Escape (close)
    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (!modal) return;
        if (modal.classList.contains('hidden')) {
          openModal();
        } else {
          closeModal();
        }
      }
      if (e.key === 'Escape') {
        closeModal();
      }
    });
  });
})();
