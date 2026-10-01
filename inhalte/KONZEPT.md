# Konzept – abgestimmte Entscheidungen

Stand: 01.10.2026. Grundlage: Audit der bisherigen Website (www.itcorenet.com, Stand 2017) und
Entscheidungen des Inhabers.

## Domain und Sprachen

- `itcorenet.com/de/` – Deutsch, `itcorenet.com/en/` – Englisch, beide vollständig
- `itcorenet.de` und `www.itcorenet.de` → dauerhafte Weiterleitung (301) auf `itcorenet.com/de/`
- `itcorenet.com/` → Weiterleitung auf `/de/`; alte Adresse `/index.html` → `/en/`
- **DNS, MX-Einträge und E-Mail werden nicht verändert.** `support@itcorenet.com` muss weiter
  funktionieren. Die Weiterleitung von `itcorenet.de` soll ohne DNS-Änderung über `.htaccess`
  erfolgen (vor dem Deployment zu prüfen).

## Unternehmen

- Einzelunternehmen (Gewerbe), Inhaber Alessandro Kempka, keine Angestellten
- Zielgruppe: Unternehmen und Privatkunden
- Kein Preisbereich; Leistungen werden individuell angeboten
- Keine konkrete Jahreszahl zur Berufserfahrung
- Texte suggerieren kein Team und keine Firmengröße

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
