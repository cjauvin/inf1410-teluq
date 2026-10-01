# /// script
# requires-python = ">=3.11"
# dependencies = ["beautifulsoup4", "pillow"]
# ///
"""Génère le cours en PDF et en EPUB, à partir de la page /livre/ construite par Hugo.

    uv run scripts/livre/generer.py                  # construit le site (production) puis le livre
    uv run scripts/livre/generer.py --site public    # utilise un site déjà construit (CI)

Le livre suit automatiquement ce qui est en ligne. Les fichiers sont écrits dans
<site>/telechargements/, d'où la page « Télécharger le cours en livre » les offre.

Étapes : la page /livre/ (layouts/livre.html) enchaîne toutes les pages dans
l'ordre du menu ; ce script la nettoie pour pandoc (figures, encadrés,
formules, liens internes, SVG insérés dans la page, blocs de code exécutables,
applets et vidéos remplacées par un renvoi au site), puis pandoc produit l'EPUB directement et le PDF par LuaLaTeX.
"""
import argparse
import datetime
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from PIL import Image

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent.parent
TRAVAIL = RACINE / "build" / "livre"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def construire_site() -> Path:
    site = TRAVAIL / "site"
    shutil.rmtree(site, ignore_errors=True)
    subprocess.run(["hugo", "--environment", "production", "--noBuildLock", "--quiet", "-d", str(site)],
                   cwd=RACINE, check=True)
    return site


def ident(url_page: str) -> str:
    chemin = urllib.parse.unquote(urllib.parse.urlparse(url_page).path)
    return "p-" + (re.sub(r"[^\w]+", "-", chemin).strip("-") or "accueil")


# caractères absents de la police du PDF
CARACTERES = {"✗": "×", "✓": "✔", "▸": "›", "✅": "✔", "🎉": "", "🚨": "", "📂": "", "🤖": ""}
CJK = re.compile(r"[\u2e80-\u9fff\uf900-\ufaff\uff00-\uffef]+")


def remplacer_caracteres(section, soup):
    """Caractères absents des polices du PDF : remplacés (CARACTERES), mis en exposant (ᵉ),
    ou balisés pour une police de repli (chinois, japonais : span.cjk, voir livre.lua)."""
    decoupe = re.compile(r"(ᵉ|[\u2e80-\u9fff\uf900-\ufaff\uff00-\uffef]+)")
    for texte in list(section.find_all(string=True)):
        s = str(texte)
        for a, b in CARACTERES.items():
            s = s.replace(a, b)
        dans_code = texte.find_parent(["pre", "code"]) is not None
        if dans_code or not decoupe.search(s):
            if s != str(texte):
                texte.replace_with(NavigableString(s))
            continue
        for morceau in decoupe.split(s):
            if morceau == "ᵉ":
                x = soup.new_tag("sup")
                x.string = "e"
            elif CJK.fullmatch(morceau):
                x = soup.new_tag("span", attrs={"class": "cjk"})
                x.string = morceau
            else:
                x = NavigableString(morceau)
            texte.insert_before(x)
        texte.extract()


def remplacer_formules(section, soup):
    """Formules MathJax ($…$, \\( … \\), $$ … $$, \\[ … \\]) → span.math, avec la source TeX
    dans data-tex ; le filtre livre.lua en fait des formules pandoc."""
    motif = re.compile(r"\$\$(.+?)\$\$|\\\[(.+?)\\\]|\\\((.+?)\\\)|(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", re.S)
    for texte in list(section.find_all(string=True)):
        if texte.find_parent(["pre", "code", "script", "style"]):
            continue
        s = str(texte)
        if "$" not in s and "\\(" not in s and "\\[" not in s:
            continue
        morceaux, pos = [], 0
        for m in motif.finditer(s):
            morceaux.append(NavigableString(s[pos:m.start()].replace("\\$", "$")))
            inline = m.group(3) is not None or m.group(4) is not None
            tex = next(g for g in m.groups() if g is not None)
            span = soup.new_tag("span", attrs={"class": "math " + ("inline" if inline else "display"), "data-tex": tex.strip()})
            span.string = tex
            morceaux.append(span)
            pos = m.end()
        morceaux.append(NavigableString(s[pos:].replace("\\$", "$")))
        for x in morceaux:
            texte.insert_before(x)
        texte.extract()


