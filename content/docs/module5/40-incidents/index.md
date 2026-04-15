---
title: "La fiabilité et les incidents"
weight: 40
slug: "incidents"
---

# Que faire quand ça casse ?

Dans les sections précédentes, nous avons construit un pipeline qui amène le
code en production et des outils pour observer ce qui s'y passe. Mais tôt ou
tard, quelque chose va casser. Ce n'est pas une question de "si", mais de
"quand". Le 28 février 2017, un ingénieur d'Amazon a exécuté une commande de
maintenance de routine sur le service S3, l'infrastructure de stockage qui
héberge une part considérable du web. Une faute de frappe dans un paramètre a
retiré plus de serveurs que prévu, déclenchant une cascade de pannes qui a rendu
inaccessibles des milliers de sites et services pendant plusieurs heures. La
même année, un administrateur de base de données chez GitLab a accidentellement
exécuté un `rm -rf` sur le mauvais serveur de base de données, effaçant 300 Go
de données de production. Sur les cinq mécanismes de sauvegarde en place, aucun
ne fonctionnait correctement. La récupération a été diffusée en direct sur
YouTube, et le postmortem public est devenu un cas d'école en fiabilité
logicielle. Ces incidents ne sont pas des aberrations causées par des
incompétents : ils se produisent dans les organisations les plus sophistiquées du
monde. La question centrale de cette section n'est donc pas "comment éviter
toute panne" — c'est impossible — mais plutôt : comment s'organiser pour
détecter vite, réagir bien, et surtout apprendre de chaque incident ?

Cette philosophie — accepter la faillibilité et s'organiser en conséquence — a
trouvé sa formalisation la plus influente chez Google, sous le nom de *Site
Reliability Engineering* (SRE). Le terme a été inventé par Ben Treynor Sloss,
qui a fondé la première équipe SRE chez Google en 2003. L'idée de départ était
simple : plutôt que de séparer les développeurs (qui écrivent le code) et les
opérateurs (qui le font tourner), pourquoi ne pas confier les opérations à des
ingénieurs logiciels qui abordent les problèmes d'exploitation comme des
problèmes de code ? Un SRE écrit des outils d'automatisation, des systèmes de
monitoring, des scripts de déploiement — il traite la fiabilité comme une
fonctionnalité du système, pas comme une responsabilité extérieure. Google a
formalisé cette approche dans le livre *Site Reliability Engineering* (2016),
disponible gratuitement en ligne, qui est devenu une référence incontournable.
Le SRE n'est pas en opposition avec DevOps : c'est plutôt une implémentation
concrète et opiniâtrée de ses principes. Là où DevOps est une philosophie
(abattre le mur entre dev et ops), le SRE est un ensemble de pratiques
spécifiques pour y arriver.

L'une des idées les plus puissantes du SRE est celle de l'*error budget*, que
nous avons brièvement introduite dans la section sur l'observabilité. Le
raisonnement est le suivant : si un service a un SLO de 99,9 % de
disponibilité, cela signifie qu'on accepte explicitement 0,1 %
d'indisponibilité, soit environ 43 minutes par mois. Ces 43 minutes ne sont pas
un échec : elles sont un *budget* qu'on peut dépenser. Tant qu'il en reste,
l'équipe peut déployer de nouvelles fonctionnalités, prendre des risques,
expérimenter. Quand le budget est épuisé, on gèle les déploiements non
essentiels et on se concentre sur la fiabilité. Ce mécanisme transforme une
tension politique (les développeurs veulent livrer vite, les ops veulent de la
stabilité) en une décision basée sur des données. Il n'y a plus de débat
subjectif : on regarde le budget restant. C'est aussi un antidote à la quête
illusoire du 100 % de disponibilité. Comme le rappelle le livre Google SRE,
viser 100 % est non seulement impossible, mais contre-productif : le coût
marginal de chaque "9" supplémentaire est exponentiel, et les utilisateurs ne
font généralement pas la différence entre 99,99 % et 99,999 % — leur propre
connexion internet est probablement moins fiable que le service qu'ils
utilisent.

## Anatomie d'un incident

