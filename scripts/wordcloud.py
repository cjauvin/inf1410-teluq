#!/usr/bin/env python3
"""Génère assets/wordcloud.svg à partir de tout le contenu Markdown du cours.

Usage : python3 scripts/wordcloud.py

Le SVG produit est destiné à être inséré dans la page (shortcode wordcloud),
et non référencé par <img> : inséré, il hérite des couleurs du thème et suit
donc la bascule clair/sombre.
"""
import re, pathlib, collections, math, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
N_MOTS = 75
LARGEUR, HAUTEUR = 1150, 560
TAILLE_MIN, TAILLE_MAX = 11, 72

STOP = set("""
a à ai aie ainsi alors après as au aucun aucune aujourd auquel aussi autant autre autres aux avaient avait avant avec avoir
beaucoup bien bon ça car ce ceci cela celle celles celui cependant certain certaine certaines certains ces cet cette ceux
chacun chaque chez comme comment dans de dedans dehors déjà depuis des dès désormais deux devait devient
doit doivent donc dont du duquel durant elle elles en encore enfin ensuite entre est et étaient était
étant été êtes être eux fait faire fais faisait fallait faut fois font fut hors ici il ils jamais
je jusqu jusque juste la laquelle le lequel les lesquelles lesquels leur leurs lors lorsque lui ma mais me même mêmes
mes mieux moi moins mon ne ni non nos notre nous nul on ont ou où par parce parfois parmi pas peu
peut peuvent plupart plus plusieurs plutôt pour pourquoi pourtant pouvait pouvoir premier première près puis puisque
quand que quel quelle quelles quels quelque quelques qui quoi rien sa sais sait sans se sera serait seront ses
seul seulement si sien soi soit son sont sous souvent suis suit sur ta tandis tant te tel telle telles tels tes
toi ton toujours tous tout toute toutes très trop un une va vais vers veut veux via voici voilà voir vont vos votre
vous avez avons ayant chose choses cas exemple exemples autrement notamment surtout simplement vraiment généralement
partie lieu façon manière moment monde niveau nombre point points type types grand grande
petit petite nouvelle bonne bonnes mauvais mauvaise long longue possible impossible
rendre donner prendre mettre savoir comprendre utiliser permet permettre utilisé utilisée
utilisés utilisées appelle appelée appelé etc deviennent devenir reste restent existe existent
nbsp trois quatre cinq six sept huit neuf dix cent mille afin lorsqu puisqu quelqu aujourd hui
suffit agit trouve trouvent ajoute veulent devra devrait pourra pourrait vient viennent
the for and of to is in with that this it as be on are was not you your from at by an or if we can
section module cours
""".split())

SC_CODE = ("pyodide", "sql", "js", "applet")


def frequences():
    textes = []
    for f in sorted((RACINE / "content").rglob("*.md")):
        p = str(f)
        if "/.venv/" in p or "/requests" in p:
            continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        t = re.sub(r"^---.*?^---", " ", t, flags=re.S | re.M)
        for sc in SC_CODE:  # shortcodes appariés dont le contenu est du code
            t = re.sub(r"\{\{[<%]\s*" + sc + r"\b.*?\{\{[<%]\s*/\s*" + sc + r"\s*[>%]\}\}",
                       " ", t, flags=re.S)
        t = re.sub(r"```.*?```", " ", t, flags=re.S)
        t = re.sub(r"^(?: {4}|\t).*$", " ", t, flags=re.M)
        t = re.sub(r"`[^`]*`", " ", t)
        t = re.sub(r"\{\{[<%].*?[>%]\}\}", " ", t, flags=re.S)
        t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
        t = re.sub(r"&[a-z]+;", " ", t)
        t = re.sub(r"<[^>]+>", " ", t)
        t = re.sub(r"https?://\S+", " ", t)
        t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)
        textes.append(t)

    blob = re.sub(r"[’']", " ", " ".join(textes))
    c = collections.Counter()
    for m in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ-]{2,}", blob):
        w = m.lower().strip("-")
        if len(w) >= 3 and w not in STOP:
            c[w] += 1
    for w in list(c):  # pluriels fusionnés vers le singulier
        if w.endswith("s") and not w.endswith("ss"):
            sg = w[:-1]
            if sg in c and c[sg] >= 3 and sg not in STOP:
                c[sg] += c[w]
                del c[w]
    return c


def disposer(mots):
    """Placement en spirale d'Archimède, du plus gros au plus petit."""
    fmax = mots[0][1]
    places, rects = [], []
    cx, cy = LARGEUR / 2, HAUTEUR / 2
    for i, (mot, n) in enumerate(mots):
        taille = TAILLE_MIN + (TAILLE_MAX - TAILLE_MIN) * (n / fmax) ** 0.8
        w = len(mot) * taille * 0.62  # mesuré : 0.38 à 0.65 selon les lettres
        h = taille * 1.15  # mesuré : 1.14 à 1.23 (ascendantes + jambages)
        pose = None
        pas, angle = 0.0, i * 1.7  # départ décalé pour éviter les alignements
        while pas < 3000:
            r = 2.1 * pas
            x = cx + r * math.cos(angle) - w / 2
            y = cy + r * math.sin(angle) * 0.62 - h / 2
            if x >= 2 and y >= 2 and x + w <= LARGEUR - 2 and y + h <= HAUTEUR - 2:
                boite = (x, y, x + w, y + h)
                if not any(boite[0] < q[2] and boite[2] > q[0] and
                           boite[1] < q[3] and boite[3] > q[1] for q in rects):
                    pose = (x, y, w, h, taille)
                    break
            angle += 0.28
            pas += 0.28 / (2 * math.pi)
        if pose:
            rects.append((pose[0], pose[1], pose[0] + pose[2], pose[1] + pose[3]))
            places.append((mot, n, pose))
    return places


def svg(places):
    fmax = max(n for _, n, _ in places)
    out = [
        f'<svg class="wordcloud" viewBox="0 0 {LARGEUR} {HAUTEUR}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Nuage des mots les plus fréquents du cours">',
        '<title>Les mots du cours</title>',
    ]
    for mot, n, (x, y, w, h, taille) in places:
        # Le poids visuel suit la fréquence : opacité et graisse.
        op = 0.42 + 0.58 * (n / fmax) ** 0.5
        poids = 600 if taille > 34 else 500 if taille > 20 else 400
        out.append(
            f'<text x="{x + w / 2:.1f}" y="{y + h * 0.84:.1f}" font-size="{taille:.1f}" '
            f'font-weight="{poids}" text-anchor="middle" fill="currentColor" '
            f'opacity="{op:.2f}"><title>{mot} ({n})</title>{mot}</text>'
        )
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    c = frequences()
    places = disposer(c.most_common(N_MOTS))
    cible = RACINE / "assets" / "wordcloud.svg"
    cible.write_text(svg(places) + "\n", encoding="utf-8")
    print(f"{len(places)}/{N_MOTS} mots placés → {cible.relative_to(RACINE)}")
    print("top 10 :", ", ".join(m for m, _ in c.most_common(10)))
