/**
 * Orel Fashion — scroll animations & UI enhancements
 */
(function () {
  'use strict';

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

  const header = document.getElementById('site-header');
  let lastScrollY = window.scrollY;

  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('shadow-sm', window.scrollY > 10);

      if (window.scrollY > lastScrollY && window.scrollY > 20) {
        document.body.classList.add('showcase-header-hidden');
      } else if (window.scrollY < lastScrollY - 6) {
        document.body.classList.remove('showcase-header-hidden');
      }

      lastScrollY = window.scrollY;
    }, { passive: true });
  }

  const hero = document.querySelector('.showcase-hero');
  const title = document.querySelector('.showcase-title');
  const media = document.querySelector('.showcase-bg-media');
  const overlay = document.querySelector('.showcase-dark-overlay');
  const card1 = document.querySelector('.showcase-card-1');
  const card2 = document.querySelector('.showcase-card-2');
  const card3 = document.querySelector('.showcase-card-3');

  let cardsTriggered = false;

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function triggerCards() {
    if (cardsTriggered) return;
    cardsTriggered = true;

    if (media && media.tagName.toLowerCase() === 'video') {
      media.pause();
    }

    setTimeout(() => card1 && card1.classList.add('is-visible'), 0);
    setTimeout(() => card2 && card2.classList.add('is-visible'), 110);
    setTimeout(() => card3 && card3.classList.add('is-visible'), 220);
  }

  function resetCards() {
    cardsTriggered = false;

    card1 && card1.classList.remove('is-visible');
    card2 && card2.classList.remove('is-visible');
    card3 && card3.classList.remove('is-visible');

    if (media && media.tagName.toLowerCase() === 'video') {
      media.play().catch(() => {});
    }
  }

  function handleShowcaseHero() {
    if (!hero || !title || !media || !overlay || !card1 || !card2 || !card3) return;

    const rect = hero.getBoundingClientRect();
    const scrollInside = -rect.top;
    const maxScroll = hero.offsetHeight - window.innerHeight;
    const progress = clamp(scrollInside / maxScroll, 0, 1);

    title.style.transform = `translateY(-${progress * window.innerHeight * 1.15}px)`;

    title.style.opacity =
      progress < 0.50
        ? '1'
        : String(clamp(1 - ((progress - 0.50) / 0.10), 0, 1));

    const darkProgress = clamp((progress - 0.22) / 0.32, 0, 1);
    media.style.filter = `blur(${darkProgress * 8}px)`;
    media.style.transform = `scale(${1 + darkProgress * 0.045})`;
    overlay.style.background = `rgba(0, 0, 0, ${0.22 + darkProgress * 0.58})`;

    if (progress >= 0.68) triggerCards();
    if (progress < 0.58) resetCards();

  }

  window.addEventListener('scroll', handleShowcaseHero, { passive: true });
  window.addEventListener('resize', handleShowcaseHero);
  handleShowcaseHero();

  document.body.addEventListener('htmx:afterSwap', (e) => {
    if (e.detail.target?.id === 'cart-badge') {
      document.body.dispatchEvent(new Event('cartUpdated'));
    }
  });
})();