# Anleitung: Neue Website auf IONOS veröffentlichen

Für Alessandro – Schritt für Schritt mit dem Programm **FileZilla**.
Zeitbedarf: ca. 30–45 Minuten. **E-Mail, DNS und MX-Einträge werden dabei nicht angefasst.**

Du bekommst von mir ein ZIP-Paket `itcorenet-website-JJJJ-MM-TT.zip`. Es enthält:

| Ordner im Paket | Wofür |
|---|---|
| `website/` | Die neue Website – kommt in den Website-Ordner auf dem Webspace |
| `fuer-archivordner/.htaccess` | Sperrt den Archivordner mit der alten Website gegen Abruf aus dem Internet |
| `fuer-itcorenet-de/.htaccess` | Nur nötig, falls `itcorenet.de` auf einen **eigenen** Ordner zeigt (siehe Schritt 1) |

---

## Schritt 0 – FileZilla einrichten

1. FileZilla **Client** von der offiziellen Seite `filezilla-project.org` laden. Beim Installieren
   angebotene Zusatzprogramme **ablehnen**.
2. In FileZilla: *Datei → Servermanager → Neuer Server*
   - Protokoll: **SFTP – SSH File Transfer Protocol**
   - Server: die Adresse aus dem IONOS-Kundenbereich (*Hosting → SFTP & SSH*), Port **22**
   - Verbindungsart: *Normal*, Benutzer und Passwort deines **SFTP-Benutzers** (nicht dein IONOS-Hauptpasswort)
3. Beim ersten Verbinden fragt FileZilla nach einem „unbekannten Server-Schlüssel“. Wenn IONOS auf der
   SFTP-Seite einen Fingerabdruck anzeigt, vergleichen; dann bestätigen.
4. Menü *Server → Anzeige versteckter Dateien erzwingen* einschalten (sonst fehlt die `.htaccess`).

## Schritt 1 – Nachsehen, wohin die Domains zeigen

Im IONOS-Kundenbereich unter *Domains & SSL* bei jeder Domain auf das Zahnrad → *Ziel/Verwendung* schauen und notieren:

| Domain | zeigt auf Ordner |
|---|---|
| `www.itcorenet.com` | |
| `itcorenet.com` | |
| `itcorenet.de` / `www.itcorenet.de` | |

Außerdem unter *Hosting → PHP-Einstellungen* die **PHP-Version** notieren (8.1 oder neuer).
Hier **nichts ändern** – nur nachsehen. Die Notizen schickst du mir; danach sage ich dir, ob Schritt 4b nötig ist.

## Schritt 2 – Sicherung der alten Website (Pflicht!)

1. In FileZilla rechts den **gesamten Webspace** markieren (alle Ordner und Dateien, auch versteckte).
2. Rechtsklick → *Herunterladen* in einen neuen Ordner auf deinem Rechner, z. B. `Sicherung-Website-2026-10-xx`.
3. Den Ordner zusätzlich als ZIP an einem zweiten Ort speichern (z. B. USB-Stick oder Cloud-Speicher).
4. Stichprobe: Liegt in der Sicherung die alte `index.html` und der Ordner `base/`? Dann ist sie vollständig.

**Diese Sicherung nicht löschen**, bis die neue Seite mindestens einige Wochen stabil läuft.

## Schritt 3 – Alte Website im Webspace beiseitelegen

Im Ordner, auf den `www.itcorenet.com` zeigt (Schritt 1):

1. Neuen Ordner anlegen: `_archiv-alte-website-2026-10-xx`
2. Die **alten Website-Dateien** in diesen Ordner verschieben (in FileZilla rechts per Ziehen):
   `index.html`, `base/`, ggf. `favicon.ico`, alte `.htaccess` und alles andere, was zur alten Seite gehört.
   **Nicht verschieben:** Ordner, die zu anderen Domains oder Diensten gehören – im Zweifel vorher fragen.
3. Die Datei `fuer-archivordner/.htaccess` aus dem Paket **in den Archivordner** hochladen.
   Damit ist die alte Seite nicht mehr aus dem Internet abrufbar, bleibt aber vollständig erhalten.

Ab hier ist die Website für wenige Minuten nicht erreichbar – also zügig weiter mit Schritt 4.

## Schritt 4 – Neue Website hochladen

**4a.** Den **Inhalt** des Paket-Ordners `website/` (nicht den Ordner selbst) in den Website-Ordner hochladen.
Danach liegen dort u. a. `.htaccess`, `404.html`, `de/`, `en/`, `assets/`, `formular/`, `robots.txt`, `sitemap.xml`.

