---
title: "Le développement assisté par IA"
weight: 60
slug: "ia"
---

# Le développement assisté par IA

La section précédente se terminait sur une question ouverte : l'IA générative
sera-t-elle enfin la silver bullet que Brooks jugeait impossible en 1986 ? La
question mérite d'être posée sérieusement, parce que quelque chose de
fondamentalement différent est en train de se passer. Depuis 2021, des outils
capables de générer du code à partir de descriptions en langage naturel ont
commencé à transformer le quotidien des développeurs. Pas comme une curiosité de
laboratoire, mais comme un changement concret dans la manière de travailler :
en 2024, GitHub rapportait que plus de la moitié du code sur sa plateforme était
écrit avec l'assistance de Copilot. Que l'on soit enthousiaste ou sceptique, il
est difficile de nier que le développement logiciel est en train de vivre sa
transformation la plus profonde depuis l'invention des langages de haut niveau.
Pour comprendre ce qui se passe, il faut d'abord comprendre d'où vient cette
technologie.

## D'où vient l'intelligence artificielle

### L'IA symbolique (années 1950-1980)

L'idée de créer des machines capables de "penser" est aussi vieille que
l'informatique elle-même. En 1950, Alan Turing publiait "Computing Machinery
and Intelligence", l'article qui posait la question "Can machines think?" et
proposait le fameux test de Turing comme critère opérationnel. Six ans plus tard,
en 1956, une conférence au Dartmouth College réunissait John McCarthy, Marvin
Minsky, Claude Shannon et d'autres pionniers pour ce qui est considéré comme
l'acte de naissance officiel de l'intelligence artificielle comme discipline. Le
terme lui-même, "artificial intelligence", a été inventé par McCarthy pour
l'occasion. L'approche dominante de cette époque était symbolique : l'idée que
l'intelligence pouvait être reproduite en manipulant des symboles selon des
règles logiques, comme un programme qui enchaîne des déductions. Les systèmes
experts des années 1970 et 1980 représentent l'aboutissement de cette approche :
des programmes qui codifiaient les connaissances d'un spécialiste humain sous
forme de règles "si... alors..." pour diagnostiquer des maladies, configurer des
ordinateurs ou analyser des données géologiques. Certains ont eu un succès
commercial réel, mais tous partageaient une limitation fondamentale : il fallait
que des humains programment explicitement chaque règle. Le système ne pouvait
rien savoir qu'on ne lui avait pas dit. Cette approche a connu deux "hivers de
l'IA" (AI winters), des périodes de désillusion et de coupures de financement,
quand les promesses initiales se sont heurtées à la réalité : l'intelligence
humaine ne se réduit pas à un ensemble de règles logiques, et les problèmes du
monde réel résistent à la formalisation complète.

Il serait toutefois trompeur de conclure que l'IA symbolique a échoué. En
réalité, une grande partie de ses idées se sont fondues dans la programmation
ordinaire, au point qu'on ne les associe plus à l'"intelligence artificielle".
Les arbres de décision, la recherche dans des graphes, les algorithmes de
planification, les moteurs de règles : tout cela vient directement de la
recherche en IA des années 1960 et 1970. Les compilateurs que nous utilisons
chaque jour reposent sur des techniques de parsing et d'analyse formelle issues
de cette tradition. Les systèmes de types statiques, la vérification de
contraintes, même l'autocomplétion classique dans un IDE comme Intellisense
de Microsoft (1996) sont des héritiers de l'approche symbolique. L'IA symbolique
n'a pas disparu : elle est devenue invisible à force de succès, absorbée dans
les fondations mêmes de la programmation moderne.

### Le machine learning (années 1990-2000)

