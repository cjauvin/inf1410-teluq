---
title: "Les tests"
slug: "tests"
weight: 20
---

# Les tests

Dans la section précédente, nous avons vu que la programmation repose sur des
structures de données, des algorithmes et des systèmes de types. Mais écrire du
code qui *semble* correct ne suffit pas : il faut pouvoir *vérifier* qu'il se
comporte comme on le pense. C'est exactement ce que Peter Naur décrivait dans
*Programming as Theory Building* : le programmeur construit un modèle mental de
ce que le programme est censé faire. Les tests sont la manière la plus directe
de confronter ce modèle mental à la réalité.

Un compilateur, dans un langage comme C ou Java, détecte automatiquement toute
une classe d'erreurs avant même que le programme ne s'exécute : une variable mal
nommée, un type incompatible, une fonction appelée avec le mauvais nombre
d'arguments. En Python, rien de tout cela n'est vérifié à l'avance. La raison
est simple : Python est un langage interprété, qui exécute le code ligne par
ligne, au moment de l'exécution. Il n'y a pas d'étape de compilation qui
analyserait l'ensemble du programme avant de le lancer. Un programme Python peut
donc contenir une faute de frappe dans un nom de variable et ne planter que
lorsque cette ligne précise est atteinte à l'exécution. Les tests jouent donc un
double rôle en Python : ils vérifient la logique du programme, mais ils servent
aussi de filet de sécurité de base, un peu comme le ferait un compilateur, en
s'assurant que le code s'exécute sans erreur dans les cas prévus. Dans un
contexte où une grande quantité de code Python est développée et maintenue par
une grosse équipe, cette absence de vérification statique rend les tests
carrément essentiels : sans eux, il devient pratiquement impossible de s'assurer
que les modifications d'une personne ne cassent pas le travail des autres.

Un test est donc un programme qui teste le code d'un autre programme, en
appellant ses fonctions de manière isolée et systématique, avec des paramètres spécifiques, afin
de vérifier (valider) que les résultats sont exacts et corrects.

## Le mécanisme de base : `assert`

L'idée fondamentale d'un test est de comparer le comportement observé d'un
programme avec le comportement attendu. En Python, le mécanisme le plus simple
pour exprimer cela est l'instruction `assert` : elle prend une condition, et si
cette condition est fausse, le programme plante immédiatement avec une erreur.

{{< pyodide >}}
def addition(a, b):
    return a + b

assert addition(2, 3) == 5
assert addition(-1, 1) == 0
assert addition(0, 0) == 0

print("Tous les tests passent!")
{{< /pyodide >}}

On peut essayer de modifier la fonction `addition` pour qu'elle retourne une
valeur incorrecte, et observer ce qui se passe lorsqu'un `assert` échoue :

{{< pyodide >}}
def addition(a, b):
    return a * b  # bug volontaire!

assert addition(2, 3) == 5
{{< /pyodide >}}

## La pyramide des tests

L'instruction `assert` suffit pour vérifier qu'une petite fonction se comporte
correctement, mais un logiciel réel est composé de nombreuses parties qui
interagissent entre elles. La question devient alors : à quel niveau faut-il
tester? Une fonction individuelle? L'interaction entre deux modules? Le système
au complet, du point de vue de l'utilisateur? La *pyramide des tests*,
popularisée par Mike Cohn dans *Succeeding with Agile* (2009), propose un modèle
pour y réfléchir. Elle distingue trois niveaux, du plus fin au plus large :

- **Tests unitaires** (la base, la plus large) : ils testent une fonction ou une
  petite unité de code en isolation. Ils sont rapides, nombreux, et faciles à
  écrire.
- **Tests d'intégration** (le milieu) : ils vérifient que plusieurs composants
  fonctionnent correctement ensemble, par exemple qu'une fonction qui appelle une
  base de données obtient les bons résultats.
- **Tests end-to-end** (le sommet, la plus petite) : ils simulent le parcours
  complet d'un utilisateur à travers le système. Ils sont lents, fragiles, et
  coûteux à maintenir, mais ils vérifient que tout fonctionne de bout en bout.

{{< image src="pyramid.png" alt="" title="" loading="lazy" >}}

La forme de pyramide reflète une règle pratique : on devrait avoir *beaucoup* de
tests unitaires, *quelques* tests d'intégration, et *peu* de tests end-to-end.
La raison est économique : plus on monte dans la pyramide, plus les tests sont
lents à exécuter, difficiles à écrire, et fragiles face aux changements. Un test
unitaire qui vérifie une fonction de calcul prend une fraction de seconde; un
test end-to-end qui simule un utilisateur navigant dans une application web peut
prendre plusieurs secondes, et casser dès qu'un bouton change de place.

