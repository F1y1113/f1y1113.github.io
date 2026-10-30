// Keep the initial viewport aligned with complete entries as text wraps or fonts load.
(() => {
  const viewport = document.getElementById('news-window');
  const list = document.getElementById('news-list');
  if (!viewport || !list) return;

  const fitNews = () => {
    const count = Number(viewport.dataset.visibleCount) || 10;
    const last = list.children[Math.min(count, list.children.length) - 1];
    if (!last) return;
    const bottomPadding = parseFloat(getComputedStyle(list).paddingBottom) || 0;
    const height = last.getBoundingClientRect().bottom - viewport.getBoundingClientRect().top + viewport.scrollTop + bottomPadding;
    viewport.style.setProperty('--news-window-height', `${Math.ceil(height)}px`);
  };

  fitNews();
  if ('ResizeObserver' in window) {
    new ResizeObserver(fitNews).observe(list);
  } else {
    window.addEventListener('resize', fitNews);
  }
  if (document.fonts) document.fonts.ready.then(fitNews);
})();
