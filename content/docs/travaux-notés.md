---
title: "Travaux notés"
weight: 20
---

# Les travaux notés

## Le projet fil rouge

Ce cours est structuré autour d'un projet de développement logiciel unique, que vous ferez évoluer d'un bout à l'autre de la session. L'idée est simple : plutôt que de produire des travaux déconnectés les uns des autres, vous allez construire quelque chose de concret, en appliquant progressivement les outils et les pratiques vus dans chaque module. Ce projet est donc à la fois un fil conducteur pédagogique et une occasion de vivre, de l'intérieur, les défis réels du génie logiciel moderne. Il n'est pas attendu de vous que vous maîtrisiez ou utilisiez la totalité des techniques et des outils abordés dans le cours — l'objectif est plutôt que vous fassiez des choix éclairés, et que vous soyez capables de les justifier.

## Équipes

Vous pouvez travailler seul ou en équipe de deux ou trois personnes. La coordination et la communication entre équipiers se font sur la plateforme Discord du cours. Si vous travaillez seul, vous devrez simuler au moins deux rôles distincts dans votre processus : celui de chef de projet et celui de développeur. Si vous travaillez en équipe, vous pouvez vous distribuer ces rôles naturellement, ou adopter toute autre organisation qui vous semblera raisonnable.

## Le projet

Vous devrez concevoir et développer une application web de nature commerciale et transactionnelle — pensez à un service de type SaaS, une boutique en ligne, une plateforme de réservation, ou tout autre concept qui implique des utilisateurs, des données et des transactions. Dans un premier temps, il vous faudra imaginer la nature exacte de cette application, pour ensuite simuler une rencontre avec un client imaginaire, afin d'en extraire les spécifications et le fonctionnement attendus.

Votre application devra obligatoirement comporter les éléments suivants : un mécanisme d'authentification et de création d'usagers, une base de données relationnelle (SQL) pour la gestion des données, et l'intégration de l'API Stripe pour le traitement de paiements en ligne simulés. Elle devra également être déployée et accessible en ligne pour les correcteurs, sans qu'ils aient à installer quoi que ce soit sur leur poste. Une plateforme d'infonuagique (Digital Ocean, AWS, Azure, etc.) est une option naturelle, mais toute autre solution permettant d'atteindre cet objectif est acceptable.

## Les jalons

Le projet est évalué à travers quatre jalons, répartis sur la session. Chaque jalon correspond à une étape logique du développement et est ancré dans les modules du cours qui le précèdent. La pondération totale des travaux notés est de 100%, répartie comme suit : J1 (20%), J2 (25%), J3 (25%), J4 (30%).

### Jalon 1 — Fondations (20%)

*À remettre après le module 2*

Ce premier jalon pose les bases de votre projet. Vous devrez avoir clarifié la nature de votre application et établi les fondations techniques et organisationnelles du développement.

Livrables :
- Un rapport de la rencontre (imaginaire ou non) avec le client, décrivant les spécifications et le fonctionnement attendus de l'application
- Un dépôt GitHub contenant le code source initial, avec une structure de projet claire et un fichier `README.md` qui décrit l'application
- Un ensemble de tests automatisés couvrant au moins les fonctionnalités de base déjà implantées
- Une première entrée dans votre journal de bord

### Jalon 2 — Architecture et données (25%)

*À remettre après le module 3*

Ce jalon marque le passage d'un prototype initial à une application mieux structurée. Vous devrez avoir réfléchi à l'architecture de votre système et formalisé votre modèle de données.

Livrables :
- Un document de conception décrivant l'architecture de votre application : les grandes composantes, leurs responsabilités et leurs interactions
- Un document expliquant votre modèle de données : les tables, les relations, et les choix de conception qui les justifient
- Une mise à jour du dépôt GitHub reflétant l'évolution du code depuis le jalon 1
- Une mise à jour du journal de bord

### Jalon 3 — Développement en équipe (25%)

*À remettre après le module 4*

Ce jalon met l'accent sur les pratiques collaboratives et la gestion du projet. Même si vous travaillez seul, vous devrez démontrer une utilisation sérieuse des outils de collaboration et de planification.

Livrables :
- Un lien vers votre plateforme de gestion de projet (GitHub Projects, Jira, Linear, etc.), avec un historique de tâches, d'itérations ou de sprints qui reflète l'évolution réelle du travail
- Un historique de commits et de branches non trivial dans votre dépôt GitHub, qui démontre clairement l'évolution du travail et une utilisation sérieuse du versioning
- Une mise à jour du journal de bord

### Jalon 4 — Livraison finale (30%)

*À remettre après le module 6*

Ce jalon représente l'aboutissement du projet. Votre application doit être complète, fonctionnelle et accessible en ligne.

Livrables :
- Un lien vers votre application déployée et pleinement fonctionnelle, accessible sans installation
- Une mise à jour finale du dépôt GitHub
- Une version finale et complète du journal de bord, incluant une section réflexive sur l'usage que vous avez fait de l'IA dans votre processus de développement, ainsi que sur les outils et bibliothèques open source que vous avez choisis et pourquoi

## Le journal de bord

Le journal de bord est un livrable transversal : vous le commencez dès le jalon 1 et vous l'enrichissez à chaque jalon suivant. Il prend la forme d'entrées datées qui retracent vos décisions, vos difficultés et votre réflexion tout au long du projet. Il peut être hébergé sous n'importe quelle forme moderne : un blogue, un wiki, un dépôt de fichiers Markdown, une page Notion, ou tout autre outil de documentation qui vous convient. L'objectif n'est pas de produire un compte rendu exhaustif de chaque action posée, mais plutôt de démontrer que vous avez fait des choix conscients et que vous êtes capables de les mettre en relation avec les idées et les pratiques vues dans le cours. Un journal rédigé rétrospectivement à la dernière minute sera facilement reconnaissable et ne répondra pas aux attentes.
