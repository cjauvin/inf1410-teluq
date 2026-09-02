---
title: "Processus et threads"
slug: "processus-threads"
weight: 20
---

# Processus et threads

## Un programme n'est pas un processus

Il faut d'abord séparer deux choses que le langage courant confond. Un
**programme** est un fichier, une suite d'instructions posée sur un disque, aussi
inerte qu'une partition rangée dans un tiroir. Un **processus** est ce qui arrive
quand on l'exécute. Le système d'exploitation lit le fichier, réserve une zone
de mémoire, y installe les instructions et de quoi ranger les données, retient
à quelle instruction on en est, tient la liste des fichiers ouverts, et laisse
courir. Le même programme lancé trois fois donne trois processus, qui portent
le même code et n'ont rien d'autre en commun&nbsp;: trois zones de mémoire
distinctes, trois positions différentes dans ce code, trois jeux de fichiers
ouverts. C'est ce qui permet à deux fenêtres du même éditeur de texte
peuvent afficher deux documents sans se mélanger, alors qu'elles exécutent
exactement les mêmes instructions.

## Pourquoi ils ne peuvent pas se toucher

Cette étanchéité n'est pas une politesse que les processus s'accordent entre
eux, c'est une impossibilité matérielle. Chaque processus reçoit son propre
**espace d'adressage**, un plan de mémoire qui n'appartient qu'à lui. Quand deux
processus manipulent tous les deux l'adresse 4096, ils ne désignent pas le même
endroit&nbsp;: une pièce du processeur appelée **unité de gestion mémoire** traduit ces
adresses vers des emplacements physiques différents, en suivant une table que
seul le système d'exploitation a le droit d'écrire. Un processus ne peut donc
pas lire la mémoire d'un autre, et ce n'est pas parce que ce serait interdit,
c'est parce qu'il n'a aucun moyen de la nommer. La conséquence est
considérable, et on l'oublie d'autant plus facilement qu'on en profite sans
cesse&nbsp;: un processus qui s'effondre n'emporte que lui-même. Le reste de la
machine ne s'en aperçoit même pas.

## Une garantie plus récente qu'on ne croit

Cette garantie n'a pourtant rien d'éternel, et elle est plus récente qu'on ne
l'imagine. Les premiers ordinateurs personnels n'offraient aucune protection.
Sous MS-DOS, un programme pouvait écrire n'importe où en mémoire, y compris
par-dessus le système d'exploitation lui-même, et une seule adresse mal
calculée suffisait à emporter la machine entière. Le Mac OS classique, jusqu'à
sa version 9, laissait toutes les applications se partager une mémoire commune,
si bien qu'un traitement de texte fautif faisait tomber le reste avec lui.
L'idée de donner à chaque programme une mémoire qui n'existe que pour lui, la
**mémoire virtuelle**, vient des gros systèmes universitaires et militaires des
années 60, avec l'Atlas de Manchester en 1962 puis Multics. Il aura fallu
attendre les années 90 et 2000 pour qu'elle atteigne enfin les machines de
bureau. L'écran bleu de Windows et la bombe du Mac, que les plus anciens se
rappellent, sont les vestiges d'une époque où un seul programme pouvait tout
faire tomber.

{{< image src="ecran-bleu.webp" alt="L'écran bleu de Windows 98 : du texte blanc sur fond bleu uni annonce qu'une exception fatale s'est produite dans l'application en cours, et invite à appuyer sur une touche pour tenter de continuer, ou sur Ctrl+Alt+Suppr pour redémarrer, en perdant le travail non sauvegardé" title="L'écran bleu de Windows 9x. Image dans le domaine public, via Wikimedia Commons" loading="lazy" >}}

{{< image src="bombe-mac.webp" alt="La boîte de dialogue d'erreur système du Mac OS classique : une bombe à mèche allumée, le message Sorry, a system error occurred, et un bouton Restart, seule issue possible" title="La bombe du Mac OS classique, ère du Système 7. Image dans le domaine public, via Wikimedia Commons" loading="lazy" >}}

