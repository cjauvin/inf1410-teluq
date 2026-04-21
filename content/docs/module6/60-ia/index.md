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

{{< image src="turing.jpg" alt="" title="" loading="lazy" >}}

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

{{< image src="neuron.webp" alt="" title="" loading="lazy" >}}

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

{{< image src="bengio.jpg" alt="" title="" loading="lazy" >}}

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

{{< image src="mila.webp" alt="" title="" loading="lazy" >}}

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
ses collègues (dont l'auteur de ce cours) ont publié "A Neural Probabilistic Language Model", un article qui
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

{{< image src="embeddings.webp" alt="" title="" loading="lazy" >}}

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

{{< image src="transformer.png" alt="" title="" loading="lazy" >}}

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

{{< image src="chatgpt.webp" alt="" title="" loading="lazy" >}}

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

{{< image src="vsc-ai.jpg" alt="" title="" loading="lazy" >}}

Puis, en novembre 2022, OpenAI a lancé ChatGPT, et tout a basculé. ChatGPT
n'était pas un outil de développement : c'était un agent conversationnel
généraliste. Mais les développeurs ont immédiatement commencé à l'utiliser pour
écrire du code, déboguer des erreurs, expliquer des algorithmes et générer des
tests. L'interface de conversation rendait l'interaction plus naturelle que
l'autocomplétion dans un IDE : on pouvait décrire un problème en langage
naturel, poser des questions de suivi, demander des modifications. En quelques
mois, Stack Overflow a vu son trafic chuter significativement, un signal
révélateur du changement de comportement des développeurs.

## La confusion autour du terme « agent »

L'annonce de ChatGPT en novembre 2022 avait ouvert une boîte de Pandore conceptuelle. En quelques mois, un nouveau vocabulaire envahissait les conversations sur l'IA : *agent*, *agentic*, *autonomous AI*. Le désir était là, palpable : passer de l'assistant qui répond à l'agent qui agit. Mais dès qu'on essayait de définir ce que "agent" voulait dire concrètement, la discussion se brouillait. Voulait-on dire un modèle capable de raisonner en plusieurs étapes ? Un système qui peut appeler des outils externes ? Un programme qui s'exécute de manière autonome sans intervention humaine ? Un LLM doté d'une mémoire persistante ? En 2023, chaque entreprise, chaque chercheur, chaque blog tech avait sa propre définition, et elles ne se recoupaient qu'en partie.

C'est d'ailleurs de ce flou qu'est née, paradoxalement, l'une des contributions techniques les plus concrètes de cette période. En novembre 2024, Anthropic a publié le protocole MCP (Model Context Protocol), une spécification ouverte qui définit une interface standard entre un LLM et des "outils" externes : des serveurs qui peuvent fournir des données, exécuter des commandes, lire des fichiers, interroger des bases de données. MCP ne prétendait pas définir ce qu'est un "agent" en général; il répondait à une question plus précise&nbsp;: comment un modèle de langage peut-il interagir de manière fiable et sécurisée avec son environnement ? Le protocole a rapidement été adopté par d'autres acteurs de l'industrie, et est devenu une brique de base de l'écosystème agentique, un peu comme HTTP l'avait été pour le web.

Au fil de ces expérimentations, une définition s'est progressivement imposée dans la pratique, moins par consensus théorique que par l'usage. Un agent, c'est un LLM qui peut manipuler des outils locaux : lire et écrire des fichiers, exécuter des commandes shell, lancer des tests, appeler des APIs. La boucle est simple : le modèle reçoit une instruction, choisit un outil, observe le résultat, et itère jusqu'à ce que la tâche soit accomplie. Ce que cette définition perd en généralité, elle le gagne en clarté opérationnelle. Et c'est le succès d'outils comme Claude Code, lancé par Anthropic en 2025, qui a contribué à ancrer cette vision : un agent de développement qui vit dans le terminal, qui lit votre dépôt, exécute vos tests, et itère sur son propre travail, sans interface graphique, sans magie apparente, juste un modèle de langage avec accès à bash.

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

{{< image src="vibe-coding.png" alt="" title="" loading="lazy" >}}

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

## Démonstrations avec Claude Code

Une note sur la conception de cette section : les deux démonstrations qui suivent
ont elles-mêmes été conçues avec Claude Code. Il y a quelque chose de
délibérément récursif dans cette démarche : utiliser l'outil pour enseigner
l'outil. Mais il serait facile de mal comprendre ce que cela signifie. L'agent
n'a pas simplement généré des exemples tout faits que l'auteur a copiés-collés
dans le cours. La méthode adoptée a été différente : demander à Claude Code
d'expliquer quoi faire étape par étape, puis exécuter chaque étape manuellement,
vérifier que le résultat est correct, et seulement ensuite intégrer l'exemple
dans le cours. Cette distinction est fondamentale. Un exemple généré sans
vérification peut contenir des erreurs invisibles, des commandes qui ne
fonctionnent pas dans un contexte légèrement différent, ou des comportements
qui dépendent d'une version spécifique d'un outil. Un exemple exécuté et
validé par un humain est fiable. Cette méthodologie — demander à l'IA de
proposer, puis vérifier soi-même avant d'accepter — devrait être au coeur de
tout développement assisté par IA. Elle ne ralentit pas le travail de manière
significative, mais elle réduit considérablement le risque d'introduire des
erreurs qu'on ne comprend pas et qu'on ne saurait pas corriger.

{{< image src="inception.avif" alt="" title="" loading="lazy" >}}

Les deux démonstrations qui suivent rendent ces idées concrètes. Elles ont été
réalisées avec Claude Code, un agent de développement développé par Anthropic
qui peut naviguer dans un dépôt, lire des fichiers, exécuter des commandes,
lancer des tests et itérer sur son travail.

{{< image src="claude-alien.png" alt="" title="" loading="lazy" >}}

Claude Code est disponible sous plusieurs formes. La plus dépouillée est le CLI
(interface en ligne de commande) : on installe l'outil, on tape `claude` dans
un terminal, et on interagit directement avec l'agent. Il existe aussi des
extensions pour VS Code et les IDE JetBrains, qui intègrent Claude Code
directement dans l'éditeur avec une visualisation des diffs et une interface de
chat dans le panneau latéral. Pour ceux qui préfèrent une interface graphique
autonome, une application desktop (macOS et Windows) permet de gérer plusieurs
sessions en parallèle. Enfin, une version web accessible depuis `claude.ai/code`
ne nécessite aucune installation et fonctionne même depuis un téléphone. Dans
tous les cas, c'est le même moteur qui tourne en arrière-plan. Les deux
démonstrations qui suivent illustrent des usages différents, et chacune utilise
une interface différente : la première utilise le CLI pour explorer un codebase
existant, la seconde utilise l'extension VS Code pour créer une petite
application de zéro. Ce choix n'est pas arbitraire : le CLI convient bien à
l'exploration pure, où on pose des questions en mode conversationnel sans
modifier de fichiers ; l'extension VS Code est plus naturelle pour la
construction, parce qu'elle permet de voir les diffs et d'accepter ou rejeter
les modifications directement dans l'éditeur.

### Explorer un codebase : Requests

L'une des situations les plus courantes pour un développeur est d'arriver sur
un projet existant et de devoir en comprendre la structure, les choix de
conception et le fonctionnement interne. C'est exactement la situation décrite
par Peter Naur : il faut reconstruire la théorie d'un programme qu'on n'a pas
écrit. Traditionnellement, cela implique de lire le code, la documentation,
l'historique git, et de poser des questions aux collègues qui étaient là avant.
Un agent IA peut accélérer considérablement ce processus.

Pour cette démonstration, nous utilisons Requests, la bibliothèque HTTP la plus
populaire de l'écosystème Python. Créée par Kenneth Reitz en 2011, Requests est
utilisée par pratiquement tous les projets Python qui ont besoin de faire des
appels HTTP. Sa popularité repose sur une API d'une simplicité remarquable :
`requests.get("https://example.com")` suffit pour faire une requête. Mais
derrière cette façade simple se cache une architecture plus complexe, avec la
gestion des sessions, des cookies, des redirections, de l'authentification et
des adaptateurs de transport. C'est un excellent terrain d'exploration.

La première chose à faire est de cloner le dépôt de Requests depuis GitHub,
exactement comme le ferait un nouveau développeur qui rejoint le projet. On se
retrouve alors avec un répertoire `requests/` contenant le code source, et on
peut lancer Claude Code directement dans ce contexte.

```shell
$ git clone git@github.com:psf/requests.git
$ cd requests
$ claude
```

Une fois l'agent démarré, on peut lui adresser des messages en langage naturel,
mais Claude Code offre aussi des *commandes slash* : des instructions spéciales
préfixées d'un `/` qui contrôlent le comportement de l'agent plutôt que de lui
poser une question. Par exemple, `/help` affiche la liste des commandes
disponibles, `/compact` demande à l'agent de résumer la conversation pour
libérer de la mémoire, `/usage` affiche la consommation de la session en cours
et la facturation hebdomadaire, et `/quit` termine la session. La première commande
utile quand on arrive sur un nouveau projet est `/init` : elle demande à
l'agent d'analyser le dépôt courant et de générer automatiquement un fichier
`CLAUDE.md` à sa racine.

Ce fichier `CLAUDE.md` est le mécanisme principal pour donner des instructions
persistantes à Claude Code sur un projet. On peut y décrire l'architecture du
projet, les conventions de code adoptées par l'équipe, les commandes à
connaître pour lancer les tests ou le serveur de développement, ou tout autre
contexte que l'agent devrait avoir en tête à chaque session. Contrairement à
une question posée dans la conversation (qui disparaît quand on ferme le
terminal), le contenu de `CLAUDE.md` est relu automatiquement à chaque
démarrage. C'est une forme de mémoire externe pour l'agent, ancrée dans le
dépôt lui-même, et donc partagée avec toute l'équipe si le fichier est versionné
avec git. Quand `/init` génère ce fichier, il produit un premier portrait du
projet qu'on peut ensuite compléter et affiner manuellement.

{{< image src="cc1.png" alt="" title="" loading="lazy" >}}

Avant d'écrire le fichier `CLAUDE.md`, l'agent s'arrête et demande la
permission. Ce comportement est au coeur du modèle de confiance de Claude Code :
l'agent ne modifie jamais un fichier, n'exécute jamais une commande shell, et
n'appelle jamais un outil externe sans avoir d'abord demandé l'autorisation.
Quand une telle action est sur le point d'être effectuée, Claude Code affiche
une description de ce qu'il s'apprête à faire et attend une réponse. On peut
approuver l'action pour cette fois, la refuser, ou choisir de toujours
l'autoriser pour la session courante (ce qui évite d'avoir à confirmer à chaque
fois des actions répétitives comme l'exécution des tests). Ce système de
permissions existe pour une raison simple : un agent qui peut lire des fichiers,
écrire du code et exécuter des commandes shell a un pouvoir considérable sur
l'environnement dans lequel il tourne. La supervision humaine n'est pas une
contrainte artificielle, c'est une pratique saine, surtout quand on commence à
travailler avec un outil qu'on ne connaît pas encore bien.

{{< image src="cc2.png" alt="" title="" loading="lazy" >}}

**Première question : la vue d'ensemble.**

On commence par demander à Claude Code un portrait général de l'architecture du
projet.

```
Peux-tu me donner une vue d'ensemble de l'organisation et
du fonctionnement de ce projet
```

La réponse est structurée en plusieurs niveaux. D'abord, une description
de ce qu'est Requests en une phrase : une bibliothèque qui enveloppe urllib3,
qui enveloppe elle-même `http.client` de la bibliothèque standard, pour offrir
une API simple qualifiée par son auteur d'"HTTP for Humans". Ensuite, un
diagramme textuel montrant le cycle de vie d'une requête à travers les couches :
de `requests.get()` dans `api.py` jusqu'à urllib3, en passant par `Session`
dans `sessions.py`, `PreparedRequest` dans `models.py`, et `HTTPAdapter` dans
`adapters.py`. Enfin, un tableau récapitulatif des modules de support
(`auth.py`, `cookies.py`, `exceptions.py`, etc.) avec le rôle de chacun. Ce
premier échange illustre un usage fondamental : obtenir une carte mentale
complète d'un projet en quelques secondes, avec une profondeur qu'il faudrait
plusieurs heures de lecture pour construire manuellement.

{{< image src="cc3.png" alt="" title="" loading="lazy" >}}

**Deuxième question : suivre le chemin d'une requête.**

On demande ensuite à l'agent :

```
Peux-tu tracer et expliquer clairement et brièvement ce qui se passe
quand on exécute requests.get("https://example.com")
```

Avant de répondre, l'agent lit de sa propre initiative les trois fichiers clés pour
pouvoir citer des références précises. La réponse prend la forme de six étapes
numérotées, chacune ancrée dans le code réel avec des numéros de ligne : de
`api.get()` en `api.py:73` jusqu'à `build_response()` qui enveloppe la réponse
brute d'urllib3 dans un objet `Response`. Deux détails ressortent de cette
trace. D'abord, l'étape 2 montre que `api.request()` crée une `Session` via un
bloc `with`, ce qui garantit que les sockets sont libérés à la fin — mais aussi
que chaque appel à `requests.get()` ouvre et ferme une session complète ; pour
des appels répétés vers le même serveur, créer une `Session` manuellement est
plus efficace parce qu'elle réutilise les connexions TCP. Ensuite, l'étape 4
révèle un mécanisme peu documenté&nbsp;: après avoir envoyé la requête,
`Session.send()` déclenche un système de *hooks* qui permet d'exécuter des
fonctions arbitraires sur la réponse avant qu'elle soit retournée. La réponse
se termine par un schéma textuel en arbre qui résume toute la chaîne d'un coup
d'oeil. Ce type d'analyse serait fastidieux à faire manuellement : il faut
ouvrir plusieurs fichiers, trouver les bons points d'entrée, suivre les appels
de méthode en méthode. L'agent le fait en quelques secondes et produit une
explication linéaire qui reconstruit la *théorie* du programme, au sens de
Naur.

{{< image src="cc4.png" alt="" title="" loading="lazy" >}}

**Troisième question : un détail architectural surprenant.**

On demande finalement à l'agent d'expliquer le rôle du pattern Adapter dans
Requests. La réponse commence par identifier le problème que ce pattern résout :
`Session` a deux responsabilités bien distinctes, gérer l'état (cookies, auth,
headers, redirections) et assurer le transport (ouvrir une socket, gérer TLS,
envoyer les octets). Si ces deux responsabilités étaient mélangées dans la même
classe, changer de backend de transport (remplacer urllib3 par `httpx`, ou par un
mock pour les tests) impliquerait de modifier `Session` elle-même, un objet
déjà complexe. Le pattern Adapter isole le transport derrière une interface
minimale, `BaseAdapter`, dont la seule méthode obligatoire est `send()`. Les
adaptateurs sont montés par préfixe d'URL dans le constructeur de `Session` :
`https://` et `http://` sont associés par défaut à `HTTPAdapter`. L'agent
énumère ensuite trois usages concrets que ce design rend possibles&nbsp;: les
tests avec un faux adaptateur monté à la place du vrai, les protocoles custom
(un adaptateur pour `ftp://` ou pour des sockets Unix), et des configurations
différentes par hôte. La réponse se conclut sur un résumé qui rappelle
l'essentiel : `Session` orchestre, urllib3 transporte, et les deux s'ignorent
mutuellement. Cet échange illustre comment l'agent peut relier du code concret
à des concepts théoriques que l'étudiant a déjà vus dans le module 3 : le
pattern adaptateur, la séparation des responsabilités, l'inversion de
dépendances.

