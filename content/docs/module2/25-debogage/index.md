---
title: "Le débogage"
slug: "debogage"
weight: 25
---

# Le débogage

Un test rouge dit qu'une chose est fausse. Il ne dit pas pourquoi. Entre les
deux, il y a une activité que tout programmeur pratique des heures par
semaine et que presque aucun cours n'enseigne, comme si elle allait de soi&nbsp;:
le **débogage**, chercher la cause d'un comportement qu'on n'a pas voulu. Cette
section la prend au sérieux. Elle commence par l'outil que tout le monde
utilise sans l'avouer, le `print`, continue avec celui que tout le monde
connaît de nom et utilise trop peu, le **débogueur** (*debugger*), et finit
dans l'éditeur, où le second est devenu si facile qu'il n'y a plus d'excuse.

## Le bogue a d'abord été un insecte

Le mot est plus vieux que l'informatique. Le musée d'histoire américaine de
la Smithsonian rappelle que les ingénieurs parlent de *bugs* pour les petits
défauts d'une machine depuis plus d'un siècle, et que Thomas Edison en
signalait déjà dans ses circuits électriques dans les années 1870. L'histoire
qu'on raconte partout est plus tardive et, pour une fois, elle est vraie&nbsp;: le
9 septembre 1947, l'équipe du calculateur Mark II, à Harvard, trouve une mite
coincée dans un relais, la scotche dans le journal de bord et écrit dessous « first actual
case of bug being found », premier cas réel de bogue trouvé. Le notebook est
conservé au musée, mite comprise. Grace Hopper faisait partie de l'équipe, ce
qui lui vaut souvent la paternité de l'anecdote&nbsp;; le musée précise que le
notebook n'était probablement pas le sien, mais que son équipe et elle ont
répandu les mots *bug* et *debug* chez les programmeurs. Le vocabulaire est
resté, et il dit quelque chose de juste&nbsp;: un bogue n'est pas une faute
morale, c'est un corps étranger dans une machine, et on le cherche comme on
cherche un corps étranger, en ouvrant la machine et en regardant dedans.

{{< image src="mite-1947.webp" alt="La page du journal de bord du Mark II, le 9 septembre 1947 : des heures et des notes manuscrites, et, collée au ruban adhésif au milieu de la page, une mite, avec la mention manuscrite First actual case of bug being found" title="Le journal de bord du Mark II, 9 septembre 1947. Photo : U.S. Naval Historical Center, NH 96566-KN, domaine public, via Wikimedia Commons" loading="lazy" >}}

## Le print, ou l'aveu de tout le monde

Commençons par ce que vous faites déjà. Voici la fonction `est_palindrome`
de la section sur les tests, et deux phrases célèbres pour l'essayer. La
seconde devrait passer, et elle ne passe pas.

{{< pyodide >}}
def est_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(est_palindrome("Engage le jeu que je le gagne"))
print(est_palindrome("Ésope reste ici et se repose"))
{{< /pyodide >}}

Le réflexe universel est d'ajouter une ligne pour voir ce que la fonction
compare vraiment, juste avant le `return`&nbsp;:

{{< pyodide >}}
def est_palindrome(s):
    s = s.lower().replace(" ", "")
    print(f"comparé : {s!r} et {s[::-1]!r}")
    return s == s[::-1]

print(est_palindrome("Ésope reste ici et se repose"))
{{< /pyodide >}}

Et le bogue saute aux yeux&nbsp;: la chaîne commence par `é` et finit par `e`.
L'accent de la majuscule survit à `lower()`, et la phrase n'est un palindrome
qu'à condition d'ignorer les accents, ce que la fonction ne fait pas. Ce que
le `print` a fait ici est exactement ce qu'un bogue demande&nbsp;: montrer la
valeur d'une variable à un moment précis de l'exécution, à l'intérieur de la
fonction, là où le test ne voit qu'un `False`. C'est une sonde, et elle est
d'une efficacité redoutable. En 1979, dans le manuel du système Unix, Brian
Kernighan présentait le débogueur de l'époque, `adb`, comme « utile pour
fouiller les cadavres des programmes C, mais plutôt difficile à apprendre à
utiliser efficacement », et concluait par une phrase que près de cinquante ans de
progrès des outils n'ont pas démentie&nbsp;: « L'outil de débogage le plus efficace
reste la réflexion attentive, accompagnée de quelques `print` judicieusement
placés. » Il n'y a donc aucune honte à en mettre. Il y a seulement leurs
limites, et elles tiennent en trois mots. Il faut *deviner* où regarder, et
un bogue est précisément ce qu'on n'a pas su prévoir. Il faut *relancer* le
programme à chaque nouvelle question, et certains bogues ne se reproduisent
pas à volonté. Et il faut *retirer* les sondes ensuite, sans en oublier une
dans le code livré. Le débogueur répond à ces trois limites d'un coup&nbsp;: c'est
un `print` qu'on n'écrit pas, qu'on pose après coup sur n'importe quelle
ligne, et qui montre toutes les variables à la fois.

