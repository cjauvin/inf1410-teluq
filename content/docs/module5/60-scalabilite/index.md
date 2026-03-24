---
title: "Est-ce que ça va tenir la charge ?"
weight: 60
slug: "scalabilite"
---

# Est-ce que ça va tenir la charge ?

Les cinq sections précédentes de ce module ont abordé des questions fondamentales
de l'exploitation d'un logiciel : où il tourne, comment le déployer, comment
savoir s'il fonctionne, quoi faire quand il casse, et comment le protéger. Mais
il reste une question que ces réponses ne couvrent pas : que se passe-t-il quand
le logiciel rencontre le succès ? Un système peut être parfaitement conçu,
déployé de manière impeccable, instrumenté avec soin, protégé contre les
attaques... et s'écrouler le jour où le nombre d'utilisateurs double. La
scalabilité, c'est la capacité d'un système à maintenir ses performances
lorsque la charge augmente. Ce n'est pas un problème que tous les systèmes
rencontrent, mais quand il se manifeste, il met à l'épreuve chaque décision
architecturale prise en amont.

L'histoire du web regorge d'exemples de systèmes victimes de leur propre succès.
Twitter, dans ses premières années, était tristement célèbre pour son « fail
whale », une illustration de baleine qui s'affichait quand le site s'écroulait
sous la charge, ce qui arrivait régulièrement lors d'événements populaires.

<!-- ILLUSTRATION: Le "fail whale" de Twitter, image iconique des problèmes de scalabilité -->

Le site, initialement construit comme une application Ruby on Rails monolithique,
n'avait tout simplement pas été conçu pour supporter des millions de tweets
simultanés. Twitter a passé plusieurs années à réécrire ses composants critiques,
migrant progressivement vers une architecture de microservices en Java et Scala.
Plus près de nous, Shopify, l'entreprise d'Ottawa fondée par Tobias Lütke en
2006, fait face chaque année à un défi de scalabilité extrême : le Black Friday.
Pendant quelques heures, le trafic sur sa plateforme explose à des niveaux
plusieurs fois supérieurs à la normale, alors que des milliers de boutiques en
ligne gèrent simultanément des pics de commandes. En 2023, Shopify a traité
4,2 milliards de dollars de ventes pendant le weekend du Black Friday/Cyber
Monday. Cet exploit ne repose pas sur un seul truc magique, mais sur l'ensemble
des techniques que nous allons explorer dans cette section : caching agressif,
load balancing, files d'attente, et une infrastructure capable de s'étirer et de
se contracter selon la demande.

## Scalabilité verticale vs horizontale

Face à un système qui ne tient plus la charge, la réponse la plus intuitive est
d'acheter une machine plus puissante. Plus de RAM, un processeur plus rapide, un
disque SSD plus performant. C'est la **scalabilité verticale** (*scaling up*) :
augmenter les ressources d'un seul serveur. L'approche est séduisante par sa
simplicité. Le code ne change pas, l'architecture reste la même, il n'y a rien à
redistribuer. Pendant longtemps, c'était la stratégie par défaut : les bases de
données Oracle, par exemple, tournaient typiquement sur des serveurs uniques de
plus en plus coûteux. Mais la scalabilité verticale a une limite physique : à un
certain point, il n'existe tout simplement pas de machine plus puissante, ou son
coût devient prohibitif. Et elle a une limite de fiabilité : si cette machine
unique tombe en panne, tout le système s'arrête. C'est un point de défaillance
unique (*single point of failure*), un concept que nous avons rencontré dans la
section sur les incidents.

L'alternative est la **scalabilité horizontale** (*scaling out*) : au lieu d'une
machine plus grosse, on utilise plusieurs machines plus petites qui se partagent
le travail. C'est l'approche qu'a rendue possible le cloud computing (section
« Où est-ce que ça tourne ? ») et que nous avons déjà vue en action dans le
tutoriel Kubernetes, quand nous avons passé notre application Flask de une à
trois répliques. Le principe semble simple, mais il introduit une famille
entière de problèmes nouveaux. Si trois serveurs répondent aux requêtes, comment
décider lequel traite chaque requête ? Si un utilisateur modifie ses données sur
le serveur A, comment s'assurer que le serveur B voit la modification ? Si un
des serveurs tombe en panne, comment redistribuer sa charge sans que les
utilisateurs s'en aperçoivent ? La scalabilité horizontale échange la simplicité
d'une seule machine contre la complexité de la coordination entre plusieurs.
C'est un compromis fondamental, et chaque technique que nous allons examiner
dans cette section est une manière de gérer un aspect de cette complexité.

