---
title: "L'intégration continue (CI)"
slug: "ci"
weight: 50
---

# L'intégration continue (CI)

## Quel est le problème qu'on cherche à résoudre?

Dans les sections précédentes, nous avons vu comment écrire des tests pour
vérifier qu'un programme se comporte correctement, comment utiliser git pour
gérer l'évolution du code, et comment gérer les dépendances d'un projet avec uv.
Mais il reste un problème important : toutes ces vérifications dépendent de la
discipline individuelle du programmeur. Rien ne garantit qu'un développeur va
exécuter les tests avant de pousser son code. Rien ne garantit non plus que son
environnement local est représentatif de l'environnement réel : peut-être que
les tests passent sur sa machine parce qu'il a une dépendance installée
globalement, ou une version de Python légèrement différente. Le fameux "ça marche
sur ma machine" est l'un des problèmes les plus classiques du développement
logiciel.

L'intégration continue (CI, pour *continuous integration*) est la pratique qui
résout ce problème en automatisant les vérifications à chaque changement. L'idée
est simple : chaque fois qu'un développeur pousse du code vers le dépôt partagé,
un serveur distant exécute automatiquement une série de vérifications (tests,
linting, etc.) dans un environnement propre et reproductible. Si quelque chose
échoue, l'équipe en est immédiatement informée.

Le terme "intégration continue" vient de l'Extreme Programming (XP), la
méthodologie proposée par Kent Beck à la fin des années 90, dont on a parlé dans
le module 1. L'une des pratiques centrales de XP était justement d'intégrer le
code de tous les développeurs plusieurs fois par jour, plutôt que d'attendre des
semaines ou des mois avant de fusionner les changements de chacun. En 2006,
Martin Fowler a publié un article influent intitulé *Continuous Integration* qui
a formalisé et popularisé la pratique au-delà de la communauté XP. Son argument
principal était que plus on attend avant d'intégrer, plus les conflits sont
difficiles à résoudre, et que l'automatisation des vérifications est la clé pour
rendre l'intégration fréquente viable.

## YAML