Dans le cadre de ce cours, nous allons surtout nous concentrer sur les tests
unitaires, qui sont à la fois les plus fondamentaux et les plus accessibles.

## pytest

L'instruction `assert` est un bon point de départ, mais elle a ses limites. Si
on a des dizaines de tests répartis dans plusieurs fichiers, comment les
découvrir et les exécuter automatiquement? Comment obtenir un rapport clair de ce
qui passe et de ce qui échoue? Comment organiser les tests de manière lisible?

C'est le rôle d'un *framework de test*. En Python, le plus populaire est
**pytest**. Son principe est simple : on écrit des fonctions dont le nom commence
par `test_`, on y met des `assert`, et pytest se charge du reste. Voici un
exemple. Supposons qu'on ait un fichier `calcul.py` :

```python
# calcul.py
def addition(a, b):
    return a + b

def factorielle(n):
    if n <= 1:
        return 1
    return n * factorielle(n - 1)
```

On crée un fichier `test_calcul.py` à côté :

```python
# test_calcul.py
from calcul import addition, factorielle

def test_addition_simple():
    assert addition(2, 3) == 5

def test_addition_negatifs():
    assert addition(-1, 1) == 0

def test_factorielle_base():
    assert factorielle(0) == 1
    assert factorielle(1) == 1

def test_factorielle_recursive():
    assert factorielle(5) == 120
```

On peut installer `pytest` dans un projet avec `uv`, avec le terminal :

```shell
$ uv add pytest
```

On peut ensuite lancer `pytest` dans le terminal, et il découvre et exécute
automatiquement tous les fichiers `test_*.py` :

```shell
$ uv run pytest
=================== test session starts ====================
collected 4 items

test_calcul.py ....                                  [100%]

==================== 4 passed in 0.01s =====================
```

Si on introduit un bug dans la fonction `factorielle` :

```python
def factorielle(n):
    if n <= 1:
        return 0  # bug!
    return n * factorielle(n - 1)
```

pytest produit un rapport détaillé qui montre exactement quelle assertion a
échoué, avec les valeurs comparées :

```shell
=============================== test session starts ===============================
test_calcul.py ..FF                                                          [100%]

=================================== FAILURES ======================================
____________________________ test_factorielle_base ________________________________

    def test_factorielle_base():
>       assert factorielle(0) == 1
E       assert 0 == 1
E        +  where 0 = factorielle(0)

test_calcul.py:14: AssertionError
__________________________ test_factorielle_recursive _____________________________

    def test_factorielle_recursive():
>       assert factorielle(5) == 120
E       assert 0 == 120
E        +  where 0 = factorielle(5)

test_calcul.py:19: AssertionError
============================= short test summary info =============================
FAILED test_calcul.py::test_factorielle_base - assert 0 == 1
FAILED test_calcul.py::test_factorielle_recursive - assert 0 == 120
============================ 2 failed, 2 passed in 0.02s ==========================
```

C'est un avantage important par rapport à un `assert` brut, qui se contente de
planter avec un message `AssertionError` sans aucun détail. pytest décompose
l'expression et montre les valeurs intermédiaires, ce qui facilite
considérablement le diagnostic.

## TDD : Test-Driven Development

Jusqu'ici, nous avons écrit le code d'abord, puis les tests ensuite. Le
*Test-Driven Development* (TDD), popularisé par Kent Beck au début des années
2000, propose d'inverser l'ordre : on écrit le test *avant* le code.

Le cycle TDD se déroule en trois étapes, souvent appelées "Red-Green-Refactor" :

1. **Red** : écrire un test qui échoue (parce que la fonctionnalité n'existe pas
   encore)
2. **Green** : écrire le code *minimal* pour faire passer le test
3. **Refactor** : améliorer le code tout en s'assurant que le test passe toujours

L'idée peut sembler contre-intuitive, mais elle a un avantage profond : elle
force le programmeur à clarifier ce qu'il attend du code *avant* de l'écrire. En
termes de Naur, le test devient une manière d'expliciter sa théorie du programme
avant de la construire.

Prenons un exemple concret : on veut écrire une fonction `est_palindrome` qui
vérifie si une chaine de caractères se lit de la même manière dans les deux sens.

**Étape 1 (Red)** : on écrit les tests d'abord, sans avoir écrit la fonction :

```python
# test_palindrome.py
from palindrome import est_palindrome

def test_palindrome_simple():
    assert est_palindrome("kayak") == True

def test_non_palindrome():
    assert est_palindrome("bonjour") == False

def test_palindrome_vide():
    assert est_palindrome("") == True
```

```shell
$ uv run pytest test_palindrome.py
E   ModuleNotFoundError: No module named 'palindrome'
```

Le test échoue : c'est normal, le module n'existe même pas encore.

