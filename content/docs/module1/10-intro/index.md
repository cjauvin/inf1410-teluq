---
title: "Introduction"
slug: "intro"
weight: 10
---

# Introduction au génie logiciel

Le logiciel est partout. Il fait fonctionner les téléphones, les voitures, les hôpitaux, les banques, les avions. Pourtant, malgré des décennies de progrès, construire du logiciel reste une activité notoirement difficile. Les projets dépassent leurs budgets, les délais explosent, les bogues s'accumulent. En 1994, le Standish Group publiait son rapport *CHAOS*, révélant que seulement 16% des projets logiciels étaient livrés à temps et dans les limites du budget. Trente ans plus tard, les échecs spectaculaires continuent de faire les manchettes. Au Québec, le projet SAAQclic de la Société de l'assurance automobile, estimé à 638 millions de dollars en 2017, a fini par coûter plus de 1,1 milliard, et son déploiement en 2023 a été marqué par des pannes majeures et des dépassements de coûts dissimulés pendant des années. Le génie logiciel, en tant que discipline, est né de ce constat : il ne suffit pas de savoir programmer pour construire du logiciel qui fonctionne.

Mais qu'est-ce que le génie logiciel, au juste? On pourrait le définir simplement comme l'ensemble des pratiques qui permettent de construire du logiciel de manière fiable, à une échelle qui dépasse celle du programmeur individuel. Programmer, c'est écrire du code qui résout un problème. Faire du génie logiciel, c'est s'assurer que ce code puisse être compris par d'autres, testé, modifié, déployé et maintenu pendant des années. Un programme écrit seul, en une nuit, pour un usage unique, n'a pas besoin de génie logiciel. Mais dès qu'un deuxième développeur entre en jeu, dès que le logiciel doit survivre à sa première version, les questions changent de nature : comment organiser le code? Comment s'assurer qu'une modification n'en brise pas une autre? Comment coordonner le travail de plusieurs personnes sur la même base de code?

Fred Brooks, dans son essai célèbre *No Silver Bullet* (1986), propose une distinction éclairante entre deux types de complexité. La **complexité essentielle** est celle qui est inhérente au problème qu'on tente de résoudre : les règles d'affaires, les cas limites, les interactions entre les composantes d'un système. La **complexité accidentelle** est celle qu'on s'impose à soi-même par nos choix d'outils, de langages, d'architecture ou de processus. Par exemple, considérons un système qui doit calculer le prix d'une commande avec taxes et rabais :

```python
def calculer_prix(items, rabais_pct, taux_taxe):
    sous_total = sum(item.prix * item.quantite for item in items)
    rabais = sous_total * rabais_pct / 100
    taxe = (sous_total - rabais) * taux_taxe / 100
    return sous_total - rabais + taxe
```

La logique elle-même (sous-total, rabais, taxe) est de la complexité essentielle. Mais si cette fonction de cinq lignes se retrouve enfouie dans un *framework* (cadriciel) de mille lignes de configuration, de couches d'abstraction et de patrons de conception superflus, on a ajouté de la complexité accidentelle. Une bonne partie du génie logiciel consiste justement à minimiser cette complexité accidentelle, tout en gérant efficacement la complexité essentielle.

Ce cours propose d'explorer le génie logiciel à travers six modules qui suivent une progression naturelle. On commence par le présent module, qui pose les bases historiques et conceptuelles de la discipline. On passe ensuite aux pratiques du développeur individuel : le contrôle de version, la gestion des dépendances, les tests. Puis on élargit la perspective au logiciel comme système, avec ses composantes architecturales, ses données et ses interfaces. On aborde ensuite la dimension collective du développement, avec les méthodes de travail en équipe et la collaboration. Le cinquième module traite de la vie opérationnelle du logiciel : comment le déployer, le surveiller, le faire fonctionner de manière fiable. Enfin, on termine par un regard sur l'écosystème plus large du logiciel, incluant la culture de l'open source et l'impact croissant de l'intelligence artificielle sur la pratique du développement.