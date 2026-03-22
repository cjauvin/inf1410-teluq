# Module 1 — Le génie logiciel

## Introduction au génie logiciel (complété)
- Le problème fondamental : pourquoi le logiciel est difficile (rapport CHAOS, SAAQclic)
- Définition du GL : programmer vs faire du génie logiciel
- Complexité essentielle vs accidentelle (Fred Brooks, *No Silver Bullet*)
- Présentation de la structure du cours (les six modules)

## Histoire du GL (complété)

### Quelques livres et articles fameux référencés
- *The Mythical Man-Month* (Fred Brooks)
- *The Pragmatic Programmer* (Hunt, Thomas)
- *Clean Code* (Robert Martin)
- *Design Patterns* (Gang of Four)
- *No Silver Bullet* (Fred Brooks)
- *Programming as Theory Building* (Peter Naur)

### Les années 40 à mi-60 : l'ère pré-GL
- ENIAC et les premiers ordinateurs
- Premiers assembleurs et compilateurs
- FORTRAN, LISP, ALGOL et COBOL
- Premiers OS

### Les années 60 et 70 : la crise logicielle et la naissance du GL
- Conférence NATO (crise du logiciel)
- Programmation structurée (Dijkstra)
- Modèle en cascade (waterfall)
- Modèle relationnel (Edgar Codd)
- Modèle en spirale (Barry Boehm)
- *The Mythical Man-Month* et la loi de Brooks
- *No Silver Bullet*
- Unix et C

### Les années 80 : l'ère des abstractions, du PC et du GUI
- OOP et C++
- GUI et programmation événementielle (Macintosh, Windows)
- Standardisation de la stack de networking (TCP/IP)

### Les années 90 : la naissance du web
- Web (Tim Berners-Lee)
- JavaScript
- Java
- Python (Guido van Rossum)
- Open source, Linux (Linus Torvalds)
- Design patterns (Gang of Four)
- UML
- Extreme Programming (Kent Beck)
- *The Pragmatic Programmer* et le principe DRY

### Les années 00 : l'ère de l'agilité
- Manifeste Agile (Snowbird 2001)
- Scrum, Kanban
- Web 2.0
- AWS (2006)
- GitHub (2008)

### Les années 10 : l'ère du cloud et du DevOps
- CI/CD
- Microservices
- Docker, Kubernetes
- Serverless

### Les années 20 : l'ère de l'IA
- LLM, GitHub Copilot, ChatGPT, Claude Code

# Module 2 - Concevoir un logiciel correct

## Introduction (complété)
- *Programming as Theory Building* (Peter Naur) : programmer comme construction d'une théorie / d'un modèle mental
- Fil conducteur du module : les outils pour formaliser, vérifier et préserver cette théorie