{{< image src="cc5.png" alt="" title="" loading="lazy" >}}

En fin de session, la commande `/usage` donne une vue sur la consommation :
la portion du contexte de la session courante utilisée, la consommation
hebdomadaire tous modèles confondus, et le montant facturé depuis le début du
cycle de facturation. C'est un rappel utile que l'agent n'est pas gratuit, et
que des sessions longues ou des dépôts volumineux coûtent plus que de courtes
interactions.

{{< image src="cc6.png" alt="" title="" loading="lazy" >}}

L'exploration d'un codebase avec un agent IA n'est pas du vibe coding : on ne
génère pas de code à l'aveugle, on construit activement une compréhension. Le
développeur pose des questions, évalue les réponses, approfondit les points qui
l'intéressent. L'IA accélère la construction de la théorie du programme, mais
c'est toujours le développeur qui la construit.

### Créer un utilitaire : md-link-check

La deuxième démonstration illustre l'autre usage fondamental : construire
quelque chose de neuf. On utilise ici l'extension VS Code, qui change
sensiblement l'expérience. Claude Code s'intègre dans le panneau latéral de
l'éditeur, et quand l'agent propose des modifications à un fichier, elles
apparaissent directement dans l'éditeur sous forme de diff : les lignes ajoutées
en vert, les lignes supprimées en rouge, avec des boutons pour accepter ou
rejeter chaque modification. C'est plus interactif que le CLI, et plus naturel
quand on est en train de construire quelque chose.

