---
title: "Survol historiquee des jalons du GL"
weight: 60
---

# Les jalons historiques du génie logiciel

L'histoire du génie logiciel est le récit d'une transition : d'un "artisanat" manuel vers une automatisation à l'échelle industrielle. Cette évolution a été rythmée par la nécessité constante de dompter une complexité croissante et de répondre aux besoins changeants de la société.

---

## 1. L'ère des pionniers (Années 1940 – 1967)
*Focus : Maîtriser le matériel. La programmation est alors perçue comme une extension de l'ingénierie électrique.*

* **1952 : Le premier compilateur (Technologie)**
    Grace Hopper a développé le **système A-0**, le premier outil capable de traduire des instructions mathématiques en code machine. Avant cela, les programmeurs devaient écrire manuellement en binaire ou en assembleur. Cette invention a ouvert la voie à l'abstraction, permettant aux humains de communiquer avec les machines dans un langage plus proche du leur.
* **1957 : FORTRAN (Langage)**
    Créé par John Backus chez IBM, FORTRAN (Formula Translation) est le premier langage de haut niveau largement adopté. Il a prouvé qu'un langage compilé pouvait être aussi efficace que du code écrit à la main, tout en rendant les programmes beaucoup plus lisibles et portables d'une machine à une autre.
* **1958 : LISP (Tendance/Technologie)**
    Inventé par John McCarthy pour la recherche en intelligence artificielle, LISP a introduit des concepts révolutionnaires comme les fonctions récursives, le typage dynamique et le "garbage collection" (gestion automatique de la mémoire). Il reste l'un des langages les plus influents sur la conception des langages modernes.
