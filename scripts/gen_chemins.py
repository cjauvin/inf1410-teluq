# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright"]
# ///
"""Travaux notés, « Le projet fil rouge » : chacun trace son chemin dans le cours.

Le paysage touffu des six modules, de gauche à droite, avec quatre chemins de
couleurs différentes. Ils partent du même point et arrivent au même sommet, et
passent tous par les quatre jalons, les « passages obligés ». Entre deux jalons,
chacun va où son projet le mène : l'un traverse une région en profondeur,
l'autre la longe, et le violet fait un détour par le module 4 avant le jalon 1,
comme ce jalon le demande.

Le dessin est écrit en SVG, puis rendu en PNG par Chrome (Playwright), parce
que le shortcode image ne connaît pas les dimensions d'un SVG.

    uv run scripts/gen_chemins.py
"""
import math
import random
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent.parent / "content" / "docs" / "travaux-notés"
PNG = DOSSIER / "chemins.png"

W, H = 960, 520
Y0 = 30  # le haut du dessin est vide : on le retranche du cadre
FOND = "#fbfaf5"
ENCRE, ENCRE_PALE = "#3a3531", "#6b625a"
REGIONS = ["#dfeccb", "#e8efc6", "#d4e8c8", "#e6ebc0", "#d8e9cf", "#e3ecc4"]
BORD_REGION = "#b9cf9e"
SAPIN, SAPIN_FONCE, FEUILLU, FEUILLU_FONCE, TRONC = "#4f8a4a", "#3d7039", "#7aad55", "#5f9142", "#8a6a4a"
ROUGE, BLEU, ORANGE, VIOLET = "#c8352e", "#2f6fb0", "#e08a24", "#7b4fa6"

random.seed(1410)

MODULES = [
    ("Module 1", "Le génie logiciel"),
    ("Module 2", "Le programme"),
    ("Module 3", "Le système"),
    ("Module 4", "L'équipe"),
    ("Module 5", "La production"),
    ("Module 6", "L'écosystème"),
]
# Centres des régions, de gauche à droite, légèrement décalés en hauteur.
CENTRES = [(140, 285), (275, 300), (420, 280), (565, 295), (705, 285), (835, 300)]
RAYONS = [(82, 175), (78, 185), (84, 178), (80, 182), (78, 176), (74, 170)]

DEPART = (52, 300)
JALONS = [(345, 296), (492, 290), (636, 296), (912, 168)]  # le jalon 4 est au sommet


def catmull(points, ferme=False, tension=0.5):
    """Courbe lisse qui passe par chaque point (Catmull-Rom convertie en Bézier)."""
    pts = list(points)
    n = len(pts)
    if ferme:
        etendu = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        etendu = [pts[0]] + pts + [pts[-1]]
    d = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
    segments = n if ferme else n - 1
    for i in range(segments):
        p0, p1, p2, p3 = etendu[i], etendu[i + 1], etendu[i + 2], etendu[i + 3]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    if ferme:
        d.append("Z")
    return " ".join(d)


def tache(cx, cy, rx, ry, n=14):
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        r = 1 + random.uniform(-0.12, 0.10)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return catmull(pts, ferme=True)


o = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<svg viewBox="0 {Y0} {W} {H - Y0}" width="{W}" height="{H - Y0}" xmlns="http://www.w3.org/2000/svg" role="img" '
    'font-family="system-ui, -apple-system, \'Segoe UI\', sans-serif">',
    "<title>Chacun son chemin dans le cours</title>",
    "<desc>Un paysage boisé et touffu, divisé en six régions, une par module du cours, de gauche à droite. "
    "Quatre chemins de couleurs différentes, rouge, bleu, orange et violet, partent du même point à gauche et "
    "arrivent au même sommet, marqué d'un drapeau, à droite. Ils passent tous par les mêmes quatre cercles, les "
    "jalons, mais entre deux jalons ils se séparent : l'un traverse une région en profondeur, un autre la longe "
    "par le bord. Le chemin violet fait un détour par la région du module 4 avant de revenir au jalon 1.</desc>",
    f'<clipPath id="cadre"><rect x="0" y="{Y0}" width="{W}" height="{H - Y0}" rx="14"/></clipPath>',
    f'<rect x="0" y="{Y0}" width="{W}" height="{H - Y0}" rx="14" fill="{FOND}"/>',
    '<g clip-path="url(#cadre)">',
]

# Les six régions.
for (cx, cy), (rx, ry), coul in zip(CENTRES, RAYONS, REGIONS):
    o.append(f'<path d="{tache(cx, cy, rx, ry)}" fill="{coul}" stroke="{BORD_REGION}" stroke-width="1.2"/>')

# La montagne du sommet, par-dessus le bord droit du module 6, qui s'efface vers le bas.
o.append('<defs><linearGradient id="fondu" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0.45" stop-color="#ffffff" stop-opacity="1"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>'
         '</linearGradient><mask id="efface"><rect x="760" y="150" width="220" height="300" fill="url(#fondu)"/></mask></defs>')
o.append('<g mask="url(#efface)">')
o.append('<path d="M835,450 L912,160 L975,300 L975,450 Z" fill="#a9bccf"/>')
o.append('<path d="M900,450 L942,255 L975,300 L975,450 Z" fill="#c2d0dd"/>')
o.append('</g>')
o.append('<path d="M912,160 L899,198 L909,190 L918,203 L926,183 Z" fill="#ffffff"/>')