L'objectif est de créer un petit utilitaire en ligne de commande qui vérifie
que les liens dans des fichiers Markdown sont valides. Un outil simple, utile,
et dont le périmètre est assez restreint pour tenir dans une démonstration.

La première étape n'implique pas encore Claude Code. On initialise le projet
avec `uv`, l'outil de gestion de projets Python que nous avons vu dans le
module 2 :

```shell
$ uv init md-link-check
$ cd md-link-check
```

Cette commande crée la structure de base : un fichier `pyproject.toml` pour les
métadonnées et les dépendances, un `README.md`, et un `hello.py` de
démarrage. C'est à partir de ce squelette qu'on va ouvrir VS Code et lancer
Claude Code.

**Étape 1 : initialiser et décrire l'intention.**

La première chose à faire dans l'extension VS Code est la même que dans la démo
CLI : taper `/init`. L'agent analyse le squelette du projet et génère un
`CLAUDE.md` initial. Avant d'écrire le fichier, il demande la permission,
exactement comme on l'a vu avec Requests. On choisit "Yes, allow all edits this
session" pour ne pas avoir à confirmer chaque modification pendant le reste de
la démonstration.

{{< image src="cc-md-1.png" alt="" title="" loading="lazy" >}}

Le `CLAUDE.md` généré est minimal : il décrit la structure de base du projet.
C'est maintenant qu'on l'édite manuellement pour y ajouter l'intention de
l'outil : ce qu'il doit faire, les choix techniques (bibliothèque `requests`,
tests avec `pytest`), le format de sortie attendu. Cette étape est importante :
on écrit la spécification dans le dépôt, versionnée avec git, plutôt que de
tout expliquer dans le chat à chaque session. La section ajoutée est mise en
évidence dans le screenshot — quatre points qui décrivent précisément le
comportement attendu, plus une ligne sur les choix techniques.