<!-- ILLUSTRATION: Diagramme comparant scaling vertical (une machine qui grossit) vs scaling horizontal (plusieurs machines côte à côte) -->

## Load balancing

Dès qu'un système passe à plusieurs serveurs, une question se pose
immédiatement : comment répartir les requêtes entre eux ? C'est le rôle du
**load balancer** (répartiteur de charge), un composant qui se place entre les
clients et les serveurs, reçoit toutes les requêtes entrantes, et les distribue
selon une stratégie définie. Le load balancer est le premier élément
d'infrastructure qu'on ajoute quand on passe au scaling horizontal, et nous
l'avons déjà rencontré sans le nommer : dans le tutoriel Kubernetes, quand nous
avions trois répliques de notre application Flask, le Service Kubernetes jouait
exactement ce rôle, distribuant les requêtes entre les pods.

L'algorithme de répartition le plus simple est le **round-robin** : les requêtes
sont distribuées à tour de rôle, en rotation. La première requête va au serveur
A, la deuxième au serveur B, la troisième au serveur C, puis on revient au
serveur A. C'est facile à implémenter et ça fonctionne bien quand les serveurs
ont des capacités similaires et que les requêtes sont à peu près équivalentes en
coût. Mais ce n'est pas toujours le cas : certaines requêtes prennent 10
millisecondes, d'autres 10 secondes. Le **least connections** (moindre nombre de
connexions) tente de résoudre ce problème en envoyant chaque nouvelle requête au
serveur qui a le moins de requêtes en cours de traitement. D'autres algorithmes
existent : le **weighted round-robin**, qui donne plus de requêtes aux serveurs
plus puissants, ou le **IP hash**, qui envoie toujours les requêtes d'un même
client au même serveur, ce qui peut être utile quand le serveur maintient un
état en mémoire (comme une session).

Un load balancer ne se contente pas de distribuer les requêtes : il doit aussi
savoir quand un serveur ne fonctionne plus. C'est le rôle des **health checks**,
des vérifications périodiques où le load balancer envoie une requête de test
(typiquement un simple `GET /health`) à chaque serveur. Si un serveur ne répond
pas, ou répond avec une erreur, le load balancer le retire automatiquement de la
rotation et cesse de lui envoyer du trafic. Quand le serveur redevient sain, il
est réintégré. Ce mécanisme, que nous avons déjà croisé avec les *liveness
probes* et *readiness probes* de Kubernetes, est ce qui permet au scaling
horizontal d'offrir une meilleure fiabilité que le scaling vertical : si un
serveur sur trois tombe en panne, les deux autres absorbent la charge, et les
utilisateurs ne voient qu'une légère dégradation plutôt qu'une panne totale. Les
outils de load balancing les plus courants sont nginx et HAProxy pour les
déploiements traditionnels, les Services et Ingress dans Kubernetes, et les load
balancers managés des fournisseurs cloud (AWS ELB, Google Cloud Load Balancing,
Azure Load Balancer).

## Caching

Le load balancing distribue la charge entre plusieurs serveurs, mais il ne
réduit pas la quantité de travail totale. Si chaque requête nécessite une
requête à la base de données, ajouter des serveurs ne fait que répartir les
requêtes à la base de données, qui devient à son tour le goulot d'étranglement.
Le **caching** (mise en cache) attaque le problème différemment : au lieu de
faire le même travail plusieurs fois, on garde le résultat en mémoire et on le
réutilise. C'est une idée d'une simplicité trompeuse, que Phil Karlton,
ingénieur chez Netscape, a immortalisée dans une citation célèbre : « There are
only two hard things in Computer Science: cache invalidation and naming
things. » La difficulté n'est pas de mettre des données en cache, c'est de
savoir quand les données en cache ne sont plus valides.