## Se parler coûte cher

Cette isolation a un prix, et c'est lui qui explique tout ce qui suit. Deux
processus qui doivent collaborer n'ont aucun moyen direct de le faire. Il leur
faut passer par le système d'exploitation, au moyen d'un **tuyau** (*pipe*),
d'une **socket**, d'un fichier, ou d'une zone de mémoire partagée réclamée
explicitement. Chaque échange suppose alors de recopier les données depuis
l'espace du premier vers celui du second, en passant par le noyau. Pour deux
programmes qui s'envoient un message de temps à autre, la dépense est
invisible. Pour deux morceaux d'un même travail qui manipulent sans arrêt les
mêmes données, un navigateur qui affiche une page pendant qu'il en télécharge
les images, un tableur qui recalcule pendant qu'on tape, la facture devient
absurde. On passerait plus de temps à recopier qu'à travailler.

## Plusieurs fils dans un même processus

La réponse tient en une idée simple&nbsp;: garder un seul processus, mais y faire
courir plusieurs exécutions à la fois. C'est ce qu'on appelle un **thread**, ou
fil d'exécution. Un thread possède en propre le strict minimum, sa position
dans le code et sa **pile** (*stack*), c'est-à-dire l'endroit où s'empilent ses
appels de fonction et ses variables locales. Tout le reste, il le partage avec
ses frères, le même espace d'adressage, les mêmes variables globales, les mêmes
fichiers ouverts. Deux threads d'un même processus qui lisent une même variable
ne recopient rien et ne dérangent pas le noyau&nbsp;: ils vont chercher le même
emplacement en mémoire, directement. Le problème du paragraphe précédent
disparaît d'un coup. Il disparaît même si complètement qu'on va bientôt
regretter l'isolation qu'on vient d'abandonner.

## Ce que chacun coûte

Le partage n'est pas le seul avantage des threads&nbsp;: ils sont aussi beaucoup
moins chers à créer. Un processus exige que le système bâtisse un espace
d'adressage complet, avec ses tables de traduction. Un thread ne demande qu'une
pile et de quoi noter où il en est. On peut mesurer l'écart en quelques lignes,
en créant cinq cents fois chacun et en les laissant s'arrêter aussitôt.

```python
import os, time, threading

N = 500

def chrono(nom, f):
    debut = time.perf_counter()
    f()
    duree = time.perf_counter() - debut
    print(f"{nom:12s} {duree / N * 1e6:7.1f} µs par unité")

def threads():
    ts = [threading.Thread(target=lambda: None) for _ in range(N)]
    for t in ts: t.start()
    for t in ts: t.join()

def processus():
    pids = []
    for _ in range(N):
        pid = os.fork()          # l'enfant repart d'ici avec pid valant 0
        if pid == 0:
            os._exit(0)          # et s'arrête immédiatement
        pids.append(pid)
    for pid in pids:
        os.waitpid(pid, 0)       # on attend chacun d'eux

chrono("thread", threads)
chrono("processus", processus)
```

```shell
$ uv run --no-project python cout.py
thread           42.8 µs par unité
processus       222.8 µs par unité
```

{{% hint warning %}}
`os.fork()` n'existe que sur les systèmes de la famille Unix, donc macOS et
Linux. Sous Windows sans WSL, ce script s'arrêtera sur une `AttributeError`,
parce que le système n'offre tout simplement pas cette manière de créer un
processus. Sous WSL, qui est un vrai Linux, tout fonctionne, et c'est
d'ailleurs l'environnement que
[le cours recommande]({{< relref "/docs/environnements" >}}) aux utilisateurs
de Windows. La portion sur les threads, elle, fonctionne partout.
{{% /hint %}}

Un processus coûte donc environ **cinq fois** un thread, ce qui est déjà
notable quand on en crée beaucoup, mais reste loin des ordres de grandeur qu'on
lit parfois. Ces chiffres viennent d'un portable récent, et ils varieront chez
vous, mais c'est le rapport entre les deux qui compte, pas leur valeur absolue.

