---
title: "Catastrophes, éthique et responsabilité"
weight: 40
slug: "catastrophes"
---

# Catastrophes, éthique et responsabilité

Les sections précédentes ont exploré les dynamiques économiques et politiques du
logiciel. Mais le logiciel n'est pas qu'un enjeu commercial : il contrôle des
avions, des appareils médicaux, des marchés financiers, des systèmes de paye.
Quand il échoue, les conséquences peuvent être mesurées en vies humaines, en
milliards de dollars ou en services publics paralysés pendant des années. Cette
section examine des cas où le logiciel a failli, non pas pour le plaisir morbide
du catalogue d'horreurs, mais parce que chaque catastrophe révèle quelque chose
de profond sur la manière dont on conçoit, teste, déploie et fait évoluer les
systèmes logiciels. Les leçons qu'on en tire font écho à pratiquement tout ce
que nous avons vu dans ce cours.

## Catastrophes techniques

Le cas le plus cité dans l'enseignement du génie logiciel est probablement celui
du Therac-25, un appareil de radiothérapie fabriqué par Atomic Energy of Canada
Limited (AECL). Entre 1985 et 1987, au moins six patients ont reçu des surdoses
massives de radiation, causant des décès et des blessures graves. Les versions
précédentes de la machine (Therac-6 et Therac-20) utilisaient des verrous
matériels (*hardware interlocks*) pour empêcher l'émission de doses dangereuses.
Le Therac-25 avait remplacé ces verrous par des contrôles purement logiciels, en
réutilisant du code des versions précédentes qui n'avait jamais été conçu pour
être la seule ligne de défense. Le bogue était une condition de course (*race
condition*) : si l'opérateur modifiait les paramètres de traitement trop
rapidement, le logiciel pouvait configurer la machine pour un faisceau à haute
énergie tout en affichant les paramètres d'un faisceau à faible énergie.
L'enquête a révélé que le logiciel n'avait jamais été soumis à une revue de code
indépendante, qu'il n'existait pas de tests systématiques, et que les rapports
d'incidents des hôpitaux avaient été ignorés par AECL pendant des mois. C'est un
cas qui illustre simultanément l'absence de tests (module 2), les dangers de la
réutilisation de code sans validation des hypothèses (module 3), et l'importance
d'une culture organisationnelle qui prend les signaux d'alarme au sérieux.

{{< image src="therac.webp" alt="" title="" loading="lazy" >}}

Le 4 juin 1996, la fusée Ariane 5 de l'Agence spatiale européenne a explosé 37
secondes après son lancement, détruisant une cargaison de satellites d'une
valeur d'environ 370 millions de dollars. La cause était un débordement
arithmétique (*integer overflow*) : un nombre à virgule flottante de 64 bits,
représentant la vitesse horizontale de la fusée, a été converti en un entier
signé de 16 bits. La valeur dépassait la capacité du type cible, ce qui a
provoqué une exception non gérée, l'arrêt du système de navigation inertiel, et
la perte de contrôle de la fusée. Le détail le plus frappant est que le code
fautif provenait du système de référence inertiel d'Ariane 4, où il
fonctionnait parfaitement. Ariane 4 avait une trajectoire de vol différente,
avec des vitesses horizontales plus faibles qui ne dépassaient jamais la capacité
d'un entier de 16 bits. Le code avait été réutilisé sans vérifier que les
hypothèses implicites du programme (la plage de valeurs possibles) restaient
valides dans le nouveau contexte. Pire encore, la conversion problématique
n'était même pas nécessaire au fonctionnement d'Ariane 5 : c'était du code
résiduel d'un alignement pré-lancement qui n'avait plus de raison d'être actif
après le décollage. Le rapport d'enquête, rédigé par un comité présidé par
Jacques-Louis Lions, est devenu un document de référence en génie logiciel. Il
illustre un thème récurrent : la réutilisation de code est une pratique
essentielle, mais elle exige de comprendre les hypothèses sous-jacentes, pas
seulement de copier ce qui a fonctionné ailleurs.

{{< image src="ariane5.jpg" alt="" title="" loading="lazy" >}}

