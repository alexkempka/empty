# ITCoreNet – Website

Die Website von ITCoreNet (www.itcorenet.com) auf Deutsch und Englisch.
Statisches HTML/CSS, wenig eigenes JavaScript, ein kleines PHP-Skript für das Kontaktformular.
Keine Datenbank, kein Framework, keine Cookies, keine Anfragen an fremde Server.

> **Stand:** Fertig programmiert und lokal getestet. **Noch nicht veröffentlicht.**
> Die bisherige Website bleibt unverändert online, bis die Veröffentlichung ausdrücklich freigegeben ist.

---

## 1. Was ist wo?

| Ordner / Datei | Inhalt |
|---|---|
| `src/pages/de/` | **Texte der deutschen Seiten** (eine Datei pro Seite) |
| `src/pages/en/` | **Texte der englischen Seiten** (gleiche Dateinamen wie Deutsch) |
| `src/pages/404.html` | Fehlerseite (zweisprachig) |
| `src/pages/*/imprint.html`, `privacy.html` | **Impressum und Datenschutzerklärung** |
| `src/assets/img/` | **Bilder**: Logo-Varianten, Banner, Leistungsbilder, Favicons, Vorschaubild |
| `src/assets/fonts/` | **Schriften** (IBM Plex, lokal) mit Lizenztexten |
| `src/assets/css/style.css` | Gestaltung (Farben, Abstände, Layout) |
| `src/assets/js/` | Handy-Menü (`main.js`) und Logo-Animation (`logo-animation.js`) |
| `src/formular/` | Kontaktformular (PHP) und Vorlage für die Konfiguration |
| `src/.htaccess` | Serverregeln: Weiterleitungen, HTTPS, Sicherheits-Header, Komprimierung |
| `build.py` | Baut aus `src/` die fertige Website in `dist/` |
| `dist/` | **Fertige Website zum Hochladen** (wird erzeugt, nicht im Repository) |
| `tests/` | Automatische Prüfungen (Browser, Server, Barrierefreiheit) |
| `gestaltung/` | Quellen der Grafiken, Logo-Original, Animations-Quelltext, **`LIZENZEN.md`** |
| `inhalte/` | Freigegebene Textentwürfe, Konzept (`KONZEPT.md`), **offene Punkte (`OFFENE-PUNKTE.md`)** |

Seitenadressen:

| Seite | Deutsch | Englisch | Quelldatei |
|---|---|---|---|
| Startseite | `/de/` | `/en/` | `home.html` |
| Leistungen | `/de/leistungen/` | `/en/services/` | `services.html` |
| Projekterfahrung | `/de/projekterfahrung/` | `/en/project-experience/` | `experience.html` |
| Über ITCoreNet | `/de/ueber-itcorenet/` | `/en/about/` | `about.html` |
| Kontakt | `/de/kontakt/` | `/en/contact/` | `contact.html` |
| Danke-Seite | `/de/kontakt/danke/` | `/en/contact/thank-you/` | `thanks.html` |
| Impressum | `/de/impressum/` | `/en/legal-notice/` | `imprint.html` |
| Datenschutz | `/de/datenschutz/` | `/en/privacy/` | `privacy.html` |

## 2. Texte ändern

1. Datei in `src/pages/de/` öffnen (z. B. `services.html`) und den Text zwischen den HTML-Markierungen ändern.
2. **Dieselbe Änderung in `src/pages/en/`** machen – beide Sprachen müssen inhaltlich gleich bleiben.
3. Ganz oben in jeder Datei stehen Seitentitel (`title`) und Beschreibung für Suchmaschinen (`description`).
4. Website neu bauen (Abschnitt 3) und prüfen.

Rechtlich relevante Texte (Impressum, Datenschutz) nur nach Prüfung ändern und **nie maschinell übersetzen**.
Neue Fotos oder Grafiken nur mit geklärter Lizenz verwenden und in `gestaltung/LIZENZEN.md` eintragen.

## 3. Bauen

Voraussetzung: Python 3 (ohne Zusatzpakete).

```
python3 build.py              # Vorschau-Build
python3 build.py --release    # Veröffentlichungs-Build
```

Der Veröffentlichungs-Build **bricht ab**, solange in einem Text noch eine Markierung `[OFFEN …]` steht
(z. B. in der Datenschutzerklärung). So kann nichts Unfertiges online gehen.

## 4. Lokal ansehen

