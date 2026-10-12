(() => {
  const controls = document.querySelector('.filters');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const publications = [...document.querySelectorAll('#publication-list [data-category]')];
  const count = document.querySelector('#publication-count');

  if (!controls || !count || !publications.length) return;
  const allWorksLabel = count.textContent;
  controls.hidden = false;

  for (const button of buttons) {
    button.addEventListener('click', () => {
      const filter = button.dataset.filter;
      for (const option of buttons) {
        option.setAttribute('aria-pressed', String(option === button));
      }
      let visible = 0;
      for (const publication of publications) {
        const matches = filter === 'all' || publication.dataset.category === filter;
        publication.hidden = !matches;
        if (matches) visible += 1;
      }
      count.textContent = filter === 'all'
        ? allWorksLabel
        : `Showing ${visible} works · ${button.textContent.trim()}`;
    });
  }
})();
