#!/usr/bin/env python3
"""Baut die ITCoreNet-Website aus src/ nach dist/.

Aufruf:  python3 build.py              (Vorschau)
         python3 build.py --release    (Veröffentlichung; bricht ab, solange [OFFEN]-Punkte im Text stehen)
         python3 build.py --release --zip   (zusätzlich ZIP-Paket zum Hochladen)
Ergebnis: Ordner dist/ – genau dieser Inhalt wird auf den IONOS-Webspace hochgeladen.

Benötigt nur Python 3 (keine Zusatzpakete).
"""
import hashlib
import html
import sys
import zipfile
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
BASE_URL = "https://www.itcorenet.com"

# Seiten: Schlüssel -> (deutscher Pfad, englischer Pfad, im Menü?, in Sitemap?)
PAGES = {
    "home":       ("",                  "",                     None,         True),
    "services":   ("leistungen/",       "services/",            "services",   True),
    "experience": ("projekterfahrung/", "project-experience/",  "experience", True),
    "about":      ("ueber-itcorenet/",  "about/",               "about",      True),
    "contact":    ("kontakt/",          "contact/",             "contact",    True),
    "thanks":     ("kontakt/danke/",    "contact/thank-you/",   None,         False),
    "imprint":    ("impressum/",        "legal-notice/",        None,         False),
    "privacy":    ("datenschutz/",      "privacy/",             None,         False),
}
NAV = ["services", "experience", "about", "contact"]

LABELS = {
    "de": {
        "nav": {"services": "Leistungen", "experience": "Projekterfahrung", "about": "Über ITCoreNet", "contact": "Kontakt"},
        "skip": "Zum Inhalt springen", "menu": "Menü", "mainnav": "Hauptnavigation", "legalnav": "Rechtliches",
        "cta": "Anfrage senden", "home": "ITCoreNet – zur Startseite", "langname": "Deutsch",
        "imprint": "Impressum", "privacy": "Datenschutz", "switch": "Sprache wählen", "locale": "de_DE",
    },
    "en": {
        "nav": {"services": "Services", "experience": "Project experience", "about": "About ITCoreNet", "contact": "Contact"},
        "skip": "Skip to content", "menu": "Menu", "mainnav": "Main navigation", "legalnav": "Legal",
        "cta": "Send an enquiry", "home": "ITCoreNet – go to home page", "langname": "English",
        "imprint": "Legal notice", "privacy": "Privacy", "switch": "Choose language", "locale": "en_GB",
    },
}


def url(lang, key):
    return f"/{lang}/" + PAGES[key][0 if lang == "de" else 1]


def read_page(path):
    """Seitendatei: JSON-Kopf zwischen zwei '---'-Zeilen, danach HTML."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise SystemExit(f"Kopfbereich fehlt: {path}")
    return json.loads(m.group(1)), m.group(2)


def strip_comments(s):
    return re.sub(r"<!--(?!\[).*?-->", "", s, flags=re.S)


def layout(lang, key, meta, body):
    L = LABELS[lang]
    other = "en" if lang == "de" else "de"
    e = html.escape
    canonical = BASE_URL + url(lang, key)
    alt_de, alt_en = BASE_URL + url("de", key), BASE_URL + url("en", key)
    robots = '<meta name="robots" content="noindex, follow">' if meta.get("noindex") else ""

    current = ' aria-current="page"'
    nav_items = "".join(
        f'<li><a href="{url(lang, k)}"{current if k == key else ""}>{L["nav"][k]}</a></li>'
        for k in NAV
    )
    lang_switch = (
        f'<li class="lang" aria-label="{L["switch"]}">'
        f'<span aria-current="true" lang="{lang}">{lang.upper()}</span><span aria-hidden="true">|</span>'
        f'<a href="{url(other, key)}" hreflang="{other}" lang="{other}">'
        f'<span class="visually-hidden">{LABELS[other]["langname"]}: </span>{other.upper()}</a></li>'
    )
    scripts = "".join(f'<script src="/assets/js/{s}.js?v={VERSION}" defer></script>' for s in meta.get("scripts", []))
    jsonld = ""
    if key == "home":
        data = {
            "@context": "https://schema.org", "@type": "ProfessionalService", "name": "ITCoreNet",
            "url": BASE_URL + f"/{lang}/", "logo": BASE_URL + "/assets/img/itcorenet-logo.svg",
            "image": BASE_URL + "/assets/img/og-image.png", "email": "support@itcorenet.com",
            "founder": {"@type": "Person", "name": "Alessandro Kempka"},
            "address": {"@type": "PostalAddress", "streetAddress": "Jägerstr. 10 C", "postalCode": "63322",
                        "addressLocality": "Rödermark", "addressCountry": "DE"},
            "vatID": "DE202184042", "knowsLanguage": ["de", "en"],
        }
        jsonld = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"

    php_head = meta.get("php_head", "")
    return f"""{php_head}<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(meta["title"])}</title>
