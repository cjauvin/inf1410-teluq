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

- Gerald Weinberg, *The Psychology of Computer Programming* (1971) : approche
  psychologique du développement logiciel, introduction de l'*egoless
  programming* → [Module 2, Introduction]({{< ref "/docs/module2" >}}),
  [Module 2, L'intégration continue]({{< ref "/docs/module2/50-ci" >}}),
  [Module 4, Scrum]({{< ref "/docs/module4/20-agile/10-scrum" >}})
- Fred Brooks, *The Mythical Man-Month* (1975) : réflexions sur la gestion de
  grands projets logiciels, dont la célèbre « loi de Brooks » → [Module 1, Perspective historique]({{< ref "/docs/module1/10-historique" >}}),
  [Module 6, L'économie du logiciel]({{< ref "/docs/module6/20-economie" >}})
- Andrew Hunt et David Thomas, *The Pragmatic Programmer* (1999) : conseils
  pratiques pour le développeur, origine du principe DRY → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- Kent Beck, *Extreme Programming Explained* (1999) : manifeste de l'XP, origine
  de YAGNI et du TDD → [Module 1, Perspective historique]({{< ref "/docs/module1/10-historique" >}})
- Robert C. Martin, *Agile Software Development: Principles, Patterns, and
  Practices* (2003) : formalisation des principes SOLID, acronyme suggéré par
  Michael Feathers → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
- Robert C. Martin, *Clean Code* (2008) : principes de conception et de
  lisibilité du code → [Module 3, Architecture et modularité]({{< ref "/docs/module3/10-architecture" >}})
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

- Edsger W. Dijkstra, *Cooperating Sequential Processes* (EWD123, 1965)
  [[texte](https://www.cs.utexas.edu/~EWD/ewd01xx/EWD123.PDF)]&nbsp;: le problème
  de l'exclusion mutuelle, le sémaphore qui le résout, et le dîner des
  philosophes qui montre ce que les verrous cassent à leur tour → [Module 2, Ce qui casse]({{< ref "/docs/module2/concurrence/30-ce-qui-casse" >}})
- C. A. R. Hoare, *Communicating Sequential Processes* (CACM, 1978)
  [[texte](https://www.cs.cmu.edu/~crary/819-f09/Hoare78.pdf)]&nbsp;: des tâches
  qui ne partagent rien et ne s'échangent que des messages. Baptise le dîner
  des philosophes, et fonde la lignée qui mène à Go → [Module 2, Ce qui casse]({{< ref "/docs/module2/concurrence/30-ce-qui-casse" >}}),
  [Module 2, Ne pas partager]({{< ref "/docs/module2/concurrence/40-ne-pas-partager" >}})
- Jim Gray, *The Transaction Concept: Virtues and Limitations* (VLDB, 1981)
  [[texte](https://jimgray.azurewebsites.net/papers/thetransactionconcept.pdf)]&nbsp;:
  la transaction comme réponse de la base de données au même problème que le
  verrou résout dans le programme → [Module 2, Ce qui casse]({{< ref "/docs/module2/concurrence/30-ce-qui-casse" >}}),
  [Module 3, Les données (stockage)]({{< ref "/docs/module3/40-données/20-stockage" >}})
- Edward A. Lee, *The Problem with Threads* (IEEE Computer, mai 2006) [[DOI](https://doi.org/10.1109/MC.2006.180)]&nbsp;: les
  threads détruisent le déterminisme, c'est-à-dire ce qui permet de comprendre
  un programme en le lisant. À l'appui, son propre projet Ptolemy, relu par des
  spécialistes de la concurrence et couvert à 100&nbsp;% par des tests, resté quatre
  ans sans incident avant de se bloquer le 26 avril 2004 sur un interblocage
  présent depuis le premier jour →
  [Module 2, Concurrence et parallélisme]({{< ref "/docs/module2/concurrence" >}}),
  [Module 2, Ce qui casse]({{< ref "/docs/module2/concurrence/30-ce-qui-casse" >}})
- Carl Hewitt, Peter Bishop et Richard Steiger, *A Universal Modular ACTOR
  Formalism for Artificial Intelligence* (IJCAI, 1973)
  [[texte](https://www.ijcai.org/Proceedings/73/Papers/027B.pdf)]&nbsp;: l'acteur,
  un état que lui seul touche et une boîte aux lettres, cinq ans avant CSP et
  avec des messages asynchrones → [Module 2, Ne pas partager]({{< ref "/docs/module2/concurrence/40-ne-pas-partager" >}})
- Joe Armstrong, *Making Reliable Distributed Systems in the Presence of
  Software Errors* (thèse, KTH, 2003)
  [[texte](https://erlang.org/download/armstrong_thesis_2003.pdf)]&nbsp;: Erlang
  expliqué par son auteur, let it crash et les superviseurs. À lire aussi pour
  ce qu'elle dit des fameux neuf neuf de l'AXD301, dont la seule source était
  une présentation PowerPoint → [Module 2, Ne pas partager]({{< ref "/docs/module2/concurrence/40-ne-pas-partager" >}})
- Andrew Gerrand, *Share Memory By Communicating* (blogue de Go, 2010)
  [[texte](https://go.dev/blog/codelab-share)]&nbsp;: la formule de Go, ne
  communiquez pas en partageant la mémoire, partagez la mémoire en
  communiquant → [Module 2, Ne pas partager]({{< ref "/docs/module2/concurrence/40-ne-pas-partager" >}})
- Rich Hickey, *Clojure Rationale* [[texte](https://clojure.org/about/rationale)]&nbsp;:
  l'état mutable comme « désastre pour la concurrence », et l'immutabilité qui
  permet de « partager librement entre threads » → [Module 2, Ne pas partager]({{< ref "/docs/module2/concurrence/40-ne-pas-partager" >}})
- *The Rust Programming Language*, chapitre *Fearless Concurrency*
  [[texte](https://doc.rust-lang.org/book/ch16-00-concurrency.html)]&nbsp;: les
  erreurs de concurrence comme erreurs de compilation plutôt que d'exécution → [Module 2, Ne pas partager]({{< ref "/docs/module2/concurrence/40-ne-pas-partager" >}})
- QNX, *System Architecture*, chapitres sur le micronoyau et la communication
  entre processus
  [[noyau](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.sys_arch/topic/kernel.html),
  [messages](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.sys_arch/topic/ipc.html)]&nbsp;:
  un système d'exploitation canadien où tout, jusqu'aux systèmes de fichiers,
  s'exécute hors du noyau et communique par messages synchrones → [Module 2, Ne pas partager]({{< ref "/docs/module2/concurrence/40-ne-pas-partager" >}})
- Sam Gross, *PEP 703&nbsp;: Making the Global Interpreter Lock Optional in CPython*
  (2023) [[texte](https://peps.python.org/pep-0703/)]&nbsp;: la proposition qui défait un compromis vieux de trente ans, acceptée
  puis livrée en variante expérimentale. Le même code y devient trois fois plus
  rapide en threads, et révèle du même coup des bogues que le verrou masquait →
  [Module 2, Processus et threads]({{< ref "/docs/module2/concurrence/20-processus-et-threads" >}})
- Gene Amdahl, *Validity of the Single Processor Approach to Achieving Large
  Scale Computing Capabilities* (AFIPS, 1967) [[texte](https://inst.eecs.berkeley.edu/~n252/paper/Amdahl.pdf)]&nbsp;: quatre pages qui
  fixent le plafond du parallélisme, la part séquentielle d'un programme
  bornant le gain quel que soit le nombre de processeurs → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/concurrence/10-pourquoi" >}})
- Gordon Moore, *Cramming More Components onto Integrated Circuits* (1965) [[texte](https://www.cs.utexas.edu/~fussell/courses/cs352h/papers/moore.pdf), [DOI](https://doi.org/10.1109/N-SSC.2006.4785860)]&nbsp;:
  l'observation, sur deux pages, que le nombre de composants gravés sur une
  puce double à intervalle régulier. Moore y parle de quantité, jamais de
  vitesse → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/concurrence/10-pourquoi" >}})
- Robert Dennard et coll., *Design of Ion-Implanted MOSFET's with Very Small
  Physical Dimensions* (1974) [[DOI](https://doi.org/10.1109/JSSC.1974.1050511)]&nbsp;: la loi de proportionnalité qui, en gardant la
  densité thermique constante quand les transistors rétrécissent, a converti la
  loi de Moore en gain de vitesse pendant trente ans → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/concurrence/10-pourquoi" >}})
- Herb Sutter, *The Free Lunch Is Over* (2005) [[texte](http://www.gotw.ca/publications/concurrency-ddj.htm)]&nbsp;: le moment où l'accélération
  cesse d'être offerte par le matériel et devient un travail de programmeur →
  [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/concurrence/10-pourquoi" >}})
- Rob Pike, *Concurrency Is Not Parallelism* (conférence, 2012) [[vidéo et diapositives](https://go.dev/blog/waza-talk)]&nbsp;: la concurrence
  est une manière de structurer un programme, le parallélisme une manière de
  l'exécuter → [Module 2, Pourquoi la concurrence]({{< ref "/docs/module2/concurrence/10-pourquoi" >}})
- Dan Kegel, *The C10K problem* (1999, mis à jour jusqu'en 2014)
  [[texte](http://www.kegel.com/c10k.html)]&nbsp;: la page qui pose le problème
  des dix mille connexions, et la division qui condamne le thread par client → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- Node.js, *About Node.js* [[texte](https://nodejs.org/en/about)]&nbsp;: Node
  décrit par lui-même, une boucle d'événements comme construction de
  l'environnement d'exécution plutôt que comme bibliothèque → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- Ryan Dahl, *Porting Node to Windows With Microsoft's Help* (blogue de Node,
  2011) [[texte](https://nodejs.org/en/blog/uncategorized/porting-node-to-windows-with-microsofts-help)]&nbsp;:
  le portage vers l'API IOCP de Windows, d'où est née libuv → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- libuv, *Design overview* [[texte](https://docs.libuv.org/en/v1.x/design.html)]&nbsp;:
  la boucle au centre, liée à un seul thread, et les noms de Kegel, epoll,
  kqueue, IOCP, derrière une seule interface. Reprise par uvloop pour Python → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- Barbara Liskov et Liuba Shrira, *Promises&nbsp;: Linguistic Support for
  Efficient Asynchronous Procedure Calls in Distributed Systems* (PLDI, 1988)
  [[DOI](https://doi.org/10.1145/53990.54016)]&nbsp;: le mot et l'idée, un objet
  qui représente un résultat pas encore arrivé, pour les systèmes distribués,
  vingt-sept ans avant leur entrée dans JavaScript → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- *Promises/A+* [[texte](https://promisesaplus.com/)]&nbsp;: le standard
  communautaire des promesses JavaScript, dont la première phrase est la
  définition à retenir → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- Don Syme, Tomas Petříček et Dmitry Lomov, *The F# Asynchronous Programming
  Model* (PADL, 2011) [[DOI](https://doi.org/10.1007/978-3-642-18378-2_15)]&nbsp;:
  l'origine d'`async` et `await`, chez Microsoft, avant C#, Python et
  JavaScript → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- Guido van Rossum, *PEP 3156&nbsp;: Asynchronous IO Support Rebooted&nbsp;: the
  « asyncio » Module* (2012) [[texte](https://peps.python.org/pep-3156/)]&nbsp;:
  la boucle d'événements de la bibliothèque standard, trois ans avant les
  mots-clés qui la rendent agréable → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- Yury Selivanov, *PEP 492&nbsp;: Coroutines with async and await syntax* (2015)
  [[texte](https://peps.python.org/pep-0492/)]&nbsp;: les coroutines comme
  fonctionnalité native de Python, clairement séparées des générateurs → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- Python, documentation du module *asyncio*
  [[texte](https://docs.python.org/3/library/asyncio.html)]&nbsp;: « convient
  souvent parfaitement au code I/O-bound », et la fondation des serveurs web
  Python d'aujourd'hui → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- FastAPI, *Concurrency and async / await*
  [[texte](https://fastapi.tiangolo.com/async/)]&nbsp;: quand écrire `async def`,
  expliqué avec des hamburgers, par le framework qui en dépend → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
- Node.js, documentation du module *worker_threads*
  [[texte](https://nodejs.org/api/worker_threads.html)]&nbsp;: des threads
  « utiles pour les opérations intensives en calcul », et « peu utiles » pour
  les entrées-sorties, où la boucle fait mieux → [Module 2, Ne jamais bloquer]({{< ref "/docs/module2/concurrence/50-ne-jamais-bloquer" >}})
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
- Daniel Lemire, *Python sets and dictionaries can have quadratic-time
  performance* (blogue, 2026) [[texte](https://lemire.me/blog/2026/09/03/python-sets-and-dictionaries-can-have-quadratic-time-performance/)]&nbsp;:
  un professeur de la TÉLUQ montre, mesures à l'appui, que le temps constant
  des tables de hachage est un modèle, et comment le faire mentir avec des clés
  bien choisies → [Module 2, Survol rapide de la programmation]({{< ref "/docs/module2/10-programmation" >}})
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