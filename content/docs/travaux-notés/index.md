---
title: "Travaux notés"
weight: 20
---

# Les travaux notés

## Le projet fil rouge

Ce cours est structuré autour d'un projet de développement logiciel unique, que vous ferez évoluer d'un bout à l'autre de la session. L'idée est simple : plutôt que de produire des travaux déconnectés les uns des autres, vous allez construire quelque chose de concret, en appliquant progressivement les outils et les pratiques vus dans chaque module. Ce projet est donc à la fois un fil conducteur pédagogique et une occasion de vivre, de l'intérieur, les défis réels du génie logiciel moderne. Il n'est pas attendu de vous que vous maîtrisiez ou utilisiez la totalité des techniques et des outils abordés dans le cours — l'objectif est plutôt que vous fassiez des choix éclairés, et que vous soyez capables de les justifier.

{{< image src="ligne-rouge.png" alt="" title="" loading="lazy" >}}

Avant d'entrer dans le détail, une chose mérite d'être dite d'emblée. Cette page est longue parce qu'elle est précise, et une bonne part de ce qu'elle décrit concerne la façon dont votre travail sera évalué. Mais l'évaluation n'est pas le sujet du projet, elle en est la conséquence. Ce qui est réellement attendu de vous, c'est que vous construisiez quelque chose qui vous intéresse, en assumant des choix que vous serez capables de défendre.

Voici, en un coup d'oeil, la structure de la session. Chaque étape est détaillée dans la [section sur les jalons](#les-jalons).

| Étape | Quand | Poids |
|---|---|---|
| Jalon 1, Fondations | après le module 2 | 10&nbsp;% |
| Jalon 2, Architecture et données | après le module 3 | 15&nbsp;% |
| Entretien mi-parcours | dans les deux semaines suivant le jalon 2 | 10&nbsp;% |
| Jalon 3, Développement | après le module 4 | 15&nbsp;% |
| Jalon 4, Livraison finale | après le module 6 | 25&nbsp;% |
| Entretien final | dans les deux semaines suivant le jalon 4 | 25&nbsp;% |

## Le projet

Vous devrez concevoir et développer une application web de nature transactionnelle, comme un service de réservation, une plateforme communautaire, un outil de gestion, ou tout autre concept qui implique des utilisateurs, des données et des interactions. Votre application devra obligatoirement comporter un mécanisme d'authentification et de création d'usagers, ainsi qu'une base de données relationnelle (SQL) pour la gestion des données. Elle devra également être déployée et accessible en ligne pour les correcteurs, sans qu'ils aient à installer quoi que ce soit sur leur poste.

Le choix du langage et des technologies est entièrement libre. Python, JavaScript, Go, Ruby, Java, Rust — tout est acceptable, sans aucune restriction. De la même façon, le choix du framework web, de l'outil de déploiement ou de la base de données vous appartient complètement. Ce qui compte, c'est la qualité de votre démarche et la pertinence de vos choix, pas la technologie utilisée pour les mettre en oeuvre.

L'intégration d'une API tierce, comme Stripe pour le traitement de paiements, Twilio pour les notifications, ou toute autre API pertinente à votre domaine, n'est pas obligatoire. De façon générale, les choix techniques ambitieux sont activement encouragés dans ce cours. Un projet qui tente quelque chose de difficile, qui explore des territoires moins familiers, sera toujours évalué avec plus d'intérêt qu'un projet techniquement correct mais sans ambition. Le degré de complexité supplémentaire que vous vous imposez est en soi un critère positif.

Dans le même esprit, la **conteneurisation** est une avenue particulièrement intéressante. Empaqueter votre application et sa base de données dans des conteneurs [Docker]({{< relref "module5/10-infrastructure/10-docker/index.md" >}}), orchestrés localement par `docker compose`, règle d'un coup le vieux problème du « ça marche sur ma machine » et rend votre déploiement reproductible d'un environnement à l'autre. Pour les plus ambitieux, [Kubernetes]({{< relref "module5/10-infrastructure/20-kubernetes/index.md" >}}) ouvre la porte à l'orchestration à plus grande échelle, et un tableau de bord Grafana branché sur votre application vous donnerait une [observabilité]({{< relref "module5/30-observabilite/index.md" >}}) que peu de projets étudiants atteignent. Rien de tout cela n'est exigé, et ces sujets ne sont abordés qu'au module 5, donc après le jalon 3. Mais si vous vous y aventurez, ce sera remarqué.