**Étape 2 (Green)** : on écrit le code minimal pour faire passer les tests :

```python
# palindrome.py
def est_palindrome(s):
    return s == s[::-1]
```

```shell
$ uv run pytest test_palindrome.py
=================== test session starts ====================
collected 3 items

test_palindrome.py ...                               [100%]

==================== 3 passed in 0.01s =====================
```

Les tests passent.

**Étape 3 (Refactor)** : on peut maintenant enrichir les tests pour couvrir des
cas plus subtils, par exemple ignorer les majuscules et les espaces :

```python
def test_palindrome_majuscules():
    assert est_palindrome("Kayak") == True

def test_palindrome_avec_espaces():
    assert est_palindrome("esope reste ici et se repose") == True
```

Ces nouveaux tests échouent, ce qui nous pousse à améliorer la fonction :

```python
def est_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]
```

Et le cycle recommence.

## La couverture de code

Une question naturelle se pose : comment savoir si nos tests sont suffisants? La
*couverture de code* (code coverage) est une métrique qui mesure quelle
proportion du code source est effectivement exécutée par les tests. L'outil de
référence en Python est **coverage.py**, créé et maintenu par Ned Batchelder
depuis 2004. L'extension **pytest-cov** est simplement un pont qui permet
d'utiliser coverage.py directement depuis pytest. On peut l'installer facilement
avec `uv` en faisant :

```shell
$ uv add pytest-cov
```

Reprenons ensuite notre fichier `calcul.py`, en y ajoutant une fonction `division` :

```python
# calcul.py
def addition(a, b):
    return a + b

def factorielle(n):
    if n <= 1:
        return 1
    return n * factorielle(n - 1)

def division(a, b):
    if b == 0:
        raise ValueError("Division par zéro")
    return a / b
```

Si nos tests ne couvrent que `addition` et `factorielle`, la couverture sera
incomplète :

```shell
$ uv run pytest --cov=calcul test_calcul.py

=================== test session starts ====================
platform darwin -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
rootdir: .../test-examples
configfile: pyproject.toml
plugins: cov-7.1.0
collected 4 items

test_calcul.py ....                                   [100%]

===================== tests coverage =======================
__ coverage: platform darwin, python 3.13.5-final-0 __

Name        Stmts   Miss  Cover
-------------------------------
calcul.py      10      3    70%
-------------------------------
TOTAL          10      3    70%
===================== 4 passed in 0.03s ====================
```

Les trois lignes manquantes correspondent à la fonction `division`, que nos tests
ne touchent pas du tout.

Il est tentant de viser une couverture de 100%, mais c'est un objectif trompeur.
Une couverture élevée garantit que le code a été *exécuté*, pas qu'il est
*correct*. Il existe même une famille de bogues qu'une couverture de 100&nbsp;% ne
peut pas voir par construction, et la section sur [la concurrence]({{< relref "/docs/module2/concurrence/30-ce-qui-casse" >}}) en donne un exemple resté quatre ans invisible. On pourrait exécuter chaque ligne sans jamais vérifier que les
résultats sont bons. La couverture est un indicateur utile pour repérer du code
non testé, mais elle ne remplace pas la réflexion sur la qualité des tests
eux-mêmes.

## Les fixtures

Jusqu'ici, nos tests étaient autonomes : chaque fonction de test créait ses
propres données et n'avait besoin de rien d'autre. Mais dans un projet réel,
plusieurs tests ont souvent besoin du même contexte initial : une connexion à une
base de données, un fichier temporaire, un objet configuré d'une certaine
manière. Sans mécanisme dédié, on se retrouve à copier-coller le même code de
préparation dans chaque test, ce qui viole le principe DRY et rend la suite de
tests fragile : si le setup doit changer, il faut le modifier partout.

Prenons un exemple. Supposons qu'on teste une classe simple `Inventaire` qui
gère une liste de produits :

```python
# inventaire.py
class Inventaire:
    def __init__(self):
        self.produits = {}

    def ajouter(self, nom, quantite):
        self.produits[nom] = self.produits.get(nom, 0) + quantite

    def total(self):
        return sum(self.produits.values())

    def contient(self, nom):
        return nom in self.produits
```

Sans fixtures, chaque test doit créer et remplir son propre inventaire :

```python
# test_inventaire.py
from inventaire import Inventaire

def test_ajouter():
    inv = Inventaire()
    inv.ajouter("pommes", 5)
    inv.ajouter("bananes", 3)
    assert inv.produits["pommes"] == 5

def test_total():
    inv = Inventaire()
    inv.ajouter("pommes", 5)
    inv.ajouter("bananes", 3)
    assert inv.total() == 8

def test_contient():
    inv = Inventaire()
    inv.ajouter("pommes", 5)
    inv.ajouter("bananes", 3)
    assert inv.contient("pommes")
    assert not inv.contient("oranges")
```