## Arrêter le temps

Un débogueur est un programme qui exécute le vôtre en gardant la main dessus.
Il peut l'arrêter à une ligne que vous désignez, un **point d'arrêt**
(*breakpoint*), et, pendant l'arrêt, tout est visible&nbsp;: la valeur de chaque
variable, la ligne exacte où l'on est, et la **pile d'appels** (*call stack*),
c'est-à-dire la suite des fonctions qui ont mené jusqu'ici, chacune avec ses
propres variables. Puis vous décidez de la suite, et c'est le **pas à pas**&nbsp;:
exécuter la ligne courante et s'arrêter à la suivante, entrer dans la fonction
qu'elle appelle pour la suivre de l'intérieur, ou reprendre la course jusqu'au
prochain point d'arrêt. Python en a un dans sa bibliothèque standard depuis
toujours, `pdb`, que sa documentation décrit comme « un débogueur interactif de
code source », avec des « points d'arrêt, conditionnels au besoin, le pas à pas
ligne par ligne, et l'inspection des cadres de la pile ». Depuis Python 3.7, on
l'appelle d'un seul mot, `breakpoint()`, une fonction native proposée par Barry
Warsaw en 2017 qui « entre dans un débogueur à l'endroit de l'appel ». Posez-la
dans `est_palindrome`, à la place du `print` de tout à l'heure, et lancez le
fichier au terminal&nbsp;: le programme s'arrête, et une invite `(Pdb)` attend vos
questions.

```shell
$ uv run python palindrome.py
> palindrome.py(3)est_palindrome()
-> breakpoint()
(Pdb) p s
'ésoperesteicietserepose'
(Pdb) p s[::-1]
'esoperesteicietsereposé'
(Pdb) p s[0], s[-1]
('é', 'e')
(Pdb) c
False
```

Comparez avec le `print`. Le même renseignement est là, mais vous n'avez pas
eu à deviner d'avance qu'il faudrait regarder `s`&nbsp;: la troisième question,
comparer le premier et le dernier caractère, est venue en lisant la réponse à
la deuxième, sans relancer quoi que ce soit. `c` reprend l'exécution, `n`
avance d'une ligne, `s` entre dans la fonction appelée, et la documentation
tient la distinction en une phrase, « `step` s'arrête à l'intérieur d'une
fonction appelée, alors que `next` exécute les fonctions appelées » d'un
trait. Un point d'arrêt peut aussi être **conditionnel**, ne s'arrêter que si
une expression est vraie, ou qu'au centième passage, ce qui est la réponse au
bogue qui ne se produit que sur le millième élément d'une liste. Et un
débogueur sait faire l'autopsie, s'ouvrir sur un programme qui vient de
planter, la pile encore en place, ce que `pdb` appelle le mode
*post-mortem*. Rien de tout cela n'est neuf. Le débogueur de référence du
monde C et Unix, GDB, dont Richard Stallman a écrit la première version pour
le projet GNU, offrait déjà tout ce vocabulaire, et c'est lui qui l'a fixé
pour tous les autres.

## Le débogueur est une boucle interactive (REPL) arrêtée

Regardez de nouveau l'invite `(Pdb)`. Elle vous a laissé taper une expression,
`s[0], s[-1]`, l'a évaluée et a affiché le résultat, puis a attendu la
suivante. C'est exactement la boucle interactive de la page des
[environnements]({{< relref "/docs/environnements" >}}), le `>>>` de Python,
à une différence près, qui fait tout&nbsp;: elle est arrêtée à une ligne précise
d'un programme en cours, et ses variables sont celles du programme à cet
instant. Un débogueur est un REPL avec un contexte.

