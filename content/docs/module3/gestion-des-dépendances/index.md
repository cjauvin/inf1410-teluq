---
title: "La gestion des dépendances"
weight: 20
---

# La gestion des dépendances

Dès qu'un programme devient un peu plus complexe, deux phénomènes interviennent
habituellement :

1. Le programme est décomposé en plusieurs modules
2. Certaines fonctionnalités du programmes peuvent être accomplies par des
   programmes (ou des librairies) externes

Dans le cas (2), on nomme parfois les librairies externes des "dépendances", ou des
"paquets" (packages en anglais, plus communément).

Dans les débuts de l'ingénierie logicielle, ces dépendances étaient gérées à la
main, en copiant et échangeant des fichiers.

Avec l'apparition de Linux au début des années 90, une innovation importante
allait vite apparaître : les gestionnaire de paquets. Des exemples fameux sont
[APT](https://fr.wikipedia.org/wiki/Advanced_Packaging_Tool) pour les
distributions Debian et Ubuntu de Linux, et
[RPM](https://fr.wikipedia.org/wiki/RPM_Package_Manager) pour d'autres
distributions comme Red Hat, Fedora, etc.

Ces paquets sont en général des programmes et des librairies qui sont
compatibles avec une version particulière de Linux et des sous-systèmes qui sont
présents dans une distribution particulière. Par exemple si on utilise Ubuntu
24.04, une version particulière d'une distribution particulière de Linux basée
sur Debian, le gestionnaire de paquets `apt` ne permettra que d'installer des
programmes compatibles avec Ubuntu 24.04. Non seulement la compatibilité des versions
est gérée au niveau du système global, mais aussi entre les paquets (programmes ou librairies, entre eux). Si par exemple l'installation de la version 7 de LibreOffice
nécessite une version particulière de Java, le gestionnaire de paquets gérera les
dépendances intelligemment, et automatiquement.

## Le versionnage sémantique : SemVer

Au fil du temps et de l'évolution de la culture du développement logiciel, le
versionnage dit _sémantique_ (SemVer) s'est imposé en tant que convention pour numéroter
les versions d'un logiciel, que ce soit un programme ou une librairie.

{{< image src="semver.png" alt="" title="" loading="lazy" >}}

Bien que l'interprétation ne soit pas toujours identique, en général on
s'accorde pour dire que la composante "majeure" du numéro de version correspond
à un changement important, qui "brise" la compatibilité avec les versions
précédentes (s'il y en a). S'il s'agit d'une librairie logicielle par exemple,
la mise à jour demandera probablement un travail assez important, non-trivial.

Le deuxième nombre, la version mineure, indique l’ajout de nouvelles
fonctionnalités qui demeurent compatibles avec l’existant. Le logiciel
s’enrichit, mais sans obliger les utilisateurs à modifier leur code. Enfin, le
troisième nombre, appelé correctif ou patch, correspond à des réparations
internes : corrections de bugs, améliorations de performance ou failles de
sécurité qui ne modifient pas l’interface offerte aux autres programmes.

Grâce à cette structure simple, un numéro de version devient une véritable
promesse. Il permet aux équipes de décider automatiquement quelles mises à jour
peuvent être installées sans risque et lesquelles exigent une attention
particulière. Les gestionnaires de dépendances modernes s’appuient largement sur
cette logique pour éviter les surprises. Sans une convention partagée, une
nouvelle version pourrait tout aussi bien contenir une amélioration bénigne
qu’un changement radical rendant l’application inutilisable.

Adopter SemVer revient donc à instaurer une relation de confiance entre les
mainteneurs d’un logiciel et celles et ceux qui l’intègrent dans leurs propres
projets. Le numéro n’est plus simplement un identifiant : il devient une
information sur la stabilité, la continuité et l’effort requis pour évoluer avec
le produit.

Il est à noter que bien que SemVer soit le schéma le plus répandu, il en existe
d'autres : Ubuntu par exemple utilise des numéros de version qui correspondent à
l'année et au mois de livraison d'une certaine version.

Il y a aussi une notion assez populaire, qui consiste à considérer qu'un
logiciel ou une librairie ne peut pas être considérée _stable_ tant qu'elle n'a
pas atteint au moins la version `1.0.0`. Certains projets restent d'ailleurs
indéfiniment dans un schéma de versions `0.x.y`, afin d'échapper à une certaine
pression sociale, et ainsi pouvoir conserver une certaine liberté créative et
d'action.

Il est à noter que pour les langages de programmation (qui sont à la fois des
programmes et des librairies), la question du numéro de version est
particulièrement cruciale et parfois même controversée. Un cas fameux est la
transition de la version 2 du langage Python, à la version 3, qui était prévue
devoir être relativement simple et rapide, mais qui a pris au moins 10 ans à
intervenir, étant donné toute la complexité technique et sociale que cette
transition a entraînée.

La notion de versionnage sémantique est tellement importante et omniprésente
qu'elle a de l'influence à l'extérieur de la sphère du développement logiciel.
On parlera ainsi de la Playstation 5, de la Mazda 3, etc. Même des choses qui
pourraient à priori ressembler à du logiciel, comme le Web 2.0 et le Web3, n'en
sont pas vraiment.

## Le gestionnaire `uv` pour Python

```shell
$ uv init
Initialized project `uv-demo`
$ ls -la
total 24
drwxr-xr-x@ 6 cjauvin  staff  192 Feb 11 14:46 ./
drwxr-xr-x@ 4 cjauvin  staff  128 Feb 11 14:42 ../
-rw-r--r--@ 1 cjauvin  staff    5 Feb 11 14:46 .python-version
-rw-r--r--@ 1 cjauvin  staff   85 Feb 11 14:46 main.py
-rw-r--r--@ 1 cjauvin  staff  153 Feb 11 14:46 pyproject.toml
-rw-r--r--@ 1 cjauvin  staff    0 Feb 11 14:46 README.md
```

