---
title: "L'orchestration (Kubernetes)"
weight: 20
slug: "kubernetes"
---

# L'orchestration (Kubernetes)

Docker compose, que nous venons de voir, permet de gérer un groupe de containers
sur une seule machine. Mais que se passe-t-il quand une application doit tourner
sur des dizaines ou des centaines de machines, avec des exigences de haute
disponibilité ? Si un container tombe, qui le redémarre ? Si la charge augmente,
qui décide de créer de nouvelles instances ? Comment répartir le trafic entre les
containers disponibles ? Ces questions définissent le problème de
l'*orchestration*.

Google a été confronté à ce problème très tôt. En interne, l'entreprise
utilisait depuis le milieu des années 2000 un système appelé Borg pour gérer des
millions de containers à travers ses centre de données. En 2014, Google a décidé de
publier une version open source des idées de Borg sous le nom de Kubernetes (du
grec "pilote" ou "timonier", souvent abrégé K8s). Le projet a rapidement été
adopté par l'industrie et est aujourd'hui le standard de facto pour
l'orchestration de containers.

{{< image src="k8s.png" alt="" title="" loading="lazy" >}}

Les concepts fondamentaux de Kubernetes sont relativement peu nombreux, même si
leur combinaison peut devenir complexe. Un *pod* est la plus petite unité
déployable : il contient un ou plusieurs containers qui partagent le même réseau
et le même stockage (en pratique, un pod contient souvent un seul container). Un
*deployment* décrit l'état souhaité d'un groupe de pods : combien d'instances on
veut, quelle image utiliser, comment gérer les mises à jour. Kubernetes s'assure
en permanence que l'état réel du cluster correspond à cet état souhaité. Si un
pod tombe, il en crée un nouveau. Si on modifie le deployment pour demander une
nouvelle version de l'image, Kubernetes effectue un *rolling update*, remplaçant
les pods un par un pour éviter toute interruption. Un *service* fournit une
adresse réseau stable pour accéder à un groupe de pods, jouant le rôle de load
balancer interne. Ce modèle est fondamentalement *déclaratif* : on décrit *ce
qu'on veut* plutôt que *comment l'obtenir*, et le système se charge de converger
vers l'état souhaité. C'est le même paradigme que celui de SQL, que nous avons
rencontré dans le module 3 : de la même manière qu'une requête SQL décrit les
données qu'on veut obtenir sans spécifier comment les chercher (le moteur de
requêtes s'en charge), un fichier de configuration Kubernetes décrit l'état
désiré du système sans spécifier les étapes pour y arriver (le *control plane*
s'en charge). Cette convergence n'est pas un hasard : le paradigme déclaratif
s'avère particulièrement puissant quand le système sous-jacent est complexe et
que les chemins pour atteindre un état donné sont multiples.

## De docker compose à Kubernetes

Nous avons décrit les concepts fondamentaux de Kubernetes de manière abstraite.
Pour les rendre concrets, nous allons transposer l'application Flask+Redis que
nous avons construite avec docker compose vers Kubernetes. Pour expérimenter
localement sans avoir besoin d'un cluster cloud, nous utiliserons k3d, un outil
qui crée un cluster Kubernetes léger (basé sur k3s, une distribution allégée de
Kubernetes créée par Rancher) directement dans des containers Docker. Comme
Docker est déjà installé sur notre machine, il n'y a pas de couche
supplémentaire à ajouter. C'est un environnement limité en termes de capacité,
mais il implémente la même API et les mêmes mécanismes qu'un vrai cluster :
tout ce que nous apprendrons ici s'applique directement en production. Pour
observer ce qui se passe dans le cluster, nous utiliserons k9s, une interface
textuelle interactive (TUI) qui permet de naviguer les ressources Kubernetes de
manière beaucoup plus fluide que la ligne de commande. Nous aurons aussi besoin
de `kubectl`, l'outil CLI standard de Kubernetes, pour appliquer nos fichiers
de configuration.

## Préparation

Avant de commencer, adaptons légèrement notre application Flask. Kubernetes
attribue automatiquement un nom unique à chaque pod, accessible via la variable
d'environnement `HOSTNAME` à l'intérieur du container. Nous allons modifier
`main.py` pour afficher ce nom, ce qui nous sera utile plus tard pour observer
le comportement du cluster quand plusieurs instances de notre application
tournent en parallèle :

```python
# main.py

from flask import Flask
import redis
import os

app = Flask(__name__)

red = redis.Redis("redis")
KEY = "some_key"
POD_NAME = os.environ.get("HOSTNAME", "unknown")

@app.route("/set/<val>")
def set_value(val):
    red.set(KEY, val)
    return f"[{POD_NAME}] Your value ({val}) is now set in the database"

@app.route("/get")
def get_value():
    val = red.get(KEY)
    if val is None:
        return f"[{POD_NAME}] No value was stored, use /set"
    return f"[{POD_NAME}] Your stored value is {val}"
```

On remarque deux changements : l'ajout de `POD_NAME` qui lit le nom d'hôte du
container, et le remplacement de `"db"` par `"redis"` comme adresse du serveur
Redis. Avec docker compose, le nom du service (`db`) servait de nom de domaine
interne. Avec Kubernetes, c'est le nom du *service* Kubernetes qui jouera ce
rôle, et nous l'appellerons `redis` pour plus de clarté.

Créons maintenant le cluster k3d :

```shell
$ k3d cluster create demo -p "8080:80@loadbalancer"
```

Une fois le cluster créé on peut constater qu'il fonctionne :

```shell
$ kubectl cluster-info
Kubernetes control plane is running at https://0.0.0.0:6443
```

La commande `k3d cluster create` mérite une explication. L'option
`-p "8080:80@loadbalancer"` configure le port forwarding : le trafic arrivant
sur le port 8080 de notre machine sera redirigé vers le port 80 du load
balancer intégré à k3d (Traefik), qui le distribuera ensuite vers nos pods.
C'est l'équivalent de la directive `ports` dans notre fichier docker compose,
mais avec une couche supplémentaire : le load balancer, qui sera capable de
répartir le trafic entre plusieurs instances de notre application.

## Le deployment Redis

Commençons par déployer Redis. Dans Kubernetes, chaque composant de notre
application est décrit par un ou plusieurs fichiers YAML qu'on appelle des
*manifests*. Créons un fichier `redis-deployment.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis
          ports:
            - containerPort: 6379
```

Ce fichier mérite qu'on s'y attarde, car il illustre la structure commune à
tous les manifests Kubernetes. Les champs `apiVersion` et `kind` identifient le
type de ressource (ici un Deployment). Le champ `metadata.name` lui donne un
nom. Le bloc `spec` contient la partie intéressante : `replicas: 1` indique
qu'on veut exactement une instance de ce pod. Le `selector` et les `labels`
forment un mécanisme d'association : le deployment gère tous les pods qui
portent le label `app: redis`. C'est un système souple et découplé, très
différent de docker compose où l'association entre un service et sa définition
est directe et implicite. Enfin, `template.spec.containers` décrit le container
lui-même, de manière analogue à ce qu'on faisait dans docker compose avec
`image: redis`.

Pour que d'autres pods puissent communiquer avec Redis, il faut aussi créer un
*service*, dans un fichier `redis-service.yaml` :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
spec:
  selector:
    app: redis
  ports:
    - port: 6379
```

Le service crée une adresse réseau stable (`redis`) qui pointe vers tous les
pods portant le label `app: redis`. C'est ce nom que notre application Flask
utilise dans `redis.Redis("redis")`. Le service joue le même rôle que le réseau
interne créé automatiquement par docker compose, mais de manière explicite et
configurable.

## Le deployment Flask

Notre application Flask nécessite une image Docker personnalisée. Avec k3d, la
manière la plus simple de rendre une image locale disponible au cluster est de
la construire puis de l'importer :

```shell
$ docker build -t flask-app:latest .
$ k3d image import flask-app:latest -c demo
```

La première commande construit l'image comme nous l'avons fait dans le tutoriel
Docker. La seconde la transfère dans le registre interne du cluster k3d, la
rendant accessible aux pods. Le fichier `web-deployment.yaml` décrit le
deployment de notre application :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: flask-app:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 5000
          env:
            - name: FLASK_APP
              value: main
```

La structure est identique à celle du deployment Redis. On retrouve le même
patron : un nombre de répliques souhaité, un sélecteur par labels, et la
description du container. La directive `imagePullPolicy: Never` indique à
Kubernetes de ne pas tenter de télécharger l'image depuis un registre distant :
elle est déjà disponible localement grâce à notre commande `k3d image import`.
La différence notable est la section `env`, qui définit des variables
d'environnement à l'intérieur du container. C'est l'équivalent de la clé
`environment` dans docker compose. Ce mécanisme est au coeur du facteur III de
la Twelve-Factor App : la configuration d'une application doit être stockée dans
l'environnement, pas dans le code.

Le fichier `web-service.yaml` expose notre application à l'intérieur du
cluster :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
    - port: 5000
      targetPort: 5000
```

Mais contrairement à Redis, dont le service n'a besoin d'être accessible qu'aux
autres pods, notre application Flask doit être accessible depuis l'extérieur du
cluster. C'est le rôle de l'*ingress*, un dernier type de ressource Kubernetes
qui définit des règles de routage HTTP. Le fichier `web-ingress.yaml` configure
le load balancer intégré de k3d (Traefik) pour rediriger tout le trafic entrant
vers notre service :

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 5000
```

## Déploiement et vérification

On peut maintenant déployer l'ensemble de notre application avec
`kubectl apply` :

```shell
$ kubectl apply -f redis-deployment.yaml -f redis-service.yaml
deployment.apps/redis created
service/redis created

$ kubectl apply -f web-deployment.yaml -f web-service.yaml -f web-ingress.yaml
deployment.apps/web created
service/web created
ingress.networking.k8s.io/web created
```

C'est ici que le modèle déclaratif de Kubernetes prend tout son sens. La
commande `kubectl apply` ne dit pas "crée un container Redis" : elle dit "voici
l'état que je souhaite, assure-toi que la réalité y correspond". Si on exécute
la même commande une deuxième fois, Kubernetes ne crée rien de nouveau : il
constate que l'état actuel correspond déjà à l'état désiré et ne fait rien.
C'est ce qu'on appelle l'*idempotence*, une propriété fondamentale qui rend les
déploiements reproductibles et sûrs.

Avant de tester l'application, vérifions que les pods sont bien en état
`Running` avec `kubectl get pods`. Si un pod reste bloqué en
`ContainerCreating`, la commande `kubectl describe` permet d'inspecter ses
événements et d'identifier le problème&nbsp;:

```shell
$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
redis-6d5dcfd66b-8sk59   1/1     Running   0          46s
web-79d54d9df8-9xjs4     1/1     Running   0          45s

$ kubectl describe pod -l app=web
```

{{% hint warning %}}
Si les événements de `kubectl describe` indiquent une erreur du type
`failed to resolve reference "docker.io/rancher/mirrored-pause:..."`, votre
démon Docker utilise un serveur DNS qui ne répond pas aux requêtes provenant
des containers. La solution est de configurer Docker pour utiliser un serveur
DNS public.

Avec Colima, ajoutez la ligne suivante dans `~/.colima/default/colima.yaml`,
dans la section `network`&nbsp;:

```yaml
dns: [8.8.8.8, 8.8.4.4]
```

Avec Docker Desktop, allez dans **Settings > Docker Engine** et ajoutez la
clé `"dns"` à la configuration JSON&nbsp;:

```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```

Dans les deux cas, redémarrez Docker (`colima restart` ou **Apply & Restart**
dans Docker Desktop), puis supprimez et recréez le cluster k3d.
{{% /hint %}}

On peut maintenant vérifier que l'application fonctionne&nbsp;:

```shell
$ curl localhost:8080/set/hello
[web-79d54d9df8-fsq6j] Your value (hello) is now set in the database

$ curl localhost:8080/get
[web-79d54d9df8-fsq6j] Your stored value is b'hello'
```

Le résultat est fonctionnellement identique à celui obtenu avec docker compose.
La différence visible est le préfixe entre crochets : `web-79d54d9df8-fsq6j`
est le nom unique que Kubernetes a attribué au pod. Ce nom deviendra intéressant
dans un instant, quand nous aurons plusieurs instances.

## Résilience : le moment Kubernetes

Jusqu'ici, notre déploiement Kubernetes produit le même résultat que docker
compose. La différence fondamentale apparait quand quelque chose tourne mal.
Avec docker compose, si un container s'arrête, il reste arrêté (à moins d'avoir
configuré une politique de redémarrage). Kubernetes, lui, surveille en
permanence l'écart entre l'état désiré et l'état réel du cluster. C'est son
*control loop* : un cycle continu d'observation et de correction.

