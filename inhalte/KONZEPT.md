# Konzept – abgestimmte Entscheidungen

Stand: 01.10.2026. Grundlage: Audit der bisherigen Website (www.itcorenet.com, Stand 2017) und
Entscheidungen des Inhabers.

## Domain und Sprachen

- `itcorenet.com/de/` – Deutsch, `itcorenet.com/en/` – Englisch, beide vollständig
- `itcorenet.de` und `www.itcorenet.de` → dauerhafte Weiterleitung (301) auf `itcorenet.com/de/`
- Hauptadresse: **`https://www.itcorenet.com`** (die heutige Website läuft unter www; `itcorenet.com` ohne www
  wird – sofern es auf denselben Webspace zeigt – dorthin umgeleitet)
- `/` → Weiterleitung auf `/de/`; alte Adresse `/index.html` → `/en/`
- **DNS, MX-Einträge und E-Mail werden nicht verändert.** `support@itcorenet.com` muss weiter
  funktionieren. Die Weiterleitung von `itcorenet.de` soll ohne DNS-Änderung über `.htaccess`
  erfolgen (vor dem Deployment zu prüfen).

## Unternehmen

- Einzelunternehmen (Gewerbe), Inhaber Alessandro Kempka, keine Angestellten
- Zielgruppe: Unternehmen und Privatkunden
- Nicht im Handelsregister eingetragen (kein e. K.) – keine Registerangabe im Impressum
- USt-IdNr. DE202184042
- Keine Preise auf der Website; die Preisgestaltung bleibt bewusst offen
  („Jedes Vorhaben ist anders. Sie erhalten ein individuelles Angebot …“)
- Berufserfahrung: „mehr als 20 Jahre“ (vom Inhaber bestätigt), keine genauere Zahl
- Vom Inhaber bestätigt: Projektleitung auch international; Projekte auf Deutsch und Englisch;
  Impressum-Adresse ist zugleich Geschäftssitz (Rödermark)
- Website und Projektsprachen: nur Deutsch und Englisch
- Texte suggerieren kein Team und keine Firmengröße
- Managed Services nur allgemein: „Laufende Betreuung der IT nach individuell vereinbartem
  Umfang“ – keine konkreten Zusagen (z. B. 24/7, Helpdesk, Patch-Management, Monitoring), solange
  nicht ausdrücklich bestätigt

## Verbraucherschlichtung (Prüfergebnis, keine Rechtsberatung)

- **Website:** Kein Hinweis nötig. Die allgemeine Informationspflicht nach § 36 VSBG gilt nicht für
  Unternehmer mit höchstens 10 Beschäftigten (§ 36 Abs. 3 VSBG); ITCoreNet hat keine Angestellten.
  Ein freiwilliger Standardsatz wird bewusst nicht aufgenommen.
- **EU-Plattform zur Online-Streitbeilegung:** Die Plattform wurde am 20.07.2025 eingestellt
  (Verordnung (EU) 2024/3228); ein Link ist nicht mehr nötig.
- **Wichtig für den Geschäftsalltag:** Kommt es mit einem Privatkunden zu einem Streit, der nicht
  beigelegt werden kann, gilt § 37 VSBG unabhängig von der Betriebsgröße: Dann muss der Kunde in
  Textform auf eine zuständige Verbraucherschlichtungsstelle hingewiesen werden, mit der Angabe, ob
  ITCoreNet zur Teilnahme bereit ist. Das betrifft nicht die Website.
- Sobald ITCoreNet mehr als 10 Beschäftigte hat, neu prüfen.

## Positionierung

- **Claim:** „IT beraten. Umsetzen. Betreiben.“ / „Advise. Implement. Operate.“
- **Kernaussage:** ITCoreNet verbindet IT-Beratung mit Umsetzung: Lösungen werden gemeinsam
  entwickelt, praktisch umgesetzt und auf Wunsch im laufenden Betrieb betreut.

## Leistungsbereiche

1. IT-Beratung & IT-Management (inkl. CIO as a Service / vCIO)
2. IT-Projekte & Infrastruktur
3. Hardware-Beschaffung & Lifecycle
4. Managed Services

Veraltete Produkte und Versionen (Exchange 2003/2013, SCCM, MobileIron) werden nicht als heutiges
Angebot genannt.

## Seiten

| Seite | Deutsch | Englisch |
|---|---|---|
| Startseite | `/de/` | `/en/` |
| Leistungen | `/de/leistungen/` | `/en/services/` |
| Ausgewählte Projekterfahrung | `/de/projekterfahrung/` | `/en/project-experience/` |
| Über ITCoreNet | `/de/ueber-itcorenet/` | `/en/about/` |
| Kontakt | `/de/kontakt/` | `/en/contact/` |
| Kontakt – Danke | `/de/kontakt/danke/` | `/en/contact/thank-you/` |
| Impressum | `/de/impressum/` | `/en/legal-notice/` |
| Datenschutz | `/de/datenschutz/` | `/en/privacy/` |
| Fehlerseite | `/404.html` (zweisprachig) | |

## Projekterfahrung

Die fünf Projekte der alten Website stammen aus früheren Anstellungen des Inhabers. Sie werden
anonymisiert und ausdrücklich **nicht** als Kundenprojekte von ITCoreNet dargestellt. Ohne
Kundennamen, Logos, Standorte und Erfolgszahlen; Größenordnungen nur gerundet. Keine
Verschwiegenheitspflicht steht entgegen (bestätigt).

## Gestaltung

Hell, viel Weißraum, klare Typografie, eine Akzentfarbe aus dem Logo, Linien-Icons und einfache
Schaubilder. Keine Stockfotos, keine Partikel- oder Hacker-Optik, keine großen Animationen.
Alte Bilder werden nicht übernommen; das Logo hat der Inhaber selbst erstellt.

## Technik

Statisches HTML/CSS, minimales eigenes JavaScript, PHP nur für das Kontaktformular (Versand über
den IONOS-Mailserver, ohne externen Formulardienst und ohne externes CAPTCHA). Kein jQuery, kein
Bootstrap, keine Datenbank, lokale Schriften, keine Drittanbieter-Anfragen. Sicherheits-Header,
Komprimierung, Caching, Sitemap, robots.txt, Canonical, hreflang, Barrierearmut, Mobiloptimierung.
Hosting: IONOS Webhosting Pro.

## Logo-Animation (Entscheidung des Inhabers)

- Nachbau der ursprünglichen GIF-Animation als Canvas-Skript (`gestaltung/animation/`), ca. 10 KB
- Einsatz auf **beiden** Seiten: im Kopfbereich der Startseite (statt des drehenden Punkt-Rings)
  und als Eröffnung der Seite „Über ITCoreNet“
- Läuft pro Seitenaufruf einmal ab und steht dann still; bei „Bewegung reduzieren“ sofort fertiges Logo
- Kein „schon gesehen“-Merker im Browser (würde nach § 25 TDDDG eine Einwilligung erfordern)
- Nennung des Neffen: vorerst nicht (Inhaber fragt nach)