### Un piège de mesure, et il est courant

Si on refait la mesure avec `multiprocessing.Process`, la bibliothèque standard
prévue pour ça, le résultat explose&nbsp;: environ **7100 µs** par processus sur le
même portable, soit 167 fois un thread au lieu de cinq. La conclusion qu'on en
tire spontanément, que les processus coûtent sept millisecondes, est fausse.

Ce n'est pas le prix d'un processus, c'est celui du démarrage d'un interpréteur
Python complet. Sur macOS et sur Windows, `multiprocessing` emploie par défaut
la méthode **spawn**, qui lance un nouvel interpréteur vierge et lui fait
réimporter votre module. Sur Linux, il emploie **fork**, qui duplique le
processus courant, et la mesure y est bien plus basse. Le même programme, avec
le même code, n'a donc pas du tout le même coût selon le système.

La conséquence pratique est simple. Créer un processus par tâche est ruineux,
créer une réserve de processus au démarrage et la réutiliser ne coûte presque
rien. C'est exactement ce que fait `multiprocessing.Pool`, et c'est précisément sa raison d'être.

## Comment un seul coeur fait semblant

Un coeur exécute une suite d'instructions à la fois, et rien ne changera cela.
Pourtant, bien avant que les puces aient plusieurs coeurs, une machine faisait
déjà tourner un traitement de texte, une horloge et une impression en même
temps. L'illusion repose sur un mécanisme matériel très simple, une minuterie
qui, toutes les quelques millisecondes, interrompt ce qui se passe et rend la
main au système d'exploitation. La partie de celui-ci qui décide alors quoi
faire s'appelle l'**ordonnanceur** (*scheduler*). Il range l'état du thread en
cours, ses registres et sa position dans le code, puis installe à la place
l'état d'un autre thread qui attendait son tour. C'est ce qu'on appelle un
**changement de contexte**, et il se produit assez souvent pour que rien ne se
voie. Chaque programme n'avance qu'une fraction du temps, mais il avance si
fréquemment que l'oeil n'y distingue aucune interruption.

### Prendre la main plutôt que la demander

Que la minuterie interrompe un programme sans lui demander son avis n'a rien
d'évident, et ce n'est pas ainsi qu'on a commencé. On appelle cela la
**préemption**, par opposition au **multitâche coopératif**, où chaque
programme devait rendre la main de lui-même, en appelant régulièrement une
fonction prévue pour cela. Le Mac OS classique et Windows 3.x fonctionnaient
de cette manière. Il suffisait donc qu'un seul programme oublie de céder son
tour, ou reste coincé dans une boucle, pour que la machine entière se fige,
souris comprise. C'est exactement la même trajectoire que la protection
mémoire, vue plus haut&nbsp;: une garantie née sur les gros systèmes des années 60,
restée trente ans hors de portée des machines personnelles, et qu'on tient
aujourd'hui pour si acquise qu'on ne la remarque plus.

### La distinction de Pike, mécaniquement

On peut maintenant relire la formule de Rob Pike autrement que comme un jeu de
mots. Sur une machine à un seul coeur, un programme découpé en dix tâches qui
progressent chacune à leur rythme est parfaitement **concurrent**, et il n'a
strictement **aucun parallélisme**. Les dix tâches existent bel et bien, elles
se relaient, aucune n'est terminée avant que les autres aient commencé, mais à
chaque instant une seule avance. Donnez dix coeurs à ce même programme, sans
changer une ligne, et il devient parallèle. La concurrence était dans le code
depuis le début, le parallélisme est arrivé avec la machine. C'est ce qui fait que la distinction n'est pas une subtilité de vocabulaire&nbsp;: elle sépare
ce que vous écrivez de ce sur quoi vous n'avez aucune prise.

## Le verrou global de Python

