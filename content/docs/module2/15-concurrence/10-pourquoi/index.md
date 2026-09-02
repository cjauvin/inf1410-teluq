---
title: "Pourquoi la concurrence"
slug: "pourquoi"
weight: 10
---

# Pourquoi la concurrence

## Le repas gratuit

Pendant une trentaine d'années, les programmeurs ont profité d'un arrangement
remarquable&nbsp;: il suffisait d'attendre. Un programme jugé trop lent en 1995
devenait parfaitement acceptable en 1997, sans qu'une seule ligne soit
modifiée, parce que les processeurs devenaient plus rapides d'année en année.
Intel vendait des Pentium à 100 MHz en 1994, et des Pentium 4 à plus de 3 GHz
en 2002. Le même code en profitait automatiquement, sans effort et sans
risque. Herb Sutter a donné à cette période un nom qui est resté, celui du
repas gratuit, dans un article de 2005 dont le titre annonçait la mauvaise
nouvelle&nbsp;: *The Free Lunch Is Over*.

## La loi de Moore, et celle qu'on oublie

Tout le monde a entendu parler de la **loi de Moore**, et presque tout le monde
la cite de travers. En avril 1965, Gordon Moore, alors chez Fairchild
Semiconductor et pas encore cofondateur d'Intel, publie dans la revue
*Electronics* une observation de deux pages&nbsp;: le nombre de composants qu'on
sait graver sur une puce, à coût égal, double à intervalle régulier. Il parle
d'un doublement annuel, qu'il révisera en 1975 à deux ans. La formule est
devenue le raccourci favori de toute l'industrie pour dire que les ordinateurs
vont toujours plus vite. Or Moore ne parle pas de vitesse. Il parle de
*quantité*, du nombre de transistors, et de rien d'autre.

Le lien entre la quantité et la vitesse vient d'une seconde loi, bien moins
connue, qu'on doit à Robert Dennard, chez IBM, en 1974. La **loi de Dennard**
dit que lorsqu'on réduit un transistor, la puissance qu'il dissipe diminue
d'autant, si bien que la densité thermique de la puce reste constante. On peut
donc à la fois graver plus de transistors et les faire battre plus vite, sans
que la puce chauffe davantage. C'est cette loi-là, et non celle de Moore, qui
payait le repas gratuit. Et c'est elle, on va le voir, qui a cessé de tenir.

## La fin, en 2004

Le repas s'est arrêté vers 2004. En octobre de cette année-là, Intel annonce
l'abandon de son Pentium 4 à 4 GHz, une machine promise et jamais livrée.
L'obstacle n'était pas la finesse de gravure, qui continuait de progresser,
mais bien la fin de la loi de Dennard. En dessous d'une certaine taille, les
transistors se mettent à fuir du courant et la densité thermique repart à la
hausse. Intel montrait depuis la fin des années 90 des projections où celle de
ses processeurs rejoignait celle d'un réacteur nucléaire si la tendance se
poursuivait. Les transistors continuaient donc de doubler, comme le voulait
Moore, mais ils ne pouvaient plus servir à aller plus vite. Les **fondeurs**,
c'est-à-dire les entreprises qui gravent les puces, s'en sont servis pour aller
plus large, en plaçant plusieurs coeurs sur une même puce. La puissance a
continué d'augmenter. Elle a simplement cessé d'être gratuite.

{{< illustration src="moore-dennard.svg" legende="La loi de Moore n'a pas cessé de tenir. C'est celle de Dennard qui s'est arrêtée, et les transistors qu'on continuait de graver sont devenus des coeurs faute de pouvoir devenir de la vitesse." >}}

## Ce qu'est un coeur

Un mot sur ce qu'est un coeur, puisque tout le reste en dépend. Le **processeur**
est la pièce qui exécute les instructions d'un programme, une par une, dans
l'ordre. Un **coeur** est une de ces machines à exécuter, complète et autonome&nbsp;:
elle possède ses propres registres, sa propre position dans le programme, et
elle avance sans rien demander aux autres. Une puce à dix coeurs contient donc
dix exécuteurs indépendants, capables de faire progresser dix suites
d'instructions différentes dans la même seconde. C'est cette dernière phrase
qui compte, et c'est à peu près la seule chose que le matériel offre&nbsp;: la
possibilité que plusieurs choses avancent en même temps. Il ne dit rien de la
manière de découper un programme pour en profiter, ni de ce qui arrive quand
deux coeurs touchent à la même donnée.


## Le travail change de main

Le déplacement est plus profond qu'il n'y paraît. Jusque-là, l'accélération
était un service rendu par le matériel, silencieusement, à du code qui n'avait
rien demandé. Elle devient une propriété qu'il faut écrire soi-même. Un
programme qui ne fait qu'une chose à la fois, sur une machine à dix coeurs, en
occupe un et laisse les neuf autres allumés à ne rien faire. Le portable sur
lequel ces lignes ont été écrites en compte dix, un téléphone courant en compte
six ou huit, et cette abondance est devenue la norme jusque dans les objets les
plus modestes. Le programmeur hérite donc d'une tâche que personne n'avait à
faire avant lui, celle de découper son travail pour occuper une machine qu'on
ne lui vend plus autrement.

