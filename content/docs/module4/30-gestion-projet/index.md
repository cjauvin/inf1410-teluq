---
title: "Gestion de projet et coordination"
slug: "gestion-projet"
weight: 30
---

# Gestion de projet et coordination

Les méthodes agiles comme Scrum et Kanban fournissent un cadre pour organiser le
travail d'une équipe. Mais au quotidien, une équipe de développement doit aussi
résoudre des problèmes plus terre-à-terre : comment partager les décisions
techniques importantes ? Comment communiquer efficacement quand tout le monde
n'est pas dans la même pièce ? Comment s'assurer qu'un nouveau membre de
l'équipe peut comprendre non seulement le code, mais aussi les raisons derrière
les choix qui ont été faits ? Ces questions relèvent de la coordination au sens
large, et les réponses ne se trouvent pas dans un framework ou un outil, mais
dans un ensemble de pratiques que les équipes développent, souvent par essais et
erreurs.

## La documentation comme outil de coordination

Le code source capture *ce que* fait un logiciel, mais rarement *pourquoi* il le
fait de cette manière. Pourquoi a-t-on choisi PostgreSQL plutôt que MongoDB ?
Pourquoi l'authentification passe-t-elle par un service externe plutôt qu'être
implémentée en interne ? Ces décisions architecturales sont prises après
réflexion, discussion, parfois débat, puis elles se cristallisent dans le code
et tout le monde oublie le raisonnement qui les sous-tend. Six mois plus tard,
un nouveau développeur (ou le même développeur qui a oublié) se retrouve devant
le code et se demande pourquoi les choses sont faites ainsi. Pire, il risque de
remettre en question une décision sans en comprendre les contraintes originales.
Peter Naur dirait que la "théorie" du programme se perd quand le raisonnement
n'est pas explicite. C'est exactement ce problème que les *Architecture Decision
Records* (ADRs) cherchent à résoudre. Popularisés par Michael Nygard en 2011
dans un billet de blog devenu référence, les ADRs sont des documents courts et
structurés qui capturent une décision technique significative. Le format est
volontairement simple : un titre, un contexte (quel problème on cherchait à
résoudre), la décision prise, et les conséquences (positives et négatives).
Chaque ADR est numéroté et stocké dans le dépôt du projet, souvent dans un
répertoire `doc/adr/`. L'accumulation de ces documents forme une chronique des
décisions du projet, lisible par quiconque veut comprendre non seulement l'état
actuel du système, mais le chemin qui y a mené.

Les ADRs capturent les décisions déjà prises. Mais pour les changements
significatifs, il est souvent utile de formaliser la réflexion *avant* de coder.
C'est le rôle des *RFCs* (Request For Comments), un terme emprunté au processus
de standardisation d'Internet (les RFCs de l'IETF, dont la première date de
1969). Dans le contexte d'une équipe de développement, une RFC est un document
qui propose un changement technique important, expose les alternatives
considérées, et invite les commentaires de l'équipe avant toute implémentation.
L'idée est que l'écriture force la clarification de la pensée. Quand on doit
expliquer par écrit pourquoi on veut remplacer le système de cache, on découvre
souvent des angles morts qu'une discussion orale aurait laissé passer. Google
utilise des "design docs" internes pour tout changement significatif. Le projet
Rust utilise un processus de RFC public pour toute évolution du langage. Le même
modèle se retrouve dans l'évolution des langages de programmation eux-mêmes :
les PEPs pour Python, le processus TC39 pour JavaScript. Le principe est
toujours le même : proposer par écrit, discuter collectivement, décider de
manière traçable. Beaucoup d'équipes plus petites adoptent des versions
simplifiées : un document d'une ou deux pages dans le dépôt, révisé en pull
request comme du code. La frontière entre ADR et RFC est d'ailleurs floue : un
ADR peut être rédigé après une RFC, comme trace permanente de la décision qui en
a résulté. Ce qui compte, c'est que les décisions importantes laissent une trace
écrite, accessible à toute l'équipe, présente et future.

## Communication synchrone et asynchrone

La coordination d'une équipe ne passe pas seulement par des documents et des
décisions formelles. Elle passe aussi, et peut-être surtout, par la
communication quotidienne. Le sixième principe du manifeste Agile affirme que
« la méthode la plus simple et la plus efficace pour transmettre de
l'information est la conversation en face à face ». En 2001, quand le manifeste
a été rédigé, la plupart des équipes de développement travaillaient dans le même
bureau. Deux décennies plus tard, la réalité est très différente.

L'outil qui a peut-être le plus transformé la communication dans les équipes
logicielles est Slack. Son histoire est improbable : Stewart Butterfield,
cofondateur de Flickr, travaillait sur un jeu vidéo en ligne appelé Glitch. Le
jeu a échoué, mais l'outil de chat interne que l'équipe avait développé pour se
coordonner s'est avéré plus intéressant que le produit lui-même. Lancé en 2013,
Slack a connu une adoption fulgurante, atteignant un million d'utilisateurs
quotidiens en moins de deux ans. L'intuition de Butterfield était que l'email,
avec ses messages formels et ses longs fils de discussion, ne correspondait pas
au rythme de la collaboration logicielle. Slack proposait quelque chose de plus
fluide : des canaux thématiques, des messages courts, des intégrations avec les
outils de développement (GitHub, CI, monitoring). En quelques années, Slack (et
ses concurrents comme Microsoft Teams et Discord) est devenu le centre nerveux
des équipes de développement, le lieu où circulent les questions rapides, les
alertes automatisées, les liens vers les pull requests.

