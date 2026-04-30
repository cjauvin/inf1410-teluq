---
title: "Travaux notés"
weight: 20
---

# Les travaux notés

## Le projet fil rouge

Ce cours est structuré autour d'un projet de développement logiciel unique, que vous ferez évoluer d'un bout à l'autre de la session. L'idée est simple : plutôt que de produire des travaux déconnectés les uns des autres, vous allez construire quelque chose de concret, en appliquant progressivement les outils et les pratiques vus dans chaque module. Ce projet est donc à la fois un fil conducteur pédagogique et une occasion de vivre, de l'intérieur, les défis réels du génie logiciel moderne. Il n'est pas attendu de vous que vous maîtrisiez ou utilisiez la totalité des techniques et des outils abordés dans le cours — l'objectif est plutôt que vous fassiez des choix éclairés, et que vous soyez capables de les justifier.

{{< image src="../ligne-rouge.png" alt="" title="" loading="lazy" >}}

## L'intelligence artificielle dans ce cours

L'usage de l'IA est non seulement permis dans ce cours, il est activement encouragé. Savoir formuler de bonnes questions, évaluer les réponses et intégrer les suggestions de l'IA de manière critique fait partie des compétences que tout développeur doit maîtriser aujourd'hui. Ignorer ces outils dans un cours de génie logiciel moderne serait à contre-courant de la réalité du métier.

Cette ouverture crée cependant un défi d'évaluation réel. Si un outil peut produire du code fonctionnel, des ADRs convaincants et des réflexions de blogue plausibles, comment distinguer un apprentissage authentique d'une délégation totale ? Ce cours s'attaque à ce problème par deux mécanismes complémentaires.

Le premier est l'entretien de suivi. Ces rencontres visent à évaluer la cohérence entre le niveau de sophistication que vos travaux affichent et la profondeur de votre compréhension réelle, telle qu'elle se manifeste dans une conversation en temps réel. Un écart important entre les deux est, en soi, un signal d'évaluation. L'idée n'est pas d'exiger une mémorisation parfaite de chaque détail, mais de vérifier que vous maîtrisez ce que vous avez produit. Pour quelqu'un qui a réellement travaillé sur le projet, cela devrait aller de soi. Dans certains cas, l'entretien pourra inclure un court exercice pratique sans assistance, à l'image de ce qu'un cours de programmation pourrait faire avec un exercice de code sur tableau blanc. Ce cours n'étant pas un cours de programmation à proprement parler, l'exercice serait adapté en conséquence&nbsp;: une question de conception architecturale, un problème de modélisation de données, ou toute autre tâche en lien direct avec le contenu de votre projet.

Le second mécanisme porte sur la traçabilité temporelle des artefacts. Le problème central avec une délégation excessive à l'IA, c'est qu'elle permet de produire en quelques heures ce qui devrait résulter de semaines de travail itératif. Pour contrer cela, l'évaluation porte non seulement sur ce que vous avez produit, mais sur quand vous l'avez produit.

La plateforme GitHub se prête naturellement à cet exercice. Les commits, les issues, les pull requests et les entrées de blogue hébergés en ligne comportent tous des horodatages enregistrés par les serveurs de GitHub au moment de leur réception. Contrairement aux métadonnées d'un dépôt git local, qui peuvent techniquement être modifiées, ces traces en ligne sont extrêmement difficiles à altérer rétrospectivement. Le graphe d'activité, l'historique des contributions et la chronologie des issues constituent ainsi un journal de bord de votre progression que le correcteur peut consulter avec confiance.

Un projet dont tous les commits arrivent dans les 48 heures précédant une remise, ou dont les entrées de blogue semblent avoir été rédigées en rafale en une seule soirée, ne ressemble pas à un projet qui a évolué pendant plusieurs semaines. Cette différence est visible, et elle est prise en compte dans l'évaluation. L'objectif n'est pas de surveiller chaque geste, mais de vous encourager à travailler de façon régulière et à documenter votre réflexion au moment où elle se produit, ce qui est, au passage, la meilleure façon d'apprendre durablement.

Sur le plan de l'évaluation, une règle simple s'applique&nbsp;: plus vous avez utilisé l'IA, plus les attentes seront élevées quant à la façon dont vous en parlez dans votre blogue technique. Écrire « j'ai utilisé l'IA pour générer du code » est insuffisant. Ce qui est attendu, c'est un regard réflexif et, idéalement, original&nbsp;: comment avez-vous affiné votre façon d'interagir avec ces outils au fil du projet ? Où vous ont-ils surpris, déçu, ou conduit à repenser votre approche ? Avez-vous découvert des usages inattendus, ou développé des techniques d'expérimentation qui vous sont propres ? L'IA est un territoire suffisamment nouveau pour que vos observations personnelles aient de la valeur, et c'est cette curiosité exploratoire qui sera valorisée.

