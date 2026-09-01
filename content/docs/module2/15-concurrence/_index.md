---
title: "Concurrence et parallélisme"
slug: "concurrence"
weight: 15
bookCollapseSection: true
---

# Concurrence et parallélisme



Il y a une hypothèse que tout programmeur fait sans jamais y penser&nbsp;: que les
choses arrivent dans l'ordre. La ligne 12 s'exécute après la ligne 11, une
variable qu'on vient d'écrire contient bien ce qu'on y a mis, et un programme
qui a fonctionné une fois se comportera pareil la fois suivante. Cette
hypothèse est si profondément installée qu'on ne la remarque qu'au moment où
elle cesse d'être vraie. C'est exactement ce qui se produit dès qu'un programme
fait plusieurs choses à la fois, et c'est ce qui rend le sujet réputé
difficile. Il ne s'agit pas d'apprendre une bibliothèque de plus, mais de
renoncer à une intuition.


{{< illustration src="cuisine.svg" legende="Dans les deux cas, trois plats avancent. À gauche une seule paire de mains les mène tour à tour, à droite trois paires travaillent vraiment en même temps. La concurrence est une manière d'organiser le travail, le parallélisme une manière de l'exécuter." >}}

On pourrait espérer que tout cela ne regarde que les auteurs de systèmes
d'exploitation. Ce n'est pas le cas. L'application que vous développerez cette session devra répondre à
plusieurs personnes en même temps, sans faire patienter la deuxième jusqu'à ce
que la première ait fini. Quand elle enverra un courriel de confirmation, elle
ne devra pas immobiliser celui qui vient de cliquer pendant que le message
chemine. Rien de tout cela n'est exotique, et pourtant rien de tout cela ne
fonctionne si le programme ne sait mener qu'une chose à la fois. Le reste du
cours s'appuie d'ailleurs déjà sur ces mécanismes sans les avoir jamais
expliqués, dans les sections sur
[les APIs]({{< relref "/docs/module3/20-apis" >}}) et sur
[la scalabilité]({{< relref "/docs/module5/60-scalabilite" >}}).

Reste que c'est difficile, et d'une difficulté particulière&nbsp;: les outils sur
lesquels vous avez appris à compter n'y voient rien. Edward Lee dirige à
Berkeley, depuis 2000, un projet qui construit exactement ce genre de logiciels,
avec une discipline peu commune&nbsp;: relecture ligne à ligne par des gens qui
connaissent le sujet mieux que quiconque, tests de non-régression couvrant
100&nbsp;% du code. Le système a tourné quatre ans sans le moindre incident. Le
26 avril 2004, il s'est figé d'un coup et n'a plus rien fait du tout. Le défaut
y était depuis le premier jour.

Retenez ce chiffre de 100&nbsp;%, parce que la section sur
[les tests]({{< relref "/docs/module2/20-tests" >}}) vous apprendra à vous en
méfier, et voici son démenti le plus spectaculaire. Ni la relecture par des
experts, ni une couverture totale n'ont révélé le défaut. C'est la première
fois dans ce cours qu'on rencontre une catégorie d'erreurs contre laquelle nos
outils habituels ne peuvent à peu près rien, et c'est ce qui justifie de lui
consacrer une section entière.

Sa place dans ce module découle du reste. Le module 2 s'intitule « Concevoir un
programme correct », et une erreur de ce genre en est l'archétype&nbsp;: elle ne
fait pas planter le programme, elle lui fait produire une mauvaise réponse, de
temps en temps, sans jamais rien signaler.

Le parcours suit cinq étapes. On commencera par **pourquoi** le sujet s'impose,
en remontant au moment où le matériel a cessé d'accélérer tout seul, et en
posant les deux distinctions qui organisent le reste. On verra ensuite ce que
le système d'exploitation offre réellement, avec les **processus et les
threads**, puis **ce qui casse** quand plusieurs d'entre eux touchent aux mêmes
données. On étudiera la réponse historique alternative, qui consiste à **ne pas
partager** du tout, avant de terminer sur la manière dont un seul fil
d'exécution peut servir des milliers de connexions à condition de **ne jamais
bloquer**.