Le 1er août 2012, la firme de trading Knight Capital a perdu 440 millions de
dollars en 45 minutes, un montant qui a failli entraîner la faillite de
l'entreprise. La cause était un déploiement bâclé. Knight avait développé un
nouveau module de trading pour se conformer à un programme de la Bourse de New
York. Le déploiement devait activer le nouveau code sur huit serveurs. Un
technicien n'a mis à jour que sept des huit serveurs. Le huitième a continué à
exécuter un ancien module de test, désactivé depuis des années mais jamais
supprimé du code, qui avait été réactivé accidentellement par un drapeau de
configuration (*feature flag*) réutilisé pour le nouveau module. L'ancien code,
conçu pour tester des ordres, s'est mis à acheter et vendre des actions à un
rythme frénétique, sans aucun contrôle de risque. Le temps que les ingénieurs
identifient le problème et arrêtent le système, les pertes étaient
irréversibles. Knight Capital a dû être rachetée en urgence quelques jours plus
tard. L'incident est un cas d'école en déploiement logiciel : absence de
déploiement automatisé (le processus était manuel, serveur par serveur), code
mort laissé dans la base de code, réutilisation dangereuse d'un identifiant de
configuration, et absence de mécanisme de rollback rapide. C'est exactement le
type de catastrophe que les pratiques de CI/CD (module 2) et de DevOps
(module 5) cherchent à prévenir.

{{< image src="stock-market-crash.png" alt="" title="" loading="lazy" >}}

Les accidents du Boeing 737 MAX, le vol Lion Air 610 en octobre 2018 et le vol
Ethiopian Airlines 302 en mars 2019, ont causé la mort de 346 personnes. Au
cœur des deux catastrophes se trouvait le MCAS (Maneuvering Characteristics
Augmentation System), un logiciel conçu pour corriger automatiquement l'angle de
vol de l'avion. Le 737 MAX utilisait des moteurs plus gros que les versions
précédentes du 737, montés plus en avant sur les ailes, ce qui modifiait les
caractéristiques aérodynamiques de l'appareil. Plutôt que de reconcevoir l'avion
(ce qui aurait exigé une nouvelle certification, un processus long et coûteux),
Boeing a choisi de compenser le changement par un correctif logiciel. Le MCAS
s'appuyait sur un seul capteur d'angle d'attaque, sans redondance. Quand ce
capteur transmettait des données erronées, le MCAS poussait le nez de l'avion
vers le bas de manière répétée, et les pilotes, qui n'avaient pas été informés
de l'existence du système ni formés à le désactiver, ne pouvaient pas reprendre
le contrôle. Les enquêtes ont révélé que des ingénieurs de Boeing avaient
signalé des préoccupations concernant le MCAS, mais que la pression pour livrer
l'avion à temps et maintenir les coûts de formation au minimum avait primé. La
FAA (Federal Aviation Administration), qui déléguait une part croissante de la
certification à Boeing elle-même, n'avait pas détecté le problème. Le 737 MAX
illustre un type de défaillance différent des cas précédents : ce n'est pas un
bogue caché ou une erreur de déploiement, c'est une décision organisationnelle
de traiter un problème matériel par un correctif logiciel minimal, sous pression
commerciale, en sacrifiant la redondance et la transparence.

{{< image src="plane-crash.jpg" alt="" title="" loading="lazy" >}}

## Échecs de grands projets gouvernementaux

Les catastrophes précédentes impliquaient des bogues ou des décisions techniques
spécifiques. Les échecs de grands projets gouvernementaux relèvent d'un problème
différent, plus systémique : ce sont des projets qui échouent non pas à cause
d'une ligne de code particulière, mais à cause de la manière dont ils sont
gérés, spécifiés et contractualisés. Le Canada et le Québec offrent
malheureusement plusieurs exemples récents.