Pour visualiser ce mécanisme, ouvrons k9s dans un terminal :

```shell
$ k9s
```

k9s est une interface textuelle interactive (TUI) qui permet de naviguer dans
les ressources du cluster en temps réel. Les commandes s'entrent en tapant `:`
suivi du nom du type de ressource — k9s ouvre alors un prompt de commande en
bas de l'écran. Par exemple, `:pod` affiche les pods, `:deploy` les
deployments, `:svc` les services, `:ingress` les ingress. La touche `d`
affiche les détails d'une ressource, `l` ses logs, et `Escape` permet de
revenir en arrière. Commençons par naviguer vers la vue des pods avec `:pod`. Par défaut, k9s
affiche les pods de tous les namespaces — pour ne voir que ceux du namespace
`default` (les nôtres), on appuie sur `1`. On y voit alors nos deux pods
(`redis` et `web`) en état `Running`.

{{< image src="k9s-pods.png" alt="" title="" loading="lazy" >}}

Sélectionnons le pod `web` et appuyons sur `Ctrl-k` pour le supprimer (*kill*).
Le pod disparait... et réapparait presque instantanément, avec un nouveau nom.
C'est le deployment qui a détecté que le nombre de pods réels (0) ne
correspondait plus à l'état désiré (`replicas: 1`), et qui en a immédiatement
créé un nouveau. Ce comportement est le coeur de la philosophie Kubernetes : les
pods sont *éphémères*, et c'est normal. Le système ne tente pas de réparer un
pod défaillant, il le remplace. C'est le même principe que l'*immutable
infrastructure* que nous avons évoqué plus haut : plutôt que de corriger, on
reconstruit.

