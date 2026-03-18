---
title: "Kanban"
slug: "kanban"
weight: 20
---

# La méthode Kanban

Le mot *kanban* (看板) signifie littéralement « panneau visuel » ou « enseigne »
en japonais. Le concept naît dans les usines Toyota dans les années 1940-1950,
sous l'impulsion de Taiichi Ohno, ingénieur et futur vice-président de
l'entreprise. Ohno cherche à éliminer le gaspillage (*muda*) dans la production
automobile. Son idée centrale est simple : au lieu de produire en grandes
quantités puis de stocker, chaque poste de travail ne produit que ce que le
poste suivant lui demande. Pour signaler ce besoin, on utilise une carte
physique (un *kanban*) qui circule entre les postes. Quand un poste a besoin de
pièces, il envoie un kanban au poste en amont, qui lance alors la production.
C'est un système *à flux tiré* (*pull system*) : le travail est déclenché par
la demande réelle, pas par une planification centrale. Ce principe est au cœur
du *Toyota Production System* (TPS), qui deviendra l'une des plus grandes
innovations de l'histoire industrielle du XXe siècle.

C'est en 2010 que David Anderson publie *Kanban: Successful Evolutionary Change
for Your Technology Business*, qui formalise l'adaptation de ces idées au
développement logiciel. Anderson ne propose pas de révolutionner la manière de
travailler d'une équipe du jour au lendemain. Au contraire, son approche est
explicitement évolutive : on part du processus existant, on le rend visible, et
on l'améliore graduellement. C'est une philosophie très différente de Scrum, qui
impose dès le départ un cadre structuré avec des rôles et des cérémonies
définis.

## Les principes fondamentaux

La méthode Kanban repose sur un petit nombre de principes, qu'Anderson résume en
six pratiques. Trois d'entre elles sont particulièrement centrales pour
comprendre la différence avec Scrum.

Le premier principe est de *visualiser le flux de travail*. C'est le tableau
Kanban que nous avons déjà rencontré dans la
[section sur Scrum]({{< relref "/docs/module4/agile/scrum" >}}) : des colonnes
qui représentent les étapes du processus, et des cartes qui se déplacent de
gauche à droite. Mais là où une équipe Scrum utilise le tableau comme un outil
parmi d'autres au sein d'un cadre plus large (sprints, cérémonies, rôles), en
Kanban le tableau *est* le cadre. Tout le fonctionnement de l'équipe tourne
autour de ce qu'il révèle.

Le deuxième principe est de *limiter le travail en cours* (*Work In Progress*,
ou WIP). C'est l'idée la plus contre-intuitive de Kanban, et probablement la
plus puissante. L'intuition naturelle est que pour aller plus vite, il faut
travailler sur plus de choses en parallèle. Kanban affirme le contraire : en
limitant le nombre de tâches qui peuvent se trouver simultanément dans chaque
colonne, on force l'équipe à terminer ce qu'elle a commencé avant de commencer
autre chose. Si la colonne *In Progress* a une limite de 2 et qu'elle est
pleine, personne ne peut y ajouter une nouvelle tâche tant qu'une des deux en
cours n'a pas avancé vers la colonne suivante. Ce mécanisme crée une pression
saine : au lieu d'accumuler du travail partiellement fait, l'équipe se concentre
sur ce qui est le plus près d'être terminé. C'est le même principe que le flux
tiré de Toyota : le travail en aval « tire » le travail en amont, plutôt que
l'amont qui « pousse » du travail vers l'aval.

L'analogie la plus parlante est celle d'une autoroute. Quand une autoroute est
peu chargée, les voitures circulent vite et le débit est élevé. Quand on ajoute
trop de voitures, tout le monde ralentit, et au-delà d'un certain seuil, c'est
l'embouteillage : le débit réel (le nombre de voitures qui arrivent à
destination par heure) diminue alors même que le nombre de voitures sur la route
augmente. Limiter le WIP revient à réguler l'accès à l'autoroute pour maintenir
un débit optimal.

