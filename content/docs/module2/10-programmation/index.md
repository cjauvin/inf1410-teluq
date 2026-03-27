---
title: "Survol rapide de la programmation"
slug: "programmation"
weight: 10
---

# Survol rapide de la programmation

Nous allons faire un survol rapide des idées les plus importantes et
fondamentales de la programmation logicielle. Pour aller droit au but, nous
allons utiliser le langage Python, qui est très facile à comprendre, presque
même sans expérience préalable.

## Structures de données fondamentales

Au-delà des types de base, qui sont généralement des nombres de différents types
(entiers, réels, etc) et les chaines de caractères (strings), nous avons les
structures de données, qui sont des constructions logiques plus complexes
(non-atomiques) qui impliquent, en général, les types de base, d'une manière ou
d'une autre (une liste, par exemple, doit être une liste de _quelque chose_,
d'entiers, de strings, etc).

Pourquoi commencer par les structures de données ? Rob Pike, l'un des créateurs
du langage Go (avec Ken Thompson, co-créateur d'Unix), a formulé dans ses
célèbres ["5 règles de
programmation"](https://www.cs.unc.edu/~stotts/COMP590-059-f24/robsrules.html)
une idée qui mérite d'être gardée en tête tout au long de cette section. Sa
règle 5 stipule : "Data dominates. If you've chosen the right data structures
and organized things well, the algorithms will almost always be self-evident."
(Les données dominent. Si vous avez choisi les bonnes structures de données et
bien organisé les choses, les algorithmes seront presque toujours évidents.)
Pike attribue lui-même cette idée à Fred Brooks, l'auteur de *The Mythical
Man-Month*, un ouvrage fondamental dont nous avons parlé dans le module 1. En
d'autres mots, les structures de données ne sont pas un simple préalable
technique : elles sont au coeur de la programmation, et le choix de la bonne
structure dicte souvent la solution à un problème.

### La liste et le `set`

La liste est une structure de données qui est une collection de valeurs, par
exemple en Python, où les listes sont très naturelles et puissantes :

{{< pyodide >}}
a = [10, 20, 30]
print(a)
{{< /pyodide >}}

Il est possible d'y ajouter, ou d'enlever des éléments :

{{< pyodide >}}
a.append(40)
print(a)
a.remove(10)
print(a)
print(len(a))
{{< /pyodide >}}

{{< image src="list.png" alt="" title="" loading="lazy" >}}

La liste a une taille et ses éléments ont un ordre. En contraste, le `set` a une taille, mais ses éléments
n'ont aucun ordre (il s'agit d'un "sac" de valeurs). Il est également possible de lui ajouter ou enlever
des éléments :

{{< pyodide >}}
s = {10, 20, 30, 40}
print(len(s))
s.add(50)
s.remove(20)
print(s)
{{< /pyodide >}}

Il est d'une importance **capitale** d'avoir un modèle mental **archi-clair** de
la différence entre ces deux structures de données à l'apparence si semblable,
pour la raison fondamentale suivante : **chercher un item dans une liste a un coût
proportionnel à la taille de la liste, tandis que chercher un item dans un `set`
se fait en temps constant en moyenne** :

{{< pyodide >}}
print(20 in a)  # coût proportionnel à la taille de `a`
print(20 in s)  # coût fixe, extrêmement faible !
{{< /pyodide >}}

{{< image src="set.png" alt="" title="" loading="lazy" >}}

Imaginez que vous cherchiez une aiguille dans une botte de foin :

{{< image src="haystack.png" alt="" title="" loading="lazy" >}}

Préférez-vous que votre botte de foin soit :

1. Une liste
2. Un `set`

### Le dictionnaire (table associative, etc)

La notion de "table associative" a plusieurs noms, selon les langages et les
cultures de programmation :

1. On parle d'un `dict` en Python (pour dictionnaire)
2. D'un `Object` en JavaScript (ou `{}`, à ne pas confondre avec les "objets" de la programmation orientée-objet, bien que ces concepts sont reliés)
3. Un `Hash` en Ruby
4. Un `array` (associatif) en PHP
5. Une `table` en Lua
6. Une `map` en Go
etc.

Il s'agit d'une autre famille de structures de données pour laquelle il est
crucial d'avoir un modèle mental clair et limpide. Une manière de se représenter
le fonctionnement d'une table associative est en tant qu'extension d'un `set` :
imaginons qu'à chaque élément (ou valeur) d'un `set`, nous attachons une valeur.

{{< image src="dict.png" alt="" title="" loading="lazy" >}}

On considère le `dict` comme une structure de données plus versatile et générale
que les autres parce qu'il est possible d'implémenter, par exemple, une liste
avec un `dict` :

{{< image src="dict-as-list.png" alt="" title="" loading="lazy" >}}

Il est aussi possible d'implémenter un `set` avec un `dict` :

{{< image src="dict-as-set.png" alt="" title="" loading="lazy" >}}

### Le dictionnaire en tant que `record`

Étant donné la structure du dictionnaire, il est souvent possible de l'utiliser
en tant
qu'[enregistrement](https://fr.wikipedia.org/wiki/Enregistrement_(structure_de_donn%C3%A9es))
(record en anglais, plus couramment), c'est-à-dire en tant que contenant pouvant
contenir des valeurs diverses pour un "object". Ce type d'usage est très courant dans
les langages de plus haut niveau. Par exemple en Python :

{{< pyodide >}}
# =========================
# 1) dict
# =========================

person_dict = {
    "name": "Alice",
    "age": 30
}

print("DICT:")
print(person_dict["name"])
print(person_dict["age"])


# =========================
# 2) class
# =========================

class PersonClass:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

person_class = PersonClass("Alice", 30)

print("\nCLASS:")
print(person_class.name)
print(person_class.age)


# =========================
# 3) dataclass
# =========================

from dataclasses import dataclass

@dataclass
class PersonDataClass:
    name: str
    age: int

person_dataclass = PersonDataClass("Alice", 30)

print("\nDATACLASS:")
print(person_dataclass.name)
print(person_dataclass.age)
{{< /pyodide >}}

Ou encore en JavaScript, avec l'[object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object), qui ressemble au `dict` Python :

```js
/*
Exemples simples de "record" en JavaScript :
- objet littéral
- class
- objet immuable (style record)
*/

////////////////////
// 1) Objet littéral
////////////////////

const personObject = {
  name: "Alice",
  age: 30
};

console.log("OBJECT:");
console.log(personObject.name);
console.log(personObject.age);


////////////////////
// 2) Class
////////////////////

class PersonClass {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
}

const personClass = new PersonClass("Alice", 30);

console.log("\nCLASS:");
console.log(personClass.name);
console.log(personClass.age);


////////////////////////////////////
// 3) Objet immuable (record-like)
////////////////////////////////////

const personRecord = Object.freeze({
  name: "Alice",
  age: 30
});

console.log("\nIMMUTABLE OBJECT:");
console.log(personRecord.name);
console.log(personRecord.age);
```

### L'implémentation du dictionnaire

Nous avons jusqu'ici parlé du dictionnaire du point de vue des langages de
programmation d'assez haut niveau, comme Python et JS. Ceux-ci permettent
d'utiliser un dictionnaire, mais en cache un aspect crucial : leur
implémentation ! Étant donné que Python, le langage lui-même, est écrit dans le
langage C, comment écrit-on un `dict` Python, en C? Il existe plusieurs manières
de le faire, mais l'une d'elles est [table de
hachage](https://fr.wikipedia.org/wiki/Table_de_hachage) (hash table en
anglais). En gros, l'idée est d'appliquer une [fonction de hachage]({{< ref
"/docs/module2/30-versioning#fonction-de-hachage" >}}) à un élément (la clé), ce
qui permet de déterminer l'index dans un tableau, où on pourra mettre la valeur
associée. On constate donc que si on regarde "sous le capot", un dictionnaire
est fondamentalement une liste, dans ce sens. Dans certaines implémentations, il
est nécessaire de gérer les collisions possibles : si deux clés mènent au même
index par exemple, il sera possible d'utiliser une liste, pour cette clé
particulière.

{{< image src="hashtable.png" alt="" title="" loading="lazy" >}}

### La correspondance avec JSON

Une fois que vous avez des modèles mentaux clairs et efficaces par rapport aux
différences et similarités de ces trois structures de données dont nous avons
parlées dans cette section (listes, sets et dictionnaires), il est utile de
considérer leur correspondance assez directe avec la notation JSON.

JSON (JavaScript Object Notation) est un format textuel léger destiné à
représenter des données structurées de façon simple et lisible, à partir de
quelques constructions de base : objets clé-valeur, tableaux ordonnés et valeurs
primitives. Conçu à l’origine pour les échanges de données dans les applications
Web, il correspond étroitement aux structures de données que l’on retrouve dans
la plupart des langages de programmation modernes, ce qui explique son adoption
massive comme format d’échange entre systèmes, en particulier dans les API et
les applications distribuées.

```json
{
  "nom": "Alice",
  "age": 30,
  "competences": ["Python", "JavaScript", "SQL"],
  "adresse": {
    "ville": "Montréal",
    "pays": "Canada"
  }
}
```

La totalité d'un document JSON est souvent un dictionnaire (que l'on reconnaît à
l'usage des `{}`), mais un document JSON complet peut aussi être un tableau, une
chaîne, un nombre, un booléen ou `null`. Il existe aussi des formats apparentés
(JSONL, NDJSON, etc). Quand le document JSON est un dictionnaire, il contient la
plupart du temps des champs (clés) dont les valeurs peuvent être, elles-mêmes,
des dictionnaires, des listes ou des valeurs scalaires (nombres, chaines de
caractères ou valeurs booléennes).

## Complexité algorithmique et performance

Le sujet de la [complexité
algorithmique](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_la_complexit%C3%A9_(informatique_th%C3%A9orique))
est en général présenté et discuté de manière très mathématique (et même parfois
carrément
[philosophique](https://fr.wikipedia.org/wiki/Probl%C3%A8me_P_%E2%89%9F_NP)),
mais la plupart des programmeurs d'expérience en ont un modèle mental assez
simplifié.

La préoccupation fondamentale à la base de sujet est la performance d'un
algorithme, ou en termes encore plus simples le temps qu'il prend à exécuter.
Bien qu'en pratique les détails d'implémentation (comment un programme est
écrit) et les particularités matérielles de l'environnement où il est exécuté
(l'ordinateur particulier qui est utilisé) sont très importants, en général
quand on parle de complexité algorithmique on a en tête quelque chose de plus
abstrait.

Examinons certains exemples. Imaginons tout d'abord que nous avons une fonction
qui construit une liste de `N` nombres entiers aléatoires (entre 1 et `N`) :

{{< pyodide >}}
import random

def get_random_numbers(n):
    return [random.randint(1, n) for _ in range(n)]

a = get_random_numbers(10)

print(a)
{{< /pyodide >}}

Imagions ensuite que nous aimerions savoir si une paire de nombres distincts,
dans cette liste, résulte en une somme donnée `K`.

{{< image src="two-sum.png" alt="" title="" loading="lazy" >}}

Une méthode naive pour résoudre ce problème consiste à considérer toutes les
paires :

{{< image src="two-sum-quadratic.png" alt="" title="" loading="lazy" >}}

{{< pyodide >}}
def two_sum_quadratic_version(a, k):
    for i, x in enumerate(a):
        for j, y in enumerate(a):
            if i == j: continue
            if x + y == k:
                return (x, y)

    return None

print("Fonction 'two_sum_quadratic_version' définie.")
{{< /pyodide >}}

Cette méthode est assez coûteuse parce que pour chaque item de la liste (qui
contient `N` items), il faut considérer une sous-liste (en fait la même liste,
implicitement), de `N` éléments. Il faut donc faire, au maximum, $N^2$ (`N` au
carré) vérifications. On parle donc d'un algorithme de complexité
[_quadratique_](https://fr.wikipedia.org/wiki/Fonction_quadratique). On utilise
parfois la notation appelée ["Grand
O"](https://fr.wikipedia.org/wiki/Comparaison_asymptotique#La_famille_de_notations_de_Landau_O,_o,_%CE%A9,_%CF%89,_%CE%98,_~)
pour décrire la complexité algorithmique d'une fonction, dans ce cas $O(N^2)$.

Si on y pense un peu, une méthode beaucoup plus efficace consisterait à utiliser
un `set` pour conserver les valeurs qu'on a déjà rencontrées, et à chaque
nouvelle valeur de la liste (à ne pas confondre avec le `set`!), tester si "`K`
moins la nouvelle valeur" se trouve dans le `set` :

{{< image src="two-sum-linear.png" alt="" title="" loading="lazy" >}}

{{< pyodide >}}
def two_sum_linear_version(a, k):
    seen = set()
    for x in a:
        target = k - x
        if target in seen:
            return (x, target)
        seen.add(x)

    return None

print("Fonction 'two_sum_linear_version' définie.")
{{< /pyodide >}}

La raison pour laquelle cet algorithme est beaucoup plus efficace est due au
fait que tester l'inclusion d'un item dans un `set` (ce qui se fait, dans le
code ci-haut, à l'aide de l'opérateur `in`, dans la ligne `if target in seen`),
contrairement au fait de le faire dans une liste, est extrêmement efficace : si
on utilise la notation "grand O", on dit que chercher un item dans une liste est
$O(N)$, alors que le faire dans un `set` est en moyenne $O(1)$, c'est-à-dire en
temps constant. Mais étant donné que nous devons tout de même passer à travers
tous les items de la liste une seule fois, la complexité finale de l'algorithme
reste tout de même $O(N)$, ce qu'on appelle une complexité linéaire.

Pour comparer de manière empirique la performance de ces deux algorithmes, nous
avons besoin de considérer plusieurs résultats (c-à-d plusieurs sommes
possibles), car un seul appel pourrait être "chanceux" (la première paire
considérée est tout de suite la bonne). On peut utiliser cette fonction, qui
prend en entrée une variable `fn`, qui va contenir la fonction qui sera exécutée
(`two_sum_linear_version` ou `two_sum_quadratic_version`) :

{{< pyodide >}}
def test_algo(fn, a):
    for k in range(len(a)):
        res = fn(a, k)
        if res:
            assert res[0] + res[1] == k

print("Fonction 'test_algo' définie.")
{{< /pyodide >}}

Quand la taille de la liste est raisonnable, la différence entre les deux
algorithmes n'est pas si notable (ici on utilise la console
[ipython](https://ipython.org/), qui possède des fonctionnalités pratiques pour
mesurer le temps d'exécution)&nbsp;

{{< pyodide >}}
import time

a = get_random_numbers(1000)

start = time.time()
test_algo(two_sum_quadratic_version, a)
print(f"Quadratique: {time.time() - start:.3f}s")

start = time.time()
test_algo(two_sum_linear_version, a)
print(f"Linéaire: {time.time() - start:.3f}s")
{{< /pyodide >}}

Mais si on augmente `N`, la différence devient rapidement assez dramatique :

{{< pyodide >}}
a = get_random_numbers(5000)

start = time.time()
test_algo(two_sum_quadratic_version, a)
print(f"Quadratique: {time.time() - start:.3f}s")

start = time.time()
test_algo(two_sum_linear_version, a)
print(f"Linéaire: {time.time() - start:.3f}s")
{{< /pyodide >}}

Il est très important de comprendre à quel point l'utilisation de la bonne
structure de données est cruciale, pour certains algorithmes. Si on remplace
le `set` de la méthode linéaire par une liste, elle redevient quadratique :

{{< pyodide >}}
def two_sum_falsely_linear_version(a, k):
    seen = []
    for x in a:
        target = k - x
        if target in seen:
            return (x, target)
        seen.append(x)

    return None

print("Fonction 'two_sum_falsely_linear_version' définie.")
{{< /pyodide >}}

{{< image src="two-sum-falsely-linear.png" alt="" title="" loading="lazy" >}}

{{< pyodide >}}
start = time.time()
test_algo(two_sum_falsely_linear_version, a)
print(f"Faussement linéaire: {time.time() - start:.3f}s")
{{< /pyodide >}}

Nous avons dit que cet algorithme est "faussement linéaire", et qu'il est en
fait quadratique, en raison de l'usage de la liste (plutôt qu'un `set`). Mais
pourquoi la performance semble être "entre les deux", dans ce cas particulier,
si on compare les temps d'exécution? La réponse est que l'opérateur `in` est
fortement optimisé en Python (qui est lui-même écrit dans le langage C), et
qu'il est beaucoup plus efficace que ce qu'on pourrait faire nous-même, avec
notre propre boucle `for`. On peut donc en dégager une idée générale, un modèle
mental simplifié avec lequel il est possible de faire beaucoup de chemin : la
complexité algorithmique se réduit souvent à la question du nombre de boucles
`for` imbriquées que notre code contient ! Chaque boucle imbriquée
supplémentaire correspond à un facteur par lequel on multiplie le temps
d'exécution de notre algorithme, en gros. On peut donc généraliser ce principe,
et comprendre qu'un algorithme qui contiendrait trois boucles `for` imbriquées,
par exemple, serait $O(N^3)$, ce qui serait évidemment encore plus coûteux.

### Au-delà et en-deça de la complexité polynomiale

Nous avons vu jusqu'ici des algorithmes et des structures de données qui ont
suggéré un ordre dans la complexité : $O(1)$ (temps constant), qui est le plus
rapide, à privilégier quand c'est possible évidemment, $O(N^2)$, le temps
quadratique, qui est beaucoup moins efficace. Et nous avons vu qu'il est
possible de généraliser au-delà : $O(N^3)$, temps cubique, etc. On appelle cette
classe de performance _polynomiale_.

Il existe cependant d'autres profils de performance dont il est utile de
connaître l'existence. Supposons qu'on ait une liste triée de nombres, et qu'on
cherche un nombre particulier dans cette liste :

{{< image src="sorted-list.png" alt="" title="" loading="lazy" >}}

Est-ce qu'il existe un algorithme plus performant que $O(N)$ pour ce problème?

{{< image src="binary-search.png" alt="" title="" loading="lazy" >}}

Cet algorithme très fameux s'appelle la "recherche binaire", et son temps
d'exécution est $O(log N)$, car il s'agit essentiellement d'une série de
"division par deux" (à chaque fois qu'on coupe la liste en deux), l'inverse donc
d'une multiplication. Dans le contexte de ce que nous avons vu jusqu'à
maintenant, il  s'agit donc d'une performance intermédiaire, entre $O(1)$ et
$O(N)$. Dans la pratique, si un tel algorithme est possible, c'est souvent
extrêmement avantageux, car la fonction $log(N)$ progresse beaucoup plus
lentement qu'une fonction linéaire ($O(N)$).

Dans le problème précédent, une difficulté était cachée : comment fait-on pour
trier une liste, et quel coût ça a? Pour les algorithmes de tri fondés sur des
comparaisons, la meilleure performance générale possible est $O(N log N)$, ce
qu'on appelle parfois une méthode supra-linéaire, et qui se trouve entre $O(N)$
et $O(N^2)$. Il est mathématiquement impossible de faire mieux qu'une
performance supra-linéaire dans ce cadre général.

Finalement, certains algorithmes ont des profils de performance encore plus
coûteux que la classe polynomiale : ils nécessitent un temps exponentiel, par
exemple $O(2^N)$. Voici certains exemples fameux de problèmes pour lesquels les
algorithmes exacts ou les généralisations théoriques les plus naturelles mènent
à des coûts exponentiels :

{{< image src="tsp.png" alt="" title="" loading="lazy" >}}

Le [problème du voyageur de
commerce](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_voyageur_de_commerce),
qui consister à déterminer le circuit le plus court passant par une série de
villes, dans un graphe.

Les échecs :

{{< image src="chess.png" alt="" title="" loading="lazy" >}}

Et finalement, le jeu de Sudoku :

{{< image src="sudoku.png" alt="" title="" loading="lazy" >}}

## Les paradigmes de programmation

Nous avons vu comment organiser les données avec les structures de données, et
comment mesurer l'efficacité d'un algorithme avec la complexité. Mais il existe
un autre axe fondamental selon lequel les langages et les programmes varient :
la manière dont on organise le code lui-même. On appelle cela un *paradigme* de
programmation. Un paradigme n'est pas simplement une question de syntaxe ou de
préférence personnelle : c'est une façon de penser un problème, de le
décomposer, et de structurer sa solution. Tout comme le choix d'une structure de
données influence profondément la performance d'un algorithme, le choix d'un
paradigme influence la manière dont on conçoit, lit et maintient un programme.

### Le paradigme impératif

Le paradigme le plus ancien et le plus intuitif est le paradigme *impératif* :
un programme est une séquence d'instructions qui modifient l'état du programme,
étape par étape. C'est la manière la plus directe de dire à l'ordinateur *quoi
faire*, dans quel ordre. Les premiers langages de programmation, comme Fortran
(1957) et COBOL (1959), étaient entièrement impératifs.

Une variante importante du paradigme impératif est la *programmation
procédurale*, qui consiste à regrouper des séquences d'instructions dans des
fonctions (ou procédures) réutilisables. Le langage C (1972) en est l'exemple
canonique. C'est aussi dans ce contexte que Dijkstra a mené sa célèbre croisade
contre l'instruction `goto`, arguant que les programmes devraient être
structurés à l'aide de boucles et de conditions plutôt que de sauts arbitraires.
Cette idée, connue sous le nom de *programmation structurée*, est aujourd'hui si
universellement adoptée qu'on n'y pense même plus.

Voici un exemple simple en Python, dans un style purement impératif. On veut
extraire les nombres pairs d'une liste et les mettre au carré :

{{< pyodide >}}
nombres = [1, 2, 3, 4, 5, 6, 7, 8]
résultat = []
for n in nombres:
    if n % 2 == 0:
        résultat.append(n ** 2)
print(résultat)  # [4, 16, 36, 64]
{{< /pyodide >}}

On reconnaît le style impératif : une boucle qui parcourt les éléments un par
un, une condition, une modification explicite de l'état (la liste `résultat` qui
grandit à chaque itération).

### Le paradigme orienté-objet

Le paradigme *orienté-objet* (OOP) propose une autre manière de structurer un
programme : au lieu de penser en termes de séquences d'instructions, on pense en
termes d'*objets* qui encapsulent à la fois des données et des comportements.
L'idée fondatrice est que le monde réel est composé d'entités qui ont des
propriétés et qui interagissent entre elles, et que nos programmes devraient
refléter cette structure.

Les racines de l'OOP remontent au langage Simula (1967), créé par Ole-Johan
Dahl et Kristen Nygaard en Norvège pour des problèmes de simulation. Mais c'est
Alan Kay, avec Smalltalk dans les années 1970 au Xerox PARC, qui a
véritablement cristallisé la vision de la programmation orientée-objet. Pour
Kay, l'idée centrale n'était pas tant les classes ou l'héritage, mais le
*passage de messages* entre objets autonomes. Il a d'ailleurs déclaré plus tard
regretter d'avoir utilisé le terme "orienté-objet", car il aurait préféré qu'on
retienne l'idée de messagerie plutôt que celle d'objet.

Les concepts centraux de l'OOP sont l'*encapsulation* (regrouper données et
comportements dans un objet, en cachant les détails internes), l'*héritage*
(créer de nouvelles classes à partir de classes existantes) et le
*polymorphisme* (traiter des objets de types différents de manière uniforme).
Voici un exemple simple qui illustre ces trois concepts :

{{< pyodide >}}
class CompteBancaire:
    def __init__(self, titulaire, solde=0):
        self.titulaire = titulaire
        self.solde = solde

    def déposer(self, montant):
        self.solde += montant

    def retirer(self, montant):
        if montant > self.solde:
            print("Fonds insuffisants")
        else:
            self.solde -= montant

    def afficher(self):
        print(f"{self.titulaire} : {self.solde} $")

class CompteÉpargne(CompteBancaire):
    def __init__(self, titulaire, solde=0, taux=0.02):
        super().__init__(titulaire, solde)
        self.taux = taux

    def appliquer_intérêts(self):
        self.solde += self.solde * self.taux

compte1 = CompteBancaire("Alice", 1000)
compte2 = CompteÉpargne("Bob", 5000, taux=0.03)

for compte in [compte1, compte2]:
    compte.déposer(500)
    compte.afficher()
# Alice : 1500 $
# Bob : 5500 $

compte2.appliquer_intérêts()
compte2.afficher()
# Bob : 5665.0 $
{{< /pyodide >}}

On voit ici les trois piliers de l'OOP en action. L'*encapsulation* : chaque
compte regroupe ses données (`titulaire`, `solde`) et ses opérations (`déposer`,
`retirer`). L'*héritage* : `CompteÉpargne` étend `CompteBancaire` en ajoutant
un taux d'intérêt, sans réécrire la logique de base. Le *polymorphisme* : dans
la boucle `for`, on traite les deux types de comptes de manière uniforme, car
ils partagent la même interface. L'OOP a dominé le développement logiciel
pendant des décennies, notamment à travers des langages comme C++ (1985), Java
(1995) et C# (2000), et elle reste le paradigme dominant dans l'industrie
aujourd'hui.

### Le paradigme fonctionnel

Le paradigme *fonctionnel* aborde la programmation sous un angle radicalement
différent : au lieu de décrire une séquence de modifications d'état, on exprime
un programme comme une composition de *fonctions pures*, c'est-à-dire des
fonctions qui retournent toujours le même résultat pour les mêmes arguments, et
qui ne produisent aucun effet secondaire (pas de modification de variable
externe, pas d'écriture sur disque, etc.).

Les origines du paradigme fonctionnel sont remarquablement anciennes. Elles
remontent au *lambda calcul*, un formalisme mathématique développé par Alonzo
Church dans les années 1930, avant même l'invention des ordinateurs. Le premier
langage fonctionnel, Lisp, a été créé par John McCarthy en 1958 au MIT, ce qui
en fait l'un des plus vieux langages encore utilisés aujourd'hui (sous des
formes modernisées comme Clojure). D'autres langages fonctionnels influents
incluent Haskell (1990), qui pousse le paradigme à sa forme la plus pure, et
Erlang (1986), conçu pour les systèmes téléphoniques hautement concurrents chez
Ericsson.

Deux idées centrales du paradigme fonctionnel méritent une attention
particulière. La première est l'*immutabilité* : plutôt que de modifier une
structure de données existante, on en crée une nouvelle. Cela élimine toute une
classe de bugs liés aux modifications inattendues de l'état. La seconde est
l'usage de *fonctions d'ordre supérieur*, c'est-à-dire des fonctions qui
prennent d'autres fonctions en argument ou qui en retournent. Les plus célèbres
sont `map`, `filter` et `reduce`, qui permettent de transformer des collections
de données de manière déclarative.

Reprenons notre exemple, cette fois dans un style fonctionnel en Python :

{{< pyodide >}}
nombres = [1, 2, 3, 4, 5, 6, 7, 8]
résultat = list(map(lambda n: n ** 2, filter(lambda n: n % 2 == 0, nombres)))
print(résultat)  # [4, 16, 36, 64]
{{< /pyodide >}}

On remarque qu'il n'y a ici aucune boucle, aucune variable qui s'accumule : on
*déclare* ce qu'on veut (filtrer les pairs, puis mettre au carré) plutôt que de
décrire *comment* le faire étape par étape. La liste d'origine n'est jamais
modifiée. Ce style est souvent qualifié de *déclaratif*, par opposition au style
*impératif*.

### Les langages multi-paradigmes

En pratique, la plupart des langages modernes ne se limitent pas à un seul
paradigme. Python en est un excellent exemple : nous venons d'écrire le même
programme dans trois styles différents, et les trois sont du Python parfaitement
valide. On peut écrire du Python impératif, orienté-objet ou fonctionnel, selon
ce qui convient le mieux au problème à résoudre. D'ailleurs, Python offre une
syntaxe qui se situe quelque part entre le style impératif et le style
fonctionnel, les *compréhensions de liste* (list comprehensions) :

{{< pyodide >}}
nombres = [1, 2, 3, 4, 5, 6, 7, 8]
résultat = [n ** 2 for n in nombres if n % 2 == 0]
print(résultat)  # [4, 16, 36, 64]
{{< /pyodide >}}

Cette tendance au mélange des paradigmes est une caractéristique forte de
l'évolution récente des langages de programmation. JavaScript a ajouté les
classes (empruntées à l'OOP) tout en renforçant ses capacités fonctionnelles
avec les fonctions fléchées et les méthodes comme `map`, `filter` et `reduce`.
Java, longtemps le bastion de l'OOP pure, a introduit les expressions lambda et
les streams dans sa version 8 (2014). Rust combine programmation système de bas
niveau, traits inspirés de l'OOP et influences fonctionnelles comme le pattern
matching et l'immutabilité par défaut.

La leçon à retenir est qu'un paradigme n'est pas un dogme, mais un *outil de
pensée*. Un bon programmeur connaît plusieurs paradigmes et sait choisir celui
qui exprime le plus clairement son intention dans un contexte donné. Nous
verrons dans le module 3 comment ces choix de paradigme influencent directement
l'architecture des systèmes logiciels.

## Les types

Nous avons vu que le choix de la bonne structure de données peut avoir un impact
fondamental sur la performance d'un programme. Les types sont un autre concept
fondamental de la programmation, et ils jouent un rôle analogue mais différent :
alors que les structures de données organisent l'information, les types
permettent de contraindre et de clarifier la nature de cette information. En ce
sens, ils constituent un outil puissant pour formaliser notre modèle mental de ce
que notre programme manipule, et de ce qu'il est censé faire. Cette idée devient
encore plus centrale dans le contexte de la programmation orientée-objet, où les
types ne se limitent pas à décrire des valeurs simples, mais définissent des
entités complètes avec leurs données et leurs comportements.

### Typage statique vs dynamique

Pour bien comprendre cette distinction, il est utile de rappeler qu'il existe
deux grandes familles de langages de programmation. Les langages compilés, comme
C ou Rust, passent par une étape de compilation qui transforme le code source en
un programme exécutable, avant que celui-ci ne puisse être lancé. Les langages
interprétés, comme Python ou JavaScript, sont exécutés directement, ligne par
ligne, par un interpréteur, sans cette étape préalable de transformation. En
réalité, cette distinction est davantage un spectre qu'une frontière nette :
Java, par exemple, compile le code source en un format intermédiaire appelé
bytecode, qui est ensuite interprété par une machine virtuelle (la JVM). Python
fait quelque chose de similaire avec ses fichiers `.pyc`, bien qu'on le
considère généralement comme un langage interprété.

La distinction entre typage statique et dynamique est étroitement liée à celle
entre compilation et interprétation. Dans un langage à typage statique, comme C,
Rust ou Java, le type de chaque variable doit être connu au moment de la
compilation, avant même que le programme ne s'exécute. Le compilateur peut ainsi
détecter toute une classe d'erreurs avant l'exécution. Dans un langage à typage
dynamique, comme Python ou JavaScript, les types ne sont vérifiés qu'au moment
de l'exécution : on peut assigner n'importe quelle valeur à n'importe quelle
variable, et c'est seulement quand le programme tente une opération incompatible
qu'une erreur survient.

En Python, par exemple, rien n'empêche de changer le type d'une variable en
cours de route :

{{< pyodide >}}
x = 42        # x est un entier
x = "hello"   # x est maintenant une chaine de caractères
x = [1, 2, 3] # x est maintenant une liste
print(x)
{{< /pyodide >}}

En C, le type d'une variable est fixé à la déclaration, et le compilateur refuse
toute incohérence :

```c
int x = 42;
x = "hello";  // erreur de compilation !
```

### Typage fort vs faible

La distinction entre typage statique et dynamique est souvent confondue avec une
autre distinction, tout aussi importante : celle entre typage fort et typage
faible. Un langage à typage fort refuse les opérations entre types
incompatibles, même au moment de l'exécution. Un langage à typage faible, au
contraire, tentera de convertir implicitement les valeurs pour que l'opération
puisse se faire, ce qui peut mener à des résultats surprenants.

Python, bien que dynamique, est un langage à typage fort :

{{< pyodide >}}
"5" + 3  # TypeError !
{{< /pyodide >}}

JavaScript, également dynamique, est à typage faible :

```js
"5" + 3  // "53" (!)
```

On voit donc que ces deux axes sont indépendants l'un de l'autre. On peut les
combiner pour situer les langages les plus courants :

| | Typage fort | Typage faible |
|---|---|---|
| **Statique** | Rust, Java | C |
| **Dynamique** | Python | JavaScript |

C est un cas intéressant : bien qu'il soit statique, son typage est considéré
comme relativement faible, car il permet des conversions implicites entre types
numériques et des manipulations directes de la mémoire via les pointeurs, ce qui
peut mener à des comportements non détectés par le compilateur.

### Les type hints en Python

Une tendance intéressante dans l'évolution des langages modernes est l'ajout
d'un typage statique optionnel à des langages historiquement dynamiques. Python a
introduit les type hints à partir de la version 3.5, et TypeScript est
essentiellement JavaScript avec un système de types statiques ajouté par-dessus.

En Python, les type hints permettent d'annoter les types des paramètres et des
valeurs de retour d'une fonction :

```python
def addition(a: int, b: int) -> int:
    return a + b
```

Il est important de comprendre que Python n'impose pas lui-même ces annotations
au moment de l'exécution. Elles servent plutôt de documentation formelle, qui
peut être vérifiée par un outil externe comme `mypy`, avant l'exécution :

```shell
$ mypy exemple.py
exemple.py:4: error: Argument 2 to "addition" has incompatible type "str"; expected "int"
```

On obtient ainsi une partie des avantages du typage statique (la détection
précoce d'erreurs), tout en conservant la flexibilité d'un langage dynamique.
C'est un compromis de plus en plus populaire dans l'industrie.

### Les types et les schémas

L'idée de contraindre la forme des données ne se limite pas aux langages de
programmation. Quand on valide un document JSON contre un schéma JSON, on fait
essentiellement la même chose que ce que fait un compilateur quand il vérifie les
types : on s'assure que les données respectent une structure attendue, avant de
les utiliser. Considérons par exemple un schéma JSON qui décrit une personne :

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "nom": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["nom", "age"]
}
```

Un document comme `{"nom": "Alice", "age": 30}` serait valide selon ce schéma,
mais `{"nom": "Alice", "age": "trente"}` serait rejeté, exactement comme un
compilateur refuserait de passer une chaine de caractères là où un entier est
attendu.

Cette même idée se retrouve dans les bases de données relationnelles, où le
schéma d'une table définit le nom et le type de chaque colonne. Par exemple, une
table `personnes` pourrait être définie ainsi en SQL :

```sql
CREATE TABLE personnes (
    nom TEXT NOT NULL,
    age INTEGER NOT NULL
);
```

On retrouve donc la même idée fondamentale à trois niveaux différents : les
types dans un langage de programmation, les schémas JSON pour valider des
documents échangés entre systèmes, et les schémas de bases de données pour
structurer les données persistantes. Dans tous les cas, il s'agit de formaliser
nos attentes sur la forme des données, pour que les erreurs soient détectées le
plus tôt possible. Nous reviendrons en détail sur les bases de données et leurs
schémas dans le module 3.
