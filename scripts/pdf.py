# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright", "pypdf", "pillow"]
# ///
"""Produit un PDF complet du cours, dans l'ordre du menu.

Lancer depuis la racine du dépôt :

    uv run scripts/pdf.py                      # écrit ~/Desktop/INF1410.pdf
    uv run scripts/pdf.py --out /chemin/x.pdf

Le principe : on laisse le navigateur faire le rendu, plutôt que de convertir
le Markdown. Le site est construit par Hugo dans un dossier temporaire, servi
localement, et chaque page y est lue. Les articles sont assemblés en un seul
document HTML, avec la feuille de style du site et MathJax, puis Chrome (par
Playwright) l'imprime en un seul PDF : pagination continue, liens internes qui
restent cliquables, maths et coloration du code déjà rendus par le site.

Ce qui est adapté pour le papier :
- les blocs exécutables (js, pyodide, sql) gardent leur code, perdent leurs
  boutons et leur zone de sortie, avec une mention de la version en ligne ;
- les applets (iframes) deviennent un lien vers la page en ligne ;
- les liens entre pages du cours deviennent des liens internes au PDF ;
- les identifiants de titres sont préfixés par page, pour éviter les collisions
  (deux pages ont une « Conclusion ») ;
- les boîtes défilantes (blocs de code) redeviennent coupables entre deux
  pages, sinon Chrome laisse un grand vide devant chaque bloc long ;
- les images de la copie temporaire du site sont réduites à 1400 pixels de
  large (170 points par pouce sur la page) et réencodées, en JPEG pour les
  photos et captures, en PNG pour les dessins à peu de couleurs. Sans cela,
  Chrome embarque chaque PNG à pleine résolution et le PDF dépasse 100 Mo.

La table des matières porte des numéros de page, ce qui demande deux rendus :
le premier pour lire, dans le PDF, la page où tombe chaque cible de la
table (Chrome les écrit comme destinations nommées), le second pour imprimer
les numéros. Les signets du lecteur PDF sont ajoutés
ensuite par pypdf, à partir des mêmes cibles.

Navigateurs : Playwright utilise ceux de ~/Library/Caches/ms-playwright ;
`uv run --with playwright playwright install chromium` s'ils manquent.
"""

import argparse
import datetime
import html
import http.server
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import urllib.parse
from functools import partial
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit

RACINE = Path(__file__).resolve().parent.parent
PREFIXE = "/inf1410-teluq/"
PORT = 8767
TITRE = "INF1410 - Initiation au génie logiciel"
AUTEUR = "Christian Jauvin, Université TÉLUQ"
SITE_EN_LIGNE = "https://cjauvin.github.io/inf1410-teluq/"


# ---------------------------------------------------------------- construction

def construire_site(destination: Path) -> None:
    base = f"http://127.0.0.1:{PORT}{PREFIXE}"
    subprocess.run(
        ["hugo", "--quiet", "--baseURL", base, "--destination", str(destination / PREFIXE.strip("/"))],
        cwd=RACINE, check=True, capture_output=True, text=True,
    )


class _Silencieux(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # noqa: D102
        pass


def servir(dossier: Path) -> http.server.ThreadingHTTPServer:
    handler = partial(_Silencieux, directory=str(dossier))
    serveur = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    return serveur


LARGEUR_MAX = 1200


def reduire_images(site: Path) -> tuple[int, int]:
    """Réduit sur place les images du site temporaire. Renvoie (avant, après) en octets.

    Le fichier garde son nom : Chrome reconnaît le format au contenu, pas à
    l'extension. Les SVG ne sont pas touchés.
    """
    avant = apres = 0
    for f in site.rglob("*"):
        if f.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        avant += f.stat().st_size
        try:
            img = Image.open(f)
            img.load()
        except Exception:
            apres += f.stat().st_size
            continue
        if img.width > LARGEUR_MAX:
            img = img.resize((LARGEUR_MAX, round(img.height * LARGEUR_MAX / img.width)), Image.LANCZOS)
        peu_de_couleurs = img.convert("RGBA").getcolors(256) is not None
        if peu_de_couleurs:
            img.convert("RGBA").quantize(256).save(f, format="PNG", optimize=True)
        else:
            fond = Image.new("RGB", img.size, "white")
            fond.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[3])
            fond.save(f, format="JPEG", quality=82, optimize=True, progressive=True)
        apres += f.stat().st_size
    return avant, apres