## Scaling

L'autre avantage fondamental de Kubernetes est la facilité avec laquelle on
peut ajuster le nombre d'instances d'un service. Dans k9s, naviguons vers la
vue des deployments en tapant `:deploy`. Sélectionnons le deployment `web` et
appuyons sur `s` pour *scale*. Changeons le nombre de répliques de 1 à 3.

On peut aussi le faire en ligne de commande :

```shell
$ kubectl scale deployment web --replicas=3
```

{{< image src="k9s-3-web-pods.png" alt="" title="" loading="lazy" >}}

En revenant à la vue des pods (`:pod` dans k9s), on voit maintenant trois pods
`web` en état `Running`, chacun avec un nom unique. Notre service et notre
ingress n'ont pas changé, mais ils distribuent maintenant automatiquement le
trafic entre les trois instances. On peut le vérifier :

```shell
$ curl -s localhost:8080/get
[web-79d54d9df8-fsq6j] Your stored value is b'hello'

$ curl -s localhost:8080/get
[web-79d54d9df8-m2x7p] Your stored value is b'hello'

$ curl -s localhost:8080/get
[web-79d54d9df8-k9n4r] Your stored value is b'hello'
```

On constate que le nom du pod change entre les requêtes : le load balancer
(Traefik) répartit le trafic entre nos trois instances. Chacune accède au même
service Redis, donc les données restent cohérentes. C'est exactement le type de
*scaling horizontal* que les architectures cloud-native sont conçues pour
faciliter : plutôt que de donner plus de ressources à une seule machine (scaling
vertical), on ajoute des instances identiques derrière un load balancer. Et
grâce au modèle déclaratif, cette opération est triviale : un seul chiffre à
changer.