Le système de paye Phénix, déployé par le gouvernement fédéral en février 2016,
devait remplacer l'ancien système de paye de la fonction publique canadienne.
Développé par IBM sur la plateforme PeopleSoft, le projet avait été estimé
initialement à 310 millions de dollars. Dès les premières semaines, des dizaines
de milliers de fonctionnaires ont été affectés : certains ne recevaient plus de
paye, d'autres recevaient des montants erronés, d'autres encore étaient trop
payés et recevaient des avis de recouvrement des mois plus tard. En 2024, huit
ans après le déploiement, le problème n'était toujours pas résolu, et le coût
total du projet (incluant les correctifs et les employés embauchés pour traiter
manuellement les dossiers) dépassait les 2,5 milliards de dollars. Les causes
identifiées par le vérificateur général du Canada sont un condensé de tout ce
qu'il ne faut pas faire : un échéancier irréaliste (la mise en service a été
devancée malgré les signaux d'alarme), l'élimination du personnel de paye
expérimenté *avant* que le nouveau système ne fonctionne, des tests insuffisants
sur des scénarios de paye réels, et un contrat structuré de manière à limiter la
responsabilité du fournisseur. C'est la loi de Brooks incarnée à grande
échelle : un projet déjà en difficulté où l'on a tenté de rattraper le retard en
ajoutant des ressources, ne faisant qu'aggraver la situation.

{{< image src="phoenix.avif" alt="" title="" loading="lazy" >}}

Au Québec, le déploiement de SAAQclic en février 2023 a reproduit plusieurs des
mêmes erreurs. Le système, développé par une alliance de SAP et de LGS (une
filiale d'IBM) pour remplacer les systèmes informatiques vieillissants de la
Société de l'assurance automobile du Québec (SAAQ), devait moderniser l'ensemble
des services : permis de conduire, immatriculation, gestion des dossiers. Le
contrat, remporté en 2017, était initialement évalué à 458 millions de dollars.
Dès sa mise en service, le système s'est révélé extrêmement lent et instable.
Les temps d'attente dans les points de service ont explosé, passant de quelques
minutes à plusieurs heures. Des citoyens se sont retrouvés dans l'impossibilité
de renouveler leur permis ou d'immatriculer un véhicule. La commission
d'enquête a révélé des problèmes à plusieurs niveaux : SAP avait participé à
l'évaluation des besoins de la SAAQ avant même de remporter le contrat, le
projet était si vaste qu'il n'y avait pas suffisamment d'informaticiens au
Québec familiers avec la plateforme SAP, et des développeurs recrutés à
l'étranger ne connaissaient pas le fonctionnement de la SAAQ. Le cas SAAQclic
illustre un pattern récurrent dans les grands projets gouvernementaux : le
remplacement complet d'un système existant en une seule opération (le *big
bang*), plutôt qu'une migration progressive. Les méthodes agiles que nous avons
vues dans le module 4 préconisent exactement l'inverse : livrer de la valeur par
petits incréments, valider chaque étape avec les utilisateurs réels, et ajuster
en cours de route. Mais les processus d'appel d'offres gouvernementaux, avec
leurs cahiers des charges détaillés et leurs contrats à prix fixe, imposent
souvent une approche waterfall qui est en tension directe avec ces principes.
Nous avions mentionné SAAQclic dans le module 1 comme exemple contemporain de la
"crise du logiciel" : le voici revisité avec les outils conceptuels que nous
avons accumulés depuis.

{{< image src="saaqclic.webp" alt="" title="" loading="lazy" >}}