Cela explique un nom qu'on rencontre vite en cherchant de la documentation
sur `pdb`, celui d'`ipdb`. Puisque le débogueur est une boucle interactive,
on peut lui donner la meilleure des boucles interactives, et c'est ce que
fait `ipdb`, le même `pdb` avec le confort d'IPython, la complétion, la
coloration, les meilleures traces, « avec la même interface que le module
`pdb` », dit son README, donc les mêmes commandes. On n'a même pas à modifier le code pour l'utiliser&nbsp;: la
fonction `breakpoint()` consulte d'abord la variable d'environnement
`PYTHONBREAKPOINT`, qui nomme le débogueur à lancer, et `0` la neutralise, ce
qui permet de laisser un `breakpoint()` oublié sans qu'il arrête plus rien.
C'était le but de Warsaw, changer de débogueur sans toucher au programme.

```shell
$ PYTHONBREAKPOINT=ipdb.set_trace uv run --with ipdb python palindrome.py
> palindrome.py(3)est_palindrome()
      2     s = s.lower().replace(" ", "")
----> 3     breakpoint()
      4     return s == s[::-1]
ipdb> p s[0], s[-1]
('é', 'e')
ipdb> c
False

$ PYTHONBREAKPOINT=0 uv run python palindrome.py
False
```

La même idée, prise par l'autre bout, éclaire le notebook Jupyter de la page
des [environnements]({{< relref "/docs/environnements" >}}). Si un débogueur
est une boucle interactive arrêtée dans un programme, un notebook est une
boucle interactive qui n'oublie rien&nbsp;: un programme découpé en cellules
qu'on exécute une à une, l'état restant vivant entre deux, autrement dit un
point d'arrêt permanent, dans lequel on peut écrire. C'est ce
qui le rend irremplaçable pour explorer des données, et c'est aussi son piège,
qui est un piège de débogage&nbsp;: l'état survit aux cellules, on les exécute
dans le désordre, on en modifie une sans relancer les autres, et l'on obtient
des résultats que personne ne saura reproduire, pas même soi le lendemain. La
règle de survie tient en un geste, relancer le notebook de zéro avant de
croire un résultat. Ce qui a changé depuis Kernighan, c'est le prix
d'entrée&nbsp;: il trouvait `adb` difficile à apprendre, et il avait raison. Dans
l'éditeur, tout ce que la session `(Pdb)` a demandé en quatre commandes se
voit sans en taper une seule.

## Dans VS Code

Le bogue de l'encart des tests tenait dans la ligne même où le test échouait.
Ce n'est pas le cas général. Voici un module plus réaliste, à ajouter au
projet d'exemple des tests, qui calcule une facture avec les taxes
québécoises&nbsp;: la TPS à 5 % et la TVQ à 9,975 %, que Revenu Québec demande
d'appliquer toutes deux au prix de vente. Cinq fonctions qui s'appellent en
chaîne, une boucle, et un bogue quelque part.

```python
# facture.py
TPS = 0.05
TVQ = 0.09975

RABAIS = {"ETUDIANT": 0.10, "FIDELE": 0.05}


def prix_ligne(ligne):
    """Prix d'une ligne de facture : quantité fois prix unitaire."""
    return ligne["quantite"] * ligne["prix"]


def sous_total(lignes):
    total = 0.0
    for ligne in lignes:
        total += prix_ligne(ligne)
    return total


def appliquer_rabais(montant, code):
    if code is None:
        return montant
    return montant * (1 - RABAIS[code])


def taxes(montant):
    """TPS et TVQ sur un montant, en dollars."""
    tps = montant * TPS
    tvq = (montant + tps) * TVQ
    return tps, tvq


def calculer_total(lignes, code=None):
    avant_taxes = appliquer_rabais(sous_total(lignes), code)
    tps, tvq = taxes(avant_taxes)
    return round(avant_taxes + tps + tvq, 2)
```

