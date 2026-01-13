---
title: "Le versioning avec git"
weight: 10
---

# Le versioning

## Quel est le problème qu'on cherche à résoudre?

Le logiciel (et le code source dont il est constitué) a une particularité
fondamentale : il change tout le temps. Même un programme simple est rapidement
modifié - pour corriger un bug, ajouter une fonctionnalité, améliorer la
performance ou simplement rendre le code plus lisible. Et très vite, une
question apparaît : comment savoir ce qui a changé, quand, et pourquoi ?

Sans système de versioning, le développement logiciel devient fragile. On copie
des fichiers, on renomme des dossiers (« version2 », « version_finale », «
version_finale_bis »), on échange du code par courriel ou sur un disque partagé.
Ces solutions fonctionnent… jusqu’au moment où elles ne fonctionnent plus : on
perd une modification importante, on ne sait plus quelle version est la bonne,
ou deux personnes écrasent mutuellement leur travail.

Le versioning n’est pas une simple sauvegarde. Sauvegarder, c’est garder une
photo du code à un instant donné. Versionner, c’est garder la mémoire de son
évolution. Un bon système de versioning permet de revenir en arrière, de
comprendre l’historique d’un projet, de travailler à plusieurs sans se gêner, et
d’expérimenter sans casser ce qui fonctionne.

À mesure que les projets grossissent et que le travail devient collectif, le
versioning devient indispensable. Il structure la façon dont on travaille, dont
on collabore, et même dont on réfléchit au code. C’est ce problème — gérer le
changement — qui a conduit à la création des systèmes de contrôle de versions,
et en particulier de Git, que nous allons étudier dans ce chapitre.

## Bref historique des systèmes de gestion de versions

### Première génération : local et fichier unique

**SCCS** (Source Code Control System, 1972) — Bell Labs
- Premier système de versioning, créé par Marc Rochkind
- Stockage par deltas (différences) pour économiser l'espace
- Un seul fichier à la fois, un seul utilisateur à la fois
- Verrouillage exclusif pour éviter les conflits

**RCS** (Revision Control System, 1982) — Walter Tichy, Purdue
- Amélioration de SCCS, plus rapide grâce aux deltas inversés (stocke la version courante en entier, reconstruit les anciennes)
- Toujours limité à des fichiers individuels
- Reste local à une machine

### Deuxième génération : centralisé et projets entiers

**CVS** (Concurrent Versions System, 1986–1990) — Dick Grune, puis Brian Berliner
- Construit au-dessus de RCS mais gère des arborescences de fichiers
- Premier système vraiment *concurrent* : plusieurs développeurs peuvent modifier simultanément
- Modèle client-serveur avec un dépôt central
- Faiblesses notoires : pas de commits atomiques, gestion pénible des renommages et des branches

**Perforce** (1995) — commercial
- Très performant sur de gros dépôts binaires
- Encore utilisé dans l'industrie du jeu vidéo et les grandes entreprises

**Subversion (SVN)** (2000) — CollabNet
- Conçu explicitement pour corriger les défauts de CVS
- Commits atomiques, versioning des répertoires, renommages suivis
- Toujours centralisé : le serveur est la source de vérité unique
- Numérotation linéaire des révisions (r1, r2, r3…)

### Troisième génération : distribué

**BitKeeper** (1998–2000) — Larry McVoy
- Premier système distribué utilisé à grande échelle (noyau Linux de 2002 à 2005)
- Licence propriétaire controversée, ce qui a mené à la création de Git

**GNU Arch / Bazaar / Darcs** (début 2000)
- Expérimentations diverses sur le versioning distribué
- Darcs introduit une approche par patches commutatifs (théorie des patches)

**Git** (2005) — Linus Torvalds
- Créé en quelques semaines après la rupture avec BitKeeper
- Objectifs : vitesse, intégrité des données, support massif des branches
- Caractéristiques clés :
 - Chaque clone est un dépôt complet avec tout l'historique
 - Stockage par snapshots (pas deltas) avec déduplication via SHA-1
 - Branches ultra-légères (simples pointeurs)
 - Travail hors ligne total
 - Modèle de staging (index) avant commit
- Devenu le standard de facto grâce à GitHub (2008)

**Mercurial** (2005) — Matt Mackall
- Lancé la même semaine que Git, mêmes motivations
- Interface plus simple, concepts similaires
- Utilisé par Facebook, Mozilla (historiquement)
- Moins dominant aujourd'hui, mais toujours actif

---