Tout ce qui précède décrit ce que le système d'exploitation offre. Reste à
savoir ce que le langage en fait, et Python réserve ici une surprise. Son
implémentation courante, CPython, protège son fonctionnement interne par un
verrou unique que l'on nomme le **GIL**, pour *global interpreter lock*.
Un seul thread à la fois peut le détenir, et sans lui aucun code Python ne
s'exécute. Autrement dit, quel que soit le nombre de coeurs de la machine et
le nombre de threads du programme, **un seul thread exécute du Python à un
instant donné**.

Reprenons le calcul le plus bête possible, une somme de carrés, répété quatre
fois, en séquentiel puis réparti sur quatre threads puis sur quatre processus.

```python
import time, threading, multiprocessing

def calcul(n):
    somme = 0
    for i in range(n):
        somme += i * i
    return somme

N, K = 30_000_000, 4          # 4 fois le même calcul, bien assez long

def chrono(nom, f):
    debut = time.perf_counter()
    f()
    print(f"{nom:16s} {time.perf_counter() - debut:5.2f} s")

def sequentiel():
    for _ in range(K):
        calcul(N)

def avec_threads():
    ts = [threading.Thread(target=calcul, args=(N,)) for _ in range(K)]
    for t in ts: t.start()
    for t in ts: t.join()

def avec_processus():
    with multiprocessing.Pool(K) as pool:
        pool.map(calcul, [N] * K)

if __name__ == "__main__":        # obligatoire pour multiprocessing
    chrono("séquentiel", sequentiel)
    chrono("4 threads", avec_threads)
    chrono("4 processus", avec_processus)
```

```shell
$ uv run --no-project python gil.py
séquentiel        2.51 s
4 threads         2.62 s
4 processus       0.89 s
```

Les quatre threads ne font rien gagner du tout, et sont même **légèrement plus
lents** que le code séquentiel, parce qu'on paie les changements de contexte et
la dispute autour du verrou sans jamais rien exécuter en parallèle. Les quatre
processus, eux, divisent le temps par presque trois. Rien d'étonnant&nbsp;: chacun a
son propre interpréteur, donc son propre GIL, et le verrou ne les gêne plus.

Pourquoi s'infliger un tel verrou&nbsp;? Parce qu'il achète beaucoup de choses. Il
rend l'interpréteur correct sans qu'il faille protéger individuellement chacune
de ses structures internes, il garde le code à un seul thread rapide, cas de
loin le plus fréquent, et il permet d'écrire des extensions en C sans se
soucier de la concurrence. C'est un compromis assumé, choisi il y a trente ans,
et qui a rendu Python beaucoup plus simple à faire évoluer.

### Le verrou bloque le calcul, jamais l'attente

Il serait facile de conclure de ce qui précède que les threads ne servent à
rien en Python. Ce serait une demi-vérité, et elle coûte cher, parce qu'elle
prive d'un outil parfaitement adapté à la moitié des situations. Reprenons
exactement la même comparaison, mais avec un programme qui attend au lieu
de calculer. Cinquante requêtes réseau de cent millisecondes chacune, ici
simulées par une pause pour que l'expérience soit reproductible hors ligne.

```python
import time, threading

N, LATENCE = 50, 0.1          # 50 « requêtes » de 100 ms chacune

def chrono(nom, f):
    debut = time.perf_counter()
    f()
    print(f"{nom:16s} {time.perf_counter() - debut:5.2f} s")

def sequentiel():
    for _ in range(N):
        time.sleep(LATENCE)   # ici, une vraie requête réseau

def avec_threads():
    ts = [threading.Thread(target=time.sleep, args=(LATENCE,)) for _ in range(N)]
    for t in ts: t.start()
    for t in ts: t.join()

chrono("séquentiel", sequentiel)
chrono("50 threads", avec_threads)
```

```shell
$ uv run --no-project python attente.py
séquentiel        5.17 s
50 threads        0.11 s
```

