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

Le sprint est l'unité de temps fondamentale de Scrum : une période fixe,
généralement de deux semaines, pendant laquelle l'équipe s'engage à livrer un
incrément fonctionnel du produit. Chaque sprint commence par une séance de
planification (*sprint planning*) où l'équipe sélectionne des éléments du
product backlog et définit un objectif pour le sprint. Pendant le sprint,
l'équipe tient une courte réunion quotidienne (*daily standup*) d'environ quinze
minutes, souvent debout, où chaque membre répond à trois questions : qu'est-ce
que j'ai fait hier, qu'est-ce que je fais aujourd'hui, est-ce que quelque chose
me bloque? À la fin du sprint, deux événements se succèdent : la *sprint
review*, où l'équipe présente ce qui a été accompli aux parties prenantes et
recueille leurs commentaires, et la *rétrospective*, où l'équipe réfléchit à son
propre fonctionnement et identifie des améliorations pour le prochain sprint.

Avant de passer à un exemple concret, il faut clarifier une confusion
fréquente. Quand on pense à Scrum (ou à l'agilité en général), on visualise
souvent un tableau avec des colonnes ("À faire", "En cours", "Terminé") et des
cartes qu'on déplace de gauche à droite. Ce tableau est un outil de
visualisation qu'on appelle un *tableau Kanban*. Mais Kanban est aussi le nom
d'une méthode de gestion à part entière, que nous verrons dans la
[prochaine section]({{< relref "/docs/module4/20-agile/20-kanban" >}}). Le tableau
et la méthode ne sont pas la même chose. Le tableau Kanban est un outil
générique que pratiquement toutes les équipes utilisent, quelle que soit leur
méthode. Dans la pratique, une équipe Scrum organise typiquement son sprint
autour d'un tel tableau, et c'est exactement ce que nous allons faire dans la
démonstration qui suit.

## Démonstration avec GitHub Projects

Pour illustrer concrètement comment Scrum fonctionne au quotidien, nous allons
suivre une petite équipe à travers son premier sprint. Nous retrouvons Leila et
Sara, que nous avons rencontrées dans la
[section sur GitHub]({{< relref "/docs/module4/10-github" >}}). Elles travaillent
maintenant au sein d'une équipe de quatre personnes qui développe *RéservaSalle*,
une application web permettant de réserver des salles dans un espace de
coworking. Leila joue le rôle de Product Owner : c'est elle qui a la vision du
produit et qui décide des priorités. Sara et Marco sont développeurs. Nadia est
Scrum Master : elle facilite le processus et s'assure que l'équipe n'est pas
bloquée. Pour mettre en place et suivre leur sprint, l'équipe utilise GitHub
Projects, l'outil de gestion de projet intégré à GitHub.

### Mise en place du projet

La première étape est de créer un projet GitHub Projects, en sélectionnant le
template *Board* depuis l'onglet *Projects* du profil ou de l'organisation. Le
projet est nommé « RéservaSalle ».

GitHub Projects offre trois types de vues pour visualiser le contenu d'un
projet, chacune adaptée à un usage différent. La vue *Table* présente les
éléments sous forme de tableau, semblable à un tableur : chaque ligne est une
tâche, chaque colonne un champ (titre, statut, assigné, etc.). C'est la vue la
plus pratique pour éditer rapidement les propriétés de plusieurs tâches à la
fois. La vue *Board* organise les tâches en colonnes, chaque colonne
correspondant à une valeur d'un champ donné (typiquement le statut). C'est le
tableau Kanban dont nous avons parlé plus haut : on y visualise le flux de
travail et on déplace les cartes de gauche à droite au fil de leur progression.
Enfin, la vue *Roadmap* affiche les tâches sur un axe temporel, ce qui est utile
pour visualiser la planification à plus long terme. Un même projet peut avoir
plusieurs vues, et on peut passer de l'une à l'autre sans perdre d'information :
ce sont simplement des façons différentes de regarder les mêmes données. Pour
notre démonstration, nous allons principalement utiliser la vue *Board*, qui est
la plus naturelle pour suivre un sprint Scrum au quotidien.

<!-- ILLUSTRATION: les trois types de vues côte à côte ou en séquence -->

Lorsqu'on crée un projet avec le template *Board*, le tableau contient par
défaut trois colonnes : *Todo* (le travail qui reste à faire), *In Progress* (ce
sur quoi quelqu'un travaille en ce moment) et *Done* (ce qui est terminé). Ces
colonnes correspondent aux valeurs d'un champ appelé *Status* : déplacer une
carte d'une colonne à une autre revient à changer la valeur de ce champ. On peut
ajouter, renommer ou réordonner ces colonnes en modifiant les valeurs du champ
Status dans les paramètres du projet.

<!-- ILLUSTRATION: tableau GitHub Projects vide avec les 3 colonnes par défaut -->

Pour notre projet, on ajoute une quatrième colonne : *In Review*, insérée entre
*In Progress* et *Done*. Cette colonne représente le moment où un développeur a
terminé son travail et ouvert une pull request qui attend la revue d'un
coéquipier. C'est un ajout simple, mais il reflète un aspect fondamental du
travail en équipe : le code ne passe pas directement de « en cours » à
« terminé ». Il transite par une étape de validation par les pairs, celle-là
même que nous avons vue dans la
[section sur GitHub]({{< relref "/docs/module4/10-github" >}}).

<!-- ILLUSTRATION: tableau avec les 4 colonnes : Todo, In Progress, In Review, Done -->

En plus du statut, GitHub Projects permet d'ajouter des champs personnalisés à
chaque tâche. Les champs sont typés : on peut créer des champs de texte, de
nombre, de date, de sélection unique, et quelques types spécialisés. Deux champs
supplémentaires seront essentiels pour le sprint.

Le premier est un champ numérique nommé *Story Points*. Les story points sont
une unité d'estimation utilisée par beaucoup d'équipes Scrum pour évaluer
l'effort relatif que représente chaque tâche. L'idée n'est pas de mesurer le
temps en heures ou en jours, mais de comparer les tâches entre elles : si
l'équipe estime qu'une tâche vaut 2 points et qu'une autre en vaut 5, elle
exprime que la seconde est environ deux fois et demie plus complexe que la
première. Les valeurs utilisées suivent généralement la suite de Fibonacci (1, 2,
3, 5, 8, 13...), ce qui force l'équipe à faire des choix tranchés plutôt que de
se perdre dans des distinctions trop fines entre des tâches de taille similaire.
Il faut noter que les story points ne font pas partie du Scrum Guide officiel :
c'est une pratique complémentaire qui s'y est greffée au fil du temps, et
certaines équipes expérimentées préfèrent des approches plus simples, comme
découper le travail en tâches de taille à peu près équivalente et simplement les
compter. Mais le concept reste largement répandu et les étudiants le
rencontreront presque certainement en milieu professionnel.

Le second champ est de type *Iteration*. Une itération dans GitHub Projects
correspond exactement à un sprint : c'est une période de temps fixe (ici
configurée à deux semaines) à laquelle on associe des tâches. Ce champ permettra
de filtrer le tableau pour ne voir que les tâches du sprint en cours, et plus
tard de comparer la charge de travail d'un sprint à l'autre.

<!-- ILLUSTRATION: paramètres du projet montrant les champs ajoutés (Story Points et Iteration) -->

### Le product backlog

Le product backlog est la liste ordonnée de tout ce qui pourrait être développé
dans le produit. C'est le Product Owner qui en est responsable : c'est lui qui
décide quels éléments y figurent et dans quel ordre de priorité. Dans GitHub,
chaque élément du backlog prend naturellement la forme d'une *issue* dans le
dépôt du projet.

Les éléments du backlog sont souvent formulés sous forme de *user stories*. Le
format classique est : « En tant que [rôle], je veux [action] afin de
[bénéfice] ». À première vue, cette formulation peut sembler inutilement
verbeuse. Pourquoi ne pas simplement écrire « Page d'affichage des salles » et
passer à autre chose ?

La réponse tient dans ce que le format force à expliciter. La partie « en tant
que » oblige à identifier *qui* a besoin de la fonctionnalité. Ce n'est pas
toujours évident : dans un système comme RéservaSalle, les utilisateurs qui
réservent des salles, les administrateurs qui les gèrent et les développeurs qui
maintiennent le code ont des besoins différents. Un titre comme « Gérer les
salles » est ambigu : est-ce pour l'utilisateur qui cherche une salle, ou pour
l'administrateur qui en ajoute une nouvelle ? La partie « afin de » force à
énoncer le *pourquoi*, ce qui est souvent la partie la plus révélatrice. Si
l'équipe n'arrive pas à formuler le bénéfice d'une fonctionnalité, c'est
peut-être que cette fonctionnalité n'est pas nécessaire, ou qu'elle est mal
comprise. Le format agit comme un filtre : il pousse l'équipe à se demander si
chaque élément du backlog apporte réellement de la valeur, et à qui.

Cette pratique s'inscrit dans un changement de perspective plus large apporté par
l'agilité. Dans les approches traditionnelles, les exigences étaient souvent
formulées du point de vue du système (« le système doit permettre de... »). La
user story renverse cette perspective en partant de l'humain qui utilise le
logiciel. C'est un choix délibéré, pas juste une convention stylistique.

Pour RéservaSalle, le backlog initial contient les issues suivantes :

| # | Titre | User story |
|---|-------|-----------|
| 1 | Modèle de données | En tant que développeur, je veux un modèle de données pour les salles et les réservations afin de pouvoir stocker les informations du système |
| 2 | API liste des salles | En tant qu'utilisateur, je veux voir les salles disponibles afin de choisir celle qui me convient |
| 3 | Page d'affichage des salles | En tant qu'utilisateur, je veux une page qui affiche les salles afin de naviguer visuellement dans l'offre |
| 4 | API de réservation | En tant qu'utilisateur, je veux pouvoir réserver une salle afin de garantir ma place |
| 5 | Authentification | En tant qu'utilisateur, je veux m'authentifier afin que mes réservations soient associées à mon compte |
| 6 | CI avec GitHub Actions | En tant que développeur, je veux un pipeline de CI afin que les tests soient exécutés automatiquement à chaque push |

On remarque que certaines issues sont des fonctionnalités destinées aux
utilisateurs finaux (2, 3, 4, 5) tandis que d'autres sont des tâches techniques
qui n'apportent pas de valeur directe à l'utilisateur mais sont nécessaires au
bon fonctionnement du projet (1, 6). Dans un projet mature, le backlog
contiendrait aussi des rapports de bugs et des tâches de maintenance
(refactoring, mise à jour de dépendances, etc.). On peut distinguer ces types à
l'aide de *labels* GitHub, par exemple `story`, `tech`, `bug`.

Créer six issues via l'interface web est un processus répétitif. C'est
l'occasion d'introduire `gh`, l'outil en ligne de commande officiel de GitHub.
Il ne faut pas confondre `gh` et `git` : `git` est l'outil de versioning que
nous avons vu dans le
[module 2]({{< relref "/docs/module2/30-versioning" >}}), il gère les commits,
les branches et l'historique d'un dépôt. `gh`, lui, interagit avec GitHub en
tant que plateforme : il permet de créer des issues, ouvrir des pull requests,
gérer des projets, consulter les résultats de CI, bref, d'effectuer depuis le
terminal la plupart des opérations qu'on ferait normalement dans le navigateur.
Les deux outils sont complémentaires : on utilise `git` pour travailler sur son
code, et `gh` pour interagir avec les services de GitHub autour de ce code.

Pour ceux qui souhaitent reproduire les manipulations de cette démonstration,
voici comment créer les issues du backlog d'un seul coup :

```shell
gh issue create -R cjauvin/reservasalle \
  --title "Modèle de données pour les salles et réservations" \
  --body "En tant que développeur, je veux un modèle de données pour les salles et les réservations afin de pouvoir stocker les informations du système" \
  --label tech
gh issue create -R cjauvin/reservasalle \
  --title "API pour lister les salles disponibles" \
  --body "En tant qu'utilisateur, je veux voir les salles disponibles afin de choisir celle qui me convient" \
  --label story
gh issue create -R cjauvin/reservasalle \
  --title "Page d'affichage des salles" \
  --body "En tant qu'utilisateur, je veux une page qui affiche les salles afin de naviguer visuellement dans l'offre" \
  --label story
gh issue create -R cjauvin/reservasalle \
  --title "API de réservation d'une salle" \
  --body "En tant qu'utilisateur, je veux pouvoir réserver une salle afin de garantir ma place" \
  --label story
gh issue create -R cjauvin/reservasalle \
  --title "Authentification des utilisateurs" \
  --body "En tant qu'utilisateur, je veux m'authentifier afin que mes réservations soient associées à mon compte" \
  --label story
gh issue create -R cjauvin/reservasalle \
  --title "CI avec GitHub Actions" \
  --body "En tant que développeur, je veux un pipeline de CI afin que les tests soient exécutés automatiquement à chaque push" \
  --label tech
```

Une fois les issues créées et ajoutées au projet, elles apparaissent dans la vue
par défaut du projet, qui est de type *Table*. Cette vue tabulaire correspond
exactement au product backlog : c'est la liste de toutes les tâches du projet,
avec leurs propriétés (statut, story points, itération, labels, etc.) affichées
en colonnes. C'est dans cette vue qu'on peut le plus facilement trier le backlog
par priorité, modifier les champs de plusieurs issues à la fois, ou avoir une
vue d'ensemble de tout ce qui reste à faire. En basculant vers la vue *Board*,
on retrouve ces mêmes issues organisées visuellement par statut. Pour l'instant,
elles se trouvent toutes dans la colonne *Todo*.

<!-- ILLUSTRATION: vue Table montrant les 6 issues avec leurs champs, puis vue Board avec les mêmes issues dans Todo -->

### Les cérémonies du sprint

Scrum structure le travail autour d'un ensemble de réunions qu'on appelle les
*cérémonies* (le Scrum Guide utilise le terme *événements*). Ce ne sont pas des
réunions au sens bureaucratique : chacune a un objectif précis, une durée
limitée, et un résultat attendu. Il y en a quatre : le *sprint planning* lance
le sprint en définissant ce que l'équipe va accomplir. Le *daily standup*
synchronise l'équipe chaque matin. La *sprint review* présente le travail
accompli aux parties prenantes. La *rétrospective* permet à l'équipe de
réfléchir à son propre fonctionnement. Ces quatre cérémonies forment un cycle
qui se répète à chaque sprint, et c'est ce cycle régulier qui donne son rythme
au projet. Voyons-les en action à travers notre premier sprint.

### Le sprint planning

Le sprint planning est la réunion qui lance chaque sprint. C'est le moment où
l'équipe décide collectivement de ce qu'elle s'engage à livrer pendant les deux
prochaines semaines. La réunion se déroule en trois temps : le Product Owner
présente les éléments les plus prioritaires du backlog, l'équipe les estime en
story points, puis elle sélectionne ceux qu'elle pense pouvoir compléter pendant
le sprint.

Pour l'estimation, l'équipe de RéservaSalle passe en revue chaque issue du
backlog. La discussion est souvent plus révélatrice que le chiffre lui-même :
c'est en débattant de la complexité d'une tâche qu'on découvre des ambiguïtés,
des dépendances cachées ou des risques techniques que personne n'avait anticipés.
Après discussion, l'équipe attribue les story points suivants :

| # | Titre | Story Points |
|---|-------|:------------:|
| 1 | Modèle de données | 3 |
| 2 | API liste des salles | 3 |
| 3 | Page d'affichage des salles | 5 |
| 4 | API de réservation | 5 |
| 5 | Authentification | 8 |
| 6 | CI avec GitHub Actions | 2 |

Le total du backlog est de 26 points. Comme c'est le premier sprint, l'équipe
n'a pas encore de vélocité de référence (c'est-à-dire le nombre de points
qu'elle est capable de compléter en un sprint). Elle doit donc faire une
estimation prudente. Avec deux développeurs sur deux semaines, l'équipe décide de
prendre les issues #1, #2, #3 et #6, pour un total de 13 points. L'issue #1
(modèle de données) est un prérequis pour les deux APIs, et l'issue #6 (CI) est
une tâche d'infrastructure qu'il vaut mieux mettre en place tôt. L'issue #3
(page d'affichage) dépend de l'API #2, mais l'équipe estime que les deux peuvent
avancer en parallèle si le contrat d'API est défini à l'avance.

Leila, en tant que Product Owner, propose un objectif de sprint : « À la fin du
sprint, un utilisateur peut voir la liste des salles disponibles dans le
navigateur, et le pipeline de CI valide automatiquement chaque push. » L'objectif
de sprint n'est pas une liste de tâches, c'est une phrase qui décrit le résultat
attendu en termes de valeur. Il donne une direction à l'équipe et permet de
trancher les décisions en cours de sprint : si une tâche ne contribue pas à
l'objectif, elle peut probablement attendre.

Dans GitHub Projects, les issues sélectionnées pour le sprint sont associées à
l'itération « Sprint 1 » via le champ *Iteration*. On peut ensuite filtrer la
vue Board pour n'afficher que les issues du sprint en cours, ce qui donne un
tableau épuré qui reflète exactement le travail en cours.

<!-- ILLUSTRATION: vue Board filtrée sur Sprint 1, avec les 4 issues sélectionnées dans la colonne Todo -->

### Le déroulement du sprint

Le sprint est lancé. Chaque matin, l'équipe se réunit brièvement pour le *daily
standup* : chaque membre dit ce qu'il a fait la veille, ce qu'il compte faire
aujourd'hui, et s'il est bloqué par quelque chose. Cette réunion dure environ
quinze minutes et se fait souvent debout, justement pour décourager les
discussions qui s'éternisent. L'objectif n'est pas de rendre des comptes, mais
de synchroniser l'équipe et de détecter les problèmes rapidement. Si Marco
mentionne qu'il est bloqué en attendant une décision sur le schéma de la base de
données, c'est à Nadia, en tant que Scrum Master, de s'assurer que l'obstacle
est levé dans la journée.

Suivons le parcours d'une issue à travers le tableau pour comprendre le flux de
travail concret. Sara prend l'issue #1 (modèle de données) et se l'assigne dans
GitHub. Elle déplace la carte de *Todo* vers *In Progress*. Comme nous l'avons
vu dans la [section sur GitHub]({{< relref "/docs/module4/10-github" >}}), elle
crée une branche dédiée à cette issue, y fait ses commits, puis ouvre une pull
request lorsque son travail est prêt. À ce moment, elle déplace la carte vers
*In Review* : le code est écrit, mais il attend la relecture d'un coéquipier.
Marco fait la revue, laisse quelques commentaires, Sara apporte les corrections,
et Marco approuve la PR. Une fois la pull request fusionnée, la carte passe dans
*Done*.

<!-- ILLUSTRATION: séquence montrant une carte qui traverse les 4 colonnes, avec en parallèle le flux Git (branche → PR → review → merge) -->

Ce va-et-vient entre le tableau et Git n'est pas une coïncidence : les deux
outils reflètent le même processus vu sous des angles différents. Le tableau
montre *où en est* chaque tâche dans le flux de travail. Git et les pull
requests montrent *comment* le travail est réalisé techniquement. GitHub Projects
permet d'ailleurs d'automatiser une partie de ce lien : on peut configurer le
projet pour qu'une issue soit automatiquement déplacée vers *In Review* lorsqu'une
pull request liée est ouverte, et vers *Done* lorsque la PR est fusionnée. Dans
la pratique, ce genre d'automatisation réduit le travail manuel et garantit que
le tableau reste à jour, même quand l'équipe oublie de déplacer ses cartes.

Pendant ce temps, le tableau évolue jour après jour. Voici à quoi il pourrait
ressembler en milieu de sprint :

<!-- ILLUSTRATION: tableau en milieu de sprint, par exemple : Todo (#3), In Progress (#2 assignée à Marco, #6 assignée à Sara), In Review (#1), Done (vide) -->

Vers la fin de la deuxième semaine, l'équipe a complété les issues #1, #2 et #6.
L'issue #3 (page d'affichage des salles) est en cours de revue. Le tableau final
du sprint ressemble à ceci :

<!-- ILLUSTRATION: tableau en fin de sprint : Todo (vide), In Progress (vide), In Review (#3), Done (#1, #2, #6) -->

### La fin du sprint

Le sprint se termine par deux événements distincts : la *sprint review* et la
*rétrospective*.

La sprint review est tournée vers le produit. L'équipe présente ce qui a été
accompli pendant le sprint aux parties prenantes (dans le cas de RéservaSalle,
ce pourrait être le responsable de l'espace de coworking, ou d'autres collègues
intéressés par le projet). L'important est de montrer un logiciel fonctionnel,
pas des diapositives : l'équipe fait une démonstration en direct du modèle de
données en place, de l'API qui retourne la liste des salles, et du pipeline de
CI qui exécute les tests automatiquement. L'issue #3 (page d'affichage) n'est
pas encore terminée, elle est toujours en revue. C'est normal : Scrum n'exige
pas que tout soit complété, mais que l'équipe soit transparente sur ce qui l'est
et ce qui ne l'est pas. L'issue #3 sera reportée au sprint suivant. Les parties
prenantes peuvent aussi profiter de cette réunion pour donner du feedback qui
influencera les priorités du prochain sprint : peut-être que la fonctionnalité de
réservation (#4) est plus urgente que prévu, ou qu'une nouvelle idée a émergé.

La vélocité de ce premier sprint est de 8 points (les issues #1, #2 et #6, à
3 + 3 + 2 points). Ce chiffre servira de référence pour le prochain sprint
planning : l'équipe sait maintenant qu'elle peut raisonnablement s'engager sur
environ 8 points de travail par sprint. Au fil des sprints, cette vélocité se
stabilisera et deviendra un outil de planification de plus en plus fiable.

La rétrospective, elle, est tournée vers l'équipe et son fonctionnement. Ce
n'est pas une réunion sur le code ou les fonctionnalités, c'est une réunion sur
la manière de travailler ensemble. Chaque membre est invité à répondre à trois
questions : qu'est-ce qui a bien fonctionné ? Qu'est-ce qui pourrait être
amélioré ? Quelles actions concrètes l'équipe s'engage-t-elle à prendre pour le
prochain sprint ? Par exemple, l'équipe pourrait constater que les revues de code
ont pris plus de temps que prévu parce que les PR étaient trop volumineuses, et
décider de faire des PR plus petites et plus fréquentes au prochain sprint. Ou
que le daily standup avait tendance à dépasser les quinze minutes, et convenir
d'un format plus strict. La rétrospective est le mécanisme par lequel Scrum
s'améliore de sprint en sprint : sans elle, l'équipe répète les mêmes erreurs
indéfiniment.

Ce premier sprint illustre un principe fondamental de Scrum : le processus
s'auto-calibre au fil du temps. Au départ, l'équipe ne savait pas combien de
travail elle pouvait accomplir en deux semaines. Elle a fait une estimation
prudente, a livré 8 points, et dispose maintenant d'une donnée concrète pour
planifier le sprint suivant. Si au sprint 2 elle complète 11 points, puis 10 au
sprint 3, sa vélocité moyenne se stabilise et les prédictions deviennent de plus
en plus fiables. Le même mécanisme opère pour la qualité du travail d'équipe :
chaque rétrospective identifie un ou deux ajustements concrets, qui sont mis en
pratique au sprint suivant, puis réévalués à la rétrospective d'après. Scrum ne
demande pas de tout faire parfaitement dès le départ. Il demande de boucler le
cycle, d'observer ce qui s'est passé, et d'ajuster. C'est cette boucle de
rétroaction courte et régulière qui fait sa force, bien plus que n'importe quel
artefact ou cérémonie pris isolément.