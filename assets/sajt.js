// Logika table (renderVals u project/Racunar.dc.html) prepisana za običnu stranicu.
(function () {
  var $ = function (q, el) { return (el || document).querySelector(q); };
  var $$ = function (q, el) { return Array.prototype.slice.call((el || document).querySelectorAll(q)); };

  // meni za telefon
  var mbtn = $('.menu-btn'), mnav = $('.mnav');
  function setMenu(open) {
    mnav.className = open ? 'mnav open' : 'mnav';
    mbtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    mbtn.setAttribute('aria-label', open ? 'Zatvori meni' : 'Otvori meni');
    $('path', mbtn).setAttribute('d', open ? 'M6 6l12 12M18 6 6 18' : 'M4 7h16M4 12h16M4 17h16');
  }
  mbtn.addEventListener('click', function () { setMenu(mbtn.getAttribute('aria-expanded') !== 'true'); });
  $$('a', mnav).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  // pauza utisaka
  var mqb = $('.mqbtn'), mqs = $('.mqs');
  mqb.addEventListener('click', function () {
    var p = mqb.getAttribute('aria-pressed') !== 'true';
    mqb.setAttribute('aria-pressed', p ? 'true' : 'false');
    mqs.className = p ? 'mqs paused' : 'mqs';
    $('path', mqb).setAttribute('d', p ? 'M8 5.5v13l10.5-6.5z' : 'M9 6v12M15 6v12');
    mqb.lastChild.textContent = p ? 'Pusti utiske' : 'Pauziraj utiske';
  });

  // poređenje 1. i 5. dana
  var cut = $('.cmp .cut'), hand = $('.cmp .hand'), range = $('.cmpctl input');
  function setCmp(v, snap) {
    cut.style.clipPath = 'inset(0 0 0 ' + v + '%)';
    hand.style.left = v + '%';
    cut.classList.toggle('snap', snap);
    hand.classList.toggle('snap', snap);
    range.value = v;
    range.setAttribute('aria-valuetext', v >= 95 ? 'Prikazan prvi dan' : v <= 5 ? 'Prikazan peti dan' : 'Prvi dan levo, peti dan desno');
  }
  range.addEventListener('input', function () { setCmp(Number(range.value), false); });
  var cbtn = $$('.cmpctl button');
  cbtn[0].addEventListener('click', function () { setCmp(100, true); });
  cbtn[1].addEventListener('click', function () { setCmp(0, true); });

  // karusel radova polaznica
  var deck = $('.deck'), cards = $$('.dcard', deck), N = cards.length, cur = 0, sup = false, dk = null;
  var POS = { '0': 'dcard d0', '1': 'dcard d1', '-1': 'dcard dm1', '2': 'dcard d2', '-2': 'dcard dm2' };
  function go(i) {
    cur = (i + N) % N;
    cards.forEach(function (c, j) {
      var d = (j - cur + N) % N;
      if (d > 2) d -= N;
      c.className = POS[String(d)];
      c.setAttribute('aria-current', d === 0 ? 'true' : 'false');
    });
    $('.dnum').textContent = (cur + 1) + ' / ' + N;
  }
  cards.forEach(function (c, i) { c.addEventListener('click', function () { if (i !== cur && !sup) go(i); }); });
  var rb = $$('.dctl .rbtn');
  rb[0].addEventListener('click', function () { go(cur - 1); });
  rb[1].addEventListener('click', function () { go(cur + 1); });
  deck.addEventListener('pointerdown', function (e) {
    if (e.button > 0) return;
    dk = { x: e.clientX, dx: 0, moved: false, id: e.pointerId, hist: [{ x: e.clientX, t: e.timeStamp }] };
  });
  deck.addEventListener('pointermove', function (e) {
    if (!dk || e.pointerId !== dk.id) return;
    dk.dx = e.clientX - dk.x;
    dk.hist.push({ x: e.clientX, t: e.timeStamp });
    if (dk.hist.length > 6) dk.hist.shift();
    if (!dk.moved && Math.abs(dk.dx) > 10) { dk.moved = true; try { deck.setPointerCapture(dk.id); } catch (err) {} }
    var c = dk.moved && $('.d0', deck);
    if (c) { c.style.transition = 'none'; c.style.transform = 'translateX(' + dk.dx + 'px)'; }
  });
  function up() {
    var k = dk;
    dk = null;
    if (!k) return;
    var c = $('.d0', deck);
    if (c) { c.style.transition = ''; c.style.transform = ''; }
    if (!k.moved) return;
    sup = true;
    setTimeout(function () { sup = false; }, 0);
    var a = k.hist[0], b = k.hist[k.hist.length - 1];
    var v = b.t > a.t ? (b.x - a.x) / (b.t - a.t) * 1000 : 0;
    var projected = k.dx + (v / 1000) * 0.99 / 0.01;
    if (Math.abs(projected) > deck.getBoundingClientRect().width * 0.2) go(projected < 0 ? cur + 1 : cur - 1);
  }
  deck.addEventListener('pointerup', up);
  deck.addEventListener('pointercancel', up);

  // jedan reveal stil: svaka sekcija se pojavi jednom; bez JS-a sve je odmah vidljivo
  var root = $('.lk');
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.setAttribute('data-in', ''); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  $$('main > section:not(.hero) > .wrap, .crz-wrap > section > .wrap', root).forEach(function (el) {
    el.setAttribute('data-reveal', ''); io.observe(el);
  });
  root.setAttribute('data-motion', '');
})();