Le caching n'est pas un concept propre à l'infrastructure. Tout programmeur qui
a déjà stocké le résultat d'un calcul dans une variable pour éviter de le
refaire a fait du caching. En programmation, cette technique s'appelle la
**mémoïsation** (*memoization*), un terme introduit par Donald Michie en 1968.
Python offre un mécanisme intégré pour ça : le décorateur `@functools.cache` (ou
`@lru_cache` pour une version avec une taille maximale) qui mémorise
automatiquement les résultats d'une fonction en fonction de ses arguments :

```python
from functools import cache

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Sans le décorateur, `fibonacci(50)` prendrait un temps astronomique à cause des
appels récursifs redondants. Avec le cache, chaque valeur n'est calculée qu'une
seule fois. Le principe est exactement le même quand on passe à l'échelle d'un
système distribué, mais les contraintes changent. Un `@cache` vit dans la
mémoire d'un seul processus : si le serveur redémarre, le cache disparaît, et
si trois serveurs tournent en parallèle, chacun a son propre cache indépendant.
C'est pourquoi on utilise un service de cache partagé comme Redis ou Memcached,
accessible par tous les serveurs, persistant au-delà de la vie d'un processus
individuel.

Le caching opère à plusieurs niveaux dans l'architecture d'un système web. La
première couche est le **cache du navigateur** : quand un serveur envoie une
réponse HTTP, il peut inclure des en-têtes (`Cache-Control`, `ETag`, `Expires`)
qui indiquent au navigateur de garder le résultat en mémoire pendant une durée
déterminée. La prochaine fois que l'utilisateur demande la même ressource, le
navigateur la sert directement depuis son cache local, sans même contacter le
serveur. C'est extrêmement efficace pour les ressources statiques (images,
fichiers CSS et JavaScript) qui changent rarement. La deuxième couche est le
**CDN**, que nous aborderons dans la prochaine sous-section. La troisième
couche, celle sur laquelle le développeur a le plus de contrôle, est le **cache
applicatif** : un espace mémoire rapide, typiquement Redis ou Memcached, où
l'application stocke les résultats de calculs coûteux ou de requêtes fréquentes
à la base de données.

Le pattern le plus courant est le **cache-aside** (aussi appelé *lazy loading*) :
l'application vérifie d'abord si le résultat est en cache, et ne consulte la
base de données que si ce n'est pas le cas. Voici un exemple simplifié avec
Redis :

```python
import redis
import json

cache = redis.Redis(host="localhost", port=6379)

def get_user_profile(user_id):
    # Vérifier le cache d'abord
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Cache miss : aller chercher dans la base de données
    profile = db.query("SELECT * FROM users WHERE id = :id", {"id": user_id})

    # Stocker en cache pour 5 minutes
    cache.setex(f"user:{user_id}", 300, json.dumps(profile))

    return profile