Le programme de Modernisation du versement des prestations (MVP), encore en cours
au moment d'écrire ces lignes, risque de devenir le troisième grand fiasco
informatique gouvernemental canadien. Présenté comme le plus grand projet de
modernisation informatique jamais entrepris par le gouvernement fédéral, le
programme vise à remplacer les vieux systèmes utilisés pour verser les
prestations de la Sécurité de la vieillesse, de l'assurance-emploi et du Régime
de pensions du Canada. Au cœur du projet se trouve Curam, un logiciel commercial
développé à l'origine par IBM, aujourd'hui propriété de Merative. Le coût estimé
du programme est passé de 1,75 milliard de dollars en 2017 à 6,6 milliards en
2025, soit presque un quadruplement. Depuis la mise en service du nouveau
système pour la Sécurité de la vieillesse en mars 2025, des dizaines de
milliers d'aînés ont subi des retards ou des erreurs dans le versement de leurs
prestations, et les fonctionnaires qui utilisent le système lui attribuent des
notes désastreuses. Le parallèle avec Phénix est frappant : un logiciel
commercial adapté aux besoins canadiens plutôt que développé sur mesure, un
écart massif entre les coûts prévus et réels, et des utilisateurs qui subissent
les conséquences des problèmes. Une enquête de La Presse a révélé que Curam
avait causé des problèmes similaires dans d'autres pays qui l'avaient adopté, ce
qui soulève une question troublante : pourquoi répéter les mêmes erreurs quand
les signaux d'alarme sont publiquement disponibles ?

Ces trois fiascos canadiens, malgré leurs différences, partagent des patterns
troublants. Dans chaque cas, on retrouve le choix d'un logiciel commercial
générique adapté aux besoins spécifiques de l'organisation, plutôt qu'un
développement sur mesure ou une migration progressive. Dans chaque cas, les
coûts ont explosé bien au-delà des estimations initiales. Dans chaque cas, les
signaux d'alarme ont été ignorés ou minimisés par les dirigeants. Et dans chaque
cas, le processus d'approvisionnement gouvernemental, avec ses appels d'offres
rigides, ses contrats à prix fixe et ses cahiers des charges rédigés des années
avant la livraison, a imposé une approche de type waterfall à des projets dont
la complexité exigeait exactement l'inverse : des itérations courtes, du
feedback continu, et la capacité de changer de direction en cours de route.
C'est la tension entre l'agilité (module 4) et les contraintes
institutionnelles. La loi de Brooks, que nous avons rencontrée dès le module 1,
s'applique à chacun de ces projets : face aux retards, la réponse a été
d'ajouter des ressources (des consultants, des sous-traitants, des équipes à
l'étranger), ce qui n'a fait qu'accroître la complexité de coordination sans
résoudre les problèmes de fond.

## Les lois de Lehman

Les catastrophes que nous venons d'examiner ne sont pas des accidents isolés. En
1974, Meir "Manny" Lehman, un informaticien travaillant chez IBM, a formulé un
ensemble de lois sur l'évolution des logiciels, fruit de ses observations sur le
développement du système d'exploitation OS/360. Deux de ces lois sont
particulièrement éclairantes. La première, la loi du changement continu, stipule
qu'un logiciel utilisé dans le monde réel doit être continuellement adapté, sous
peine de devenir progressivement moins satisfaisant. Un logiciel n'est pas un
pont ou un bâtiment : le monde autour de lui change (les besoins des
utilisateurs évoluent, les réglementations changent, les systèmes avec lesquels
il interagit sont mis à jour), et s'il ne suit pas, il se dégrade relativement à
son environnement. La deuxième, la loi de la complexité croissante, affirme qu'à
mesure qu'un logiciel évolue, sa complexité augmente, à moins qu'un effort
délibéré ne soit fait pour la réduire. Chaque correction de bogue, chaque
fonctionnalité ajoutée, chaque adaptation à un nouveau besoin ajoute une couche
de complexité. Sans refactoring régulier (module 3), sans tests pour filet de
sécurité (module 2), sans une architecture qui gère cette complexité (module 3),
le système devient progressivement incompréhensible, fragile et coûteux à
maintenir. C'est précisément ce qui était arrivé aux vieux systèmes que Phénix,
SAAQclic et le programme MVP devaient remplacer, et c'est l'ironie de ces
projets : les nouveaux systèmes, censés résoudre le problème de la complexité
accumulée, ont eux-mêmes succombé à une complexité différente, celle de la
migration.

## Éthique et responsabilité