La pandémie de 2020 a accéléré brutalement cette tendance. Du jour au lendemain,
des millions de développeurs sont passés du bureau à leur domicile, et les
outils de visioconférence comme Zoom (fondé en 2011 par Eric Yuan, mais devenu
omniprésent en 2020) sont devenus le substitut par défaut aux réunions en
personne. Cette transition forcée a révélé une distinction fondamentale entre
deux types de communication. La communication *synchrone* (réunions Zoom,
conversations Slack en temps réel, pair programming) a une bande passante
élevée : on peut clarifier un malentendu en quelques secondes, lire les
réactions de l'autre, ajuster son propos à la volée. Mais elle est aussi
interruptive et éphémère : ce qui se dit dans une réunion est souvent perdu si
personne ne prend de notes, et les interruptions constantes fragmentent le temps
de concentration que le développement logiciel exige. La communication
*asynchrone* (issues GitHub, pull requests, documents partagés, emails) a les
propriétés inverses : elle est persistante, réfléchie, et respecte le rythme de
chacun, mais elle est plus lente et plus sujette aux malentendus.

La transition vers le travail à distance a aussi mis en lumière ce qu'on
perdait. Dans un bureau, une part significative de la coordination se fait de
manière informelle : la conversation devant la machine à café (ce qu'on appelle
en anglais les "watercooler conversations"), le commentaire en passant devant
l'écran d'un collègue, le déjeuner où on découvre par hasard qu'un autre
développeur travaille sur un problème similaire au sien. Ces échanges informels
semblent anodins, mais ils jouent un rôle crucial dans la diffusion de
l'information et la construction de la confiance. Ils sont difficiles à
reproduire dans un contexte distribué. Certaines équipes essaient de compenser
avec des canaux Slack dédiés aux échanges non professionnels, des "virtual
coffee" programmés aléatoirement entre membres de l'équipe, ou des sessions de
pair programming qui recréent une forme de proximité. Mais ces substituts
restent imparfaits, et la tension entre efficacité du travail à distance et
richesse de la communication en personne n'est pas résolue.

Les équipes distribuées les plus efficaces ont développé des pratiques pour tirer
le meilleur des deux modes. GitLab, une entreprise entièrement distribuée depuis
sa fondation, a formalisé un principe qu'ils appellent "handbook first" : toute
information importante doit d'abord être écrite dans la documentation de
l'entreprise, et les réunions servent à discuter ce qui a été écrit, pas à
transmettre de l'information nouvelle. Basecamp (l'entreprise derrière Ruby on
Rails) a adopté une philosophie similaire, décrite dans *Shape Up* (Ryan Singer,
2019) : les propositions de fonctionnalités sont rédigées sous forme de
"pitches" écrits, discutés de manière asynchrone, et les réunions synchrones
sont réservées aux décisions finales. Ces approches ne rejettent pas la
communication synchrone, elles la réservent pour ce qu'elle fait le mieux : les
discussions nuancées, la résolution de conflits, la construction de liens
humains. Tout le reste passe par l'écrit, qui a l'avantage d'être cherchable,
partageable et durable.

## L'estimation

Nous avons vu dans la
[section sur Scrum]({{< relref "/docs/module4/20-agile/10-scrum" >}}) que les
équipes utilisent les story points pour estimer l'effort relatif de chaque
tâche. Mais la question de l'estimation en développement logiciel est plus
profonde que le choix d'une échelle. Fred Brooks, dans *The Mythical Man-Month*,
constatait déjà en 1975 que les programmeurs sont des optimistes chroniques : ils
sous-estiment systématiquement la difficulté de leur travail, en partie parce
qu'ils ne tiennent pas compte du temps passé à comprendre le problème, à
déboguer, à tester, à communiquer. L'estimation de logiciel est fondamentalement
difficile parce que le travail n'est pas répétitif. Quand un maçon estime le
temps pour construire un mur, il peut se baser sur les murs précédents, car les
murs sont largement similaires. En logiciel, si une tâche est identique à une
précédente, on ne la refait pas : on réutilise le code existant. Chaque tâche
estimée est donc, par définition, quelque chose qu'on n'a jamais fait exactement
de cette manière. L'une des techniques les plus connues pour atténuer ce
problème est le *planning poker*, où chaque membre de l'équipe propose
simultanément une estimation (souvent en story points) en révélant une carte en
même temps que les autres. L'idée est d'éviter l'effet d'ancrage, un biais
cognitif où la première estimation énoncée influence toutes les suivantes. Quand
les estimations divergent fortement, la discussion qui s'ensuit est souvent plus
précieuse que le chiffre final : elle révèle des hypothèses différentes sur la
portée ou la complexité de la tâche. Certaines équipes expérimentées finissent
d'ailleurs par abandonner l'estimation en points au profit d'une approche plus
simple : découper le travail en tâches suffisamment petites pour être terminées
en un ou deux jours, et simplement compter le nombre de tâches. L'important
n'est pas la méthode d'estimation, mais la conversation qu'elle provoque et la
conscience qu'estimer du logiciel est un exercice intrinsèquement incertain.