Quand un incident survient, la manière dont une organisation réagit suit
généralement un cycle bien défini. La première phase est la **détection** :
quelque chose signale que le système ne fonctionne pas normalement. Idéalement,
c'est une alerte automatique (Prometheus qui détecte que le taux d'erreurs
dépasse un seuil, par exemple) qui donne l'alarme avant même que les
utilisateurs ne s'en rendent compte. En pratique, il arrive encore souvent que
ce soient les utilisateurs eux-mêmes qui signalent le problème, par le support
client ou sur les réseaux sociaux — un signe que l'observabilité du système est
insuffisante. La deuxième phase est le **triage** : évaluer la gravité de
l'incident. Est-ce que ça affecte tous les utilisateurs ou un sous-ensemble ?
Est-ce que des données sont en danger ? La réponse détermine le niveau d'urgence
et les personnes à mobiliser. Vient ensuite la **mitigation** : l'objectif
immédiat n'est pas de comprendre la cause profonde, mais de rétablir le service.
Redémarrer un pod, activer un feature flag pour désactiver la fonctionnalité
problématique, basculer vers une base de données répliquée — on cherche à
limiter l'impact, quitte à appliquer un pansement temporaire. La **résolution**
proprement dite vient après : identifier la cause racine et appliquer un
correctif durable. Enfin, et c'est la phase la plus importante pour
l'apprentissage, le **postmortem** : documenter ce qui s'est passé, pourquoi, et
ce qu'on va changer pour que ça ne se reproduise pas.

Dans les organisations qui prennent la fiabilité au sérieux, la détection d'un
incident ne tombe pas dans le vide : elle déclenche un processus d'astreinte
(*on-call*). Un ingénieur de garde, désigné par rotation, reçoit l'alerte et
devient le premier intervenant. C'est un rôle exigeant : l'astreinte implique
d'être joignable en tout temps pendant la période de garde (souvent une
semaine), y compris la nuit et les fins de semaine. Le livre Google SRE insiste
sur le fait que la charge d'astreinte doit rester soutenable : pas plus de 25 %
du temps d'un ingénieur devrait être consacré au travail opérationnel, le reste
étant dédié à du travail de projet (automatisation, amélioration des outils).
Quand la charge d'astreinte dépasse ce seuil, c'est un signal que le système a
des problèmes de fiabilité structurels qu'il faut adresser. Pour les incidents
majeurs, un rôle distinct émerge : l'*incident commander* (IC). L'IC ne résout
pas le problème lui-même — il coordonne la réponse. Il maintient un canal de
communication (souvent un channel Slack ou une salle de visioconférence dédiée),
assigne les tâches, tient les parties prenantes informées, et prend les
décisions d'escalade. Cette séparation entre coordination et investigation est
cruciale : sans elle, les incidents complexes dégénèrent rapidement en chaos,
avec plusieurs personnes qui tentent des corrections contradictoires en
parallèle.

## Postmortems blameless

La phase d'apprentissage après un incident est souvent la plus négligée, et
pourtant c'est celle qui a le plus de valeur à long terme. Le réflexe naturel
après une panne est de chercher un coupable : qui a fait l'erreur ? Qui a
approuvé ce déploiement ? L'approche *blameless* (sans blâme) prend le
contre-pied de cette tendance. Son postulat est que dans un système complexe,
les erreurs humaines sont presque toujours le symptôme d'un problème systémique,
pas la cause. L'ingénieur d'Amazon qui a provoqué la panne de S3 en 2017 a
exécuté une commande que le système lui permettait d'exécuter, sans garde-fou
suffisant. L'administrateur de GitLab a fait un `rm -rf` parce que la procédure
de récupération n'avait jamais été testée en conditions réelles. Punir ces
individus n'aurait rien changé aux conditions qui ont rendu l'erreur possible —
et aurait eu un effet pervers : dans une culture punitive, les gens cachent
leurs erreurs au lieu de les signaler, ce qui rend les incidents futurs plus
probables et plus graves.

Le postmortem blameless a été popularisé par John Allspaw, alors CTO d'Etsy,
dans un article influent de 2012 intitulé *Blameless PostMortems and a Just
Culture*. Allspaw s'appuyait sur les travaux de Sidney Dekker en sécurité des
systèmes complexes (*The Field Guide to Understanding Human Error*, 2006) et sur
les pratiques de l'aviation et de la médecine, deux domaines où l'analyse non
punitive des incidents a produit des améliorations spectaculaires en sécurité. Un
bon postmortem documente une chronologie détaillée de l'incident, identifie les
facteurs contributifs (pas "la" cause unique), et surtout produit une liste
d'*action items* concrets : corriger le bug, ajouter un garde-fou, améliorer le
monitoring, mettre à jour le runbook. Sans action items, un postmortem n'est
qu'un récit — il ne change rien.

## Chaos engineering

