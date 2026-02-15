---
title: "La gestion des dépendances"
weight: 20
---

# La gestion des dépendances

Dès qu'un programme devient un peu plus complexe, deux phénomènes interviennent
habituellement&nbsp;:

1. Le programme doit être décomposé en plusieurs modules
2. Certaines fonctionnalités du programmes, pouvant être accomplies par des
   programmes (ou des librairies) externes, doivent être détachées en des
   composantes ou des librairies distinctes, qu'il est possible de réutiliser
   (c'est un peu le [principe
   DRY](../module2/principes#dry-dont-repeat-yourself-ne-vous-répétez-pas-) que
   nous avons vu, appliqué dans le sens plus large d'un écosystème logiciel)

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
programmes compatibles avec Ubuntu 24.04. Un aspect important des systèmes de
gestion de ce genre est que les dépendances ne sont pas des objets atomiques et
isolées : en général une dépendance est liée à une autre, ce qui forme un graphe
de dépendances, qu'on dit transitives, ou récursives (si `X` dépend de `Y` qui
dépend de `Z`, alors `X` dépend de `Z`, de manière transitive). Donc non
seulement la compatibilité des versions est gérée au niveau du système global,
mais aussi entre les paquets (programmes ou librairies, entre eux). Si par
exemple l'installation de la version 7 de LibreOffice nécessite une version
particulière de Java, le gestionnaire de paquets gérera les dépendances
intelligemment, et automatiquement.

Par exemple on peut voir le graphe de dépendances du paquet `sl` sur Ubuntu,
en utilisant l'utilitaire `apt-rdepends` :

```shell
$ apt-rdepends sl
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
sl
  Depends: libc6 (>= 2.2.5)
  Depends: libncurses6 (>= 6)
  Depends: libtinfo6 (>= 6)
libc6
  Depends: libgcc-s1
libgcc-s1
  Depends: gcc-14-base (= 14.2.0-4ubuntu2~24.04)
  Depends: libc6 (>= 2.35)
gcc-14-base
libncurses6
  Depends: libc6 (>= 2.34)
  Depends: libtinfo6 (= 6.4+20240113-1ubuntu2)
libtinfo6
  Depends: libc6 (>= 2.34)
  ```

{{< image src="sl-deps.png" alt="" title="" loading="lazy" >}}

## La sécurité

Les gestionnaires de paquets jouent aujourd’hui un rôle central dans le
développement logiciel, mais ils introduisent également des enjeux importants de
sécurité. Lorsqu’un projet déclare une dépendance, il ne fait pas seulement
confiance à une bibliothèque précise, mais aussi à l’ensemble de ses dépendances
transitives, parfois très nombreuses, ainsi qu’aux personnes et aux
infrastructures qui les distribuent. Cette situation élargit considérablement la
surface d’attaque potentielle : un paquet compromis, un mainteneur malveillant,
une prise de contrôle d’un compte ou encore une simple faute de frappe dans le
nom d’une librairie (typosquatting) peuvent entraîner l’intégration de code
hostile dans un système sans que l’équipe de développement ne s’en aperçoive
immédiatement. Pour répondre à ces risques, les écosystèmes modernes proposent
divers mécanismes comme les audits automatiques de vulnérabilités connues, les
signatures cryptographiques, la vérification d’intégrité et la production
d’inventaires de composants (SBOM). Comprendre ces mécanismes fait désormais
partie des compétences essentielles du génie logiciel, car la gestion des
dépendances n’est plus seulement une question de commodité, mais aussi de
responsabilité opérationnelle et parfois légale. Les gestionnaires de
dépendances permettent

## Le versionnage sémantique (SemVer)

Au fil du temps et de l'évolution de la culture du développement logiciel, le
versionnage dit _sémantique_ (SemVer) s'est imposé en tant que convention pour
numéroter les versions d'un logiciel, que ce soit un programme ou une librairie.

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

{{< image src="versions.png" alt="" title="" loading="lazy" >}}

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
transition a entraînée. En fait il est très probable que Python ne passe jamais
à la version 4, étant donné son historique et sa position centrale dans de
nombreux écosystèmes technologiques (web, IA, calcul scientifique, etc).

