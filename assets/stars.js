// Keep the verified local snapshot visible unless the live badge loads successfully.
document.querySelectorAll('img[data-live-src]').forEach((badge) => {
  const live = new Image();
  live.onload = () => {
    badge.src = live.src;
    badge.alt = 'GitHub Stars';
    badge.title = 'Live GitHub star count';
  };
  live.src = badge.dataset.liveSrc;
});