L'idée alternative à l'IA symbolique existait dès les débuts du domaine, mais
elle a mis des décennies à porter ses fruits. Plutôt que de programmer
explicitement des règles, pourquoi ne pas laisser la machine les découvrir
elle-même à partir d'exemples ? C'est le principe du machine learning
(apprentissage automatique) : on fournit au système des données étiquetées (des
images avec leurs légendes, des courriels marqués comme spam ou non, des
transactions frauduleuses ou légitimes) et un algorithme ajuste ses paramètres
internes jusqu'à ce qu'il parvienne à reproduire les bonnes réponses. Le
perceptron, un modèle de neurone artificiel proposé par Frank Rosenblatt en
1958, avait déjà exploré cette voie, mais ses limitations, démontrées par Minsky
et Papert en 1969, avaient contribué au premier hiver de l'IA. Il a fallu
attendre les années 1980 et 1990 pour que les réseaux de neurones reviennent en
force, grâce notamment à l'algorithme de rétropropagation (backpropagation)
popularisé par Rumelhart, Hinton et Williams en 1986, qui permettait
d'entraîner des réseaux à plusieurs couches. Les années 1990 et 2000 ont vu le
machine learning s'imposer progressivement dans des applications concrètes :
filtres anti-spam, systèmes de recommandation, reconnaissance optique de
caractères, traduction statistique. Mais les réseaux de neurones de cette époque
restaient modestes en taille, limités par la puissance de calcul disponible, et
ils étaient souvent surpassés par des méthodes statistiques plus simples comme
les machines à vecteurs de support (SVM). Le vrai changement allait venir d'une
combinaison de trois facteurs : des données massives (le web), du matériel
puissant (les GPU, des processeurs graphiques détournés pour le calcul
scientifique) et des architectures de réseaux de neurones plus profondes. C'est
le deep learning.

### Le deep learning et Montréal (années 2010)

Le deep learning (apprentissage profond) désigne l'utilisation de réseaux de
neurones comportant de nombreuses couches successives, chacune apprenant des
représentations de plus en plus abstraites des données. Un réseau de
reconnaissance d'images, par exemple, apprend dans ses premières couches à
détecter des contours et des textures, puis dans les couches intermédiaires à
reconnaître des formes (un oeil, une roue), et dans les couches profondes à
identifier des objets complets (un visage, une voiture). L'idée n'était pas
nouvelle, mais pendant longtemps, on ne parvenait pas à entraîner efficacement
des réseaux profonds : les gradients utilisés pour ajuster les paramètres
s'évanouissaient ou explosaient à mesure qu'on ajoutait des couches. Un petit
groupe de chercheurs a persisté malgré le scepticisme de la communauté, et
trois d'entre eux ont joué un rôle déterminant : Geoffrey Hinton (Université de
Toronto), Yann LeCun (Bell Labs puis NYU) et Yoshua Bengio (Université de
Montréal). Ils recevront ensemble le prix Turing en 2018, souvent décrit comme
le "prix Nobel de l'informatique", pour leurs travaux sur le deep learning.