Les trois premières lignes de chaque test sont identiques. Avec trois tests,
c'est tolérable; avec trente, ça devient un problème de maintenance.

pytest résout ce problème avec les *fixtures* : des fonctions marquées par le
décorateur `@pytest.fixture`, qui préparent un contexte réutilisable. Pour
injecter une fixture dans un test, il suffit de la nommer comme paramètre de la
fonction de test. pytest se charge de l'appeler automatiquement et de passer le
résultat :

```python
# test_inventaire.py
import pytest
from inventaire import Inventaire

@pytest.fixture
def inventaire_garni():
    inv = Inventaire()
    inv.ajouter("pommes", 5)
    inv.ajouter("bananes", 3)
    return inv

def test_ajouter(inventaire_garni):
    assert inventaire_garni.produits["pommes"] == 5

def test_total(inventaire_garni):
    assert inventaire_garni.total() == 8

def test_contient(inventaire_garni):
    assert inventaire_garni.contient("pommes")
    assert not inventaire_garni.contient("oranges")
```

{{% hint info %}}
La fixture `inventaire_garni` est une fonction, et le fait que pytest puisse la
passer automatiquement en paramètre à une autre fonction (le test) repose sur
une propriété fondamentale de Python : les fonctions sont des **objets de
première classe** (*first-class objects*). Cela signifie qu'une fonction peut
être assignée à une variable, stockée dans une structure de données, ou passée
en argument à une autre fonction, exactement comme n'importe quelle autre
valeur. En coulisses, pytest inspecte les paramètres de chaque fonction de test,
repère ceux qui correspondent à des fixtures déclarées, les appelle, puis
transmet leurs résultats au test.
{{% /hint %}}

Le code de préparation n'existe plus qu'à un seul endroit. Si on veut changer
les données initiales, on modifie la fixture et tous les tests en bénéficient.

Un détail important : par défaut, pytest appelle la fixture *à nouveau* pour
chaque test qui l'utilise. Chaque test reçoit donc sa propre instance fraîche de
l'inventaire. Cela garantit que les tests sont isolés les uns des autres : si un
test modifie l'inventaire (par exemple en ajoutant un produit), cette
modification n'affecte pas les autres tests. C'est un principe fondamental en
testing : chaque test doit pouvoir s'exécuter indépendamment, dans n'importe
quel ordre, sans effet de bord.

Ce comportement correspond au scope `"function"`, qui est le scope par défaut.
Mais pytest offre d'autres scopes qui contrôlent la durée de vie d'une fixture :

- `"function"` (par défaut) : la fixture est recréée pour chaque test
- `"module"` : la fixture est créée une seule fois par fichier de test, puis
  partagée entre tous les tests de ce fichier
- `"session"` : la fixture est créée une seule fois pour l'ensemble de la suite
  de tests

```python
@pytest.fixture(scope="session")
def connexion_db():
    conn = creer_connexion("test.db")
    return conn
```

Les scopes plus larges sont utiles pour des ressources coûteuses à créer, comme
une connexion à une base de données. Mais ils introduisent un compromis : les
tests qui partagent une fixture ne sont plus complètement isolés. Il faut donc
les utiliser avec discernement.

Certaines fixtures doivent non seulement préparer un contexte, mais aussi le
nettoyer après le test. Par exemple, si une fixture crée un fichier temporaire,
on veut s'assurer que ce fichier est supprimé une fois le test terminé, peu
importe si le test a réussi ou échoué. pytest permet cela en utilisant `yield`
au lieu de `return` dans la fixture : le code avant `yield` s'exécute avant le
test, et le code après `yield` s'exécute après.

```python
import pytest
import os

@pytest.fixture
def fichier_temp():
    # Setup : créer le fichier
    chemin = "donnees_test.txt"
    with open(chemin, "w") as f:
        f.write("contenu de test")
    yield chemin
    # Teardown : nettoyer après le test
    os.remove(chemin)

def test_lecture(fichier_temp):
    with open(fichier_temp) as f:
        assert f.read() == "contenu de test"
    # Même si le test échoue, le fichier sera supprimé
```

{{% hint info %}}
Le mot-clé `yield` utilisé ici repose sur le mécanisme des **générateurs** de
Python. Un générateur est une fonction qui, au lieu de retourner une valeur
unique avec `return`, peut *suspendre* son exécution avec `yield` et la
*reprendre* plus tard exactement là où elle s'était arrêtée. C'est ce
comportement qui permet à pytest de découper la fixture en deux phases : tout ce
qui précède `yield` s'exécute avant le test (setup), puis l'exécution est
suspendue le temps du test, et tout ce qui suit `yield` s'exécute après
(teardown).
{{% /hint %}}

