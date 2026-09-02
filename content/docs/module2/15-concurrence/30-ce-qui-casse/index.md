---
title: "Ce qui casse"
slug: "ce-qui-casse"
weight: 30
---

# Ce qui casse

## Trois étapes, pas une

Reprenons le compteur de la sous-section précédente, celui qui donnait
4 000 000 sur un interpréteur et 1 014 951 sur l'autre. La ligne coupable est
`compteur += 1`, et tout tient au fait qu'elle n'est pas une opération mais
trois. Le processeur **lit** la valeur courante en mémoire, l'**augmente** de un
dans un registre, puis **écrit** le résultat à sa place. Entre la lecture et
l'écriture s'écoule un temps minuscule mais réel, et rien n'interdit à
l'ordonnanceur d'y glisser un autre thread. Si ce second thread lit à ce
moment-là, il obtient la même valeur que le premier, l'augmente lui aussi de
un, et l'écrit à son tour. Chacun a ajouté un. Le compteur n'a avancé que
d'un. En cuisine, c'est le cuisinier qui goûte la soupe, la trouve fade, et
part chercher le sel pendant que son collègue, qui l'a goûtée une seconde plus
tôt, y verse déjà le sien.

Voici d'abord ce qui devrait se passer, quand A termine ses trois étapes avant
que B commence les siennes. Deux incréments, et le compteur avance de deux.

| Instant | Thread A | Thread B | Valeur en mémoire |
|---|---|---|---|
| 1 | lit 41 | | 41 |
| 2 | calcule 42 | | 41 |
| 3 | écrit 42 | | 42 |
| 4 | | lit 42 | 42 |
| 5 | | calcule 43 | 42 |
| 6 | | écrit 43 | **43** |

Et voici le même travail quand B commence avant que A ait fini. Chacun lit 41,
chacun écrit 42.

| Instant | Thread A | Thread B | Valeur en mémoire |
|---|---|---|---|
| 1 | lit 41 | | 41 |
| 2 | | lit 41 | 41 |
| 3 | calcule 42 | | 41 |
| 4 | | calcule 42 | 41 |
| 5 | écrit 42 | | 42 |
| 6 | | écrit 42 | **42** |

Deux incréments, un seul de compté. On appelle cela une **condition de course**
(*race condition*), parce que le résultat dépend de qui arrive le premier, et
que personne ne contrôle l'ordre d'arrivée. Le mot important est *dépend*. Le
programme n'est pas faux dans l'absolu&nbsp;: il est juste quand A finit avant que
B commence, et faux quand leurs trois étapes se chevauchent. Sur le million
d'incréments de chaque thread, ce chevauchement s'est produit à peu près trois
fois sur quatre.

## Vingt façons de se croiser, puis des milliards

Le tableau ne montre qu'un seul ordre parmi ceux qui sont possibles, et c'est
là que le problème prend sa vraie dimension. Deux threads de trois instructions
chacun peuvent se croiser de vingt manières différentes, et l'ordonnanceur en
choisit une à chaque exécution, sans que rien dans le programme ne dise
laquelle. Certaines donnent la bonne réponse, celles où A termine ses trois
étapes avant que B commence la première, ou l'inverse. Les autres perdent un
incrément. Trois threads de trois instructions se croisent de 1680 façons, et
quatre threads de cinq instructions, ce qui reste un programme minuscule, de
plus de onze milliards. Aucun test n'explore une fraction appréciable de ce
nombre. Pire, le même test lancé mille fois emprunte presque toujours les mêmes
chemins, parce que l'ordonnanceur n'est pas aléatoire, il est seulement
imprévisible.

{{< illustration src="entrelacements.svg" legende="Les mêmes six instructions, en séquentiel puis réparties sur deux threads. Le nombre d'ordres d'exécution possibles explose bien plus vite que la taille du programme, et vos tests n'en parcourent qu'une poignée, toujours à peu près la même." >}}

## Un seul à la fois

Le remède tient en une idée&nbsp;: rendre les trois étapes indivisibles, non pas en
les fusionnant, ce que le processeur ne sait pas toujours faire, mais en
interdisant à un second thread d'y entrer tant que le premier n'en est pas
sorti. L'objet qui impose cela s'appelle un **verrou** (*lock*), et la portion
de code qu'il protège une **section critique**. Un thread qui veut y entrer
prend le verrou. S'il est déjà pris, il attend qu'on le libère. En cuisine,
c'est la règle qu'un seul cuisinier à la fois s'approche de la salière&nbsp;: le
second attend que le premier ait salé, goûté et reposé la salière.

