---
title: "Principes et idées clés"
weight: 15
---

# Principes et idées clés du génie logiciel

Cette page rassemble les principes et idées importantes qui traversent
l'ensemble du cours. Chaque principe est traité en profondeur dans le module où
il est le plus pertinent ; les liens ci-dessous pointent vers ces sections.

## Gestion de la complexité

- **Complexité essentielle vs accidentelle** (Fred Brooks, *No Silver Bullet*, 1986) → [Module 3, Introduction]({{< ref "/docs/module3" >}}), [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})

## Principes de conception

- **Information hiding** (David Parnas, 1972) : chaque module cache une décision de conception susceptible de changer → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- **DRY** (Don't Repeat Yourself, Hunt & Thomas, *The Pragmatic Programmer*, 1999) : chaque connaissance doit avoir une représentation unique → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- **KISS** (Keep It Simple Stupid)
- **YAGNI** (You Ain't Gonna Need It, Kent Beck, Extreme Programming) : ne construis pas d'abstraction pour un besoin qui n'existe pas encore → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- **Separation of Concerns** : diviser un système en parties qui traitent chacune un aspect distinct du problème → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}}), [Module 3, Les données (OLTP vs OLAP)]({{< ref "/docs/module3/40-données/20-stockage" >}})
- **SOLID** (Robert C. Martin, *Agile Software Development*, 2003) : cinq principes de conception OO (S, O, L, I, D) → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- **Design patterns** (Gang of Four, *Design Patterns*, 1994) : vocabulaire partagé de solutions récurrentes à des problèmes de conception ; plusieurs patrons classiques sont absorbés par les langages modernes → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- **Convention over Configuration** (David Heinemeier Hansson, Rails, 2004) : préférer des conventions par défaut sensées à une configuration explicite, pour réduire les décisions répétitives → [Module 3, L'architecture des applications web]({{< ref "/docs/module3/30-interfaces/20-architectures-web" >}})
- **Law of Demeter**
- **Composition over inheritance** (Gang of Four, *Design Patterns*, 1994) : favoriser l'assemblage d'objets plutôt que l'héritage de classes → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- **Loi de Conway** (Melvin Conway, 1967) : la structure d'un système reflète la structure de communication de l'organisation qui le produit → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}}), [Module 4, Scrum]({{< ref "/docs/module4/20-agile/10-scrum" >}}), [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})
- **Manœuvre de Conway inverse** (LeRoy et Simons, 2010) : structurer délibérément les équipes pour obtenir l'architecture souhaitée → [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})
- **Principle of Least Astonishment (POLA)**
- **Principe du moindre privilège** (*Principle of Least Privilege*) : chaque composant d'un système ne devrait avoir accès qu'aux ressources strictement nécessaires à sa tâche → [Module 5, Est-ce que c'est sécuritaire ?]({{< ref "/docs/module5/50-securite" >}})
- **Idempotence** : une opération qu'on peut exécuter plusieurs fois avec le même résultat, propriété cruciale pour les APIs réseau → [Module 3, Les APIs]({{< ref "/docs/module3/20-apis" >}}), [Module 5, Comment je le déploie ?]({{< ref "/docs/module5/20-deploiement" >}})
- **Immutable infrastructure** : ne jamais modifier un artefact déployé, toujours le remplacer. Lien avec l'immutabilité en programmation fonctionnelle → [Module 5, Comment je le déploie ?]({{< ref "/docs/module5/20-deploiement" >}})

## Concurrence et parallélisme

- **La concurrence n'est pas le parallélisme** (Rob Pike, 2012)&nbsp;: la concurrence
  est une manière de structurer un programme en tâches indépendantes, le
  parallélisme une manière de l'exécuter sur plusieurs coeurs. La première est
  une propriété du code, la seconde une propriété de la machine. Un programme
  découpé en dix tâches sur une machine à un seul coeur est parfaitement
  concurrent et n'a aucun parallélisme → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/15-concurrence/10-pourquoi" >}}),
  [Module 2, Processus et threads]({{< ref "/docs/module2/15-concurrence/20-processus-et-threads" >}})
- **Les threads pour attendre, les processus pour calculer**&nbsp;: en Python, le
  verrou global (GIL) empêche deux threads d'exécuter du code simultanément,
  mais un thread qui attend le relâche. Les threads n'accélèrent donc jamais un
  calcul et accélèrent énormément une série d'attentes → [Module 2, Processus et threads]({{< ref "/docs/module2/15-concurrence/20-processus-et-threads" >}})
- **Préemption** (par opposition au multitâche coopératif)&nbsp;: le système
  d'exploitation reprend la main sur un programme sans lui demander son avis,
  plutôt que de compter sur sa bonne volonté. Comme la protection mémoire, la
  garantie naît sur les gros systèmes des années 60 et met trente ans à
  atteindre les machines personnelles → [Module 2, Processus et threads]({{< ref "/docs/module2/15-concurrence/20-processus-et-threads" >}})
- **Condition de course** (*race condition*)&nbsp;: quand le résultat d'un
  programme dépend de l'ordre dans lequel ses threads s'entrelacent, ordre que
  personne ne choisit. Le programme n'est pas faux, il est parfois faux, et ses
  tests passent → [Module 2, Ce qui casse]({{< ref "/docs/module2/15-concurrence/30-ce-qui-casse" >}})
- **Interblocage** (*deadlock*, Dijkstra, 1965)&nbsp;: deux threads qui tiennent
  chacun le verrou dont l'autre a besoin s'attendent pour toujours, sans
  planter ni rien signaler. La règle qui l'évite tient en une ligne, toujours
  prendre les verrous dans le même ordre, et elle est difficile à tenir parce
  qu'elle doit valoir pour tout le programme → [Module 2, Ce qui casse]({{< ref "/docs/module2/15-concurrence/30-ce-qui-casse" >}})
- **On achète la correction avec de la vitesse**&nbsp;: un verrou remet les
  threads en file indienne devant ce qu'il protège, et une file indienne n'est
  pas du parallélisme. Protéger le moins possible pour en perdre le moins
  possible → [Module 2, Ce qui casse]({{< ref "/docs/module2/15-concurrence/30-ce-qui-casse" >}})
- **CPU-bound et I/O-bound**&nbsp;: un programme est lent soit parce qu'il calcule,
  limité par le processeur, soit parce qu'il attend, limité par les
  entrées-sorties. Les deux se ressemblent vus du dehors et leurs remèdes sont
  opposés, des coeurs pour le premier, ne jamais bloquer pour le second → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/15-concurrence/10-pourquoi" >}})
- **Loi d'Amdahl** (Gene Amdahl, 1967)&nbsp;: la part d'un programme qu'on ne peut
  pas répartir fixe un plafond au gain du parallélisme. Avec 10&nbsp;% de travail
  séquentiel, dix coeurs donnent un peu plus de cinq fois, et une infinité de
  coeurs jamais plus de dix → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/15-concurrence/10-pourquoi" >}})
- **Loi de Moore** (Gordon Moore, 1965)&nbsp;: le nombre de composants gravés sur une
  puce, à coût égal, double à intervalle régulier. Elle porte sur la quantité de
  transistors, et non sur la vitesse, contrairement à ce qu'on lui fait souvent
  dire → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/15-concurrence/10-pourquoi" >}})
- **Loi de Dennard** (Robert Dennard, 1974)&nbsp;: en réduisant les transistors, la
  puissance dissipée par unité de surface reste constante. C'est elle, et non
  celle de Moore, qui a cessé de s'appliquer vers 2004, forçant l'industrie à
  multiplier les coeurs plutôt que les cycles → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/15-concurrence/10-pourquoi" >}})

## Principes de systèmes distribués

- **Théorème CAP** (Eric Brewer, 2000) : un système distribué ne peut garantir simultanément que deux des trois propriétés suivantes : cohérence, disponibilité, tolérance aux partitions → [Module 5, Est-ce que ça va tenir la charge ?]({{< ref "/docs/module5/60-scalabilite" >}})
- **Premature optimization** (Donald Knuth) : « Premature optimization is the root of all evil. » Ne pas concevoir pour des millions d'utilisateurs avant d'en avoir besoin → [Module 5, Est-ce que ça va tenir la charge ?]({{< ref "/docs/module5/60-scalabilite" >}})

## Principes de mesure et d'observation

- **Loi de Goodhart** (Charles Goodhart, 1975) : « Lorsqu'une mesure devient un objectif, elle cesse d'être une bonne mesure. » → [Module 4, L'agilité (critique)]({{< ref "/docs/module4/20-agile" >}})
- **Dette technique** (Ward Cunningham, 1992) : le code imparfait livré consciemment est une dette qui génère des intérêts → [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})

## Principes de pratique

- **Refactoring** (Martin Fowler, *Refactoring*, 1999) : modifier la structure interne du code sans changer son comportement observable, mécanisme de remboursement de la dette technique → [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})
- **Egoless programming** (Gerald Weinberg, *The Psychology of Computer Programming*, 1971) : dissocier son ego de son code, accueillir les critiques comme des contributions → [Module 2, Introduction]({{< ref "/docs/module2" >}})
- **Shift left** : déplacer les vérifications de qualité le plus tôt possible dans le processus de développement, plutôt que de les confier à une équipe séparée en aval → [Module 2, L'intégration continue]({{< ref "/docs/module2/50-ci" >}})
- **Boy Scout Rule** : "Always leave the campground cleaner than you found it."
