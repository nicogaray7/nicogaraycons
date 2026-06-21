/* Suivi des clics CTA (évènement GA4 clic_cta). Respecte le Consent Mode via gtag. */
(function () {
  function send(name, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params);
    } else {
      (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: name }, params));
    }
  }
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a, button') : null;
    if (!a) return;
    var href = (a.getAttribute && a.getAttribute('href')) || '';
    var cls = a.className || '';
    var isCTA = /btn|cta/i.test(cls) || /calendly\.com|\/go\/rdv/i.test(href);
    if (!isCTA) return;
    var label = (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60);
    send('clic_cta', { cta_label: label, cta_url: href || '(sans lien)' });
  }, true);
})();
