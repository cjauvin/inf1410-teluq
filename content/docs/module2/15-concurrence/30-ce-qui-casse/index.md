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

<!-- À ÉCRIRE, en conclusion de cette sous-section, comme pont vers « Ne pas
     partager » : Edward Lee et le projet Ptolemy. Un logiciel construit à
     Berkeley depuis 2000 par des spécialistes de la concurrence, relu ligne à
     ligne, couvert à 100 % par des tests de non-régression, qui a tourné
     quatre ans sans incident puis s'est figé le 26 avril 2004 sur un
     interblocage présent depuis le premier jour. L'anecdote arrive après que
     le lecteur a vu un interblocage de ses yeux, donc elle porte. Renvoyer à
     la section sur les tests (limites de la couverture). Enchaîner sur la
     thèse de son article *The Problem with Threads* (IEEE Computer, mai 2006) :
     les threads détruisent le déterminisme, ce qui permet de comprendre un
     programme en le lisant. C'est la conclusion naturelle de « Ce qui casse »
     et l'ouverture de « Ne pas partager ». Portrait : edward-lee.webp dans le
     dossier de la section, CC BY-SA 4.0, crédit dans le title. -->
