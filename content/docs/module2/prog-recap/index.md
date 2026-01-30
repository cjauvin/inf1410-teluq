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

La notion de table associative est une autre famille de structures de données
pour laquelle il est crucial d'avoir un modèle mental clair et limpide. Une
manière de se représenter le fonctionnement d'une table associative est en tant
qu'extension d'un `set` : imaginons qu'à chaque élément (ou valeur) d'un `set`,
nous attachons une valeur.

{{< image src="dict.png" alt="" title="" loading="lazy" >}}

## Algorithmes importants