/**
 * shelf-daily.js — Daily deterministic book rotation [#192]
 *
 * Uses dayOfYear as an LCG seed to pick 6 books consistently for the day.
 * "전체 보기" toggles all remaining cards sorted by date desc.
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
      var tmp = result[i];
      result[i] = result[j];
      result[j] = tmp;
    }
    return result;
  }

  /** Day-of-year (1–366) — changes every midnight, consistent across time zones using UTC */
  function getDayOfYear() {
    var now = new Date();
    var start = Date.UTC(now.getUTCFullYear(), 0, 0);
    var today = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
    return Math.floor((today - start) / 86400000);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var grid = document.getElementById('shelf-grid');
    var showAllBtn = document.getElementById('shelf-show-all');
    if (!grid) return;

    var cards = Array.from(grid.querySelectorAll('[data-shelf-card]'));
    if (!cards.length) return;

    var seed = getDayOfYear();
    var indices = cards.map(function (_, i) { return i; });
    var shuffled = lcgShuffle(indices, seed);

    // Split: today's 6 vs rest
    var todayIndices = shuffled.slice(0, DAILY_COUNT);
    var todaySet = new Set(todayIndices);

    // Show today's cards in shuffled order
    todayIndices.forEach(function (idx) {
      cards[idx].classList.remove('hidden');
    });

    if (!showAllBtn) return;

    // Collect remaining cards (not in today's set) sorted by date desc
    var restCards = cards.filter(function (_, i) { return !todaySet.has(i); });
    restCards.sort(function (a, b) {
      var da = a.getAttribute('data-date') || '';
      var db = b.getAttribute('data-date') || '';
      return db.localeCompare(da); // desc
    });

    var expanded = false;

    showAllBtn.addEventListener('click', function () {
      expanded = !expanded;
      showAllBtn.setAttribute('aria-expanded', String(expanded));

      if (expanded) {
        // Move rest cards to end of grid in sorted order, then show
        restCards.forEach(function (card) {
          grid.appendChild(card);
          card.classList.remove('hidden');
        });
        showAllBtn.querySelector('svg').setAttribute('style', 'transform:rotate(180deg)');
        var textNode = showAllBtn.childNodes[showAllBtn.childNodes.length - 2];
        if (textNode) {
          // Update button label (find the text node between svg and span)
          var spans = showAllBtn.querySelectorAll('span');
          if (spans.length) {
            var labelEl = showAllBtn.querySelector('.shelf-btn-label');
            if (!labelEl) {
              // wrap text in span if not already
              Array.from(showAllBtn.childNodes).forEach(function (node) {
                if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                  var s = document.createElement('span');
                  s.className = 'shelf-btn-label';
                  s.textContent = node.textContent;
                  showAllBtn.replaceChild(s, node);
                }
              });
            }
            labelEl = showAllBtn.querySelector('.shelf-btn-label');
            if (labelEl) labelEl.setAttribute('data-original', labelEl.textContent);
          }
        }
        showAllBtn.setAttribute('data-original-text', showAllBtn.textContent.trim());
      } else {
        // Collapse: hide rest cards
        restCards.forEach(function (card) {
          card.classList.add('hidden');
        });
        showAllBtn.querySelector('svg').removeAttribute('style');
      }
    });
  });
})();
