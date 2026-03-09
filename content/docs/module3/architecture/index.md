---
title: "Architecture et modularité"
weight: 10
---

# Architecture et modularité

Quand un programme est petit, sa structure importe peu. On peut tout mettre dans
un seul fichier, avec quelques fonctions, et ça fonctionne. Mais dès que le
programme grossit, cette approche atteint ses limites. Un fichier de 5000 lignes
devient difficile à naviguer. Deux développeurs qui modifient le même fichier se
marchent sur les pieds. Un changement dans une partie du code casse quelque
chose dans une autre. Le programme est devenu un système, mais sa structure ne
le reflète pas encore. La question n'est alors pas *s'il faut* découper le
système en parties, mais *comment* le découper. Et cette question est bien plus
subtile qu'elle n'y paraît.

## Parnas et l'information hiding (1972)

En 1972, l'informaticien américain David Parnas publie un court article qui va
devenir l'un des plus influents de l'histoire du génie logiciel : *On the
Criteria To Be Used in Decomposing Systems into Modules*. Le titre est direct :
quels critères devrait-on utiliser pour découper un système en modules ? Pour
répondre, Parnas prend un exemple concret, un programme appelé KWIC (Key Word In
Context). Le principe de KWIC est simple : on lui donne une liste de titres, et
il produit un index de tous les mots-clés significatifs, chacun présenté dans
son contexte original. Par exemple, à partir du titre "The Pragmatic
Programmer", KWIC produirait les entrées "Pragmatic Programmer, The" et
"Programmer, The Pragmatic" (en ignorant les mots non significatifs comme
"The"). C'est un système qui était couramment utilisé pour indexer des articles
scientifiques.

L'idée vient du monde de la documentation scientifique. Dans les années 50 et
60, avant les moteurs de recherche, les bibliothécaires et les chercheurs
avaient besoin de trouver rapidement des articles par mots-clés. Un index KWIC
prend une liste de titres et produit une entrée pour chaque mot significatif du
titre, en le présentant dans son contexte original. Par exemple, à partir de ces
trois titres :

```
The Pragmatic Programmer
Clean Code
No Silver Bullet
```

Un index KWIC produirait (en ignorant les mots non significatifs comme "The",
"No") :

```
Silver Bullet              ← entrée pour "Bullet"
Clean Code                 ← entrée pour "Clean"
Code                       ← entrée pour "Code" (rotation de "Clean Code")
Pragmatic Programmer       ← entrée pour "Pragmatic"
Programmer The Pragmatic   ← entrée pour "Programmer"
Silver Bullet No           ← entrée pour "Silver"
```

Chaque titre est "tourné" (rotated) de manière à ce que le mot-clé apparaisse
en premier, et les entrées sont triées alphabétiquement. Le résultat est un
index compact qui permet de retrouver un titre à partir de n'importe lequel de
ses mots significatifs.

{{< hint info >}}
**L'utilitaire `ptx`**

L'idée de l'index KWIC a été suffisamment importante pour qu'un utilitaire Unix
lui soit dédié : `ptx` (permuted index), qui fait partie des GNU coreutils.
On peut l'essayer directement sur la ligne de commande :

```shell
$ echo -e "The Pragmatic Programmer\nClean Code\nNo Silver Bullet" | ptx -S '\n' -w 72
                           No Silver   Bullet
                                       Clean Code
                               Clean   Code
                                       No Silver Bullet
                                 The   Pragmatic Programmer
                       The Pragmatic   Programmer
                                  No   Silver Bullet
                                       The Pragmatic Programmer
```

Chaque ligne est formatée de manière à ce que le mot-clé apparaisse aligné au
début de la colonne de droite, avec son contexte à gauche. C'est un petit
vestige d'une époque où l'indexation automatique des textes était une
préoccupation centrale de l'informatique.
{{< /hint >}}

### Décomposition 1 : par flux de traitement

Parnas compare deux manières de découper ce même système KWIC en modules. La
première, qu'on pourrait qualifier de "naïve", suit le flux de traitement des
données : un module pour lire l'entrée, un module pour produire les rotations,
un module pour trier, un module pour afficher. C'est la décomposition la plus
intuitive, celle qu'on ferait naturellement si on pensait le programme comme une
séquence d'étapes. Voici à quoi elle ressemblerait en Python :