* **1964 : IBM System/360 (Système d'exploitation)**
    IBM a lancé la première famille d'ordinateurs utilisant la même architecture. Pour la première fois, un logiciel écrit pour une petite machine pouvait fonctionner sur une plus grande sans être réécrit. Cela a forcé la création de l'OS/360, l'un des premiers projets logiciels massifs, illustrant pour la première fois les défis de la gestion d'équipes de développement géantes.

---

## 2. La naissance du génie logiciel (1968 – 1982)
*Focus : Résoudre la "crise du logiciel". Les projets sont systématiquement en retard, hors budget et truffés de bugs.*

* **1968 : La conférence de l'OTAN (Méthode)**
    Le terme "génie logiciel" (Software Engineering) est officiellement consacré lors de cette conférence à Garmisch, en Allemagne. L'objectif était de transformer la création de logiciels, alors perçue comme un art mystérieux et imprévisible, en une discipline d'ingénierie rigoureuse, basée sur des processus théoriques et reproductibles.
* **1970 : Le modèle en cascade / Waterfall (Méthode)**
    Winston Royce a décrit le premier modèle de processus séquentiel (analyse, conception, codage, tests). Bien que Royce ait lui-même prévenu que ce modèle était risqué sans itérations, il est devenu la norme industrielle pendant des décennies car il offrait une structure rassurante pour la gestion de projet traditionnelle.
* **1972 : C et UNIX (Technologie)**
    Dennis Ritchie crée le **langage C** et Ken Thompson développe **UNIX**. Ce duo a permis d'écrire des systèmes d'exploitation performants sans dépendre du langage assembleur spécifique à un processeur. C est devenu le "latin" de l'informatique, servant de fondation à presque tous les systèmes d'exploitation et langages modernes.
* **1975 : "The Mythical Man-Month" (Tendance)**
    Fred Brooks a publié cet ouvrage fondateur basé sur son expérience chez IBM. Il y formule la **Loi de Brooks** : "Ajouter de la main-d'œuvre à un projet logiciel en retard ne fait que le retarder davantage". Ce livre a déplacé l'attention des problèmes purement techniques vers les problèmes de communication et de structure humaine.

---

## 3. Maîtriser la complexité et le PC (1983 – 1994)
*Focus : Favoriser la réutilisation du code et gérer l'explosion de l'informatique personnelle.*

* **1983 : C++ (Langage)**
    Bjarne Stroustrup a ajouté des "classes" au langage C, popularisant la **programmation orientée objet (POO)**. Cette approche permet de structurer le code en modules réutilisables (objets), ce qui est devenu indispensable pour gérer les interfaces graphiques complexes et les logiciels de bureau des nouveaux PC.
* **1985 : Windows et les interfaces graphiques (Système d'exploitation)**
    Avec le lancement de Windows 1.0 (puis le succès massif de la version 3.0), Microsoft a généralisé l'interface graphique (GUI) sur PC. Pour les ingénieurs, cela a marqué un tournant : il ne s'agissait plus de programmer des flux linéaires, mais des systèmes "dirigés par les événements" (event-driven programming), où le logiciel attend et réagit aux actions de l'utilisateur (clics, mouvements de souris).
* **1985 : Le modèle en spirale (Méthode)**
    Barry Boehm propose un modèle basé sur la gestion des risques. Contrairement à la cascade, la spirale encourage des cycles répétitifs de prototypage et d'évaluation. C'est le premier pas majeur vers une reconnaissance que le logiciel doit évoluer par essais et erreurs plutôt que par un plan parfait initial.



* **1991 : Linux et le Web (Technologie/Tendance)**
    Linus Torvalds publie le noyau Linux, prouvant que le modèle de développement "Open Source" pouvait produire des logiciels de qualité industrielle. Simultanément, Tim Berners-Lee invente le World Wide Web, transformant le logiciel en un outil de réseau mondial plutôt qu'une application isolée.

---

## 4. La révolution agile et Internet (1995 – 2009)
*Focus : Vitesse, flexibilité et passage au navigateur comme plateforme principale.*

* **1995 : Java et JavaScript (Langages)**
    Java a introduit la promesse "Écrire une fois, exécuter partout" grâce à sa machine virtuelle, tandis que JavaScript a permis de rendre le Web interactif. Ensemble, ils ont déplacé le centre de gravité du logiciel des machines locales vers les navigateurs et les serveurs distants.
* **2001 : Le manifeste agile (Méthode)**
    Dix-sept experts se réunissent pour signer un texte qui privilégie "les individus et leurs interactions" sur les processus et les outils. C'est un rejet massif des méthodes lourdes au profit de cycles de livraison courts et d'une adaptation constante aux besoins changeants des clients.
* **2006 : AWS et le cloud computing (Technologie)**
    Le lancement d'Amazon Web Services a transformé l'infrastructure en logiciel (Infrastructure-as-Code). Les développeurs n'ont plus besoin d'attendre des mois pour des serveurs physiques ; ils peuvent louer de la puissance de calcul à la demande, favorisant l'émergence des architectures en microservices.
* **2009 : Node.js (Technologie)**
    En permettant à JavaScript de s'exécuter côté serveur, Node.js a unifié le développement web. Les développeurs peuvent désormais utiliser un seul langage pour l'ensemble de la pile applicative (Full-stack), simplifiant radicalement les équipes et les processus de développement.

---

## 5. L'ingénierie continue et l'IA (2010 – présent)
*Focus : Automatisation totale, résilience et assistance par l'intelligence artificielle.*

* **2010 : L'essor du DevOps (Tendance)**
    Le DevOps brise le mur entre le développement (Dev) et l'exploitation (Ops). L'objectif est l'intégration et le déploiement continus (**CI/CD**), permettant à des entreprises de mettre à jour leur logiciel des dizaines de fois par jour sans interruption de service.



* **2013 : Docker et les conteneurs (Technologie)**
    Docker a popularisé la conteneurisation, permettant d'empaqueter une application avec toutes ses dépendances dans une unité isolée. Cela a résolu définitivement le problème du "ça marche sur ma machine", garantissant qu'un logiciel fonctionne à l'identique dans tous les environnements.
* **2017 : Modèles transformers et IA (Tendance)**
    La publication du papier "Attention Is All You Need" a posé les bases des grands modèles de langage (LLM). Aujourd'hui, l'IA change le métier d'ingénieur : elle ne se contente plus d'être intégrée aux produits, elle aide à générer, corriger et documenter le code via des assistants comme Copilot.
* **Présent : Low-code et no-code (Tendance)**
    Un mouvement visant à démocratiser la création logicielle. En utilisant des interfaces visuelles pour construire des applications, ces outils permettent aux experts métier de créer leurs propres solutions, réduisant ainsi la dépendance historique envers les seuls ingénieurs logiciels pour les besoins simples.

---

### Tableau récapitulatif

| Époque | Langage phare | Système/OS phare | Méthode dominante |
| :--- | :--- | :--- | :--- |
| **Pionniers** | FORTRAN | IBM OS/360 | Artisanale |
| **Crise/Structure** | C | UNIX | Cascade (Waterfall) |
| **Objet / PC** | C++ | Windows | Spirale / Itératif |
| **Agile/Web** | Java / JS | Linux | Agile / Scrum |
| **DevOps/IA** | Go / Rust | Cloud (AWS/Azure) | DevOps / CI-CD |