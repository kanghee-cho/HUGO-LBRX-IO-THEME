/**
 * search.js — Pagefind JS API integration
 * Task #161: lazy-loads Pagefind on first modal open, debounces input 300ms,
 * renders result cards into #search-results.
 *
 * Note: Pagefind index only exists after `npm run build`.
 * In hugo server dev mode, the modal shows a fallback message.
 */
(function () {
  var DEBOUNCE_MS = 300;
  var pagefind = null;
  var debounceTimer = null;
  var isLoaded = false;
  var isLoading = false;

  var modal = null;
  var input = null;
  var results = null;
  var backdrop = null;

  function openModal() {
    if (!modal) return;
    modal.removeAttribute('hidden');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    if (input) {
      setTimeout(function () { input.focus(); }, 50);
    }
    if (!isLoaded && !isLoading) {
      loadPagefind();
    }
  }

  function closeModal() {
    if (!modal) return;
    modal.setAttribute('hidden', '');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (input) input.value = '';
    if (results) results.innerHTML = '';
  }

  function loadPagefind() {
    isLoading = true;
    import('/pagefind/pagefind.js')
      .then(function (pf) {
        pagefind = pf;
        isLoaded = true;
        isLoading = false;
        if (results) results.innerHTML = '';
      })
      .catch(function () {
        isLoading = false;
        if (results) {
          results.innerHTML =
            '<p class="text-sm text-zinc-500 dark:text-zinc-400 text-center py-6">' +
            'Search index not found. Run <code class="font-mono bg-zinc-100 dark:bg-zinc-800 px-1 rounded">npm run build</code> first.' +
            '</p>';
        }
      });
  }

  function debounce(fn, delay) {
    return function () {
      var args = arguments;
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () { fn.apply(null, args); }, delay);
    };
  }

  function renderResults(items) {
    if (!results) return;
    if (!items || items.length === 0) {
      results.innerHTML =
        '<p class="text-sm text-zinc-500 dark:text-zinc-400 text-center py-6">No results found.</p>';
      return;
    }
    Promise.all(items.slice(0, 10).map(function (item) { return item.data(); }))
      .then(function (dataList) {
        results.innerHTML = dataList
          .map(function (d) {
            return (
              '<a href="' + d.url + '" class="block px-4 py-3 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors group" onclick="document.getElementById(\'search-modal\').setAttribute(\'hidden\',\'\');document.body.style.overflow=\'\'">' +
              '<p class="text-xs text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-0.5">' +
              (d.meta && d.meta.section ? d.meta.section : '') +
              '</p>' +
              '<p class="font-medium text-zinc-900 dark:text-zinc-100 group-hover:text-zinc-700 dark:group-hover:text-zinc-300 line-clamp-1">' +
              (d.meta && d.meta.title ? d.meta.title : d.url) +
              '</p>' +
              (d.excerpt
                ? '<p class="text-sm text-zinc-600 dark:text-zinc-400 mt-0.5 line-clamp-2">' + d.excerpt + '</p>'
                : '') +
              '</a>'
            );
          })
          .join('');
      });
  }

  var doSearch = debounce(function (query) {
    if (!pagefind || !query.trim()) {
      if (results) results.innerHTML = '';
      return;
    }
    pagefind.search(query).then(function (res) {
      renderResults(res.results);
    });
  }, DEBOUNCE_MS);

  document.addEventListener('DOMContentLoaded', function () {
    modal = document.getElementById('search-modal');
    input = document.getElementById('search-input');
    results = document.getElementById('search-results');
    backdrop = document.getElementById('search-backdrop');

    if (!modal) return;

    document.querySelectorAll('[data-search-open]').forEach(function (btn) {
      btn.addEventListener('click', openModal);
    });
    document.querySelectorAll('[data-search-close]').forEach(function (btn) {
      btn.addEventListener('click', closeModal);
    });

    if (backdrop) backdrop.addEventListener('click', closeModal);

    if (input) {
      input.addEventListener('input', function () { doSearch(input.value); });
    }

    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (modal.hasAttribute('hidden')) { openModal(); } else { closeModal(); }
      }
      if (e.key === 'Escape') { closeModal(); }
    });
  });
})();