{{< image src="cc-md-2.png" alt="" title="" loading="lazy" >}}

**Étape 2 : planifier avant d'implémenter.**

Avant d'envoyer la demande d'implémentation, on bascule en **Plan mode** via le
menu des modes dans le panneau Claude Code. Ce mode a un comportement distinct
des deux autres options disponibles : "Ask before edits" demande une approbation
avant chaque modification individuelle, "Edit automatically" applique les
changements sans confirmation, et "Plan mode" ne touche à aucun fichier — il
se contente d'explorer le code et de produire un plan complet avant d'agir.
C'est l'équivalent de demander à un développeur de réfléchir à voix haute avant
de commencer à taper.

{{< image src="cc-md-3.png" alt="" title="" loading="lazy" >}}

Une fois le mode activé, on envoie simplement :

```
Implémente le projet tel que décrit dans CLAUDE.md
```

L'agent relit `CLAUDE.md` et produit un plan complet — sans toucher à aucun fichier.

{{< image src="cc-md-4.png" alt="" title="" loading="lazy" >}}

Le plan est structuré en trois sections. D'abord le contexte : l'agent confirme
sa compréhension du projet en résumant ce qu'il a lu dans `CLAUDE.md`. Ensuite
les fichiers concernés : `main.py` à créer avec les fonctions `extract_links()`,
`check_url()` et `check_file()`, un fichier de tests `test_main.py`, et
`pyproject.toml` à mettre à jour pour ajouter `requests` et `pytest` comme
dépendances. Enfin la vérification : comment lancer les tests après
l'implémentation. La boîte en bas de l'écran demande si on accepte ce plan,
avec trois options — accepter et continuer automatiquement, accepter et
demander confirmation avant chaque modification, ou ne pas retenir le plan.
C'est un deuxième niveau de contrôle : on a validé le plan de haut niveau, et
on peut encore choisir le degré de supervision pour l'exécution. On choisit
"Yes, and auto-accept" : le plan a été relu et approuvé, on peut maintenant
faire confiance à l'agent pour l'exécuter.