Le rôle de Montréal dans cette histoire mérite d'être souligné. Yoshua Bengio
est arrivé à l'Université de Montréal en 1993 et y a fondé ce qui allait
devenir le MILA (aujourd'hui l'Institut québécois d'intelligence artificielle),
le plus grand centre de recherche académique en deep learning au monde. Pendant
les années 2000, alors que la plupart des départements d'informatique
considéraient les réseaux de neurones comme une voie sans issue, Bengio et ses
étudiants ont continué à publier des travaux fondamentaux. Montréal est devenue
un pôle d'attraction mondiale pour la recherche en IA, attirant des laboratoires
de Google, Meta, Microsoft et Samsung, et engendrant un écosystème de startups
spécialisées. Cette concentration de talent n'est pas un accident : elle
résulte directement de la persévérance d'un chercheur et de l'université qui
l'a soutenu pendant les années de vaches maigres.

Le moment charnière est arrivé en 2012. Lors de la compétition ImageNet, un
défi annuel de classification d'images, Alex Krizhevsky, un étudiant de Hinton
à Toronto, a soumis AlexNet, un réseau de neurones profond entraîné sur des
GPU. AlexNet a écrasé la compétition, réduisant le taux d'erreur de 26 % à
15 %, un bond sans précédent. Ce résultat a forcé le reste de la communauté à
prendre le deep learning au sérieux. En quelques années, les réseaux profonds
ont atteint puis dépassé la performance humaine dans des tâches de vision par
ordinateur, de reconnaissance vocale et de traduction automatique. Google,
Facebook, Amazon et les autres géants technologiques se sont lancés dans une
course au recrutement de chercheurs en deep learning, et l'IA est passée d'un
champ de recherche marginal à la technologie la plus convoitée de la décennie.

### Des modèles de langage aux LLM (2003-2023)

Le deep learning a d'abord triomphé dans la vision par ordinateur, mais c'est
son application au langage qui allait transformer le développement logiciel. Et
cette histoire commence, encore une fois, à Montréal. En 2003, Yoshua Bengio et
ses collègues ont publié "A Neural Probabilistic Language Model", un article qui
proposait une idée en apparence simple mais aux conséquences profondes : plutôt
que de traiter les mots comme des symboles discrets et arbitraires (l'approche
dominante en linguistique computationnelle), on pouvait représenter chaque mot
comme un vecteur dans un espace continu, un point dans un espace mathématique
à plusieurs centaines de dimensions. Dans cet espace, les mots ayant des sens
similaires se retrouvent proches les uns des autres. Le modèle apprenait ces
représentations (appelées *word embeddings*) en même temps qu'il apprenait à
prédire le mot suivant dans une phrase. Cette idée a ouvert la voie à une
décennie de progrès. En 2013, Tomas Mikolov et son équipe chez Google ont
publié Word2Vec, une méthode efficace pour apprendre des embeddings à grande
échelle, et les résultats avaient quelque chose de fascinant : les vecteurs
capturaient des relations sémantiques. L'exemple devenu célèbre est que le
vecteur "roi" moins "homme" plus "femme" donnait un résultat proche de "reine",
comme si le modèle avait appris, sans supervision explicite, des concepts
abstraits comme le genre et la royauté.

L'étape suivante est venue, encore une fois, du MILA. En 2014, Dzmitry
Bahdanau, Kyunghyun Cho et Yoshua Bengio ont publié "Neural Machine Translation
by Jointly Learning to Align and Translate", un article qui introduisait le
mécanisme d'attention dans le contexte de la traduction automatique. Le problème
était le suivant : les modèles de traduction neuronaux de l'époque lisaient
toute la phrase source et la compressaient en un seul vecteur de taille fixe
avant de générer la traduction. Pour des phrases longues, ce goulot
d'étranglement faisait perdre de l'information. Le mécanisme d'attention
permettait au modèle, à chaque étape de la génération, de "porter attention" à
différentes parties de la phrase source, en pondérant dynamiquement l'importance
de chaque mot. Les résultats étaient remarquables, et l'idée s'est rapidement
propagée bien au-delà de la traduction.

C'est en généralisant cette idée que Google a produit la vraie révolution
architecturale, en 2017, avec un article intitulé "Attention is All You Need",
qui introduisait le Transformer.
Les modèles de langage précédents traitaient le texte de manière séquentielle,
mot par mot, ce qui les rendait lents à entraîner et incapables de capturer
efficacement les relations entre des mots éloignés dans une phrase. Le
mécanisme d'attention du Transformer résolvait ce problème en permettant au
modèle de "regarder" simultanément tous les mots d'une séquence et de pondérer
leur importance relative. Cette architecture était aussi massivement
parallélisable, ce qui permettait de l'entraîner sur des quantités de texte
sans précédent en exploitant la puissance des GPU. Le Transformer est devenu la
brique de base de presque tous les modèles de langage modernes.

OpenAI a été parmi les premiers à exploiter cette architecture à grande échelle.
GPT (Generative Pre-trained Transformer), publié en 2018, puis GPT-2 en 2019
et GPT-3 en 2020, ont montré qu'en augmentant la taille du modèle (le nombre
de paramètres) et la quantité de données d'entraînement, on obtenait des
comportements qualitativement nouveaux. GPT-3, avec ses 175 milliards de
paramètres entraînés sur une portion massive du web, pouvait rédiger des textes
cohérents, répondre à des questions, traduire entre langues, et, de manière
remarquable, écrire du code. Ces comportements n'avaient pas été programmés
explicitement : ils émergeaient de l'entraînement sur suffisamment de données.
C'est ce qu'on appelle les capacités émergentes des grands modèles de langage
(large language models, ou LLM). Le code source présent en grande quantité dans
les données d'entraînement (GitHub, Stack Overflow, documentation technique)
faisait en sorte que ces modèles "comprenaient" les langages de programmation
de la même manière qu'ils comprenaient l'anglais ou le français : comme des
patterns statistiques dans des séquences de tokens. La frontière entre comprendre
du texte et comprendre du code s'est brouillée, et c'est précisément cette
convergence qui a rendu possible les outils de développement assisté par IA.

## L'IA entre dans l'éditeur

L'autocomplétion de code n'a pas attendu les LLM. Dès 1996, Intellisense de
Microsoft proposait dans Visual Basic des suggestions basées sur l'analyse
statique du code : le système connaissait les types, les méthodes disponibles,
les signatures de fonctions, et pouvait compléter un nom de variable ou proposer
une liste de méthodes applicables. Cette autocomplétion classique, présente
aujourd'hui dans tous les IDE, est un héritage direct de l'IA symbolique : elle
repose sur un parsing rigoureux du code, des tables de symboles et des règles
de typage. Elle est fiable et prévisible, mais elle ne peut compléter que ce
qui est syntaxiquement et sémantiquement déductible du code existant. Elle ne
peut pas deviner l'intention du programmeur.