# -------------------------------------------------------------------- lecture

def pages_du_menu(site: Path) -> list[tuple[str, str]]:
    """Les pages dans l'ordre du menu latéral, la page d'accueil en tête."""
    accueil = (site / PREFIXE.strip("/") / "index.html").read_text()
    menu = re.search(r'<aside class="book-menu">.*?</aside>', accueil, re.S).group(0)
    liens = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', menu, re.S)
    pages = [(PREFIXE, "Accueil")]
    for href, titre in liens:
        titre = html.unescape(re.sub(r"<[^>]+>", "", titre)).strip()
        pages.append((urllib.parse.unquote(href), titre))
    return pages


def fichier_de(site: Path, chemin: str) -> Path:
    return site / chemin.strip("/") / "index.html"


def article_de(site: Path, chemin: str) -> str:
    s = fichier_de(site, chemin).read_text()
    m = re.search(r'<article class="markdown book-article">(.*?)</article>', s, re.S)
    return m.group(1) if m else ""


# ------------------------------------------------------------- transformation

NOTE_BLOC = (
    '<p class="print-note">Bloc exécutable dans la version en ligne du cours.</p>'
)


def aplatir_blocs(article: str) -> str:
    """Les blocs js/pyodide/sql deviennent des blocs de code ordinaires."""
    motif = re.compile(
        r'<div class="(js|pyodide|sql)-block"[^>]*>\s*'
        r'<textarea[^>]*>(.*?)</textarea>\s*'
        r'<div class="\1-toolbar">.*?</div>\s*'
        r'<(pre|div) class="\1-output[^"]*"[^>]*>.*?</\3>\s*'
        r'</div>',
        re.S,
    )
    langue = {"js": "javascript", "pyodide": "python", "sql": "sql"}

    def remplacer(m):
        code = m.group(2).strip("\n")
        return (
            f'<div class="highlight print-runner"><pre class="chroma"><code class="language-{langue[m.group(1)]}">'
            f"{code}</code></pre></div>{NOTE_BLOC}"
        )

    return motif.sub(remplacer, article)


def remplacer_applets(article: str, url_page: str) -> str:
    motif = re.compile(r'<div class="applet-wrapper"[^>]*>.*?</iframe>\s*</div>', re.S)
    lien = SITE_EN_LIGNE.rstrip("/") + url_page[len(PREFIXE) - 1:]
    note = (
        f'<p class="print-note">Applet interactive, à essayer dans la version en ligne&nbsp;: '
        f'<a href="{lien}">{lien}</a></p>'
    )
    return motif.sub(note, article)


def prefixer_ids(article: str, p: str) -> str:
    article = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{p}-{m.group(1)}"', article)
    article = re.sub(r'\bfor="([^"]+)"', lambda m: f'for="{p}-{m.group(1)}"', article)
    article = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}-{m.group(1)}"', article)
    return article


def relier_pages(article: str, index: dict[str, str]) -> str:
    """Un lien vers une autre page du cours devient un lien interne au PDF."""

    def remplacer(m):
        cible = urllib.parse.unquote(m.group(1))
        chemin, _, frag = cible.partition("#")
        if not chemin.endswith("/"):
            chemin += "/"
        p = index.get(chemin)
        if p is None:
            return m.group(0)
        return f'href="#{p}-{frag}"' if frag else f'href="#{p}"'

    # relref donne un chemin absolu sans hôte, ref donne l'URL complète
    return re.sub(rf'href="(?:http://127\.0\.0\.1:{PORT})?(/inf1410-teluq/[^"]*)"', remplacer, article)


