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
| 5 | Speicherdauer der Server-Logdateien bei IONOS Webhosting Pro → in Datenschutzerklärung eintragen |
| 6 | Zeigen `itcorenet.de`, `www.itcorenet.de` und `itcorenet.com` (ohne www) auf denselben Webspace? Nur dann greifen die Weiterleitungen aus der `.htaccess` ohne DNS-Änderung |
| 7 | PHP-Version des Webspace (empfohlen: 8.1 oder neuer; lokal getestet mit 8.3) |
| 8 | Test-Strategie vor dem Umschalten festlegen (die Seite nutzt Pfade ab Domain-Wurzel; ein Test in einem Unterordner reicht dafür nicht, eine Test-Subdomain wäre eine DNS-Ergänzung und braucht Freigabe) |
| 9 | Datum „Stand“ der Datenschutzerklärung beim Veröffentlichen eintragen |

## Nicht geprüft (Werkzeug in der Entwicklungsumgebung nicht verfügbar)

- Darstellung in **Firefox, Safari und Edge** – getestet wurde mit Chromium (Grundlage von Chrome und Edge).
  Empfehlung: nach dem Test-Upload auf eigenen Geräten (iPhone/Safari, Windows/Edge, Firefox) ansehen.
- Echter Mailversand über den IONOS-Mailserver (lokal wird mail() in eine Datei umgeleitet).

## Empfehlung

Impressum und Datenschutzerklärung vor der Veröffentlichung juristisch prüfen lassen.

## Erledigt

- AV-Vertrag mit IONOS abgeschlossen (laut Inhaber, 01.10.2026) – in Datenschutzerklärung DE/EN eingetragen
- SFTP-Benutzer bei IONOS angelegt (laut Inhaber)

- Anschrift der Aufsichtsbehörde aktualisiert: Wilhelmstraße 7, 65185 Wiesbaden (Umzug am 16.03.2026,
  laut Pressemitteilung des HBDI)
- Kein Hinweis zur Verbraucherschlichtung nötig (siehe `KONZEPT.md`)