# Une forêt dense, dessinée de haut en bas pour que les arbres proches cachent les lointains.
arbres = []
for (cx, cy), (rx, ry) in zip(CENTRES, RAYONS):
    for _ in range(70):
        while True:
            x, y = random.uniform(-1, 1), random.uniform(-1, 1)
            if x * x + y * y < 0.78:
                break
        arbres.append((cx + x * rx, cy + y * ry, random.random() < 0.55, random.uniform(0.75, 1.2)))
arbres.sort(key=lambda a: a[1])
for x, y, sapin, t in arbres:
    if sapin:
        h, l = 17 * t, 7 * t
        o.append(f'<path d="M{x:.1f},{y - h:.1f} L{x + l:.1f},{y:.1f} L{x - l:.1f},{y:.1f} Z" '
                 f'fill="{random.choice((SAPIN, SAPIN_FONCE))}"/>')
    else:
        o.append(f'<rect x="{x - 1:.1f}" y="{y - 4 * t:.1f}" width="2" height="{5 * t:.1f}" fill="{TRONC}"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y - 8 * t:.1f}" r="{6 * t:.1f}" '
                 f'fill="{random.choice((FEUILLU, FEUILLU_FONCE))}"/>')

# Le village de départ.
for dx, dy, s in ((-18, 8, 1.0), (-4, 18, 0.85), (-24, 26, 0.8)):
    x, y = DEPART[0] + dx, DEPART[1] + dy
    o.append(f'<rect x="{x - 7 * s:.1f}" y="{y - 9 * s:.1f}" width="{14 * s:.1f}" height="{10 * s:.1f}" fill="#e9dcc6" stroke="#9b8466"/>')
    o.append(f'<path d="M{x - 9 * s:.1f},{y - 9 * s:.1f} L{x:.1f},{y - 17 * s:.1f} L{x + 9 * s:.1f},{y - 9 * s:.1f} Z" fill="#b5523b"/>')

# Les quatre chemins : départ, points de passage, jalons, sommet.
J1, J2, J3, J4 = JALONS
CHEMINS = [
    (ROUGE, [DEPART, (110, 230), (190, 190), (270, 260), J1, (420, 200), J2, (520, 380), (600, 360), J3,
             (700, 240), (790, 200), (860, 200), J4]),
    (BLEU, [DEPART, (130, 360), (230, 410), (300, 340), J1, (400, 330), (450, 400), J2, (560, 240), J3,
            (690, 380), (780, 420), (850, 330), J4]),
    (ORANGE, [DEPART, (150, 300), (240, 230), J1, (390, 420), (470, 360), J2, (540, 190), (610, 210), J3,
              (700, 300), (760, 250), (820, 150), J4]),
    (VIOLET, [DEPART, (120, 160), (300, 140), (480, 150), (570, 200), (520, 250), (410, 330), J1, (440, 250), J2,
              (590, 410), J3, (720, 170), (840, 260), J4]),
]
for coul, pts in CHEMINS:
    d = catmull(pts)
    o.append(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>')
    o.append(f'<path d="{d}" fill="none" stroke="{coul}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')

# Les jalons, les passages obligés.
for i, (x, y) in enumerate(JALONS, 1):
    o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#ffffff" stroke="{ENCRE}" stroke-width="3"/>')
    dy = -18 if i == 4 else 30
    fond = f'<rect x="{x - 34}" y="{y + dy - 16}" width="68" height="22" rx="11" fill="#ffffff" fill-opacity="0.92" stroke="#cfc6b8"/>'
    o.append(fond)
    o.append(f'<text x="{x}" y="{y + dy}" font-size="14.5" font-weight="700" fill="{ENCRE}" text-anchor="middle">Jalon {i}</text>')

# Le départ et le drapeau.
o.append(f'<circle cx="{DEPART[0]}" cy="{DEPART[1]}" r="7" fill="{ENCRE}"/>')
o.append(f'<rect x="{DEPART[0] - 40}" y="{DEPART[1] + 38}" width="88" height="24" rx="12" fill="#ffffff" fill-opacity="0.92" stroke="#cfc6b8"/>')
o.append(f'<text x="{DEPART[0] + 2}" y="{DEPART[1] + 55}" font-size="14.5" font-weight="700" fill="{ENCRE}" text-anchor="middle">Votre idée</text>')
fx, fy = J4[0], J4[1] - 30
o.append(f'<line x1="{fx}" y1="{fy}" x2="{fx}" y2="{fy - 34}" stroke="{ENCRE}" stroke-width="2"/>')
o.append(f'<path d="M{fx},{fy - 34} L{fx + 22},{fy - 27} L{fx},{fy - 20} Z" fill="{ROUGE}"/>')

# Les noms des modules, au-dessus de leur région.
for (titre, sous), (cx, _), (_, _) in zip(MODULES, CENTRES, RAYONS):
    o.append(f'<text x="{cx}" y="60" font-size="17" font-weight="700" fill="{ENCRE}" text-anchor="middle">{titre}</text>')
    o.append(f'<text x="{cx}" y="80" font-size="14.5" fill="{ENCRE_PALE}" text-anchor="middle" font-style="italic">{sous}</text>')

o.append("</g></svg>")
svg = "\n".join(o)

from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as p:
    try:
        nav = p.chromium.launch(channel="chrome")
    except Exception:
        nav = p.chromium.launch()
    page = nav.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
    page.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
    page.locator("svg").screenshot(path=str(PNG), omit_background=True)
    nav.close()
print(PNG)
