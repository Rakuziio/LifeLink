document.addEventListener("DOMContentLoaded", () => {
  const flashes = document.querySelectorAll('.flash');
  if (!flashes.length) return;

  setTimeout(() => {
    flashes.forEach(el => el.remove());
  }, 6000);
});