### Tableau récapitulatif

| Système | Année | Modèle | Granularité | Particularité |
|---------|-------|--------|-------------|---------------|
| SCCS | 1972 | Local | Fichier | Premier système, deltas |
| RCS | 1982 | Local | Fichier | Deltas inversés |
| CVS | 1990 | Centralisé | Projet | Accès concurrent |
| SVN | 2000 | Centralisé | Projet | Commits atomiques |
| Git | 2005 | Distribué | Projet | Snapshots, branches légères |
| Mercurial | 2005 | Distribué | Projet | Interface épurée |

L'évolution suit une logique claire : d'abord résoudre le problème du suivi pour
un fichier, puis pour un projet, puis permettre la collaboration, et enfin
décentraliser pour la résilience et la flexibilité.

## Un système de gestion des versions moderne et extrêmement populaire : git

### Fonction de hachage

Pour se faire un bon modèle mental du fonctionnement de git, il est essentiel de
bien comprendre tout d'abord la notion de **fonction de hachage**.

Une fonction de hachage est une fonction mathématique qui prend en entrée un
nombre, et qui retourne un autre nombre. Une fonction de hachage ne peut pas
être n'importe quelle fonction par contre (comme par exemple $f(x) = mx + b$),
elle doit avoir certaines caractéristiques :

* Déterminisme : Pour une même donnée en entrée, vous obtiendrez toujours exactement le même hash en sortie.

* Rapidité : Le calcul du hash doit être presque instantané.

* Effet d'avalanche : Si vous changez ne serait-ce qu'une virgule ou une
  majuscule dans le texte d'origine, le hash produit sera totalement différent.

* Irréversibilité (Hachage cryptographique) : Il est impossible de retrouver la
  donnée d'origine à partir du hash. C'est un sens unique.

* Résistance aux collisions : Il est extrêmement improbable que deux entrées
  différentes produisent le même hash.

