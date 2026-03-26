---
title: "Module 2 - Concevoir un programme correct"
weight: 200
bookCollapseSection: true
---

# Module 2 - Concevoir un programme correct

Dans le module précédent, on a vu que le génie logiciel est né d'un constat :
programmer et construire du logiciel fiable sont deux choses très différentes.
Mais avant de parler d'architecture, d'équipes ou de déploiement, il faut
s'arrêter sur ce que signifie vraiment programmer. En 1985, l'informaticien
danois Peter Naur publie un article au titre provocateur [*Programming as Theory
Building*](https://pages.cs.wisc.edu/~remzi/Naur.pdf). Sa thèse centrale est que
programmer n'est pas produire du code. C'est construire une théorie, un modèle
mental du problème qu'on cherche à résoudre. Le code n'est qu'un artefact
secondaire de cette compréhension. Un programmeur qui comprend profondément son
domaine peut modifier, adapter et faire évoluer son logiciel avec assurance. Un
autre programmeur, même s'il a accès au même code source et à toute la
documentation du monde, ne pourra pas le maintenir aussi efficacement sans avoir
reconstruit ce modèle mental pour lui-même.

{{< image src="naur.jpg" alt="Peter Naur" title="" loading="lazy" >}}

Cette idée a des conséquences profondes. Si la valeur réelle du travail de
programmation réside dans le modèle mental plutôt que dans le code, alors les
outils du programmeur ne servent pas seulement à produire du code : ils servent
à construire, vérifier et préserver ce modèle mental. Les types permettent de
formaliser les contraintes qu'on a en tête. Les tests vérifient que notre
compréhension du problème correspond bien au comportement du programme. Le
versioning avec git préserve l'historique de nos décisions et de leur évolution.
La gestion des dépendances nous permet d'intégrer le travail et la compréhension
des autres dans notre propre modèle. Et l'intégration continue automatise la
vérification constante que tout tient ensemble. Ce sont ces outils que nous
allons explorer dans ce module.