## En équipe ou en solo

Vous pouvez travailler seul ou en équipe de deux ou trois personnes. Les deux options sont équivalentes sur le plan des exigences techniques de base&nbsp;: qualité du code, tests automatisés, intégration continue, ADRs, déploiement et blogue technique sont attendus dans les deux cas.

{{< image src="team-vs-solo.webp" alt="" title="" loading="lazy" >}}

La principale différence porte sur la gestion de projet. Le travail en équipe implique une dimension organisationnelle que le travail solo n'a pas, notamment l'attribution des tâches, la coordination et le suivi des priorités. Pour refléter cet effort, l'utilisation de **GitHub Projects** (tableau de bord, suivi des issues, progression visible) est **requise pour les équipes**. Elle est **optionnelle pour les personnes travaillant seules**. Là où les jalons mentionnent GitHub Projects, la mention *(équipe)* indique que ce livrable ne s'applique qu'aux équipes.

Une équipe est par ailleurs attendue sur un projet **proportionnellement plus ambitieux**. À deux ou trois, la capacité de travail est plus grande, et l'évaluation en tient compte. Un projet d'équipe qui ressemble à ce qu'une personne seule aurait pu livrer sera jugé en deçà des attentes. L'ambition dont il est question plus haut, dans la section sur le projet, se mesure donc à l'aune de la taille de l'équipe.

Il vous revient aussi de vous assurer que le travail est **raisonnablement distribué** entre les membres. Deux approches fonctionnent bien. Vous pouvez attribuer des **rôles fixes**, chacun devenant responsable d'un domaine comme la base de données, l'interface ou le pipeline de déploiement, ce qui donne de la profondeur mais crée des angles morts. Vous pouvez aussi **faire alterner les rôles** d'un jalon à l'autre, ce qui exige plus de coordination mais garantit que chacun touche à tout. Dans les deux cas, la répartition doit rester visible dans l'historique du dépôt et dans le tableau GitHub Projects, et un déséquilibre marqué se remarquera.

La coordination de l'équipe se fera dans **un canal Discord privé**, créé pour vous sur le [serveur du cours]({{< relref "discord.md" >}}), et auquel j'aurai accès. C'est là que devraient vivre vos échanges de travail, vos décisions et vos arbitrages, plutôt que dans une conversation privée dont il ne resterait aucune trace.

Autant le dire franchement, **c'est une expérience**. Cette façon de faire n'a jamais été tentée dans ce cours, et je ne sais pas encore ce qu'elle donnera. Elle rend visible une dimension du travail d'équipe qui reste d'ordinaire invisible de l'extérieur, la coordination elle-même, qui est pourtant l'endroit où une bonne partie du génie logiciel se joue. Nous découvrirons ensemble ce que ça donne, et c'est une des choses que j'attends avec le plus de curiosité cette session.

## Le dépôt GitHub

**Chaque étudiant doit avoir son propre compte GitHub**, y compris au sein d'une équipe. C'est la condition pour que les contributions soient attribuables individuellement, ce sur quoi repose une bonne partie de l'évaluation. Un compte partagé, ou un seul membre qui pousse le travail de tous, rend cette lecture impossible et sera pénalisé.

Le dépôt GitHub de votre projet est le lieu central où vit votre travail. Tous les livrables qui ne sont pas du code — ADRs, schémas de données, documentation — doivent être rédigés en texte brut (Markdown de préférence) ou en PDF.

{{% hint warning %}}

**Attention&nbsp;: aucun document au format MS Office (Word, Excel, PowerPoint) ne sera accepté**, dans tous les contextes.

{{% /hint %}}

