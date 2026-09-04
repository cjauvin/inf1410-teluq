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
case of bug being found », premier cas réel de bogue trouvé. Le carnet est
conservé au musée, mite comprise. Grace Hopper faisait partie de l'équipe, ce
qui lui vaut souvent la paternité de l'anecdote&nbsp;; le musée précise que le
carnet n'était probablement pas le sien, mais que son équipe et elle ont
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
