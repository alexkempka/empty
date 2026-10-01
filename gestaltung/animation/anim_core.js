function itcAnimate(cv, opts) {
  opts = opts || {};
  var W = 960, H = 540, BG = '#011e3c';
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  cv.width = W * dpr; cv.height = H * dpr;
  var ctx = cv.getContext('2d');
  var MS = 0.27, MX = W / 2 - 534 * MS, MY = 70;
  var WS = 0.2, WX = W / 2 - 978 * WS, WY = 70 + 1003 * MS + 34;
  var words = WORD.map(function (d) { return new Path2D(d); });
  var seed = 7; function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
  var core = DOTS.map(function (d) {
    var tx = MX + d[0] * MS, ty = MY + d[1] * MS;
    return { tx: tx, ty: ty, r: Math.max(1.6, d[2] * MS), c: d[3] === 'c' ? '#00a6ca' : '#ffffff',
      sx: W + 80 + rnd() * 700, sy: ty + (rnd() - 0.5) * 180, d: rnd() * 0.7 };
  });
  var cols = ['#4fd1e8', '#00a6ca', '#3d6fe0', '#8fb3ff'];
  var amb = [];
  for (var i = 0; i < 240; i++) {
    var band = rnd() < 0.8;
    amb.push({ x: W + rnd() * 1400, y: band ? 110 + rnd() * 300 : rnd() * H, v: 500 + rnd() * 1100,
      w: 0.8 + rnd() * 2.2, a: 0.25 + rnd() * 0.6, c: cols[Math.floor(rnd() * cols.length)] });
  }
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(k) { return 1 - Math.pow(1 - k, 3); }
  function pos(p, t) { var e = ease(clamp((t - p.d) / 1.9)); return [p.sx + (p.tx - p.sx) * e, p.sy + (p.ty - p.sy) * e, e]; }
  function frame(t) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
    ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
    var fade = t < 2.1 ? 1 : Math.max(0, 1 - (t - 2.1) / 0.9);
    if (fade > 0) {
      ctx.globalCompositeOperation = 'lighter'; ctx.lineCap = 'round';
      for (var i = 0; i < amb.length; i++) {
        var p = amb[i], x = p.x - p.v * t, len = p.v * 0.07;
        if (x + len < 0 || x > W + 40) continue;
        ctx.globalAlpha = p.a * fade; ctx.strokeStyle = p.c; ctx.lineWidth = p.w;
        ctx.beginPath(); ctx.moveTo(x, p.y); ctx.lineTo(x + len, p.y); ctx.stroke();
      }
    }
    ctx.globalCompositeOperation = 'source-over';
    for (var j = 0; j < core.length; j++) {
      var q = core[j], a = pos(q, t), b = pos(q, t - 0.07);
      if (a[2] < 1) {
        ctx.globalAlpha = 0.85; ctx.strokeStyle = q.c === '#ffffff' ? '#8fb3ff' : '#4fd1e8';
        ctx.lineWidth = Math.max(1.5, q.r * 0.7); ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(b[0], b[1]); ctx.lineTo(a[0], a[1]); ctx.stroke();
      }
      ctx.globalAlpha = 1; ctx.fillStyle = q.c;
      ctx.beginPath(); ctx.arc(a[0], a[1], q.r * (0.35 + 0.65 * a[2]), 0, Math.PI * 2); ctx.fill();
    }
    var k = ease(clamp((t - 2.5) / 1.0));
    if (k > 0) {
      ctx.save(); ctx.beginPath(); ctx.rect(0, 0, WX + 1956 * WS * k + 2, H); ctx.clip();
      ctx.setTransform(dpr * WS, 0, 0, -dpr * WS, dpr * WX, dpr * (WY + 360 * WS));
      ctx.fillStyle = '#ffffff'; ctx.globalAlpha = 0.35 + 0.65 * k;
      for (var w = 0; w < words.length; w++) ctx.fill(words[w], 'evenodd');
      ctx.restore();
    }
  }
  var END = 3.7, raf = 0, t0 = 0;
  var still = opts.still != null ? opts.still : (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  if (opts.at != null) { frame(opts.at); return function () {}; }
  if (still) { frame(END); return function () {}; }
  function loop(ts) { if (!t0) t0 = ts; var t = (ts - t0) / 1000; frame(Math.min(t, END)); if (t < END) raf = requestAnimationFrame(loop); }
  raf = requestAnimationFrame(loop);
  return function () { cancelAnimationFrame(raf); };
}
