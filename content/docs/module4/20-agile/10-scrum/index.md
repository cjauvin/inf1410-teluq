---
title: "Scrum"
slug: "scrum"
weight: 10
---

# La méthode Scrum

En 1986, les professeurs Hirotaka Takeuchi et Ikujiro Nonaka publient dans la
*Harvard Business Review* un article intitulé "The New New Product Development
Game". Leur sujet n'est pas le logiciel : ils étudient comment des entreprises
japonaises comme Honda, Canon et Fuji-Xerox parviennent à développer de nouveaux
produits plus rapidement que leurs concurrents. Leur constat est que les équipes
les plus performantes ne suivent pas un processus séquentiel où chaque phase est
complétée avant de passer à la suivante (ce qu'ils comparent à une course à
relais). Elles fonctionnent plutôt comme une mêlée de rugby (*scrum*) : l'équipe
avance ensemble, en bloc, en se passant le ballon d'avant en arrière tout en
progressant sur le terrain. L'analogie peut sembler anecdotique, mais elle
capture une idée profonde : le développement de produits complexes n'est pas un
processus linéaire qu'on peut planifier de bout en bout, c'est un effort
collectif, adaptatif, où les phases se chevauchent et où l'équipe s'auto-organise.

{{< image src="rugby-scrum.jpg" alt="" title="" loading="lazy" >}}

C'est dans les années 1990 que Jeff Sutherland et Ken Schwaber s'emparent de ces
idées et les transposent au développement logiciel. Sutherland, qui travaille
alors chez Easel Corporation, s'inspire directement de l'article de Takeuchi et
Nonaka pour organiser son équipe en sprints courts avec des réunions
quotidiennes. Schwaber, consultant en gestion de projet, formalise l'approche et
la présente à la conférence OOPSLA en 1995. Ensemble, ils publient le *Scrum
Guide*, un document volontairement court (une vingtaine de pages) qui définit les
rôles, les événements et les artefacts de la méthode. Ce guide a été révisé
plusieurs fois depuis, mais son esprit reste le même : fournir un cadre léger
pour gérer la complexité, pas une recette rigide à suivre à la lettre.

## Les rôles

Scrum définit trois rôles. Le *Product Owner* est responsable de déterminer
*quoi* construire : il maintient une liste ordonnée de fonctionnalités à
développer (le *product backlog*) et s'assure que l'équipe travaille toujours
sur ce qui a le plus de valeur. Le *Scrum Master* ne gère pas l'équipe au sens
traditionnel : son rôle est de faciliter le processus, de lever les obstacles
qui bloquent l'équipe, et de s'assurer que les règles de Scrum sont comprises et
respectées. Enfin, l'*équipe de développement* (typiquement entre trois et neuf
personnes) est auto-organisée : c'est elle qui décide *comment* réaliser le
travail. Il n'y a pas de chef d'équipe, pas de répartition des tâches par un
gestionnaire. Cette distinction entre le *quoi* (Product Owner) et le *comment*
(équipe) est au cœur de la philosophie Scrum.

Il est notable que Scrum ne définit que trois rôles, et que l'équipe de
développement est explicitement décrite comme *cross-fonctionnelle* : elle
contient toutes les compétences nécessaires pour livrer le produit, sans
distinction de titre entre ses membres. C'est un contraste marqué avec
l'organisation traditionnelle des équipes logicielles, qui distinguait des rôles
spécialisés : développeurs, testeurs, analystes, architectes. Le rôle de testeur
QA (*quality assurance*), en particulier, était l'un des plus courants. Dans le
modèle classique, une équipe QA distincte recevait le logiciel une fois le
développement terminé et le soumettait à des plans de test manuels, souvent
exhaustifs, avant de le déclarer prêt pour la mise en production. Ce modèle
avait sa logique dans un contexte waterfall, où les livraisons étaient espacées
de plusieurs mois. Mais dans un contexte agile, où l'équipe livre toutes les
deux semaines, une phase de test séparée devient un goulot d'étranglement. C'est
pourquoi Scrum intègre la responsabilité de la qualité à l'intérieur de l'équipe
elle-même : chaque membre est responsable de la qualité de ce qu'il livre, et
les tests automatisés (que nous avons vus au
[module 2]({{< relref "/docs/module2/20-tests" >}})) remplacent en grande partie
l'inspection manuelle. Le rôle de testeur QA n'a pas disparu pour autant, mais
il s'est transformé : dans beaucoup d'équipes modernes, les spécialistes QA se
concentrent sur les tests exploratoires (chercher les cas limites que les tests
automatisés ne couvrent pas), sur la qualité de l'expérience utilisateur, ou sur
l'automatisation des tests elle-même.