<!-- ILLUSTRATION: analogie autoroute — deux ou trois états (fluide, dense, embouteillé) montrant que le débit diminue quand le nombre de voitures augmente -->

<!-- ILLUSTRATION: deux tableaux Kanban côte à côte — un sans limites de WIP (cartes accumulées partout, chaos) et un avec limites (flux propre, peu de cartes par colonne) -->

Le troisième principe est le *flux continu*. Contrairement à Scrum, Kanban ne
découpe pas le temps en sprints. Il n'y a pas de sprint planning, pas de date de
fin fixe, pas d'engagement sur un lot de tâches. Le travail entre dans le
système de manière continue (quand une tâche est terminée, on en tire une
nouvelle du backlog) et en sort de manière continue. Le rythme n'est pas donné
par un calendrier, mais par la capacité réelle de l'équipe, telle que révélée
par les limites de WIP et le flux observable sur le tableau.

## Mesurer le flux

En Scrum, la performance de l'équipe se mesure principalement par la vélocité :
le nombre de story points complétés par sprint. Kanban utilise des métriques
différentes, centrées sur le temps plutôt que sur le volume. Les deux plus
importantes sont le *cycle time* et le *lead time*.

Le cycle time mesure le temps qu'une tâche passe dans le système actif,
c'est-à-dire entre le moment où quelqu'un commence à travailler dessus (elle
entre dans *In Progress*) et le moment où elle est terminée (elle arrive dans
*Done*). Le lead time, lui, mesure le temps total entre le moment où la tâche
est demandée (elle entre dans *Todo* ou dans le backlog) et le moment où elle
est livrée. Le lead time est toujours supérieur ou égal au cycle time, car il
inclut le temps d'attente avant que quelqu'un ne prenne la tâche en charge.

Ces deux métriques sont complémentaires. Le cycle time reflète l'efficacité de
l'équipe une fois qu'elle commence à travailler sur quelque chose. Le lead time
reflète l'expérience du point de vue du client ou du demandeur : combien de
temps entre « j'ai besoin de cette fonctionnalité » et « elle est disponible ».
Si le cycle time est court mais le lead time est long, cela signifie que les
tâches passent beaucoup de temps à attendre dans la file avant d'être prises en
charge, ce qui est un signal que les limites de WIP sont peut-être trop basses,
ou que le backlog est trop chargé. C'est ce type d'analyse que Kanban
encourage : observer les données du flux pour identifier les goulots
d'étranglement et ajuster le processus en conséquence.

## Démonstration avec GitHub Projects

Pour illustrer concrètement comment Kanban fonctionne, reprenons le projet
RéservaSalle. Imaginons que l'équipe, après quelques sprints avec Scrum, décide
d'expérimenter avec Kanban. Le backlog et les issues restent les mêmes, mais
l'organisation du travail change.

La première différence se voit dans la configuration du projet GitHub Projects.
Le tableau garde les mêmes quatre colonnes (*Todo*, *In Progress*, *In Review*,
*Done*), mais deux champs disparaissent : les story points et les itérations. En
Kanban, on n'estime pas la taille des tâches à l'avance, et on ne découpe pas
le temps en sprints. En revanche, on ajoute quelque chose que Scrum n'avait
pas : des *limites de travail en cours* sur les colonnes. Dans GitHub Projects,
chaque colonne de la vue Board peut se voir attribuer une limite. On configure
par exemple une limite de 2 pour *In Progress* et de 2 pour *In Review*. Ces
limites ne sont pas bloquantes dans GitHub Projects (l'outil affiche un
avertissement visuel quand la limite est dépassée, mais n'empêche pas d'ajouter
une carte), ce qui correspond bien à l'esprit de Kanban : la limite est une
convention d'équipe, pas une contrainte technique.

<!-- ILLUSTRATION: tableau Kanban dans GitHub Projects avec les limites de WIP visibles sur les colonnes In Progress (2) et In Review (2) -->