```
python3 build.py
php -S localhost:8000 -t dist
```
Dann im Browser `http://localhost:8000/de/` öffnen.
Hinweis: Der einfache PHP-Server wertet die `.htaccess` nicht aus (keine Weiterleitungen, keine Sicherheits-Header).
Das Kontaktformular braucht keine Einrichtung (siehe Abschnitt 6); E-Mails verschickt der einfache PHP-Server je nach System nicht.

## 5. Tests

| Test | Aufruf | Prüft |
|---|---|---|
| Browser | `NODE_PATH=$(npm root -g) node tests/browser-tests.js` | alle Seiten in 4 Bildschirmgrößen, Links, fremde Anfragen, Cookies, Barrierefreiheit (axe-core), Tastatur, Menü, Animation, Kontaktformular inkl. Spam-Schutz |
| Server | `sh tests/server-check.sh` | Weiterleitungen, gesperrte Dateien, Sicherheits-Header, Komprimierung |

Beide Tests laufen gegen einen **lokalen Apache-Testserver** (wie bei IONOS) und rufen nie die Live-Website auf.

## 6. Kontaktformular

Funktioniert ohne Einrichtung: Empfänger und Absender sind `support@itcorenet.com`, der geheime Schlüssel wird
beim ersten Aufruf automatisch erzeugt und in `formular/daten/schluessel.php` gespeichert (von außen gesperrt).
Nur für abweichende Einstellungen `formular/config.php` nach Vorlage `formular/config.example.php` anlegen.
Der Ordner `formular/daten/` muss für PHP beschreibbar sein (bei IONOS Standard).

Spam-Schutz ohne Fremddienst: verstecktes Fallen-Feld, Mindest-Ausfülldauer (3 s), signierter Zeitstempel,
höchstens 5 Nachrichten pro Stunde und IP-Adresse (IP nur als HMAC-Prüfwert, max. 1 Stunde gespeichert).

## 7. Veröffentlichen auf IONOS (nur nach ausdrücklicher Freigabe)

Ausführliche Schritt-für-Schritt-Anleitung mit FileZilla: **[`ANLEITUNG-VEROEFFENTLICHUNG.md`](ANLEITUNG-VEROEFFENTLICHUNG.md)**

**DNS, MX-Einträge und E-Mail-Einstellungen werden dabei nicht verändert.**

1. **Zugang:** Im IONOS-Kundenbereich unter *Hosting → SFTP & SSH* einen eigenen SFTP-Benutzer anlegen.
   Niemals das Hauptpasswort des IONOS-Kontos verwenden oder weitergeben. Zugangsdaten nie ins Repository.
2. **Sicherung:** Den kompletten bisherigen Webspace per SFTP herunterladen (z. B. mit FileZilla) und an einem
   sicheren Ort aufbewahren – inklusive `.htaccess` und versteckter Dateien. Ordner benennen, z. B.
   `sicherung-website-2026-10-xx`. Diese Sicherung **nicht löschen**, bis die neue Seite stabil läuft.
3. **Bauen:** `python3 build.py --release`
4. **Testen vor dem Umschalten:** Inhalt von `dist/` zuerst in einen separaten Ordner hochladen und dort prüfen
   (Vorgehen wird vor dem Deployment gemeinsam festgelegt – siehe `inhalte/OFFENE-PUNKTE.md`).
5. **Umschalten:** Alte Website-Dateien im Wurzelordner in einen Archivordner verschieben (nicht löschen),
   dann den Inhalt von `dist/` in den Wurzelordner hochladen.
6. **Prüfen:** alle Seiten, Links, Sprachwechsel, Kontaktformular (Testnachricht), Impressum, Datenschutz, HTTPS,
   Weiterleitungen (`itcorenet.de`, alte `/index.html`), Handy-Ansicht – **und dass E-Mails an support@itcorenet.com
   weiterhin ankommen**.

## 8. Zurück zur alten Website (Rollback)

1. Neue Dateien im Wurzelordner in einen Ordner `neu-zurueckgezogen` verschieben.
2. Die gesicherten alten Dateien (Schritt 7.2) wieder in den Wurzelordner hochladen – inklusive `.htaccess`.
3. Startseite aufrufen und prüfen. E-Mail ist davon nie betroffen, da DNS und MX nicht verändert werden.

## 9. Website später aktualisieren

1. Texte/Bilder in `src/` ändern (Abschnitt 2).
2. `python3 build.py --release` und Tests ausführen (Abschnitt 5).
3. Nur die geänderten Dateien aus `dist/` per SFTP hochladen – den Ordner `formular/daten/` auf dem Server nicht überschreiben oder löschen.
4. Bei Änderungen an der Technik (Formular, Skripte) die Datenschutzerklärung prüfen.