Même avec ce choix, l'agent ne peut pas exécuter une commande shell sans
demander la permission. Avant d'installer les dépendances, il s'arrête et
affiche la commande exacte qu'il s'apprête à lancer :
`uv add requests && uv add --dev pytest`. On peut l'approuver, l'autoriser
pour toutes les commandes `uv add` du projet, ou la refuser. Cette distinction
est importante : les modifications de fichiers (écriture de code) et
l'exécution de commandes shell sont deux niveaux de permissions séparés. Écrire
du code dans un fichier est réversible avec git ; exécuter une commande shell
peut avoir des effets plus larges sur l'environnement.

{{< image src="cc-md-5.png" alt="" title="" loading="lazy" >}}

L'agent exécute ensuite le plan étape par étape : il crée `main.py` avec les
trois fonctions, crée le fichier de tests, met à jour `pyproject.toml` pour
ajouter les dépendances. Pour chaque modification de fichier, le diff apparaît
directement dans l'éditeur. Une fois les fichiers écrits, l'agent demande à
lancer les tests avec `uv run pytest tests/ -v` — on choisit d'autoriser toutes
les commandes `uv run` pour le projet, et l'agent conclut en vérifiant que tout
passe.

{{< image src="cc-md-6.png" alt="" title="" loading="lazy" >}}

Une fois la permission accordée, l'agent installe les dépendances, écrit les
fichiers et lance les tests. Le screenshot suivant montre le résumé complet de
la session : les commandes exécutées, le diff de `pyproject.toml` avec les
nouvelles dépendances en vert, et en bas la confirmation que tous les tests
passent.

{{< image src="cc-md-7.png" alt="" title="" loading="lazy" >}}

**Étape 3 : vérifier par soi-même.**