Ce tutoriel ne fait qu'effleurer les capacités de Kubernetes. Nous avons
travaillé sur un cluster à un seul *node* (une seule machine), ce qui suffit
pour comprendre les mécanismes fondamentaux. En production, un cluster
Kubernetes est composé de plusieurs nodes, et le *scheduler* se charge de
répartir les pods entre eux. Quand on passe de 1 à 3 répliques, Kubernetes ne
se contente pas de lancer trois processus sur la même machine : il choisit les
nodes les plus appropriés en fonction des ressources disponibles. Si un node
tombe en panne, les pods qu'il hébergeait sont automatiquement recréés sur les
nodes restants. On utiliserait aussi des *namespaces* pour isoler les
environnements, des *ConfigMaps* et des *Secrets* pour gérer la configuration
sensible, des *health checks* pour affiner la détection de pannes, et des
politiques d'*autoscaling* qui ajustent automatiquement le nombre de répliques
en fonction de la charge. Mais l'essentiel est là : un modèle déclaratif où
l'on décrit l'état souhaité, et un système qui converge en permanence vers cet
état. C'est cette philosophie, plus que les détails techniques, qui fait de
Kubernetes la plateforme dominante pour l'orchestration de containers.

Une fois l'exploration terminée, on peut détruire le cluster pour libérer les
ressources :

```shell
$ k3d cluster delete demo
```