Avant d'aborder GitHub Actions, il faut dire un mot sur YAML, le format utilisé
pour décrire les workflows de CI. YAML (*YAML Ain't Markup Language*) est un
format de données conçu pour être lisible par les humains. Il joue le même rôle
que JSON (décrire des structures de données), mais avec une syntaxe plus légère,
basée sur l'indentation plutôt que sur les accolades et les crochets. Voici un
exemple qui illustre les éléments de base :

```yaml
# Un commentaire
nom: Alice
age: 30

# Une liste
langages:
  - Python
  - JavaScript
  - Rust

# Un objet imbriqué
adresse:
  rue: 123 Main Street
  ville: Montréal
```

Les règles essentielles sont peu nombreuses : les clés et les valeurs sont
séparées par `:`, les listes sont indiquées par des tirets `-`, et la hiérarchie
est exprimée par l'indentation (toujours des espaces, jamais des tabulations).
YAML est très utilisé dans le monde du DevOps et de la CI, entre autres parce
que les fichiers de configuration doivent souvent être lus et modifiés à la main,
et que sa lisibilité est un avantage réel par rapport à JSON.

YAML a cependant la réputation d'être une source de frustration, justement à
cause de sa dépendance à l'indentation. Une erreur d'un seul espace peut rendre
un fichier invalide, ou pire, changer silencieusement sa signification. Par
exemple :

```yaml
# Ceci est une liste de deux éléments à l'intérieur de "fruits"
fruits:
  - pomme
  - banane

# Ceci est une erreur : "banane" n'est plus au même niveau
fruits:
  - pomme
    - banane
```

Un autre piège classique concerne les valeurs qui ressemblent à autre chose que
des chaînes de caractères. Par exemple, `version: 3.10` sera interprété comme le
nombre `3.1` (le zéro final est supprimé), et non comme la chaîne `"3.10"`. Pour
éviter ce problème, il faut mettre des guillemets explicites :
`version: "3.10"`. Ce genre de subtilité est une source fréquente de bugs dans
les fichiers de CI, en particulier lorsqu'on spécifie des versions de Python.

## GitHub Actions

GitHub Actions est le système de CI intégré directement dans GitHub. Il est
gratuit pour les projets open source et offre un quota mensuel généreux pour les
dépôts privés. Son principal avantage est qu'il ne nécessite aucune configuration
externe : tout se passe à l'intérieur de GitHub, et il suffit d'ajouter un
fichier dans le dépôt pour activer la CI.

Le fonctionnement repose sur quelques concepts clés qu'il faut comprendre :

- **Workflow** : un fichier YAML placé dans le répertoire `.github/workflows/`
  du dépôt. Chaque fichier décrit une automatisation complète. Un dépôt peut
  contenir plusieurs workflows (par exemple, un pour les tests et un autre pour
  le déploiement).

- **Event** (ou *trigger*) : l'événement qui déclenche l'exécution du workflow.
  Le plus courant est `push` (quelqu'un pousse du code), mais ça peut aussi être
  l'ouverture d'une pull request, un horaire programmé (*cron*), ou même un
  déclenchement manuel.

- **Job** : un groupe d'étapes qui s'exécutent ensemble, sur une même machine.
  Un workflow peut contenir plusieurs jobs, qui par défaut s'exécutent en
  parallèle.

- **Step** : une étape individuelle à l'intérieur d'un job. Chaque step est soit
  une commande shell (par exemple `pytest`), soit l'utilisation d'une *action*
  pré-faite.

- **Action** : un bloc réutilisable, publié par GitHub ou par la communauté, qui
  encapsule une tâche courante. Par exemple, `actions/checkout` clone le dépôt
  dans la machine, et `actions/setup-python` installe une version de Python. On
  peut voir les actions comme des fonctions de bibliothèque pour la CI.

- **Runner** : la machine qui exécute le job. C'est ici que les choses
  deviennent intéressantes. Quand un workflow se déclenche, GitHub crée à la
  volée une machine virtuelle (VM) dans le cloud, y installe le système
  d'exploitation demandé (Ubuntu, macOS ou Windows), exécute toutes les étapes du
  job, puis détruit la machine. Chaque exécution part donc d'un environnement
  complètement vierge, ce qui élimine le problème du "ça marche sur ma machine".
  Ce concept de machines éphémères dans le cloud sera exploré plus en profondeur
  dans le module 5.

## Exemple concret

Construisons un exemple de bout en bout : un petit projet Python avec un test,
un workflow GitHub Actions, et on observera le résultat sur GitHub. L'idée est de
voir tout le cycle : un `push` déclenche la CI, qui exécute les tests
automatiquement.

Commençons par créer un petit projet Python avec uv :

```shell
mkdir ci-demo
cd ci-demo
uv init
```

Ajoutons pytest comme dépendance de développement :

```shell
uv add --dev pytest
```

Créons un fichier `main.py` avec une fonction simple :

```python
def est_palindrome(mot):
    """Vérifie si un mot est un palindrome."""
    mot = mot.lower().replace(" ", "")
    return mot == mot[::-1]
```

Et un fichier `test_main.py` avec quelques tests :

```python
from main import est_palindrome

def test_palindrome_simple():
    assert est_palindrome("kayak")
    assert est_palindrome("radar")

def test_palindrome_avec_majuscules():
    assert est_palindrome("Kayak")

def test_non_palindrome():
    assert not est_palindrome("python")
```

Vérifions que les tests passent localement :

```shell
uv run pytest
```

Maintenant, créons le workflow GitHub Actions. Il faut d'abord créer le
répertoire :

```shell
mkdir -p .github/workflows
```

Puis créer le fichier `.github/workflows/ci.yml` :

```yaml
name: CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Installer Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Installer uv
        uses: astral-sh/setup-uv@v3

      - name: Installer les dépendances
        run: uv sync

      - name: Exécuter les tests
        run: uv run pytest
```

Reprenons ce fichier section par section :

```yaml
name: CI
```

Le nom du workflow, qui apparaît dans l'onglet Actions de GitHub.

```yaml
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
```

Les événements déclencheurs. Ici, le workflow s'exécute quand quelqu'un pousse du
code sur la branche `main`, ou quand une pull request cible `main`. Notez les
guillemets autour de `"main"` : c'est une bonne habitude en YAML pour éviter les
surprises d'interprétation, comme on l'a vu plus haut.

```yaml
jobs:
  tests:
    runs-on: ubuntu-latest
```

On déclare un job nommé `tests`, qui s'exécutera sur un runner Ubuntu (la
dernière version disponible). C'est la machine virtuelle éphémère que GitHub va
créer pour nous.

```yaml
    steps:
      - uses: actions/checkout@v4
```

La première étape utilise l'action `actions/checkout`, qui clone notre dépôt dans
la VM. Sans cette étape, le runner ne contiendrait aucun fichier, car la machine
est créée vierge. Le `@v4` indique la version de l'action à utiliser.

```yaml
      - name: Installer Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
```

On installe Python 3.12. Le champ `with` permet de passer des paramètres à
l'action. Notez les guillemets autour de `"3.12"` : c'est exactement le piège
YAML dont on a parlé. Sans guillemets, `3.12` serait interprété comme le nombre
`3.12`, ce qui pourrait causer des problèmes.

```yaml
      - name: Installer uv
        uses: astral-sh/setup-uv@v3
```

On installe uv en utilisant une action publiée par Astral, l'entreprise derrière
uv. C'est un bon exemple d'action communautaire : plutôt que d'écrire nous-mêmes
les commandes d'installation, on réutilise un bloc maintenu par les auteurs de
l'outil.

```yaml
      - name: Installer les dépendances
        run: uv sync

      - name: Exécuter les tests
        run: uv run pytest
```

Les deux dernières étapes sont des commandes shell ordinaires (indiquées par
`run:` plutôt que `uses:`). On installe les dépendances avec `uv sync`, puis on
exécute les tests. Ce sont exactement les mêmes commandes qu'on utiliserait
localement sur notre propre machine.

Il ne reste qu'à initialiser un dépôt git, faire un commit et pousser le tout
vers GitHub :

```shell
git init
git add .
git commit -m "Initial commit"
gh repo create ci-demo --public --source=. --push
```

Une fois le push complété, allez dans l'onglet **Actions** de votre dépôt sur
GitHub. Vous devriez voir le workflow "CI" qui s'est déclenché automatiquement.
Après quelques secondes, si tout va bien, vous verrez un check vert indiquant que
les tests ont passé.

## Au-delà des tests

Les tests sont le cas d'utilisation le plus courant de la CI, mais un workflow
peut automatiser bien d'autres vérifications. Voici quelques exemples fréquents :

- **Le linting** : des outils comme [ruff](https://docs.astral.sh/ruff/)
  analysent le code pour détecter des erreurs potentielles, des variables
  inutilisées, des imports manquants, ou des violations de conventions de style.
  C'est un peu comme un correcteur grammatical pour le code.
- **Le formatage** : on peut vérifier que le code respecte un style uniforme
  (indentation, longueur des lignes, etc.). Ruff peut aussi jouer ce rôle. La CI
  peut rejeter du code mal formaté, ce qui évite les débats de style en revue de
  code.
- **Le type checking** : des outils comme mypy, qu'on a mentionné dans la
  section sur les types, peuvent être exécutés en CI pour vérifier la cohérence
  des annotations de type.
- **La vérification des dépendances** : on peut détecter automatiquement si
  l'une des dépendances du projet contient une vulnérabilité de sécurité connue.

L'idée générale est que tout ce qui peut être vérifié automatiquement devrait
l'être en CI. Chaque vérification ajoutée au workflow est une erreur de moins qui
peut se rendre en production.

## Vers le déploiement continu (CD)

L'intégration continue se concentre sur la vérification automatique du code, mais
l'automatisation ne doit pas s'arrêter là. L'extension naturelle de la CI est le
*continuous deployment* (CD), ou déploiement continu : une fois que les
vérifications passent, le code est automatiquement déployé en production, sans
intervention humaine. On parle souvent de "pipeline CI/CD" pour désigner cette
chaîne complète, de la vérification au déploiement. GitHub Actions permet de
définir de tels pipelines dans les mêmes fichiers de workflow qu'on a vus ici.
Nous reviendrons sur le déploiement et les pratiques DevOps dans le module 5.