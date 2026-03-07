---
title: "Environnements du cours"
weight: 10
---

# Les environnements du cours

{{< image src="matrix.jpg" alt="" title="" loading="lazy" >}}

Dans ce cours, nous allons beaucoup utiliser la [ligne de
commande](https://fr.wikipedia.org/wiki/Interface_en_ligne_de_commande). La
ligne de commande est un paradigme ancien, qui survit au passage du temps dans
le monde du développement informatique en raison de sa versatilité, de sa
souplesse et de son universalité. La ligne de commande (souvent appelée CLI en
anglais, ou console) est un type d'interface usager textuelle (où on manipule du
texte, soit des mots, des commandes, des symboles, des formules, des nombres,
etc) par opposition au type plus moderne de l'[interface
graphique](https://fr.wikipedia.org/wiki/Interface_graphique) (GUI en anglais,
graphical user interface, ou souvent juste UI). Le CLI est plus "proche" de la
programmation, qui est elle aussi un média essentiellement textuel (et logique,
souvent mathématique).

Il y a beaucoup de confusion technique et sémantique autour de ce sujet, tentons
de clarifier un peu les choses. Que veut-on dire exactement par ligne de
commande? Est-ce qu'il s'agit d'une application particulière? Il s'agit plutôt
d'un assemblage d'applications imbriquées les unes dans les autres, et faites
pour fonctionner ensemble (en anglais on parle souvent d'une "stack"
d'applications).

## Le système d'exploitation

Votre cas particulier dépendra tout d'abord du système d'exploitation (OS,
operating system en anglais) que vous utilisez. De manière extrêmement générale,
il y a deux grandes familles :

* Les systèmes basés sur Unix (ce qui inclut MacOS et Linux, qui en sont des
  "saveurs" particulières)
* Les systèmes basés sur Windows

Dans le cadre de ce cours, nous allons travailler exclusivement dans le premier
contexte. Si vous utilisez Windows, vous devrez probablement utiliser
[WSL](https://fr.wikipedia.org/wiki/Windows_Subsystem_for_Linux) qui est un
sous-système Linux, qui est conçu pour fonctionner à _l'intérieur_ de Windows.

## L'émulateur de terminal

Considérons ensuite un type d'application particulier: l'[émulateur de
terminal](https://fr.wikipedia.org/wiki/%C3%89mulateur_de_terminal). Selon le
système d'exploitation que vous utilisez, il existe une multitude d'applications
de ce genre (moi personnellement j'utilise l'application iTerm2, qui roule sur
MacOS). Cette application est généralement considérée comme étant "graphique",
dans le sens qu'elle utilise le système de fenêtrage du OS, et certains éléments
de son fonctionnement (le menu avec les préférences par exemple) auront un style
"graphique". Pourtant, son essence est de nature fondamentalement textuelle : la
quasi totalité de son espace est occupé par une boite dans laquelle on peut
entrer du texte, généralement ligne par ligne. Ce type d'application est appelé
"émulateur de terminal" car il modélise des appareils physiques (réels!)
beaucoup plus anciens, qui servaient autrefois d'interfaces pour les ordinateurs
:

{{< image src="command-line-backgrounder-vt100-terminal.jpg" alt="" title="" loading="lazy" >}}

## Le shell

L'émulateur de terminal de notre choix sera en charge de rouler un autre type
d'application : un
[shell](https://fr.wikipedia.org/wiki/Interface_syst%C3%A8me). Encore ici, il y
a plusieurs possibilités, certaines très anciennes et classiques : Bash, Zsh
(pour les systèmes Unix) ou Powershell pour Windows. Le shell doit être vu comme
un autre type d'interface (de nature plus logique et procédurale, par opposition
à graphique)  entre vous (l'utilisateur) et le système d'exploitation. Les
shells sont en charge d'exécuter des commandes (comme par exemple la commande
Unix `ls`, pour lister les fichiers d'un répertoire) mais ils ont aussi leur
propre langage de programmation intégré : on parle parfois de Bash en tant que
langage de scripting. Certaines applications sont entièrement écrites avec le
langage Bash, par exemple. Pour ma part, j'ai longtemps utilisé Bash, ensuite je
suis passé à Zsh, et récemment je me suis converti à Fish.

C'est à ce dernier niveau, celui du shell, que la majorité de l'action de ce
cours se passera. Le shell est utilisé en général pour rouler toutes sortes
d'applications (par exemple `python`, `git`, `docker`, etc), et combiner ou
manipuler leurs résultats (souvent de nature textuelle eux aussi). Par exemple
si vous voyez ceci dans le cours :

```shell
$ echo "Christian" | python3 -c "import sys; print(f'Hello {sys.stdin.read().strip()}!')"
Hello Christian!
```

Il s'agit d'une commande (en fait deux, reliées entre elles) qui peut être
exécutée dans un shell Bash ou autre (les shells de type Unix ont tendance à
être très compatibles entre eux). Le caractère `$` (qui peut être différent pour
vous, ce n'est qu'une convention) indique le "prompt", le mécanisme d'entrée
pour une commande. La ligne qui suit, sans prompt, montre le résultat de la
commande. Essayez-la dans votre propre environnement ! Et si ça ne fonctionne
pas, essayez tout d'abord de comprendre pourquoi (ce que dit le message d'erreur
en particulier, qui parfois, peut être très cryptique, il est vrai).

## La philosophie Unix

La philosophie Unix est un ensemble de principes de conception logicielle qui a
émergé dans les années 1970 aux Bell Labs, en même temps que le système Unix
lui-même. Ses auteurs principaux, Ken Thompson et Dennis Ritchie (les créateurs
d'Unix et du langage C), ainsi que Doug McIlroy (l'inventeur du concept de
pipe), ont formulé une vision qui peut se résumer en quelques idées simples :
chaque programme devrait faire une seule chose et la faire bien; les programmes
devraient pouvoir être composés ensemble, la sortie de l'un devenant l'entrée de
l'autre; et le texte devrait être le format universel d'échange entre
programmes. Ces principes peuvent sembler évidents aujourd'hui, mais ils
représentaient un choix radical à une époque où la tendance dominante était de
construire de gros systèmes intégrés et monolithiques.

L'exemple de commande que nous avons vu plus haut illustre déjà ces principes en
action. Le symbole `|` (le pipe, inventé par McIlroy) permet de connecter la
sortie de la commande `echo` à l'entrée du programme `python3`. Chaque composant
fait son travail de manière indépendante, et c'est leur composition qui produit
le résultat voulu. Cette idée de composition est au coeur de la philosophie Unix,
et elle se manifeste partout dans l'écosystème : on peut par exemple compter le
nombre de fichiers Python dans un répertoire en enchaînant `ls`, `grep` et `wc`
:

```shell
$ ls | grep "\.py$" | wc -l
7
```

Trois petits programmes, chacun avec une responsabilité précise (lister,
filtrer, compter), combinés pour accomplir une tâche qu'aucun d'entre eux ne
pourrait faire seul.

Cette philosophie aurait pu rester un artefact historique des Bell Labs, mais
elle a connu une seconde vie spectaculaire grâce à Linux. En 1991, Linus
Torvalds, un étudiant finlandais, a commencé à développer un noyau de système
d'exploitation compatible Unix, qu'il a rendu disponible librement sur
l'internet naissant. Ce geste a catalysé un mouvement qui couvait depuis les
années 1980 avec le projet GNU de Richard Stallman : l'idée que le code source
d'un logiciel devrait être accessible, modifiable et redistribuable par tous.
Linux est devenu le véhicule principal de la philosophie Unix dans le monde
moderne, et son adoption a été propulsée par la croissance explosive de
l'internet. Aujourd'hui, la très grande majorité des serveurs web, des
infrastructures cloud et des superordinateurs roulent Linux. Android, le système
d'exploitation mobile le plus utilisé au monde, est lui aussi basé sur un noyau
Linux. La philosophie Unix, avec ses petits outils composables et son
orientation textuelle, s'est révélée remarquablement adaptée au monde des
serveurs et du web, où l'automatisation et le scripting sont essentiels.

L'approche de Windows est fondamentalement différente. Là où Unix propose une
multitude de petits outils indépendants qui communiquent par texte, Windows a
historiquement favorisé de grosses applications intégrées, avec des interfaces
graphiques riches et des formats de données propriétaires. Ce n'est pas un
accident : Microsoft a bâti son empire sur la vente de logiciels commerciaux
(Windows, Office, etc.), et son modèle économique reposait sur le contrôle de
l'écosystème. Le résultat est un environnement où les applications sont souvent
de grandes "boîtes noires" difficiles à composer entre elles, et où la ligne de
commande a longtemps été un citoyen de seconde classe. Il est révélateur que
Microsoft ait fini par développer WSL (Windows Subsystem for Linux), qui permet
de rouler un environnement Linux complet à l'intérieur de Windows : c'est un
aveu que pour le développement logiciel, l'écosystème Unix est devenu
incontournable. Microsoft a aussi fait l'acquisition de GitHub en 2018, et
contribue aujourd'hui activement à plusieurs projets open source, ce qui aurait
été impensable dans les années 1990, quand l'entreprise qualifiait Linux de
"cancer".

Cette victoire de l'écosystème Unix sur ses concurrents n'était pourtant pas
évidente au départ. En 1989, Richard Gabriel, un informaticien issu du monde
Lisp et de l'intelligence artificielle, a publié un essai provocateur intitulé
"Worse is Better". Gabriel y compare deux philosophies de conception :
l'approche "MIT", issue du monde académique et du langage Lisp, qui vise la
perfection et l'élégance théorique, quitte à produire des systèmes complexes;
et l'approche "New Jersey" (en référence aux Bell Labs, où Unix a été créé), qui
privilégie la simplicité d'implémentation, quitte à sacrifier certaines
garanties de correction ou de complétude. L'argument central de Gabriel est que
l'approche "pire" (celle d'Unix) gagne à long terme, parce qu'un système simple
est plus facile à porter sur de nouvelles machines, plus facile à comprendre, et
plus facile à faire adopter. Une fois adopté par une masse critique
d'utilisateurs, le système peut ensuite être amélioré graduellement. C'est
exactement ce qui s'est passé avec Unix et Linux : un système techniquement
imparfait, mais simple et portable, a fini par dominer le monde, tandis que des
systèmes théoriquement supérieurs (comme les machines Lisp) ont disparu.

L'essai de Gabriel met le doigt sur une tension fondamentale en génie logiciel,
que nous retrouverons tout au long de ce cours : la simplicité pragmatique
versus la perfection théorique. Le principe YAGNI ("You Aren't Gonna Need It"),
que nous verrons plus tard, est une incarnation directe de cette idée : mieux
vaut un système simple qui fonctionne aujourd'hui qu'un système parfait qui
n'est jamais terminé. Le succès de Linux, de Git (dont nous parlerons en
détail) et de l'écosystème open source en général témoigne de la puissance de
cette approche. Ce n'est pas que la qualité n'a pas d'importance, mais plutôt
que la bonne stratégie est souvent de commencer simple, de livrer rapidement, et
d'améliorer de manière itérative en réponse aux besoins réels des utilisateurs.

## Pourquoi travailler avec ces outils particuliers?

Pourquoi est-ce qu'on s'impose de travailler avec ces outils dans ce cours? Tout
d'abord, en général, la ligne de commande est associée plus fortement aux mondes
Unix (ce qui inclut Linux et MacOS, qui en sont des "saveurs" particulières) et
du développement logiciel. Unix et la ligne de commande sont plus "orientés"
vers le développement, et ils ont une longue tradition qui comprend une
multitude d'outils classiques, etc. Ensuite la ligne de commande est plus axée
sur une manière textuelle d'interagir avec un ordinateur, considérée
généralement comme plus "proche" de la programmation. Et finalement, Unix, en
tant qu'écosystème global (surtout avec Linux) est plus orienté web. Il est
parfaitement possible de faire du développement web sur une machine Windows (et
plusieurs le font), mais en général, étant donné qu'une grande partie des
serveurs et de l'infrastructure de l'internet roule Linux, il est considéré un
peu plus "naturel" d'utiliser aussi un système basé sur Unix, en tant que
développeur. Finalement, remarquons le fait que la ligne de commande est
tellement importante et omniprésente qu'elle se retrouve au coeur même d'outils
modernes (et graphiques) de développement. VS Code par exemple a sa propre
console (voici ma propre version, avec laquelle je développe ce cours, la
console est à droite) :

{{< image src="my-vscode.png" alt="" title="" loading="lazy" >}}

Et même les navigateurs web ont des consoles intégrées, voici mon Brave avec sa
console Javascript à droite :

{{< image src="my-brave.png" alt="" title="" loading="lazy" >}}

## Les langages du cours

Dans ce cours, nous allons principalement utiliser deux langages de
programmation : Python et JavaScript. Ce choix n'est pas arbitraire. Si on
regarde le paysage informatique actuel, on peut argumenter que trois langages (ou
familles de langages) couvrent à eux seuls une part démesurée du terrain :
C/C++, Python et JavaScript. Comprendre pourquoi ces trois-là dominent, c'est
comprendre une bonne partie de l'histoire et de la structure du monde logiciel
contemporain.

C est le langage de la fondation. Créé par Dennis Ritchie aux Bell Labs au début
des années 1970, précisément pour réécrire Unix dans un langage plus portable
que l'assembleur, C est devenu le langage dans lequel est construit une grande
partie de l'infrastructure informatique mondiale. Les noyaux de Linux, Windows
et MacOS sont écrits en C. Les interpréteurs de Python et de JavaScript le sont
aussi. C++ (créé par Bjarne Stroustrup en 1979, également aux Bell Labs) a
étendu C avec la programmation orientée objet et est devenu le langage de
prédilection pour les systèmes qui demandent à la fois performance et
abstraction : les navigateurs web, les moteurs de jeux vidéo, les bases de
données. C et C++ sont les langages "proches de la machine", ceux qui permettent
de contrôler finement la mémoire et les ressources matérielles, au prix d'une
complexité considérable pour le programmeur.

Python, créé par Guido van Rossum en 1991 (la même année que Linux, par
coïncidence), représente une philosophie très différente de C. Là où C donne un
contrôle maximal au programmeur au prix de la complexité, Python mise tout sur la
lisibilité et la simplicité. Van Rossum voulait un langage où le code se lit
presque comme de l'anglais, et où il n'y a idéalement qu'une seule façon
évidente de faire les choses (c'est le fameux "Zen of Python", accessible en
tapant `import this` dans un interpréteur Python). Le résultat est un langage
objectivement lent par rapport à C, mais d'une productivité remarquable : on
peut exprimer en quelques lignes de Python ce qui en prendrait des dizaines en
C. Cette simplicité a fait de Python le langage dominant dans l'enseignement de
la programmation, dans le scripting et l'automatisation, et surtout dans le
monde de la science des données et de l'intelligence artificielle. Les
bibliothèques comme NumPy, pandas, TensorFlow et PyTorch, qui propulsent la
révolution actuelle de l'IA, sont toutes accessibles via Python (même si leurs
entrailles sont souvent écrites en C ou C++ pour la performance). Le succès de
Python est un autre cas de "Worse is Better" : un langage techniquement
"inférieur" en performance brute, mais tellement plus simple à apprendre et à
utiliser qu'il a fini par s'imposer dans des domaines entiers.