**4b.** Nur falls `itcorenet.de` auf einen **eigenen** Ordner zeigt (Schritt 1): Dessen Inhalt ebenfalls sichern
(Schritt 2) und beiseitelegen (Schritt 3) und dann `fuer-itcorenet-de/.htaccess` dort hochladen. Diese Datei
leitet `itcorenet.de` dauerhaft auf `https://www.itcorenet.com/de/` um – ganz ohne DNS-Änderung.

## Schritt 4c – PHP-Version umstellen

Laut IONOS-Hilfe: *Menü → Hosting → Kachel „PHP“ → Verwalten*. Alle Einträge markieren (Kontrollkästchen oben links),
dann **PHP-Version auswählen** → die **neueste 8er-Version** (z. B. 8.3 oder 8.4) → **Speichern**.
Unbedenklich: Die alte Website nutzt kein PHP; die Microsoft-Subdomains zeigen per DNS direkt zu Microsoft
und werden von IONOS nie ausgeliefert. Es wird dabei **kein DNS** geändert.

## Schritt 4d – SSL-Zertifikat für itcorenet.de

Laut IONOS-Hilfe: *Menü → Domains & SSL → Kachel „Portfolio“ → bei „SSL-Zertifikate“ auf Verwalten →
„SSL-Zertifikat einrichten“* → beim gewünschten Zertifikat **Jetzt aktivieren** → Domain `itcorenet.de` wählen →
Verwendungszweck **„Für meine IONOS Website verwenden“** → Nutzungsbedingungen bestätigen → **SSL-Zertifikat einrichten**.
**Achtung Kosten:** Nur ein Zertifikat wählen, das in deinem Vertrag ohne Aufpreis enthalten ist. Wird ein Preis
angezeigt, erst abbrechen und mir Bescheid geben. (`itcorenet.com` hat bereits ein gültiges Zertifikat.)

## Schritt 5 – Prüfen

Im Browser (am besten in einem privaten Fenster):

- [ ] `https://www.itcorenet.com` → landet auf der deutschen Startseite, Animation läuft
- [ ] `itcorenet.com` und `http://www.itcorenet.com` → leiten auf `https://www.itcorenet.com/de/` um
- [ ] `itcorenet.de` → landet auf `https://www.itcorenet.com/de/`
- [ ] alle Menüpunkte auf Deutsch und Englisch, Sprachwechsel DE/EN
- [ ] Impressum und Datenschutz (Deutsch und Englisch)
- [ ] Kontaktformular: Testnachricht senden → Danke-Seite → **E-Mail kommt bei support@itcorenet.com an**
- [ ] Antwort auf diese Test-Mail geht an die eingegebene Adresse
- [ ] Eine normale E-Mail an support@itcorenet.com von außen kommt weiterhin an
- [ ] Handy: Seite aufrufen, Menü öffnen und schließen
- [ ] Safari (iPhone/Mac), Edge, Firefox kurz ansehen

Schick mir das Ergebnis – bei Auffälligkeiten mit Bildschirmfoto.

## Schritt 6 – PHP Extended Support kündigen

Erst wenn alles läuft: Der Extended Support endet **nicht automatisch**. Laut IONOS-Hilfe wird er als
„Zusatzartikel“ gekündigt (Hilfe-Artikel „Zusatzartikel kündigen“) oder über den IONOS-Kundenservice.
Vorher in *Hosting → PHP* prüfen, dass **keine** Zeile mehr eine alte Version (5.x oder 7.x) zeigt.

## Spätere Aktualisierungen

Für Änderungen an der fertigen Website gibt es ein Update-Paket `itcorenet-update-….zip`, das nur den Ordner `website/` enthält.

1. ZIP entpacken. FileZilla verbinden, *Server → Anzeige versteckter Dateien erzwingen* muss eingeschaltet sein.
2. Links den entpackten Ordner `website` öffnen, rechts den Website-Ordner auf dem Server (dort liegen `de/`, `en/`, `assets/`).
3. Links **alles im Ordner `website`** markieren → Rechtsklick → *Hochladen*.
4. Bei „Zieldatei existiert bereits“: **Überschreiben** wählen und *Immer diese Aktion verwenden* ankreuzen.
5. **Nichts auf dem Server löschen.** Insbesondere `formular/daten/` bleibt unangetastet (dort liegt der automatisch erzeugte Formular-Schlüssel; er ist nicht im Paket).
6. Im Browser mit **Strg + F5** neu laden und prüfen.

## Notfall: Zurück zur alten Website

1. Neue Dateien im Website-Ordner in einen Ordner `_neu-zurueckgezogen` verschieben.
2. Die `.htaccess` im Archivordner löschen, dann den **Inhalt** des Archivordners zurück in den Website-Ordner
   verschieben – oder die Sicherung aus Schritt 2 wieder hochladen.
3. `https://www.itcorenet.com` aufrufen: Die alte Seite ist wieder da. E-Mail war zu keinem Zeitpunkt betroffen.