```python
# test_facture.py
from facture import calculer_total, taxes

PANIER = [
    {"article": "clavier", "quantite": 1, "prix": 100.00},
    {"article": "cable", "quantite": 2, "prix": 10.00},
]


def test_taxes_sur_deux_cents_dollars():
    tps, tvq = taxes(200.0)
    assert tps == 10.0
    assert round(tvq, 2) == 19.95


def test_total_sans_rabais():
    # 120 $ + TPS 6,00 $ + TVQ 11,97 $
    assert calculer_total(PANIER) == 137.97


def test_total_etudiant():
    # 108 $ + TPS 5,40 $ + TVQ 10,77 $
    assert calculer_total(PANIER, "ETUDIANT") == 124.17
```

Lancez les tests&nbsp;: les trois sont rouges. `test_total_sans_rabais` obtient
138,57 \\$ au lieu de 137,97 \\$, soixante cents de trop, et le message de
l'assertion ne dit rien de plus. Le total est faux, mais il est calculé par
quatre fonctions, et la fautive peut être n'importe laquelle. C'est le cas où
lire ne suffit plus, et où l'on regarde le programme se dérouler.

### La chasse, pas à pas

Posez un point d'arrêt sur la première ligne de `calculer_total`, celle qui
calcule `avant_taxes`, et lancez `test_total_sans_rabais` par « Debug Test »
dans le menu de la marge de `test_facture.py`.

{{< image src="vscode-debug-0-avant.webp" alt="VS Code en thème sombre, le projet test-examples : à gauche facture.py en entier, avec un point d'arrêt rouge sur la ligne avant_taxes = appliquer_rabais(sous_total(lignes), code) de calculer_total, encadrée en rouge ; à droite test_facture.py avec ses trois tests et, dans la marge, l'icône de lancement de test_total_sans_rabais, désignée par une flèche rouge" title="Avant la chasse : le point d'arrêt à l'entrée de calculer_total, et l'icône de la marge qui lance test_total_sans_rabais, ordinairement ou sous le débogueur" loading="lazy" >}}

Le programme s'arrête à l'entrée de la fonction. Le
panneau des variables montre `lignes`, la liste du panier, et `code`, qui
vaut `None`. La pile a deux étages, `calculer_total` sous
`test_total_sans_rabais`.

{{< image src="vscode-debug-1-entree.webp" alt="VS Code arrêté sous le débogueur à l'entrée de calculer_total : la ligne 34 surlignée avec une flèche jaune dans la marge ; à gauche, le panneau Variables avec Locals, code = None et lignes, la liste du panier ; le panneau Watch vide ; le panneau Call Stack marqué Paused on breakpoint avec calculer_total, facture.py 34, puis test_total_sans_rabais ; le panneau Breakpoints ; en haut, la barre du débogueur ; à droite, Test Results indique que le test est en cours" title="L'arrêt à l'entrée : lignes et code sous les yeux, et une pile à deux étages" loading="lazy" >}}

Cette ligne appelle deux fonctions, `sous_total` puis `appliquer_rabais`.
Chaque geste qui suit a sa touche, et aussi son bouton dans la petite barre
qui est apparue en haut de la fenêtre au démarrage du débogueur, dans cet
ordre&nbsp;: continuer, passer, entrer, sortir, relancer, arrêter. Les deux
font exactement la même chose, à vous de choisir. **Entrez** (F11)&nbsp;: le
débogueur descend dans la première appelée, `sous_total`, et s'arrête sur
`total = 0.0`. **Passez** (F10) ligne par ligne, en gardant
l'oeil sur `total` dans le panneau des variables&nbsp;: 0.0, puis, après le
premier tour de boucle, 100.0, puis 120.0. Au deuxième tour, sur la ligne qui appelle
`prix_ligne`, **entrez** (F11) une fois pour voir `ligne` de l'intérieur, le câble,
quantité 2, prix 10, puis **sortez** (Maj+F11) pour revenir dans la boucle avec
la valeur en main. Le sous-total est juste, 120 \\$. **Sortez** (Maj+F11) encore, et vous
voilà de retour dans `calculer_total`, la première fonction innocentée.

{{< image src="vscode-debug-2-boucle.webp" alt="VS Code arrêté dans sous_total, à la sortie de la boucle, sur la ligne return total surlignée avec total = 120.0 écrit au bout ; à gauche, Variables avec ligne dépliée, encadrée en rouge, article cable, quantite 2, prix 10.0, puis (return) prix_ligne = 20.0 et total = 120.0, encadré en rouge ; Call Stack, Paused on step, montre sous_total, calculer_total et test_total_sans_rabais ; en haut, la barre du débogueur, encadrée, continuer, passer, entrer, sortir, relancer, arrêter" title="Au bout de la boucle : total vaut 120 dans le panneau des variables, la dernière ligne traitée était le câble, et la pile a trois étages" loading="lazy" >}}