Quarante-sept fois plus rapide, avec le même outil qui ne servait à rien
l'instant d'avant. La raison est simple une fois qu'on la connaît&nbsp;: un thread
qui s'apprête à attendre **relâche le GIL** avant de se mettre en pause, et ne
le reprend qu'au retour. Pendant qu'il patiente, il n'exécute aucun code
Python, donc il n'a aucune raison de tenir le verrou. Les quarante-neuf autres
en profitent pour lancer leur propre attente, et les cinquante pauses se
déroulent ensemble.

Voilà pourquoi la distinction entre attendre et calculer, posée dans la
sous-section précédente, valait la peine d'être posée avant tout le reste. Le
même mot de concurrence, le même outil, et deux résultats opposés selon le
problème. La règle à retenir tient en une ligne&nbsp;: en Python, les threads pour
attendre, les processus pour calculer.

## Ce que devient Python sans son verrou

Ce compromis vieux de trente ans est en train d'être défait. Le **PEP 703**,
accepté en 2023, ajoute à CPython une variante sans GIL, dite
**free-threaded**. Elle s'installe comme les autres, son numéro de version
portant simplement un `t` final, et `uv` sait la récupérer sans qu'on ait rien
à configurer.

```shell
$ uv run --python 3.14  --no-project python gil.py     # avec le verrou
$ uv run --python 3.14t --no-project python gil.py     # sans le verrou
```

Le fichier est le même, à la lettre près. Seul l'interpréteur change.

| Sur le calcul | avec GIL | sans GIL |
|---|---|---|
| séquentiel | 2,61 s | 3,03 s |
| 4 threads | 2,69 s | **0,80 s** |
| 4 processus | 0,84 s | 0,88 s |

Les threads passent d'inutiles à les plus rapides, et la règle apprise deux
paragraphes plus haut, les processus pour calculer, cesse d'être vraie. On
notera aussi que le séquentiel est un peu plus lent sans le verrou&nbsp;: retirer le
GIL coûte quelque chose au code à un seul thread, ce qui est précisément la
raison pour laquelle il a fallu vingt ans de débats avant d'y toucher.

### Le bogue était là depuis toujours

Reste le revers, et c'est la leçon la plus importante de cette sous-section.
Voici quatre threads qui incrémentent un même compteur un million de fois
chacun.

```python
import threading

compteur = 0

def incrementer(n):
    global compteur
    for _ in range(n):
        compteur += 1        # lire, ajouter, écrire : trois étapes, pas une

N, K = 1_000_000, 4
ts = [threading.Thread(target=incrementer, args=(N,)) for _ in range(K)]
for t in ts: t.start()
for t in ts: t.join()

print(f"attendu : {N * K}")
print(f"obtenu  : {compteur}")
```

```shell
$ uv run --python 3.14  --no-project python compteur.py
attendu : 4000000
obtenu  : 4000000

$ uv run --python 3.14t --no-project python compteur.py
attendu : 4000000
obtenu  : 1014951
```

Le même fichier. Correct sur un interpréteur, faux de trois quarts sur l'autre.
Et il faut bien voir que ce n'est pas le second qui est cassé&nbsp;: `compteur += 1`
n'a jamais été une opération unique, c'est une lecture, une addition et une
écriture. Quand deux threads lisent la même valeur avant que l'un des deux ait
écrit la sienne, l'un des deux incréments est perdu. **Le bogue était présent
depuis le premier jour, le verrou le rendait invisible.**

Il l'est d'ailleurs très solidement. Même en demandant à Python de faire
tourner ses threads le plus souvent possible, avec
`sys.setswitchinterval(1e-9)`, le compteur reste parfaitement juste sur
CPython 3.13 et 3.14. Sur CPython 3.9, en revanche, le même programme perdait
déjà un tiers de ses incréments. Autrement dit, la visibilité de ce bogue
dépend de la version de l'interpréteur, de la machine et de la chance, et
certainement pas de la correction du code.

C'est la première fois dans ce cours qu'on rencontre un programme dont les
tests peuvent passer mille fois sans rien prouver. Ce ne sera pas la dernière,
et c'est le sujet de la sous-section suivante.
