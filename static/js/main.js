/**
 * Orel Fashion — scroll animations & UI enhancements
 */
(function () {
  'use strict';

  // Scroll-triggered reveal animations
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('.reveal-up').forEach((el) => revealObserver.observe(el));

  // Sticky header shadow on scroll
  const header = document.getElementById('site-header');
  if (header) {
    window.addEventListener(
      'scroll',
      () => {
        header.classList.toggle('shadow-sm', window.scrollY > 10);
      },
      { passive: true }
    );
  }

  // HTMX cart update event
  document.body.addEventListener('htmx:afterSwap', (e) => {
    if (e.detail.target?.id === 'cart-badge') {
      document.body.dispatchEvent(new Event('cartUpdated'));
    }
  });
})();