<meta name="description" content="{e(meta["description"])}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="de" href="{alt_de}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_de}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ITCoreNet">
<meta property="og:title" content="{e(meta["title"])}">
<meta property="og:description" content="{e(meta["description"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{L["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#011e3c">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={VERSION}">
<script src="/assets/js/main.js?v={VERSION}"></script>
{scripts}
{jsonld}
</head>
<body>
<a class="skip-link" href="#inhalt">{L["skip"]}</a>
<header class="site-header">
<div class="wrap">
<a class="logo" href="/{lang}/"><img src="/assets/img/itcorenet-logo-quer.svg" alt="{L["home"]}" width="165" height="34"></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg><span class="visually-hidden">{L["menu"]}</span></button>
<nav class="site-nav" id="site-nav" aria-label="{L["mainnav"]}">
<ul>{nav_items}{lang_switch}<li class="nav-cta"><a class="btn btn--primary" href="{url(lang, "contact")}">{L["cta"]}</a></li></ul>
</nav>
</div>
</header>
<main id="inhalt" tabindex="-1">
{body.strip()}
</main>
<footer class="site-footer on-dark">
<div class="wrap">
<div class="brand"><img src="/assets/img/itcorenet-logo-quer-invers.svg" alt="ITCoreNet" width="126" height="26"><span>© {date.today().year}</span></div>
<nav aria-label="{L["legalnav"]}"><ul>
<li><a href="{url(lang, "imprint")}">{L["imprint"]}</a></li>
<li><a href="{url(lang, "privacy")}">{L["privacy"]}</a></li>
<li><a href="{url(lang, "contact")}">{L["nav"]["contact"]}</a></li>
</ul></nav>
</div>
</footer>
</body>
</html>
"""


def asset_version():
    """Prüfsumme über CSS und JS: ändert sich nur, wenn sich die Dateien ändern."""
    h = hashlib.sha256()
    for f in sorted((SRC / "assets").rglob("*")):
        if f.suffix in (".css", ".js"):
            h.update(f.read_bytes())
    return h.hexdigest()[:10]


VERSION = asset_version()
RELEASE = "--release" in sys.argv
_MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
STAND_DE = f"{_MONATE[date.today().month - 1]} {date.today().year}"   # „Stand“ der Datenschutzerklärung = Monat des Builds
STAND_EN = date.today().strftime("%B %Y")


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(SRC / "assets", DIST / "assets")
    shutil.copytree(SRC / "formular", DIST / "formular",
                    ignore=shutil.ignore_patterns("config.php", "daten"))
    for name in (".htaccess",):
        shutil.copy(SRC / name, DIST / name)

    sitemap = []
    for key in PAGES:
        for lang in ("de", "en"):
            meta, body = read_page(SRC / "pages" / lang / f"{key}.html")
            out_dir = DIST / url(lang, key).strip("/")
            out_dir.mkdir(parents=True, exist_ok=True)
            page = strip_comments(layout(lang, key, meta, body)).replace("{VERSION}", VERSION)
            page = page.replace("{STAND_DE}", STAND_DE).replace("{STAND_EN}", STAND_EN)
            # {SVG:name} bettet src/partials/name.svg direkt ein (für per CSS animierte Grafiken)
            page = re.sub(r"\{SVG:([a-z0-9-]+)\}",
                          lambda m: (SRC / "partials" / f"{m.group(1)}.svg").read_text(encoding="utf-8").strip(), page)
            page = re.sub(r"\n{2,}", "\n", page)
            (out_dir / ("index.php" if meta.get("php") else "index.html")).write_text(page, encoding="utf-8")
        if PAGES[key][3]:
            sitemap.append(key)

    # 404-Seite (zweisprachig)
    meta, body = read_page(SRC / "pages" / "404.html")
    page = strip_comments(layout("de", "home", meta, body)).replace("{VERSION}", VERSION)
    page = page.replace(f'<link rel="canonical" href="{BASE_URL}/de/">', "")
    page = re.sub(r'<link rel="alternate"[^>]*>\n?', "", page)
    page = re.sub(r'<script type="application/ld\+json">.*?</script>', "", page, flags=re.S)
    (DIST / "404.html").write_text(re.sub(r"\n{2,}", "\n", page), encoding="utf-8")

    # Sitemap mit Sprachverweisen
    today = date.today().isoformat()
    rows = []
    for key in sitemap:
        for lang in ("de", "en"):
            rows.append(
                f"<url><loc>{BASE_URL}{url(lang, key)}</loc><lastmod>{today}</lastmod>"
                f'<xhtml:link rel="alternate" hreflang="de" href="{BASE_URL}{url("de", key)}"/>'
                f'<xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}{url("en", key)}"/>'
                f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}{url("de", key)}"/></url>'
            )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nDisallow: /formular/\n\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    todos = [str(f.relative_to(DIST)) for f in DIST.rglob("*") if f.suffix in (".html", ".php")
             and 'class="todo"' in f.read_text(encoding="utf-8")]
    if todos:
        print("ACHTUNG – offene Punkte ([OFFEN]) in:", ", ".join(sorted(todos)))
        if RELEASE:
            shutil.rmtree(DIST)
            raise SystemExit("Abbruch: Für die Veröffentlichung müssen alle [OFFEN]-Punkte erledigt sein.")
    print(f"Fertig: {sum(1 for _ in DIST.rglob('*') if _.is_file())} Dateien in {DIST}")
    if "--zip" in sys.argv:
        make_package()


ARCHIVE_HTACCESS = "# Archiv der alten Website – nicht aus dem Internet abrufbar\nRequire all denied\n"
DE_REDIRECT_HTACCESS = (
    "# itcorenet.de dauerhaft auf die deutsche Seite von www.itcorenet.com umleiten (keine DNS-Änderung)\n"
    "<IfModule mod_rewrite.c>\n  RewriteEngine On\n  RewriteRule ^ https://www.itcorenet.com/de/ [R=301,L]\n</IfModule>\n"
)


def make_package():
    """ZIP zum Hochladen per FileZilla – siehe ANLEITUNG-VEROEFFENTLICHUNG.md."""
    if not RELEASE:
        raise SystemExit("Das Paket wird nur zusammen mit --release erzeugt.")
    name = ROOT / f"itcorenet-website-{date.today().isoformat()}.zip"
    with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(DIST.rglob("*")):
            if f.is_file():
                z.write(f, "website/" + str(f.relative_to(DIST)))
        z.writestr("fuer-archivordner/.htaccess", ARCHIVE_HTACCESS)
        z.writestr("fuer-itcorenet-de/.htaccess", DE_REDIRECT_HTACCESS)
        z.write(ROOT / "ANLEITUNG-VEROEFFENTLICHUNG.md", "ANLEITUNG-VEROEFFENTLICHUNG.md")
    print(f"Paket: {name.name}")


if __name__ == "__main__":
    build()
