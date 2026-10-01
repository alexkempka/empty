# Offene Punkte

Stand: 02.10.2026. **Die neue Website ist seit 01./02.10.2026 online** (www.itcorenet.com, DE/EN).

## Offen

| # | Punkt | Wer |
|---|---|---|
| 1 | **Kontaktformular verschickt keine E-Mails:** IONOS-Mailversand aus dem Webspace scheitert mit „535 Authentication credentials invalid“ für den IONOS-internen Versandbenutzer (laut msmtp-Protokoll). Liegt bei IONOS → Support-Ticket. Besucher erhalten bis dahin den Hinweis, direkt an support@itcorenet.com zu schreiben | Inhaber (IONOS-Support) |
| 2 | Danach: Zustellung bei Microsoft 365 testen (SPF erlaubt nur Microsoft). Bei Spam/Ablehnung: IONOS in SPF ergänzen (DNS-Änderung, braucht ausdrückliche Freigabe) oder Versand über Microsoft-365-SMTP | gemeinsam |
| 3 | **PHP Extended Support kündigen** – alle Domains stehen seit 02.10.2026 auf PHP 8.4 (Anleitung Schritt 6) | Inhaber |
| 4 | Darstellung in **Firefox und Safari** prüfen (Opera und Edge: vom Inhaber geprüft, in Ordnung) | Inhaber |
| 5 | Logo (LogoMaker.com, Kauf 17.04.2017): Nutzung auf der Website erlaubt (Nutzungsbedingungen 08/2026, Logo-Dienste 2.1 und 22.7); Symbol nicht exklusiv, daher Markenanmeldung des Symbols unsicher. Favicon/Apple-Touch-Icon (nur Symbol) bleiben – Entscheidung des Inhabers vom 01.10.2026. Optional: Kaufbeleg ablegen | Inhaber, optional |
| 10 | – (Updates „Startseite lebendiger + Themen“ und „Animation IT-Landschaft“ am 01.10.2026 hochgeladen und live geprüft) | erledigt |
| 6 | Nennung des Neffen (Logo-Animation) – nur mit dessen Einverständnis | Inhaber |
| 7 | Außerhalb der Website: DKIM und DMARC für itcorenet.com in Microsoft 365 einrichten (DNS-Änderung) | später |
| 8 | Impressum und Datenschutzerklärung juristisch prüfen lassen (Empfehlung) | Inhaber |
| 9 | Sicherung der alten Website (lokal + zweite Kopie) und Archivordner auf dem Server **nicht löschen**, bis die neue Seite einige Wochen stabil läuft | Inhaber |

## Erledigt (Veröffentlichung 01./02.10.2026)

- Sicherung des Webspace per SFTP: 310 Dateien, 0 Fehler
- Alte Website(s) nach `/_archiv-alte-website-2026-10-01/` und `/itcorenet_de/_archiv-2026-10-01/` verschoben, per `.htaccess` gesperrt (403, geprüft)
- Neue Website hochgeladen; alle Seiten 200, 404-Seite, Sitemap, robots.txt geprüft
- Weiterleitungen geprüft: `/` → `/de/`, `/index.html` → `/en/`, HTTP → HTTPS, `itcorenet.com` → `www`, `/itcorenet_de/` → `/de/`; `https://itcorenet.de` → `/de/` ohne Warnung (Inhaber)
- Sicherheits-Header (CSP, HSTS u. a.) und gzip-Komprimierung live geprüft; keine Cookies, kein X-Powered-By
- PHP für alle 10 Domains/Subdomains auf 8.4 umgestellt (Ursache des anfänglichen Fehlers 500 der Kontaktseiten: PHP 7.4)
- SSL-Zertifikat für `itcorenet.de` eingerichtet
- Formular-Schlüssel automatisch erzeugt, von außen gesperrt (403)
- Diagnose-Dateien (`php.ini`, `mail.log`, `debug.log`) nach dem Test zu löschen – enthielten interne IONOS-Zugangsdaten
- Speicherdauer IONOS-Logdateien max. 7 Tage (AVV-Anhang 1, v3.0 03/2026); AV-Vertrag abgeschlossen; Aufsichtsbehörde Wilhelmstraße 7, 65185 Wiesbaden
- Seitenzähler: vom Inhaber abgelehnt
