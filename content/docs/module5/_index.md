---
title: "Module 5 - Faire vivre le logiciel"
weight: 500
bookCollapseSection: true
---

# Faire vivre le logiciel

Dans les modules précédents, nous avons construit un logiciel de manière
méthodique : les outils du programmeur individuel (module 2), l'architecture d'un
système (module 3), la coordination en équipe (module 4). Mais tout ce travail
converge vers un moment critique : celui où le logiciel quitte l'environnement du
développeur pour rencontrer ses utilisateurs. Un programme qui passe tous ses
tests sur la machine d'un développeur, mais qui ne tourne nulle part, n'est pas
vraiment un logiciel. Il ne le devient que lorsqu'il est déployé, accessible, et
maintenu en condition opérationnelle. Ce passage du développement à la production
est le sujet de ce module.

Pendant longtemps, cette transition a été marquée par une frontière nette entre
deux mondes. D'un côté, les développeurs, dont le travail consistait à écrire du
code et à livrer de nouvelles fonctionnalités. De l'autre, les équipes
d'opérations (les "ops"), responsables de faire tourner ce code en production :
gérer les serveurs, surveiller les performances, répondre aux pannes à trois
heures du matin. Ces deux groupes avaient des incitatifs contradictoires. Les
développeurs voulaient livrer vite, changer les choses. Les ops voulaient de la
stabilité, éviter les surprises. Le résultat était prévisible : un mur, souvent
matérialisé par un processus formel de "mise en production", où les développeurs
lançaient leur code par-dessus la clôture avec un message implicite : "on l'a
codé, maintenant c'est votre problème". Un cas particulier emblématique de cette
séparation était celui du DBA (database administrator), un rôle dédié qui
contrôlait l'accès aux bases de données de production, validait et appliquait les
modifications de schéma, et servait de gardien entre le code des développeurs et
les données en production. Un développeur qui avait besoin d'ajouter une colonne
à une table devait soumettre une demande au DBA, souvent accompagnée de
justifications, et attendre. Cette friction, bien qu'elle existait pour de bonnes
raisons (protéger l'intégrité des données), illustrait parfaitement le coût de la
séparation rigide entre ceux qui écrivent le code et ceux qui gèrent
l'infrastructure.

## Le mouvement DevOps

C'est en réaction à cette séparation que le mouvement DevOps a émergé à la fin
des années 2000. Le terme lui-même, une contraction de "development" et
"operations", a été popularisé lors des premières conférences DevOpsDays,
organisées par Patrick Debois à partir de 2009 en Belgique. Mais c'est le roman
*The Phoenix Project* (Gene Kim, Kevin Behr et George Spafford, 2013) qui a
donné au mouvement son récit fondateur. Le livre raconte l'histoire de Bill, un
responsable IT qui hérite d'un projet catastrophique dans une entreprise en
crise, et qui découvre progressivement que les principes du lean manufacturing
(issus du système de production de Toyota, que nous avons rencontré avec Kanban
dans le module précédent) peuvent s'appliquer à la livraison logicielle. Le
parallèle est frappant : de la même manière qu'une usine doit optimiser le flux
de production de bout en bout plutôt que de maximiser l'efficacité de chaque
poste individuellement, une organisation logicielle doit penser le flux du code
depuis le commit du développeur jusqu'à l'utilisateur en production.

{{< image src="phoenix-project.jpg" alt="" title="" loading="lazy" >}}

Gene Kim, dans *The Phoenix Project* puis de manière plus formelle dans *The
DevOps Handbook* (2016, co-écrit avec Jez Humble, Patrick Debois et John Willis),
articule la philosophie DevOps autour de trois "voies". La première voie est
celle du *flow* : accélérer le mouvement du travail de gauche à droite, du
développement vers la production. C'est le domaine du déploiement continu, de
l'automatisation, de la conteneurisation. La deuxième voie est celle du
*feedback* : créer des boucles de rétroaction rapides de droite à gauche, de la
production vers le développement. C'est le domaine de l'observabilité, du
monitoring, des alertes. La troisième voie est celle de l'*apprentissage
continu* : cultiver une culture d'expérimentation et d'amélioration, où les
échecs sont des occasions d'apprendre plutôt que des fautes à punir. C'est le
domaine des postmortems, du chaos engineering, des error budgets. Ces trois voies
serviront de fil conducteur pour ce module : chacune des sections qui suivent
s'inscrit naturellement dans l'une d'entre elles.

Une autre référence importante pour ce module est *The Twelve-Factor App*, un
manifeste publié en 2011 par Adam Wiggins, cofondateur de Heroku, l'une des
premières plateformes cloud de type PaaS (Platform as a Service). Ce document
propose douze principes pour concevoir des applications qui se déploient et
s'opèrent bien dans un environnement cloud moderne. Certains de ces principes
nous sont déjà familiers : la gestion des dépendances (facteur II, qui rejoint
ce que nous avons vu dans le module 2 avec uv), ou le stockage du code dans un
système de versioning (facteur I). D'autres, comme la gestion de la
configuration par variables d'environnement (facteur III), le traitement des logs
comme des flux d'événements (facteur XI), ou la stricte séparation entre les
phases de build, release et run (facteur V), seront développés dans les sections
qui suivent, là où ils sont le plus pertinents. Plutôt qu'un dogme à suivre
aveuglément, la Twelve-Factor App est un ensemble d'heuristiques qui, comme les
principes SOLID ou DRY, encapsulent des leçons durement apprises par des
praticiens confrontés aux réalités de la production.

Ce module s'articule autour de six thèmes qui structurent l'exploitation d'un
logiciel. D'abord, **l'infrastructure** : l'évolution des serveurs physiques au
cloud en passant par la conteneurisation et l'orchestration. Ensuite, **le
déploiement continu** : les pipelines et les stratégies pour livrer du code en
production de manière fiable. Puis, **l'observabilité** : la capacité à
comprendre ce qui se passe à l'intérieur d'un système en production. Suivie de
**la fiabilité et les incidents** : la gestion des pannes et la culture
d'apprentissage qui permet de s'améliorer après chaque incident. Ensuite, **la
sécurité** : les menaces auxquelles un logiciel en production est exposé et les
pratiques pour s'en protéger. Enfin, **la scalabilité** : le caching et les
compromis architecturaux qui permettent à un système de servir un nombre
croissant d'utilisateurs.