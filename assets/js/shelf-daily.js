/**
 * shelf-daily.js — Daily deterministic book rotation [#194]
 *
 * - #shelf-today-grid: all cards rendered here, JS shows today's 6
 * - #shelf-rest-section / #shelf-rest-grid: remaining books shown after expand
 * - #shelf-show-all: button toggles expand/collapse, label updates accordingly
 */
(function () {
  'use strict';

  var DAILY_COUNT = 6;

  /** Linear Congruential Generator — deterministic shuffle from seed */
  function lcgShuffle(arr, seed) {
    var result = arr.slice();
    var s = seed >>> 0;
    for (var i = result.length - 1; i > 0; i--) {
      s = (Math.imul(1664525, s) + 1013904223) >>> 0;
      var j = s % (i + 1);
      var tmp = result[i]; result[i] = result[j]; result[j] = tmp;
    }
    return result;
  }

  /** Day-of-year (1–366) based on UTC date — same for all visitors on same UTC day */
  function getDayOfYear() {
    var now = new Date();
    var start = Date.UTC(now.getUTCFullYear(), 0, 0);
    var today = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
    return Math.floor((today - start) / 86400000);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var todayGrid   = document.getElementById('shelf-today-grid');
    var restSection = document.getElementById('shelf-rest-section');
    var restGrid    = document.getElementById('shelf-rest-grid');
    var btn         = document.getElementById('shelf-show-all');
    var btnLabel    = document.getElementById('shelf-show-all-label');
    var btnIcon     = document.getElementById('shelf-show-all-icon');
    var restCount   = document.getElementById('shelf-rest-count');

    if (!todayGrid) return;

    var cards = Array.from(todayGrid.querySelectorAll('[data-shelf-card]'));
    if (!cards.length) return;

    // Deterministic daily shuffle
    var seed = getDayOfYear();
    var shuffled = lcgShuffle(cards.map(function (_, i) { return i; }), seed);

    var todayIndices = shuffled.slice(0, DAILY_COUNT);
    var todaySet = new Set(todayIndices);

    // Show today's 6 in shuffled order
    todayIndices.forEach(function (idx) {
      cards[idx].classList.remove('hidden');
    });

    if (!btn || !restSection || !restGrid) return;

    // All cards sorted by date desc for the full shelf view (cloned — today's stay in today grid too)
    var allSorted = cards.slice().sort(function (a, b) {
      return (b.getAttribute('data-date') || '').localeCompare(a.getAttribute('data-date') || '');
    });

    // Update total count label
    if (restCount) restCount.textContent = cards.length + '권';

    // Populate restGrid with clones of ALL cards sorted by date desc
    // (today's 6 remain visible in todayGrid; full shelf shows everything)
    allSorted.forEach(function (card) {
      var clone = card.cloneNode(true);
      clone.classList.add('hidden');
      restGrid.appendChild(clone);
    });

    var restClones = Array.from(restGrid.querySelectorAll('[data-shelf-card]'));

    var expanded = false;
    var labelOpen  = btn.getAttribute('data-label-open')  || '전체 책장 보기';
    var labelClose = btn.getAttribute('data-label-close') || '접기';

    btn.addEventListener('click', function () {
      expanded = !expanded;
      btn.setAttribute('aria-expanded', String(expanded));

      if (expanded) {
        // Show rest section and all cloned cards
        restSection.classList.remove('hidden');
        restClones.forEach(function (card) { card.classList.remove('hidden'); });
        if (btnLabel) btnLabel.textContent = labelClose;
        if (btnIcon) btnIcon.style.transform = 'rotate(180deg)';
        // Scroll to rest section smoothly
        restSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        // Hide rest section
        restSection.classList.add('hidden');
        restClones.forEach(function (card) { card.classList.add('hidden'); });
        if (btnLabel) btnLabel.textContent = labelOpen;
        if (btnIcon) btnIcon.style.transform = '';
      }
    });
  });
})();

