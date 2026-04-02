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

Cette vision de la programmation comme activité intellectuelle plutôt que
mécanique n'est pas isolée. En 1971, Gerald Weinberg publie *The Psychology of
Computer Programming*, un livre pionnier qui aborde le développement logiciel
sous l'angle de la psychologie humaine. Son argument central est que la qualité
d'un logiciel dépend moins des outils ou des méthodes que de l'attitude des
personnes qui le construisent. Weinberg introduit la notion d'*egoless
programming* : l'idée que les programmeurs doivent apprendre à dissocier leur ego
de leur code, à accueillir les critiques et les corrections comme des
contributions plutôt que comme des attaques personnelles. Un programmeur qui
cache ses erreurs ou qui refuse qu'on relise son code produit un logiciel moins
fiable qu'un programmeur qui expose son travail et cherche activement les failles
dans son propre raisonnement. Cette idée, radicale pour l'époque, annonce des
pratiques qui sont devenues centrales dans le développement moderne : la revue de
code, les tests comme filet de sécurité, et plus largement l'idée que la qualité
est la responsabilité de chaque programmeur, pas celle d'une équipe d'inspection
séparée.

Cette idée a des conséquences profondes. Si la valeur réelle du travail de
programmation réside dans le modèle mental plutôt que dans le code, alors les
outils du programmeur ne servent pas seulement à produire du code : ils servent
à construire, vérifier et préserver ce modèle mental. Les types et les
structures de données permettent de formaliser les contraintes et les règles
logiques qu'on a en tête. Les tests vérifient que notre compréhension du
problème correspond bien au comportement du programme. Le versioning avec git
préserve l'historique de nos décisions et de leur évolution. La gestion des
dépendances nous permet d'intégrer le travail et la compréhension des autres
dans notre propre modèle. Et l'intégration continue automatise la vérification
constante que tout tient ensemble. Ce sont ces outils que nous allons explorer
dans ce module.