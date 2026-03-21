---
title: "Est-ce que ça marche ?"
weight: 30
slug: "observabilite"
---

# Est-ce que ça marche ?

Dans les sections précédentes, nous avons vu où déployer un logiciel et comment
l'y amener de manière automatisée. Mais une fois le déploiement terminé, une
question fondamentale se pose : est-ce que ça fonctionne ? Non pas au sens des
tests unitaires, qui vérifient la correction du code avant le déploiement, mais
au sens opérationnel : est-ce que les utilisateurs arrivent à se connecter ?
Est-ce que les requêtes sont traitées dans un temps raisonnable ? Est-ce que le
système consomme ses ressources de manière normale ? Sur la machine d'un
développeur, ces questions ne se posent pas vraiment. On a un debugger, des
`print()`, un terminal sous les yeux. En production, on perd tout ça. Le système
tourne sur des machines distantes, traite des milliers de requêtes simultanées,
et les problèmes qui surviennent sont souvent des problèmes qu'on n'avait pas
anticipés. L'observabilité, c'est l'art de reconstruire cette visibilité à
distance.

Le terme "observabilité" n'est pas né dans le monde du logiciel. Il vient de la
théorie du contrôle, où il a été formalisé par le mathématicien hongrois Rudolf
Kálmán en 1960. Kálmán est surtout connu pour le *filtre de Kálmán*, un
algorithme d'estimation qui est encore aujourd'hui omniprésent en ingénierie :
navigation GPS, pilotage automatique, véhicules autonomes, traitement du signal.
C'est dans ce même cadre théorique qu'il a défini la notion d'observabilité : un
système est dit "observable" si on peut déduire son état interne complet à partir
de ses sorties mesurables. L'analogie avec un système logiciel en production est
frappante : on ne peut pas s'y connecter avec un debugger, mais on peut observer
ce qu'il émet (logs, métriques, réponses HTTP) et en déduire ce qui se passe à
l'intérieur. C'est Charity Majors, cofondatrice de Honeycomb, qui a le plus
contribué à populariser ce terme dans l'industrie logicielle à partir de
2017-2018, en le distinguant explicitement du *monitoring* traditionnel. La
distinction est importante : le monitoring consiste à surveiller des indicateurs
connus à l'avance ("est-ce que l'utilisation CPU dépasse 90 % ?", "est-ce que le
taux d'erreurs dépasse 1 % ?"). L'observabilité va plus loin : elle vise à
permettre l'exploration de questions qu'on n'avait *pas* anticipées. Quand un
utilisateur signale que "c'est lent depuis ce matin", un bon système
d'observabilité permet de creuser la question en temps réel, en corrélant des
signaux de différentes sources, sans avoir à déployer de nouvelles sondes.

Cette capacité à comprendre un système en production correspond directement à la
deuxième voie de DevOps identifiée par Gene Kim : celle du *feedback*. La
première voie (le *flow*) accélère le mouvement du code vers la production,
c'est ce que nous avons vu avec l'infrastructure et le déploiement continu. La
deuxième voie crée le flux inverse : des signaux qui remontent de la production
vers les équipes de développement. Sans ce flux de retour, on déploie à
l'aveugle. On peut livrer du code rapidement, mais on ne sait pas si ce code
fonctionne bien pour les utilisateurs réels, dans les conditions réelles.
L'observabilité est le mécanisme concret qui rend cette boucle de rétroaction
possible.