**Entrez** (F11) dans `appliquer_rabais`&nbsp;: `code` vaut `None`, la fonction rend
`montant` tel quel, 120.0. Innocentée aussi. **Passez** (F10) à la ligne suivante de
`calculer_total`, `tps, tvq = taxes(avant_taxes)`, et **entrez** (F11) dans `taxes`.
**Passez** (F10) une ligne&nbsp;: `tps` vaut 6.0, juste. **Passez** (F10) encore&nbsp;: `tvq`
vaut 12.5685, soit 12,57 \\$, et 9,975 % de 120 \\$ font 11,97 \\$. Le bogue est là, sous les yeux,
et la ligne le dit dès qu'on la relit avec ce chiffre en tête, la TVQ est
calculée sur `montant + tps` au lieu de `montant`. Pour en être sûr sans
rien modifier, tapez `montant * TVQ` dans la « Debug Console »&nbsp;: 11.97. La pile a trois étages, `taxes`, `calculer_total`, `test_total_sans_rabais`, et
un clic sur `calculer_total` montre `avant_taxes` à 120.0 pendant que `taxes`
est encore en cours.

{{< image src="vscode-debug-3-bogue.webp" alt="VS Code arrêté dans taxes, sur la ligne return tps, tvq, désignée par une flèche rouge, les valeurs écrites au bout des lignes, montant = 120.0, tps = 6.0, tvq = 12.5685 ; à gauche, Variables montre montant = 120.0, tps = 6.0 et tvq = 12.5685, ce dernier encadré en rouge ; Call Stack, encadré, montre taxes, calculer_total et test_total_sans_rabais ; à droite, la Debug Console avec l'expression montant * TVQ tapée et la réponse 11.97, encadrées" title="Le bogue sous les yeux : tvq vaut 12,5685 alors que montant * TVQ, évalué dans la console, donne 11,97" loading="lazy" >}}

Quatre fonctions, une seule fautive, et on l'a trouvée sans lire le code
d'avance, en suivant les valeurs. Corrigez la ligne, `tvq = montant * TVQ`,
relancez les tests, trois verts.

### Deux gestes de plus sur le même code

Un point d'arrêt ordinaire arrête à chaque passage, ce qui devient pénible
dans une boucle de mille tours quand le bogue est au tour 743. Un clic droit
sur le point rouge dans la boucle de `sous_total` permet d'ajouter une
condition, `ligne["article"] == "cable"`, et le débogueur ne s'arrête plus que
sur le câble. La même liste propose un nombre de passages, pour ne s'arrêter
qu'au centième tour. Et le menu de la marge offre un **point de
journalisation** (*logpoint*), un point d'arrêt qui n'arrête rien mais écrit
un message dans la console de débogage à chaque passage, avec des expressions
entre accolades&nbsp;: posez-en un sur la ligne de la boucle avec
`{ligne["article"]} : {prix_ligne(ligne)}`, relancez, et la console affiche
`clavier : 100.0` puis `cable : 20.0`, sans arrêt et sans avoir touché au
code. C'est le `print` de tout à l'heure, qui disparaît avec la session.


Les boutons de la barre du haut sont les commandes de `pdb` devenues
visibles, et la documentation de VS Code les résume en une ligne chacun&nbsp;:
passer « exécute la méthode suivante comme une seule commande », entrer « y
pénètre pour la suivre ligne par ligne », sortir « revient au contexte
d'exécution précédent en terminant les lignes restantes de la méthode ».
Deux autres boutons, relancer et arrêter, font ce que leur nom dit, et le
panneau « Breakpoints » liste tous les points posés, permet de les désactiver
d'un clic sans les retirer, et ses cases du haut arrêtent le programme sur
toute exception non rattrapée, un point d'arrêt qu'on n'a pas eu à placer, à
l'endroit exact où le programme allait mourir.

### La pile, pour de vrai