L'agent a lancé les tests de son côté, mais rien n'empêche de les relancer
indépendamment dans le terminal intégré de VS Code — hors de Claude Code,
directement dans le shell. C'est un geste simple mais important : il rappelle
que l'agent et le développeur partagent le même environnement. Les tests ne
sont pas "les tests de l'IA", ils sont les tests du projet, et le développeur
peut (et devrait) les exécuter lui-même. On voit ici à la fois le code généré
dans l'éditeur et la sortie de `uv run pytest` dans le terminal — tous les
tests passent.

{{< image src="cc-md-8.png" alt="" title="" loading="lazy" >}}

**Étape 4 : tester et valider les choix de l'agent.**

Avant de relire le code, on teste l'outil sur un fichier Markdown minimal
qui contient un lien valide, un lien cassé et une image :

```shell
$ echo "Voici [Google](https://google.com) et [un lien cassé](https://exemple-inexistant-xyz.com) et ![logo](https://google.com/logo.png)" > test.md
$ uv run main.py test.md
[OK    ] test.md | Google | https://google.com | 200
[BROKEN] test.md | un lien cassé | https://exemple-inexistant-xyz.com | HTTPSConnectionPool(host='exemple-inexistant-xyz.com', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='exemple-inexistant-xyz.com', port=443): Failed to resolve 'exemple-inexistant-xyz.com' ([Errno 8] nodename nor servname provided, or not known)"))
```

{{< image src="cc-md-9.png" alt="" title="" loading="lazy" >}}

En relisant `main.py`, on remarque quelque chose d'intéressant. La regex
utilisée pour extraire les liens est :

```python
pattern = r"(?<!!)\[([^\]]+)\]\((https?://[^)]+)\)"
```

Le préfixe `(?<!!)` est un *negative lookbehind* qui signifie "pas précédé d'un
point d'exclamation" — ce qui exclut précisément les images Markdown, qui
s'écrivent `![texte alternatif](url)`. L'agent a anticipé ce cas sans qu'on le
lui demande explicitement : il a lu "exclure les images" dans `CLAUDE.md` et a
su comment l'implémenter. Le test de l'application le confirme : le fichier
`test.md` contient une image `![logo](https://google.com/logo.png)`, et cette
URL n'apparaît pas dans la sortie.

Cette relecture illustre une leçon importante. La relecture du code généré
n'est pas uniquement défensive (chercher des bugs) : c'est aussi le moyen de
comprendre ce que l'agent a fait et pourquoi. Un développeur qui accepte le
code sans le lire ne sait pas si l'agent a bien compris l'intention, même
quand tous les tests passent. Ici, l'agent a fait le bon choix — mais c'est
la relecture qui le révèle. C'est la différence entre produire du code et
construire une théorie du programme.

## Questions ouvertes

Le développement assisté par IA soulève des questions qui dépassent la technique
et qui n'ont pas encore de réponses définitives. En voici quelques-unes parmi
les plus débattues.

### Propriété intellectuelle

Les LLM qui génèrent du code ont été entraînés sur d'immenses corpus de code
source, dont une grande partie provient de dépôts open source hébergés sur
GitHub. En 2022, un recours collectif a été déposé contre GitHub, Microsoft et
OpenAI, alléguant que Copilot reproduisait parfois du code protégé par des
licences open source sans en respecter les termes (attribution, copyleft). La
question juridique reste ouverte : le code généré par un LLM est-il une oeuvre
dérivée du code d'entraînement ? Si un modèle produit un bloc de code
fonctionnellement identique à un extrait sous licence GPL, l'utilisateur est-il
tenu de respecter les termes de cette licence ? Les tribunaux n'ont pas encore
tranché. Pour les développeurs, la prudence recommande de traiter le code
généré par IA comme on traiterait du code trouvé sur Stack Overflow : utile
comme point de départ, mais à valider, à comprendre, et à adapter à son propre
contexte.

### Fiabilité et hallucinations

Les LLM produisent des réponses statistiquement plausibles, pas
nécessairement correctes. En génération de texte, on appelle ce phénomène une
"hallucination" : le modèle invente des faits avec aplomb. En génération de
code, les hallucinations prennent des formes spécifiques : des appels à des
fonctions qui n'existent pas dans la bibliothèque utilisée, des paramètres
inventés, des algorithmes qui semblent corrects mais qui ont des bugs subtils
dans les cas limites. Le problème est que le code halluciné a l'air
professionnel : il est bien formaté, utilise les bonnes conventions de nommage,
et peut même être accompagné de commentaires convaincants. C'est précisément
ce qui le rend dangereux pour un développeur qui ne vérifie pas. L'analogie
avec le compilateur trouve ici sa limite la plus nette : un compilateur ne
peut pas halluciner.