## En équipe ou en solo

Vous pouvez travailler seul ou en équipe de deux ou trois personnes. Les deux options sont équivalentes sur le plan des exigences techniques de base&nbsp;: qualité du code, tests automatisés, intégration continue, ADRs, déploiement et blogue technique sont attendus dans les deux cas.

{{< image src="../team-vs-solo.png" alt="" title="" loading="lazy" >}}

La principale différence porte sur la gestion de projet. Le travail en équipe implique une dimension organisationnelle que le travail solo n'a pas, notamment l'attribution des tâches, la coordination et le suivi des priorités. Pour refléter cet effort, l'utilisation de **GitHub Projects** (tableau de bord, suivi des issues, progression visible) est **requise pour les équipes**. Elle est **optionnelle pour les personnes travaillant seules**. Là où les jalons mentionnent GitHub Projects, la mention *(équipe)* indique que ce livrable ne s'applique qu'aux équipes.

## Le dépôt GitHub

Le dépôt GitHub de votre projet est le mécanisme central de remise et de suivi du cours. Tous les livrables qui ne sont pas du code — ADRs, schémas de données, documentation — doivent être rédigés en texte brut (Markdown de préférence) ou en PDF. Aucun document au format MS Office (Word, Excel, PowerPoint) n'est accepté.

Votre dépôt peut être public ou privé, selon votre préférence. S'il est privé, vous devrez inviter le professeur en tant que collaborateur&nbsp;: son compte GitHub est [cjauvin](https://github.com/cjauvin).

## Le serveur Discord

Le cours dispose d'un [serveur Discord]({{< relref "discord.md" >}}) accessible à tous les étudiants inscrits. Son usage n'est pas obligatoire, mais il fait partie intégrante du concept du cours&nbsp;: il est pensé comme le hub central de communication, aussi bien pour la coordination au sein des équipes que pour toute question ou discussion en lien avec le cours. Chaque équipe y disposera de son propre canal privé, mais le serveur comporte aussi des canaux ouverts à tous, pour poser une question technique, partager une ressource, ou simplement échanger avec d'autres étudiants qui travaillent sur les mêmes problèmes que vous.

Par expérience, le sentiment de communauté qui se développe sur ce genre de plateforme est l'un des aspects les plus bénéfiques de la session. Les cours en ligne peuvent être isolants&nbsp;; Discord brise cette isolation de façon naturelle, et rend l'expérience d'apprentissage plus riche et plus humaine. Les sessions où les étudiants s'y investissent sont presque toujours plus vivantes et plus intéressantes pour tout le monde, y compris pour le professeur.

## Le projet

Vous devrez concevoir et développer une application web de nature transactionnelle, comme un service de réservation, une plateforme communautaire, un outil de gestion, ou tout autre concept qui implique des utilisateurs, des données et des interactions. Votre application devra obligatoirement comporter un mécanisme d'authentification et de création d'usagers, ainsi qu'une base de données relationnelle (SQL) pour la gestion des données. Elle devra également être déployée et accessible en ligne pour les correcteurs, sans qu'ils aient à installer quoi que ce soit sur leur poste.

L'intégration d'une API tierce, comme Stripe pour le traitement de paiements, Twilio pour les notifications, ou toute autre API pertinente à votre domaine, n'est pas obligatoire. De façon générale, les choix techniques ambitieux sont activement encouragés dans ce cours. Un projet qui tente quelque chose de difficile, qui explore des territoires moins familiers, sera toujours évalué avec plus d'intérêt qu'un projet techniquement correct mais sans ambition. Le degré de complexité supplémentaire que vous vous imposez est en soi un critère positif.

## Le blogue technique de développement

Le blogue technique est le fil narratif de votre projet. Il ne s'agit pas d'un rapport de fin de session, mais d'un document vivant que vous alimentez tout au long de la session, au fur et à mesure que vous prenez des décisions, rencontrez des difficultés et faites évoluer votre application. Chaque entrée doit être datée et rédigée de façon contemporaine au développement, et non rétrospectivement.