{{< image src="office-interdit.webp" alt="Les logos de Word, Excel et PowerPoint barrés d'un cercle d'interdiction rouge" title="Aucun document en format MS Office" loading="lazy" >}}

{{% hint info %}}

Votre dépôt peut être public ou privé, selon votre préférence. S'il est privé, vous devrez inviter le professeur en tant que collaborateur&nbsp;: son compte GitHub est [cjauvin](https://github.com/cjauvin).

{{% /hint %}}

## La remise officielle

Les projets de ce cours sont volontairement hétéroclites. Chacun choisit son langage, son hébergement et sa plateforme de blogue, et son dépôt peut être public ou privé. Il n'existe donc aucun endroit unique où le correcteur saurait d'avance aller regarder.

C'est pourquoi **chaque jalon doit être accompagné d'un court document déposé dans le système officiel de remise des travaux de la TÉLUQ**. Ce document ne contient pas le travail lui-même, il dit comment y accéder&nbsp;: l'adresse du dépôt GitHub, celle du blogue, celle de l'application déployée le cas échéant, celle du tableau GitHub Projects, et les liens vers les transcriptions publiées. Un lien par ressource, avec une ligne qui dit ce qu'on y trouve.

C'est ce dépôt officiel qui fait foi de la remise et qui en fixe la date. Votre travail vit sur GitHub et sur le web, mais c'est ce document qui y donne accès, et un jalon dont les ressources ne sont pas atteignables ne peut pas être évalué.

## Le serveur Discord

Le cours dispose d'un [serveur Discord]({{< relref "discord.md" >}}) accessible à tous les étudiants inscrits. Son usage est facultatif pour qui travaille seul, et requis pour les équipes, qui y coordonnent leur travail. Il fait partie intégrante du concept du cours&nbsp;: il est pensé comme le hub central de communication, aussi bien pour la coordination au sein des équipes que pour toute question ou discussion en lien avec le cours. Chaque équipe y disposera de son propre canal privé, mais le serveur comporte aussi des canaux ouverts à tous, pour poser une question technique, partager une ressource, ou simplement échanger avec d'autres étudiants qui travaillent sur les mêmes problèmes que vous.

Par expérience, le sentiment de communauté qui se développe sur ce genre de plateforme est l'un des aspects les plus bénéfiques de la session. Les cours en ligne peuvent être isolants&nbsp;; Discord brise cette isolation de façon naturelle, et rend l'expérience d'apprentissage plus riche et plus humaine. Les sessions où les étudiants s'y investissent sont presque toujours plus vivantes et plus intéressantes pour tout le monde, y compris pour le professeur.

## Le blogue technique de développement

Le blogue technique est le fil narratif de votre projet. Il ne s'agit pas d'un rapport de fin de session, mais d'un document vivant que vous alimentez tout au long de la session, au fur et à mesure que vous prenez des décisions, rencontrez des difficultés et faites évoluer votre application. Chaque entrée doit être datée et rédigée de façon contemporaine au développement, et non rétrospectivement.