Les premiers outils d'autocomplétion neuronale, comme Kite (2014) et TabNine
(2018, renommé Tabnine), ont commencé à utiliser des modèles de machine
learning pour prédire non seulement le prochain token syntaxiquement valide,
mais la prochaine ligne ou le prochain bloc de code que le programmeur avait
probablement l'intention d'écrire. Les résultats étaient prometteurs mais
limités : les modèles étaient petits, les suggestions souvent maladroites, et
l'expérience ressemblait davantage à une autocomplétion améliorée qu'à une
véritable assistance.

Le moment charnière est arrivé en juin 2021 avec le lancement de GitHub Copilot,
développé en partenariat avec OpenAI. Copilot était alimenté par Codex, un
modèle dérivé de GPT-3 et spécifiquement entraîné sur des dépôts de code
publics hébergés sur GitHub. La différence avec les outils précédents était
qualitative, pas seulement quantitative : Copilot pouvait générer des fonctions
entières à partir d'un commentaire décrivant leur comportement, compléter des
patterns complexes en s'appuyant sur le contexte du fichier, et s'adapter au
style du code environnant. Pour beaucoup de développeurs, c'était la première
fois qu'un outil d'IA produisait du code réellement utile, pas juste
impressionnant comme démonstration.

Puis, en novembre 2022, OpenAI a lancé ChatGPT, et tout a basculé. ChatGPT
n'était pas un outil de développement : c'était un agent conversationnel
généraliste. Mais les développeurs ont immédiatement commencé à l'utiliser pour
écrire du code, déboguer des erreurs, expliquer des algorithmes et générer des
tests. L'interface de conversation rendait l'interaction plus naturelle que
l'autocomplétion dans un IDE : on pouvait décrire un problème en langage
naturel, poser des questions de suivi, demander des modifications. En quelques
mois, Stack Overflow a vu son trafic chuter significativement, un signal
révélateur du changement de comportement des développeurs.

L'étape suivante, celle que nous vivons actuellement, est le passage de
l'assistant au copilote vers l'agent. Des outils comme Cursor, Claude Code
(Anthropic) et GitHub Copilot Workspace ne se contentent plus de suggérer du
code dans un éditeur ou de répondre à des questions dans une fenêtre de chat.
Ils peuvent naviguer dans un dépôt entier, lire et comprendre des fichiers
existants, exécuter des commandes, lancer des tests, et itérer sur leur propre
travail jusqu'à ce que le résultat soit satisfaisant. Le développeur n'interagit
plus en tapant du code que l'IA complète : il décrit ce qu'il veut accomplir, et
l'agent se charge de trouver où intervenir, d'écrire le code, et de vérifier
qu'il fonctionne. C'est un changement de paradigme dans la relation entre le
développeur et son outil, et il soulève des questions profondes sur ce que
signifie "programmer".

## Le vibe coding

En février 2025, Andrej Karpathy, ancien directeur de l'IA chez Tesla et
cofondateur d'OpenAI, a publié un message qui a cristallisé un phénomène que
beaucoup de développeurs vivaient déjà sans le nommer : "There's a new kind of
coding I call 'vibe coding', where you fully give in to the vibes, embrace
exponentials, and forget that the code even exists." Le vibe coding, c'est
l'idée de coder en décrivant ce qu'on veut en langage naturel, d'accepter le
code généré par l'IA sans nécessairement le lire ou le comprendre en détail, et
d'itérer en décrivant les corrections souhaitées plutôt qu'en modifiant le code
directement. Karpathy décrivait son propre usage pour des projets personnels,
avec une honnêteté désarmante : "I just see stuff, say stuff, run stuff, and
copy-paste stuff, and it mostly works."

Le terme a immédiatement déclenché un débat intense dans la communauté des
développeurs. Pour ses défenseurs, le vibe coding est une démocratisation
radicale : des personnes qui n'auraient jamais appris à programmer peuvent
désormais créer des applications fonctionnelles. Pour ses critiques, c'est une
recette pour produire du code fragile, incompris, et potentiellement dangereux.
Le débat est riche parce qu'il touche à des questions fondamentales sur la
nature même de la programmation.

