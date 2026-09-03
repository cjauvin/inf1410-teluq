---
title: "Ne jamais bloquer"
slug: "ne-jamais-bloquer"
weight: 50
---

# Ne jamais bloquer

## Dix mille clients

En 1999, un programmeur nommé Dan Kegel ouvre une page web par une question
faussement modeste&nbsp;: « Il est temps que les serveurs web servent dix mille
clients en même temps, vous ne trouvez pas&nbsp;? » Le problème a gardé le nom
qu'il lui a donné, **C10K**, dix mille connexions, et il est resté la page de
référence du sujet pendant quinze ans, remise à jour jusqu'en 2014. Ce qui le
rendait difficile n'était pas la puissance de calcul. Dix mille personnes qui
lisent un site ne demandent presque rien au processeur. Ce qui le rendait
difficile, c'est que la manière évidente de s'y prendre ne tient pas.

La manière évidente, c'est celle de tout ce qu'on a vu jusqu'ici&nbsp;: un thread
par client. Chaque connexion reçoit son fil d'exécution, qui attend la requête,
la lit, répond, et recommence. C'est simple, c'est lisible, et Kegel montre en
une division pourquoi cela s'effondre. Un thread a besoin d'une pile, deux
mégaoctets sur le Linux de l'époque, et un processus disposait d'un gigaoctet
de mémoire virtuelle. « On manque de mémoire virtuelle à
2^30 / 2^21 = 512 threads. » Un gigaoctet divisé par deux mégaoctets, cinq
cent douze. On en voulait dix mille.
Et même en réduisant les piles, chaque thread qui attend coûte un changement de
contexte à l'ordonnanceur pour rien, puisqu'il n'a rien à faire d'autre
qu'attendre. On retrouve le cuisinier planté devant sa casserole, sauf qu'ils
sont dix mille à attendre chacun devant la sienne, et que la cuisine n'a pas
la place.

La réponse de Kegel tient en une phrase, et elle est le programme de toute
cette sous-section&nbsp;: « servir beaucoup de clients avec chaque thread, et
utiliser des entrées-sorties non bloquantes et une notification de
disponibilité ». Autrement dit, un seul cuisinier pour toutes les casseroles,
à condition qu'il ne reste jamais planté devant aucune. Au lieu de demander au
réseau « donne-moi la requête » et d'attendre qu'elle arrive, on lui demande
« préviens-moi quand une requête est arrivée » et on passe à la casserole
suivante. Le système d'exploitation offre exactement cela, sous des noms qui
varient, `select` et `poll` partout, `epoll` sur Linux, `kqueue` sur les
systèmes BSD dont macOS&nbsp;: une fonction qui reçoit une liste de connexions
et rend la main quand l'une d'elles a quelque chose à dire. Un seul thread, dix
mille connexions, et une boucle qui demande sans cesse « laquelle est
prête&nbsp;? ». On l'appelle une **boucle d'événements** (*event loop*), et c'est
ce que vous avez vu tourner sans le savoir dans les deux millions de
connexions de WhatsApp, à la fin de la sous-section précédente.

## Le multitâche coopératif, revenu par la petite porte

Il faut être précis sur ce qui change, parce que sur une image fixe, rien ne
change. Un cuisinier devant trois casseroles qui cuisent, c'est la vignette
« Concurrence » de l'introduction de cette section, et elle décrit aussi bien
dix threads sur un seul coeur qu'une boucle d'événements. Dans les deux cas,
une seule chose avance à la fois, et dans les deux cas, les casseroles cuisent
pendant qu'on s'occupe d'une autre. La différence n'est pas dans l'image, elle
est dans qui déplace le cuisinier.

Avec les threads, c'est le système qui le déplace. Vous avez vu comment dans
la sous-section sur [les processus et les threads]({{< relref "/docs/module2/15-concurrence/20-processus-et-threads" >}})&nbsp;:
une minuterie interrompt le thread en cours sans lui demander son avis,
l'ordonnanceur range son état et en installe un autre à la place. Le cuisinier
peut donc rester planté devant sa casserole autant qu'il veut, quelqu'un
viendra le pousser. Mais chaque cuisinier planté est un cuisinier entier, avec
sa pile, et chaque poussée est un changement de contexte. Dix mille clients,
c'est dix mille cuisiniers debout dans la cuisine, et c'est le compte de
Kegel.

Avec la boucle d'événements, personne ne pousse personne. Il n'y a qu'un
cuisinier, et c'est lui qui décide quand changer de casserole. Il n'a le droit
de le faire qu'à un moment précis, celui où il a demandé à être prévenu, et il
ne se plante jamais, parce que la casserole a une sonnette. Un plat en attente
n'est plus une personne, c'est une note posée sur la casserole, l'état du plat
et quoi faire quand elle sonnera.

{{< illustration src="sonnette.svg" legende="La même cuisine, les mêmes casseroles. À gauche, un cuisinier par casserole, et c'est l'ordonnanceur qui décide lequel avance, en poussant l'un pendant que les autres restent plantés, chacun avec sa pile. À droite, un seul cuisinier et une sonnette par casserole&nbsp;: il ne se plante devant aucune, et il change de casserole quand l'une sonne." >}}

Si cela vous rappelle quelque chose, c'est normal. Un programme qui rend la
main de lui-même, à des moments qu'il choisit, c'est le multitâche coopératif
que vous avez rencontré avec l'ordonnanceur, celui du Mac OS classique et de
Windows 3.x, que la préemption avait remplacé parce qu'un seul programme qui
oubliait de céder son tour figeait la machine entière. Il revient ici par la
petite porte, à l'intérieur d'un seul processus, et il revient avec sa
fragilité intacte. Si le cuisinier unique reste planté devant une casserole,
ne serait-ce qu'une seconde, les dix mille autres brûlent. C'est de là que
cette sous-section tient son titre.

Le tableau rassemble les trois modèles rencontrés jusqu'ici, sur les quatre
lignes qui les séparent vraiment.

| | Processus | Thread | Boucle d'événements |
|---|---|---|---|
| Mémoire | la sienne, isolée par la MMU | celle du processus, partagée avec les autres threads | celle du processus, un seul thread |
| Qui décide de changer de tâche | le système, par préemption | le système, par préemption | le programme lui-même, aux moments où il a demandé à être prévenu |
| Ce que coûte une tâche qui attend | un processus entier | un thread entier, avec sa pile, et un changement de contexte | une note, l'état du plat et quoi faire ensuite |
| Ce qui casse | rien n'est partagé, mais se parler coûte cher | les conditions de course | un seul appel bloquant fige tout |

<!-- MESURÉ le 2 septembre 2026 dans la page, Pyodide 3.12.7 : threading.Thread
     -> RuntimeError: can't start new thread ; os.fork et multiprocessing ->
     OSError 52 Function not implemented ; MAIS `await asyncio.sleep(0.1)` via
     runPythonAsync fonctionne (737 ms au premier appel, chauffe de la boucle
     comprise). Donc l'exemple asyncio de cette sous-section PEUT être un bloc
     exécutable dans la page, par le shortcode pyodide,, contrairement aux exemples de
     threads de la sous-section 20. À exploiter : ce serait l'exemple Python le
     plus fort de la section, l'étudiant le lance lui-même. Vérifier que le
     shortcode pyodide passe par runPythonAsync (ou l'adapter). -->
