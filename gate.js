/* Barreira de acesso do portal (dissuasão, não cofre).
   Como usar: incluir <script src="gate.js"></script> no <head> e a regra
   html.gated body{visibility:hidden} no CSS da página.
   A senha única é validada por SHA-256 local. Troca de senha: gere o hash
   de uma senha forte e substitua PORTAL_HASH abaixo. Ver docs/senha-do-portal.md */
(function () {
  'use strict';
  var PORTAL_HASH = '83b55819c2dd8106142b5497ed3599951125c39e4429c64092eaa4fb5055f539';
  var STORE_KEY = 'portal-v4-unlock-v1';
  var LOGO_SRC = 'logo-peretto-red.png';
  try {
    var cs = document.currentScript;
    if (cs && cs.src) LOGO_SRC = cs.src.replace(/gate\.js(\?.*)?$/, '') + 'logo-peretto-red.png';
  } catch (e) {}

  try { document.documentElement.className += ' gated'; } catch (e) {}

  function sha256(ascii) {
    function rr(v, a) { return (v >>> a) | (v << (32 - a)); }
    var maxWord = Math.pow(2, 32), i, j, result = '';
    var words = [], asciiBitLength = ascii.length * 8;
    var hash = (sha256.h = sha256.h || []), k = (sha256.k = sha256.k || []);
    var primeCounter = k.length, isComposite = {};
    for (var candidate = 2; primeCounter < 64; candidate++) {
      if (!isComposite[candidate]) {
        for (i = 0; i < 313; i += candidate) isComposite[i] = candidate;
        hash[primeCounter] = (Math.pow(candidate, 0.5) * maxWord) | 0;
        k[primeCounter++] = (Math.pow(candidate, 1 / 3) * maxWord) | 0;
      }
    }
    ascii += '\x80';
    while (ascii.length % 64 - 56) ascii += '\x00';
    for (i = 0; i < ascii.length; i++) {
      j = ascii.charCodeAt(i);
      if (j >> 8) return '';
      words[i >> 2] |= j << (((3 - i) % 4) * 8);
    }
    words[words.length] = (asciiBitLength / maxWord) | 0;
    words[words.length] = asciiBitLength;
    for (j = 0; j < words.length;) {
      var w = words.slice(j, (j += 16)), oldHash = hash;
      hash = hash.slice(0, 8);
      for (i = 0; i < 64; i++) {
        var w15 = w[i - 15], w2 = w[i - 2];
        var a = hash[0], e = hash[4];
        var temp1 =
          hash[7] + (rr(e, 6) ^ rr(e, 11) ^ rr(e, 25)) + ((e & hash[5]) ^ (~e & hash[6])) + k[i] +
          (w[i] = i < 16 ? w[i] : w[i - 16] + (rr(w15, 7) ^ rr(w15, 18) ^ (w15 >>> 3)) + w[i - 7] + (rr(w2, 17) ^ rr(w2, 19) ^ (w2 >>> 10)));
        var temp2 = (rr(a, 2) ^ rr(a, 13) ^ rr(a, 22)) + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
        hash = [(temp1 + temp2) | 0].concat(hash);
        hash[4] = (hash[4] + temp1) | 0;
      }
      for (i = 0; i < 8; i++) hash[i] = (hash[i] + oldHash[i]) | 0;
    }
    for (i = 0; i < 8; i++) {
      for (j = 3; j + 1; j--) {
        var b = (hash[i] >> (j * 8)) & 255;
        result += (b < 16 ? '0' : '') + b.toString(16);
      }
    }
    return result;
  }

  function unlocked() {
    try { return sessionStorage.getItem(STORE_KEY) === '1'; } catch (e) { return false; }
  }
  function reveal() {
    try { sessionStorage.setItem(STORE_KEY, '1'); } catch (e) {}
    document.documentElement.className = document.documentElement.className.replace(/\bgated\b/g, '');
    var g = document.getElementById('portal-gate');
    if (g && g.parentNode) g.parentNode.removeChild(g);
  }

  if (unlocked()) {
    document.documentElement.className = document.documentElement.className.replace(/\bgated\b/g, '');
    return;
  }

  function css() {
    return '' +
      '#portal-gate{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px;background:#F5F0E6;font-family:Montserrat,-apple-system,"Segoe UI",sans-serif;visibility:visible}' +
      '#portal-gate .pg-card{background:#FFFCF5;border:1px solid #E2D8C6;border-radius:8px;padding:34px 36px;max-width:400px;width:100%;box-shadow:0 24px 60px -20px rgba(27,22,17,.38);position:relative;overflow:hidden}' +
      '#portal-gate .pg-card::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#E50914,#ff5a5a)}' +
      '#portal-gate .pg-kicker{display:inline-block;font-size:10px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#B20710;background:#FCE9E9;border:1px solid #f3c2c2;border-radius:20px;padding:5px 13px;margin-bottom:14px}' +
      '#portal-gate h2{font-size:21px;font-weight:800;color:#1B1611;letter-spacing:-.4px;margin:0 0 8px}' +
      '#portal-gate p{font-size:12.5px;color:#8D8272;margin:0 0 18px;line-height:1.6}' +
      '#portal-gate label{display:block;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#4B4238;margin-bottom:6px}' +
      '#portal-gate input{width:100%;font-family:inherit;font-size:14px;padding:12px 14px;border:1.5px solid #D3C6AE;border-radius:10px;background:#fff;color:#1B1611;outline:none;box-sizing:border-box}' +
      '#portal-gate input:focus{border-color:#E50914}' +
      '#portal-gate button{width:100%;margin-top:12px;border:none;font-family:inherit;font-weight:700;font-size:14px;padding:13px;border-radius:12px;background:#E50914;color:#fff;cursor:pointer}' +
      '#portal-gate button:hover{background:#B20710}' +
      '#portal-gate .pg-err{display:none;font-size:12px;font-weight:700;color:#B20710;background:#FCE9E9;border:1px solid #f3c2c2;border-radius:8px;padding:9px 12px;margin-top:12px}' +
      '#portal-gate .pg-err.show{display:block}' +
      '#portal-gate .pg-foot{margin-top:16px;font-size:10.5px;color:#B5A996;text-align:center}' +
      '#portal-gate .pg-logo{display:block;height:44px;width:auto;margin:0 auto 16px}' ;
  }

  function mount() {
    var base = LOGO_SRC;
    var st = document.createElement('style');
    st.type = 'text/css';
    st.appendChild(document.createTextNode(css()));
    document.getElementsByTagName('head')[0].appendChild(st);
    var g = document.createElement('div');
    g.id = 'portal-gate';
    g.innerHTML =
      '<div class="pg-card"><img class="pg-logo" src="' + base + '" alt="Peretto &amp; Co" onerror="this.style.display=\'none\'"><span class="pg-kicker">Acesso restrito</span>' +
      '<h2>Área do portal</h2>' +
      '<p>Este material é de circulação restrita. Digite a senha única para continuar.</p>' +
      '<form id="pg-form" autocomplete="off"><label for="pg-pass">Senha</label>' +
      '<input type="password" id="pg-pass" placeholder="••••••••" autocomplete="current-password">' +
      '<div class="pg-err" id="pg-err">Senha incorreta. Tente de novo.</div>' +
      '<button type="submit">Entrar</button></form>' +
      '<div class="pg-foot">V4 Company · Peretto &amp; Co</div></div>';
    document.body.appendChild(g);
    var input = document.getElementById('pg-pass');
    if (input) input.focus();
    document.getElementById('pg-form').onsubmit = function (ev) {
      if (ev && ev.preventDefault) ev.preventDefault();
      var val = input ? input.value : '';
      var err = document.getElementById('pg-err');
      if (sha256(val) === PORTAL_HASH) {
        reveal();
      } else {
        if (err) err.className = 'pg-err show';
        if (input) { input.value = ''; input.focus(); }
      }
      return false;
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
