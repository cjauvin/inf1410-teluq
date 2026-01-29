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
texte et des commandes, des mots, des symboles et des nombres) par opposition au
type plus moderne de l'[interface
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