Le blogue peut prendre la forme qui vous convient&nbsp;: un site hébergé (GitHub Pages, Notion, etc.), un wiki dans le dépôt, ou un dossier de fichiers Markdown. Pour les plus aventureux, [Hugo](https://gohugo.io), le générateur de sites statiques avec lequel ce cours a lui-même été construit, est un excellent choix pour héberger un blogue technique sur GitHub Pages. L'essentiel est que le blogue soit accessible publiquement et qu'il raconte une progression réelle dans le temps.

Les questions posées dans chaque jalon servent de point de départ, pas de plafond. Les entrées peuvent être aussi nombreuses et détaillées que vous le jugez utile. Dans la culture du développement logiciel, le blogue technique est depuis longtemps un outil de réflexion autant que de communication&nbsp;: beaucoup de développeurs écrivent pour clarifier leur propre pensée, pour fixer ce qu'ils viennent d'apprendre, ou pour forcer l'articulation d'une idée encore floue. C'est exactement cet usage qui est valorisé ici. Quelques exemples de blogues techniques qui incarnent cet esprit, et qui valent la peine d'être lus pour leur style autant que pour leur contenu&nbsp;:

- [Joel on Software](https://www.joelonsoftware.com) de Joel Spolsky, l'un des blogues de développement les plus influents jamais écrits
- [Les essais](https://paulgraham.com/articles.html) de Paul Graham, cofondateur de Y Combinator, sur la programmation, les startups et la pensée
- [Le site de Martin Fowler](https://martinfowler.com), référence incontournable sur l'architecture et les pratiques de développement
- [Julia Evans](https://jvns.ca), qui illustre parfaitement l'idée d'écrire pour apprendre et rendre les concepts techniques accessibles

Ce qui distingue un bon blogue d'un rapport générique, c'est la spécificité. Écrire « nous avons choisi PostgreSQL » n'apporte rien. Écrire « lors de la modélisation du panier, on a réalisé que notre schéma initial ne supportait pas les items avec des variantes, ce qui nous a forcés à restructurer la relation entre `orders` et `products` »&nbsp;: voilà ce qui démontre une réflexion authentique. Pour vous guider dans cette direction, chaque jalon précise les questions auxquelles votre entrée de blogue devra répondre.

## L'intelligence artificielle dans ce cours

L'usage de l'IA est non seulement permis dans ce cours, il est activement encouragé. Savoir formuler de bonnes questions, évaluer les réponses et intégrer les suggestions de l'IA de manière critique fait partie des compétences que tout développeur doit maîtriser aujourd'hui. Ignorer ces outils dans un cours de génie logiciel moderne serait à contre-courant de la réalité du métier.

Cette ouverture crée cependant un défi d'évaluation réel. Si un outil peut produire du code fonctionnel, des [ADRs]({{< relref "module4/30-gestion-projet/index.md" >}}) convaincants et des réflexions de blogue plausibles, comment distinguer un apprentissage authentique d'une délégation totale ? Ce cours s'attaque à ce problème par trois mécanismes complémentaires.

### L'entretien de suivi

Ces rencontres visent à évaluer la cohérence entre le niveau de sophistication que vos travaux affichent et la profondeur de votre compréhension réelle, telle qu'elle se manifeste dans une conversation en tête à tête avec le professeur. Un écart important entre les deux est, en soi, un signal d'évaluation. L'idée n'est pas d'exiger une mémorisation parfaite de chaque détail, mais de vérifier que vous maîtrisez ce que vous avez produit. Pour quelqu'un qui a réellement travaillé sur le projet, cela devrait aller de soi. Dans certains cas, l'entretien pourra inclure un court exercice pratique sans assistance, à l'image de ce qu'un cours de programmation pourrait faire avec un exercice de code sur tableau blanc. Ce cours n'étant pas un cours de programmation à proprement parler, l'exercice serait adapté en conséquence&nbsp;: une question de conception architecturale, un problème de modélisation de données, ou toute autre tâche en lien direct avec le contenu de votre projet.

{{% hint warning %}}

🚨🚨🚨 **Attention : assurez-vous de ne pas prendre à la légère les entretiens de suivi de ce cours.** Tout le reste de ce que vous remettez, le code, les ADRs, les entrées de blogue, peut avoir été produit avec une assistance dont l'ampleur reste impossible à mesurer de l'extérieur. L'entretien est le seul mécanisme sur lequel le professeur peut se fier entièrement, parce qu'il met en présence votre compréhension elle-même, sans intermédiaire. Il pèse donc bien plus lourd que sa pondération ne le laisse croire. **La réussite du cours est conditionnelle à celle des deux entretiens.** Des explications insuffisantes, ou un doute raisonnable qui s'installe sans se dissiper, peuvent mener à un échec, quelle que soit la qualité apparente des livrables.

{{% /hint %}}

### La trace du temps

Le problème central avec une délégation excessive à l'IA, c'est qu'elle permet de produire en quelques heures ce qui devrait résulter de semaines de travail itératif. Pour contrer cela, l'évaluation porte non seulement sur ce que vous avez produit, mais sur quand vous l'avez produit.

La plateforme GitHub se prête naturellement à cet exercice. Les [commits]({{< relref "module2/30-versioning/index.md" >}}), les issues, les [pull requests]({{< relref "module4/10-github/index.md" >}}) et les entrées de blogue hébergés en ligne comportent tous des horodatages enregistrés par les serveurs de GitHub au moment de leur réception. Contrairement aux métadonnées d'un dépôt git local, qui peuvent techniquement être modifiées, ces traces en ligne sont plus difficiles à altérer rétrospectivement. Le graphe d'activité, l'historique des contributions et la chronologie des issues constituent ainsi un journal de bord de votre progression que le correcteur peut consulter avec confiance.

Un projet dont tous les commits arrivent dans les 48 heures précédant une remise, ou dont les entrées de blogue semblent avoir été rédigées en rafale en une seule soirée, ne ressemble pas à un projet qui a évolué pendant plusieurs semaines. Cette différence est visible, et elle est prise en compte dans l'évaluation. L'objectif n'est pas de surveiller chaque geste, mais de vous encourager à travailler de façon régulière et à documenter votre réflexion au moment où elle se produit, ce qui est, au passage, la meilleure façon d'apprendre durablement.

### Montrer plutôt que raconter

Sur le plan de l'évaluation, une règle simple s'applique&nbsp;: plus vous avez utilisé l'IA, plus les attentes seront élevées quant à la façon dont vous en parlez dans votre blogue technique. Écrire « j'ai utilisé l'IA pour générer du code » est insuffisant. Ce qui est attendu, c'est un regard réflexif et, idéalement, original&nbsp;: comment avez-vous affiné votre façon d'interagir avec ces outils au fil du projet ? Où vous ont-ils surpris, déçu, ou conduit à repenser votre approche ? Avez-vous découvert des usages inattendus, ou développé des techniques d'expérimentation qui vous sont propres ? L'IA est un territoire suffisamment nouveau pour que vos observations personnelles aient de la valeur, et c'est cette curiosité exploratoire qui sera valorisée.

Sur ce point, une conviction guide l'évaluation. Un texte qui décrit votre façon de travailler avec l'IA est une reconstruction, écrite après coup, et la mémoire lisse naturellement les hésitations, les fausses pistes et les moments d'incompréhension. Or c'est exactement là que se trouve la matière intéressante. Une transcription de session montre la chose telle qu'elle s'est produite&nbsp;: les questions que vous avez réellement posées, les réponses que vous avez écartées, l'endroit où vous avez repris la main parce que la proposition ne tenait pas.

C'est pourquoi votre blogue devra s'appuyer sur des transcriptions publiées, et pas seulement sur votre récit. L'outil [claude-code-transcripts](https://github.com/simonw/claude-code-transcripts), de Simon Willison, transforme une session Claude Code en pages HTML autonomes et lisibles sur téléphone, qu'on peut déposer dans un gist GitHub et référencer depuis une entrée de blogue.

```shell
uvx claude-code-transcripts local
```

Si vous travaillez avec un autre outil, à vous d'en trouver l'équivalent, qu'il s'agisse d'un lien de partage de conversation ou d'un export. Ce qui compte n'est pas l'outil, mais le principe de rendre la trace consultable.

Il ne s'agit surtout pas de tout publier. Une session complète est longue, et un dépôt qui les accumulerait toutes serait illisible. Choisissez-en quelques-unes qui disent quelque chose&nbsp;: celle où vous avez enfin compris un mécanisme, celle où l'IA vous a conduit dans un mur que vous avez mis du temps à voir, celle où la conversation a changé une décision d'architecture. Votre entrée de blogue commente et renvoie, elle ne paraphrase pas.

{{% hint warning %}}

**Attention&nbsp;: relisez une transcription avant de la publier.** Une session de développement traverse vos fichiers, et il n'est pas rare qu'elle contienne une clé d'API, le contenu d'un `.env`, un mot de passe de base de données, ou des chemins qui en disent long sur votre machine. Une fois dans un gist public, c'est public.

{{% /hint %}}

## La philosophie du flux continu

Les jalons qui structurent ce cours sont une nécessité organisationnelle, pas un modèle de travail. La philosophie qui devrait guider votre progression tout au long de la session est plutôt celle du [CI/CD]({{< relref "module2/50-ci/index.md" >}})&nbsp;: un flux de travail et d'apprentissage le plus continu et régulier possible, où chaque avancée est intégrée, testée et documentée au moment où elle se produit, plutôt qu'accumulée en rafale à l'approche d'une échéance.

En pratique, cela signifie committer régulièrement, alimenter le blogue technique au fil des décisions, et traiter chaque jalon non pas comme une échéance à atteindre, mais comme un point de contrôle dans un développement qui n'a jamais vraiment cessé d'avancer. Les jalons décrivent ce que vous devrez avoir produit à un moment donné&nbsp;; la philosophie du flux continu décrit comment vous devriez y arriver.

## Les jalons

Le projet est évalué à travers quatre jalons et deux entretiens de suivi, répartis sur la session, pour un total de 100&nbsp;%. Le tableau du début de page en donne la vue d'ensemble. Chacun donne lieu à une [remise officielle](#la-remise-officielle) à la TÉLUQ, sous la forme décrite plus haut.

### Jalon 1 — Fondations (10%)

*À remettre après le module 2*

Ce premier jalon pose les bases de votre projet. Vous devrez avoir clarifié la nature de votre application et établi les fondations techniques et organisationnelles du développement.

Livrables&nbsp;:
- Un dépôt GitHub contenant un `README.md` avec la **vision client** : qui est l'utilisateur, quel problème l'application résout, et quelle est la solution envisagée (environ une page, rédigée du point de vue de l'utilisateur)
- Un ensemble de **[user stories]({{< relref "module4/20-agile/10-scrum/index.md" >}})** sous forme de [GitHub Issues]({{< relref "module4/10-github/index.md" >}}), traduisant cette vision en tâches concrètes (avec des labels appropriés)
- *(équipe)* Un tableau **[GitHub Projects]({{< relref "module4/20-agile/10-scrum/index.md" >}})** initialisé avec ces issues en backlog
- Un fichier `.github/workflows/ci.yml` configurant une [pipeline CI]({{< relref "module2/50-ci/index.md" >}}) qui exécute automatiquement la suite de tests à chaque push
- Un ensemble de **[tests automatisés]({{< relref "module2/20-tests/index.md" >}})** couvrant les fonctionnalités déjà implantées
- Une première entrée dans votre **blogue technique**, répondant aux questions suivantes&nbsp;: qui sont vos utilisateurs et quel problème résolvez-vous ? Quels sont vos premiers choix techniques (langage, [framework]({{< relref "module3/30-interfaces/30-frameworks/index.md" >}}), hébergement) et quelles alternatives avez-vous considérées ? Qu'est-ce qui est encore incertain à ce stade ?

{{% hint warning %}}

**Attention&nbsp;: le projet doit être approuvé au jalon 1 pour que la session puisse se poursuivre.** Si la vision proposée n'est pas assez ambitieuse, si son ampleur est mal calibrée dans un sens ou dans l'autre, ou si elle se prête mal aux exigences techniques du cours, il faudra la retravailler et la resoumettre jusqu'à ce qu'elle soit jugée satisfaisante. Ce n'est pas une formalité administrative. Tous les jalons suivants s'appuient sur ces fondations, et un projet mal cadré au départ devient très coûteux à corriger une fois le développement engagé. Une itération de plus au début de la session vaut mieux qu'une impasse à la fin.

{{% /hint %}}

### Jalon 2 — Architecture et données (15%)

*À remettre après le module 3*

Ce jalon marque le passage d'un prototype initial à une application mieux structurée. Vous devrez avoir réfléchi à l'[architecture]({{< relref "module3/10-architecture/index.md" >}}) de votre système et formalisé votre modèle de données.

Livrables&nbsp;:
- Deux ou trois **[ADRs]({{< relref "module4/30-gestion-projet/index.md" >}})** documentant vos choix architecturaux importants : framework, organisation du code, [type de base de données]({{< relref "module3/40-données/20-stockage/index.md" >}}), etc. Ils sont hébergés dans le dépôt, par exemple dans un dossier `docs/adr/`
- Un **[schéma de données]({{< relref "module3/40-données/10-représentation/index.md" >}})** commenté décrivant vos tables, leurs champs et leurs relations, dans le dépôt
- *(équipe)* Une mise à jour du **tableau GitHub Projects** reflétant l'évolution du travail depuis le jalon 1
- Une entrée dans votre **blogue**, répondant aux questions suivantes&nbsp;: quelle décision architecturale importante avez-vous prise, quel était son contexte, et quelles alternatives avez-vous rejetées et pourquoi ? Quel obstacle concret avez-vous rencontré et comment l'avez-vous résolu ? Qu'est-ce que votre schéma de données révèle de votre compréhension du domaine ?

### Entretien mi-parcours (10%)

*Rendez-vous à prendre par vous-même, dans les deux semaines suivant la réception de votre note du jalon 2*

Il vous revient de fixer cette rencontre, une fois votre note reçue, en passant par le lien de réservation de la [page du professeur]({{< relref "professeur/index.md" >}}). Aucune convocation ne vous sera envoyée.

Cet entretien est une rencontre individuelle (ou par équipe) de 15 à 20 minutes sur Microsoft Teams. La conversation porte sur ce que vous avez produit jusqu'ici : vos choix techniques, votre schéma de données, le fonctionnement de votre pipeline CI. L'objectif n'est pas de vous piéger, mais de vérifier que vous comprenez et maîtrisez ce que reflète votre dépôt, et d'identifier les points à consolider pour la suite de la session.

### Jalon 3 — Développement (15%)

*À remettre après le module 4*

Ce jalon met l'accent sur l'évolution du projet et la rigueur des pratiques de développement. L'évaluation porte sur la démonstration que les artéfacts du projet ont évolué de manière significative et structurée depuis le jalon 2.

Livrables&nbsp;:
- *(équipe)* Un **tableau GitHub Projects** ayant évolué de manière visible : issues fermées, nouvelles issues ouvertes, progression observable dans le temps
- Un **[historique git]({{< relref "module2/30-versioning/index.md" >}})** non trivial : branches nommées de manière significative, [pull requests]({{< relref "module4/10-github/index.md" >}}) avec description, commits qui racontent une progression cohérente dans le temps
- De nouveaux **ADRs** documentant les décisions prises depuis le jalon 2
- Au moins deux **[transcriptions de session](#montrer-plutôt-que-raconter)** publiées, choisies parce qu'elles montrent quelque chose, et liées depuis l'entrée de blogue
- S'il y a lieu, une **activité de débogage** documentée&nbsp;: un bogue réel rencontré pendant le développement, la manière dont vous l'avez localisé, par exemple avec un point d'arrêt, le panneau des variables et la pile d'appels de l'éditeur, comme dans la section sur [le débogage]({{< relref "module2/25-debogage/index.md" >}}), et ce que vous avez compris en le trouvant. Un billet de blogue ou une transcription de session convient, avec des captures d'écran de préférence. Un bogue bien raconté vaut souvent plus qu'une fonctionnalité de plus.
- Une entrée dans votre **blogue**, répondant aux questions suivantes&nbsp;: qu'est-ce qui a bien fonctionné depuis le jalon 2 ? Décrivez un moment difficile (un bug, une mauvaise décision initiale, une friction dans l'équipe) et comment vous l'avez résolu. Qu'est-ce que vous feriez différemment si vous recommenciez depuis le début ?

{{% hint warning %}}

**Attention&nbsp;: au jalon 3, l'historique git n'est pas une trace du travail, c'est le livrable.** Le dépôt sera inspecté dans le détail, et pas seulement dans son état final. La distribution des commits dans le temps, leur taille et leur cohérence, la qualité des messages, le découpage en branches et le contenu des pull requests seront examinés pour y chercher la preuve d'une progression graduelle et structurée, et d'un travail en équipe bien balancé et équitable, le cas échéant. Un historique où tout arrive en quelques commits massifs à la veille de la remise raconte une autre histoire que celui d'un projet mené semaine après semaine, et cette différence se lit sans ambiguïté. C'est exactement ce que vise la [philosophie du flux continu](#la-philosophie-du-flux-continu) décrite plus haut.

{{% /hint %}}

### Jalon 4 — Livraison finale (25%)

*À remettre après le module 6*

Ce jalon représente l'aboutissement du projet. Votre application doit être complète, fonctionnelle et déployée automatiquement.

Livrables&nbsp;:
- Un lien vers votre **[application déployée]({{< relref "module5/20-deploiement/index.md" >}})** et pleinement fonctionnelle, accessible sans installation
- Un **[pipeline CI/CD complet]({{< relref "module5/20-deploiement/index.md" >}})** dans le dépôt GitHub : les tests s'exécutent automatiquement et le déploiement se déclenche sans intervention manuelle à chaque push sur la branche principale
- Une sélection de **[transcriptions de session](#montrer-plutôt-que-raconter)** couvrant l'ensemble de la session, qui rend visible l'évolution de votre façon de travailler avec ces outils
- Une **version finale du blogue**, répondant aux questions suivantes&nbsp;: comment avez-vous utilisé l'[IA]({{< relref "module6/60-ia/index.md" >}}) dans votre développement, sur quelles tâches, avec quels résultats, et à quels moments vous a-t-elle déçu ou surpris ? Quelles bibliothèques et quels outils [open source]({{< relref "module6/10-open-source/index.md" >}}) avez-vous choisis, et pourquoi ? Qu'est-ce que ce projet vous a appris que vous n'auriez pas appris autrement ?

### Entretien final (25%)

*Rendez-vous à prendre par vous-même, dans les deux semaines suivant la réception de votre note du jalon 4*

Comme pour l'entretien de mi-parcours, c'est à vous de le fixer, une fois votre note du jalon 4 reçue, par le même [lien de réservation]({{< relref "professeur/index.md" >}}).

L'entretien final est une rencontre individuelle (ou par équipe) de 25 à 30 minutes sur Microsoft Teams. Il porte sur l'ensemble du projet : ses choix techniques, son architecture, son évolution dans le temps, et votre compréhension de ce qui a été produit. Des questions comme « Pourquoi avez-vous structuré vos données de cette façon ? », « Que se passerait-il si votre application devait [gérer dix fois plus d'utilisateurs]({{< relref "module5/60-scalabilite/index.md" >}}) ? » ou « À quel endroit dans votre code l'IA a-t-elle produit quelque chose que vous avez dû corriger ou adapter ? » sont typiques de ce qui sera discuté.

À une époque où les outils d'IA permettent de générer du code fonctionnel sans nécessairement le comprendre, cet entretien est le moyen le plus direct de démontrer que vous avez développé une expertise authentique à travers ce projet.

{{% hint info %}}

## Un dernier mot : 🎉🎉🎉

Ces travaux devraient être, avant tout, un moment d'expérimentation. C'est l'occasion de construire quelque chose qui vous tient réellement à coeur, d'essayer une technologie que vous ne maîtrisez pas encore, de vous tromper et de recommencer. Un projet qui prend des risques et qui porte quelques cicatrices en dira toujours plus long sur ce que vous avez appris qu'un projet impeccable mais sans surprise. La curiosité et la créativité ne sont pas des écarts par rapport aux attentes, elles en font partie.

L'IA a toute sa place dans cette aventure, mais la façon dont vous vous en servez change tout. Comme tutrice, elle vous rend plus compétent&nbsp;: elle explique, elle propose des pistes, elle vous fait découvrir des idées que vous n'auriez pas cherchées. Comme coéquipière à qui l'on refile le gros du travail, elle produit du code dont vous n'êtes que le destinataire. La différence tient souvent à la question posée. « Pourquoi cette requête est-elle si lente ? » vous laisse quelque chose. « Écris-moi cette fonction » vous laisse une fonction.

{{% /hint %}}