### La loi d'Amdahl, ou pourquoi dix coeurs ne font pas dix fois mieux

Même parfaitement découpé, un programme ne va pas dix fois plus vite sur dix
coeurs, et la raison en a été formulée dès 1967 par Gene Amdahl, alors
architecte chez IBM. La **loi d'Amdahl** observe que tout programme contient
une part qu'on ne peut pas répartir, lire le fichier d'entrée, assembler le
résultat final, et que cette part fixe un plafond. Si 10&nbsp;% du travail
reste séquentiel, dix coeurs donnent un gain d'un peu plus de cinq fois, et une
infinité de coeurs ne donnerait jamais plus de dix. En cuisine, c'est le plat
qu'il faut de toute façon dresser à la fin, quel que soit le nombre de
cuisiniers derrière les fourneaux. Le parallélisme a donc un rendement
décroissant, et savoir où se trouve la part séquentielle d'un programme compte
davantage que le nombre de coeurs qu'on lui donne.

Avant d'aller plus loin, il faut lever une ambiguïté de vocabulaire, parce que
le mot de concurrence est employé couramment pour deux choses différentes, et
qu'un informaticien canadien a pris soin de les séparer.

## La concurrence n'est pas le parallélisme

La distinction la plus utile du domaine tient en une phrase, et on la doit à
Rob Pike, un informaticien canadien formé à l'Université de Toronto, passé par
les Bell Labs où il a travaillé sur Unix et coinventé l'UTF-8 avec Ken
Thompson, avant de concevoir le langage Go chez Google. Dans une conférence de
2012 au titre sans ambiguïté, *Concurrency Is Not Parallelism*, il pose ceci&nbsp;:
la **concurrence** consiste à s'occuper de plusieurs choses à la fois, le
**parallélisme** à en faire plusieurs à la fois. Le cuisinier seul devant ses
trois casseroles s'en occupe&nbsp;; les trois cuisiniers les font. La première est
une manière de structurer un programme, la seconde une manière de l'exécuter. Un programme
concurrent s'écrit comme un ensemble de tâches indépendantes qui progressent
chacune à leur rythme, et qu'elles avancent réellement ensemble sur dix coeurs
ou chacune à son tour sur un seul ne change rien à sa structure. La concurrence
est une propriété du code. Le parallélisme est une propriété de la machine qui
l'exécute.

### Trente ans de langages

Ce n'est pas une remarque de conférencier. Pike a passé trente ans à construire
des langages autour de cette idée. Dès la fin des années 80, aux Bell Labs, il
conçoit Newsqueak, un langage où les tâches communiquent par des canaux plutôt
qu'en se partageant de la mémoire. L'idée vient de Tony Hoare, qui avait
formalisé en 1978 un modèle où des tâches indépendantes ne s'échangent que des
messages, les *processus séquentiels communicants*. La même idée traverse
ensuite Alef puis Limbo, les langages des systèmes Plan 9 et Inferno, avant
d'aboutir en 2009 à Go, conçu chez Google avec Ken Thompson et Robert
Griesemer. Go en fait sa signature&nbsp;: ses tâches légères, les **goroutines**, se
lancent avec un seul mot-clé, et se parlent par des canaux. Le mot d'ordre du
langage tient dans une formule qu'on retrouvera plus loin dans cette section,
ne communiquez pas en partageant de la mémoire, partagez de la mémoire en
communiquant. Trente ans séparent l'article de Hoare de la sortie de Go, ce qui
dit assez la longévité des bonnes idées dans ce domaine.

{{< image src="rob-pike.webp" alt="Rob Pike donnant une conférence d'ouverture, debout devant un écran de projection" title="Rob Pike à OSCON en 2010. Photo : Kevin Shockey, CC BY 2.0" loading="lazy" >}}

## Attendre n'est pas calculer

Il reste une seconde distinction, et elle ne porte pas sur la même question.
La précédente demandait comment le travail est organisé. Celle-ci demande
pourquoi un programme est lent, et il y a deux réponses qui n'ont presque rien
à voir l'une avec l'autre. Un programme peut être lent parce qu'il **calcule**,
et il l'est alors autant que son coeur le permet, pas davantage. Il peut aussi
être lent parce qu'il **attend**, une réponse du réseau, une lecture de disque,
une requête à une base de données, et il ne fait alors strictement rien, comme
le cuisinier planté devant une eau qui n'a pas encore bouilli. Vus du
dehors les deux se ressemblent, l'utilisateur patiente dans un cas comme dans
l'autre, mais leur remède est opposé. Le premier manque de bras, et c'est là
que le vrai parallélisme sur plusieurs coeurs prend tout son sens. Le second
n'a aucun besoin d'un bras de plus, puisque celui qu'il a déjà ne bouge pas. Il
a besoin qu'on cesse de le laisser inerte pendant que la réponse chemine. Un
serveur qui attend cent réponses en même temps ne réclame pas cent coeurs. Il
lui en faut un seul, qui ne s'arrête jamais.
