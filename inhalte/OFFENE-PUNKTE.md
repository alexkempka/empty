# Offene Punkte vor der Veröffentlichung

Stand: 01.10.2026. Die Website ist fertig programmiert und lokal getestet. Diese Punkte sind noch offen.

## Vom Inhaber zu klären

| # | Punkt | Warum |
|---|---|---|
| 2 | **Logo-Lizenz:** Bei welchem Dienst wurde das Logo gekauft? Rechnung/Lizenzbedingungen ablegen | Dokumentation der Nutzungsrechte (`gestaltung/LIZENZEN.md`) |
| 3 | Nennung des Neffen (Logo-Animation) – nur mit dessen Einverständnis | Personenbezogene Angabe |

## Vor dem Deployment zu prüfen (mit IONOS-Zugang)

| # | Punkt |
|---|---|
| 6 | `itcorenet.de` zeigt vermutlich auf einen eigenen Ordner (alte deutsche Seite) → beim Upload prüfen und ggf. `fuer-itcorenet-de/.htaccess` dort ablegen (Anleitung Schritt 4b) |
| 7 | PHP-Version beim Umschalten auf 8.x stellen – **nur** für `www.itcorenet.com`, `itcorenet.com`, `itcorenet.de`; Microsoft-Subdomains (autodiscover, lyncdiscover, sip, enterpriseregistration, enterpriseenrollment, msoid) **nicht anfassen** |
| 7a | **SSL-Zertifikat für `itcorenet.de` fehlt** (rotes Schloss bei Domains & SSL) → `https://itcorenet.de` zeigt eine Browser-Warnung vor der Weiterleitung. Zertifikat in IONOS zuweisen (keine DNS-Änderung, braucht Freigabe) |
| 7b | **PHP Extended Support ist aktiv (kostenpflichtig)**. Er bleibt aktiv, solange irgendeine (Sub-)Domain eine alte Version nutzt, und muss nach der Umstellung separat gekündigt werden („Zusatzartikel kündigen“, IONOS-Hilfe). Die Microsoft-Subdomains zeigen per DNS zu Microsoft (autodiscover → outlook.com, enterprise* → Microsoft, msoid → microsoftonline) bzw. existieren nicht (lyncdiscover, sip) – ihre IONOS-PHP-Einstellung wird nie benutzt; Umstellung dort ändert kein DNS |
| 7c | **E-Mail läuft über Microsoft 365** (MX: itcorenet-com.mail.protection.outlook.com). SPF: `v=spf1 include:spf.protection.outlook.com -all` → Mails des Kontaktformulars über den IONOS-Mailserver mit Absender @itcorenet.com bestehen SPF nicht und landen evtl. im Spam oder werden abgelehnt. Beim Upload real testen; Lösungen: (1) IONOS in SPF aufnehmen – DNS-TXT-Änderung, braucht ausdrückliche Freigabe; (2) Versand über Microsoft-365-SMTP; (3) andere Absenderadresse |
| 7d | Hinweis außerhalb der Website: Für itcorenet.com sind kein DMARC und kein DKIM (selector1) eingerichtet → Schutz gegen gefälschte Absender fehlt. Mit Microsoft-365-Verwaltung besprechen (DNS-Änderung) |
| 8 | Test-Strategie vor dem Umschalten festlegen (die Seite nutzt Pfade ab Domain-Wurzel; ein Test in einem Unterordner reicht dafür nicht, eine Test-Subdomain wäre eine DNS-Ergänzung und braucht Freigabe) |

## Nicht geprüft (Werkzeug in der Entwicklungsumgebung nicht verfügbar)

- Darstellung in **Firefox, Safari und Edge** – getestet wurde mit Chromium (Grundlage von Chrome und Edge).
  Empfehlung: nach dem Test-Upload auf eigenen Geräten (iPhone/Safari, Windows/Edge, Firefox) ansehen.
- Echter Mailversand über den IONOS-Mailserver (lokal wird mail() in eine Datei umgeleitet).

## Empfehlung

Impressum und Datenschutzerklärung vor der Veröffentlichung juristisch prüfen lassen.

## Erledigt

- Seitenzähler: vom Inhaber abgelehnt – wird nicht eingebaut
- Ist-Stand PHP (01.10.2026): itcorenet.com 5.4, www.itcorenet.com und itcorenet.de 7.4, übrige 7.0 – alle ohne Community-Support. Alte Seite nutzt kein PHP → Umstellung unkritisch
- `itcorenet.com` (ohne www, A-Record 217.160.0.149) liefert byte-identisch dieselbe Startseite wie `www.itcorenet.com` (217.160.0.170) → sehr wahrscheinlich derselbe Webspace-Ordner; `.htaccess`-Weiterleitung auf www greift dann

- Speicherdauer der IONOS-Logdateien: max. 7 Tage – laut IONOS Anhang 1 zur AVV (geprüft in Version 3.0, Stand 03/2026, und Version 2.0), Abschnitt 4 „Hosting Produkte“
- „Stand“ der Datenschutzerklärung setzt build.py automatisch (Monat des Builds)

- AV-Vertrag mit IONOS abgeschlossen (laut Inhaber, 01.10.2026) – in Datenschutzerklärung DE/EN eingetragen
- SFTP-Benutzer bei IONOS angelegt (laut Inhaber)

- Anschrift der Aufsichtsbehörde aktualisiert: Wilhelmstraße 7, 65185 Wiesbaden (Umzug am 16.03.2026,
  laut Pressemitteilung des HBDI)
- Kein Hinweis zur Verbraucherschlichtung nötig (siehe `KONZEPT.md`)