def transformer(article: str, p: str, url_page: str, index: dict[str, str]) -> str:
    article = re.sub(r"<script\b.*?</script>", "", article, flags=re.S)
    article = aplatir_blocs(article)
    article = remplacer_applets(article, url_page)
    article = article.replace(' loading="lazy"', "")
    article = re.sub(r"<details\b(?![^>]*\bopen\b)", "<details open", article)
    article = prefixer_ids(article, p)  # d'abord les ancres locales (href="#x")
    article = relier_pages(article, index)  # puis les liens vers d'autres pages
    return article


def titres_h2(article: str, p: str) -> list[tuple[str, str]]:
    """Les (id préfixé, texte) des titres de niveau 2 d'un article transformé."""
    resultat = []
    for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', article, re.S):
        texte = re.sub(r'<a class="anchor".*?</a>', "", m.group(2), flags=re.S)
        texte = html.unescape(re.sub(r"<[^>]+>", "", texte)).strip()
        resultat.append((m.group(1), texte))
    return resultat


# ------------------------------------------------------------------ assemblage

STYLE = """
html { font-size: 11pt; }
main.container { display: block; }
.book-page { max-width: none; padding: 0; min-height: 0; }
.print-page { break-before: page; }
.print-page:first-of-type { break-before: auto; }
h1, h2, h3, h4 { break-after: avoid; }
a.anchor { display: none; }
.highlight, pre, .book-table, table, .markdown { overflow: visible !important; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; break-inside: auto; }
img, svg, figure, label.book-image { break-inside: avoid; }
label.book-image { display: block; }
label.book-image input { display: none; }
/* Le plafond de taille du site (--largeur-plafond, la largeur à laquelle
   l'image atteint 700 px de haut) n'est appliqué qu'à l'écran. Sur la page,
   700 px feraient 185 mm, presque toute la hauteur : on reprend le plafond à
   la moitié, ce qui garde les diagrammes larges en pleine colonne et ramène
   les portraits et les captures à une taille de figure. */
img { max-width: 100%; max-height: 220mm; height: auto; object-fit: contain; }
label.book-image img { max-width: min(100%, calc(var(--largeur-plafond, 100%) * 0.5)); max-height: 120mm; }
label.book-image { text-align: center; }
figure.wordcloud-wrap svg, figure.modules-wrap svg { max-width: 100%; height: auto; }
.book-hint { break-inside: avoid; }
.print-note { font-size: 0.85em; color: #666; margin-top: -0.6em; }
.print-runner { border-left: 3px solid #999; }

.print-cover { height: 100vh; display: flex; flex-direction: column; justify-content: center; }
.print-cover h1 { font-size: 2.4em; margin: 0 0 .3em; }
.print-cover p { font-size: 1.1em; margin: .2em 0; }
.print-cover .print-cover-note { margin-top: 3em; font-size: .95em; color: #444; }

.print-toc { break-before: page; }
.print-toc ol { list-style: none; padding: 0; margin: 0; }
.print-toc li { display: flex; align-items: baseline; gap: .4em; white-space: nowrap; overflow: hidden; margin: .15em 0; }
.print-toc li a { text-decoration: none; color: inherit; overflow: hidden; text-overflow: ellipsis; }
.print-toc li .print-dots { flex: 1; border-bottom: 1px dotted #999; min-width: 1em; }
.print-toc li .print-num { min-width: 2.5em; text-align: right; }
.print-toc li.niveau-0 { font-weight: 600; margin-top: .6em; }
.print-toc li.niveau-1 { padding-left: 1.2em; }
.print-toc li.niveau-2 { padding-left: 2.4em; }
.print-toc li.section { padding-left: 3.6em; font-size: .92em; color: #444; }
"""


def niveau_de(chemin: str) -> int:
    """0 pour un module ou une page transversale, 1 pour une section, 2 pour une sous-section."""
    parties = [x for x in chemin[len(PREFIXE):].split("/") if x]  # ["docs", "module2", "tests"]
    return max(0, min(len(parties) - 2, 2))