Le blogue peut prendre la forme qui vous convient&nbsp;: un site hébergé (GitHub Pages, Notion, etc.), un wiki dans le dépôt, ou un dossier de fichiers Markdown. Pour les plus aventureux, [Hugo](https://gohugo.io), le générateur de sites statiques avec lequel ce cours a lui-même été construit, est un excellent choix pour héberger un blogue technique sur GitHub Pages. L'essentiel est que le blogue soit accessible publiquement et qu'il raconte une progression réelle dans le temps.

Les questions posées dans chaque jalon servent de point de départ, pas de plafond. Les entrées peuvent être aussi nombreuses et détaillées que vous le jugez utile. Dans la culture du développement logiciel, le blogue technique est depuis longtemps un outil de réflexion autant que de communication&nbsp;: beaucoup de développeurs écrivent pour clarifier leur propre pensée, pour fixer ce qu'ils viennent d'apprendre, ou pour forcer l'articulation d'une idée encore floue. C'est exactement cet usage qui est valorisé ici. Quelques exemples de blogues techniques qui incarnent cet esprit, et qui valent la peine d'être lus pour leur style autant que pour leur contenu&nbsp;:

- [Joel on Software](https://www.joelonsoftware.com) de Joel Spolsky, l'un des blogues de développement les plus influents jamais écrits
- [Les essais](https://paulgraham.com/articles.html) de Paul Graham, cofondateur de Y Combinator, sur la programmation, les startups et la pensée
- [Le site de Martin Fowler](https://martinfowler.com), référence incontournable sur l'architecture et les pratiques de développement
- [Julia Evans](https://jvns.ca), qui illustre parfaitement l'idée d'écrire pour apprendre et rendre les concepts techniques accessibles

Ce qui distingue un bon blogue d'un rapport générique, c'est la spécificité. Écrire « nous avons choisi PostgreSQL » n'apporte rien. Écrire « lors de la modélisation du panier, on a réalisé que notre schéma initial ne supportait pas les items avec des variantes, ce qui nous a forcés à restructurer la relation entre `orders` et `products` »&nbsp;: voilà ce qui démontre une réflexion authentique. Pour vous guider dans cette direction, chaque jalon précise les questions auxquelles votre entrée de blogue devra répondre.

## La philosophie du flux continu

Les jalons qui structurent ce cours sont une nécessité organisationnelle, pas un modèle de travail. La philosophie qui devrait guider votre progression tout au long de la session est plutôt celle du [CI/CD]({{< relref "module2/50-ci/index.md" >}})&nbsp;: un flux de travail et d'apprentissage le plus continu et régulier possible, où chaque avancée est intégrée, testée et documentée au moment où elle se produit, plutôt qu'accumulée en rafale à l'approche d'une échéance.

En pratique, cela signifie committer régulièrement, alimenter le blogue technique au fil des décisions, et traiter chaque jalon non pas comme une échéance à atteindre, mais comme un point de contrôle dans un développement qui n'a jamais vraiment cessé d'avancer. Les jalons décrivent ce que vous devrez avoir produit à un moment donné&nbsp;; la philosophie du flux continu décrit comment vous devriez y arriver.

## Les jalons

Le projet est évalué à travers quatre jalons et deux entretiens de suivi, répartis sur la session. La pondération totale est de 100%, répartie comme suit&nbsp;: J1 (10%), J2 (15%), entretien mi-parcours (10%), J3 (15%), J4 (25%), entretien final (25%).

### Jalon 1 — Fondations (10%)

*À remettre après le module 2*

Ce premier jalon pose les bases de votre projet. Vous devrez avoir clarifié la nature de votre application et établi les fondations techniques et organisationnelles du développement.

Livrables&nbsp;:
- Un dépôt GitHub contenant un `README.md` avec la **vision client** : qui est l'utilisateur, quel problème l'application résout, et quelle est la solution envisagée (environ une page, rédigée du point de vue de l'utilisateur)
- Un ensemble de **user stories** sous forme de GitHub Issues, traduisant cette vision en tâches concrètes (avec des labels appropriés)
- *(équipe)* Un tableau **GitHub Projects** initialisé avec ces issues en backlog
- Un fichier `.github/workflows/ci.yml` configurant une pipeline CI qui exécute automatiquement la suite de tests à chaque push
- Un ensemble de **tests automatisés** couvrant les fonctionnalités déjà implantées
- Une première entrée dans votre **blogue technique**, répondant aux questions suivantes&nbsp;: qui sont vos utilisateurs et quel problème résolvez-vous ? Quels sont vos premiers choix techniques (langage, framework, hébergement) et quelles alternatives avez-vous considérées ? Qu'est-ce qui est encore incertain à ce stade ?

### Jalon 2 — Architecture et données (15%)

*À remettre après le module 3*

Ce jalon marque le passage d'un prototype initial à une application mieux structurée. Vous devrez avoir réfléchi à l'architecture de votre système et formalisé votre modèle de données.

Livrables&nbsp;:
- Deux ou trois **ADRs** documentant vos choix architecturaux importants : framework, organisation du code, type de base de données, etc. Ils sont hébergés dans le dépôt, par exemple dans un dossier `docs/adr/`
- Un **schéma de données** commenté décrivant vos tables, leurs champs et leurs relations, dans le dépôt
- *(équipe)* Une mise à jour du **tableau GitHub Projects** reflétant l'évolution du travail depuis le jalon 1
- Une entrée dans votre **blogue**, répondant aux questions suivantes&nbsp;: quelle décision architecturale importante avez-vous prise, quel était son contexte, et quelles alternatives avez-vous rejetées et pourquoi ? Quel obstacle concret avez-vous rencontré et comment l'avez-vous résolu ? Qu'est-ce que votre schéma de données révèle de votre compréhension du domaine ?

### Entretien mi-parcours (10%)

*À planifier avec le professeur dans les deux semaines suivant la remise du jalon 2*

Cet entretien est une rencontre individuelle (ou par équipe) de 15 à 20 minutes sur Microsoft Teams. La conversation porte sur ce que vous avez produit jusqu'ici : vos choix techniques, votre schéma de données, le fonctionnement de votre pipeline CI. L'objectif n'est pas de vous piéger, mais de vérifier que vous comprenez et maîtrisez ce que reflète votre dépôt, et d'identifier les points à consolider pour la suite de la session.

### Jalon 3 — Développement (15%)

*À remettre après le module 4*

Ce jalon met l'accent sur l'évolution du projet et la rigueur des pratiques de développement. L'évaluation porte sur la démonstration que les artéfacts du projet ont évolué de manière significative et structurée depuis le jalon 2.

Livrables&nbsp;:
- *(équipe)* Un **tableau GitHub Projects** ayant évolué de manière visible : issues fermées, nouvelles issues ouvertes, progression observable dans le temps
- Un **historique git** non trivial : branches nommées de manière significative, pull requests avec description, commits qui racontent une progression cohérente dans le temps
- De nouveaux **ADRs** documentant les décisions prises depuis le jalon 2
- Une entrée dans votre **blogue**, répondant aux questions suivantes&nbsp;: qu'est-ce qui a bien fonctionné depuis le jalon 2 ? Décrivez un moment difficile (un bug, une mauvaise décision initiale, une friction dans l'équipe) et comment vous l'avez résolu. Qu'est-ce que vous feriez différemment si vous recommenciez depuis le début ?

### Jalon 4 — Livraison finale (25%)

*À remettre après le module 6*

Ce jalon représente l'aboutissement du projet. Votre application doit être complète, fonctionnelle et déployée automatiquement.

Livrables&nbsp;:
- Un lien vers votre **application déployée** et pleinement fonctionnelle, accessible sans installation
- Un **pipeline CI/CD complet** dans le dépôt GitHub : les tests s'exécutent automatiquement et le déploiement se déclenche sans intervention manuelle à chaque push sur la branche principale
- Une **version finale du blogue**, répondant aux questions suivantes&nbsp;: comment avez-vous utilisé l'IA dans votre développement, sur quelles tâches, avec quels résultats, et à quels moments vous a-t-elle déçu ou surpris ? Quelles bibliothèques et quels outils open source avez-vous choisis, et pourquoi ? Qu'est-ce que ce projet vous a appris que vous n'auriez pas appris autrement ?

### Entretien final (25%)

*À planifier avec le professeur dans les deux semaines suivant la remise du jalon 4*

L'entretien final est une rencontre individuelle (ou par équipe) de 25 à 30 minutes sur Microsoft Teams. Il porte sur l'ensemble du projet : ses choix techniques, son architecture, son évolution dans le temps, et votre compréhension de ce qui a été produit. Des questions comme « Pourquoi avez-vous structuré vos données de cette façon ? », « Que se passerait-il si votre application devait gérer dix fois plus d'utilisateurs ? » ou « À quel endroit dans votre code l'IA a-t-elle produit quelque chose que vous avez dû corriger ou adapter ? » sont typiques de ce qui sera discuté.

À une époque où les outils d'IA permettent de générer du code fonctionnel sans nécessairement le comprendre, cet entretien est le moyen le plus direct de démontrer que vous avez développé une expertise authentique à travers ce projet.