L'idée a un auteur et une date. En 1965, Edsger Dijkstra, croisé au module 1
pour la programmation structurée, formalise le problème de l'**exclusion
mutuelle** et propose le **sémaphore**, un compteur qu'on ne peut modifier que
par deux opérations indivisibles, dans un texte intitulé *Cooperating
Sequential Processes*. Le nom vient des sémaphores de chemin de fer, qui
interdisent à deux trains d'entrer sur la même voie. Le verrou de Python en est
le descendant direct, et il tient en une ligne.

```python
import threading

compteur = 0
verrou = threading.Lock()

def incrementer(n):
    global compteur
    for _ in range(n):
        with verrou:             # un seul thread à la fois entre ici
            compteur += 1

N, K = 1_000_000, 4
ts = [threading.Thread(target=incrementer, args=(N,)) for _ in range(K)]
for t in ts: t.start()
for t in ts: t.join()

print(f"attendu : {N * K}")
print(f"obtenu  : {compteur}")
```

```shell
$ uv run --python 3.14t --no-project python compteur.py
attendu : 4000000
obtenu  : 4000000
```

Le résultat est juste, et ce n'est pas gratuit. Sur le même interpréteur sans
GIL, la version protégée met 0,36 s là où la version fausse en mettait 0,11,
trois fois plus. Le verrou fait exactement ce qu'on lui demande&nbsp;: il remet
les threads en file indienne devant la ligne protégée, et une file indienne
n'est pas du parallélisme. Quatre threads qui passent leur temps à attendre le
même verrou ne valent pas mieux qu'un seul, et parfois moins, puisqu'il faut
payer les changements de contexte par-dessus. C'est le premier compromis de la
concurrence&nbsp;: on achète la correction avec de la vitesse, et on protège le
moins possible pour en perdre le moins possible.

### La même idée, à l'échelle d'une base de données

Vous retrouverez ce mécanisme, sous un autre nom, dans la section sur
[le stockage des données]({{< relref "/docs/module3/40-données/20-stockage" >}}).
Inscrire une étudiante à un cours demande de vérifier qu'elle n'y est pas déjà,
puis de l'inscrire, et deux requêtes qui font cela au même moment peuvent
l'inscrire deux fois, ou perdre l'une des deux inscriptions. C'est le compteur
de tout à l'heure, avec une ligne de table à la place d'une variable. La base
de données ne demande pas au programmeur de poser un verrou. Elle lui offre la
**transaction**, un bloc d'opérations que le système s'engage à exécuter
*comme si* aucune autre ne s'entrelaçait avec lui, même s'il les entrelace en
réalité pour aller plus vite. Cette propriété, l'isolation, est l'une des
quatre que Jim Gray a formalisées sous l'acronyme ACID, et elle dit exactement
ce que les deux tableaux du début de cette page montrent&nbsp;: un entrelacement
est acceptable si, et seulement si, son résultat est celui d'un ordre
séquentiel. `with verrou:` et `BEGIN … COMMIT` sont la même idée, l'une dans
le programme, l'autre dans la base, et le prix est le même, la correction se
paie en vitesse.

## Chacun tient ce dont l'autre a besoin

Le verrou règle la condition de course, et il en crée une autre catégorie de
problème, plus sournoise encore. Deux cuisiniers, un couteau, une planche.
Le premier prend le couteau et se retourne pour attraper la planche. Le second,
au même instant, a pris la planche et tend la main vers le couteau. Chacun tient
ce dont l'autre a besoin, chacun attend que l'autre lâche, et aucun ne lâchera
jamais. On appelle cela un **interblocage** (*deadlock*). Dijkstra en a donné
en 1965 la formulation restée classique, cinq philosophes à table avec cinq
fourchettes, chacun ayant besoin de ses deux voisines pour manger, et Tony
Hoare l'a baptisée plus tard le **dîner des philosophes**. Qu'il s'agisse
d'un dîner n'est pas un hasard de cette section, c'est le problème lui-même.

```python
import threading, time

couteau = threading.Lock()
planche = threading.Lock()

def cuisinier_a():
    with couteau:                 # prend le couteau
        time.sleep(0.01)          # le temps de se retourner
        with planche:             # puis veut la planche
            print("A a coupé")

def cuisinier_b():
    with planche:                 # prend la planche
        time.sleep(0.01)
        with couteau:             # puis veut le couteau
            print("B a coupé")

# daemon=True : sans cela, le programme ne se terminerait jamais, ce qui est
# précisément le symptôme. On le laisse ici pour pouvoir constater et sortir.
a = threading.Thread(target=cuisinier_a, daemon=True)
b = threading.Thread(target=cuisinier_b, daemon=True)
debut = time.perf_counter()
a.start(); b.start()
a.join(timeout=3); b.join(timeout=3)
print(f"après {time.perf_counter() - debut:.1f} s : A vivant={a.is_alive()}, B vivant={b.is_alive()}")
```

