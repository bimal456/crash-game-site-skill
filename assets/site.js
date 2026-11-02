/* Progressive enhancement only; the site works without JS. */
(function () {
  var toc = document.querySelector('details.toc');
  if (toc && window.matchMedia && window.matchMedia('(max-width: 979px)').matches) {
    toc.removeAttribute('open');
  }
  var check = document.getElementById('nav-check');
  if (check) {
    var label = document.querySelector('label[for="nav-check"]');
    var sync = function () { if (label) label.setAttribute('aria-expanded', check.checked ? 'true' : 'false'); };
    check.addEventListener('change', sync);
    sync();
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && check.checked) { check.checked = false; sync(); check.focus(); }
    });
  }
})();