def assembler(site: Path, pages: list[tuple[str, str]], numeros: dict[str, int] | None) -> tuple[str, list[dict]]:
    """Le document complet, et la liste des entrées de la table des matières."""
    index = {chemin: f"p{i}" for i, (chemin, _) in enumerate(pages)}
    css = next((site / PREFIXE.strip("/")).glob("book.min.*.css")).name
    entrees: list[dict] = []
    corps = []
    for i, (chemin, titre) in enumerate(pages):
        p = f"p{i}"
        article = transformer(article_de(site, chemin), p, chemin, index)
        corps.append(f'<section class="print-page" id="{p}"><article class="markdown book-article">{article}</article></section>')
        entrees.append({"id": p, "titre": titre, "niveau": niveau_de(chemin) if i else 0, "section": False})
        for ident, texte in titres_h2(article, p):
            entrees.append({"id": ident, "titre": texte, "niveau": 3, "section": True})

    lignes = []
    for e in entrees:
        num = "" if numeros is None else str(numeros.get(e["id"], ""))
        classe = "section" if e["section"] else f"niveau-{e['niveau']}"
        lignes.append(
            f'<li class="{classe}"><a href="#{e["id"]}">{html.escape(e["titre"])}</a>'
            f'<span class="print-dots"></span><span class="print-num">{num}</span></li>'
        )
    date = datetime.date.today().strftime("%-d %B %Y")
    mois = {"January": "janvier", "February": "février", "March": "mars", "April": "avril", "May": "mai",
            "June": "juin", "July": "juillet", "August": "août", "September": "septembre",
            "October": "octobre", "November": "novembre", "December": "décembre"}
    for en, fr in mois.items():
        date = date.replace(en, fr)

    document = f"""<!doctype html>
<html lang="fr" data-theme="light">
<head>
<meta charset="utf-8">
<title>{html.escape(TITRE)}</title>
<link rel="stylesheet" href="{PREFIXE}{css}">
<link rel="stylesheet" href="{PREFIXE}css/applet.css">
<script>
MathJax = {{
  tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
          processEscapes: true, processEnvironments: true }},
  options: {{ skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'] }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>{STYLE}</style>
</head>
<body class="book-kind-page book-type-docs">
<main class="container flex"><div class="book-page"><div class="markdown book-article">
<section class="print-cover">
  <h1>{html.escape(TITRE)}</h1>
  <p>{html.escape(AUTEUR)}</p>
  <p>Version PDF générée le {date}</p>
  <p class="print-cover-note">La version en ligne, <a href="{SITE_EN_LIGNE}">{SITE_EN_LIGNE}</a>,
  est la référence&nbsp;: elle contient les blocs de code exécutables et les applets interactives,
  que ce document ne peut que montrer. Les liens entre les pages du cours sont conservés ici
  sous forme de liens internes.</p>
</section>
<section class="print-toc"><h1>Table des matières</h1><ol>{''.join(lignes)}</ol></section>
</div>
{''.join(corps)}
</div></main>
</body></html>"""
    return document, entrees


# ----------------------------------------------------------------------- rendu

def imprimer(html_path: Path, pdf_path: Path) -> None:
    url = f"http://127.0.0.1:{PORT}/{html_path.name}"
    with sync_playwright() as p:
        navigateur = p.chromium.launch()
        page = navigateur.new_page(viewport={"width": 1000, "height": 1300})
        page.goto(url, wait_until="networkidle", timeout=180_000)
        page.evaluate("""async () => {
            if (window.MathJax && MathJax.startup) { await MathJax.startup.promise; }
            await document.fonts.ready;
            await Promise.all(Array.from(document.images).map(i => i.complete ? null
                : new Promise(r => { i.onload = i.onerror = r; })));
        }""")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_path), format="Letter", print_background=True,
            margin={"top": "18mm", "bottom": "18mm", "left": "17mm", "right": "17mm"},
            display_header_footer=True,
            header_template=(
                "<div style='font-size:8px;color:#888;width:100%;text-align:right;padding-right:17mm'>"
                f"{html.escape(TITRE)}</div>"
            ),
            footer_template=(
                "<div style='font-size:9px;color:#444;width:100%;text-align:center'>"
                "<span class='pageNumber'></span></div>"
            ),
        )
        navigateur.close()


# --------------------------------------------------------- cibles et signets