Cette structure d'équipe n'est pas anodine. Rappelons la loi de Conway, que nous
avons introduite dans l'[introduction de ce module]({{< relref "/docs/module4" >}}) :
la structure d'une organisation tend à se refléter dans l'architecture de ses
logiciels. Une équipe Scrum de quatre ou cinq personnes, travaillant ensemble sur
un même produit, va naturellement produire un système relativement intégré. Si
l'équipe comprend un développeur frontend et un développeur backend, le système
aura vraisemblablement une séparation frontend/backend. Si on divise le travail
entre deux équipes distinctes, une pour les réservations et une pour
l'authentification, on obtiendra deux sous-systèmes avec une API entre eux. Ce
n'est ni bien ni mal en soi, mais il faut en être conscient : quand on décide de
la composition d'une équipe, on prend implicitement une décision architecturale.

## Le sprint et les cérémonies

Le sprint est l'unité de temps fondamentale de Scrum&nbsp;: une période fixe,
généralement de deux semaines, pendant laquelle l'équipe s'engage à livrer un
incrément fonctionnel du produit. Scrum structure le déroulement de chaque
sprint autour de quatre réunions qu'on appelle les *cérémonies* (le Scrum Guide
utilise le terme *événements*). Ce ne sont pas des réunions au sens
bureaucratique&nbsp;: chacune a un objectif précis, une durée limitée, et un
résultat attendu. Le sprint commence par le *sprint planning*, où l'équipe
sélectionne des éléments du product backlog et définit un objectif. Pendant le
sprint, le *daily standup* synchronise l'équipe chaque matin en quinze
minutes&nbsp;: chaque membre dit ce qu'il a fait la veille, ce qu'il fait
aujourd'hui, et s'il est bloqué. Le sprint se termine par deux
cérémonies&nbsp;: la *sprint review*, où l'équipe présente ce qui a été accompli
aux parties prenantes, et la *rétrospective*, où elle réfléchit à son propre
fonctionnement et identifie des améliorations pour le prochain sprint.

{{< image src="sprint.jpg" alt="" title="" loading="lazy" >}}

## Démonstration avec GitHub Projects

Pour illustrer concrètement comment Scrum fonctionne au quotidien, nous allons
suivre une petite équipe à travers son premier sprint. Nous retrouvons Leila et
Sara, que nous avons rencontrées dans la
[section sur GitHub]({{< relref "/docs/module4/10-github" >}}). Elles travaillent
maintenant au sein d'une équipe de quatre personnes qui développe *RéservaSalle*,
une application web permettant de réserver des salles dans un espace de
coworking. Leila joue le rôle de Product Owner&nbsp;: c'est elle qui a la vision
du produit et qui décide des priorités. Sara et Marco sont développeurs. Nadia
est Scrum Master&nbsp;: elle facilite le processus et s'assure que l'équipe n'est
pas bloquée. Pour mettre en place et suivre leur sprint, l'équipe utilise GitHub
Projects, l'outil de gestion de projet intégré à GitHub.

### Mise en place du projet

La première étape est de créer un projet GitHub Projects depuis l'onglet
*Projects* du profil ou de l'organisation. Le projet est nommé « RéservaSalle ».
Par défaut, GitHub Projects affiche les éléments du projet sous forme de **vue
Table**&nbsp;: chaque ligne est une tâche, chaque colonne un champ (titre,
statut, responsable, etc.). C'est la vue la plus simple, et aussi la plus
naturelle pour commencer&nbsp;: on est en train de construire un backlog,
c'est-à-dire une liste ordonnée de travail à faire, et un tableau ressemble
exactement à ça.

{{< image src="project-create.png" alt="" title="" loading="lazy" >}}

Les éléments qui peuplent ce tableau ne sont pas des objets propres à GitHub
Projects&nbsp;: ce sont des **issues** GitHub, c'est-à-dire les mêmes issues que
nous avons vues dans la
[section sur GitHub]({{< relref "/docs/module4/10-github" >}}). C'est un choix de
conception important&nbsp;: le backlog n'est pas une liste séparée du reste du
projet, il est ancré directement dans le dépôt. Une issue peut représenter une
fonctionnalité à développer, un bug à corriger, ou une tâche technique. On peut
créer une issue directement depuis la vue Table, ou depuis l'onglet *Issues* du
dépôt, et l'ajouter ensuite au projet.

