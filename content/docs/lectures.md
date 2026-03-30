---
title: "Lectures et publications de référence"
weight: 16
---

# Lectures et publications de référence

Cette page rassemble les livres, articles et publications importants qui sont
mentionnés à travers l'ensemble du cours. Chaque entrée pointe vers la ou les
sections où elle est discutée.

*(Cette page sera enrichie au fur et à mesure que de nouvelles références seront
intégrées dans le cours.)*

## Livres

- Fred Brooks, *The Mythical Man-Month* (1975) : réflexions sur la gestion de
  grands projets logiciels, dont la célèbre « loi de Brooks » → [Module 1, Perspective historique]({{< ref "/docs/module1/10-historique" >}}),
  [Module 6, L'économie du logiciel]({{< ref "/docs/module6/20-economie" >}})
- Andrew Hunt et David Thomas, *The Pragmatic Programmer* (1999) : conseils
  pratiques pour le développeur, origine du principe DRY → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- Kent Beck, *Extreme Programming Explained* (1999) : manifeste de l'XP, origine
  de YAGNI et du TDD → [Module 1, Perspective historique]({{< ref "/docs/module1/10-historique" >}})
- Robert C. Martin, *Clean Code* (2008) : principes de conception et SOLID →
  [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- Mike Cohn, *Succeeding with Agile* (2009) : la pyramide des tests →
  [Module 2, Les tests]({{< ref "/docs/module2/20-tests" >}})
- David Anderson, *Kanban: Successful Evolutionary Change for Your Technology
  Business* (2010) : formalisation de la méthode Kanban pour le développement
  logiciel → [Module 4, Kanban]({{< ref "/docs/module4/20-agile/20-kanban" >}})
- Gang of Four (Gamma, Helm, Johnson, Vlissides), *Design Patterns* (1994) :
  catalogue fondateur des patrons de conception → [Module 1, Perspective historique]({{< ref "/docs/module1/10-historique" >}}), [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- Martin Kleppmann, *Designing Data-Intensive Applications* (2017) : référence
  moderne sur les systèmes de données → [Module 3, Les données]({{< ref "/docs/module3/40-données" >}})
- Martin Fowler, *Refactoring: Improving the Design of Existing Code* (1999) :
  formalisation du refactoring comme discipline, mécanisme de remboursement de la
  dette technique →
  [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})
- Ryan Singer, *Shape Up* (2019) : méthodologie de développement de Basecamp,
  approche asynchrone et "pitches" écrits →
  [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})
- Matthew Skelton et Manuel Pais, *Team Topologies* (2019) : taxonomie des
  structures d'équipe et de leurs effets sur l'architecture logicielle, manœuvre
  de Conway inverse →
  [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})
- Gene Kim, Kevin Behr et George Spafford, *The Phoenix Project* (2013) : roman
  fondateur du mouvement DevOps, parallèle entre lean manufacturing et livraison
  logicielle →
  [Module 5, Introduction]({{< ref "/docs/module5" >}})
- Gene Kim, Jez Humble, Patrick Debois et John Willis, *The DevOps Handbook*
  (2016) : formalisation des trois voies de DevOps (flow, feedback, apprentissage
  continu) →
  [Module 5, Introduction]({{< ref "/docs/module5" >}})
- Google (Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy),
  *Site Reliability Engineering* (2016) : formalisation des pratiques SRE, error
  budgets, on-call, postmortems →
  [Module 5, Que faire quand ça casse ?]({{< ref "/docs/module5/40-incidents" >}})
- Sidney Dekker, *The Field Guide to Understanding Human Error* (2006) :
  approche systémique des erreurs humaines, fondement de la culture « just
  culture » et des postmortems blameless →
  [Module 5, Que faire quand ça casse ?]({{< ref "/docs/module5/40-incidents" >}})
