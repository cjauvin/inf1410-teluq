---
title: "Les données"
slug: "données"
weight: 40
bookCollapseSection: true
---

# Les données dans le contexte du génie logiciel

Le créateur du langage Pascal, le célèbre informaticien suisse Niklaus Wirth, a
publié en 1976 un livre intitulé *Algorithms + Data Structures = Programs*. Le
titre résume une intuition fondamentale&nbsp;: un programme n'est pas seulement une
séquence d'instructions, c'est aussi, et peut-être surtout, une manière
d'organiser des données. Cette intuition prend une dimension nouvelle quand on
passe du programme au système. Dans un programme simple, les données vivent en
mémoire, dans des variables et des structures que le programmeur contrôle
directement. Dans un système, elles traversent des frontières&nbsp;: entre processus,
entre machines, entre équipes. Elles doivent être représentées dans des formats
que d'autres pourront lire, stockées dans des systèmes qui survivent aux
redémarrages, et interrogées par des composants qui ne partagent pas le même
code.

Le livre *Designing Data-Intensive Applications* de Martin Kleppmann, publié en
2017, est devenu en quelques années la référence incontournable sur ces
questions. Kleppmann y montre que les choix liés aux données (comment les
encoder, où les stocker, comment garantir leur cohérence) ne sont pas des
détails techniques périphériques, mais des décisions architecturales qui
façonnent profondément la structure et le comportement d'un système. Cette
section s'inspire largement de sa vision pour explorer les trois facettes des
données dans un système logiciel.

{{< image src="kleppmann-data-book.webp" alt="" title="" loading="lazy" >}}

On commencera par la **représentation**, en examinant comment les données sont
encodées et sérialisées pour traverser les frontières d'un système, et comment
les schémas formalisent un contrat entre les composants qui les produisent et
ceux qui les consomment. On passera ensuite au **stockage**, en retraçant
l'évolution des bases de données, du modèle hiérarchique des années 60 jusqu'aux
bases spécialisées d'aujourd'hui, en passant par le modèle relationnel et la
révolution NoSQL. Enfin, on explorera les paradigmes **au-delà des bases de
données**, notamment la recherche et l'indexation, le stockage d'objets, les
données répliquées et les registres distribués.