Le flux de travail quotidien ressemble à celui de Scrum, mais sans la cadence
imposée par les sprints. L'équipe consulte le tableau chaque matin et applique
une règle simple : avant de commencer une nouvelle tâche, vérifier s'il y a
quelque chose à débloquer en aval. Si la colonne *In Review* contient deux
cartes (sa limite), la priorité n'est pas de coder quelque chose de nouveau,
mais de faire une revue de code pour libérer de la place. Ce réflexe, qu'on
appelle parfois « stop starting, start finishing », est le changement de
mentalité le plus important qu'apporte Kanban.

Concrètement, imaginons que Sara et Marco travaillent sur les issues #1 et #6
(la colonne *In Progress* est pleine à sa limite de 2). Sara termine l'issue #1
et la déplace vers *In Review*. Elle ne peut pas immédiatement prendre l'issue
#2 dans *In Progress*, car Marco y est encore avec l'issue #6. Mais la limite de
*In Review* est à 2 et il n'y a qu'une seule carte, donc Sara pourrait
techniquement prendre une nouvelle tâche si une place se libère dans *In
Progress*. En attendant, Marco termine #6 et la déplace aussi vers *In Review*.
Maintenant, *In Review* est pleine (2/2) et *In Progress* est vide. L'équipe
doit se concentrer sur les revues avant de tirer de nouvelles tâches. Sara fait
la revue de #6, Marco fait la revue de #1, les deux passent dans *Done*, et
l'équipe peut tirer les prochaines tâches prioritaires du backlog.

<!-- ILLUSTRATION: séquence de 3-4 états du tableau montrant le flux Kanban avec les limites de WIP en action -->

Ce mécanisme crée un rythme naturel qui n'a pas besoin d'être imposé par un
calendrier. Les tâches entrent et sortent du système en continu, et la vitesse à
laquelle elles le traversent dépend directement de la capacité réelle de
l'équipe, telle que régulée par les limites de WIP.

## Scrum, Kanban, ou les deux ?

Scrum et Kanban répondent au même besoin fondamental, celui de gérer la
complexité du développement logiciel de manière adaptative, mais ils le font
avec des philosophies différentes. Scrum impose une structure : des rôles
définis, des cérémonies régulières, des sprints de durée fixe. Cette structure
est rassurante, surtout pour les équipes qui débutent avec l'agilité, car elle
fournit un cadre clair et des points de synchronisation réguliers. Kanban, à
l'inverse, n'impose presque rien : pas de rôles prescrits, pas de cérémonies
obligatoires, pas de découpage temporel. Sa seule contrainte réelle est la
limite de travail en cours, et c'est cette contrainte minimale qui régule tout
le système.

Dans la pratique, beaucoup d'équipes ne choisissent pas strictement l'une ou
l'autre méthode. Elles empruntent des éléments aux deux, ce qu'on appelle
parfois *Scrumban*. Par exemple, une équipe pourrait garder les sprints et les
cérémonies de Scrum tout en ajoutant des limites de WIP sur son tableau, ou bien
utiliser un flux continu à la Kanban tout en conservant une rétrospective
régulière. L'important n'est pas la pureté de la méthode, mais que l'équipe
comprenne les principes sous-jacents et choisisse consciemment les pratiques qui
fonctionnent pour elle.

Le choix entre les deux dépend souvent du contexte. Scrum convient bien aux
équipes qui développent un produit avec des cycles de livraison réguliers, où la
prévisibilité est importante et où les parties prenantes ont besoin de points de
contact fréquents. Kanban est plus adapté aux équipes qui gèrent un flux de
travail continu et varié, comme une équipe de maintenance, une équipe DevOps, ou
une équipe de support qui traite des demandes au fil de l'eau. Mais ces
distinctions ne sont pas absolues : ce qui compte, c'est d'observer son propre
flux de travail, d'identifier ce qui le freine, et d'ajuster. C'est, au fond,
le message commun de toutes les approches agiles.