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

## Le débogueur est une boucle interactive arrêtée

Regardez de nouveau l'invite `(Pdb)`. Elle vous a laissé taper une expression,
`s[0], s[-1]`, l'a évaluée et a affiché le résultat, puis a attendu la
suivante. C'est exactement la boucle interactive de la page des
[environnements]({{< relref "/docs/environnements" >}}), le `>>>` de Python,
à une différence près, qui fait tout&nbsp;: elle est arrêtée à une ligne précise
d'un programme en cours, et ses variables sont celles du programme à cet
instant. Un débogueur est un REPL avec un contexte. Une fois qu'on a vu cela,
deux choses deviennent évidentes. La première est `ipdb`, qui donne à `pdb`
le confort d'IPython, la complétion, la coloration, les meilleures traces,
« avec la même interface que le module `pdb` », dit son README, donc les
mêmes commandes. On n'a même pas à modifier le code pour l'utiliser&nbsp;: la
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

La seconde chose évidente est le notebook Jupyter, présenté dans la page des
[environnements]({{< relref "/docs/environnements" >}})&nbsp;: un programme
découpé en cellules qu'on exécute une à une, l'état restant vivant entre deux,
autrement dit un point d'arrêt permanent, dans lequel on peut écrire. C'est ce
qui le rend irremplaçable pour explorer des données, et c'est aussi son piège,
qui est un piège de débogage&nbsp;: l'état survit aux cellules, on les exécute
dans le désordre, on en modifie une sans relancer les autres, et l'on obtient
des résultats que personne ne saura reproduire, pas même soi le lendemain. La
règle de survie tient en un geste, relancer le notebook de zéro avant de
croire un résultat. Ce qui a changé depuis Kernighan, c'est le prix
d'entrée&nbsp;: il trouvait `adb` difficile à apprendre, et il avait raison. Dans
l'éditeur, tout ce que la session `(Pdb)` a demandé en quatre commandes se
voit sans en taper une seule.