Ce mécanisme de setup/teardown garantit que les tests ne laissent pas de traces
derrière eux, ce qui est particulièrement important quand on manipule des
fichiers, des connexions réseau ou des bases de données.

Quand un projet grandit, les tests sont naturellement répartis dans plusieurs
fichiers. Si plusieurs de ces fichiers ont besoin de la même fixture, on
pourrait la copier dans chaque fichier, mais on retomberait dans le problème de
duplication qu'on cherchait justement à éviter. pytest offre une solution
élégante : le fichier `conftest.py`. Toute fixture définie dans un fichier
`conftest.py` est automatiquement disponible pour tous les fichiers de test du
même répertoire (et de ses sous-répertoires), sans aucun import explicite.

```
projet/
├── conftest.py           # fixtures partagées
├── test_inventaire.py
├── test_commandes.py
└── test_livraisons.py
```

```python
# conftest.py
import pytest
from inventaire import Inventaire

@pytest.fixture
def inventaire_garni():
    inv = Inventaire()
    inv.ajouter("pommes", 5)
    inv.ajouter("bananes", 3)
    return inv
```

Les trois fichiers de test peuvent maintenant utiliser `inventaire_garni` comme
paramètre de leurs fonctions de test, sans l'importer. pytest découvre le
`conftest.py` automatiquement et injecte les fixtures qu'il contient. On peut
aussi avoir plusieurs `conftest.py` à différents niveaux de l'arborescence :
chacun rend ses fixtures disponibles pour son répertoire et ses
sous-répertoires.

## Les tests paramétrés

Les fixtures éliminent la duplication du code de préparation, mais il existe une
autre forme de répétition très courante : tester la même logique avec plusieurs
entrées différentes. Par exemple, imaginons une fonction simple qui valide le
format d'une adresse courriel :

```python
def valider_courriel(courriel):
    """Vérifie qu'une adresse courriel a un format valide (version simplifiée)."""
    if "@" not in courriel:
        return False
    nom, domaine = courriel.split("@", 1)
    return len(nom) > 0 and "." in domaine
```

Pour vérifier qu'elle fonctionne avec différentes entrées, on pourrait écrire un
test par cas :

```python
def test_valide_normal():
    assert valider_courriel("alice@exemple.com") == True

def test_valide_sous_domaine():
    assert valider_courriel("bob@mail.exemple.com") == True

def test_invalide_sans_arobase():
    assert valider_courriel("alice.exemple.com") == False

def test_invalide_vide():
    assert valider_courriel("") == False
```

Chaque test ne diffère que par l'entrée et le résultat attendu, mais la
structure est identique. Le décorateur `@pytest.mark.parametrize` permet de
factoriser cette répétition en un seul test qui s'exécute avec chaque
combinaison de paramètres :

```python
import pytest

@pytest.mark.parametrize("courriel, attendu", [
    ("alice@exemple.com", True),
    ("bob@mail.exemple.com", True),
    ("alice.exemple.com", False),
    ("", False),
])
def test_valider_courriel(courriel, attendu):
    assert valider_courriel(courriel) == attendu
```

pytest génère automatiquement un test distinct pour chaque entrée du tableau. Si
le troisième cas échoue, pytest rapporte précisément quel jeu de paramètres a
posé problème, ce qui facilite le diagnostic. On peut aussi facilement ajouter de
nouveaux cas en ajoutant simplement une ligne au tableau, sans toucher à la
logique du test.

## Le mocking

Les fixtures résolvent le problème de la préparation répétitive des données de
test. Mais il reste un autre défi, plus subtil : comment tester du code qui
dépend de ressources externes? Une fonction qui appelle une API web, qui lit un
fichier de configuration, qui interroge une base de données ou qui vérifie
l'heure actuelle pose un problème fondamental pour les tests unitaires : on veut
tester la logique de *notre* code, pas le comportement du réseau, du système de
fichiers ou de l'horloge système. De plus, ces dépendances rendent les tests
lents, imprévisibles et difficiles à reproduire.