COTE_MAX = 1500        # pixels : au-delà, l'image est réduite
POIDS_PNG_MAX = 150_000  # octets : un PNG plus lourd est converti en JPEG


def alleger(site: Path, src: str, conv: Path) -> str:
    """Rend une image matricielle lisible par LaTeX (pas de WebP, AVIF, GIF) et assez
    légère pour que les livres restent sous la limite de 100 Mo de GitHub."""
    ext = src.rsplit(".", 1)[-1].lower()
    if ext not in ("png", "jpg", "jpeg", "webp", "avif", "gif"):
        return src
    fichier = site / src
    im = Image.open(fichier)
    im.seek(0)
    grand = max(im.size) > COTE_MAX
    if ext in ("png", "jpg", "jpeg") and not grand and (ext != "png" or fichier.stat().st_size <= POIDS_PNG_MAX):
        return src
    base = re.sub(r"[^\w]+", "-", src.rsplit(".", 1)[0]).strip("-")
    im = im.convert("RGBA")
    im.thumbnail((COTE_MAX, COTE_MAX))
    fond = Image.new("RGB", im.size, "white")       # la transparence devient du blanc
    fond.paste(im, mask=im.getchannel("A"))
    fond.save(conv / f"{base}.jpg", quality=85, optimize=True)
    return f"conv/{base}.jpg"