### Dépendance et déqualification

Si les développeurs s'habituent à laisser l'IA écrire leur code, risquent-ils
de perdre la capacité de le faire eux-mêmes ? La question n'est pas nouvelle :
on la posait déjà pour les calculatrices en mathématiques, pour les GPS en
navigation, pour les correcteurs orthographiques en écriture. Le phénomène de
déqualification (*deskilling*) est bien documenté dans d'autres professions :
les pilotes d'avion qui s'appuient trop sur le pilotage automatique peuvent
avoir des difficultés à reprendre le contrôle manuellement en situation
d'urgence. Pour le développement logiciel, le risque est que des développeurs
juniors n'acquièrent jamais les compétences fondamentales (débogage,
raisonnement algorithmique, compréhension de l'architecture) parce qu'ils
n'ont jamais eu à les exercer. Un développeur senior qui utilise l'IA comme
accélérateur garde ses compétences intactes, mais un débutant qui n'a jamais
résolu un bug sans assistance pourrait être démuni le jour où l'IA ne peut pas
l'aider. C'est un argument fort pour que la formation en informatique continue
d'exiger la maîtrise des fondamentaux, même dans un monde où l'IA est
omniprésente.

### Le slop et la dégradation des communs

L'expression *AI slop* est apparue autour de 2024 pour désigner un phénomène devenu difficile à ignorer : la prolifération de contenu généré par IA, de mauvaise qualité, qui inonde les espaces numériques. Des articles de blog écrits sans relecture, des réponses de forums copiées-collées sans vérification, des images génériques qui remplacent la photographie originale, des vidéos YouTube de formation technique produites à la chaîne sans expertise réelle. Le terme est délibérément péjoratif : il évoque la pâtée industrielle, quelque chose de produit en masse, sans soin, destiné à remplir un espace plutôt qu'à apporter de la valeur. Le problème n'est pas que l'IA génère du contenu, c'est que le coût marginal de production est devenu si faible que le rapport signal/bruit s'est effondré sur de nombreuses plateformes.

L'écosystème open source est l'un des environnements les plus touchés par ce phénomène. Des outils comme Claude Code, Copilot ou Cursor permettent de générer des pull requests en quelques minutes, sans nécessairement comprendre le projet cible. Les mainteneurs de projets populaires ont commencé à signaler un afflux de contributions générées par IA : des issues qui décrivent un "bug" déjà documenté ou inexistant, des pull requests qui corrigent un problème superficiel sans comprendre l'architecture sous-jacente, des propositions de fonctionnalités copiées-collées sans tenir compte de la philosophie du projet. Le travail de triage de ces contributions, souvent effectué bénévolement par des mainteneurs déjà surchargés, est devenu une charge supplémentaire significative. Il y a une ironie cruelle dans cette situation : une grande partie du code qui a servi à entraîner les modèles responsables de ce flot provient précisément de ces dépôts open source.

Face à cette situation, certains projets ont commencé à adapter leurs politiques de contribution. Des mainteneurs ont ajouté des clauses explicites dans leurs fichiers CONTRIBUTING.md demandant aux contributeurs de certifier qu'ils ont lu et compris le code qu'ils soumettent, que celui-ci soit écrit par un humain ou par une IA. D'autres ont simplement fermé les issues et les pull requests dont la provenance automatisée était évidente, parfois avec un message lapidaire. La plateforme PyPI, le dépôt central des paquets Python, a dû renforcer ses mécanismes de détection face à une vague de paquets générés automatiquement, dont certains contenaient du code malveillant camouflé dans du slop bénin. Ces réactions illustrent une tension fondamentale : l'open source repose sur le principe que la participation est ouverte à tous, mais ce modèle suppose implicitement que chaque contribution représente un investissement humain réel. Quand ce coût d'entrée disparaît, le modèle lui-même est mis sous pression.

### La position de Yoshua Bengio

Depuis 2023, Yoshua Bengio, dont les travaux fondateurs ont rendu les LLM
possibles, est devenu l'une des voix les plus importantes dans le débat sur les
risques de l'IA. En 2023, il a cosigné une lettre ouverte appelant à une
pause dans le développement des systèmes d'IA plus puissants que GPT-4, le
temps de mettre en place des mécanismes de sécurité adéquats. Sa position n'est
pas celle d'un technophobe : c'est celle d'un scientifique qui comprend
intimement la technologie et qui estime que la vitesse de développement dépasse
notre capacité à en comprendre et à en gérer les conséquences. Bengio a
comparé la situation à celle d'un chimiste qui découvrirait une réaction
permettant de produire une énergie considérable mais aussi de causer des
dommages immenses : la bonne réponse n'est pas d'arrêter la recherche, mais
d'exiger de la prudence et des garde-fous avant le déploiement à grande échelle.

