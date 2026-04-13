---
title: "Module 4 - Construire en équipe"
weight: 400
bookCollapseSection: true
---

# Module 4 - Construire en équipe

Dans le module 2, nous avons exploré les outils du programmeur individuel : les
tests, git, la gestion des dépendances. Dans le module 3, nous avons vu comment
un programme devient un système, avec ses couches, ses APIs, ses données. Mais
un logiciel d'une certaine envergure n'est presque jamais le produit d'une seule
personne. Dès qu'une équipe est impliquée, un nouveau type de complexité
apparaît, qui n'est ni algorithmique ni architecturale : c'est la complexité de
la coordination humaine.

Fred Brooks, dans *The Mythical Man-Month* (1975), a formulé ce problème de
manière mémorable. Sa loi la plus célèbre dit qu'ajouter des personnes à un
projet en retard ne fait que le retarder davantage. La raison est simple : la
communication entre les membres d'une équipe croît de manière quadratique. Deux
personnes ont un seul canal de communication. Trois en ont trois. Dix en ont
quarante-cinq. Chaque nouvelle personne doit se synchroniser avec toutes les
autres, comprendre le contexte, s'aligner sur les décisions déjà prises. Le
travail de coordination finit par consommer une part significative de l'effort
total, parfois plus que le travail productif lui-même.

{{< image src="brooks-teams.png" alt="" title="" loading="lazy" >}}

Une deuxième idée fondatrice pour ce module vient de Melvin Conway, qui a
observé en 1968 que la structure d'un logiciel tend à refléter la structure de
l'organisation qui le produit. Si trois équipes construisent un compilateur, on
obtiendra un compilateur en trois passes. Cette observation, devenue la "loi de
Conway", a des implications profondes : elle suggère que les problèmes
d'architecture logicielle sont souvent, au fond, des problèmes d'organisation
humaine. On ne peut pas concevoir un système modulaire avec une équipe
monolithique, ni un système intégré avec des équipes cloisonnées.
L'architecture et l'organisation co-évoluent, qu'on le veuille ou non.

{{< image src="conway-teams.png" alt="" title="" loading="lazy" >}}

Ce module explore les différentes facettes de cette coordination. Nous
commencerons par étendre notre connaissance de git vers son usage distribué avec
GitHub, en explorant les mécanismes de collaboration qu'il rend possible : les
pull requests, les workflows de branches, les code reviews. Nous prendrons
ensuite du recul pour examiner les cadres organisationnels qui ont émergé pour
structurer le travail en équipe, en particulier le mouvement agile et ses
méthodes concrètes comme Scrum et Kanban. Enfin, nous aborderons les outils et
pratiques de gestion de projet au quotidien : l'estimation, la documentation, la
communication.