```

Le paramètre `300` de `setex` est le TTL (*time to live*) en secondes : après
cinq minutes, Redis supprime automatiquement l'entrée, ce qui force
l'application à aller chercher des données fraîches à la prochaine requête. Le
TTL est la forme la plus simple d'**invalidation de cache** : on accepte que les
données puissent être périmées pendant une durée limitée, en échange de la
simplicité. C'est un compromis acceptable pour un profil utilisateur, mais pas
pour un solde bancaire. Pour les cas où la fraîcheur est critique, l'alternative
est l'invalidation explicite : quand les données changent, on supprime l'entrée
correspondante du cache (`cache.delete(f"user:{user_id}")`), de sorte que la
prochaine lecture ira chercher la version à jour.

## CDN

Un **CDN** (*Content Delivery Network*) est un réseau de serveurs distribués
géographiquement qui servent du contenu aux utilisateurs depuis l'emplacement le
plus proche. Le principe repose sur une réalité physique incontournable : la
vitesse de la lumière. Une requête entre Montréal et un serveur à Tokyo doit
parcourir environ 10 000 km, ce qui impose un temps de latence incompressible
d'au moins 30 millisecondes pour l'aller simple, et en pratique beaucoup plus à
cause des multiples sauts réseau. Un CDN résout ce problème en plaçant des
copies du contenu dans des points de présence (*PoPs*) répartis à travers le
monde. Quand un utilisateur à Montréal demande une image, elle est servie depuis
un serveur à Montréal ou à New York plutôt que depuis Tokyo. Les premiers CDN
sont apparus à la fin des années 1990, Akamai (fondé en 1998 au MIT) étant le
pionnier du domaine. Aujourd'hui, les acteurs principaux incluent Cloudflare,
Amazon CloudFront, Fastly et Google Cloud CDN.

Un usage très courant des CDN que tout développeur web rencontre rapidement est
l'inclusion de bibliothèques JavaScript ou CSS hébergées sur un CDN public. Au
lieu de télécharger une bibliothèque et de la servir depuis son propre serveur,
on peut simplement la référencer par une URL pointant vers un CDN :

```html
<!-- jQuery servi depuis le CDN de Google -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>