### Le product backlog (tableau des issues / stories)

Les éléments du backlog sont souvent formulés sous forme de *user stories*. Le
format classique est&nbsp;: « En tant que [rôle], je veux [action] afin de
[bénéfice] ». Cette formulation peut sembler inutilement verbeuse à première vue,
mais elle force à répondre à trois questions que les équipes oublient
souvent&nbsp;: *qui* a besoin de cette fonctionnalité, *quoi* exactement, et
*pourquoi*. Un titre comme « Gérer les salles » est ambigu, car il ne précise pas
si c'est pour l'utilisateur qui cherche une salle ou pour l'administrateur qui en
ajoute une nouvelle. Le format user story dissipe cette ambiguïté. Et si l'équipe
n'arrive pas à formuler le « afin de », c'est souvent le signe que la
fonctionnalité est mal comprise ou inutile.

Pour RéservaSalle, le backlog initial contient six issues. Quatre sont des
fonctionnalités destinées aux utilisateurs finaux, deux sont des tâches techniques
sans valeur directe pour l'utilisateur mais nécessaires au bon fonctionnement du
projet. On distingue ces types à l'aide de *labels* GitHub&nbsp;: `story` pour
les user stories, `tech` pour les tâches techniques.

| # | Titre | User story |
|---|-------|-----------|
| 1 | Modèle de données | En tant que développeur, je veux un modèle de données pour les salles et les réservations afin de pouvoir stocker les informations du système |
| 2 | API liste des salles | En tant qu'utilisateur, je veux voir les salles disponibles afin de choisir celle qui me convient |
| 3 | Page d'affichage des salles | En tant qu'utilisateur, je veux une page qui affiche les salles afin de naviguer visuellement dans l'offre |
| 4 | API de réservation | En tant qu'utilisateur, je veux pouvoir réserver une salle afin de garantir ma place |
| 5 | Authentification | En tant qu'utilisateur, je veux m'authentifier afin que mes réservations soient associées à mon compte |
| 6 | CI avec GitHub Actions | En tant que développeur, je veux un pipeline de CI afin que les tests soient exécutés automatiquement à chaque push |

Créer six issues via l'interface web est un processus répétitif. C'est l'occasion
d'introduire `gh`, l'outil en ligne de commande officiel de GitHub. Il ne faut
pas confondre `gh` et `git`&nbsp;: `git` gère les commits, les branches et
l'historique local, tandis que `gh` interagit avec GitHub en tant que
plateforme — créer des issues, ouvrir des pull requests, gérer des projets. Les
deux sont complémentaires.

```shell
$ gh issue create -R cjauvin/reservasalle \
  --title "Modèle de données pour les salles et réservations" \
  --body "En tant que développeur, je veux un modèle de données pour les salles et les réservations afin de pouvoir stocker les informations du système" \
  --label tech
$ gh issue create -R cjauvin/reservasalle \
  --title "API pour lister les salles disponibles" \
  --body "En tant qu'utilisateur, je veux voir les salles disponibles afin de choisir celle qui me convient" \
  --label story
$ gh issue create -R cjauvin/reservasalle \
  --title "Page d'affichage des salles" \
  --body "En tant qu'utilisateur, je veux une page qui affiche les salles afin de naviguer visuellement dans l'offre" \
  --label story
$ gh issue create -R cjauvin/reservasalle \
  --title "API de réservation d'une salle" \
  --body "En tant qu'utilisateur, je veux pouvoir réserver une salle afin de garantir ma place" \
  --label story
$ gh issue create -R cjauvin/reservasalle \
  --title "Authentification des utilisateurs" \
  --body "En tant qu'utilisateur, je veux m'authentifier afin que mes réservations soient associées à mon compte" \
  --label story
$ gh issue create -R cjauvin/reservasalle \
  --title "CI avec GitHub Actions" \
  --body "En tant que développeur, je veux un pipeline de CI afin que les tests soient exécutés automatiquement à chaque push" \
  --label tech
```

{{< image src="table-view-with-issues.png" alt="" title="" loading="lazy" >}}