def preparer(html: str, site: Path, conv: Path) -> tuple[str, str]:
    # SVG insérés dans la page (illustration, modules, wordcloud) → fichiers, pour pandoc.
    # Fait sur le texte brut : l'analyseur HTML mettrait viewBox et les balises SVG en minuscules.
    def extraire_svg(m):
        compteur_svg[0] += 1
        source = re.sub(r"var\(--[\w-]+,\s*([^)]+)\)", r"\1", m.group(0)).replace("currentColor", "#222222")
        if not re.search(r"<svg[^>]*\sxmlns=", source):
            source = source.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        (conv / f"svg-{compteur_svg[0]}.svg").write_text(source, encoding="utf-8")
        return f'<img src="conv/svg-{compteur_svg[0]}.svg" alt="">'

    compteur_svg = [0]
    html = re.sub(r"<svg\b.*?</svg>", extraire_svg, html, flags=re.S)
    soup = BeautifulSoup(html, "html.parser")
    corps = soup.body
    base = corps["data-base"]                      # https://…/inf1901-teluq-v2/
    rel = corps["data-rel"]                        # /inf1901-teluq-v2/
    origine = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(base))
    sections = corps.find_all("section", class_="page")
    pages = {urllib.parse.unquote(s["data-url"]): ident(s["data-url"]) for s in sections}
    couverture = None

    for tag in corps.find_all(["script", "style", "input"]):
        tag.decompose()
    for a in corps.find_all("a", class_="anchor"):
        a.decompose()

    for sec in sections:
        pid = ident(sec["data-url"])
        url_page = origine + sec["data-url"]
        titre = sec["data-titre"]

        # identifiants préfixés par la page, pour qu'ils restent uniques dans le livre
        for el in sec.find_all(id=True):
            el["id"] = f"{pid}--{el['id']}"
        h1 = sec.find("h1")
        if h1 is None:
            h1 = soup.new_tag("h1")
            h1.string = titre
            sec.insert(0, h1)
        h1["id"] = pid
        sec.insert(0, h1.extract())                # le titre avant tout (images d'ouverture)
        if sec["data-type"] == "module":
            h1["class"] = "partie"

        # blocs de code exécutables (pyodide, js, sql) → code, avec un renvoi au site
        for classe, langage in (("pyodide-block", "python"), ("js-block", "javascript"), ("sql-block", "sql")):
            for bloc in sec.find_all("div", class_=classe):
                zone = bloc.find("textarea")
                pre = soup.new_tag("pre")
                code = soup.new_tag("code", attrs={"class": f"language-{langage}"})
                code.string = zone.get_text() if zone else ""
                pre.append(code)
                note = soup.new_tag("p", attrs={"class": "renvoi-en-ligne"})
                em = soup.new_tag("em")
                em.append("Ce code peut être exécuté et modifié en ligne, sur la page « ")
                a = soup.new_tag("a", href=url_page)
                a.string = titre
                em.append(a)
                em.append(" » du site du cours.")
                note.append(em)
                bloc.replace_with(pre)
                pre.insert_after(note)

        # images du shortcode (case à cocher d'agrandissement) → figure avec légende
        for label in sec.find_all("label", class_="book-image"):
            img = label.find("img")
            if label.parent.name == "figure":          # illustration : la figure et sa légende existent déjà
                label.replace_with(img.extract())
                continue
            legende = img.get("title")
            if not legende:                            # sans légende : une image centrée, pas une figure
                label.replace_with(img.extract())
                continue
            fig = soup.new_tag("figure")
            for attr in ("title", "loading", "style", "width", "height"):
                img.attrs.pop(attr, None)
            fig.append(img.extract())
            if legende:
                cap = soup.new_tag("figcaption")
                cap.string = legende
                fig.append(cap)
            label.replace_with(fig)
        for img in sec.find_all("img"):
            for attr in ("loading", "style", "width", "height"):
                img.attrs.pop(attr, None)
            if img["src"].startswith("conv/"):       # SVG extrait plus haut
                continue
            if "logo-mono" in (img.get("class") or []):
                img["width"] = "35%"
            src = urllib.parse.unquote(img["src"])
            if src.startswith(rel):
                src = src[len(rel):]
            src = src.lstrip("/")
            img["src"] = alleger(site, src, conv)

        if sec["data-type"] == "accueil" and couverture is None:
            img = sec.find("img")                  # l'image d'accueil sert de couverture
            if img is not None:
                couverture = img["src"]
                (img.find_parent("figure") or img.find_parent("p") or img).decompose()

        # image seule dans son paragraphe (sans légende) → centrée
        for img in sec.find_all("img"):
            p = img.parent
            if p.name == "p" and not p.get_text(strip=True) and len(p.find_all(True)) == 1:
                p.wrap(soup.new_tag("div", attrs={"class": "image-seule"}))
            elif p.name not in ("p", "figure", "a", "td", "th", "li", "span", "em", "strong"):
                bloc = soup.new_tag("div", attrs={"class": "image-seule"})
                img.wrap(bloc)
                img.wrap(soup.new_tag("p"))

        # crédits photo
        for p in sec.find_all("p", class_="image-credit"):
            div = soup.new_tag("div", attrs={"class": "credit"})
            p.wrap(div)

        # encadrés (hint) et blocs repliables (details) → div.encadre
        for bq in sec.find_all("blockquote", class_="book-hint"):
            bq.name = "div"
            bq.attrs = {"class": "encadre"}
        for det in sec.find_all("details"):
            resume = det.find("summary")
            det.name = "div"
            det.attrs = {"class": "encadre"}
            if resume:
                p = soup.new_tag("p")
                b = soup.new_tag("strong")
                b.string = resume.get_text(" ", strip=True)
                p.append(b)
                resume.replace_with(p)

        # applets et vidéos : un renvoi au site
        for w in sec.find_all("div", class_="applet-wrapper"):
            p = soup.new_tag("p", attrs={"class": "renvoi-en-ligne"})
            em = soup.new_tag("em")
            em.append("Applet interactive : à utiliser en ligne, sur la page « ")
            a = soup.new_tag("a", href=url_page)
            a.string = titre
            em.append(a)
            em.append(" » du site du cours.")
            p.append(em)
            w.replace_with(p)
        for fr in sec.find_all("iframe"):
            src = fr.get("src", "")
            m = re.search(r"youtube(?:-nocookie)?\.com/embed/([\w-]+)", src)
            lien = f"https://www.youtube.com/watch?v={m.group(1)}" if m and m.group(1) != "videoseries" else src
            m2 = re.search(r"list=([\w-]+)", src)
            if m2:
                lien = f"https://www.youtube.com/playlist?list={m2.group(1)}"
            p = soup.new_tag("p", attrs={"class": "renvoi-en-ligne"})
            em = soup.new_tag("em")
            em.append("Vidéo : " if "youtube" in lien else "Contenu interactif, à consulter en ligne : ")
            a = soup.new_tag("a", href=lien)
            a.string = lien
            em.append(a)
            p.append(em)
            conteneur = fr
            while conteneur.parent is not sec and conteneur.parent.name == "div" and len(conteneur.parent.find_all(True)) <= 2:
                conteneur = conteneur.parent
            conteneur.replace_with(p)

        remplacer_formules(sec, soup)
        remplacer_caracteres(sec, soup)

        # liens : vers une page du livre → lien interne ; sinon adresse complète du site
        for a in sec.find_all("a", href=True):
            href = a["href"]
            if href.startswith(("mailto:", "http://", "https://")) and not href.startswith(origine):
                continue
            complet = urllib.parse.urljoin(url_page, href)
            u = urllib.parse.urlparse(complet)
            chemin = urllib.parse.unquote(u.path)
            if not chemin.endswith("/") and "." not in chemin.rsplit("/", 1)[-1]:
                chemin += "/"
            if u.netloc == urllib.parse.urlparse(origine).netloc and chemin in pages:
                cible = pages[chemin]
                if u.fragment:
                    frag = f"{cible}--{urllib.parse.unquote(u.fragment)}"
                    cible = frag if corps.find(id=frag) else cible
                a["href"] = "#" + cible
            else:
                a["href"] = urllib.parse.urljoin(base, href) if not href.startswith("http") else href

        sec.name = "div"
        sec.attrs = {"class": "page-du-livre"}
    return str(corps), base, couverture


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", type=Path, help="site Hugo déjà construit (sinon : construction de production)")
    args = ap.parse_args()
    site = (args.site.resolve() if args.site else construire_site())
    TRAVAIL.mkdir(parents=True, exist_ok=True)
    conv = TRAVAIL / "conv"
    conv.mkdir(exist_ok=True)

    corps, base, couverture = preparer((site / "livre" / "index.html").read_text(encoding="utf-8"), site, conv)
    aujourdhui = datetime.date.today()
    date = f"{aujourdhui.day} {MOIS[aujourdhui.month - 1]} {aujourdhui.year}"
    source = TRAVAIL / "livre.html"
    source.write_text(f"<!DOCTYPE html><html lang=\"fr\"><head><meta charset=\"utf-8\"></head>{corps}</html>",
                      encoding="utf-8")

    couverture = TRAVAIL / couverture if couverture.startswith("conv/") else site / couverture
    entete = TRAVAIL / "entete.tex"
    # police de repli pour le chinois et le japonais : la première trouvée sur la machine
    candidates = [Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
                  Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
                  Path("/System/Library/Fonts/PingFang.ttc")]
    cjk = next((c for c in candidates if c.exists()), None)
    police_cjk = (f"\\newfontfamily\\policecjk{{{cjk.name}}}[Path={cjk.parent}/]" if cjk
                  else "\\newcommand{\\policecjk}{}")
    entete.write_text(f"\\newcommand{{\\couverture}}{{{couverture}}}\n"
                      + (ICI / "entete.tex").read_text(encoding="utf-8") + police_cjk + "\n",
                      encoding="utf-8")

    nom = re.search(r'^fichier:\s*"?([^"\n]+)"?\s*$', (ICI / "metadonnees.yaml").read_text(encoding="utf-8"), re.M).group(1)
    sortie = site / "telechargements"
    sortie.mkdir(exist_ok=True)
    commun = ["pandoc", str(source), "-f", "html", "--resource-path", f"{site}:{TRAVAIL}",
              "--metadata-file", str(ICI / "metadonnees.yaml"),
              "-M", f"date=Version générée le {date}",
              "-M", f"site={base}",
              "--lua-filter", str(ICI / "livre.lua"), "--toc", "--toc-depth=2"]
    subprocess.run(commun + ["-t", "epub3", "--mathml", "--split-level=1",
                             "--css", str(ICI / "epub.css"),
                             "--epub-cover-image", str(couverture),
                             "-o", str(sortie / f"{nom}.epub")], check=True)
    subprocess.run(commun + ["--pdf-engine=lualatex", "--top-level-division=chapter",
                             "-H", str(entete),
                             "-o", str(sortie / f"{nom}.pdf")], check=True)
    if not args.site:
        # en local : copie dans static/ (ignoré par git), pour que le serveur Hugo
        # serve les livres et que les liens de la page de téléchargement fonctionnent
        local = RACINE / "static" / "telechargements"
        local.mkdir(exist_ok=True)
        for f in sortie.iterdir():
            shutil.copy2(f, local / f.name)
        sortie = local
    for f in sorted(sortie.iterdir()):
        print(f"{f}  ({f.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    sys.exit(main())
