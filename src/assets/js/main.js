/* ITCoreNet – Menü für kleine Bildschirme. Ohne JavaScript bleibt das Menü einfach aufgeklappt. */
document.documentElement.classList.add('js');
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
});

/* Sanftes Einblenden beim Scrollen. Alles oberhalb des unteren Bildrands wird sichtbar,
   auch nach schnellem Springen; ohne JavaScript ist ohnehin alles sofort sichtbar. */
document.addEventListener('DOMContentLoaded', function () {
  var items = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if (!items.length) return;
  var queued = false;
  function check() {
    queued = false;
    var limit = window.innerHeight * 0.92;
    items = items.filter(function (el) {
      if (el.getBoundingClientRect().top > limit) return true;
      var idx = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
      el.style.transitionDelay = Math.min(idx, 5) * 70 + 'ms';
      el.classList.add('is-visible');
      return false;
    });
    if (!items.length) {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
    }
  }
  function onScroll() { if (!queued) { queued = true; window.requestAnimationFrame(check); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  check();
});