Le cas de JavaScript est peut-être l'illustration la plus extrême de "Worse is
Better" dans l'histoire des langages de programmation. En 1995, Brendan Eich, un
ingénieur chez Netscape, a créé JavaScript en seulement 10 jours, sous la
pression de livrer rapidement un langage de scripting pour le navigateur
Netscape Navigator. Le résultat était un langage truffé d'incohérences et de
comportements surprenants (les bizarreries de la coercition de types en JS sont
devenues légendaires). On aurait très bien pu imaginer qu'un autre langage,
mieux conçu, finisse par prendre sa place. Plusieurs ont d'ailleurs essayé :
Java avec ses applets, Flash avec ActionScript, même Dart de Google visait
explicitement à remplacer JavaScript dans le navigateur. Mais aucun n'a réussi,
pour une raison simple et brutale : JavaScript était déjà là. Il était le seul
langage exécutable nativement dans tous les navigateurs, et cette position de
monopole de fait s'est auto-renforcée au fil du temps. Plutôt que de remplacer
le langage, la communauté a choisi de l'améliorer graduellement (les versions
modernes d'ECMAScript ont corrigé beaucoup de ses défauts originaux) et de
construire par-dessus : Node.js (2009) a permis d'utiliser JavaScript côté
serveur, et des frameworks comme React, Vue et Angular en ont fait un outil de
développement d'interfaces sophistiqué. Aujourd'hui, JavaScript est probablement
le langage le plus utilisé au monde, et il est difficile de concevoir un
développeur web qui ne le connaît pas. C'est un triomphe du pragmatisme sur
l'élégance, de l'adoption sur la conception.

Ces trois familles de langages forment ensemble une sorte de colonne vertébrale
du monde logiciel : C/C++ pour les fondations et la performance, Python pour la
productivité et l'IA, JavaScript pour le web et les interfaces. Dans ce cours,
nous utiliserons surtout Python (pour sa clarté pédagogique et son omniprésence
dans les outils de développement moderne) et JavaScript (pour tout ce qui touche
au web). Mais il est utile de garder en tête que ces langages ne sont pas des
choix neutres : ils portent en eux des philosophies, des histoires et des
compromis qui reflètent les tensions fondamentales du génie logiciel.