```python
# Décomposition 1 : par flux de traitement
# Chaque module correspond à une étape du pipeline

# Les données partagées entre les modules
lines = []
rotations = []
sorted_rotations = []

STOP_WORDS = {"the", "a", "an", "of", "in", "to", "and", "is", "for"}

def read_input(titles):
    """Étape 1 : lire les titres"""
    lines.clear()
    lines.extend(titles)

def make_rotations():
    """Étape 2 : produire toutes les rotations de chaque titre"""
    rotations.clear()
    for line in lines:
        words = line.split()
        for i, word in enumerate(words):
            if word.lower() not in STOP_WORDS:
                rotated = words[i:] + words[:i]
                rotations.append(" ".join(rotated))

def sort_rotations():
    """Étape 3 : trier les rotations alphabétiquement"""
    sorted_rotations.clear()
    sorted_rotations.extend(sorted(rotations, key=str.lower))

def display_output():
    """Étape 4 : afficher le résultat"""
    for rotation in sorted_rotations:
        print(rotation)

# Utilisation
read_input(["The Pragmatic Programmer", "Clean Code", "No Silver Bullet"])
make_rotations()
sort_rotations()
display_output()
```

Le problème de cette décomposition est que tous les modules partagent les mêmes
données globales (`lines`, `rotations`, `sorted_rotations`). Si on décide de
changer la manière dont les lignes sont stockées, par exemple en passant d'une
liste à un fichier, il faut modifier *tous* les modules. Le découpage par flux
de traitement crée un couplage fort autour de la représentation interne des
données.

### Décomposition 2 : par information hiding (Parnas)

Parnas propose une autre décomposition, fondée sur un principe différent :
chaque module doit cacher une *décision de conception* susceptible de changer.
Au lieu de découper par étapes de traitement, on découpe par *responsabilité*.
Le module de stockage des lignes ne sait rien du tri ; le module de rotation ne
sait rien de la manière dont les lignes sont stockées. Chaque module expose une
interface simple et cache ses détails internes. Parnas appelle ce principe
l'*information hiding* (masquage de l'information).

```python
# Décomposition 2 : par information hiding (Parnas)
# Chaque module cache une décision de conception

class LineStorage:
    """Cache la décision : comment les lignes sont stockées en mémoire."""
    def __init__(self):
        self._lines = []

    def add(self, line):
        self._lines.append(line)

    def get(self, index):
        return self._lines[index]

    def count(self):
        return len(self._lines)


class Rotator:
    """Cache la décision : comment les rotations sont calculées."""
    STOP_WORDS = {"the", "a", "an", "of", "in", "to", "and", "is", "for"}

    def rotations(self, line):
        words = line.split()
        result = []
        for i, word in enumerate(words):
            if word.lower() not in self.STOP_WORDS:
                result.append(words[i:] + words[:i])
        return result


class Sorter:
    """Cache la décision : comment le tri est effectué."""
    def sort(self, items):
        return sorted(items, key=lambda words: [w.lower() for w in words])


class KWICSystem:
    """Assemble les modules sans connaître leurs détails internes."""
    def __init__(self):
        self.storage = LineStorage()
        self.rotator = Rotator()
        self.sorter = Sorter()

    def process(self, titles):
        for title in titles:
            self.storage.add(title)

        all_rotations = []
        for i in range(self.storage.count()):
            line = self.storage.get(i)
            all_rotations.extend(self.rotator.rotations(line))

        for words in self.sorter.sort(all_rotations):
            print(" ".join(words))


kwic = KWICSystem()
kwic.process(["The Pragmatic Programmer", "Clean Code", "No Silver Bullet"])
```

La différence est subtile mais profonde. Si on décide demain de stocker les
lignes dans un fichier plutôt qu'en mémoire, il suffit de modifier
`LineStorage`. Si on change l'algorithme de tri, seul `Sorter` est touché. Si on
veut ajouter des règles de filtrage des stop words, seul `Rotator` est concerné.
Chaque changement est *local* à un module. C'est exactement ce que Parnas
voulait démontrer : le bon critère de décomposition n'est pas "quelle étape du
traitement", mais "quelle décision pourrait changer".