La notion de versionnage sémantique est tellement importante et omniprésente
qu'elle a de l'influence à l'extérieur de la sphère du développement logiciel.
On parlera ainsi de la Playstation 5, de la Mazda 3, etc. Même des choses qui
pourraient à priori ressembler à du logiciel, comme le [Web
2.0](https://fr.wikipedia.org/wiki/Web_2.0) et le
[Web3](https://fr.wikipedia.org/wiki/Web3), n'en sont pas vraiment, ils sont
plus des "évolutions culturelles et technologiques".

## La reproductibilité

Comme on le verra avec git, le code source d'une application est un objet férocement
dynamique, qui change tout le temps

L'utilisation de numéros de version a un autre avantage : elle permet d'identifier
de manière unique

## Le gestionnaire `uv` pour Python

Pour explorer concrètement ces idées, nous allons utiliser le gestionnaire de
librairies `uv`, pour Python. `uv` est un outil très intéressant, car il est
apparu relativement tard dans l'histoire de Python (en 2024), à la suite d'une
longue lignée d'outils du même genre : `pipenv`, `poetry`, etc. Ces outils ne
doivent pas être confondus avec `pip`, qui est l'outil de base dans la
distribution Python, qui est moins puissant que les gestionnaires de
dépendances, dont il sera question ici. `uv` est apparu au bon moment, avec les
bonnes caractéristiques : extrêmement rapide (il est écrit lui-même dans le
langage Rust), avec une implémentation très complète et flexible des standards
de l'écosystème de packaging pour Python, qui ont pris un long moment avant de
maturer. Pendant de nombreuses années, la gestion du packaging en Python était
considéré un sujet pénible et beaucoup de controverse existait. L'apparition de
`uv` a introduit une certaine sérénité dans la culture de Python.

### La librairie `my-lib`

Nous allons tout d'abord créer, avec `uv`, une petite librairie simple, qui
n'offrira qu'une seule fonction&nbsp;:

```shell
$ uv init --lib my-lib
Initialized project `my-lib` at `.../uv-demo2/my-lib`
```

La structure initiale de notre nouveau projet de librairie devrait ressembler à
ceci :

```
my-lib/
├── pyproject.toml
├── src/
│   └── my_lib/
│       └── __init__.py
```

`uv` a créé la structure de notre librairie, mais il n'a évidemment pas fourni
le code qu'on veut y offrir, qu'il nous faut définir nous-même, dans le fichier
`src/my_lib/secret.py` (qui doit être créé) :

```python
def get_secret_number():
   return 42
```

Le projet ressemble donc maintenant à ceci :

```
my-lib/
├── pyproject.toml
├── src/
│   └── my_lib/
│       ├── __init__.py
│       └── secret.py      ← contient notre fonction get_secret_number
```

On peut tout d'abord tester notre librairie avec cette commande :

```shell
$ cd my-lib
$ uv run python -c 'from my_lib.secret import get_secret_number; print(get_secret_number())'
42
```

On doit ensuite produire un artefact de type `wheel`, qui va contenir la totalité
de notre librairie, en un seul fichier `.whl` (qu'il sera possible d'installer dans un
autre projet)&nbsp;:

```shell
$ cd my-lib
$ uv build --out-dir ../packages
Building source distribution (uv build backend)...
Building wheel from source distribution (uv build backend)...
Successfully built ../packages/my_lib-0.1.0.tar.gz
Successfully built ../packages/my_lib-0.1.0-py3-none-any.whl
```

Voici maintenant où nous en sommes&nbsp;:
```shell
$ tree
.
├── my-lib
│   ├── pyproject.toml
│   ├── README.md
│   ├── src
│   │   └── my_lib
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-313.pyc
│   │       │   └── secret.cpython-313.pyc
│   │       ├── py.typed
│   │       └── secret.py
│   └── uv.lock
└── packages
    ├── my_lib-0.1.0-py3-none-any.whl
    └── my_lib-0.1.0.tar.gz

6 directories, 10 files
```

{{< image src="mylib.png" alt="" title="" loading="lazy" >}}

### L'application `my-app` (qui utilise la librairie `my-lib`)

Créons maintenant un nouveau projet avec `uv`, d'une application cette fois, que
nous appellerons `my-app` :

```shell
$ cd ..  # on doit être au même niveau que my-lib
$ uv init my-app
Initialized project `my-app` at `.../uv-demo2/my-app`
```

Étant donné que `my-app` devra utiliser le code de la librairie `my-lib`, nous
voudrons y ajouter une dépendance vers notre librairie `my-lib`. Mais tout
d'abord, étant donné que ceci est un exercice d'apprentissage, nous devons
modifier notre configuration quelque peu, en ajoutant le bloc `[tool.uv]` qui
contient deux lignes supplémentaires, à notre fichier `my-app/pyproject.toml` :

```toml {hl_lines="9-11"}
[project]
name = "my-app"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []

[tool.uv]
no-index = true
find-links = ["../packages"]
```

Ces deux lignes sont très importantes dans notre contexte :

1. `no-index` empêche `uv` d'aller chercher `my-lib` sur le dépôt public [PyPI](https://pypi.org), qui contient déjà apparemment une [librairie avec ce nom](https://pypi.org/project/my-lib/). Nous voulons que `uv` utilise notre version locale de `my-lib`, que nous avons sur notre propre disque
2. `find-links` indique le lieu où `uv` devra trouver les fichiers "wheels", qui sont des sortes de "zip" d'une librairie entière, optimisée pour un système particulier

Une fois cette configuration effectuée, on peut ajouter notre dépendance avec `uv add` :

```shell
$ cd my-app
$ uv add my-lib
Using CPython 3.13.5
Creating virtual environment at: .venv
Resolved 2 packages in 26ms
Prepared 1 package in 4ms
Installed 1 package in 3ms
 + my-lib==0.1.0
```

On peut constater l'état du projet de notre application avec cette commande :

```shell
$ uv tree
Resolved 2 packages in 3ms
my-app v0.1.0
└── my-lib v0.1.0
```

Tout comme nous l'avons fait pour `my-lib`, c'est à nous qu'incombe la
responsabilité de fournir le code source pour l'application, qui sera très
simple. Dans le fichier `my-app/main.py` (qui a été créé automatiquement par `uv`
puisqu'il s'agissait d'une application), nous devons remplacer le contenu par :

```python
from my_lib.secret import get_secret_number

def main():
    print(f"The secret number is: {get_secret_number()}")

if __name__ == "__main__":
    main()
```

On peut maintenant tester notre application :

```shell
$ cd my-app
$ uv run main.py
The secret number is: 42
```

{{< image src="mylib+myapp.png" alt="" title="" loading="lazy" >}}

Maintenant regardons attentivement notre fichier `my-app/pyproject.toml` :

```toml {hl_lines="7-9"}
[project]
name = "my-app"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "my-lib>=0.1.0",
]

[tool.uv]
no-index = true
find-links = ["../packages"]
```

On note que `my-app` définie sa dépendance à `my-lib` en spécifiant : n'importe quelle
version de `my-lib` dont la version est plus grande ou égale à `0.1.0`. Ceci peut
être dangereux, car que se passerait-il dans le cas où une nouvelle version de `my-lib`
serait publiée, et qu'elle contiendra des changements qui feraient en sorte de modifier
le comportement de `my-app`? Soyons plus conservateur en fixant plus précisément notre
limite de version pour `my-lib` :

```shell
$ uv add "my-lib>=0.1.0,<0.2.0"
Resolved 2 packages in 7ms
Audited 1 package in 0.28ms
```

On peut maintenant constater l'effet de cette précision dans notre même fichier
`my-app/pyproject.toml` :

```toml {hl_lines="7-9"}
[project]
name = "my-app"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "my-lib>=0.1.0,<0.2.0",
]

[tool.uv]
no-index = true
find-links = ["../packages"]
```

La version de `my-lib` pour `my-map` est "pinnée" (mot anglais) à `0.1.x`, ce
qui veut donc dire que seules les versions avec des "patchs" différents (pour la
résolution de bogues, en général) seront tolérées : par exemple `0.1.1`,
`0.1.2`, etc. La version `0.2.0`, si elle en venait à exister, serait
"interdite" par le gestionnaire `uv` (remarquez bien l'usage de `<0.2.0`, et
non `<=0.2.0`).

### La librairie `my-lib` évolue

Imaginons maintenant que la librairie `my-lib` évolue, et que la fonction
offerte change : par exemple, au lieu d'être 42, le nombre magique devient 99.
Modifions tout d'abord le code de `my-lib/src/secret.py` :

```python
def get_secret_number():
    return 99
```

Ensuite incrémentons la version de `my-lib` :

```shell
$ cd my-lib
$ uv version --bump minor  # 0.1.0 -> 0.2.0
Resolved 1 package in 16ms
      Built my-lib @ file:///Users/cjauvin/gh/inf1410-teluq/content/docs/module3/gestion-de
Prepared 1 package in 7ms
Uninstalled 1 package in 0.67ms
Installed 1 package in 1ms
 - my-lib==0.1.0 (from file:///Users/cjauvin/gh/inf1410-teluq/content/docs/module3/gestion-des-deps/uv-demo3/my-lib)
 + my-lib==0.2.0 (from file:///Users/cjauvin/gh/inf1410-teluq/content/docs/module3/gestion-des-deps/uv-demo3/my-lib)
my-lib 0.1.0 => 0.2.0
```

On peut constater dans notre fichier `my-lib/pyproject.toml` que le changement a
été fait :

```toml {hl_lines="3"}
[project]
name = "my-lib"
version = "0.2.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Christian Jauvin", email = "cjauvin@gmail.com" }
]
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["uv_build>=0.8.22,<0.9.0"]
build-backend = "uv_build"
```

On peut maintenant "builder" notre librairie afin d'en produire un artefact de type
"wheel" pour la nouvelle version `0.2.0`, comme nous avons fait pour la précédente
version `0.1.0` :

```shell
$ uv build --out-dir ../packages
Building source distribution (uv build backend)...
Building wheel from source distribution (uv build backend)...
Successfully built ../packages/my_lib-0.2.0.tar.gz
Successfully built ../packages/my_lib-0.2.0-py3-none-any.whl
```

On constate donc la présence du fichier `../packages/my_lib-0.2.0-py3-none-any.whl`, qui
contient la totalité de notre librairie, prête à être installée dans le contexte de
n'importe quel projet, par `uv`.

### L'application `my-app` devrait donc évoluer elle aussi !

Retournons maintenant à `my-app`. Si on tente de la mettre à jour :

```shell
$ uv sync --upgrade
Resolved 2 packages in 17ms
Audited 1 package in 0.28ms
```

{{< image src="myapp1.png" alt="" title="" loading="lazy" >}}

Rien ne se passe, car bien que `my-lib` version `0.2.0` soit disponible, la
configuration de `my-app` ne lui permet pas d'utiliser une version aussi élevée.
Pour changer cela, on peut utiliser la commande :

```shell
uv add "my-lib>=0.1.0,<=0.2.0"
Resolved 2 packages in 17ms
Audited 1 package in 0.23ms
```

qui devrait maintenant permettre de faire en sorte de laisser passer la version `0.2.0`
de `my-lib` :

```shell
$ uv sync --upgrade
Resolved 2 packages in 26ms
Prepared 1 package in 0.78ms
Uninstalled 1 package in 1ms
Installed 1 package in 1ms
 - my-lib==0.1.0
 + my-lib==0.2.0
```

On peut constater l'effet de cette mise à niveau de `my-lib`, sur notre
application elle-même :

```shell
$ uv run main.py
The secret number is: 99
```

Finalement, étant donné ce changement de comportement important, et pour éviter
de confondre les utilisateurs, on va vouloir mettre à jour la version de
`my-app` elle-même :

```shell
$ uv version --bump major
Resolved 2 packages in 7ms
Audited 1 package in 0.25ms
my-app 0.1.0 => 1.0.0
```

Dans ce cas étant donné qu'il s'agit d'une application, nous avons choisi de
changer la version majeure, qui passe donc à `1.0.0`.

{{< image src="myapp2.png" alt="" title="" loading="lazy" >}}