Si les incidents sont inévitables, pourquoi attendre qu'ils surviennent
d'eux-mêmes ? C'est le raisonnement à l'origine du *chaos engineering*, une
discipline qui consiste à provoquer délibérément des pannes dans un système pour
tester sa résilience. L'idée est née chez Netflix en 2010, quand l'entreprise a
migré son infrastructure de ses propres datacenters vers AWS. Pour s'assurer que
ses systèmes pouvaient survivre aux défaillances inévitables du cloud, l'équipe
de Greg Orzell a créé *Chaos Monkey*, un programme qui éteint aléatoirement des
machines virtuelles en production pendant les heures de bureau. Le raisonnement
était simple : si un service ne survit pas à la perte d'une instance, il vaut
mieux le découvrir un mardi à 14 h, quand toute l'équipe est disponible, qu'un
samedi à 3 h du matin. Chaos Monkey a ensuite donné naissance à toute une "armée
du chaos" chez Netflix : *Chaos Kong* (qui simule la perte d'une région AWS
entière), *Latency Monkey* (qui injecte des délais réseau), et d'autres. En
2014, Netflix a publié les *Principles of Chaos Engineering*, un document qui
formalise la discipline autour de quatre principes : formuler une hypothèse sur
le comportement normal du système, varier les conditions réelles (pas juste en
staging), minimiser le rayon d'impact de l'expérience, et automatiser les
expériences pour qu'elles tournent en continu.

Le chaos engineering est étroitement lié à la notion de *game day*, un exercice
planifié où une équipe simule un incident majeur pour tester non seulement la
résilience technique du système, mais aussi la réponse humaine : est-ce que les
alertes se déclenchent ? Est-ce que l'on sait qui appeler ? Est-ce que les
runbooks sont à jour ? Amazon pratique régulièrement des game days à l'échelle de
l'entreprise. L'analogie avec les exercices d'évacuation incendie est parlante :
personne ne trouve absurde de pratiquer une évacuation avant qu'un feu ne se
déclare. Le chaos engineering applique la même logique aux systèmes logiciels.
C'est aussi un lien direct avec la troisième voie de DevOps (l'apprentissage
continu) : chaque expérience de chaos est une occasion d'apprendre quelque chose
sur le système qu'on ne savait pas.

## Runbooks et automatisation

Un runbook est un document qui décrit, étape par étape, la procédure à suivre
pour diagnostiquer et résoudre un type d'incident connu. Par exemple : "si
l'alerte X se déclenche, vérifier d'abord Y, puis essayer Z, et si ça ne
fonctionne pas, escalader à l'équipe W". Les runbooks sont un outil ancien (les
administrateurs système en tenaient depuis bien avant DevOps), mais leur rôle
prend une importance particulière dans le contexte du SRE. Un ingénieur
d'astreinte réveillé à 3 h du matin n'est pas dans les meilleures conditions
pour improviser une solution créative. Un bon runbook lui donne un chemin à
suivre, réduit le temps de résolution, et diminue le risque d'aggraver le
problème par une mauvaise manipulation. Les alertes actionnables que nous avons
vues dans la section sur l'observabilité devraient idéalement pointer vers un
runbook pertinent. L'étape suivante, naturellement, est l'automatisation : quand
un runbook est suffisamment mature et que ses étapes sont déterministes, on peut
le transformer en script ou en mécanisme automatique. Kubernetes fait déjà cela
pour certains cas simples : quand un pod échoue à son health check, le système
le redémarre automatiquement, sans intervention humaine. C'est un runbook qui
est devenu du code.

## La dette technique comme source d'incidents

Il y a un lien direct entre la dette technique, que nous avons abordée dans le
module 4, et la fréquence des incidents en production. Un code mal structuré, des
tests insuffisants, des dépendances obsolètes, une documentation inexistante —
toutes ces formes de dette accumulent silencieusement des risques opérationnels.
Le raccourci pris il y a six mois pour livrer une fonctionnalité à temps devient
le bug mystérieux qui fait tomber le service un vendredi soir. Ward Cunningham,
quand il a introduit la métaphore de la dette en 1992, pensait précisément à ce
phénomène : les intérêts de la dette finissent par se payer, souvent au moment
le moins opportun. Les postmortems révèlent souvent que la cause profonde d'un
incident n'est pas un événement ponctuel, mais l'accumulation progressive de
décisions qui ont dégradé la qualité du système. C'est pourquoi les
organisations matures allouent explicitement du temps au remboursement de la
dette technique, souvent en utilisant les rétrospectives et les postmortems
comme sources pour prioriser ce travail. L'error budget offre un mécanisme
concret pour cela : quand le budget est épuisé par des incidents liés à la
dette, l'équipe est contrainte de s'y attaquer avant de livrer de nouvelles
fonctionnalités.