Sa position illustre une tension fondamentale dans l'histoire de la technologie.
Les personnes les mieux placées pour comprendre les risques d'une innovation
sont souvent celles qui l'ont créée, mais elles sont rarement celles qui
décident de la manière dont elle est déployée. Oppenheimer et la bombe
atomique, les ingénieurs qui ont alerté sur le Therac-25 ou le Boeing 737 MAX
(section précédente) : l'histoire est remplie de cas où l'expertise technique
a été ignorée par les décideurs. Le mérite de Bengio est d'utiliser sa
crédibilité scientifique pour forcer le débat public, quitte à être critiqué
par une partie de l'industrie qui préfère accélérer sans contrainte.

### Retour à Brooks : silver bullet ou pas ?

Alors, l'IA générative est-elle la silver bullet que Brooks jugeait impossible ?
La réponse honnête est : pas encore, et probablement pas au sens où Brooks
l'entendait. Brooks distinguait la complexité accidentelle (celle des outils et
des processus) de la complexité essentielle (celle du problème qu'on résout).
L'IA générative est remarquablement efficace pour réduire la complexité
accidentelle : elle élimine le boilerplate, elle accélère les tâches répétitives,
elle rend accessible ce qui demandait auparavant une expertise technique
pointue. Mais la complexité essentielle, elle, reste intacte. Comprendre un
domaine métier, prendre les bonnes décisions d'architecture, anticiper les
conséquences d'un choix de conception : ce sont des problèmes fondamentalement
humains que l'IA, pour l'instant, ne résout pas.

Ce qui a changé, et que Brooks n'avait probablement pas anticipé, c'est que la
frontière entre complexité accidentelle et complexité essentielle s'est
déplacée. Des tâches qui relevaient autrefois de la complexité essentielle
(écrire un parser, implémenter un algorithme de tri, configurer un pipeline
CI/CD) sont devenues de la complexité accidentelle, parce que l'IA les
automatise de manière fiable. Ce déplacement de frontière est peut-être plus
important que la silver bullet elle-même : il libère le développeur pour se
concentrer sur les problèmes qui comptent vraiment. Le développeur de demain
passera moins de temps à écrire du code et plus de temps à décider quel code
devrait exister, à valider que le code fait ce qu'il devrait, et à comprendre
les systèmes dans lesquels il s'insère. C'est, paradoxalement, un retour aux
origines du génie logiciel : non pas la production de code, mais la gestion de
la complexité.

## Conclusion

Ce cours a commencé, dans le module 1, par une question simple : pourquoi le
logiciel est-il si difficile à construire ? Nous avons vu que la réponse de
Fred Brooks en 1986, la distinction entre complexité essentielle et complexité
accidentelle, reste le cadre le plus utile pour penser le métier. Puis nous
avons traversé les outils et les pratiques qui, couche par couche, tentent de
maîtriser cette complexité : les tests et le versioning pour le développeur
individuel (module 2), l'architecture et les APIs pour structurer les systèmes
(module 3), les méthodes agiles et la collaboration pour travailler en équipe
(module 4), le DevOps et l'observabilité pour faire vivre un logiciel en
production (module 5). Ce dernier module a élargi le regard vers le monde dans
lequel le logiciel existe : son économie, sa régulation, ses catastrophes, et
maintenant l'IA qui transforme la manière même de le construire.

Le fil conducteur de tout le cours est que le logiciel est une activité
fondamentalement humaine. Les outils changent, les langages évoluent, les
méthodes se transforment, mais les problèmes de fond restent les mêmes :
comprendre ce qu'on construit (Naur), gérer la complexité (Brooks), travailler
avec les autres (le Manifeste Agile), et prendre la responsabilité de ce qu'on
met au monde (l'éthique). L'IA ne change pas ces problèmes. Elle change la
vitesse à laquelle on peut produire du code, mais pas la difficulté de décider
quel code devrait exister.

Peter Naur écrivait en 1985 que la programmation est avant tout la construction
d'une théorie, un modèle mental du problème et de sa solution. Cette idée,
vieille de quarante ans, n'a jamais été aussi pertinente. Dans un monde où
n'importe qui peut générer du code en décrivant ce qu'il veut en langage
naturel, la valeur du développeur ne réside plus dans sa capacité à écrire des
lignes de code. Elle réside dans sa capacité à comprendre, à juger et à
décider. À construire la théorie.