En 1979, Edsger Dijkstra, l'un des pères de la programmation structurée que
nous avons rencontré dans le module 1, a écrit un texte au titre sans
équivoque : "On the foolishness of 'natural language programming'". Pour
Dijkstra, l'idée de programmer en langage naturel n'était pas seulement
impraticable, elle était fondamentalement mal conçue. Les langages de
programmation sont précis justement parce qu'ils éliminent l'ambiguïté
inhérente au langage naturel. Quand un compilateur reçoit une instruction, il
n'y a qu'une seule interprétation possible. Le langage naturel, lui, est
truffé d'ambiguïtés, de sous-entendus, de contexte implicite. Dire à une
machine "trie cette liste de manière intelligente" est une instruction
parfaitement claire pour un humain et parfaitement vague pour un ordinateur.
Pour Dijkstra, la rigueur formelle des langages de programmation n'était pas un
obstacle à surmonter mais une conquête à préserver, et vouloir programmer en
langage naturel revenait à abandonner volontairement l'outil qui rend le
raisonnement rigoureux possible. Quarante-cinq ans plus tard, le vibe coding
ressemble exactement à ce que Dijkstra jugeait insensé.

Et pourtant, il y a un argument en sens inverse qui mérite d'être pris au
sérieux. Si on regarde l'histoire de l'informatique avec du recul, le
développement logiciel a toujours progressé en montant d'un niveau
d'abstraction. Les premiers programmeurs écrivaient en code machine, des
séquences de 0 et de 1 que le processeur exécutait directement. L'assembleur a
introduit un premier niveau d'indirection : des mnémoniques lisibles par un
humain, traduits automatiquement en code machine par un assembleur. Puis les
langages de haut niveau comme FORTRAN et C ont ajouté un niveau
supplémentaire : on décrit des opérations (boucles, conditions, fonctions) dans
un langage plus proche de la pensée humaine, et le compilateur se charge de la
traduction. Python et les langages interprétés ont monté encore d'un cran, en
éliminant la gestion manuelle de la mémoire et en rapprochant encore le code
du raisonnement naturel. Vue sous cet angle, l'IA générative est simplement le
prochain étage de cette fusée : on décrit ce qu'on veut en langage naturel, et
le modèle se charge de le traduire en code. Et à chaque étape de cette
histoire, les programmeurs de la génération précédente ont protesté que le
nouveau niveau d'abstraction était une perte de contrôle inacceptable. Les
programmeurs en assembleur trouvaient que les compilateurs C produisaient du
code inefficace. Les développeurs C trouvaient que les langages interprétés
cachaient trop de détails. L'histoire leur a donné partiellement raison à chaque
fois (on perd effectivement du contrôle), mais elle a aussi montré que le gain
en productivité et en accessibilité l'emportait largement.

L'analogie est séduisante, mais elle a des limites importantes, et c'est
probablement Dijkstra qui a le dernier mot sur ce point précis. Un compilateur
est déterministe : le même code source produit toujours le même résultat. Un
LLM est stochastique : la même instruction en langage naturel peut produire du
code différent à chaque exécution. Un compilateur garantit la correction de sa
traduction : si le programme compile, la traduction du code source en code
machine est fidèle à la sémantique du langage. Un LLM ne garantit rien : il
peut produire du code qui a l'air correct, qui passe même certains tests, mais
qui contient des erreurs subtiles ou des hallucinations. Et surtout, le langage
naturel reste fondamentalement ambigu, exactement comme Dijkstra l'avait
diagnostiqué. Quand on dit à un compilateur `for i in range(10)`, il n'y a
aucune ambiguïté. Quand on dit à un LLM "parcours les dix premiers éléments",
le modèle doit inférer de quel type de collection on parle, si l'indexation
commence à 0 ou à 1, et ce qu'on entend par "parcourir". La plupart du temps,
il infère correctement, grâce au contexte. Mais "la plupart du temps" n'est pas
"toujours", et en programmation, la différence compte.