<!-- Bootstrap servi depuis le CDN cdnjs -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css" />
```

L'avantage est double. D'abord, le fichier est servi depuis un serveur
géographiquement proche de l'utilisateur. Ensuite, si l'utilisateur a déjà
visité un autre site qui référençait la même URL, le fichier est peut-être déjà
dans le cache de son navigateur, ce qui élimine complètement le téléchargement.
Des services comme cdnjs, jsDelivr et unpkg se sont spécialisés dans
l'hébergement de bibliothèques open source sur CDN, servant collectivement des
milliards de requêtes par jour.

Les CDN sont particulièrement efficaces pour les contenus statiques : images,
fichiers CSS et JavaScript, vidéos, documents PDF. Ces ressources ne changent
pas entre les utilisateurs et se prêtent naturellement à la mise en cache
géographique. C'est d'ailleurs ce qui rend le modèle du *Static Site
Generation* (SSG), que nous avons rencontré dans la section sur les interfaces
utilisateur au module 3, si performant : un site généré statiquement par Hugo,
Jekyll ou Astro n'est qu'un ensemble de fichiers HTML, CSS et JavaScript qui
peuvent être servis entièrement par un CDN, sans aucun serveur applicatif. Ce
cours lui-même, construit avec Hugo, pourrait être déployé sur un CDN et servir
des milliers d'étudiants simultanément sans aucun problème de scalabilité. Mais
les CDN modernes vont au-delà du contenu statique. Des services comme Cloudflare
Workers ou AWS Lambda@Edge permettent d'exécuter du code directement sur les
serveurs du CDN, à la périphérie du réseau (*edge computing*). Cela permet, par
exemple, de personnaliser une page en fonction de la langue de l'utilisateur ou
de rediriger une requête vers le bon backend, le tout sans que la requête ne
quitte la région géographique de l'utilisateur.

## Réplication et sharding

Le load balancing et le caching permettent de distribuer et de réduire la charge
sur les serveurs applicatifs, mais à un certain point, c'est la base de données
elle-même qui devient le goulot d'étranglement. Une application peut tourner sur
cinquante serveurs derrière un load balancer, si tous ces serveurs envoient
leurs requêtes à une seule base de données PostgreSQL, c'est cette base qui fixe
la limite. Deux stratégies complémentaires permettent de passer à l'échelle au
niveau des données : la **réplication** et le **sharding**.

La **réplication** consiste à maintenir plusieurs copies identiques de la base
de données. La forme la plus courante est la réplication **leader-follower**
(aussi appelée *primary-replica* ou historiquement *master-slave*, une
terminologie que l'industrie abandonne progressivement). Le principe : une seule
instance, le leader, accepte les écritures. Chaque écriture est ensuite propagée
aux followers, qui maintiennent une copie à jour des données. Les lectures,
elles, peuvent être distribuées entre tous les followers. Ce modèle fonctionne
bien quand les lectures sont beaucoup plus fréquentes que les écritures, ce qui
est le cas de la majorité des applications web : un site de commerce en ligne
reçoit des milliers de consultations de fiches produits pour chaque commande
passée. Mais la réplication introduit un délai : entre le moment où une écriture
est effectuée sur le leader et celui où elle apparaît sur les followers, il y a
un décalage (*replication lag*). Pendant ce décalage, un utilisateur qui vient
de modifier son profil pourrait ne pas voir sa modification s'il est servi par
un follower qui n'a pas encore reçu la mise à jour. C'est un compromis entre
performance et cohérence que nous retrouverons avec le théorème CAP.

Le **sharding** (aussi appelé *partitionnement horizontal*) attaque ce problème
en découpant les données elles-mêmes : au lieu de stocker tous les utilisateurs
dans une seule base, on les répartit entre plusieurs bases selon un critère
déterministe. Par exemple, les utilisateurs dont le nom commence par A-M vont
sur le shard 1, et N-Z sur le shard 2. En pratique, on utilise plutôt une
fonction de hachage sur une clé (comme l'identifiant de l'utilisateur) pour
distribuer les données uniformément. Chaque shard ne contient qu'une fraction
des données et ne traite qu'une fraction des requêtes, ce qui permet de passer à
l'échelle aussi bien en lecture qu'en écriture.

Le prix du sharding est la complexité. Les requêtes qui touchent un seul shard
restent simples et rapides, mais les requêtes qui doivent combiner des données
de plusieurs shards deviennent beaucoup plus coûteuses. Si les utilisateurs A-M
sont sur le shard 1 et les utilisateurs N-Z sur le shard 2, une requête
« afficher les 10 utilisateurs les plus récents » doit interroger les deux
shards, combiner les résultats, puis trier. Les jointures entre tables réparties
sur des shards différents sont particulièrement pénibles. Le choix de la **clé
de sharding** est donc crucial : une mauvaise clé peut créer des « hot spots »
(un shard qui reçoit beaucoup plus de trafic que les autres) ou rendre les
requêtes courantes impossibles sans interroger tous les shards. Rééquilibrer les
shards quand la distribution devient inégale, ou ajouter de nouveaux shards à un
système existant, sont des opérations complexes et risquées. C'est pourquoi le
sharding est généralement considéré comme une solution de dernier recours : on
réplique d'abord, on optimise les requêtes, on ajoute du caching, et on ne
sharde que quand on a épuisé les autres options. Le principe YAGNI s'applique
pleinement ici.

<!-- ILLUSTRATION: Diagramme montrant la réplication (un leader avec plusieurs followers) et le sharding (données découpées entre plusieurs bases) -->

## Le théorème CAP

En 2000, lors d'un keynote au symposium PODC (*Principles of Distributed
Computing*), l'informaticien Eric Brewer de l'Université de Californie à
Berkeley a formulé une conjecture qui allait devenir l'un des résultats les plus
cités en systèmes distribués. La conjecture, prouvée formellement par Seth
Gilbert et Nancy Lynch du MIT en 2002, affirme qu'un système distribué ne peut
garantir simultanément que deux des trois propriétés suivantes :

- **Consistency** (cohérence) : tous les nœuds voient les mêmes données au même
  moment. Une lecture retourne toujours le résultat de l'écriture la plus
  récente.
- **Availability** (disponibilité) : chaque requête reçoit une réponse, même si
  certains nœuds sont en panne.
- **Partition tolerance** (tolérance aux partitions réseau) : le système continue
  de fonctionner même si des messages sont perdus entre les nœuds.

Pour comprendre intuitivement pourquoi ces trois propriétés ne peuvent pas
coexister, imaginons un scénario simple. Une application bancaire réplique ses
données sur deux serveurs, A et B. Alice a un solde de 1 000 $ visible sur les
deux serveurs. Maintenant, une partition réseau survient : A et B ne peuvent
plus communiquer entre eux. Alice envoie une requête au serveur A pour retirer
500 $. Le serveur A met à jour le solde localement : 500 $. Mais il ne peut pas
informer le serveur B, puisque la connexion est coupée. À ce moment, si Bob
consulte le solde d'Alice sur le serveur B, que se passe-t-il ? Le système a
deux options. Première option : le serveur B répond avec l'ancienne valeur,
1 000 $. Le système est disponible (B a répondu) mais incohérent (B retourne
une donnée périmée). C'est le choix AP. Deuxième option : le serveur B refuse
de répondre, parce qu'il sait qu'il n'est peut-être pas à jour. Le système est
cohérent (on ne retourne jamais de donnée périmée) mais indisponible (B n'a pas
répondu). C'est le choix CP. Il n'existe pas de troisième option : tant que la
partition persiste, on ne peut pas avoir à la fois une réponse et la garantie
qu'elle est à jour. Et le choix **CA** (cohérence + disponibilité, mais sans
tolérance aux partitions) ? C'est un système qui suppose que les partitions
réseau n'arrivent jamais. Une base de données PostgreSQL sur un seul serveur
est techniquement CA : elle est cohérente et disponible, mais si le réseau entre
l'application et la base tombe, tout s'arrête. Dès qu'on distribue les données
sur plusieurs nœuds, les partitions deviennent une réalité inévitable, et le
choix se réduit à CP ou AP.

Le théorème peut sembler abstrait, mais il a une implication très concrète. Dans
un système distribué, les partitions réseau ne sont pas un cas théorique : elles
arrivent. Un câble est coupé, un switch tombe en panne, un datacenter devient
temporairement injoignable. La tolérance aux partitions n'est donc pas vraiment
un choix, c'est une contrainte imposée par la réalité. Le vrai dilemme est entre
cohérence et disponibilité. Quand une partition survient, le système doit
choisir : soit il refuse de répondre aux requêtes tant que les nœuds ne sont pas
resynchronisés (il sacrifie la disponibilité pour préserver la cohérence, c'est
le choix **CP**), soit il continue de répondre avec des données potentiellement
périmées (il sacrifie la cohérence pour préserver la disponibilité, c'est le
choix **AP**). Les bases de données relationnelles traditionnelles (PostgreSQL,
MySQL) font un choix CP : elles privilégient la cohérence, quitte à devenir
indisponibles en cas de partition. Des bases NoSQL comme Cassandra ou DynamoDB
font le choix inverse, AP : elles restent disponibles, mais acceptent que
différents nœuds puissent temporairement retourner des données différentes, un
modèle appelé **cohérence à terme** (*eventual consistency*).

## Files d'attente et traitement asynchrone

Toutes les techniques que nous avons vues jusqu'ici partagent un même modèle
d'interaction : un client envoie une requête et attend la réponse. C'est le
modèle **synchrone**, simple et naturel. Mais certaines opérations ne se prêtent
pas bien à ce modèle. Quand un utilisateur passe une commande sur un site de
commerce en ligne, la réponse immédiate devrait être « votre commande est
confirmée ». Mais en arrière-plan, il faut valider le paiement, mettre à jour
l'inventaire, générer une facture, envoyer un courriel de confirmation, notifier
l'entrepôt pour la livraison. Si toutes ces opérations sont exécutées de manière
synchrone avant de répondre à l'utilisateur, la requête prend plusieurs
secondes, et le serveur est occupé pendant tout ce temps, incapable de traiter
d'autres requêtes. La solution est de **découpler** le traitement : le serveur
accepte la commande, la dépose dans une **file d'attente** (*message queue*), et
répond immédiatement à l'utilisateur. Des processus séparés, appelés *workers*
ou *consumers*, consomment les messages de la file et exécutent les tâches en
arrière-plan, à leur propre rythme.

Ce modèle est directement lié à l'**architecture événementielle** que nous avons
rencontrée dans le module 3 : la file d'attente joue le même rôle de découplage
entre producteurs et consommateurs que nous avions décrit avec Kafka et
RabbitMQ. La différence de perspective est que dans le module 3, nous parlions
d'architecture (comment structurer les interactions entre composants), alors
qu'ici nous parlons de scalabilité (comment absorber la charge). Mais le
mécanisme est le même. RabbitMQ est une file d'attente classique : un message
est délivré à un seul consumer, et une fois traité, il disparaît. Kafka, comme
nous l'avons vu, fonctionne plutôt comme un journal (*log*) distribué où les
messages sont conservés et peuvent être lus par plusieurs consumers
indépendants. Dans l'écosystème Python, **Celery** est l'outil le plus courant
pour le traitement asynchrone. Il s'appuie sur un *broker* de messages (Redis ou
RabbitMQ) et permet de définir des tâches qui seront exécutées en arrière-plan
par des workers séparés.

Voici un exemple simplifié d'une tâche Celery pour le traitement d'une
commande :

```python
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379")