La facture n'enfonce la pile que de trois étages. Pour la voir vraiment,
prenez `factorielle`, dans `calcul.py`, posez un point d'arrêt sur sa première
ligne, `if n <= 1:`, et lancez `test_factorielle_recursive` sous le débogueur.
Premier arrêt, `n` vaut 5, deux étages. **Continuez** (F5)&nbsp;: c'est le même
point d'arrêt, un étage plus bas, `n` vaut 4. Encore, 3, puis 2, puis 1, et le
programme s'arrête sur `return 1`, le cas de base, avec six étages dans la
pile, `factorielle` cinq fois sous le test. Les quatre appels du dessous sont
tous suspendus à la même ligne, `return n * factorielle(n - 1)`, chacun avec
son propre `n`, qu'un clic sur l'étage fait apparaître, en attendant la
valeur de celui du dessus. C'est la pile de la section sur la programmation,
vue de l'intérieur. Sur cette ligne récursive, **passer** (F10) exécute toute
la récursion restante d'un coup, et **entrer** (F11) descend d'un seul
étage&nbsp;: la différence entre les deux gestes n'est jamais aussi nette qu'ici.

{{< image src="vscode-debug-5-pile.webp" alt="VS Code arrêté dans factorielle sur la ligne return 1, le cas de base, avec n = 1 dans Variables et un point d'arrêt rouge sur la ligne if n <= 1 ; à gauche, le panneau Call Stack, encadré en rouge et désigné par une flèche, montre factorielle cinq fois, la première à la ligne 8 et les quatre autres à la ligne 9, puis test_factorielle_recursive ; à droite, test_calcul.py avec test_factorielle_recursive en cours" title="La pile pour de vrai : six étages, factorielle cinq fois sous le test, les quatre du dessous suspendus à la ligne récursive" loading="lazy" >}}

Ce qui tourne derrière est l'extension « Python Debugger », installée avec
l'extension Python, qui s'appuie sur `debugpy`, le même mécanisme que `pdb`
piloté par messages plutôt que par une invite. Pour un fichier ordinaire,
plutôt qu'un test, la flèche à côté du bouton de lancement propose
« Python Debugger: Debug Python File », et la touche F5 fait de même. La
documentation mentionne un fichier `launch.json` pour les configurations de
débogage&nbsp;; vous n'en aurez pas besoin avant longtemps, F5 sans
configuration suffit pour un script. Deux gestes valent la peine d'être
connus dès maintenant. Un clic droit sur le point rouge permet de le rendre
conditionnel, par une expression, `b == 0` par exemple, ou par un nombre de
passages, pour ne s'arrêter qu'à la centième itération d'une boucle. Et
`breakpoint()` fonctionne aussi sous l'éditeur&nbsp;: un programme lancé avec le
débogueur s'y arrête comme sur un point rouge, ce qui permet de laisser un
point d'arrêt dans le code plutôt que dans l'éditeur.

Le notebook des environnements s'ouvre lui aussi ici. Ouvrez
`palindromes.ipynb`, et l'éditeur l'affiche cellule par cellule, avec un
bouton de lancement devant chacune et, en haut à droite, le choix du noyau,
où il faut prendre le Python du venv, exactement comme pour l'interpréteur de
l'encart des venvs. Les sorties sont les mêmes que dans le navigateur, puisque c'est le même
fichier et le même noyau, et les numéros d'exécution continuent de compter
d'une exécution à l'autre tant que le noyau tourne, c'est lui qui les tient.
Seule la page qui les affiche a changé, ce qui est, une dernière fois, toute
la leçon de ces encarts.

{{< image src="vscode-notebook.webp" alt="VS Code en thème sombre, le projet test-examples, palindromes.ipynb ouvert dans l'éditeur de notebooks : la barre du haut avec Generate, Code, Markdown, Run All et Restart, et à droite le sélecteur de noyau, encadré en rouge, qui affiche test-examples (3.13.5) (Python 3.13.5) ; le titre Palindromes, la phrase Un notebook garde l'état entre les cellules, puis les trois cellules de code exécutées, numérotées 2, 3 et 4, avec une coche verte, la sortie kayak, radar, Engage le jeu que je le gagne, et la sortie False" title="Le même notebook dans VS Code, exécuté avec le Python du venv du projet : mêmes sorties, et des numéros qui continuent de compter tant que le noyau tourne" loading="lazy" >}}