Une fois les issues créées, elles apparaissent dans la vue Table. C'est aussi le
moment d'enrichir le projet avec deux champs supplémentaires. GitHub Projects
permet d'ajouter des champs personnalisés typés&nbsp;: texte, nombre, date,
sélection, et quelques types spécialisés. Le premier est un champ numérique nommé
*Story Points*. Les story points sont une unité d'estimation utilisée par
beaucoup d'équipes Scrum pour évaluer l'effort relatif de chaque tâche. L'idée
n'est pas de mesurer le temps en heures, mais de comparer les tâches entre
elles&nbsp;: si une tâche vaut 2 points et une autre en vaut 5, la seconde est
environ deux fois et demie plus complexe. Les valeurs suivent généralement la
suite de Fibonacci (1, 2, 3, 5, 8, 13...), ce qui force des choix tranchés
plutôt que des distinctions trop fines. Il faut noter que les story points ne
font pas partie du Scrum Guide officiel&nbsp;: c'est une pratique complémentaire
largement répandue, mais certaines équipes préfèrent simplement découper le
travail en tâches de taille équivalente et les compter.

Le second champ est de type *Iteration*. Une itération dans GitHub Projects
correspond exactement à un sprint&nbsp;: c'est une période de temps fixe, ici
configurée à deux semaines, à laquelle on associe des tâches. Ce champ a deux
utilités concrètes&nbsp;: filtrer la vue pour ne voir que les tâches du sprint en
cours, et comparer la charge de travail d'un sprint à l'autre au fil du temps.
Une fois les deux champs ajoutés, la vue Table du backlog affiche maintenant plusieurs
colonnes&nbsp;: titre, statut (nous verrons cela plus loin), responsable (le programmeur qui sera attitré à la tâche), story points et itération, ainsi que d'autres colonnes possibles, dont nous ne parlerons pas.

### La première cérémonie : le sprint planning

Le sprint planning est la première cérémonie du sprint. C'est le moment où
l'équipe décide collectivement de ce qu'elle s'engage à livrer pendant les deux
prochaines semaines. La cérémonie se déroule en trois temps&nbsp;: le Product
Owner présente les éléments les plus prioritaires du backlog, l'équipe les estime
en story points, puis elle sélectionne ceux qu'elle pense pouvoir compléter
pendant le sprint. La discussion autour de l'estimation est souvent plus
révélatrice que le chiffre lui-même&nbsp;: c'est en débattant de la complexité
d'une tâche qu'on découvre des ambiguïtés, des dépendances cachées ou des risques
techniques que personne n'avait anticipés.

Pour RéservaSalle, l'équipe passe en revue chaque issue et remplit le champ
*Story Points* directement dans la vue Table. Après discussion, voici les
estimations retenues&nbsp;:

| # | Titre | Story Points |
|---|-------|:------------:|
| 1 | Modèle de données | 3 |
| 2 | API liste des salles | 3 |
| 3 | Page d'affichage des salles | 5 |
| 4 | API de réservation | 5 |
| 5 | Authentification | 8 |
| 6 | CI avec GitHub Actions | 2 |

Le total du backlog est de 26 points. Comme c'est le premier sprint, l'équipe
n'a pas encore de vélocité de référence&nbsp;: elle ne sait pas encore combien de
points elle est capable de compléter en deux semaines. Elle doit donc faire une
estimation prudente. Avec deux développeurs, elle choisit les issues #1, #2, #3
et #6, pour un total de 13 points. L'issue #1 (modèle de données) est un
prérequis pour les deux APIs. L'issue #6 (CI) est une tâche d'infrastructure
qu'il vaut mieux mettre en place tôt. L'issue #3 (page d'affichage) dépend de
l'API #2, mais les deux peuvent avancer en parallèle si le contrat d'API est
défini à l'avance.

Leila, en tant que Product Owner, formule un objectif de sprint&nbsp;: « À la
fin du sprint, un utilisateur peut voir la liste des salles disponibles dans le
navigateur, et le pipeline de CI valide automatiquement chaque push. » L'objectif
de sprint n'est pas une liste de tâches&nbsp;: c'est une phrase qui décrit le
résultat attendu en termes de valeur. Il donne une direction à l'équipe et permet
de trancher les décisions en cours de sprint&nbsp;: si une tâche ne contribue pas
à cet objectif, elle peut probablement attendre.

