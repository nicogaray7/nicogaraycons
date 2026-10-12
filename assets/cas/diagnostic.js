/* Use-case diagnostic: shows the agent card that matches the problem the visitor picks.
   Progressive enhancement: without this script every card stays visible. */
(function () {
  var root = document.querySelector('.dx');
  if (!root) return;
  var options = Array.prototype.slice.call(root.querySelectorAll('.dx-opt'));
  var panels = Array.prototype.slice.call(root.querySelectorAll('.dx-panel'));
  var panelsBox = root.querySelector('.dx-panels');
  if (!options.length || !panels.length) return;

  function track(id) {
    var params = { use_case: id };
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'use_case_select', params);
    } else {
      (window.dataLayer = window.dataLayer || []).push({ event: 'use_case_select', use_case: id });
    }
  }

  function show(id, fromVisitor) {
    options.forEach(function (opt) {
      opt.setAttribute('aria-pressed', opt.getAttribute('aria-controls') === id ? 'true' : 'false');
    });
    panels.forEach(function (panel) {
      panel.hidden = panel.id !== id;
    });
    if (!fromVisitor) return;
    track(id);
    // On a phone the card sits below the choices: bring it into view.
    if (window.matchMedia && window.matchMedia('(max-width: 959px)').matches && panelsBox) {
      panelsBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  options.forEach(function (opt) {
    opt.addEventListener('click', function () {
      show(opt.getAttribute('aria-controls'), true);
    });
  });

  root.classList.add('dx-js');
  show(options[0].getAttribute('aria-controls'), false);
})();