```shell
$ uv run --no-project python interblocage.py
après 6.0 s : A vivant=True, B vivant=True
```

Regardez ce qui **ne** s'est **pas** affiché. Ni « A a coupé », ni « B a
coupé », ni la moindre erreur. Un interblocage ne fait pas planter le programme
et ne lève aucune exception. Il l'arrête, en silence, pour toujours. Sans le
`daemon=True` et les `join` à délai, ce script ne rendrait jamais la main, et
c'est ainsi qu'un tel défaut se manifeste en production&nbsp;: par un service qui
répond de moins en moins, puis plus du tout, sans une ligne dans les journaux.
C'est exactement ce qui a figé le projet d'Edward Lee dont on parlera plus bas.

Le remède tient en une règle, et elle est plus simple que le problème&nbsp;:
**toujours prendre les verrous dans le même ordre.** Si les deux cuisiniers
conviennent de saisir le couteau avant la planche, celui qui a le couteau
finira toujours par avoir la planche, parce que l'autre n'a pas encore le droit
d'y toucher. Dans le programme ci-dessus, cela revient à inverser les deux
verrous de `cuisinier_b`, pour qu'il les prenne dans le même ordre que
`cuisinier_a`. C'est le seul changement.

```python
def cuisinier_b():
    with couteau:                 # le couteau d'abord, comme A
        time.sleep(0.01)
        with planche:             # la planche ensuite
            print("B a coupé")
```

Relancé avec cette seule fonction modifiée, le même fichier se termine
aussitôt.

```shell
$ uv run --no-project python interblocage.py
A a coupé
B a coupé
après 0.0 s : A vivant=False, B vivant=False
```

La règle est simple à énoncer et difficile à tenir, parce qu'elle doit valoir
pour tous les verrous de tout le programme, y compris ceux que prennent les
bibliothèques qu'on appelle sans le savoir. C'est pour cela que quatre ans de
tests n'ont rien vu chez Lee&nbsp;: l'ordre fautif ne se produisait que sous une
charge que personne n'avait provoquée.

## Ce que les tests ne peuvent pas voir

Tout ce que cette sous-section a montré a une propriété commune, et c'est la
plus inquiétante&nbsp;: ça passe les tests. Le compteur faux donnait 4 000 000
sur CPython 3.13, la bonne réponse, mille fois de suite. L'interblocage ne se
produit que si A et B se retournent au même centième de seconde, ce qu'aucun
test n'a de raison de provoquer. Et la couverture, dont
[la section sur les tests]({{< relref "/docs/module2/20-tests" >}}) vous a
appris à vous méfier, mesure quelles lignes ont été exécutées, pas dans lequel
des onze milliards d'ordres elles l'ont été. Un test goûte la soupe une fois.
Il n'a aucun moyen de savoir qu'une fois sur cent, deux cuisiniers la salent.

L'histoire la plus parlante sur ce point est celle d'Edward Lee, professeur à
l'Université de Californie à Berkeley, qui y dirige depuis 2000 le projet
Ptolemy. Ce projet construit
des logiciels concurrents pour des systèmes embarqués avec une discipline peu
commune&nbsp;: relecture ligne à ligne par des spécialistes de la concurrence,
tests de non-régression couvrant 100&nbsp;% du code. Le système a tourné quatre
ans sans le moindre incident. Le 26 avril 2004, il s'est figé. C'était un
interblocage, exactement celui que vous venez de provoquer en vingt lignes, et
il était dans le code depuis le premier jour. Quatre ans de tests l'avaient
traversé sans le voir, parce que l'ordre fautif ne se produisait que sous une
charge que personne n'avait jamais exercée.

{{< image src="edward-lee.webp" alt="Edward A. Lee, professeur d'informatique à l'Université de Californie à Berkeley" title="Edward A. Lee en 2018. Photo : Edward A. Lee, CC BY-SA 4.0, via Wikimedia Commons" loading="lazy" >}}

Lee en a tiré une conclusion tranchée, dans un article de 2006 au titre sans
ambiguïté, *The Problem with Threads*. Les threads, dit-il, ne sont pas une
mauvaise réalisation d'une bonne idée. Ce sont une mauvaise abstraction. Ils
prennent un programme séquentiel, compréhensible parce que **déterministe**,
c'est-à-dire parce qu'il fait la même chose à chaque exécution, et le rendent
non déterministe par défaut. Puis ils demandent au programmeur de reconquérir
le déterminisme perdu à coups de verrous, un par un, sans jamais lui donner le
moyen de prouver qu'il n'en manque pas. C'est le monde à l'envers. La bonne
question n'est pas comment poser assez de verrous, mais comment ne pas avoir à
en poser. C'est le sujet de la sous-section suivante.
