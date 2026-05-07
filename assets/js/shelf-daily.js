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

    // Collect rest cards sorted by date desc
    var restCards = cards
      .filter(function (_, i) { return !todaySet.has(i); })
      .sort(function (a, b) {
        return (b.getAttribute('data-date') || '').localeCompare(a.getAttribute('data-date') || '');
      });

    if (!restCards.length) {
      // Fewer than 6 books — hide the button entirely
      var wrap = document.getElementById('shelf-show-all-wrap');
      if (wrap) wrap.style.display = 'none';
      return;
    }

    // Update rest count label
    if (restCount) restCount.textContent = restCards.length + '권';

    // Move rest cards into restGrid (out of today grid, into separate section)
    restCards.forEach(function (card) {
      card.classList.add('hidden');
      restGrid.appendChild(card);
    });

    var expanded = false;
    var labelOpen  = btn.getAttribute('data-label-open')  || '전체 책장 보기';
    var labelClose = btn.getAttribute('data-label-close') || '접기';

    btn.addEventListener('click', function () {
      expanded = !expanded;
      btn.setAttribute('aria-expanded', String(expanded));

      if (expanded) {
        // Show rest section and all its cards
        restSection.classList.remove('hidden');
        restCards.forEach(function (card) { card.classList.remove('hidden'); });
        if (btnLabel) btnLabel.textContent = labelClose;
        if (btnIcon) btnIcon.style.transform = 'rotate(180deg)';
        // Scroll to rest section smoothly
        restSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        // Hide rest section
        restSection.classList.add('hidden');
        restCards.forEach(function (card) { card.classList.add('hidden'); });
        if (btnLabel) btnLabel.textContent = labelOpen;
        if (btnIcon) btnIcon.style.transform = '';
      }
    });
  });
})();