@app.task
def process_order(order_id):
    validate_payment(order_id)
    update_inventory(order_id)
    generate_invoice(order_id)
    send_confirmation_email(order_id)
```

Côté application web, au lieu d'exécuter toutes ces étapes avant de répondre à
l'utilisateur, on dépose simplement la tâche dans la file :

```python
@app.route("/order", methods=["POST"])
def create_order():
    order = save_order(request.json)
    process_order.delay(order.id)  # .delay() envoie la tâche à la file
    return jsonify({"status": "confirmed", "order_id": order.id}), 201
```

Le point clé est que l'appel `process_order.delay()` est **non-bloquant** : il
ne fait que déposer un message dans la file d'attente Redis et retourne
immédiatement, sans attendre que la tâche soit terminée. Le serveur web est
libre de traiter la requête suivante pendant qu'un worker, dans un processus
séparé, exécute les étapes de traitement de la commande. C'est le contraire d'un
appel **bloquant**, où le serveur resterait immobilisé en attendant la fin de
chaque étape (validation du paiement, envoi de courriel, etc.) avant de pouvoir
répondre au client. La distinction est fondamentale pour la scalabilité : un
serveur qui bloque pendant cinq secondes sur chaque commande ne peut traiter que
12 commandes par minute. Le même serveur, avec un traitement non-bloquant, peut
accepter des centaines de commandes par minute, puisque chaque requête ne prend
que quelques millisecondes, le temps de sauvegarder la commande et de la déposer
dans la file. Si la charge augmente et que les tâches s'accumulent dans la file,
on peut simplement lancer plus de workers, ce qui est une forme de scaling
horizontal appliquée au traitement asynchrone plutôt qu'aux requêtes HTTP.

## La scalabilité comme spectre de compromis

Chaque technique que nous avons explorée dans cette section apporte une solution
à un aspect du problème de la charge, mais chacune introduit aussi de la
complexité. Le load balancing demande de gérer des serveurs multiples et de
s'assurer qu'ils sont interchangeables. Le caching demande de décider quand les
données sont périmées. La réplication introduit le délai de propagation. Le
sharding complique les requêtes qui traversent les partitions. Les files
d'attente ajoutent une couche d'indirection et rendent le traitement plus
difficile à suivre et à déboguer. Le théorème CAP nous rappelle que certains
compromis sont inévitables, pas parce que nos outils sont imparfaits, mais parce
que la physique des systèmes distribués l'impose.

C'est pourquoi le principe YAGNI, que nous avons rencontré dans le module 3, est
particulièrement pertinent en matière de scalabilité. Un système qui sert
quelques centaines d'utilisateurs n'a pas besoin de sharding, de CDN, ni de
files d'attente. Un seul serveur avec une base de données PostgreSQL et un peu
de caching peut aller remarquablement loin. Les premières versions de Twitter,
de Shopify, de GitHub, toutes tournaient sur des architectures simples qui
auraient fait sourire un architecte de systèmes distribués. Ce n'est que lorsque
le succès est arrivé que ces architectures ont dû évoluer, souvent dans la
douleur. La bonne approche n'est pas de concevoir pour des millions
d'utilisateurs dès le premier jour, mais de comprendre les outils disponibles
pour savoir vers lesquels se tourner quand le besoin se manifeste. Comme le dit
l'adage souvent attribué à Donald Knuth : « Premature optimization is the root
of all evil. »