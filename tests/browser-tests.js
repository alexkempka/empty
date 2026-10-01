/*
 * Browser-Tests gegen den LOKALEN Testserver (Apache auf 127.0.0.1).
 * www.itcorenet.com wird im Testbrowser fest auf 127.0.0.1 umgebogen – die Live-Website wird nie aufgerufen.
 *
 * Aufruf:  NODE_PATH=$(npm root -g) node tests/browser-tests.js
 * Ergebnis: Konsolenbericht + Bildschirmfotos in tests/ergebnisse/
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = 'https://www.itcorenet.com';
const SPKI = process.env.TEST_CERT_SPKI;            // Fingerabdruck des lokalen Test-Zertifikats
const OUT = path.join(__dirname, 'ergebnisse');
const AXE = fs.readFileSync(path.join(__dirname, 'node_modules/axe-core/axe.min.js'), 'utf8');
const MAILS = '/tmp/itc-mails.txt';
const RATE = path.join(__dirname, '../dist/formular/daten/rate.json');

const PAGES = [
  '/de/', '/de/leistungen/', '/de/projekterfahrung/', '/de/ueber-itcorenet/', '/de/kontakt/', '/de/kontakt/danke/', '/de/impressum/', '/de/datenschutz/',
  '/en/', '/en/services/', '/en/project-experience/', '/en/about/', '/en/contact/', '/en/contact/thank-you/', '/en/legal-notice/', '/en/privacy/',
];
const SIZES = { desktop: [1440, 900], laptop: [1280, 800], tablet: [768, 1024], smartphone: [390, 844] };

let failures = 0;
const ok = (cond, msg) => { if (!cond) { failures++; console.log('  FEHLER:', msg); } return cond; };

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium',
    args: ['--no-proxy-server', '--host-resolver-rules=MAP www.itcorenet.com 127.0.0.1, MAP itcorenet.com 127.0.0.1, MAP * ~NOTFOUND',
      `--ignore-certificate-errors-spki-list=${SPKI}`],
  });

  // 1. Jede Seite in jeder Größe: Status, Fehler, fremde Anfragen, Cookies, Speicher, Überbreite
  const external = new Set(); const internalLinks = new Set();
  for (const [name, [w, h]] of Object.entries(SIZES)) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    for (const p of [...PAGES, '/gibt-es-nicht']) {
      const page = await ctx.newPage(); const errors = [];
      page.on('console', m => { if (m.type() === 'error' || /Content Security Policy/i.test(m.text())) errors.push(m.text()); });
      page.on('pageerror', e => errors.push(e.message));
      page.on('request', r => { const u = new URL(r.url()); if (u.protocol.startsWith('http') && u.host !== 'www.itcorenet.com') external.add(r.url()); });
      page.on('requestfailed', r => errors.push('Anfrage fehlgeschlagen: ' + r.url()));
      const res = await page.goto(BASE + p, { waitUntil: 'networkidle' });
      await page.waitForTimeout(p.includes('ueber') || p.includes('about') || p.length <= 4 ? 4200 : 200);
      const expect = p === '/gibt-es-nicht' ? 404 : 200;
      ok(res.status() === expect, `${name} ${p}: Status ${res.status()} statt ${expect}`);
      const errs = p === '/gibt-es-nicht' ? errors.filter(t => !/status of 404/.test(t)) : errors;
      ok(errs.length === 0, `${name} ${p}: Konsolenfehler ${JSON.stringify(errs)}`);
      const sw = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      ok(sw <= 0, `${name} ${p}: ${sw}px seitlicher Überlauf`);
      const storage = await page.evaluate(() => [document.cookie, localStorage.length, sessionStorage.length]);
      ok(storage[0] === '' && storage[1] === 0 && storage[2] === 0, `${name} ${p}: Speicher im Browser ${JSON.stringify(storage)}`);
      if (name === 'desktop') {
        (await page.$$eval('a[href^="/"]', as => as.map(a => a.getAttribute('href')))).forEach(h => internalLinks.add(h));
      }
      const file = `${name}${p.replace(/\//g, '_') || '_root'}.png`;
      await page.screenshot({ path: path.join(OUT, file), fullPage: true });
      await page.close();
    }
    ok((await ctx.cookies()).length === 0, `${name}: Cookies gesetzt: ${JSON.stringify(await ctx.cookies())}`);
    await ctx.close();
  }
  ok(external.size === 0, 'Anfragen an fremde Server: ' + [...external].join(', '));
  console.log(`1. Seiten × Größen geprüft (${PAGES.length + 1} Seiten, ${Object.keys(SIZES).length} Größen). Fremde Anfragen: ${external.size}`);

  // 2. Alle internen Links erreichbar
  // Prüfung aus dem Testbrowser heraus (nur so greift die Umleitung auf 127.0.0.1)
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, bypassCSP: true });
  const page = await ctx.newPage();
  await page.goto(BASE + '/de/');
  for (const href of internalLinks) {
    const st = await page.evaluate(async h => (await fetch(h.split('#')[0], { redirect: 'manual' })).status, href);
    ok(st === 200, `Link ${href}: Status ${st}`);
    const anchor = href.split('#')[1];
    if (anchor) {
      await page.goto(BASE + href);
      ok(await page.$('#' + anchor) !== null, `Sprungziel #${anchor} fehlt`);
    }
  }
  console.log(`2. ${internalLinks.size} interne Links geprüft`);

  // 3. Barrierefreiheit (axe-core, WCAG 2.0/2.1/2.2 A + AA)
  let violations = 0;
  for (const p of [...PAGES, '/gibt-es-nicht']) {
    await page.goto(BASE + p); await page.addScriptTag({ content: AXE });
    const r = await page.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] })).violations
      .map(v => `${v.id} (${v.impact}): ${v.nodes.length}× – ${v.nodes.slice(0, 2).map(n => n.target.join(' ')).join(' | ')}`));
    if (r.length) { violations += r.length; console.log(`  axe ${p}:`, r); }
  }
  ok(violations === 0, `axe meldet ${violations} Verstöße`);
  console.log(`3. Barrierefreiheit (axe) geprüft: ${violations} Verstöße`);

  // 4. Tastatur: Sprunglink, sichtbarer Fokus, Sprachwechsel, hreflang
  await page.goto(BASE + '/de/');
  await page.keyboard.press('Tab');
  ok(await page.evaluate(() => document.activeElement.classList.contains('skip-link')), 'Erster Tab trifft nicht den Sprunglink');
  let noOutline = 0;
  for (let i = 0; i < 14; i++) {
    await page.keyboard.press('Tab');
    const o = await page.evaluate(() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2; });
    if (!o) noOutline++;
  }
  ok(noOutline === 0, `${noOutline} Elemente ohne sichtbaren Fokusrahmen`);
  for (const [p, other] of [['/de/leistungen/', '/en/services/'], ['/en/about/', '/de/ueber-itcorenet/'], ['/de/impressum/', '/en/legal-notice/']]) {
    await page.goto(BASE + p);
    ok(await page.$(`.lang a[href="${other}"]`) !== null, `Sprachwechsel auf ${p} zeigt nicht auf ${other}`);
    ok(await page.$(`link[rel="alternate"][hreflang][href="${BASE}${other}"]`) !== null, `hreflang auf ${p} fehlt`);
    ok(await page.$(`link[rel="canonical"][href="${BASE}${p}"]`) !== null, `canonical auf ${p} fehlt`);
  }
  console.log('4. Tastatur, Fokus, Sprachwechsel, hreflang, canonical geprüft');

  // 5. Handy-Menü
  const mctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const mp = await mctx.newPage(); await mp.goto(BASE + '/de/');
  ok(!(await mp.isVisible('#site-nav')), 'Menü auf dem Handy nicht zugeklappt');
  await mp.click('.nav-toggle');
  ok(await mp.isVisible('#site-nav') && (await mp.getAttribute('.nav-toggle', 'aria-expanded')) === 'true', 'Menü öffnet nicht');
  await mp.screenshot({ path: path.join(OUT, 'smartphone_menue-offen.png') });
  await mp.keyboard.press('Escape');
  ok(!(await mp.isVisible('#site-nav')), 'Escape schließt Menü nicht');
  console.log('5. Handy-Menü geprüft');

  // 6. Animation
  await page.goto(BASE + '/de/'); await page.waitForTimeout(500);
  ok(await page.$('.anim-stage.is-live canvas') !== null, 'Animation startet nicht (Startseite)');
  await page.goto(BASE + '/en/about/'); await page.waitForTimeout(500);
  ok(await page.$('.anim-stage.is-live canvas') !== null, 'Animation startet nicht (About)');
  const rm = await browser.newContext({ reducedMotion: 'reduce' }); const rp = await rm.newPage();
  await rp.goto(BASE + '/de/'); await rp.waitForTimeout(300);
  await rp.screenshot({ path: path.join(OUT, 'bewegung-reduziert_start.png') });
  console.log('6. Animation geprüft (inkl. „Bewegung reduzieren“, siehe Bildschirmfoto)');

  // 7. Kontaktformular
  fs.writeFileSync(MAILS, ''); try { fs.unlinkSync(RATE); } catch (e) {}
  const mails = () => fs.readFileSync(MAILS, 'utf8').split(/^To: /m).length - 1;
  await page.goto(BASE + '/de/kontakt/');
  await page.waitForTimeout(3500); await page.click('button[type=submit]'); await page.waitForLoadState();
  ok(await page.$$eval('[aria-invalid="true"]', e => e.length) === 3, 'Leeres Formular: 3 Fehler erwartet');
  ok(await page.isVisible('.alert[role=alert]'), 'Fehlerübersicht fehlt');
  await page.screenshot({ path: path.join(OUT, 'formular_fehler.png'), fullPage: true });
  // zu schnell abgeschickt
  await page.goto(BASE + '/de/kontakt/');
  await page.fill('#f-name', 'Test'); await page.fill('#f-email', 'test@example.org'); await page.fill('#f-message', 'Hallo');
  await page.click('button[type=submit]'); await page.waitForLoadState();
  ok((await page.textContent('.alert')).includes('zu schnell'), 'Zu schnelles Absenden nicht erkannt');
  ok((await page.inputValue('#f-name')) === 'Test', 'Eingaben gehen bei Fehler verloren');
  // XSS-Versuch wird als Text ausgegeben
  await page.goto(BASE + '/de/kontakt/');
  await page.fill('#f-name', '<script>alert(1)</script>'); await page.fill('#f-email', 'kein-mail');
  await page.waitForTimeout(3500); await page.click('button[type=submit]'); await page.waitForLoadState();
  ok((await page.inputValue('#f-name')) === '<script>alert(1)</script>' && !(await page.content()).includes('<script>alert(1)</script>'), 'Ausgabe nicht maskiert');
  // gültige Nachricht DE + EN
  for (const [p, thanks] of [['/de/kontakt/', '/de/kontakt/danke/'], ['/en/contact/', '/en/contact/thank-you/']]) {
    const before = mails();
    await page.goto(BASE + p);
    await page.fill('#f-name', 'Erika Mustermann'); await page.fill('#f-company', 'Muster GmbH');
    await page.fill('#f-email', 'erika@example.org'); await page.fill('#f-message', 'Testnachricht\nmit zwei Zeilen – äöüß');
    await page.waitForTimeout(3500); await page.click('button[type=submit]'); await page.waitForLoadState();
    ok(page.url() === BASE + thanks, `${p}: keine Weiterleitung auf Danke-Seite (${page.url()})`);
    ok(mails() === before + 1, `${p}: keine E-Mail erzeugt`);
  }
  // Fallen-Feld: Danke-Seite, aber keine E-Mail
  const before = mails();
  await page.goto(BASE + '/de/kontakt/');
  await page.fill('#f-name', 'Bot'); await page.fill('#f-email', 'bot@example.org'); await page.fill('#f-message', 'Spam');
  await page.evaluate(() => { document.getElementById('f-website').value = 'http://spam.example'; });
  await page.waitForTimeout(3500); await page.click('button[type=submit]'); await page.waitForLoadState();
  ok(page.url() === BASE + '/de/kontakt/danke/' && mails() === before, 'Fallen-Feld: Bot-Nachricht wurde versendet');
  // Begrenzung: nach 5 Nachrichten pro Stunde ist Schluss
  for (let i = 0; i < 4; i++) {
    await page.goto(BASE + '/de/kontakt/');
    await page.fill('#f-name', 'Viel'); await page.fill('#f-email', 'viel@example.org'); await page.fill('#f-message', 'Nr. ' + i);
    await page.waitForTimeout(3200); await page.click('button[type=submit]'); await page.waitForLoadState();
  }
  ok((await page.textContent('.alert') || '').includes('mehrere Nachrichten'), 'Begrenzung greift nicht');
  const raw = fs.readFileSync(RATE, 'utf8');
  ok(!raw.includes('127.0.0.1'), 'IP-Adresse im Klartext gespeichert');
  const mailText = fs.readFileSync(MAILS, 'utf8');
  ok(/Reply-To: erika@example\.org/.test(mailText) && /From: ITCoreNet Website <support@itcorenet\.com>/.test(mailText), 'Mail-Kopfzeilen falsch');
  fs.writeFileSync(path.join(OUT, 'beispiel-mails.txt'), mailText);
  console.log(`7. Kontaktformular geprüft (${mails()} Test-Mails, Beispiel in ergebnisse/beispiel-mails.txt)`);

  await browser.close();
  console.log(failures ? `\nERGEBNIS: ${failures} Fehler` : '\nERGEBNIS: alle Prüfungen bestanden');
  process.exit(failures ? 1 : 0);
})();