- Reid Hoffman, *Blitzscaling* (2018) : formalisation de la stratégie de
  croissance rapide des startups technologiques, tension entre vitesse et
  qualité →
  [Module 6, L'économie du logiciel]({{< ref "/docs/module6/20-economie" >}})
- Michael Feathers, *Working Effectively with Legacy Code* (2004) : définition
  du legacy code comme code sans tests, techniques pour travailler sur du code
  existant →
  [Module 6, Le métier de développeur]({{< ref "/docs/module6/50-metier" >}})

## Essais et manifestes

- Eric Raymond, *The Cathedral and the Bazaar* (1997) : comparaison des modèles
  de développement cathédrale (GNU) et bazar (Linux), loi de Linus →
  [Module 6, L'open source]({{< ref "/docs/module6/10-open-source" >}})
- Adam Wiggins, *The Twelve-Factor App* (2011) : douze principes pour concevoir
  des applications cloud-native, issus de l'expérience de Heroku →
  [Module 5, Introduction]({{< ref "/docs/module5" >}}),
  [Module 5, Comment je le déploie ?]({{< ref "/docs/module5/20-deploiement" >}})

## Articles et essais

- Edgar F. Codd, *A Relational Model of Data for Large Shared Data Banks* (1970) :
  article fondateur du modèle relationnel → [Module 1, Perspective historique]({{< ref "/docs/module1/10-historique" >}}), [Module 3, Les données (stockage)]({{< ref "/docs/module3/40-données/20-stockage" >}})
- David Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*
  (1972) : introduction de l'information hiding → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- Peter Naur, *Programming as Theory Building* (1985) : programmer comme
  construction d'un modèle mental → [Module 2, Introduction]({{< ref "/docs/module2" >}}),
  [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})
- Fred Brooks, *No Silver Bullet* (1986) : complexité essentielle vs
  accidentelle → [Module 3, Introduction]({{< ref "/docs/module3" >}}),
  [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})
- Melvin Conway, *How Do Committees Invent?* (1968) : la structure d'un système
  reflète celle de l'organisation qui le produit (loi de Conway) →
  [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}}),
  [Module 4, Scrum]({{< ref "/docs/module4/20-agile/10-scrum" >}}),
  [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})
- Ward Cunningham, *The WyCash Portfolio Management System* (OOPSLA 1992) :
  introduction de la métaphore de la dette technique →
  [Module 4, Gestion de projet]({{< ref "/docs/module4/30-gestion-projet" >}})
- Rob Pike, *Notes on Programming in C* (1989) : contient les « 5 règles de
  programmation » de Pike, dont la règle 5 sur la primauté des structures de
  données → [Module 2, Survol rapide de la programmation]({{< ref "/docs/module2/10-programmation" >}})
- Edsger Dijkstra, *Go To Statement Considered Harmful* (1968) : plaidoyer pour
  la programmation structurée → [Module 1, Perspective historique]({{< ref "/docs/module1/10-historique" >}})
- Edsger Dijkstra, *On the foolishness of "natural language programming"*
  (EWD667, 1979) : critique de l'idée de programmer en langage naturel,
  l'ambiguïté comme problème fondamental →
  [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})
- Martin Fowler, *Continuous Integration* (2006) : article de référence sur
  l'intégration continue → [Module 2, L'intégration continue]({{< ref "/docs/module2/50-ci" >}})
- Roy Fielding, *Architectural Styles and the Design of Network-based Software
  Architectures* (thèse de doctorat, 2000) : définition de REST →
  [Module 3, Les APIs]({{< ref "/docs/module3/20-apis" >}})
- Roy Fielding, *REST APIs must be hypertext-driven* (billet de blog, 2008) :
  critique des APIs « REST » qui n'implémentent pas HATEOAS →
  [Module 3, Les APIs]({{< ref "/docs/module3/20-apis" >}})
- Peter Deutsch et al., *Fallacies of Distributed Computing* (1994) : huit
  hypothèses fausses sur les systèmes distribués →
  [Module 3, Les APIs]({{< ref "/docs/module3/20-apis" >}})
- Leonard Richardson, *Richardson Maturity Model* : classification des APIs
  REST en quatre niveaux de maturité →
  [Module 3, Les APIs]({{< ref "/docs/module3/20-apis" >}})
- Jim Gray, contributions aux transactions et bases de données (prix Turing
  1998) : formalisation des propriétés ACID →
  [Module 3, Les données (stockage)]({{< ref "/docs/module3/40-données/20-stockage" >}})
- Gerard Salton, *A Theory of Indexing* (1975) et le système SMART : père de
  l'*information retrieval*, concepts fondateurs de TF-IDF et de l'index inversé →
  [Module 3, Les données (au-delà des BD)]({{< ref "/docs/module3/40-données/30-au-delà" >}})
