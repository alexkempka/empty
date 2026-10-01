// Erzeugt Favicon-PNGs und das Open-Graph-Bild aus den SVG-Dateien (einmalig, Ergebnis wird eingecheckt).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const img = p => 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(__dirname, '../src/assets/img', p)).toString('base64');
const font = p => 'data:font/woff2;base64,' + fs.readFileSync(path.join(__dirname, '../src/assets/fonts', p)).toString('base64');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
  const p = await b.newPage();
  const shot = async (w, h, html, out) => {
    await p.setViewportSize({ width: w, height: h });
    await p.setContent(`<html><head><style>@font-face{font-family:P;font-weight:600;src:url(${font('ibm-plex-sans-latin-600-normal.woff2')})}@font-face{font-family:M;src:url(${font('ibm-plex-mono-latin-400-normal.woff2')})}body{margin:0}</style></head><body>${html}</body></html>`);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, '../src/assets/img', out), omitBackground: out.startsWith('favicon') });
  };
  await shot(32, 32, `<img src="${img('itcorenet-zeichen.svg')}" style="width:32px;height:30px;display:block;margin-top:1px">`, 'favicon-32.png');
  await shot(180, 180, `<div style="width:180px;height:180px;background:#fff;display:flex;align-items:center;justify-content:center"><img src="${img('itcorenet-zeichen.svg')}" style="width:136px"></div>`, 'apple-touch-icon.png');
  await shot(1200, 630, `<div style="width:1200px;height:630px;box-sizing:border-box;background:#011e3c;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:48px 48px;display:flex;align-items:center;gap:72px;padding:0 96px;color:#fff">
    <img src="${img('itcorenet-logo-invers.svg')}" style="width:340px">
    <div><div style="font-family:M;font-size:22px;letter-spacing:.08em;text-transform:uppercase;color:#4fd1e8;margin-bottom:24px">IT-Beratung · Umsetzung · Betrieb</div>
    <div style="font-family:P;font-weight:600;font-size:64px;line-height:1.08;letter-spacing:-.02em">IT beraten.<br>Umsetzen.<br><span style="color:#4fd1e8">Betreiben.</span></div></div></div>`, 'og-image.png');
  await b.close();
})();
