"""Erzeugt die Illustration 'IT-Landschaft' (selbst gezeichnet, keine fremden Vorlagen).
Aufruf: python3 gestaltung/grafiken/erzeuge-it-landschaft.py  ->  src/assets/img/it-landschaft.svg"""
import math, random
from pathlib import Path

W, H = 600, 460
CX, CY = 300, 230
NAVY, CYAN, LIGHT, ACTION, LINE = "#002f65", "#00a6ca", "#4fd1e8", "#00799a", "#d9e2ec"
random.seed(7)
out = []
add = out.append

# feines Punktraster
for x in range(20, W, 28):
    for y in range(20, H, 28):
        add(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{NAVY}" fill-opacity=".09"/>')

# Umlaufbahnen
for r, dash, op in ((120, "2 7", .5), (190, "1 9", .35)):
    add(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{ACTION}" stroke-opacity="{op}" stroke-width="1.5" stroke-dasharray="{dash}" stroke-linecap="round"/>')

# Knoten (Winkel, Radius, Symbol)
nodes = [(-90, 190, "cloud"), (-30, 190, "server"), (30, 190, "shield"),
         (90, 190, "laptop"), (150, 190, "wifi"), (210, 190, "building")]
pos = []
for a, r, kind in nodes:
    t = math.radians(a)
    pos.append((CX + r * math.cos(t) * 1.25, CY + r * math.sin(t) * .95, kind))

# Verbindungen: Mitte -> Knoten und Nachbarn
for x, y, _ in pos:
    add(f'<path d="M{CX} {CY} L{x:.1f} {y:.1f}" stroke="{ACTION}" stroke-opacity=".35" stroke-width="1.5"/>')
for i in range(len(pos)):
    x1, y1, _ = pos[i]; x2, y2, _ = pos[(i + 1) % len(pos)]
    add(f'<path d="M{x1:.1f} {y1:.1f} Q{CX} {CY} {x2:.1f} {y2:.1f}" fill="none" stroke="{LINE}" stroke-width="1.2"/>')

# Datenpunkte auf den Verbindungen
for x, y, _ in pos:
    for f, rr in ((.35, 3), (.62, 2.2)):
        add(f'<circle cx="{CX + (x - CX) * f:.1f}" cy="{CY + (y - CY) * f:.1f}" r="{rr}" fill="{CYAN}"/>')

# verstreute Punkte in Logofarben
for _ in range(26):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(215, 260)
    x, y = CX + r * math.cos(a) * 1.1, CY + r * math.sin(a) * .82
    if 8 < x < W - 8 and 8 < y < H - 8:
        add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.choice((1.8, 2.5, 3.5, 4.5))}" fill="{random.choice((CYAN, LIGHT, NAVY))}" fill-opacity="{random.choice((.35, .55, .8))}"/>')

ICONS = {
    "cloud": '<path d="M-11 6h22a7 7 0 0 0 0-14 10 10 0 0 0-19-2 7 7 0 0 0-3 16z"/>',
    "server": '<rect x="-11" y="-11" width="22" height="9" rx="2"/><rect x="-11" y="2" width="22" height="9" rx="2"/><path d="M-6 -6.5h1M-6 6.5h1"/>',
    "shield": '<path d="M0-12l10 4v7c0 6-4 10-10 13-6-3-10-7-10-13v-7z"/><path d="M-4 0l3 3 5-6"/>',
    "laptop": '<rect x="-10" y="-9" width="20" height="13" rx="1.5"/><path d="M-14 8h28"/>',
    "wifi": '<path d="M-12-3a17 17 0 0 1 24 0M-8 2a11 11 0 0 1 16 0M-4 7a5 5 0 0 1 8 0"/><circle cx="0" cy="11" r="1"/>',
    "building": '<rect x="-9" y="-12" width="18" height="24" rx="1"/><path d="M-4-7h2M2-7h2M-4-2h2M2-2h2M-4 3h2M2 3h2M-2 12v-4h4v4"/>',
}
for x, y, kind in pos:
    add(f'<g transform="translate({x:.1f} {y:.1f})"><circle r="34" fill="{CYAN}" fill-opacity=".12"/>'
        f'<circle r="26" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
        f'<g fill="none" stroke="{NAVY}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[kind]}</g></g>')

# Zentrum: Ansprechpartner/Koordination
add(f'<circle cx="{CX}" cy="{CY}" r="62" fill="{CYAN}" fill-opacity=".14"/>')
add(f'<circle cx="{CX}" cy="{CY}" r="46" fill="{NAVY}"/>')
add(f'<g transform="translate({CX} {CY})" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle r="7" cx="0" cy="-6"/><path d="M-13 15c1-8 6-12 13-12s12 4 13 12"/></g>')
add(f'<circle cx="{CX + 33}" cy="{CY - 33}" r="9" fill="{LIGHT}" stroke="#fff" stroke-width="3"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
       f'aria-label="Illustration: ein Ansprechpartner in der Mitte, verbunden mit Cloud, Server, Sicherheit, Arbeitsplatz, WLAN und Standort">'
       + "".join(out) + "</svg>\n")
target = Path(__file__).resolve().parents[2] / "src/assets/img/it-landschaft.svg"
target.write_text(svg, encoding="utf-8")
print(target, len(svg), "Bytes")
