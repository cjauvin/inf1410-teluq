---
title: "Concurrence et parallélisme"
slug: "concurrence"
weight: 15
bookCollapseSection: true
---

# Concurrence et parallélisme

Il y a une hypothèse que tout programmeur fait sans jamais y penser&nbsp;: que les
choses arrivent dans l'ordre. La ligne 12 s'exécute après la ligne 11, une
variable qu'on vient d'écrire contient bien ce qu'on y a mis, et un programme
qui a fonctionné une fois se comportera pareil la fois suivante. Cette
hypothèse est si profondément installée qu'on ne la remarque qu'au moment où
elle cesse d'être vraie. C'est exactement ce qui se produit dès qu'un programme
fait plusieurs choses à la fois, et c'est ce qui rend le sujet réputé
difficile. Il ne s'agit pas d'apprendre une bibliothèque de plus, mais de
renoncer à une intuition.

Le texte le plus tranchant sur la question s'intitule *The Problem with
Threads*, publié par Edward Lee dans *IEEE Computer* en mai 2006. Lee y soutient
que les threads sont une mauvaise abstraction, non parce qu'ils seraient mal
réalisés, mais parce qu'ils détruisent le **déterminisme**, c'est-à-dire
justement ce qui permet de comprendre un programme en le lisant. Son argument
s'appuie sur sa propre expérience, et elle donne à réfléchir. Le projet
Ptolemy, qu'il dirige à Berkeley depuis 2000, construit des systèmes embarqués
concurrents avec une discipline peu commune&nbsp;: revues de code menées par des
spécialistes de la concurrence, tests de non-régression couvrant 100&nbsp;% du code.
Le système a tourné quatre ans sans le moindre incident. Le 26 avril 2004, il
s'est bloqué. L'interblocage y était depuis le premier jour.

Retenez bien ce chiffre de 100&nbsp;%, parce que la section sur
[les tests]({{< relref "/docs/module2/20-tests" >}}) vous apprendra à vous en
méfier, et voici son démenti le plus spectaculaire. Ni la relecture par des
experts, ni une couverture totale n'ont révélé le défaut. C'est la première
fois dans ce cours qu'on rencontre une catégorie de bogues contre laquelle nos
outils habituels ne peuvent à peu près rien.

{{< illustration src="entrelacements.svg" legende="Un programme séquentiel n'a qu'un seul déroulement. Le même travail réparti sur quelques threads en a des milliards, et rien ne garantit que celui qui révèle le défaut sera jamais exécuté pendant vos tests." >}}

Si le sujet est si périlleux, on pourrait souhaiter l'éviter. Ce n'est plus
possible, et vous l'avez déjà rencontré sans qu'on vous en avertisse. Le
`async def` qui ouvre les exemples de la section sur
[les APIs]({{< relref "/docs/module3/20-apis" >}}) est un mot-clé de
programmation asynchrone. Les files d'attente et les travailleurs en arrière-plan
de la section sur [la scalabilité]({{< relref "/docs/module5/60-scalabilite" >}})
sont de la concurrence répartie sur plusieurs machines. Le sujet traverse le
cours de bout en bout, et cette section vient combler le trou&nbsp;: on vous
enseignait l'asynchronisme au niveau du système sans jamais vous l'avoir
expliqué au niveau du programme.

Sa place dans ce module découle du reste. Le module 2 s'intitule « Concevoir un
programme correct », et une erreur de concurrence est l'archétype du défaut de
correction&nbsp;: elle ne fait pas planter le programme, elle lui fait produire une
mauvaise réponse, de temps en temps, sans jamais rien signaler.

Le parcours suit cinq étapes. On commencera par **pourquoi** le sujet s'impose,
en remontant au moment où le matériel a cessé d'accélérer tout seul, et en
posant les deux distinctions qui organisent le reste. On verra ensuite ce que
le système d'exploitation offre réellement, avec les **processus et les
threads**, puis **ce qui casse** quand plusieurs fils touchent aux mêmes
données. On étudiera la réponse historique alternative, qui consiste à **ne pas
partager** du tout, avant de terminer sur la manière dont un seul fil
d'exécution peut servir des milliers de connexions à condition de **ne jamais
bloquer**.