Le dernier critère implique que l'_image_ de la fonction (l'ensemble de ses
valeurs possibles) soit extrêmement grand. La fonction de hachage
[SHA-1](https://fr.wikipedia.org/wiki/SHA-1), utilisée couramment par git,
produit par exemple des valeurs de 160 bits, ce qui correspond à $2^{160}$
valeurs possibles, ce qui est un nombre vraiment très grand, mais tout de même
plus petit que ceux produits par la fonction
[SHA-256](https://fr.wikipedia.org/wiki/SHA-2), aussi utilisée par les versions
plus modernes de git, et dont la taille de l'image se rapproche du nombre estimé
d'atomes dans l'univers (environ $2^{266}$, ou $10^{80}$).

Il est important de comprendre que le but d'une fonction de hachage, dans le
contexte de git, est de calculer un nombre unique, à partir d'un "objet". Cet
"objet" (au sens digital) peut être de plusieurs natures :

1. Une chaîne de caractères
2. Un fichier (ou document)
3. Un groupe de plusieurs fichiers
4. Une arborescence (récursive) de fichiers
5. Etc.

Chacun de ces objets peut être considéré comme étant un nombre, avec les
conversions nécessaires. C'est ici qu'entrent en jeu les qualités particulières
que nous avons énumérées ci-haut&nbsp;: pour un objet donné (un fichier par
exemple), la valeur de hash doit être unique (résistance aux collisions), et
toujours la même, sans exception (déterminisme). Si on ne change ne serait-ce
qu'un bit d'un fichier, la valeur _doit_ changer (effet d'avalanche).
L'implémentation de cette fonction (dans un langage comme Python, avec la
librairie [hashlib](https://docs.python.org/3/library/hashlib.html) par exemple
doit être suffisamment rapide, parce que git l'utilisera extrêmement souvent,
étant donné qu'il s'agit d'une de ses opérations fondamentales.

{{% details "Implémentation de SHA-256 en Python pur (sans la libraire `hashlib`), pour les curieux" %}}

```python
# Implémentation pédagogique de SHA-256 en Python pur (sans hashlib)

def rotation_droite(valeur, decalage):
    """
    Rotation circulaire à droite sur 32 bits
    """
    return ((valeur >> decalage) | (valeur << (32 - decalage))) & 0xFFFFFFFF


def sha256(message: bytes) -> str:
    """
    Calcule le hash SHA-256 d'un message (bytes)
    et retourne une chaîne hexadécimale
    """

    # Valeurs initiales du hash
    # (32 premiers bits des parties fractionnaires
    # des racines carrées des 8 premiers nombres premiers)
    H = [
        0x6a09e667,
        0xbb67ae85,
        0x3c6ef372,
        0xa54ff53a,
        0x510e527f,
        0x9b05688c,
        0x1f83d9ab,
        0x5be0cd19,
    ]

    # Constantes de ronde
    # (32 premiers bits des parties fractionnaires
    # des racines cubiques des 64 premiers nombres premiers)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    # --- Prétraitement (padding) ---

    longueur_originale = len(message) * 8  # en bits
    message += b'\x80'  # ajout du bit 1

    # Ajout de zéros jusqu'à atteindre 448 bits modulo 512
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    # Ajout de la longueur originale sur 64 bits
    message += longueur_originale.to_bytes(8, 'big')

    # --- Traitement par blocs de 512 bits ---

    for debut_bloc in range(0, len(message), 64):
        bloc = message[debut_bloc:debut_bloc + 64]
        W = [0] * 64  # planification du message

        # Les 16 premiers mots proviennent directement du bloc
        for i in range(16):
            W[i] = int.from_bytes(bloc[i*4:(i+1)*4], 'big')

        # Extension des 16 mots en 64
        for i in range(16, 64):
            s0 = (
                rotation_droite(W[i-15], 7)
                ^ rotation_droite(W[i-15], 18)
                ^ (W[i-15] >> 3)
            )
            s1 = (
                rotation_droite(W[i-2], 17)
                ^ rotation_droite(W[i-2], 19)
                ^ (W[i-2] >> 10)
            )
            W[i] = (W[i-16] + s0 + W[i-7] + s1) & 0xFFFFFFFF

        # Initialisation des registres de travail
        a, b, c, d, e, f, g, h = H

        # --- Boucle principale de compression ---
        for i in range(64):
            S1 = (
                rotation_droite(e, 6)
                ^ rotation_droite(e, 11)
                ^ rotation_droite(e, 25)
            )
            choix = (e & f) ^ (~e & g)
            temp1 = (h + S1 + choix + K[i] + W[i]) & 0xFFFFFFFF

            S0 = (
                rotation_droite(a, 2)
                ^ rotation_droite(a, 13)
                ^ rotation_droite(a, 22)
            )
            majorite = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + majorite) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        # Ajout du résultat du bloc au hash courant
        H = [
            (x + y) & 0xFFFFFFFF
            for x, y in zip(H, [a, b, c, d, e, f, g, h])
        ]

    # Conversion finale en hexadécimal
    return ''.join(f'{valeur:08x}' for valeur in H)


# Exemple d'utilisation
if __name__ == "__main__":
    print(sha256(b"hello world"))
```

{{% /details %}}

Une valeur de hash particulière pourrait être par exemple&nbsp;:

`2123f2435e1dbe255a323c90e97e38f759fe8946`

ce qui correspond à un nombre hexadécimal (en base 16 donc, qui s'exprime avec
les dix chiffres 0 à 10, ainsi que les 6 premières lettres de l'alphabet, de `a`
à `f`) de 40 "chiffres". Chaque caractère hexadécimal de cette chaîne étant
équivalent à 4 bits, nous avons donc un nombre de $40 \times 4 = 160$ bits, qui
permet d'exprimer donc $2^{160}$ valeurs possibles.

Une manière de comprendre le rôle que peut jouer une fonction de hachage est
en tant que _signature_ : une signature _représente_ une personne ou un document
de manière unique, sans aucune ambiguïté possible. Il est également possible de
se représenter un hash en tant que _pointeur_ vers quelque chose.

### Les fondements de git

Git est un outil pour la ligne de commande qui utilise une base de données
particulière pour représenter le contenu et l'évolution historique de l'ensemble
de fichiers d'un projet de développement logiciel. Nous allons l'étudier tout en
l'utilisant concrètement. Je vous recommande d'entrer les commandes dans votre
propre ligne de commande au moment de la lecture, afin de rendre plus concrète
les notions que nous verrons.

La première notion importante de git est celle de _dépôt_ (repository en anglais), qui
correspond à un répertoire particulier, et qui constitue un projet git. Ce répertoire
peut déjà exister (et contenir des fichiers) ou être créé pour l'occasion et donc être vide.
Nous allons donc tout d'abord créer un nouveau répertoire :

```shell
$ mkdir mon_premier_depot
$ cd mon_premier_depot
$ ls -al
total 0
drwxr-xr-x@  2 cjauvin  staff    64 Jan 13 16:54 ./
drwxr-x---+ 75 cjauvin  staff  2400 Jan 13 16:54 ../
```

Notre répertoire n'est pas encore un dépôt git, mais avec cette commande il le devient :

```shell
$ git init
Initialized empty Git repository in /Users/cjauvin/mon_premier_depot/.git/
```

On peut constater que git a ajouté un répertoire spécial dans notre répertoire :

```shell
$ ls -al
total 0
drwxr-xr-x@  3 cjauvin  staff    96 Jan 13 16:58 ./
drwxr-x---+ 75 cjauvin  staff  2400 Jan 13 16:54 ../
drwxr-xr-x@  9 cjauvin  staff   288 Jan 13 17:10 .git/
```

Ce répertoire contient toutes les données dont git aura besoin pour gérer notre dépôt :

```shell
$ ls -al .git
total 24
drwxr-xr-x@  9 cjauvin  staff  288 Jan 13 17:10 ./
drwxr-xr-x@  3 cjauvin  staff   96 Jan 13 16:58 ../
-rw-r--r--@  1 cjauvin  staff  137 Jan 13 16:58 config
-rw-r--r--@  1 cjauvin  staff   73 Jan 13 16:58 description
-rw-r--r--@  1 cjauvin  staff   21 Jan 13 16:58 HEAD
drwxr-xr-x@ 16 cjauvin  staff  512 Jan 13 16:58 hooks/
drwxr-xr-x@  3 cjauvin  staff   96 Jan 13 16:58 info/
drwxr-xr-x@  4 cjauvin  staff  128 Jan 13 16:58 objects/
drwxr-xr-x@  4 cjauvin  staff  128 Jan 13 16:58 refs/
```

Créons tout d'abord un premier fichier :

```
$ echo "hello!" >> toto.txt
```

À ce stade, l'état du fichier est "untracked", c'est-à-dire qu'il ne fait pas partie
du dépôt (même si git a tout de même remarqué sa présence) :

```shell
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        toto.txt

nothing added to commit but untracked files present (use "git add" to track)
```

On peut ajouter le fichier dans le "staging area" de git, qui constitue une sorte d'espace de travail
temporaire, qui sert à accumuler les changement que nous voudrons "commiter" plus tard :

```shell
git add toto.txt
```

Une fois le fichier ajouté, la même commande permet de constater le changement d'état :

```shell
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   toto.txt
```

On est maintenant prêt à faire notre premier commit, qui est simplement l'ajout de ce fichier :

```shell
$ git commit -m "Premier commit"
[main (root-commit) 1359fb1] Premier commit
 1 file changed, 1 insertion(+)
 create mode 100644 toto.txt
```

Une fois ce premier commit effectué, notre dépôt git est démarré en bonne et due
forme, et on peut commencer à l'inspecter en profondeur pour en comprendre le
fonctionner. Il est important de comprendre que les commandes qui vont suivre
sont très rarement utilisées dans l'usage quotidien de git. On s'en sert ici en
tant qu'outils pédagogiques.

Git fonctionne en manipulant quatre types fondamentaux d'objets. Le premier type
est le _blob_, qui correspond aux données données binaires compressées d'un
fichier donné (ici `toto.txt`) :

```shell
$ git ls-tree -r HEAD
100644 blob 4effa19f4f75f846c3229b9dbdbad14eff362f32    toto.txt
```

Notre premier blob a donc comme identifiant le hash `4effa19f4f75f846c3229b9dbdbad14eff362f32`.
Voici comment git calcule le hash :

```shell
 git hash-object toto.txt
4effa19f4f75f846c3229b9dbdbad14eff362f32
```

Ce blob est en fait un fichier, qui est sauvegardé dans la base de données
spéciale de git (dans le répertoire caché `.git`). Le chemin vers ce fichier (de
blob) est créé à partir du hash, qui est séparé en deux parties (la première
correspondant à son suffixe de deux lettres) :

```shell
ll .git/objects/
total 0
drwxr-xr-x@ 3 cjauvin  staff    96B Jan 13 17:28 13/
drwxr-xr-x@ 3 cjauvin  staff    96B Jan 13 17:25 4e/
drwxr-xr-x@ 3 cjauvin  staff    96B Jan 13 17:28 c4/
drwxr-xr-x@ 2 cjauvin  staff    64B Jan 13 16:58 info/
drwxr-xr-x@ 2 cjauvin  staff    64B Jan 13 16:58 pack/
$
$ ll .git/objects/4e/
total 8
-r--r--r--@ 1 cjauvin  staff    22B Jan 13 17:25 ffa19f4f75f846c3229b9dbdbad14eff362f32
```

Contrairement à `toto.txt`, qui est un fichier texte, le blob n'est pas facile à
lire, car il est constitué de données binaires compressées :

```shell
cat .git/objects/4e/ffa19f4f75f846
c3229b9dbdbad14eff362f32
xK��OR0g�H���W�"6⏎
```





 à l'aide des objets fondamentaux
suivants :

1. Les _blobs_, qui contiennent les données binaires brutes des fichiers
   (seulement les données, aucune autre métadonnées associées aux fichiers,
   comme les noms de fichier, les permissions, etc).

{{< image src="git-blob.png" alt="Un blob git" title="A placeholder" loading="lazy" >}}

2. Les _arbres_, (trees en anglais) qui représentent l'arborescence des fichiers
   du dépôt; cette représentation est _récursive_ : un fichier est représenté à
   l'aide d'un hash qui "pointe" vers le blob correspondant, et un répertoire
   est représenté avec un hash qui pointe vers un arbre.

{{< image src="git-tree.png" alt="Un blob git" title="A placeholder" loading="lazy" >}}

3. Les _commits_, qui représentent des "instantanés" (en anglais snapshots) de
   l'état total du dépôt, au moment du commit.

4. Les _tags_, qui sont des étiquettes particulières, associés à des commits particuliers.

Chaque fois qu'un fichier est ajouté au dépôt (avec la commande `git add`), son
contenu est sauvegardé dans un blob binaire, qui se trouve dans le répertoire
spécial `.git`, à la base du depot.

Chaque fois qu'un commit est créé (avec la commande `git commit`), un nouvel
objet (de type commit) est ajouté à la base de données, qui contient trois
choses :

1. Un pointeur (identifiant, sous la forme d'un hash) vers un arbre qui
   représente (de manière récursive) l'état du dépôt.

2. Un ou plusieurs pointeurs (hash) vers les commits _parents_ (le ou les commits qui
   ont précédé ce commit particulier)

3. Des métadonnées diverses, comme la date et l'heure de création du commit,
   l'adresse de courriel du commiteur, etc.

Étant donné la présence du pointeur vers un parent, le fait d'ajouter un commit crée
une chaîne de commits :

{{< image src="git-chain.png" alt="" title="" loading="lazy" >}}

Chaque commit a donc un pointeur qui pointe vers son commit prédécesseur (nous
verrons plus loin qu'il est possible pour un commit d'avoir plus d'un parents,
et en quoi c'est utile).

Jusqu'ici, git ne nous permet que d'évoluer de manière linéaire, étant donné que
n'avons qu'une chaîne de commits. Pourtant, le développement logiciel, surtout s'il est
effectué par une équipe, est tout sauf linéaire. Des embranchements peuvent être nécessaires
dans le processus d'évolution du code source. Pour illustrer cela, représentez-vous
la scénario suivant :

1. Une équipe de développement a complété la première version (v1) d'un logiciel de prise de rendez-vous
2. La première version est maintenant en ligne, et est utilisée par le grand public
3. L'équipe doit commencer à travailler sur la nouvelle version (v2)

Si on voulait modéliser le développement à l'aide d'une séquence linéaire, voici ce que ça
pourrait donner :

{{< image src="git-linear-versions.png" alt="" title="" loading="lazy" >}}

Maintenant que se passe-t-il si un bogue est découvert dans la version 1,
présentement en ligne (et qui correspond au commit `C4` dans cet exemple)?

{{< image src="git-linear-versions-bug.png" alt="" title="" loading="lazy" >}}

Le problème est donc que la chaîne de commits est déjà rendue plus loin, au deuxième
commit de la version 2, soit le commit `C6` ! Comment peut-on gérer une telle situation
avec un outil comme git? En utilisant une _branche_ :

{{< image src="git-with-branch-bugfix.png" alt="" title="" loading="lazy" >}}

Donc au moment exact où le travail sur la version 1 a été complété (au commit
`C4` donc), il fallait créer une nouvelle branche (nommée `v2`), pour le
travail qui allait être effectué sur la nouvelle version 2. De cette manière,
quand un problème survient avec la version 1, il est possible de le résoudre
en ajoutant simplement un commit (`C7`) à la branche `main`, correspondant à la
version 1.

{{< applet src="/html/applets/git.html" width="140%" scale="1.0" >}}