- Google, *Bigtable: A Distributed Storage System for Structured Data* (2006) :
  article fondateur du stockage orienté colonnes à grande échelle →
  [Module 3, Les données (stockage)]({{< ref "/docs/module3/40-données/20-stockage" >}})
- Tomas Mikolov et al., *Efficient Estimation of Word Representations in Vector
  Space* (2013) : introduction de Word2Vec et des embeddings de mots →
  [Module 3, Les données (stockage)]({{< ref "/docs/module3/40-données/20-stockage" >}}),
  [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})
- Marc Shapiro, Nuno Preguiça, Carlos Baquero et Marek Zawirski, *Conflict-free
  Replicated Data Types* (2011) : formalisation des CRDTs →
  [Module 3, Les données (au-delà des BD)]({{< ref "/docs/module3/40-données/30-au-delà" >}})
- Satoshi Nakamoto, *Bitcoin: A Peer-to-Peer Electronic Cash System* (2008) :
  livre blanc introduisant la blockchain et le consensus distribué →
  [Module 3, Les données (au-delà des BD)]({{< ref "/docs/module3/40-données/30-au-delà" >}})
- Hirotaka Takeuchi et Ikujiro Nonaka, *The New New Product Development Game*
  (Harvard Business Review, 1986) : article fondateur qui introduit l'approche
  « rugby » du développement de produit, inspiration directe de Scrum →
  [Module 4, Scrum]({{< ref "/docs/module4/20-agile/10-scrum" >}})
- Dave Thomas, *Agile is Dead (Long Live Agility)* (billet de blog, 2014) :
  critique de la récupération commerciale du mot "agile" par un des signataires
  du manifeste →
  [Module 4, L'agilité]({{< ref "/docs/module4/20-agile" >}})
- Jez Humble et David Farley, *Continuous Delivery* (2010) : automatisation
  complète du chemin entre le commit et la production, concept du deployment
  pipeline →
  [Module 5, Comment je le déploie ?]({{< ref "/docs/module5/20-deploiement" >}})
- John Allspaw, *Blameless PostMortems and a Just Culture* (2012) :
  formalisation de l'approche non punitive après les incidents, inspirée de
  l'aviation et de la médecine →
  [Module 5, Que faire quand ça casse ?]({{< ref "/docs/module5/40-incidents" >}})
- Netflix, *Principles of Chaos Engineering* (2014) : formalisation du chaos
  engineering, expériences en production pour tester la résilience →
  [Module 5, Que faire quand ça casse ?]({{< ref "/docs/module5/40-incidents" >}})
- Eric Brewer, *Towards Robust Distributed Systems* (keynote PODC, 2000) :
  formulation du théorème CAP (Consistency, Availability, Partition tolerance),
  prouvé formellement par Seth Gilbert et Nancy Lynch (2002) →
  [Module 5, Est-ce que ça va tenir la charge ?]({{< ref "/docs/module5/60-scalabilite" >}})
- Alan Turing, *Computing Machinery and Intelligence* (1950) : article fondateur
  posant la question "Can machines think?" et proposant le test de Turing →
  [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})
- Yoshua Bengio, Réjean Ducharme, Pascal Vincent et Christian Jauvin,
  *A Neural Probabilistic Language Model* (2003) : introduction des word
  embeddings appris conjointement avec un modèle de langage neuronal, fondation
  des LLM modernes →
  [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})
- Dzmitry Bahdanau, Kyunghyun Cho et Yoshua Bengio, *Neural Machine Translation
  by Jointly Learning to Align and Translate* (2014) : introduction du mécanisme
  d'attention, fondation du Transformer →
  [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})
- Ashish Vaswani et al., *Attention is All You Need* (2017) : introduction de
  l'architecture Transformer, brique de base de tous les LLM modernes →
  [Module 6, Le développement assisté par IA]({{< ref "/docs/module6/60-ia" >}})
- Richard Gabriel, *Worse is Better* (1989) : essai opposant la philosophie
  "the right thing" (MIT/Lisp) à "worse is better" (Unix/C), la simplicité
  d'implémentation l'emporte sur la perfection →
  [Module 6, Le métier de développeur]({{< ref "/docs/module6/50-metier" >}})