Dans la vue Table, les quatre issues sélectionnées reçoivent la valeur
« Itération 1 » dans le champ *Iteration* (notez qu'il faut tout d'abord créer l'itération, dans l'interface appropriée). C'est aussi le bon moment pour basculer
vers la **vue Board** (on peut créer une nouvelle vue de type "board", si elle n'existe pas). Maintenant que le sprint est planifié et que les tâches
sont assignées, on veut suivre leur progression à travers les étapes du
travail&nbsp;: c'est exactement ce pour quoi cette vue est conçue. En basculant
vers le Board, on retrouve les quatre issues du sprint dans la colonne *Todo*,
prêtes à être travaillées.

{{< image src="selected-issues-iter1.png" alt="" title="" loading="lazy" >}}

{{% hint warning %}}

Avant de commencer à déplacer des cartes, il faut clarifier une confusion
fréquente. Cette vue Board est ce qu'on appelle un *tableau Kanban*&nbsp;: un
tableau avec des colonnes représentant les étapes du travail, et des cartes
qu'on déplace de gauche à droite au fil de leur progression. Mais Kanban est
aussi le nom d'une méthode de gestion à part entière, que nous verrons dans la
[prochaine section]({{< relref "/docs/module4/20-agile/20-kanban" >}}). Le tableau
et la méthode ne sont pas la même chose&nbsp;: le tableau Kanban est un outil
générique que pratiquement toutes les équipes utilisent, quelle que soit leur
méthode.

{{% /hint %}}

Le tableau par défaut a trois colonnes, mais le flux de travail réel de l'équipe
en comporte quatre. Une tâche terminée ne passe pas directement de « en cours »
à « terminé »&nbsp;: elle transite d'abord par une étape de revue de code, celle
que nous avons vue dans la
[section sur GitHub]({{< relref "/docs/module4/10-github" >}}). On ajoute donc
une colonne *In Review* entre *In Progress* et *Done*, en ajoutant simplement
une valeur au champ *Status* dans les paramètres du projet. Ensuite, la vue
board doit être filtrée en fonction du critère `itération:"itération 1"`, afin
de ne laisser apparaître que nos 4 issues du sprint courant. Notez qu'une vue
peut être sauvegardée, afin d'être plus facilement réutilisée et partagée.

{{< image src="board-view.png" alt="" title="" loading="lazy" >}}

### Le déroulement du sprint

Le sprint est lancé. Chaque matin, l'équipe se réunit pour le *daily standup*,
la deuxième cérémonie&nbsp;: chaque membre dit ce qu'il a fait la veille, ce
qu'il compte faire aujourd'hui, et s'il est bloqué par quelque chose. Cette
cérémonie dure environ quinze minutes, souvent debout pour décourager les
discussions qui s'éternisent. L'objectif n'est pas de rendre des comptes, mais
de synchroniser l'équipe et de détecter les problèmes rapidement. Si Marco
mentionne qu'il attend une décision sur le schéma de la base de données, c'est à
Nadia, en tant que Scrum Master, de s'assurer que l'obstacle est levé dans la
journée.

{{% hint warning %}}

Dans les faits, il est très difficile de faire en sorte que la cérémonie
du daily standup soit correctement effectuée, et qu'elle reste utile, au fil
du temps. Jour après jour, elle a tendance à évoluer vers des conversations
répétitives et vides, qui sont de moins en moins utiles. Le fait d'insister
pour la garder courte est donc une bonne stratégie, en général.

{{% /hint %}}

Suivons le parcours de l'issue #1 (modèle de données) à travers le tableau. Sara
se l'assigne et déplace la carte de *Todo* vers *In Progress*. Elle crée une
branche dédiée, y fait ses commits, puis ouvre une pull request lorsque son
travail est prêt. La carte passe alors dans *In Review*&nbsp;: le code est écrit,
mais il attend la relecture de Marco. Marco laisse des commentaires, Sara apporte
les corrections, Marco approuve la PR. Une fois la pull request fusionnée, la
carte passe dans *Done*. Ce va-et-vient entre le tableau et Git n'est pas une
coïncidence&nbsp;: les deux outils reflètent le même processus vu sous des angles
différents. Le tableau montre *où en est* chaque tâche dans le flux de
travail&nbsp;; Git et les pull requests montrent *comment* le travail est réalisé
techniquement. GitHub Projects permet d'ailleurs d'automatiser une partie de ce
lien&nbsp;: on peut configurer le projet pour qu'une issue se déplace
automatiquement vers *In Review* lorsqu'une pull request liée est ouverte, et
vers *Done* lorsque la PR est fusionnée.

Pendant ce temps, le reste du sprint avance en parallèle. Voici à quoi pourrait
ressembler le tableau vers le milieu de la deuxième semaine&nbsp;:

{{< image src="sprint-mid.png" alt="" title="" loading="lazy" >}}

Vers la fin du sprint, l'équipe a complété les issues #1, #2 et #6. L'issue #3
(page d'affichage des salles) est en cours de revue. Le tableau final du sprint
ressemble à ceci&nbsp;:

{{< image src="sprint-fin.png" alt="" title="" loading="lazy" >}}

### La fin du sprint

Le sprint se termine par deux cérémonies distinctes&nbsp;: la *sprint review* et
la *rétrospective*.

La sprint review est tournée vers le produit. L'équipe présente ce qui a été
accompli aux parties prenantes — dans le cas de RéservaSalle, le responsable de
l'espace de coworking. L'important est de montrer un logiciel fonctionnel, pas
des diapositives&nbsp;: l'équipe fait une démonstration en direct du modèle de
données en place, de l'API qui retourne la liste des salles, et du pipeline de CI
qui exécute les tests automatiquement. L'issue #3 (page d'affichage) n'est pas
encore terminée, elle est toujours en revue. Ce n'est pas un échec, c'est une
information&nbsp;: Scrum n'exige pas que tout soit complété, mais que l'équipe
soit transparente sur ce qui l'est et ce qui ne l'est pas. L'issue #3 sera
reportée au sprint suivant. Les parties prenantes peuvent aussi profiter de cette
réunion pour donner du feedback qui influencera les priorités du prochain sprint.

La rétrospective, elle, est tournée vers l'équipe plutôt que vers le produit. Ce
n'est pas une réunion sur le code ou les fonctionnalités, c'est une cérémonie
sur la manière de travailler ensemble. Chaque membre répond à trois
questions&nbsp;: qu'est-ce qui a bien fonctionné ? Qu'est-ce qui pourrait être
amélioré ? Quelles actions concrètes l'équipe s'engage-t-elle à prendre pour le
prochain sprint ? Par exemple, l'équipe pourrait constater que les revues de code
ont pris plus de temps que prévu parce que les PR étaient trop volumineuses, et
décider d'en faire des plus petites au prochain sprint. La rétrospective est le
mécanisme par lequel Scrum s'améliore de sprint en sprint&nbsp;: sans elle,
l'équipe répète les mêmes erreurs indéfiniment.

La vélocité de ce premier sprint est de 8 points (les issues #1, #2 et #6, à
3 + 3 + 2 points). Il reste 18 points au backlog&nbsp;: l'issue #3 reportée du
sprint 1 (5 points), plus les issues #4 (5 points) et #5 (8 points). C'est ici
que la **vue Roadmap** devient utile. Elle affiche les itérations sur un axe
temporel, ce qui permet de visualiser d'un coup d'oeil comment le travail
restant pourrait se répartir sur les prochains sprints. On peut esquisser que le
Sprint 2 contiendra les issues #3 et #4 (10 points), et le Sprint 3 l'issue #5
(8 points). Ce n'est pas une prédiction ferme&nbsp;: la vélocité va se raffiner
au fil des sprints, mais c'est une première approximation utile pour communiquer
une direction aux parties prenantes.

<!-- ILLUSTRATION: vue Roadmap avec Sprint 1 terminé, Sprint 2 et Sprint 3 esquissés sur la timeline -->

Ce premier sprint illustre un principe fondamental de Scrum&nbsp;: le processus
s'auto-calibre au fil du temps. Au départ, l'équipe ne savait pas combien de
travail elle pouvait accomplir en deux semaines. Elle a fait une estimation
prudente, a livré 8 points, et dispose maintenant d'une donnée concrète pour
planifier le sprint suivant. Le même mécanisme opère pour la qualité du travail
d'équipe&nbsp;: chaque rétrospective identifie un ou deux ajustements concrets,
mis en pratique au sprint suivant, puis réévalués à la rétrospective d'après.
Scrum ne demande pas de tout faire parfaitement dès le départ. Il demande de
boucler le cycle, d'observer ce qui s'est passé, et d'ajuster. C'est cette
boucle de rétroaction courte et régulière qui fait sa force, bien plus que
n'importe quel artefact ou cérémonie pris isolément.