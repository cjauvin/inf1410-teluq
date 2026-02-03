---
title: "Survol rapide de la programmation"
weight: 10
---

# Survol rapide de la programmation

Nous allons faire un survol rapide des idées les plus importantes et
fondamentales de la programmation logicielle. Pour aller droit au but, nous
allons utiliser le langage Python, qui est très facile à comprendre, même sans
aucune expérience explicite.

## Structures de données fondamentales

Au-delà des types de base, qui sont généralement des nombres de différents types
(entiers, réels, etc) et les chaines de caractères (strings), nous avons les
structures de données, qui sont des constructions logiques plus complexe
(non-atomique) qui impliquent, en général, les types de base, d'une manière ou
d'une autre.

### La liste et le `set`

La liste est une structure de données qui est une collection de valeurs :

```python
>>> a = [10, 20, 30]
```

Il est possible d'y ajouter, ou d'enlever des éléments :

```python
>>> a.append(40)
>>> a
[10, 20, 30, 40]
>>> a.remove(10)
>>> a
[20, 30, 40]
>>> len(a)
3
```

{{< image src="list.png" alt="" title="" loading="lazy" >}}

La liste a une taille et ses éléments ont un ordre. En contraste, le `set` a une taille, mais ses éléments
n'ont aucun ordre (il s'agit d'un "sac" de valeurs). Il est également possible de lui ajouter ou enlever
des éléments :

```python
>>> s = {10, 20, 30, 40}
>>> len(s)
4
>>> s.add(50)
>>> s.remove(20)
>>> s
{40, 10, 50, 30}
```

Il est d'une importance **capitale** d'avoir un modèle mental **archi-clair** de
la différence entre ces deux structures de données à l'apparence si semblable,
pour la raison fondamentale suivante : **chercher un item dans une liste a un coût
proportionnel à la taille de la liste, tandis que chercher un item dans un `set`
a un coût fixe (et très faible)** :

```python
>>> 20 in a  # coût proportionnel à la taille de `a`
True
>>>
>>> 20 in s  # coût fixe, extrêmement faible !
False
```

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

```python
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
```

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
anglais). En gros, l'idée est d'appliquer une [fonction de
hachage](docs/module3/versioning/#fonction-de-hachage) à un élément (la clé), ce
qui permet de déterminer l'index dans un tableau, où on pourra mettre la valeur
associée. Dans certaines implémentations, il est nécessaire de gérer les
collisions possibles : si deux clés mènent au même index par exemple, il sera
possible d'utiliser une liste, pour cette clé particulière.

{{< image src="hashtable.png" alt="" title="" loading="lazy" >}}

### La correspondance avec JSON

Une fois que vous avez des modèles mentaux clairs et efficaces par rapport aux
différences et similarités de ces trois structures de données dont nous avons
parlées dans cette section, il est utile de considérer leur correspondance avec
la notation JSON.

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
  "name": "Alice",
  "age": 30,
  "skills": ["Python", "JavaScript", "SQL"],
  "address": {
    "city": "Montreal",
    "country": "Canada"
  }
}
```

La totalité d'un document JSON est souvent un dictionnaire (que l'on reconnaît à
l'usage des `{}`), mais il existe toutefois d'autres formats (JSONL, NDJSON,
etc). Ce dictionnaire contient la plupart du temps des champs (clés) dont les
valeurs peuvent être, elles-mêmes, des dictionnaires, des listes ou des valeurs
scalaires (nombres, chaines de caractères ou valeurs booléennes).