Le *mocking* (de l'anglais *mock*, « imitation ») consiste à remplacer
temporairement une dépendance réelle par un faux objet au comportement contrôlé.
Au lieu d'appeler véritablement une API, le test substitue un faux qui retourne
toujours la même réponse prédéfinie. Cela permet d'isoler le code qu'on teste et
de vérifier sa logique indépendamment du monde extérieur.

Prenons un exemple. Supposons qu'on ait une fonction qui récupère la météo d'une
ville via une API web :

```python
# meteo.py
import requests

def obtenir_temperature(ville):
    reponse = requests.get(f"https://api.meteo.example/ville/{ville}")
    donnees = reponse.json()
    return donnees["temperature"]

def message_meteo(ville):
    temp = obtenir_temperature(ville)
    if temp > 30:
        return f"Il fait chaud à {ville} ({temp}°C)"
    elif temp < 0:
        return f"Il fait froid à {ville} ({temp}°C)"
    else:
        return f"Température normale à {ville} ({temp}°C)"
```

On veut tester la logique de `message_meteo` : est-ce qu'elle produit le bon
message selon la température? Mais si on l'appelle directement dans un test,
elle va réellement contacter l'API, ce qui pose plusieurs problèmes : le test
nécessite une connexion internet, il est lent, et surtout, la température réelle
change constamment, ce qui rend le résultat imprévisible. On ne peut pas écrire
`assert message_meteo("Montréal") == "Il fait froid..."` si on ne contrôle pas
la température retournée.

pytest fournit une fixture intégrée appelée `monkeypatch` qui permet de
remplacer temporairement n'importe quel attribut, fonction ou variable
d'environnement pendant un test. Le remplacement est automatiquement annulé à la
fin du test, ce qui garantit l'isolation. Pour notre exemple, on peut utiliser
`monkeypatch.setattr` pour remplacer la fonction `obtenir_temperature` par une
fausse version qui retourne une valeur fixe :

```python
# test_meteo.py
from meteo import message_meteo
import meteo

def test_message_chaud(monkeypatch):
    monkeypatch.setattr(meteo, "obtenir_temperature", lambda ville: 35)
    assert message_meteo("Montréal") == "Il fait chaud à Montréal (35°C)"

def test_message_froid(monkeypatch):
    monkeypatch.setattr(meteo, "obtenir_temperature", lambda ville: -10)
    assert message_meteo("Montréal") == "Il fait froid à Montréal (-10°C)"

def test_message_normal(monkeypatch):
    monkeypatch.setattr(meteo, "obtenir_temperature", lambda ville: 20)
    assert message_meteo("Montréal") == "Température normale à Montréal (20°C)"
```

Aucun de ces tests ne contacte l'API. La fonction `obtenir_temperature` est
remplacée par un simple `lambda` (une fonction anonyme en Python, c'est-à-dire
une fonction définie en une seule ligne sans lui donner de nom :
`lambda ville: 35` est équivalent à écrire une fonction qui prend `ville` en
paramètre et retourne toujours 35) qui retourne la valeur qu'on veut tester. On
peut ainsi vérifier chaque branche de la logique de `message_meteo` de manière
déterministe et instantanée.

`monkeypatch` ne se limite pas au remplacement de fonctions. On peut aussi
l'utiliser pour simuler des variables d'environnement, ce qui est courant dans
les applications qui lisent leur configuration depuis l'environnement :

```python
# config.py
import os

def obtenir_mode():
    mode = os.environ.get("APP_MODE", "production")
    if mode == "debug":
        return "Mode débogage activé"
    return "Mode production"
```

```python
# test_config.py
from config import obtenir_mode

def test_mode_debug(monkeypatch):
    monkeypatch.setenv("APP_MODE", "debug")
    assert obtenir_mode() == "Mode débogage activé"

def test_mode_production(monkeypatch):
    monkeypatch.delenv("APP_MODE", raising=False)
    assert obtenir_mode() == "Mode production"
```

`monkeypatch.setenv` définit une variable d'environnement pour la durée du test,
et `monkeypatch.delenv` la supprime. Dans les deux cas, l'état original est
restauré automatiquement après le test.

`monkeypatch` est l'outil de mocking le plus naturel dans l'écosystème pytest,
grâce à sa simplicité et son intégration comme fixture. Mais il n'est pas le
seul : la bibliothèque standard de Python inclut le module `unittest.mock`, qui
offre des fonctionnalités plus avancées. Son objet `Mock` peut enregistrer
comment il a été appelé (combien de fois, avec quels arguments), ce qui permet
de vérifier non seulement le résultat d'une fonction, mais aussi son
*comportement* : a-t-elle bien appelé telle dépendance, avec les bons
paramètres? Ces vérifications comportementales sont utiles dans des cas plus
complexes, mais pour la majorité des tests unitaires, `monkeypatch` est
amplement suffisant.

## Le property-based testing

Dans tous les exemples vus jusqu'ici, nous avons écrit des tests avec des valeurs
spécifiques choisies à la main : `addition(2, 3)`, `factorielle(5)`,
`est_palindrome("kayak")`. Cette approche fonctionne bien, mais elle dépend
entièrement de notre capacité à imaginer les bons cas de test. Or, les bugs se
cachent souvent dans des cas auxquels on n'a pas pensé.

Le *property-based testing* propose une approche différente : au lieu de tester
des cas précis, on décrit une *propriété* que la fonction devrait toujours
respecter, et on laisse l'ordinateur générer automatiquement des centaines de cas
aléatoires pour essayer de la violer. En Python, la bibliothèque de référence
pour cela est **Hypothesis**.

Prenons un exemple. Une propriété fondamentale de notre fonction `addition` est
qu'elle devrait être commutative : `addition(a, b)` devrait toujours être égal à
`addition(b, a)`, peu importe les valeurs de `a` et `b`.

```python
# test_addition_avec_hypothesis.py
from hypothesis import given
from hypothesis.strategies import integers
from calcul import addition

@given(a=integers(), b=integers())
def test_addition_commutative(a, b):
    assert addition(a, b) == addition(b, a)
```

Quand on lance ce test, Hypothesis génère automatiquement des centaines de paires
d'entiers (positifs, négatifs, très grands, zéro) et vérifie la propriété pour
chacune. Si elle trouve un contre-exemple, elle le simplifie automatiquement pour
donner le cas le plus petit qui fait échouer le test.

On peut appliquer la même idée à notre fonction `est_palindrome`. Une propriété
intéressante : pour n'importe quelle chaine de caractères `s`, la concaténation
de `s` avec son inverse (`s + s[::-1]`) devrait *toujours* être un palindrome.

```python
# test_palindrome_avec_hypothesis.py
from hypothesis import given
from hypothesis.strategies import text
from palindrome import est_palindrome

@given(s=text())
def test_concatenation_inverse_est_palindrome(s):
    assert est_palindrome(s + s[::-1]) == True
```

Ce test va générer des centaines de chaines aléatoires, y compris des chaines
vides, des chaines avec des accents, des caractères spéciaux, des emojis, etc.
Si notre fonction a un bug subtil qui ne se manifeste qu'avec certains
caractères, Hypothesis a de bonnes chances de le trouver.

L'intérêt est puissant : on n'a plus besoin de deviner les bons cas de test, on
décrit ce qui *devrait être vrai*, et la machine se charge de chercher ce qui ne
l'est pas.

Le property-based testing est un cousin du *fuzzing*, une technique plus ancienne
issue du domaine de la sécurité informatique. Le fuzzing consiste à bombarder un
programme avec des entrées aléatoires ou semi-aléatoires pour provoquer des
crashes et révéler des vulnérabilités, sans formuler de propriété explicite. Il
est surtout utilisé dans les langages bas niveau comme C et C++, où les erreurs
mémoire sont courantes. Hypothesis peut être vu comme une version plus structurée
et plus intelligente du fuzzing, adaptée au monde du développement applicatif.

## Dans VS Code

Tout ce que cette section a construit se retrouve dans l'éditeur, et c'est
l'endroit où le voir d'un coup. Avec l'extension Python installée et le projet
d'exemple ouvert, une icône en forme d'éprouvette apparaît dans la barre
d'activité, celle qui porte l'explorateur de fichiers et la recherche&nbsp;: c'est
l'explorateur de tests. La première fois, il est vide, dit qu'aucun test n'a
encore été trouvé dans ce dossier, et propose un bouton « Configure Python
Tests », qui demande deux choses, le cadre de test, `pytest` ici plutôt que
`unittest`, celui de la bibliothèque standard, et le dossier qui contient les
tests. C'est tout. L'extension lance alors
la découverte, avec les mêmes règles que `pytest` au terminal, les fichiers
`test_*.py` et leurs fonctions `test_*`, et affiche l'arbre du projet&nbsp;: un
noeud par fichier, une feuille par test, y compris les tests paramétrés, qui
apparaissent avec un enfant par jeu de paramètres, et ceux d'Hypothesis, qui ne
se distinguent en rien des autres. La condition pour que cela fonctionne est
celle de l'encart précédent&nbsp;: l'interpréteur du venv doit être choisi, sinon
l'explorateur ne trouve ni `pytest` ni `hypothesis`, et reste vide.

{{< rangee >}}
{{< image src="vscode-tests-config.webp" alt="VS Code en thème sombre, le projet test-examples ouvert, la vue Testing affichée à gauche : elle dit qu'aucun test n'a encore été trouvé dans ce dossier et propose un bouton Configure Python Tests, encadré en rouge ; une flèche rouge désigne l'icône en forme d'éprouvette dans la barre d'activité, en bas" title="Avant la configuration : l'explorateur de tests est vide et propose de choisir le cadre de test et le dossier" loading="lazy" >}}
{{< image src="vscode-tests-cadre.webp" alt="La même vue, après un clic sur Configure Python Tests : une liste s'ouvre en haut de la fenêtre, Select a test framework/tool to enable, avec deux choix, unittest et pytest ; pytest est encadré en rouge et désigné par une flèche" title="Deuxième étape : choisir le cadre de test, pytest plutôt que unittest" loading="lazy" >}}
{{< /rangee >}}


Lancer, ensuite, se fait de trois endroits. Le bouton en haut de l'explorateur
lance tout. Dans un fichier de test ouvert, une petite icône de lancement se
trouve dans la marge, à côté de chaque fonction, et un clic n'exécute que ce
test-là, ce qui est le geste qu'on fait cent fois par jour quand on travaille
sur une fonction. Et la palette a ses commandes, `Test: Run All Tests`,
`Test: Run Tests in Current File`, `Test: Run Test at Cursor`. Dans les trois
cas, c'est `pytest` qui tourne, et le panneau « Test Results » le prouve&nbsp;:
il affiche la commande exacte, `pytest` avec ses arguments, puis la trace
habituelle, la liste des fichiers, les pourcentages, et « 17 passed ». Ce que l'éditeur ajoute, c'est le résultat à l'endroit même du
code&nbsp;: une coche verte ou une croix rouge devant chaque test, et, pour un test
qui échoue, un repère rouge sur la ligne même de sa définition, et le détail
de l'assertion dans le panneau « Test Results », sans avoir à remonter la
sortie du terminal.

{{< image src="vscode-tests-decouverts.webp" alt="VS Code en thème sombre, la vue Testing après la configuration : No test results yet, puis l'arbre Project test-examples avec ses six fichiers de test, test_addition_avec_hypothesis, test_calcul, test_inventaire, test_meteo, test_palindrome_avec_hypothesis, test_palindrome ; en haut de la vue, le bouton de lancement est encadré en rouge et désigné par une flèche" title="Les tests découverts, pas encore lancés : un noeud par fichier, et le bouton qui lance tout" loading="lazy" >}}

{{< image src="vscode-tests-vert.webp" alt="La même vue après le lancement : 17/17 en vert, 490 ms, chaque fichier coché ; au centre, le panneau Test Results montre la commande pytest exacte avec ses arguments, puis la sortie habituelle de pytest, platform darwin, Python 3.13.5, pytest 9.0.2, plugins hypothesis et cov, collected 17 items, les pourcentages par fichier et 17 passed in 0.23s ; à droite, la liste des dix-sept tests cochés" title="Tout vert, et la preuve que c'est pytest qui tourne : sa commande et sa trace dans le panneau Test Results" loading="lazy" >}}

Voyez maintenant un test qui échoue, et provoquez-le vous-même, c'est
l'affaire d'un caractère. Dans
`calcul.py`, remplacez le `+` de `addition` par un `-`, puis lancez
`test_calcul.py` depuis l'explorateur. Deux tests sur quatre rougissent,
`test_addition_simple` et `test_addition_negatifs`, la marge les marque d'une
croix, et le panneau montre la sortie de `pytest` telle que vous la
connaissez, `assert -1 == 5`, avec le détail que `-1` vient de
`addition(2, 3)`. Vous savez tout, sans avoir quitté l'éditeur. Remettez le
`+`, et gardez ce bogue en tête, la section suivante le reprend pour autre
chose que lire un message.

{{< image src="vscode-tests-rouge.webp" alt="VS Code en thème sombre après l'erreur volontaire dans addition : l'explorateur de tests affiche 2/4 en rouge, test_calcul.py encadré ; au centre, test_calcul.py avec une croix rouge dans la marge devant test_addition_simple et test_addition_negatifs, une coche verte devant les deux tests de factorielle ; à droite, le panneau Test Results montre la sortie de pytest, FAILURES, assert -1 == 5 where -1 = addition(2, 3), assert -2 == 0, et 2 failed, 2 passed in 0.09s" title="Deux rouges sur quatre : la croix dans la marge, et le détail de l'assertion dans Test Results, la sortie de pytest telle quelle" loading="lazy" >}}

Deux boutons de plus méritent d'être connus. Le premier lance les tests avec la
couverture, celle du chapitre sur la couverture de code&nbsp;: les lignes exécutées
et les lignes jamais atteintes se colorent directement dans l'éditeur, et un
onglet « Test Coverage » de l'explorateur donne le pourcentage par fichier. C'est
la manière la plus parlante de voir ce que ce chapitre disait, qu'une ligne
colorée a été exécutée, pas vérifiée. Le second bouton, une icône d'insecte,
lance un test sous le débogueur&nbsp;: on pose un point d'arrêt dans la fonction
testée, le test s'arrête dessus, et on regarde les variables au moment précis
où l'assertion va échouer. C'est souvent la manière la plus rapide de comprendre
un test rouge, et c'est l'objet de la section suivante.