## Survol rapide de la programmation (complété)
- Structures de données (listes, ensembles, dictionnaires)
- Complexité algorithmique (Big O, Two Sum, recherche binaire)
- Paradigmes de programmation :
  - Impératif/procédural (Fortran, C, programmation structurée de Dijkstra)
  - Orienté-objet (Simula, Smalltalk/Alan Kay, encapsulation/héritage/polymorphisme)
  - Fonctionnel (lambda calcul, Lisp/McCarthy, Haskell, Erlang, immutabilité, fonctions d'ordre supérieur)
  - Langages multi-paradigmes (Python, tendance moderne)
- Types : compilé vs interprété, statique vs dynamique, fort vs faible,
  type hints Python/mypy, lien avec les schémas JSON et SQL

## Les tests (complété)
- Pourquoi tester : confronter le modèle mental (Naur) à la réalité
- Tests comme substitut partiel au compilateur en Python
- Le mécanisme de base : `assert`
- Pyramide des tests : unitaires, d'intégration, end-to-end
- pytest comme framework de test
- TDD (Test-Driven Development) : cycle Red-Green-Refactor (Kent Beck)
- Coverage (coverage.py, pytest-cov) et ses limites
- Fixtures : `@pytest.fixture`, scopes, yield/teardown, `conftest.py`
- Mocking : `monkeypatch` (setattr, setenv/delenv), mention de `unittest.mock`
- Property-based testing (Hypothesis) et lien avec le fuzzing

## Le versioning avec git (complété)
- Problème fondamental du changement
- Histoire du versioning (SCCS → CVS → SVN → Git)
- Objets git (blobs, trees, commits), branches, merges, DAG

## La gestion des dépendances (complété)
- Problème de la réutilisation et de la décomposition
- Sécurité de la chaîne d'approvisionnement
- Versionnement sémantique (SemVer)
- uv comme outil concret (bibliothèques, applications, venv, lock files)

## L'intégration continue - CI (complété)
- Le problème : vérifications manuelles, "ça marche sur ma machine"
- Historique : Extreme Programming (Kent Beck), article de Martin Fowler (2006)
- Aparté sur YAML : syntaxe de base, pièges (indentation, types implicites)
- GitHub Actions : concepts (workflow, event, job, step, action, runner)
- Exemple concret : projet Python avec pytest, workflow CI, démo sur GitHub
- Au-delà des tests : linting (ruff), formatage, type checking (mypy), sécurité des dépendances
- Lien CI → CD (déploiement continu), renvoi au module 5

# Module 3 - Du programme au système

## Introduction : la complexité comme problème central (complété)
- Le passage du programme au système
- Complexité essentielle vs accidentelle (Brooks, *No Silver Bullet*)
- La gestion de la complexité comme fil conducteur
- Les principes fameux comme heuristiques (introduction, avec renvoi vers
  la page de référence transversale `content/docs/principes.md`)
- Les principes sont développés en profondeur dans les sections où ils
  sont le plus pertinents (dans ce module et les suivants)

NOTE : revisiter les modules 1 et 2 pour y intégrer des références aux
principes pertinents (ex: DRY dans la gestion des dépendances, etc.)

NOTE : définir les termes SRE (Site Reliability Engineer) et SWE (Software
Engineer) quelque part dans le cours (probablement module 5 ou module 1)

## Architecture et modularité (complété)
- Introduction : pourquoi découper ?
- Parnas et l'information hiding (1972)
  - Exemple KWIC (Key Word In Context) reproduit en Python
  - Deux décompositions comparées : par flux vs par information hiding
  - Principe : Separation of Concerns
- Couplage et cohésion
  - Définitions avec exemples Python
  - Lien avec DRY : la duplication comme symptôme de mauvais découpage
- SOLID (principes de conception OO)
  - Focus sur S (Single Responsibility) et D (Dependency Inversion)
  - Les autres (O, L, I) traités plus brièvement
  - Perspective critique : lien avec YAGNI
- Composition over inheritance
  - Exemple Python : héritage vs composition
  - Lien avec le principe d'inversion des dépendances
- Les couches (layers)
  - Pattern présentation → logique → données
  - Exemple concret en Python
- Monolithe vs microservices
  - Le monolithe comme point de départ raisonnable
  - Quand et pourquoi découper
  - Loi de Conway (pont vers module 4)
- Patterns architecturaux
  - Client-server
  - MVC (Reenskaug, 1979) et frameworks web (Rails, Django, Flask, etc.)
  - Pipes and filters (philosophie Unix, lien avec KWIC)
  - Architecture événementielle (event-driven, Kafka, RabbitMQ)

## Les APIs (complété)

### L’API comme concept évolutif
- L’API au sens originel : l’interface d’une bibliothèque (fonctions qu’on appelle dans son propre code)
- Le virage réseau : l’API comme contrat entre systèmes distribués (introduction du réseau, latence, pannes, sérialisation)
- L’API comme produit : Stripe, Twilio, etc. Documentation, versioning, SLAs. L’économie de l’API.

### Les paradigmes d’APIs réseau
- RPC (Remote Procedure Call) : faire semblant que l’appel réseau est un appel de fonction
  - CORBA, XML-RPC, SOAP
  - Les fallacies of distributed computing (Peter Deutsch, 1994) : pourquoi l’illusion du RPC transparent est dangereuse
- REST (Roy Fielding, thèse de doctorat, 2000) : rupture conceptuelle, manipulation de ressources
  - HTTP comme protocole applicatif (verbes, codes de statut, headers)
  - Richardson Maturity Model (niveaux 0-3)
  - HATEOAS : la vision originale de Fielding vs la pratique (billet de 2008)
  - Exemple concret : API FastAPI avec curl
- GraphQL (Facebook, 2015) : le client décide de la forme des données
  - Problème du over-fetching/under-fetching
  - Comparaison SQL vs GraphQL (niveaux différents de l'architecture)
  - Schéma introspectable comme alternative à HATEOAS pour la découvrabilité
  - Exemple concret : serveur Strawberry avec curl
- gRPC (Google, 2015) : retour au RPC avec les leçons apprises (Protobuf, HTTP/2, streaming)
- Webhooks : l’inversion du modèle requête-réponse (lien avec l’architecture événementielle)

### Design d’API et schémas
- Principes de design : nommage, versioning, gestion des erreurs, idempotence
- Schémas comme contrat : OpenAPI/Swagger (REST), fichiers .proto (gRPC), schéma introspectable (GraphQL)
- Lien avec DRY : le schéma comme source unique de vérité
- Lien avec la section sur les schémas (module 3, données)

### Le pattern Backend For Frontend (BFF)
- BFF (Sam Newman, 2015) : un backend dédié par type de client
- Lien avec GraphQL : deux réponses au même problème (besoins différents par client)
- Lien avec la fragmentation multi-plateforme (section interfaces, tensions et convergences)
- Nuance : YAGNI quand un seul type de client, complémentarité avec GraphQL

## Les interfaces utilisateur (complété)

### Perspective historique (complété)
- Les terminaux texte et les interfaces en ligne de commande (CLI)
  - Teletypes (TTY), terminaux vidéo (VT100), shells (Bourne Shell, Bash, Zsh, PowerShell)
  - Puissance de composition de la CLI, lien avec pipes and filters (Unix)
- Xerox PARC, Smalltalk et la naissance du GUI (années 70-80)
  - Alto (1973), métaphore du bureau, souris (Engelbart, 1968)
  - Smalltalk (Alan Kay), MVC (Reenskaug, 1979), renvoi vers la section architecture
  - Macintosh (1984), Windows (1985/1990)
- Le modèle événementiel : de la boucle d'événements aux callbacks
  - Inversion du contrôle, exemple comparé CLI vs Tkinter en Python
- Visual Basic (1991) : démocratisation du développement GUI par drag-and-drop (RAD)
- Les toolkits desktop : Tk, Win32/MFC, Cocoa, GTK, Java AWT/Swing, Qt
  - Tension multiplateforme : Java "write once, run anywhere" vs Qt code natif
- Flash/ActionScript (Macromedia, puis Adobe) : le web interactif avant HTML5, mort annoncée par Steve Jobs (2010)
- Web 2.0 (Tim O'Reilly, 2004) : AJAX, Google Maps, le web comme média de participation
- Le web comme plateforme UI : HTML/CSS/JS, avantage du déploiement, migration des applications desktop vers le web

### L'architecture des applications web (complété)
- Le modèle traditionnel : rendu côté serveur (SSR), pages complètes, formulaires (PHP, Django, Rails)
- AJAX : le navigateur devient un acteur, tension client/serveur
- Single Page Application (SPA) : principe, avantages, inconvénients, renvoi vers les frameworks JS
- Le retour du SSR et les approches hybrides : hydration, meta-frameworks (Next.js, Nuxt, SvelteKit)
- Static Site Generation (SSG) et Jamstack : Hugo, Jekyll, Gatsby, Astro, CDN

### Les frameworks JavaScript (complété)
- Le DOM (Document Object Model) : représentation vivante de la page, API de manipulation
- La tension déclaratif vs impératif comme fil conducteur
- jQuery (2006, John Resig) : simplification du DOM, uniformisation des navigateurs, spaghetti jQuery
- Angular (2010 AngularJS / 2016 Angular) : framework complet, two-way data binding, TypeScript, opinionné
- React (2013, Facebook) : DOM virtuel, composants fonctionnels, hooks, JSX, Separation of Concerns revisitée
  - Composants : concept universel du UI, correspondance OOP naturelle, approche fonctionnelle de React
- Vue.js (2014, Evan You) : approche progressive, réactivité par observables, templates avec directives
- Svelte (2016, Rich Harris) : compilation, disparition du framework au runtime, SvelteKit
- Préoccupations transversales : state management (Redux, Pinia, stores), routing côté client, meta-frameworks

### Desktop, web et mobile : tensions et convergences (complété)
- Applications desktop natives : performance, accès système, distribution complexe
- Applications mobiles natives (iOS/Swift, Android/Kotlin) : écosystèmes fermés, app stores, commission 30%
  - Langages et toolkits : Objective-C/Swift/UIKit/SwiftUI, Java/Kotlin/Android SDK/Jetpack Compose
  - Conventions de design : Human Interface Guidelines (Apple), Material Design (Google)
- Responsive web design (Ethan Marcotte, 2010, *A List Apart*) : media queries CSS, adaptation dynamique
- Frameworks cross-platform : React Native (2015), Flutter (2018, Dart, Skia/Impeller), .NET MAUI, Kotlin Multiplatform
- Progressive Web Apps (PWA, Google 2015) : service workers, manifeste, mode hors-ligne, résistance d'Apple
- Electron (GitHub, 2014) : Chromium embarqué, VS Code/Slack/Discord, consommation mémoire
- Tauri (2022) : WebView natif, backend Rust, alternative légère à Electron
- WebAssembly (WASM, W3C 2017) : code compilé dans le navigateur, Figma, Google Earth
- La tension fondamentale : write once run anywhere vs expérience native optimale

## Les données (complété)

### La représentation des données (complété)
- Données vs information vs connaissances (pyramide DIKW)
- Encodage et sérialisation (ASCII, UTF-8, CSV, XML, JSON, Protobuf)
- La notion de schéma (SQL DDL, type hints, OpenAPI, JSON Schema)
- Évolution des schémas (compatibilité avant/arrière)

### Le stockage des données (complété)
- Arc historique : modèle hiérarchique (IMS, IBM, 1966) → réseau (CODASYL, 1969) → relationnel (Codd, 1970)
- Transactions et propriétés ACID (Jim Gray)
- ORMs et impedance mismatch (Hibernate, ActiveRecord, SQLAlchemy)
- La révolution NoSQL (2009) :
  - Bases clé-valeur (Redis, caching, invalidation)
  - Bases orientées documents (MongoDB, lien avec IMS)
  - Bases orientées colonnes (OLTP vs OLAP, data warehouse, ETL)
  - Bases orientées graphes (Neo4j, Cypher, lien avec CODASYL)
- Bases de séries temporelles (InfluxDB, Prometheus, TimescaleDB)
- Bases vectorielles (embeddings, Word2Vec, RAG, ANN/HNSW)

### Au-delà des bases de données (complété)
- Recherche et indexation (Salton, SMART, index inversé, TF-IDF, Elasticsearch)
- Stockage objet (S3, MinIO, data lake vs data warehouse)
- Données répliquées et CRDTs (Shapiro et al. 2011, Automerge, Yjs)
- Registres immuables et blockchain (Nakamoto 2008, event sourcing, chaînage cryptographique)

# Module 4 - Construire en équipe

## Introduction (complété)
- Brooks (*The Mythical Man-Month*) : la communication comme coût quadratique
- Loi de Conway : l’organisation et le logiciel se façonnent mutuellement
- Tension autonomie vs coordination comme problème central

## Git distribué et GitHub (complété)
- Distinction git vs GitHub (Torvalds 2005, Preston-Werner/Wanstrath/Hyett 2008, rachat Microsoft 2018)
- Git distribué : push, pull, clone, remotes, le "quatrième endroit"
- Pull requests et collaboration (scénario Leila/Sara)
- Workflows git : Git Flow (Driessen 2010), GitHub Flow, trunk-based development
- Code reviews : inspections de Fagan (IBM 1976), objectifs, dimension humaine, pratiques Google
- Protection de branches et lien CI

## L’agilité (complété)
- Le manifeste Agile et contexte historique (complété)
- Mention d’XP avec renvois vers module 2 (TDD, CI) (complété)
- Perspective critique (complété) : l’agilité dévoyée, "Agile is Dead" (Dave Thomas, 2014),
  Dark Scrum (Ron Jeffries), loi de Goodhart, industrie des certifications, cargo cult agile,
  dette organisationnelle

### Scrum (complété)
- Historique : Takeuchi et Nonaka (1986), Sutherland et Schwaber (1990s), Scrum Guide
- Rôles : Product Owner, Scrum Master, équipe de développement
- Rappel de la loi de Conway : composition de l'équipe comme décision architecturale implicite
- Démonstration GitHub Projects (scénario RéservaSalle, équipe Leila/Sara/Marco/Nadia) :
  - Mise en place : vues (Table, Board, Roadmap), colonnes (Status), ajout In Review, champs (Story Points, Iteration)
  - Product backlog : user stories (format « En tant que... »), labels (story, tech, bug), introduction de l’outil `gh`
  - Cérémonies du sprint : sprint planning (estimation, vélocité, objectif de sprint), daily standup, sprint review, rétrospective
  - Déroulement d’un sprint : flux des issues (Todo → In Progress → In Review → Done), lien avec branches/PR, automatisation
  - Auto-calibration : vélocité mesurée, amélioration continue via les rétrospectives

### Kanban (complété)
- Historique : Toyota (Taiichi Ohno, TPS, flux tiré), David Anderson (2010)
- Principes fondamentaux : visualisation du flux, limites de WIP, flux continu
- Analogie de l'autoroute pour illustrer le WIP
- Métriques : cycle time et lead time (contraste avec la vélocité de Scrum)
- Démonstration GitHub Projects (scénario RéservaSalle) :
  - Configuration : mêmes colonnes, pas de story points ni d'itérations, limites de WIP
  - Flux de travail : « stop starting, start finishing », régulation par les limites
- Comparaison Scrum vs Kanban, Scrumban, critères de choix

## Gestion de projet et coordination (complété)
- Documentation comme outil de coordination :
  - ADRs (Architecture Decision Records, Michael Nygard 2011), lien avec Naur
  - RFCs internes (Google design docs, Rust RFCs, PEPs Python, TC39 JavaScript)
- Communication synchrone vs asynchrone :
  - Slack (Stewart Butterfield 2013, histoire de Glitch), Microsoft Teams, Discord
  - Zoom et la pandémie de 2020
  - Watercooler conversations et communication informelle
  - GitLab "handbook first", Basecamp/Shape Up (Ryan Singer 2019)
  - Manœuvre de Conway inverse, *Team Topologies* (Skelton et Pais, 2019)
- Estimation :
  - Difficulté fondamentale (lien avec Brooks, optimisme chronique)
  - Planning poker, effet d'ancrage
  - Approches alternatives (découpage en petites tâches)
- Dette technique :
  - Métaphore de Ward Cunningham (OOPSLA 1992)
  - Quadrant de Fowler (2009) : délibérée/accidentelle × prudente/imprudente
  - Refactoring (Fowler 1999), lien avec tests et CI (module 2), architecture (module 3)
  - Gestion en équipe : allocation sprint, arbitrage features vs dette, communication avec les gestionnaires
  - Lien vers module 5 : conséquences opérationnelles de la dette non remboursée

# Module 5 - Faire vivre le logiciel

## Introduction (complété)
- Le mur historique entre dev et ops : « on l'a codé, maintenant c'est votre problème »
- *The Phoenix Project* (Gene Kim, 2013) et la naissance du mouvement DevOps
- Les trois voies de DevOps (flow, feedback, apprentissage continu) comme grille de lecture
- La Twelve-Factor App (Adam Wiggins, Heroku, 2011) : présentation générale, principes distribués dans le module
- Pont avec les modules précédents (CI du module 2, équipes du module 4)

## « Où est-ce que ça tourne ? » (complété)
- L'ère pré-cloud : le serveur physique, le datacenter, la colocation
- La virtualisation (VMware, Xen) et le virage vers l'abstraction
- Le cloud (AWS 2006, GCP, Azure) : IaaS, PaaS, SaaS, pay-as-you-go
- Serverless / FaaS (Lambda 2014) : pousser l'abstraction à l'extrême
- La conteneurisation : contexte historique (chroot, cgroups, namespaces Linux),
  Docker (Solomon Hykes, 2013), section existante intégrée
- L'orchestration : Kubernetes (Google, Borg → K8s 2014), pods, deployments,
  services, ingress, labels/selectors, modèle déclaratif, control loop
- Tutoriel k3d : transposer l'app Flask+Redis de docker compose vers Kubernetes
  - k3d (cluster local), k9s (TUI), kubectl
  - Manifests YAML, résilience (kill pod, recréation automatique),
    scaling horizontal (3 répliques, load balancing), nodes
- Infrastructure as Code :
  - Le problème du snowflake server
  - Le paradigme déclaratif comme fil rouge (SQL, K8s, Terraform, Ansible)
  - Terraform (HashiCorp 2014) : HCL, plan/apply, state, provisioning
  - Configuration management : Puppet (2005), Chef (2009), Ansible (Red Hat 2012, agentless, playbooks)
  - GitOps (Weaveworks 2017) : git comme source de vérité pour l'infrastructure

## « Comment je le déploie ? » (complété)
- Du CI au CD : reprendre le fil du module 2
  - *Continuous Delivery* (Jez Humble et David Farley, 2010) : le livre fondateur
  - Le deployment pipeline comme concept
  - Distinction continuous delivery vs continuous deployment
- Le pipeline en pratique avec GitHub Actions
  - Workflow CI/CD complet : job tests → job deploy
  - Mécanismes : `needs`, environments, secrets, tag par `github.sha`
  - Lien avec les commandes connues : `uv sync`, `docker build`, `kubectl set image`
  - Facteur III de la Twelve-Factor App (config dans l'environnement)
- Stratégies de déploiement
  - Rolling update : remplacement progressif, comportement par défaut de Kubernetes
    - Démonstration k3d : ajout d'un endpoint `/version`, observation de la transition avec `curl`
  - Blue-green deployment : deux environnements, bascule instantanée (Martin Fowler, Humble/Farley)
  - Canary deployment : déploiement progressif, monitoring des métriques (Netflix)
  - Synthèse et combinaisons possibles
- Feature flags
  - Découpler déploiement et activation
  - Exemple Python : variable d'environnement comme flag
  - Dark launching (Facebook, 2008) : ancêtre des feature flags
  - Outils spécialisés : LaunchDarkly, Unleash, Flagsmith
  - Mise en garde : dette technique des flags non nettoyés
- Immutable infrastructure
  - Philosophie : ne jamais modifier, toujours remplacer
  - Lien avec l'immutabilité en programmation fonctionnelle (module 2)
  - Facteur V (build/release/run) : les trois phases du déploiement
  - Facteur X (dev/prod parity) : Docker comme solution
  - Facteur III (config) : la configuration comme seule variable entre environnements

## « Est-ce que ça marche ? » (complété)
- Introduction : perte de visibilité en production, deuxième voie de DevOps (feedback)
  - Origine du terme : Rudolf Kálmán (théorie du contrôle, 1960), filtre de Kálmán
  - Monitoring vs observabilité : Charity Majors (Honeycomb, 2017-2018)
- Les trois piliers de l'observabilité : logs, métriques, traces
- Logs (complété) :
  - Du `print()` au logging structuré, exemple Python progressif
  - syslog (Eric Allman, 1983), module `logging` Python, logs JSON structurés
  - Stack ELK (Elasticsearch, Logstash, Kibana, 2012-2014)
  - Twelve-Factor facteur XI : logs comme flux d'événements (stdout)
- Métriques (complété) :
  - Quatre golden signals (Google SRE 2016) : latence, trafic, erreurs, saturation
  - Graphite (Chris Davis, Orbitz, 2008) et StatsD (Etsy, 2011) : modèle push
  - Prometheus (SoundCloud, 2012, inspiré de Borgmon) : modèle pull, CNCF
  - Types de métriques : counter, gauge, histogram, summary
  - Instrumentation Python avec `prometheus_client`
  - Grafana (Torkel Ödegaard, 2014) : visualisation et dashboards
- Tracing distribué (complété) :
  - Dapper (Google, 2010) : trace ID, spans, arborescence
  - Zipkin (Twitter, 2012), Jaeger (Uber, 2017)
  - OpenTelemetry (2019) : fusion OpenTracing + OpenCensus, standard unifié
  - Granularité : interactions entre services, pas appels de fonctions (→ profilers)
- Alertes (complété) :
  - Fatigue d'alerte, parallèle avec le domaine médical
  - Alertes actionnables (Google SRE) : pages, tickets, logs
  - Symptômes vs causes, seuils réalistes, runbooks
- SLIs, SLOs, SLAs (complété) :
  - SLI : mesure du point de vue utilisateur (ratio bonnes/totales)
  - SLO : cible sur un SLI, coût exponentiel des "9"
  - SLA : contrat formel avec conséquences financières
  - Error budget : le droit à l'erreur comme ressource, lien avec la troisième voie de DevOps
- Tutoriel pratique (complété) : app FastAPI instrumentée + Prometheus + Grafana dans k3d

## « Que faire quand ça casse ? » (complété)
- L'incident est inévitable : accepter la faillibilité (AWS S3 2017, GitLab 2017)
- Site Reliability Engineering (Ben Treynor Sloss, Google 2003, livre 2016) : cadre de référence
- Error budgets : quantifier le droit à l'erreur, lien avec les SLOs (section observabilité)
- Anatomie d'un incident : détection → triage → mitigation → résolution → postmortem
- On-call et incident commander : rôles concrets pendant un incident
- Postmortems blameless : John Allspaw (Etsy, 2012), Sidney Dekker, just culture
- Chaos engineering : Netflix Chaos Monkey (2010), Principles of Chaos Engineering (2014), game days
- Runbooks et automatisation : du document au code, lien avec Kubernetes health checks
- La dette technique comme source d'incidents : lien avec le module 4 (Ward Cunningham 1992)

## « Est-ce que c'est sécuritaire ? » (à développer)
- La sécurité comme préoccupation transversale, pas une couche ajoutée après
- DevSecOps et shift left : intégrer la sécurité dans le pipeline
- OWASP Top 10 : tour d'horizon des vulnérabilités web
- HTTPS/TLS : le chiffrement en transit
- Gestion des secrets (vaults, variables d'environnement)
- Authentification et autorisation (OAuth 2.0, JWT, sessions)
- Sécurité de la supply chain logicielle (lien avec module 2, dépendances)
- Principe du moindre privilège

## « Est-ce que ça va tenir la charge ? » (à développer)
- Scalabilité verticale vs horizontale
- Load balancing (round-robin, health checks)
- Caching (navigateur, CDN, Redis/Memcached, invalidation)
- Réplication de bases de données, sharding
- CDN (Content Delivery Network)
- Théorème CAP (Brewer, 2000)
- Files d'attente et traitement asynchrone (lien avec architecture événementielle, module 3)

# Module 6 - Au-delà du logiciel

## Le développement assisté par IA (à développer)
- Historique : autocomplétion → Copilot (2021) → ChatGPT (2022) → agents (Claude Code, Cursor, etc.)
- Le "vibe coding" et ses limites
- Impact sur les pratiques du GL : tests encore plus importants, code review change de nature
- Questions ouvertes : propriété intellectuelle, fiabilité, dépendance

## Les grandes catastrophes logicielles et leurs leçons (à développer)
- Therac-25 (radiothérapie mortelle), Ariane 5, Knight Capital (440M$ en 45 minutes), Boeing 737 MAX MCAS
- Boucle avec le module 1 : la crise du logiciel revisitée avec des cas concrets et modernes
- Lois de Lehman sur l'évolution du logiciel (1974) : un logiciel qui ne change pas devient progressivement inutile
- Éthique et responsabilité : biais algorithmiques, vie privée, ACM Code of Ethics

## Le métier de développeur et son évolution (à développer)
- Le mythe du "10x developer", l'impostor syndrome, le burnout
- Le débat craft vs engineering : Manifeste du Software Craftsmanship (2009)
- *Working Effectively with Legacy Code* (Michael Feathers, 2004) : la réalité du code existant
- Évolution du rôle : programmeur → développeur → full-stack → DevOps → AI-augmented

## La dette intellectuelle du domaine (à développer)
- Les idées qui reviennent en cycle (Lisp → fonctionnel moderne, Smalltalk → React, etc.)
- Fred Brooks revisité 30 ans plus tard : a-t-on trouvé la silver bullet ?
- "Worse is better" (Richard Gabriel, 1989) : pourquoi les solutions imparfaites gagnent souvent

## L'open source (à développer)
- Historique : Stallman, GNU (1983), FSF, GPL vs licences permissives (MIT, Apache, BSD)
- *The Cathedral and the Bazaar* (Eric Raymond, 1997)
- Le problème du mainteneur épuisé (left-pad 2016, xz backdoor 2024, Heartbleed)
- Business models : support, dual licensing, open core, SaaS