Ce qui nous ramène à Peter Naur. Si programmer, c'est construire une théorie du
programme, une compréhension profonde de pourquoi le code est comme il est et
comment il devrait évoluer, alors le vibe coding pose un problème fondamental :
il produit du code sans théorie. Le développeur qui accepte du code généré sans
le comprendre se retrouve immédiatement dans la situation décrite par Naur quand
le développeur original quitte le projet : il y a du code, mais la théorie qui
le sous-tend n'existe pas. Par la définition de Michael Feathers, c'est du
legacy code instantané : du code qu'on ne peut pas modifier en confiance, non
pas parce qu'il est vieux, mais parce que personne ne le comprend. Et les
conséquences pratiques dépendent énormément du niveau de compétence du
développeur. Pour un développeur senior, le vibe coding peut être un
accélérateur puissant : il génère rapidement du code que le développeur est
capable de lire, d'évaluer et de corriger, parce qu'il possède déjà la théorie
du domaine. Pour un débutant, c'est un piège potentiel : le code fonctionne, il
ne sait pas pourquoi, et quand il cesse de fonctionner, il ne sait pas comment
le réparer. Ce n'est pas un argument contre l'utilisation de l'IA pour
apprendre à programmer, bien au contraire, mais c'est un argument pour que
l'apprentissage de la programmation reste centré sur la compréhension, pas sur
la production de code.

## Ce qui change dans les pratiques du génie logiciel

L'arrivée de l'IA générative ne rend pas obsolètes les pratiques que nous avons
étudiées dans ce cours. Au contraire, elle les rend plus importantes que jamais,
tout en transformant la manière dont elles s'appliquent.

Les tests, que nous avons abordés en profondeur dans le module 2, deviennent le
filet de sécurité indispensable du développement assisté par IA. Quand un
développeur écrit son propre code, il a une certaine confiance dans sa
correction parce qu'il a construit la théorie du programme en même temps que le
code. Quand le code est généré par un LLM, cette confiance n'existe pas a
priori : le code a l'air correct, mais il pourrait contenir des erreurs subtiles
que seule l'exécution peut révéler. Les tests automatisés deviennent alors le
mécanisme principal de vérification. Un workflow de développement assisté par IA
bien conçu ressemble souvent à du TDD inversé : on écrit les tests d'abord (ou
on les fait écrire par l'IA et on les valide), puis on demande à l'IA de
générer le code qui les fait passer. Si les tests sont bons, le code généré est
vérifiable, quelle que soit la manière dont il a été produit. La pyramide des
tests, le coverage, les tests de propriété avec Hypothesis : tout ce que nous
avons vu dans le module 2 prend une pertinence nouvelle quand le code n'est pas
écrit par un humain.

La revue de code (module 4) change de nature elle aussi. Traditionnellement, le
code review servait à la fois de vérification de qualité et de mécanisme de
partage de connaissances au sein d'une équipe. Avec du code généré par IA, la
dimension de vérification devient plus critique : le relecteur doit se demander
non seulement "est-ce que ce code est correct et lisible ?", mais aussi "est-ce
que ce code fait bien ce qu'on pense qu'il fait, même dans les cas limites ?".
Les hallucinations des LLM sont souvent plausibles : le code a la bonne
structure, utilise les bons noms de fonctions, mais fait quelque chose de
subtilement différent de ce qui était demandé. Un oeil humain exercé reste, pour
l'instant, le meilleur détecteur de ces erreurs.

L'architecture et la modularité (module 3) deviennent paradoxalement plus
importantes dans un monde de code généré. Un LLM travaille mieux sur du code
bien structuré : des modules avec des responsabilités claires, des interfaces
bien définies, des fonctions courtes avec des noms descriptifs. Plus le code
existant est propre et modulaire, plus les suggestions de l'IA seront
pertinentes, parce que le modèle dispose de meilleur contexte pour comprendre
ce qui est attendu. À l'inverse, une base de code mal structurée, avec des
dépendances enchevêtrées et des responsabilités floues, va produire des
suggestions incohérentes. Les principes SOLID, le découplage, la séparation des
préoccupations : tout cela facilite non seulement le travail humain, mais aussi
le travail de l'IA. C'est un argument inattendu en faveur du bon design : il
rend le développement assisté par IA plus efficace.

Enfin, le débogage et la compréhension du code restent fondamentalement humains.
Un LLM peut suggérer des pistes quand on lui présente un message d'erreur, et
il le fait souvent remarquablement bien. Mais quand le bug est subtil, quand il
implique une interaction entre plusieurs composantes du système, quand il ne se
manifeste que sous certaines conditions de charge ou avec certaines données, la
capacité de raisonner sur le système dans son ensemble, de formuler des
hypothèses et de les tester méthodiquement, reste une compétence irremplaçable.
Le développeur qui comprend les fondamentaux (comment fonctionne la mémoire, ce
que fait réellement une requête SQL, pourquoi une condition de course se produit)
sera toujours plus efficace, avec ou sans IA, que celui qui ne fait que
manipuler des abstractions sans en comprendre les mécanismes sous-jacents.
