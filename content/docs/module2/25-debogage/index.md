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
