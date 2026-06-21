/* Suivi GA4 : clic_cta (avec emplacement) + scroll par paliers. Respecte le Consent Mode via gtag. */
(function () {
  function send(name, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params);
    } else {
      (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: name }, params));
    }
  }

  // Détermine l'emplacement d'un CTA (nav, hero, footer, ou section la plus proche)
  function ctaLocation(el) {
    if (el.getAttribute && el.getAttribute('data-cta')) return el.getAttribute('data-cta');
    if (el.closest('nav')) return 'nav';
    if (el.closest('footer')) return 'footer';
    if (el.closest('header, .hero')) return 'hero';
    var sec = el.closest('section, .cta-band, .contact-card');
    if (sec) {
      if (sec.id) return sec.id;
      var h = sec.querySelector('h1, h2, h3');
      if (h) return h.textContent.trim().toLowerCase().replace(/\s+/g, '-').slice(0, 40);
    }
    return 'autre';
  }

  // 1) clic_cta sur tout clic de CTA
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a, button') : null;
    if (!a) return;
    var href = (a.getAttribute && a.getAttribute('href')) || '';
    var cls = a.className || '';
    var isCTA = /btn|cta/i.test(cls) || /calendly\.com|\/go\/rdv/i.test(href);
    if (!isCTA) return;
    var label = (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60);
    send('clic_cta', {
      cta_label: label,
      cta_url: href || '(sans lien)',
      cta_location: ctaLocation(a)
    });
  }, true);

  // 2) scroll par paliers (25/50/75/90), une fois chacun
  var fired = {};
  var thresholds = [25, 50, 75, 90];
  function onScroll() {
    var doc = document.documentElement;
    var scrollable = (doc.scrollHeight - window.innerHeight);
    if (scrollable <= 0) return;
    var pct = Math.round(((window.scrollY || doc.scrollTop) / scrollable) * 100);
    for (var i = 0; i < thresholds.length; i++) {
      var t = thresholds[i];
      if (pct >= t && !fired[t]) {
        fired[t] = true;
        send('scroll_paliers', { percent_scrolled: t });
      }
    }
    if (fired[90]) window.removeEventListener('scroll', onScroll);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
})();