def cibles_de_la_table(pdf_path: Path, entrees: list[dict]) -> dict[str, tuple[int, float]]:
    """Pour chaque entrée de la table, (index de page, ordonnée) de sa cible.

    Chrome écrit chaque ancre visée par un lien comme une destination nommée,
    du nom de l'identifiant HTML (encodé en pourcentage s'il est accentué).
    """
    lecteur = PdfReader(str(pdf_path))
    destinations = {}
    for nom, dest in lecteur.named_destinations.items():
        ident = urllib.parse.unquote(nom.lstrip("/"))
        page = lecteur.get_destination_page_number(dest)
        haut = float(dest.top) if dest.top is not None else 0.0
        destinations[ident] = (page, haut)
    manquantes = [e["id"] for e in entrees if e["id"] not in destinations]
    if manquantes:
        raise SystemExit(f"cibles introuvables dans le PDF : {manquantes[:5]}… ({len(manquantes)})")
    return {e["id"]: destinations[e["id"]] for e in entrees}


def ajouter_signets(pdf_in: Path, pdf_out: Path, entrees: list[dict], cibles: dict[str, tuple[int, float]]) -> None:
    lecteur = PdfReader(str(pdf_in))
    ecrivain = PdfWriter()
    ecrivain.append(lecteur)
    parents: dict[int, object] = {}
    for e in entrees:
        page, haut = cibles[e["id"]]
        niveau = 3 if e["section"] else e["niveau"]
        parent = None
        for n in range(niveau - 1, -1, -1):
            if n in parents:
                parent = parents[n]
                break
        item = ecrivain.add_outline_item(e["titre"], page, parent=parent, fit=Fit.xyz(left=0, top=haut, zoom=0))
        parents[niveau] = item
        for n in list(parents):
            if n > niveau:
                del parents[n]
    ecrivain.add_metadata({"/Title": TITRE, "/Author": AUTEUR})
    ecrivain.write(str(pdf_out))


# ------------------------------------------------------------------------ main

def main() -> None:
    ap = argparse.ArgumentParser(description="PDF complet du cours")
    ap.add_argument("--out", type=Path, default=Path.home() / "Desktop" / "INF1410.pdf")
    ap.add_argument("--garder", action="store_true", help="garder le dossier de travail et l'afficher")
    args = ap.parse_args()

    travail = Path(tempfile.mkdtemp(prefix="inf1410-pdf-"))
    try:
        print("construction du site…", flush=True)
        construire_site(travail)
        site = travail
        avant, apres = reduire_images(site)
        print(f"images réduites : {avant / 1e6:.0f} Mo → {apres / 1e6:.0f} Mo", flush=True)
        serveur = servir(travail)
        pages = pages_du_menu(site)
        print(f"{len(pages)} pages, dans l'ordre du menu", flush=True)

        document, entrees = assembler(site, pages, None)
        (travail / "cours.html").write_text(document)
        print("premier rendu (pour les numéros de page)…", flush=True)
        imprimer(travail / "cours.html", travail / "passe1.pdf")
        cibles = cibles_de_la_table(travail / "passe1.pdf", entrees)

        numeros = {k: v[0] + 1 for k, v in cibles.items()}
        document, entrees = assembler(site, pages, numeros)
        (travail / "cours.html").write_text(document)
        print("second rendu (avec les numéros)…", flush=True)
        imprimer(travail / "cours.html", travail / "passe2.pdf")
        cibles2 = cibles_de_la_table(travail / "passe2.pdf", entrees)
        decales = sum(1 for k in cibles if cibles[k][0] != cibles2[k][0])
        if decales:
            print(f"attention : {decales} cibles ont changé de page entre les deux rendus", flush=True)

        ajouter_signets(travail / "passe2.pdf", args.out, entrees, cibles2)
        serveur.shutdown()
        n = len(PdfReader(str(args.out)).pages)
        print(f"écrit {args.out} ({n} pages, {args.out.stat().st_size / 1e6:.1f} Mo)")
    finally:
        if args.garder:
            print(f"dossier de travail gardé : {travail}")
        else:
            shutil.rmtree(travail, ignore_errors=True)


if __name__ == "__main__":
    main()