La suite de cette section s'organise autour de ce que l'on appelle couramment
les trois piliers de l'observabilité : les **logs** (un enregistrement textuel
des événements), les **métriques** (des mesures numériques agrégées dans le
temps) et les **traces** (le suivi du parcours d'une requête à travers les
composants d'un système). Chacun de ces piliers répond à un type de question
différent. Les logs racontent *ce qui s'est passé*. Les métriques montrent
*comment le système se porte*. Les traces expliquent *pourquoi une opération est
lente ou échoue*. Après avoir exploré ces trois piliers, nous verrons comment
les alertes permettent de transformer ces signaux en actions, puis comment les
SLIs, SLOs et SLAs formalisent la notion de fiabilité du point de vue de
l'utilisateur. Enfin, un tutoriel pratique montrera comment instrumenter une
application FastAPI et visualiser ses métriques en temps réel avec Prometheus et
Grafana dans un cluster Kubernetes local.

## Les logs

L'outil d'observabilité le plus ancien et le plus intuitif est le log : un
enregistrement textuel d'un événement qui s'est produit dans le système. Tout
développeur a déjà écrit un `print()` pour comprendre le comportement de son
code. Quand une fonction ne retourne pas le résultat attendu, le premier réflexe
est souvent d'insérer des `print()` stratégiques pour suivre le fil de
l'exécution :

```python
def calculer_prix(produit, quantite, code_promo=None):
    prix = produit["prix"] * quantite
    print(f"prix de base: {prix}")

    if code_promo and code_promo in PROMOS_VALIDES:
        rabais = PROMOS_VALIDES[code_promo]
        prix *= (1 - rabais)
        print(f"promo {code_promo} appliquée, rabais de {rabais*100}%")
    else:
        print(f"pas de promo (code_promo={code_promo})")

    if quantite >= 10:
        prix *= 0.95
        print("rabais volume appliqué")

    print(f"prix final: {prix}")
    return prix
```

Ce réflexe, universel et efficace pour le débogage local, a un problème
fondamental : il ne survit pas au passage en production. Les `print()` n'ont pas
de niveau de sévérité, pas d'horodatage, pas de contexte structuré. On ne peut
pas les filtrer, les chercher efficacement, ni les désactiver sans modifier le
code. Le log est la version disciplinée de ce réflexe.

Sous Unix, la notion de journal système est formalisée depuis 1983 avec syslog,
conçu par Eric Allman (qui est aussi l'auteur de Sendmail). Le protocole syslog
introduisait déjà les concepts fondamentaux qu'on retrouve aujourd'hui : des
niveaux de sévérité (DEBUG, INFO, WARNING, ERROR, CRITICAL), une source
identifiée, et un horodatage. Chaque message avait une gravité, ce qui
permettait de filtrer le bruit et de se concentrer sur les événements
significatifs.

En Python, le module `logging` de la bibliothèque standard permet de passer du
`print()` à un vrai système de logs en quelques lignes :

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculer_prix(produit, quantite, code_promo=None):
    prix = produit["prix"] * quantite
    logger.info(f"Calcul du prix pour {produit['nom']}, quantité={quantite}")

    if code_promo and code_promo in PROMOS_VALIDES:
        rabais = PROMOS_VALIDES[code_promo]
        prix *= (1 - rabais)
        logger.info(f"Promo {code_promo} appliquée, rabais de {rabais*100}%")
    else:
        logger.debug(f"Pas de promo (code_promo={code_promo})")

    if quantite >= 10:
        prix *= 0.95
        logger.info("Rabais volume appliqué")

    logger.info(f"Prix final: {prix}")
    return prix
```

On gagne immédiatement plusieurs choses : un horodatage automatique, des niveaux
de sévérité qui permettent de filtrer (en production, on peut n'afficher que les
WARNING et plus, sans toucher au code), et un nom de source (`__name__`) qui
identifie quel module a émis le message. Mais ces logs restent du texte libre,
des chaînes de caractères destinées à l'œil humain. Quand un système produit des
milliers de lignes de logs par seconde, lire du texte ne suffit plus. Il faut
pouvoir chercher, filtrer et agréger automatiquement. C'est ce qui a motivé le
passage au **log structuré**.

L'idée est simple : au lieu d'émettre une ligne de texte formatée pour un
humain, on émet un objet JSON contenant des champs nommés. Plutôt que :

```
2025-03-15 14:23:01 INFO Promo PRINTEMPS20 appliquée, rabais de 20%
```

on émet :

```json
{
  "timestamp": "2025-03-15T14:23:01.342Z",
  "level": "INFO",
  "message": "Promo appliquée",
  "code_promo": "PRINTEMPS20",
  "rabais": 0.2,
  "produit": "Widget Pro",
  "prix_avant": 150.0,
  "prix_apres": 120.0
}
```

La différence est considérable. Avec du texte, pour trouver toutes les
applications de la promo PRINTEMPS20, il faut écrire une expression régulière
fragile. Avec du JSON, c'est une simple requête sur un champ. On peut calculer
le rabais moyen accordé, filtrer par produit, agréger par période. Les logs
deviennent des données interrogeables, pas juste un journal qu'on feuillette.

C'est cette transition vers le log structuré qui a rendu possible l'émergence de
plateformes centralisées d'analyse de logs. La plus emblématique est la stack
**ELK**, un acronyme pour trois projets open source complémentaires :
**Elasticsearch** (un moteur de recherche et d'indexation, que nous avons
rencontré dans la section sur les données du module 3), **Logstash** (un
pipeline d'ingestion qui collecte, transforme et achemine les logs) et
**Kibana** (une interface web de visualisation et d'exploration). Apparue vers
2012-2014, la stack ELK a transformé la gestion des logs en permettant, pour la
première fois de manière accessible, de centraliser les logs de dizaines ou
centaines de services dans un même endroit et de les interroger en temps réel. Un
développeur pouvait taper une requête dans Kibana et retrouver en quelques
secondes un événement spécifique parmi des millions de lignes de logs.
Aujourd'hui, des alternatives commerciales et open source existent (Datadog,
Grafana Loki, Splunk), mais le principe reste le même : les logs sont collectés,
indexés et rendus cherchables depuis une interface centralisée.

Cette idée de centralisation rejoint directement le **facteur XI** de la
Twelve-Factor App : *"Logs — Treat logs as event streams"*. Le principe est que
l'application ne devrait jamais se préoccuper du stockage ou du routage de ses
logs. Elle ne devrait pas écrire dans un fichier, ni gérer la rotation des
fichiers, ni décider où les logs sont envoyés. Son seul rôle est d'émettre ses
logs sur la sortie standard (`stdout`), comme un flux continu d'événements.
C'est l'environnement d'exécution (le conteneur Docker, l'orchestrateur
Kubernetes, la plateforme cloud) qui se charge de capturer ce flux et de
l'acheminer vers la bonne destination : un fichier local en développement, un
agrégateur ELK en production, un service cloud comme CloudWatch. Cette séparation
des responsabilités est élégante : l'application reste simple et portable, et la
stratégie de gestion des logs peut changer sans modifier une seule ligne de code.

## Les métriques

Les logs racontent des événements individuels : telle requête a été reçue, telle
erreur s'est produite, telle promo a été appliquée. Mais quand un système traite
des milliers de requêtes par seconde, les événements individuels deviennent trop
nombreux pour donner une vue d'ensemble. On a besoin d'un autre type de signal :
des **métriques**, c'est-à-dire des mesures numériques agrégées dans le temps.
Combien de requêtes par seconde ? Quel temps de réponse moyen ? Quel pourcentage
d'erreurs ? Les métriques ne racontent pas ce qui s'est passé pour une requête
particulière, elles montrent comment le système se porte globalement. Si les logs
sont l'équivalent d'un journal de bord, les métriques sont le tableau de bord.

Le livre *Site Reliability Engineering* (2016), publié par Google, a formalisé
cette idée en proposant les **quatre golden signals**, quatre métriques qu'il
faut surveiller en priorité pour n'importe quel service :

- **La latence** : le temps que prend le système pour répondre à une requête. Il
  est important de distinguer la latence des requêtes réussies de celle des
  requêtes en erreur, car une erreur retournée en 2 millisecondes peut masquer
  un problème si on ne regarde que la moyenne.
- **Le trafic** : le volume de demandes que le système reçoit. Pour une API web,
  c'est typiquement le nombre de requêtes HTTP par seconde. Cette métrique donne
  le contexte : une latence élevée n'a pas la même signification à 10 requêtes
  par seconde qu'à 10 000.
- **Les erreurs** : le taux de requêtes qui échouent, que ce soit explicitement
  (codes HTTP 5xx) ou implicitement (une réponse 200 qui contient un résultat
  incorrect, ou une réponse qui dépasse un seuil de latence acceptable).
- **La saturation** : à quel point le système est proche de ses limites. C'est
  la mesure de la capacité restante : utilisation CPU, mémoire, nombre de
  connexions à la base de données, espace disque. La saturation est le signal
  d'alerte précoce : les problèmes de latence et d'erreurs surviennent souvent
  quand un système approche de la saturation.

Avant Prometheus, l'approche dominante pour la collecte de métriques reposait sur
un modèle *push* : c'est l'application qui envoie activement ses métriques vers
un serveur de collecte. **Graphite**, créé par Chris Davis chez Orbitz en 2008, a
été l'un des premiers systèmes open source à offrir une solution complète de
stockage et de visualisation de métriques sous forme de séries temporelles.
Quelques années plus tard, **StatsD**, développé par l'équipe d'Etsy en 2011 et
présenté dans un billet de blogue devenu célèbre (*"Measure Anything, Measure
Everything"*), a simplifié l'instrumentation côté application : quelques lignes
de code suffisaient pour envoyer un compteur ou un timer via UDP vers un serveur
StatsD, qui agrégeait les données avant de les transmettre à Graphite. Le duo
StatsD + Graphite a démocratisé l'idée que les métriques n'étaient pas réservées
aux équipes d'opérations, que les développeurs eux-mêmes devaient instrumenter
leur code. C'est dans ce contexte que Prometheus a émergé, en proposant une
approche différente.

L'outil qui a fini par s'imposer comme standard dans les architectures
cloud-native est **Prometheus**. Son histoire est intimement liée à celle de
Google et de Kubernetes. En interne, Google utilisait un système appelé Borgmon
pour surveiller les services déployés sur Borg, son orchestrateur de conteneurs
(l'ancêtre de Kubernetes, comme nous l'avons vu dans la section sur
l'infrastructure). Quand d'anciens ingénieurs de Google ont fondé SoundCloud, ils
ont voulu recréer un outil similaire pour le monde open source. Le résultat,
Prometheus, a été rendu public en 2012 et est devenu un projet de la Cloud Native
Computing Foundation (CNCF) en 2016, le deuxième après Kubernetes lui-même.

Le fonctionnement de Prometheus repose sur un modèle *pull* : plutôt que les
applications poussent leurs métriques vers un serveur central, c'est Prometheus
qui interroge périodiquement (par défaut toutes les 15 secondes) un endpoint
HTTP exposé par chaque application, typiquement `/metrics`. Cet endpoint
retourne les métriques dans un format textuel simple. L'application n'a besoin
d'aucune connaissance de Prometheus : elle expose ses métriques, et c'est tout.
Cette approche rejoint la philosophie du facteur XI de la Twelve-Factor App que
nous avons vue pour les logs : l'application émet des signaux, l'infrastructure
se charge de les collecter.

Prometheus définit quatre types fondamentaux de métriques, chacun adapté à un
type de mesure différent. Le **counter** est un compteur qui ne fait
qu'augmenter : le nombre total de requêtes reçues, le nombre d'erreurs
survenues. On ne regarde jamais la valeur absolue d'un counter (qui augmente
indéfiniment), mais son *taux de variation* : combien de requêtes par seconde,
combien d'erreurs par minute. Le **gauge** est une valeur qui monte et descend
librement : l'utilisation CPU, la mémoire consommée, le nombre de connexions
actives à un instant donné. C'est une photographie instantanée de l'état du
système. Le **histogram** enregistre la distribution d'une valeur, typiquement la
latence des requêtes. Plutôt qu'une simple moyenne (qui peut masquer des
problèmes), un histogram permet de calculer des **percentiles** : le p50 (la
latence médiane), le p95 (la latence en dessous de laquelle tombent 95 % des
requêtes) et le p99. La distinction entre ces percentiles est cruciale : un
service peut avoir une latence médiane excellente de 20 ms tout en ayant un p99
de 3 secondes, ce qui signifie qu'un utilisateur sur cent a une expérience
dégradée. Enfin, le **summary** est similaire au histogram mais calcule les
percentiles directement côté application plutôt que côté Prometheus ; il est
moins flexible et moins couramment utilisé.

En Python, la bibliothèque `prometheus_client` permet d'instrumenter une
application en quelques lignes :

```python
from prometheus_client import Counter, Gauge, Histogram

# Counter : combien de requêtes au total ?
requetes_total = Counter(
    "http_requetes_total",
    "Nombre total de requêtes HTTP",
    ["methode", "endpoint", "status"]
)

# Gauge : combien de connexions en ce moment ?
connexions_actives = Gauge(
    "connexions_actives",
    "Nombre de connexions actives"
)

# Histogram : quelle est la distribution de la latence ?
latence = Histogram(
    "http_latence_secondes",
    "Latence des requêtes HTTP en secondes",
    ["endpoint"]
)
```

Chaque type s'utilise naturellement dans le code. On incrémente un counter quand
un événement se produit (`requetes_total.labels(methode="GET", endpoint="/prix",
status="200").inc()`), on ajuste un gauge quand un état change
(`connexions_actives.inc()` à l'ouverture, `connexions_actives.dec()` à la
fermeture), et on observe une valeur dans un histogram pour alimenter la
distribution (`latence.labels(endpoint="/prix").observe(0.042)`).

Pour que ces métriques soient utiles, il faut pouvoir les visualiser. C'est le
rôle de **Grafana**, un outil open source de visualisation créé en 2014 par
Torkel Ödegaard. Grafana se connecte à Prometheus (et à de nombreuses autres
sources de données) et permet de construire des tableaux de bord (*dashboards*)
composés de graphiques, de jauges et de tableaux. On peut voir en temps réel
l'évolution du trafic, la latence par percentile, le taux d'erreurs, la
saturation des ressources. Le couple Prometheus + Grafana est devenu un standard
de facto dans l'écosystème cloud-native, au point que la plupart des tutoriels
Kubernetes incluent leur installation comme étape de base. Nous les utiliserons
ensemble dans le tutoriel pratique à la fin de cette section.

## Le tracing distribué

Les logs racontent ce qui s'est passé à un endroit précis du système. Les
métriques donnent une vue d'ensemble agrégée. Mais dans une architecture
distribuée, où une seule requête utilisateur peut traverser cinq, dix, voire
vingt services différents avant de produire une réponse, il manque un troisième
angle : la capacité de suivre le **parcours complet** d'une requête à travers
tous les composants qu'elle traverse. C'est le rôle du tracing distribué.

Prenons un exemple concret. Un utilisateur clique sur "Confirmer la commande"
dans une application web. Cette action déclenche une requête HTTP vers un service
API, qui appelle un service d'inventaire pour vérifier la disponibilité, un
service de paiement pour débiter la carte, un service de notification pour
envoyer un courriel de confirmation, et un service d'analytique pour enregistrer
l'événement. Si l'utilisateur signale que "la confirmation est lente", où est le
problème ? Le service de paiement met-il trop de temps à répondre ? Le service
d'inventaire fait-il une requête coûteuse à la base de données ? Le problème
est-il dans le réseau entre deux services ? Sans tracing, répondre à ces
questions exige de fouiller manuellement dans les logs de chaque service et de
tenter de corréler les événements par horodatage, un exercice pénible et
fragile.

Le concept moderne de tracing distribué a été formalisé par Google dans le papier
**Dapper** (2010), qui décrivait le système interne utilisé pour tracer les
requêtes à travers l'infrastructure massive de Google. L'idée centrale de Dapper
est élégante : quand une requête entre dans le système, on lui assigne un
identifiant unique (un *trace ID*) qui est propagé de service en service via les
en-têtes HTTP. Chaque service enregistre un **span**, une unité de travail avec
un début, une fin, et des métadonnées (quel service, quelle opération, combien
de temps). L'ensemble des spans d'une requête, reliés entre eux par des
relations parent-enfant, forme une **trace** : une arborescence qui représente le
parcours complet de la requête. En visualisant cette arborescence, on voit
immédiatement où le temps est passé.

Le papier Dapper a inspiré une série d'implémentations open source. **Zipkin**,
développé par Twitter et rendu public en 2012, a été le premier à rendre le
tracing distribué accessible en dehors de Google. **Jaeger**, créé par Uber en
2017 et nommé d'après le mot allemand pour "chasseur", a suivi avec une
architecture plus moderne et une intégration native avec Kubernetes. Pendant
plusieurs années, deux standards concurrents coexistaient pour l'instrumentation :
OpenTracing (une API indépendante du fournisseur) et OpenCensus (un projet de
Google qui couvrait à la fois le tracing et les métriques). En 2019, les deux
projets ont fusionné pour former **OpenTelemetry**, souvent abrégé OTel, sous
l'égide de la CNCF. OpenTelemetry est aujourd'hui le standard qui unifie les
trois piliers de l'observabilité : il fournit des bibliothèques
d'instrumentation pour les logs, les métriques et les traces, dans la plupart
des langages, avec un format de données commun et un protocole d'export unifié
(OTLP). L'idée est qu'un développeur instrumente son code une seule fois avec
OpenTelemetry, et peut ensuite envoyer les données vers Jaeger, Prometheus,
Grafana, Datadog ou n'importe quel autre backend, sans modifier le code
d'instrumentation.

<!-- ILLUSTRATION: diagramme montrant une trace distribuée avec plusieurs spans imbriqués (API → inventaire, API → paiement → banque, API → notification), avec le trace ID qui se propage, et une timeline montrant la durée de chaque span -->

Le tracing distribué est le pilier le plus récent et le plus complexe à mettre
en place des trois. Il nécessite que chaque service propage correctement le trace
ID, ce qui demande une discipline d'équipe ou l'utilisation de bibliothèques qui
le font automatiquement. Pour cette raison, beaucoup d'organisations commencent
par les logs et les métriques, et n'ajoutent le tracing que lorsque la complexité
de leur architecture le justifie. Mais quand un système atteint une certaine
taille, le tracing devient indispensable : c'est le seul outil qui permet de
répondre à la question "pourquoi *cette* requête est-elle lente ?", plutôt que
"est-ce que le système est lent en général ?". Il faut noter que la granularité
typique du tracing se situe au niveau des interactions entre composants (appels
HTTP, requêtes à la base de données, messages dans une file d'attente), pas au
niveau de chaque appel de fonction interne. Pour ce niveau de détail, on utilise
des **profilers**, des outils qui mesurent le temps passé dans chaque fonction
d'un programme. Le tracing et le profiling sont complémentaires : le premier
identifie *quel service* est le goulot d'étranglement, le second identifie
*quelle fonction* à l'intérieur de ce service.

## Les alertes

Les logs, les métriques et les traces sont des outils d'investigation : ils
permettent de comprendre ce qui se passe dans un système. Mais ils supposent que
quelqu'un regarde. Or personne ne surveille un dashboard Grafana 24 heures sur
24. Les alertes sont le mécanisme qui transforme les signaux passifs en actions :
quand une métrique franchit un seuil préoccupant, le système notifie
automatiquement les personnes concernées, par courriel, message Slack,
notification PagerDuty, ou SMS à trois heures du matin.

Le principe semble simple, mais en pratique, concevoir un bon système d'alertes
est étonnamment difficile. Le piège le plus courant est la **fatigue d'alerte**
(*alert fatigue*) : quand un système génère trop d'alertes, trop souvent, pour
des problèmes mineurs ou des faux positifs, les opérateurs finissent par les
ignorer. C'est le syndrome du garçon qui crie au loup. Des études dans le
domaine médical (où le problème est bien documenté pour les moniteurs de
patients) ont montré que les taux de faux positifs peuvent dépasser 90 %, ce qui
conduit le personnel à désactiver les alarmes ou à les traiter machinalement. Le
même phénomène se produit dans les équipes logicielles : une équipe qui reçoit
des dizaines d'alertes par jour finit par ne plus réagir à aucune, y compris aux
alertes légitimes.

Le livre *Site Reliability Engineering* de Google propose un principe directeur
pour éviter ce piège : chaque alerte doit être **actionnable**. Si une alerte se
déclenche, la personne qui la reçoit doit pouvoir faire quelque chose d'utile
immédiatement. Si la réponse habituelle à une alerte est "on la ferme et on
ignore", c'est que l'alerte ne devrait pas exister. Google distingue trois
niveaux de notification. Les **alertes** proprement dites (pages) sont réservées
aux problèmes qui nécessitent une intervention humaine immédiate : le service est
en panne, les utilisateurs sont affectés. Les **tickets** sont créés
automatiquement pour les problèmes qui nécessitent une action, mais pas dans
l'immédiat : un disque qui se remplit lentement, un certificat TLS qui expire
dans deux semaines. Les **logs** suffisent pour tout le reste : les anomalies
mineures qu'il est utile de pouvoir retrouver lors d'une investigation, mais qui
ne justifient pas d'interrompre quelqu'un.

En pratique, une bonne alerte repose sur quelques principes. D'abord, alerter
sur les **symptômes** plutôt que sur les **causes**. Alerter quand le taux
d'erreurs dépasse 1 % (un symptôme visible par l'utilisateur) est plus utile
qu'alerter quand l'utilisation CPU dépasse 80 % (une cause potentielle qui n'a
peut-être aucun impact). Ensuite, utiliser des **seuils réalistes** avec des
fenêtres de temps suffisantes pour absorber les pics normaux : un bref pic de
latence pendant 30 secondes n'est pas la même chose qu'une dégradation soutenue
pendant 10 minutes. Enfin, chaque alerte devrait idéalement être accompagnée
d'un **runbook**, un document qui décrit les étapes de diagnostic et de
résolution à suivre quand elle se déclenche. Un runbook transforme la réponse aux
incidents d'un art qui dépend de l'expertise individuelle en un processus
reproductible.

## SLIs, SLOs et SLAs

Les métriques et les alertes nous disent comment le système se porte du point de
vue technique. Mais un CPU à 75 % ou une latence p99 de 200 ms, est-ce que c'est
*bien* ? Est-ce que c'est *suffisant* ? La réponse dépend du contexte, et surtout
du point de vue qu'on adopte. Les SLIs, SLOs et SLAs sont un cadre formalisé
principalement par Google dans le livre *Site Reliability Engineering* pour
répondre à cette question en se plaçant du point de vue de l'**utilisateur**, pas
de l'infrastructure.

Un **SLI** (*Service Level Indicator*) est une mesure quantitative d'un aspect
du service tel que l'utilisateur le perçoit. Ce n'est pas l'utilisation CPU ou la
mémoire disponible, ce sont des métriques internes à l'infrastructure. Un SLI
mesure quelque chose que l'utilisateur ressent directement : la proportion de
requêtes qui réussissent (disponibilité), la proportion de requêtes servies en
moins de 300 ms (latence), la proportion de données correctement traitées
(exactitude). Le SLI est typiquement exprimé comme un ratio : le nombre de
"bonnes" interactions divisé par le nombre total d'interactions, ce qui donne un
pourcentage.

Un **SLO** (*Service Level Objective*) est une cible fixée sur un SLI. Par
exemple : "99,9 % des requêtes doivent réussir sur une fenêtre glissante de 30
jours", ou "95 % des requêtes doivent être servies en moins de 300 ms". Le choix
du SLO est une décision d'ingénierie et de produit, pas une décision purement
technique. Un SLO de 99,99 % de disponibilité (environ 4 minutes
d'indisponibilité autorisées par mois) exige une architecture radicalement
différente d'un SLO de 99 % (environ 7 heures par mois). Chaque "9"
supplémentaire coûte exponentiellement plus cher en complexité, en redondance et
en effort opérationnel. Le SLO est un outil pour rendre ce compromis explicite :
il force une conversation entre les équipes techniques, le produit et la
direction sur le niveau de fiabilité qui est réellement nécessaire.

Un **SLA** (*Service Level Agreement*) est un contrat formel entre un
fournisseur de service et ses clients, qui engage des conséquences (typiquement
financières) si les objectifs ne sont pas atteints. Les SLAs des fournisseurs
cloud sont un exemple familier : AWS garantit 99,99 % de disponibilité pour EC2,
et offre des crédits si ce seuil n'est pas respecté. Un SLA est toujours moins
ambitieux que le SLO interne : si le SLO interne vise 99,95 %, le SLA externe
pourrait promettre 99,9 %, avec une marge de sécurité pour éviter de déclencher
des pénalités contractuelles. Beaucoup d'organisations ont des SLOs sans avoir de
SLAs formels : le SLO reste un outil interne de pilotage, même en l'absence de
contrat.

L'un des concepts les plus puissants qui découlent des SLOs est celui d'**error
budget** (budget d'erreur). Si le SLO de disponibilité est de 99,9 % sur 30
jours, cela signifie que le service a "droit" à 0,1 % d'indisponibilité, soit
environ 43 minutes par mois. Ce budget d'erreur n'est pas un défaut à tolérer,
c'est une **ressource à dépenser**. Tant qu'il reste du budget, l'équipe peut
prendre des risques : déployer plus souvent, tenter des migrations, expérimenter.
Quand le budget est épuisé, on ralentit : moins de déploiements, plus de focus
sur la fiabilité. L'error budget transforme la tension traditionnelle entre
développeurs (qui veulent livrer vite) et opérations (qui veulent de la
stabilité) en une décision basée sur des données plutôt que sur des opinions.
C'est une incarnation concrète de la troisième voie de DevOps : l'apprentissage
continu et la prise de risque calculée. Nous reviendrons sur ce concept dans la
prochaine section, consacrée à la gestion des incidents.

## Tutoriel : observer une application en temps réel

Nous avons décrit les concepts de l'observabilité de manière abstraite. Pour les
rendre concrets, nous allons instrumenter une petite application FastAPI avec des
métriques Prometheus, la déployer dans un cluster Kubernetes local (avec k3d, que
nous avons utilisé dans la section sur l'infrastructure), et visualiser ses
métriques en temps réel dans un dashboard Grafana. L'objectif est de voir, de
bout en bout, comment le code d'une application se transforme en courbes sur un
écran.

### L'application

Notre application est un petit service de citations aléatoires, avec trois
endpoints :

```python
import time
import random
import logging

from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

REQUETES = Counter(
    "http_requetes_total",
    "Nombre total de requêtes HTTP",
    ["methode", "endpoint", "status"],
)

LATENCE = Histogram(
    "http_latence_secondes",
    "Latence des requêtes HTTP en secondes",
    ["endpoint"],
)

CITATIONS = [
    "Il semble que la perfection soit atteinte non quand il n'y a plus rien "
    "à ajouter, mais quand il n'y a plus rien à retrancher. "
    "— Antoine de Saint-Exupéry",
    "Premature optimization is the root of all evil. — Donald Knuth",
    "There are only two hard things in Computer Science: cache invalidation "
    "and naming things. — Phil Karlton",
    "Any fool can write code that a computer can understand. Good programmers "
    "write code that humans can understand. — Martin Fowler",
    "Simplicity is prerequisite for reliability. — Edsger Dijkstra",
]


@app.get("/")
def index():
    start = time.time()
    REQUETES.labels(methode="GET", endpoint="/", status="200").inc()
    LATENCE.labels(endpoint="/").observe(time.time() - start)
    return {"message": "Bienvenue! Essayez /quote pour une citation aléatoire."}


@app.get("/quote")
def quote():
    start = time.time()
    # Simuler une latence variable (entre 10ms et 500ms)
    delay = random.uniform(0.01, 0.5)
    time.sleep(delay)
    citation = random.choice(CITATIONS)
    logger.info(f"Citation servie en {delay:.3f}s")
    REQUETES.labels(methode="GET", endpoint="/quote", status="200").inc()
    LATENCE.labels(endpoint="/quote").observe(time.time() - start)
    return {"quote": citation}


@app.get("/error")
def error():
    start = time.time()
    # Simuler une erreur 50% du temps
    if random.random() < 0.5:
        REQUETES.labels(methode="GET", endpoint="/error", status="500").inc()
        LATENCE.labels(endpoint="/error").observe(time.time() - start)
        logger.error("Erreur simulée sur /error")
        return Response(
            content='{"error": "Erreur interne simulée"}', status_code=500
        )
    REQUETES.labels(methode="GET", endpoint="/error", status="200").inc()
    LATENCE.labels(endpoint="/error").observe(time.time() - start)
    return {"message": "Pas d'erreur cette fois!"}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

L'application a trois comportements distincts qui rendront les métriques
intéressantes. L'endpoint `/` répond instantanément. L'endpoint `/quote` simule
une latence variable (entre 10 et 500 millisecondes) pour produire une
distribution de latence réaliste. L'endpoint `/error` simule une erreur 50 % du
temps, ce qui nous donnera un taux d'erreurs visible dans les métriques.
L'endpoint `/metrics` expose les données au format Prometheus.

On retrouve les types de métriques que nous avons vus plus haut. `REQUETES` est
un **counter** avec trois labels (méthode HTTP, endpoint, code de statut), qui
nous permettra de calculer le trafic par seconde et le taux d'erreurs. `LATENCE`
est un **histogram** par endpoint, qui nous donnera les percentiles de latence.
L'instrumentation est manuelle : au début de chaque handler, on note le temps, et
à la fin, on incrémente le counter et on observe la latence dans l'histogram.

### Déploiement dans Kubernetes

Le Dockerfile est minimal : une image Python, les dépendances installées avec
pip, et uvicorn comme serveur ASGI :

```dockerfile
FROM python:3.12-slim

RUN pip install fastapi uvicorn prometheus-client

COPY main.py /app/

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Créons le cluster k3d, construisons l'image et importons-la :

```shell
$ k3d cluster create obs-demo -p "8080:80@loadbalancer"
$ docker build -t quotes-api .
$ k3d image import quotes-api:latest -c obs-demo
```

Le Deployment demande deux répliques de notre application, ce qui est réaliste
pour un service en production et nous permettra de voir les métriques agrégées de
plusieurs instances :

```yaml
# app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quotes-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: quotes-api
  template:
    metadata:
      labels:
        app: quotes-api
    spec:
      containers:
        - name: quotes-api
          image: quotes-api:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 8000
```

Le Service et l'Ingress rendent l'application accessible depuis l'extérieur du
cluster, comme dans le tutoriel précédent :

```yaml
# app-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: quotes-api
spec:
  selector:
    app: quotes-api
  ports:
    - port: 8000
      targetPort: 8000
```

```yaml
# app-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: quotes-api
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: quotes-api
                port:
                  number: 8000
```

Appliquons le tout :

```shell
$ kubectl apply -f app-deployment.yaml -f app-service.yaml -f app-ingress.yaml
```

Vérifions que l'application répond :

```shell
$ curl http://localhost:8080/quote
{"quote":"Simplicity is prerequisite for reliability. — Edsger Dijkstra"}
```

Et surtout, vérifions que l'endpoint `/metrics` expose bien les données au
format Prometheus :

```shell
$ curl http://localhost:8080/metrics
# HELP http_requetes_total Nombre total de requêtes HTTP
# TYPE http_requetes_total counter
http_requetes_total{methode="GET",endpoint="/quote",status="200"} 1.0
# HELP http_latence_secondes Latence des requêtes HTTP en secondes
# TYPE http_latence_secondes histogram
http_latence_secondes_bucket{endpoint="/quote",le="0.005"} 0.0
http_latence_secondes_bucket{endpoint="/quote",le="0.01"} 0.0
...
```

On voit ici le format textuel de Prometheus : chaque métrique est identifiée par
son nom et ses labels, avec une ligne `HELP` (description) et une ligne `TYPE`
(counter, histogram, etc.). Pour l'histogram, Prometheus crée automatiquement des
*buckets* (des tranches de valeurs) qui permettront de calculer les percentiles.

### Déployer Prometheus

Prometheus a besoin de savoir quelles cibles scraper. Cette configuration se fait
via un fichier `prometheus.yml`, que nous fournissons sous forme de ConfigMap
Kubernetes :

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: "quotes-api"
        static_configs:
          - targets: ["quotes-api:8000"]
```

La configuration est minimale : on dit à Prometheus d'interroger le service
`quotes-api` sur le port 8000 toutes les 15 secondes. Prometheus ira
automatiquement chercher l'endpoint `/metrics` à cette adresse. Le nom
`quotes-api` fonctionne comme nom de domaine à l'intérieur du cluster grâce au
Service Kubernetes que nous avons créé, de la même manière que `redis`
fonctionnait dans le tutoriel précédent.

Le Deployment de Prometheus monte ce ConfigMap comme volume pour que le conteneur
y ait accès :

```yaml
# prometheus-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus:latest
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: config
              mountPath: /etc/prometheus/prometheus.yml
              subPath: prometheus.yml
      volumes:
        - name: config
          configMap:
            name: prometheus-config
```

```yaml
# prometheus-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: prometheus
spec:
  selector:
    app: prometheus
  ports:
    - port: 9090
      targetPort: 9090
```

Appliquons le tout :

```shell
$ kubectl apply -f prometheus-config.yaml -f prometheus-deployment.yaml \
    -f prometheus-service.yaml
```

Pour accéder à l'interface web de Prometheus, on utilise `kubectl port-forward`,
qui crée un tunnel entre notre machine locale et le service à l'intérieur du
cluster :

```shell
$ kubectl port-forward svc/prometheus 9090:9090
```

En ouvrant `http://localhost:9090/targets` dans le navigateur, on peut vérifier
que Prometheus scrape bien notre application. La cible `quotes-api` devrait
apparaître en état "UP", avec la date du dernier scrape.

<!-- ILLUSTRATION: capture d'écran de l'interface Prometheus montrant la cible quotes-api en état UP -->

### Visualiser avec Grafana

Prometheus collecte et stocke les métriques, mais son interface de visualisation
est rudimentaire. Pour construire un vrai dashboard, on déploie Grafana dans le
cluster. La configuration nécessite trois éléments : dire à Grafana où trouver
Prometheus (le datasource), lui fournir un dashboard préconfiguré, et déployer le
conteneur lui-même.

Le datasource est fourni via un ConfigMap de provisioning. L'`uid` fixe
(`prometheus`) permet au dashboard de référencer cette source de données de
manière stable :

```yaml
# grafana-datasource.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasource
data:
  datasource.yml: |
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        uid: prometheus
        access: proxy
        url: http://prometheus:9090
        isDefault: true
```

Le dashboard est un fichier JSON, fourni lui aussi via ConfigMap. Grafana permet
de provisionner des dashboards automatiquement au démarrage : un premier
ConfigMap indique le dossier où chercher les fichiers JSON, et un second contient
le dashboard lui-même. Notre dashboard comporte quatre panneaux qui correspondent
aux quatre golden signals :

```yaml
# grafana-dashboard.yaml (provider)
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-provider
data:
  dashboard.yml: |
    apiVersion: 1
    providers:
      - name: default
        folder: ""
        type: file
        options:
          path: /var/lib/grafana/dashboards
```

Le JSON du dashboard définit quatre panneaux. Le premier affiche le **trafic**
(requêtes par seconde, décomposées par endpoint et code de statut) en utilisant
la fonction `rate()` de Prometheus, qui calcule le taux de variation d'un
counter. Le deuxième montre le **taux d'erreurs** en pourcentage. Le troisième
affiche la **latence** par percentile (p50, p95, p99) en utilisant
`histogram_quantile()`. Le quatrième est un simple compteur du **nombre total de
requêtes**.

Le Deployment de Grafana monte les trois ConfigMaps comme volumes et configure
l'accès anonyme pour simplifier le tutoriel (en production, on configurerait
évidemment une authentification) :

```yaml
# grafana-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
        - name: grafana
          image: grafana/grafana:latest
          ports:
            - containerPort: 3000
          env:
            - name: GF_AUTH_ANONYMOUS_ENABLED
              value: "true"
            - name: GF_AUTH_ANONYMOUS_ORG_ROLE
              value: "Admin"
          volumeMounts:
            - name: datasource
              mountPath: /etc/grafana/provisioning/datasources
            - name: dashboard-provider
              mountPath: /etc/grafana/provisioning/dashboards
            - name: dashboard-json
              mountPath: /var/lib/grafana/dashboards
      volumes:
        - name: datasource
          configMap:
            name: grafana-datasource
        - name: dashboard-provider
          configMap:
            name: grafana-dashboard-provider
        - name: dashboard-json
          configMap:
            name: grafana-dashboard-json
```

```yaml
# grafana-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: grafana
spec:
  selector:
    app: grafana
  ports:
    - port: 3000
      targetPort: 3000
```

Appliquons le tout :

```shell
$ kubectl apply -f grafana-datasource.yaml -f grafana-dashboard.yaml \
    -f grafana-deployment.yaml -f grafana-service.yaml
```

Puis ouvrons un tunnel vers Grafana :

```shell
$ kubectl port-forward svc/grafana 3000:3000
```

En ouvrant `http://localhost:3000` dans le navigateur, puis en naviguant vers
Dashboards, on trouve le dashboard "Quotes API" préconfiguré. Pour l'instant,
les graphiques sont vides : il n'y a pas encore de trafic.

### Générer du trafic et observer

Pour alimenter les métriques, un petit script shell envoie des requêtes en boucle
vers les trois endpoints :

```shell
#!/bin/bash
echo "Génération de trafic vers l'API..."
echo "Appuyez sur Ctrl+C pour arrêter."
while true; do
    curl -s http://localhost:8080/quote > /dev/null
    curl -s http://localhost:8080/ > /dev/null
    curl -s http://localhost:8080/error > /dev/null
    sleep 0.5
done
```

Après quelques minutes de trafic, le dashboard Grafana prend vie. On y observe
les quatre golden signals en temps réel :

<!-- ILLUSTRATION: capture d'écran du dashboard Grafana "Quotes API" avec les quatre panneaux montrant des courbes actives -->

- **Requêtes par seconde** : les trois endpoints apparaissent avec leur trafic
  respectif. On voit aussi la distinction par code de statut : l'endpoint
  `/error` produit à la fois des lignes 200 et 500.
- **Taux d'erreurs** : l'endpoint `/error` oscille autour de 50 %, ce qui
  correspond au `random.random() < 0.5` dans notre code. Les autres endpoints
  n'apparaissent pas, car ils ne produisent pas d'erreurs.
- **Latence par percentile** : c'est le panneau le plus instructif. L'endpoint
  `/quote`, avec son délai aléatoire entre 10 et 500 ms, produit une
  distribution visible : le p50 (la médiane) est autour de 250 ms, tandis que le
  p99 approche 500 ms. On voit concrètement pourquoi la moyenne seule est
  trompeuse : les percentiles révèlent la forme de la distribution.
- **Nombre total de requêtes** : un compteur qui augmente en continu, confirmant
  que le trafic est bien reçu.

Ce tutoriel illustre le pipeline complet de l'observabilité par métriques :
l'application instrumente son code avec `prometheus_client`, expose un endpoint
`/metrics`, Prometheus collecte ces données toutes les 15 secondes, et Grafana
les transforme en visualisations exploitables. En production, le même mécanisme
fonctionne à grande échelle : Prometheus peut scraper des centaines de services,
et Grafana peut afficher des dizaines de dashboards couvrant toute
l'infrastructure. Le principe reste le même, seul le nombre de cibles change.

Pour nettoyer l'environnement quand vous avez terminé :

```shell
$ k3d cluster delete obs-demo
```