Les cas que nous avons examinés posent une question que le génie logiciel ne peut
pas éviter : qui est responsable quand le logiciel échoue ? Pour le Therac-25,
la réponse semble claire : le fabricant, qui n'a pas testé son logiciel
adéquatement. Pour Boeing, c'est plus complexe : les ingénieurs qui ont signalé
les problèmes ont-ils une part de responsabilité pour ne pas avoir insisté
davantage ? Les gestionnaires qui ont ignoré les alertes ? Le régulateur qui a
délégué la certification ? La question devient encore plus difficile quand on
sort des systèmes critiques pour entrer dans le domaine des algorithmes qui
prennent des décisions affectant la vie quotidienne de millions de personnes.
Des algorithmes déterminent qui obtient un prêt hypothécaire, qui est convoqué en
entrevue d'embauche, quel contenu apparaît dans votre fil d'actualité, et même,
dans certains systèmes judiciaires américains, quel score de risque de récidive
est attribué à un accusé. Quand ces algorithmes reproduisent ou amplifient des
biais présents dans les données sur lesquelles ils ont été entraînés (données
historiques qui reflètent des décennies de discrimination), la question de la
responsabilité devient profondément inconfortable. Le développeur qui a écrit le
code n'avait peut-être aucune intention discriminatoire. Les données semblaient
"objectives". Le résultat est pourtant discriminatoire.

Face à ces enjeux, la profession a tenté de se doter de cadres éthiques.
L'Association for Computing Machinery (ACM), la plus grande organisation
professionnelle en informatique, a adopté en 2018 une version révisée de son
Code of Ethics and Professional Conduct. Le code énonce des principes comme
"éviter de causer du tort", "être honnête et digne de confiance", "respecter la
vie privée", et "contribuer au bien-être de la société". Il stipule explicitement
qu'un professionnel de l'informatique devrait "évaluer si les résultats des
systèmes qu'il conçoit respectent le bien commun" et, quand un système pose un
risque, "signaler le problème aux personnes responsables". Au Québec, le génie
logiciel n'est pas une profession réglementée par un ordre professionnel au même
titre que le génie civil ou le génie mécanique. L'Ordre des ingénieurs du Québec
(OIQ) encadre les ingénieurs logiciels qui portent le titre, mais la grande
majorité des développeurs travaillent sans cette accréditation. Cette asymétrie
est frappante : un ingénieur civil qui conçoit un pont est légalement
responsable de sa sécurité, mais un développeur qui conçoit un système de santé
ou un algorithme de décision judiciaire ne l'est généralement pas au même degré.
Le débat sur la professionnalisation du génie logiciel, c'est-à-dire
l'obligation d'être membre d'un ordre pour pratiquer, revient périodiquement,
mais il se heurte à la réalité d'une industrie qui valorise l'autodidaxie et la
flexibilité.

## La crise du logiciel revisitée

Ces réflexions nous ramènent au point de départ du cours. Dans le module 1, nous
avions raconté la "crise du logiciel" telle qu'elle avait été formulée à la
conférence de l'OTAN à Garmisch en 1968 : les projets logiciels coûtaient trop
cher, prenaient trop de temps, et produisaient des systèmes défectueux. Plus
d'un demi-siècle plus tard, les exemples de cette section montrent que la crise
n'a pas été résolue. Phénix, SAAQclic, Curam : les dépassements de coûts et les
systèmes défaillants sont toujours là. Le Therac-25, Ariane 5, le 737 MAX : les
défaillances logicielles continuent de coûter des vies. Les biais algorithmiques
posent des questions éthiques que les pionniers de 1968 n'avaient pas imaginées.
Mais ce serait injuste de ne voir que les échecs. Les outils et les pratiques
que nous avons étudiés tout au long de ce cours (les tests automatisés, le
versioning, l'intégration continue, l'architecture modulaire, les méthodes
agiles, le DevOps, l'observabilité) sont autant de réponses partielles mais
réelles à cette crise permanente. Le génie logiciel n'a pas trouvé de solution
définitive, et les lois de Lehman suggèrent qu'il n'en trouvera probablement
jamais. Mais il a développé un ensemble de pratiques, d'outils et de principes
qui permettent de construire des systèmes d'une complexité que les participants à
Garmisch n'auraient pas cru possible. La responsabilité de les appliquer, et de
le faire avec discernement éthique, revient à chaque développeur.
