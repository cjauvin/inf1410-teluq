---
title: "La gestion des dépendances"
slug: "gestion-des-deps"
weight: 40
---

# La gestion des dépendances

Dès qu'un programme devient un peu plus complexe, deux phénomènes interviennent
habituellement&nbsp;:

1. Le programme doit être décomposé en plusieurs modules
2. Certaines fonctionnalités du programmes, pouvant être accomplies par des
   programmes (ou des bibliothèques) externes, doivent être détachées en des
   composantes ou des bibliothèques distinctes, qu'il est possible de réutiliser
   (c'est un peu le [principe
   DRY]({{< ref "/docs/principes#dry-dont-repeat-yourself-ne-vous-répétez-pas" >}}) que
   nous avons vu, appliqué dans le sens plus large d'un écosystème logiciel)

Dans le cas (2), on nomme parfois les bibliothèques externes des "dépendances", ou des
"paquets" (packages en anglais, plus communément).

Dans les débuts de l'ingénierie logicielle, ces dépendances étaient gérées à la
main, en copiant et échangeant des fichiers.

Avec l'apparition de Linux au début des années 90, une innovation importante
allait vite apparaître : les gestionnaire de paquets. Des exemples fameux sont
[APT](https://fr.wikipedia.org/wiki/Advanced_Packaging_Tool) pour les
distributions Debian et Ubuntu de Linux, et
[RPM](https://fr.wikipedia.org/wiki/RPM_Package_Manager) pour d'autres
distributions comme Red Hat, Fedora, etc.

Ces paquets sont en général des programmes et des bibliothèques qui sont
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
mais aussi entre les paquets (programmes ou bibliothèques, entre eux). Si par
exemple l'installation de la version 7 de LibreOffice nécessite une version
particulière de Java, le gestionnaire de paquets gérera les dépendances
intelligemment, et automatiquement.

Par exemple on peut voir le graphe de dépendances du paquet `sl` sur Ubuntu Linux,
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

## Le versionnage sémantique (SemVer)

Au fil du temps et de l'évolution de la culture du développement logiciel, le
versionnage dit _sémantique_ (SemVer) s'est imposé en tant que convention pour
numéroter les versions d'un logiciel, que ce soit un programme ou une bibliothèque.

{{< image src="semver.png" alt="" title="" loading="lazy" >}}

Bien que l'interprétation ne soit pas toujours identique, en général on
s'accorde pour dire que la composante "majeure" du numéro de version correspond
à un changement important, qui "brise" la compatibilité avec les versions
précédentes (s'il y en a). S'il s'agit d'une bibliothèque logicielle par exemple,
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
logiciel ou une bibliothèque ne peut pas être considérée _stable_ tant qu'elle n'a
pas atteint au moins la version `1.0.0`. Certains projets restent d'ailleurs
indéfiniment dans un schéma de versions `0.x.y`, afin d'échapper à une certaine
pression sociale, et ainsi pouvoir conserver une certaine liberté créative et
d'action.

Il est à noter que pour les langages de programmation (qui sont à la fois des
programmes et des bibliothèques), la question du numéro de version est
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

## Le gestionnaire `uv` pour Python

Pour explorer concrètement ces idées, nous allons utiliser le gestionnaire de
bibliothèques `uv`, pour Python. `uv` est un outil très intéressant, car il est
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

### La bibliothèque `my-lib`

Nous allons tout d'abord créer, avec `uv`, une petite bibliothèque simple, qui
n'offrira qu'une seule fonction&nbsp;:

```shell
$ uv init --lib my-lib
Initialized project `my-lib` at `.../uv-demo2/my-lib`
```

La structure initiale de notre nouveau projet de bibliothèque devrait ressembler à
ceci :

```
my-lib/
├── pyproject.toml
├── src/
│   └── my_lib/
│       └── __init__.py
```

`uv` a créé la structure de notre bibliothèque, mais il n'a évidemment pas fourni
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

On peut tout d'abord tester notre bibliothèque avec cette commande :

```shell
$ cd my-lib
$ uv run python -c 'from my_lib.secret import get_secret_number; print(get_secret_number())'
42
```

On doit ensuite produire un artefact de type `wheel`, qui va contenir la totalité
de notre bibliothèque, en un seul fichier `.whl` (qu'il sera possible d'installer dans un
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

### L'application `my-app` (qui utilise la bibliothèque `my-lib`)

Créons maintenant un nouveau projet avec `uv`, d'une application cette fois, que
nous appellerons `my-app` :

```shell
$ cd ..  # on doit être au même niveau que my-lib
$ uv init my-app
Initialized project `my-app` at `.../uv-demo2/my-app`
```

Étant donné que `my-app` devra utiliser le code de la bibliothèque `my-lib`, nous
voudrons y ajouter une dépendance vers notre bibliothèque `my-lib`. Mais tout
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

1. `no-index` empêche `uv` d'aller chercher `my-lib` sur registre de paquets public [PyPI](https://pypi.org), qui contient déjà apparemment une [bibliothèque avec ce nom](https://pypi.org/project/my-lib/). Nous voulons que `uv` utilise notre version locale de `my-lib`, que nous avons sur notre propre disque
2. `find-links` indique le lieu où `uv` devra trouver les fichiers "wheels", qui sont des sortes de "zip" d'une bibliothèque entière, optimisée pour un système particulier

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

#### La notion de registre de paquets (PyPI)

Nous avons brièvement mentionné ci-haut la notion de _registre de paquets_.
Étant donné que nous voulions utiliser notre propre bibliothèque `my-lib`, et non
celle qui se trouve en ligne, nous avons dû spécifier `no-index = true` dans la
configuration `pyproject.toml` de notre projet. Que se serait-il passé, sans
cette instruction particulière? `uv` est configuré, par défaut, pour fonctionner
avec le registre en ligne et officiel [PyPI](https://pypi.org), qui est un
endroit public où il est possible de télécharger et publier des paquets.
Explorons cette notion en créant un nouveau projet avec `uv` :

```shell
$ cd ..  # on ne doit pas être dans le répertoire d'un projet existant
$ uv init my-venv
Initialized project `my-venv` at `/Users/cjauvin/gh/inf1410-teluq/content/docs/module3/gestion-des-deps/uv-demo3/my-venv`
```

Ajoutons une dépendance vers la bibliothèque [requests](https://pypi.org/project/requests/),
qui permet de faire des requêtes HTTP (web) en python :

```shell
$ cd my-venv
$ uv add requests
Using CPython 3.13.5
Creating virtual environment at: .venv
Resolved 6 packages in 183ms
Installed 5 packages in 4ms
 + certifi==2026.1.4
 + charset-normalizer==3.4.4
 + idna==3.11
 + requests==2.32.5
 + urllib3==2.6.3
```

On constate trois choses :

1. `uv` a téléchargé automatiquement la bibliothèque `requests` de PyPI, sans que l'ait rien configuré
2. La bibliothèque `requests` elle-même nécessite quelques dépendances additionnelles (des dépendances transitives donc) : `certifi`, `charset-normalizer`, etc.
3. Apparemment un "environnement virtuel" a été créé, dans le répertoire `.venv` de notre projet

Qu'est-ce qu'un environnement virtuel donc?

#### La notion d'environnement virtuel (virtual env, ou `venv`)

En fait une question reliée serait : qu'est-ce qu'un projet `uv`, au juste?
Quand j'ajoute une dépendance dans mon projet, quel est l'effet concret, et
comment puis-le constater? Voyons voir le contenu du répertoire du projet
dans lequel nous venons d'installer une dépendance :

```shell
$ cd my-venv
$ ls -la
total 24
drwxr-xr-x@ 8 cjauvin  staff  256 Feb 16 17:13 ./
drwxr-xr-x@ 5 cjauvin  staff  160 Feb 16 17:14 ../
-rw-r--r--@ 1 cjauvin  staff    5 Feb 12 14:55 .python-version
drwxr-xr-x@ 8 cjauvin  staff  256 Feb 12 14:58 .venv/
-rw-r--r--@ 1 cjauvin  staff  358 Feb 16 17:12 pyproject.toml
-rw-r--r--@ 1 cjauvin  staff    0 Feb 12 14:55 README.md
drwxr-xr-x@ 3 cjauvin  staff   96 Feb 12 14:55 src/
-rw-r--r--@ 1 cjauvin  staff  254 Feb 16 17:13 uv.lock
```

On constate un répertoire particulier, appelé `.venv` : il s'agit d'un
environnement virtuel (souvent appelé `venv`), un endroit particulier sur le
disque qui contient :

1. Une version particulière de l'interpréteur Python (par exemple la version
   3.13, dans cet exemple), ainsi qu'une série d'utilitaires reliés
2. Une série de paquets (packages) qui ont été installés dans le venv (dans le
   contexte de ce projet, un seul a été installé : `requests`)

Il est crucial de savoir et de comprendre que les paquets installés dans un venv
particulier fonctionnent exclusivement dans le contexte de l'interpréteur python
particulier, installé dans ce venv. On peut s'en convaincre avec cette commande :

```shell
$ ll .venv/lib/python3.13/site-packages/
total 24
-rw-r--r--@  1 cjauvin  staff    18B Feb 17 15:46 _virtualenv.pth
-rw-r--r--@  1 cjauvin  staff   4.2K Feb 17 15:46 _virtualenv.py
drwxr-xr-x@  7 cjauvin  staff   224B Feb 17 15:46 certifi/
drwxr-xr-x@  9 cjauvin  staff   288B Feb 17 15:46 certifi-2026.1.4.dist-info/
drwxr-xr-x@ 16 cjauvin  staff   512B Feb 17 15:46 charset_normalizer/
drwxr-xr-x@ 10 cjauvin  staff   320B Feb 17 15:46 charset_normalizer-3.4.4.dist-info/
drwxr-xr-x@ 11 cjauvin  staff   352B Feb 17 15:46 idna/
drwxr-xr-x@  8 cjauvin  staff   256B Feb 17 15:46 idna-3.11.dist-info/
drwxr-xr-x@ 20 cjauvin  staff   640B Feb 17 15:46 requests/
drwxr-xr-x@  9 cjauvin  staff   288B Feb 17 15:46 requests-2.32.5.dist-info/
drwxr-xr-x@ 18 cjauvin  staff   576B Feb 17 15:46 urllib3/
drwxr-xr-x@  8 cjauvin  staff   256B Feb 17 15:46 urllib3-2.6.3.dist-info/
```

Ceci permet un mécanisme d'isolation, qui permet d'éviter les conflits et les
problèmes de compatibilité entre les composantes. Par exemple, si un script de
traitement de données utilise la version 1 de `numpy`, on peut le rouler dans un
venv dont la version de `numpy` est gardée exclusivement à cette version. Si un
autre script utilise la version 2, il peut rouler dans son propre venv. Il est
en de même pour la version de l'interpréteur python utilisée, qui peut varier de
venv en venv, elle aussi.

{{< image src="two-venvs.png" alt="" title="" loading="lazy" >}}

> [!NOTE]
Chaque fois qu'une commande `uv` est exécutée, elle l'est dans le contexte d'un
venv particulier. Si le venv n'existe pas, il sera créé pour l'occasion.

#### La notion de reproductibilité (`uv.lock`)

Un autre fichier qu'il est intéressant de considérer dans notre projet est
`uv.lock`. Ce fichier (qu'on appelle parfois un "lockfile") contient la liste
des dépendances du projet, sous la forme de métadonnées précises et exactes,
permettant de reconstruire de manière parfaite et exhaustive le contenu d'un
venv particulier (c'est une manière de le copier donc, en le reproduisant avec
une recette). Chaque dépendance y est figée dans le temps, à l'aide
d'identifiants et de urls non-ambigus, qui permettent de faire en sorte de
réinstaller exactement le même environnement, dans un endroit différent. Quand
le projet vient d'être créé, `uv.lock` est vide. Mais dans notre cas, étant
donné que nous avons ajouté `requests` au projet, on peut constater, en
l'examinant, qu'il contient une série de références précises vers les artefacts
en ligne des packages correspondant :

```shell
$ cd my-venv
$ cat uv.lock
version = 1
revision = 3
requires-python = ">=3.13"

[[package]]
name = "certifi"
version = "2026.1.4"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/e0/2d/a891ca51311197f6ad14a7ef42e2399f36cf2f9bd44752b3dc4eab60fdc5/certifi-2026.1.4.tar.gz", hash = "sha256:ac726dd470482006e014ad384921ed6438c457018f4b3d204aea4281258b2120", size = 154268, upload-time = "2026-01-04T02:42:41.825Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/e6/ad/3cc14f097111b4de0040c83a525973216457bbeeb63739ef1ed275c1c021/certifi-2026.1.4-py3-none-any.whl", hash = "sha256:9943707519e4add1115f44c2bc244f782c0249876bf51b6599fee1ffbedd685c", size = 152900, upload-time = "2026-01-04T02:42:40.15Z" },
]
...
```

Cette notion de reproductibilité est extrêmement importante dans les
environnements de production, où certaines composantes logicielles sont parfois
installées à répétition, de manière scriptée et automatisée, dans des
environnements éphémères, comme des containers (docker ou autre), dans un
système Kubernetes, ou un environnement pour effectuer des tests.

Mais que se passerait-il si, au lieu d'installer la bibliothèque `requests`,
nous tentions d'installer, par mégarde, `request` (sans `s`)?

```shell
$ uv add request
  × No solution found when resolving dependencies:
  ╰─▶ Because request was not found in the package registry and your project depends on request, we can
      conclude that your project's requirements are unsatisfiable.
  help: If you want to add the package regardless of the failed resolution, provide the `--frozen` flag
        to skip locking and syncing.
```

Dans ce cas, le comportement souhaité est le bon : PyPI ne reconnaît pas le nom
de cette bibliothèque, et qui plus est, PyPI ne permettrait pas à quelqu'un de
publier une bibliothèque dont le nom serait trop proche d'une bibliothèque très
connue (`requests` est extrêmement populaire). Mais cette protection a ses
limites, et les registres de paquets restent vulnérables à plusieurs types
d'attaques. Nous y reviendrons en détail dans la section sur la sécurité, à la
fin de ce chapitre.

---

Après ces détours, revenons maintenant à notre application `my-app` : tout comme
nous l'avons fait pour la bibliothèque `my-lib`, c'est à nous qu'incombe la
responsabilité de fournir le code source pour l'application, qui sera très
simple. Dans le fichier `my-app/main.py` (qui a été créé automatiquement par
`uv` puisqu'il s'agissait d'une application), nous devons remplacer le contenu
par :

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

On note que `my-app` définie sa dépendance à `my-lib` en utilisant une syntaxe
particulière : `my-lib>=0.1.0`, ce qui signifie évidemment : n'importe quelle
version de `my-lib` dont la version est plus grande ou égale à `0.1.0`. Ceci peut
être dangereux, car que se passerait-il dans le cas où une nouvelle version de `my-lib`
serait publiée, et qu'elle contiendra des changements qui feraient en sorte de modifier
le comportement de `my-app`? Soyons plus conservateur en fixant plus précisément notre
limite de version pour `my-lib`. Pour ce faire, on va utiliser de nouveau cette syntaxe
particulière :

```shell
$ uv add "my-lib>=0.1.0,<0.2.0"
Resolved 2 packages in 7ms
Audited 1 package in 0.28ms
```

> [!NOTE]
Avec `uv`, les contraintes de version servent à indiquer quelles versions d’un paquet peuvent être installées. Les opérateurs classiques `<`, `<=`, `>`, `>=` permettent de fixer des bornes (par exemple `>=1.2.0` signifie « version 1.2.0 ou supérieure »), tandis que `==` impose une version exacte. `uv` suit la spécification PEP 440 de l’écosystème Python : l’opérateur `~=` (compatible release) autorise les mises à jour compatibles selon la version indiquée (par exemple `~=1.4` accepte les versions `1.x` à partir de `1.4`, sans passer à `2.0`). Ces contraintes permettent de contrôler finement la stabilité d’un projet tout en autorisant, si souhaité, certaines mises à jour automatiques lors du verrouillage (uv lock).

> [!NOTE]
La commande `uv add "my-lib~=0.1.0"` serait ici équivalent à `uv add "my-lib>=0.1.0,<0.2.0"`.

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

La version de `my-lib` pour `my-app` est "pinnée" (mot anglais) à `0.1.x`, ce
qui veut donc dire que seules les versions avec des "patchs" différents (pour la
résolution de bogues, en général) seront tolérées : par exemple `0.1.1`,
`0.1.2`, etc. La version `0.2.0`, si elle en venait à exister, serait
"interdite" par le gestionnaire `uv` (remarquez bien l'usage de `<0.2.0`, et
non `<=0.2.0`).

### La bibliothèque `my-lib` évolue

Imaginons maintenant que la bibliothèque `my-lib` évolue, et que la fonction
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

On peut maintenant "builder" notre bibliothèque afin d'en produire un artefact de type
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
contient la totalité de notre bibliothèque, prête à être installée dans le contexte de
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

## La sécurité de la chaîne d'approvisionnement

Tout au long de cette section, nous avons vu comment un gestionnaire de
dépendances permet d'assembler rapidement un projet à partir de composantes
externes. Mais cette commodité repose sur un acte de confiance implicite :
lorsqu'on exécute `uv add requests`, on ne fait pas seulement confiance à la
bibliothèque `requests` elle-même, mais aussi à `certifi`, `charset-normalizer`,
`idna` et `urllib3`, à leurs propres mainteneurs, et aux infrastructures qui les
hébergent et les distribuent. Plus un projet accumule de dépendances, plus cet
arbre de confiance s'élargit, et plus la surface d'attaque potentielle grandit.
Cette réalité a donné naissance à une catégorie de menaces qu'on appelle les
attaques de la chaîne d'approvisionnement logicielle (supply chain attacks).

Le principe d'une supply chain attack est d'exploiter la confiance que les
développeurs accordent à leur chaîne d'approvisionnement logicielle, plutôt que
d'attaquer directement le système visé. Au lieu de chercher une faille dans
l'application elle-même, l'attaquant compromet une de ses dépendances, souvent
plusieurs niveaux en profondeur dans l'arbre de dépendances transitives. Le code
malicieux est alors installé automatiquement par le gestionnaire de paquets,
parfois sans que personne ne le remarque pendant des semaines ou des mois. Les
vecteurs d'attaque les plus courants sont le typosquattage (publier un paquet
dont le nom ressemble à un paquet populaire), la prise de contrôle du compte
d'un mainteneur, et l'infiltration progressive d'un projet open source par un
contributeur qui gagne la confiance de l'équipe avant d'y injecter du code
hostile.

Plusieurs incidents majeurs ont marqué l'histoire récente du développement
logiciel et illustrent bien la diversité de ces attaques. En 2018, le paquet npm
`event-stream`, téléchargé des millions de fois par semaine, a été compromis
d'une manière particulièrement révélatrice. Le mainteneur original, épuisé par
des années de travail bénévole sur un projet qu'il n'utilisait même plus, a
accepté de transférer le contrôle du paquet à un inconnu qui s'était montré
serviable. Ce nouveau mainteneur a ensuite ajouté une dépendance vers un autre
paquet, `flatmap-stream`, qui contenait du code obfusqué conçu pour voler les
portefeuilles de Bitcoin des utilisateurs d'une application spécifique. L'attaque
est restée invisible pendant plusieurs semaines, car le code malicieux était
caché dans un paquet transitif et ne se déclenchait que dans un contexte très
précis.

Un exemple encore plus récent et particulièrement frappant est celui de LiteLLM,
une bibliothèque Python très populaire (des millions de téléchargements par
jour) servant de passerelle vers différents modèles d'IA. En mars 2026, un
groupe appelé TeamPCP a réussi une attaque en cascade d'une sophistication
remarquable. Ils ont d'abord compromis Trivy, un outil d'analyse de sécurité,
qui était justement utilisé dans le pipeline CI/CD de LiteLLM. L'ironie est
frappante : c'est un outil de sécurité qui a servi de vecteur d'attaque. En
s'exécutant dans le pipeline de compilation de LiteLLM, le Trivy compromis a
exfiltré le jeton de publication PyPI du projet, permettant aux attaquants de
publier deux versions malicieuses de LiteLLM sur PyPI. Ces versions installaient
un mécanisme qui, à chaque démarrage de Python, récoltait silencieusement les
clés API, les secrets, les identifiants de bases de données et les clés SSH
présents sur la machine. Les versions compromises n'ont été en ligne que pendant
environ 40 minutes avant d'être retirées par PyPI, mais étant donné le volume de
téléchargements, l'impact potentiel était considérable. Fait notable : les
utilisateurs qui avaient des dépendances verrouillées dans un fichier de type
lockfile n'ont pas été affectés.

Mais l'attaque de la chaîne d'approvisionnement la plus spectaculaire des
dernières années est sans doute celle qui a visé xz Utils en 2024, un petit
utilitaire de compression présent dans pratiquement toutes les distributions
Linux. Un développeur utilisant le pseudonyme Jia Tan a commencé à contribuer au
projet en 2021, de manière patiente et méthodique. Pendant plus de deux ans, il
a soumis des correctifs légitimes, gagné la confiance du mainteneur principal
(qui, comme dans le cas d'event-stream, était une personne seule et débordée),
et obtenu progressivement les droits de publication. En février 2024, il a
injecté une porte dérobée (backdoor) extrêmement sophistiquée, dissimulée dans
les fichiers de test du projet, qui permettait à un attaquant distant de prendre
le contrôle de n'importe quel serveur utilisant OpenSSH avec la bibliothèque
compromise. La backdoor a été découverte par hasard, par un ingénieur de
Microsoft qui avait remarqué que ses connexions SSH prenaient une demi-seconde de
plus que d'habitude. Sans cette observation fortuite, la porte dérobée aurait pu
se retrouver dans des millions de serveurs à travers le monde.

Ces exemples illustrent un thème commun : la sécurité de la chaîne
d'approvisionnement est autant un problème humain et social que technique. Les
mainteneurs solitaires et épuisés, les comptes mal protégés et les pipelines
CI/CD trop permissifs sont des vecteurs d'attaque au moins aussi importants que
les failles de code. Plusieurs des outils que nous avons vus dans ce chapitre
jouent un rôle défensif direct : les lockfiles permettent de figer les versions
exactes des dépendances et d'éviter qu'une mise à jour malicieuse soit installée
automatiquement, les contraintes de version SemVer limitent l'exposition aux
changements inattendus, et les registres comme PyPI mettent en place des
protections contre le typosquattage et exigent de plus en plus l'authentification
à deux facteurs pour les mainteneurs de paquets populaires. Au-delà de ces
mécanismes, des pratiques comme l'audit régulier des dépendances (`uv audit`,
`npm audit`), la production d'inventaires de composants (SBOM, pour Software
Bill of Materials) et la vérification des signatures cryptographiques font
aujourd'hui partie des compétences attendues en génie logiciel.

<!-- ILLUSTRATION: schéma montrant les différents vecteurs d'attaque sur la chaîne d'approvisionnement (typosquattage, compte compromis, dépendance transitive malicieuse, pipeline CI/CD infiltré) -->

# Pas seulement pour Python !

Tout ce que nous avons dit et expliqué à propos de `uv` et python s'applique
également à d'autres langages et leur écosystème :

1. JavaScript avec Node et NPM
2. Rust et Cargo
3. Java avec Maven ou Gradle
4. Go avec go mod
5. .NET (C#, etc) et NuGet
6. Perl et CPAN
7. Ruby et Bundler

Pour votre culture personnelle, je vous suggère d'explorer une ou plusieurs de ces "paires",
et de tenter de répondre aux questions suivantes :

1. Est-ce qu'il y a une notion d'environnement virtuel?
2. Est-ce qu'il y a un dépôt centralisé de bibliothèques et de packages (comme PyPI)?
3. Est-ce qu'il y a un mécanisme de lockfile (comme `uv.lock`)?
4. Est-ce que SemVer y est utilisé de la même manière?
5. Est-ce les contraintes au niveau des dépendances sont exprimées de la même
   manière (avec le même "mini-langage")?
6. Est-ce qu'on y retrouve la possibilité du même genre de vulnérabilité au
   niveau de la sécurité (typosquatting, etc)?