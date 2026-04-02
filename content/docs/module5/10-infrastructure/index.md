---
title: "Où est-ce que ça tourne ?"
weight: 10
slug: "infrastructure"
---

# Où est-ce que ça tourne ?

Pour qu'un logiciel soit accessible à ses utilisateurs, il doit s'exécuter
quelque part. Cette question, en apparence triviale, a donné lieu à l'une des
transformations les plus profondes de l'histoire du génie logiciel. En l'espace
de deux décennies, nous sommes passés de serveurs physiques installés dans des
placards à des plateformes cloud capables de provisionner des milliers de
machines virtuelles en quelques secondes. Cette évolution n'est pas seulement
technique : elle a fondamentalement changé la manière dont on conçoit, déploie et
opère les applications. Comprendre cette trajectoire, des machines physiques
jusqu'aux containers et à l'orchestration, est essentiel pour saisir le contexte
dans lequel les pratiques DevOps modernes ont émergé.

## L'ère du serveur physique

Jusqu'au milieu des années 2000, déployer une application signifiait, de manière
très concrète, installer un serveur. Une entreprise qui voulait mettre un site
web ou une application interne en ligne devait acheter une machine physique (ou
plusieurs), l'installer dans une salle serveur climatisée, la brancher au
réseau, installer un système d'exploitation, configurer les logiciels
nécessaires, et maintenir le tout. Ce processus pouvait prendre des semaines,
voire des mois. Si la demande augmentait et que le serveur n'arrivait plus à
suivre, il fallait commander une nouvelle machine, attendre sa livraison, et
répéter le processus. Pour les organisations qui n'avaient pas les moyens de
maintenir leur propre salle serveur, la *colocation* offrait une alternative : on
achetait le serveur, mais on le plaçait dans un centre de données (datacenter)
géré par un tiers, qui fournissait l'alimentation électrique, la climatisation et
la connectivité réseau. Pour les projets plus modestes, l'*hébergement web*
mutualisé (shared hosting) permettait de louer un espace sur un serveur partagé
entre plusieurs clients, typiquement avec un accès FTP pour déposer ses fichiers
PHP ou HTML. Des entreprises comme OVH (fondée en 1999 en France) ou GoDaddy ont
bâti des empires sur ce modèle. C'était simple et abordable, mais rigide : on
avait peu de contrôle sur l'environnement, et les ressources étaient limitées et
partagées.

## La virtualisation

Le premier grand saut vers l'abstraction de l'infrastructure a été la
virtualisation. L'idée, qui remonte en fait aux mainframes IBM des années 1960,
consiste à faire tourner plusieurs systèmes d'exploitation "invités" sur une
seule machine physique, chacun croyant disposer de sa propre machine dédiée. Un
logiciel appelé *hyperviseur* s'interpose entre le matériel et les systèmes
invités pour gérer ce partage de manière transparente. VMware, fondée en 1998, a
démocratisé cette technologie pour les serveurs x86, suivie par Xen (un projet
open source issu de l'Université de Cambridge en 2003) et KVM (intégré
directement au noyau Linux à partir de 2007). La virtualisation a transformé la
gestion des serveurs de plusieurs manières. D'abord, elle a permis de consolider
plusieurs serveurs physiques sous-utilisés en un seul, réduisant les coûts
matériels et énergétiques. Ensuite, elle a rendu possible la création de
nouvelles machines en minutes plutôt qu'en semaines : il suffisait de créer une
nouvelle machine virtuelle (VM) à partir d'une image préexistante. Enfin, elle a
introduit l'idée fondamentale que l'infrastructure pouvait être manipulée comme
une ressource logicielle, créée, copiée, déplacée et détruite à la demande.
C'est cette idée qui allait rendre le cloud possible.

## Le cloud

La virtualisation a rendu l'infrastructure manipulable comme du logiciel. Le
cloud a poussé cette logique à sa conclusion naturelle : pourquoi posséder des
serveurs quand on peut en louer à la demande ? Le moment fondateur est le
lancement d'Amazon Web Services (AWS) en 2006, avec son service EC2 (Elastic
Compute Cloud), qui permettait à n'importe qui de créer une machine virtuelle en
quelques minutes, via une API, et de payer uniquement pour le temps
d'utilisation. L'origine d'AWS est elle-même révélatrice : Amazon avait développé
une infrastructure massive pour faire fonctionner son site de commerce en ligne,
et a réalisé qu'elle pouvait la revendre comme service. Google Cloud Platform
(GCP, 2008) et Microsoft Azure (2010) ont suivi, créant un oligopole qui domine
encore aujourd'hui le marché.

Le cloud est généralement décrit en trois niveaux d'abstraction, souvent
représentés sous forme de couches. L'*Infrastructure as a Service* (IaaS) est la
couche la plus basse : on loue des machines virtuelles, du stockage et du réseau,
et on gère soi-même le système d'exploitation et les logiciels (c'est le modèle
d'EC2). La *Platform as a Service* (PaaS) monte d'un cran : le fournisseur gère
l'infrastructure et le runtime, et le développeur ne déploie que son code. Heroku
(2007), la plateforme dont est issue la Twelve-Factor App, est l'exemple
emblématique de ce modèle : un simple `git push heroku main` suffisait pour
déployer une application. Enfin, le *Software as a Service* (SaaS) est la couche
la plus abstraite : l'utilisateur final consomme un logiciel complet sans se
soucier de l'infrastructure (Gmail, Slack, Salesforce). Ces trois niveaux ne sont
pas mutuellement exclusifs : une même organisation peut utiliser du IaaS pour
certains composants et du PaaS pour d'autres.

<!-- ILLUSTRATION: diagramme des trois couches IaaS/PaaS/SaaS avec exemples -->

L'adoption du cloud a été rapide et massive. Netflix, après une panne majeure de
son datacenter en 2008, a entrepris une migration complète vers AWS qui est
devenue un cas d'étude en architecture cloud (et a produit au passage de nombreux
outils open source que nous retrouverons plus loin). Airbnb est sur AWS depuis
ses débuts, un exemple emblématique de startup qui n'a jamais possédé de serveur
physique. Spotify a migré de ses propres serveurs vers Google Cloud Platform en
2016. À l'inverse, Dropbox a fait le chemin inverse en 2016, quittant AWS pour
construire sa propre infrastructure, estimant qu'à son échelle les économies
justifiaient l'investissement. Ce dernier cas illustre que le cloud n'est pas une
fin en soi : c'est un compromis entre flexibilité, coût et contrôle, et la bonne
réponse dépend du contexte.

## Le serverless

Le modèle PaaS a ouvert la voie à une abstraction encore plus radicale : le
*serverless*, ou plus précisément le *Function as a Service* (FaaS). L'idée est
simple : au lieu de déployer une application qui tourne en permanence sur un
serveur (même virtuel), on déploie des fonctions individuelles qui sont exécutées
à la demande, en réponse à des événements. AWS Lambda, lancé en 2014, a
popularisé ce modèle. On écrit une fonction (par exemple en Python), on la
déploie sur Lambda, et elle est exécutée uniquement quand un événement
déclencheur survient : une requête HTTP, un message dans une file d'attente, un
fichier déposé dans un bucket S3. On ne paie que pour le temps d'exécution réel,
mesuré à la milliseconde. Google Cloud Functions et Azure Functions offrent des
services équivalents.

Le nom "serverless" est bien sûr trompeur : il y a toujours des serveurs quelque
part, mais le développeur n'a plus à s'en soucier. C'est l'aboutissement logique
de la trajectoire d'abstraction que nous avons suivie, du serveur physique à la
VM, de la VM au PaaS, du PaaS à la fonction. Mais cette abstraction a un coût.
Le *cold start* (le délai de démarrage quand une fonction n'a pas été appelée
récemment) peut poser des problèmes de latence. Le débogage et le monitoring
deviennent plus difficiles quand la logique est dispersée dans des dizaines de
fonctions. Et le risque de *vendor lock-in* (dépendance au fournisseur cloud) est
maximal, puisque chaque plateforme a ses propres conventions et services. Le
serverless est donc particulièrement adapté à certains cas d'usage (traitement
d'événements, tâches ponctuelles, backends légers), mais ne remplace pas les
architectures plus traditionnelles pour des systèmes complexes.

## La conteneurisation

Parallèlement à l'essor du cloud, une autre approche de l'isolation a émergé,
plus légère que la virtualisation classique. L'idée de base est ancienne : la
commande `chroot` d'Unix, disponible depuis 1979, permettait déjà de restreindre
la vision du système de fichiers d'un processus. Au fil des années, le noyau
Linux a développé des mécanismes d'isolation de plus en plus sophistiqués : les
*cgroups* (control groups, 2006), qui permettent de limiter les ressources (CPU,
mémoire) allouées à un groupe de processus, et les *namespaces* (2002-2013), qui
isolent différents aspects du système (réseau, identifiants de processus, système
de fichiers). Ces primitives existaient, mais restaient difficiles à utiliser
directement. En 2013, Solomon Hykes et son entreprise dotCloud (qui deviendra
Docker Inc) ont lancé Docker, un outil qui rend ces mécanismes accessibles à
travers une interface simple et élégante. Au lieu de virtualiser une machine
complète avec son propre noyau (comme le fait une VM), un container partage le
noyau du système hôte tout en maintenant une isolation quasi complète de
l'environnement applicatif. Le résultat est beaucoup plus léger qu'une VM : un
container démarre en secondes plutôt qu'en minutes, et consomme une fraction des
ressources. Docker a également popularisé le concept d'*image* comme artefact
reproductible et distribuable, résolvant de manière élégante le fameux problème
"ça marche sur ma machine".

Voyons concrètement comment Docker fonctionne.

### Qu'est-ce que c'est ?

Docker est un programme qui permet de "packager" une application ainsi que la
totalité de son environnement dans un fichier spécial appelé une *image*. Une
fois que cette image est disponible, Docker permet de créer et exécuter une
instance dynamique à partir de celle-ci, sous la forme d'un *container*. Un
container constitue un environnement complètement isolé du système
d'exploitation "hôte", qui exécute Docker, ainsi que des autres containers.
Cette isolation s'applique également au disque et au réseau, mais il est
possible d'introduire des exceptions à l'aide de différents mécanismes, que nous
allons explorer. Notons qu'il peut être utile de se représenter le concept
d'image comme correspondant grosso modo à celui d'une _classe_ (au sens
orienté-objet), et un container son _instance_.

### En quoi ça diffère d'une VM ?

Bien que ce modèle ressemble en apparence à celui d'une machine virtuelle (VM),
il est assez différent : au lieu de faire l'émulation complète d'une machine
physique, comme c'est le cas avec les VMs du genre VMWare ou VirtualBox, Docker
partage plutôt le système d'exploitation hôte, en utilisant ses primitives de
virtualisation. Cette différence fait en sorte que Docker est beaucoup moins
gourmand en ressources qu'une VM, et permet donc de meilleures performances.
Bien que Docker soit disponible pour toutes les plateformes, il ne peut rouler
nativement que sur Linux (originalement) et Windows (plus récemment, et moins
typiquement), tandis que sous MacOS, une couche de virtualisation supplémentaire
est nécessaire.

### Quel problème ça résout ?

Une application moderne repose sur un assemblage impressionnant de composantes
logicielles qu'il est pratiquement impossible de contrôler dans ses moindres
détails : votre environnement Conda a beau contenir exactement les mêmes
versions des bibliothèques Python que celui de votre collègue, il est possible
qu'une différence subtile subsiste dans une des composantes se trouvant dans les
profondeurs du système d'exploitation, susceptible de causer des problèmes
difficiles à diagnostiquer. Docker permet de résoudre ce problème d'une manière
assez radicale, en permettant de créer, reproduire et distribuer un
environnement dans sa totalité, en sacrifiant un minimum de performance. La
métaphore du container de transport maritime prend ainsi son sens, car il permet
de résoudre un problème apparenté dans le monde physique : rendre plus robuste
le transport des choses fragiles en les compartimentant.

En pratique, Docker est pratique et utile dans deux scénarios distincts : quand
une application complexe doit être déployée et gérée en production, et quand un
développeur veut reproduire un environnement complexe (celui de production par
exemple) localement, sans avoir à gérer une multitude de composantes complexes
sur le système hôte.

### Comment l'utiliser

#### Définir une image : Dockerfile

Supposons que nous voulions créer un petit outil Python qui effectue une tâche
très simple, avec la ligne de commande. Créons tout d'abord un répertoire de
travail :

```shell
$ mkdir util
$ cd util
```

Créons ensuite un petit programme simple en python, `say_hello.py` :

```python
import sys

name = sys.argv[1] if len(sys.argv) > 1 else 'TELUQ'

print(f'Hello {name}!')
```

On peut tout d'abord vérifier que notre programme fonctionne localement :

```shell
$ python say_hello.py
Hello TELUQ!
$ python say_hello.py Leila
Hello Leila!
```

On peut maintenant conteneuriser ("dockeriser") notre programme en créant tout
d'abord une image, que l'on pourra exécuter ensuite en tant que container. La
composition de l'image est définie par un fichier spécial nommé `Dockerfile`,
qui contient les commandes pour sa création :

```dockerfile
FROM python

COPY say_hello.py /inside_container/

WORKDIR /inside_container

ENTRYPOINT ["python", "say_hello.py"]
```

La commande `FROM` spécifie le nom de l'image (nommée `python`) de laquelle
notre propre image hérite (ou dérive), publiée sur Docker Hub, un répertoire
public d'images Docker. Dans ce cas particulier il s'agit d'une image
officielle, associée à un projet GitHub. Si on consulte ce projet, on peut y
trouver un
[Dockerfile](https://github.com/docker-library/python/blob/master/3.10/buster/Dockerfile)
(dans ce cas pour la version 3.10 de Python), qui contient lui-même une commande
[FROM](https://github.com/docker-library/python/blob/9242c448c7e50d5671e53a393fc2c464683f35dd/3.10/buster/Dockerfile#L7)
pointant vers une autre image en amont (`buildpack-deps`). Ceci démontre
l'aspect modulaire et récursif de Docker.

La commande `COPY` crée une copie de notre programme, qui correspond à son état
au moment de la création de l'image, à l'emplacement désigné (le répertoire
`/inside_container` n'existera que dans le container, quand il sera créé).
`WORKDIR` spécifie le répertoire courant qui sera utilisé par la commande
suivante `ENTRYPOINT`, qui détermine la ligne de commande qui sera utilisée par
défaut quand le container sera exécuté.

#### Créer une image : docker build

Pour créer notre image, qu'on nommera `hello`, la commande `build` prend en
entrée notre `Dockerfile` :

```shell
$ docker build . -t hello
Sending build context to Docker daemon  3.072kB
Step 1/4 : FROM python
 ---> cba42c28d9b8
Step 2/4 : COPY say_hello.py /inside_container/
 ---> 1857eaae8006
Step 3/4 : WORKDIR /inside_container
 ---> Running in 82f776c710c1
Removing intermediate container 82f776c710c1
 ---> 1bb7d819208c
Step 4/4 : ENTRYPOINT ["python", "say_hello.py"]
 ---> Running in 7721eec86a70
Removing intermediate container 7721eec86a70
 ---> 4f7eb5601e46
Successfully built 4f7eb5601e46
Successfully tagged hello:latest
```

On peut vérifier la présence de la nouvelle image en utilisant la commande
`docker images` :

```shell
$ docker images
REPOSITORY      TAG       IMAGE ID       CREATED        SIZE
hello           latest    3bfd9d7c3faf   25 hours ago   886MB
```

#### Créer et démarrer un container : docker run

Une fois qu'une image existe, on peut en instancier un (ou plusieurs)
container à volonté. Étant donné que notre premier exemple est celui
d'un programme en ligne de commande (CLI), le cycle de vie de notre
container sera bref : il sera tout d'abord créé, sa commande (définie
par le `ENTRYPOINT` dans le `Dockerfile`) sera ensuite exécutée, pour
être finalement stoppé. C'est ce que fait la commande `docker run
<image> [args]` :

```shell
$ docker run hello
Hello TELUQ!
$ docker run hello Leila
Hello Leila!
```

Comment ferait-on pour ajouter une dépendance Python à notre programme? Essayons
avec une simple modification :

```python
import sys
import cowsay

name = sys.argv[1] if len(sys.argv) > 1 else 'TELUQ'

cowsay.cow(f'Hello {name}!')
```

Si on exécute la commande `docker run` de nouveau à ce point, rien n'aura
changé, parce que nous n'avons modifié le fichier `say_hello.py` que localement,
et non dans l'image. Pour que le changement soit effectif, on doit reconstruire
l'image :

```shell
$ docker build . -t hello
```

On peut ensuite tenter d'exécuter la nouvelle version :

```shell
$ docker run hello Leila
Traceback (most recent call last):
  File "/inside_container/say_hello_cow.py", line 2, in <module>
    import cowsay
ModuleNotFoundError: No module named 'cowsay'
```

Cette erreur démontre que le container est un environnement complètement isolé,
dont l'état dépend entièrement de l'image dont il provient. Étant donné nous
n'avons pas installé de bibliothèques supplémentaires au moment de la création de
l'image, la bibliothèque `cowsay` est introuvable. Pour l'ajouter nous devons donc
modifier le `Dockerfile` :

```dockerfile
FROM python

RUN pip install cowsay

COPY say_hello.py /inside_container/

WORKDIR /inside_container

ENTRYPOINT ["python", "say_hello.py"]
```

La nouvelle version de notre `Dockerfile` ajoute une commande `RUN`, qui
effectue l'installation avec `pip` de la bibliothèque `cowsay`. On peut ensuite
créer une nouvelle image, que l'on nommera `hello-cow` pour la distinguer de la
précédente :

```shell
$ docker build . -t hello-cow
Sending build context to Docker daemon  3.072kB
Step 1/5 : FROM python
 ---> cba42c28d9b8
Step 2/5 : RUN pip install cowsay
 ---> Using cache
 ---> a3f8e71ae03c
Step 3/5 : COPY say_hello.py /inside_container/
 ---> Using cache
 ---> 5130c35145ab
Step 4/5 : WORKDIR /inside_container
 ---> Using cache
 ---> a0b2779bc537
Step 5/5 : ENTRYPOINT ["python", "say_hello.py"]
 ---> Using cache
 ---> 0438117446f5
Successfully built 0438117446f5
Successfully tagged hello-cow:latest
```

On peut tester que la nouvelle image fonctionne en créant un nouveau container :

```shell
$ docker run hello-cow Leila
 ______________
| Hello Leila! |
 ==============
              \
               \
                 ^__^
                 (oo)\_______
                 (__)\       )\/\
                     ||----w |
                     ||     ||
```

#### Partager un répertoire (volume) avec l'hôte

Dans l'exemple précédent, comme la modification à notre programme impliquait
l'ajout d'une bibliothèque, la modification de l'image était inévitable. Dans le
processus de développement d'une application par contre, la plupart des
modifications impliquent seulement le code source, et il serait donc intéressant
de ne pas avoir à payer le coût de la reconstruction de l'image à chaque fois.
Docker permet à un container de partager un répertoire (sous la forme d'un
*volume*) avec le système hôte avec le mécanisme de "bind mount". Pour en faire
l'essai, modifions encore une fois notre programme, cette fois-ci d'une manière
qui ne demande pas l'ajout d'une nouvelle bibliothèque :

```python
import sys
import datetime as dt
import cowsay

name = sys.argv[1] if len(sys.argv) > 1 else 'TELUQ'

wd = dt.datetime.today().strftime('%A')

cowsay.cow(f'Hello {name}, today is {wd}!')
```

Comme nous l'avons vu dans la section précédente, cette modification ne pourrait
pas avoir d'effet immédiat, car le fichier `say_hello.py` a seulement été
modifié localement, sur l'hôte, et non dans l'image. Avec l'usage d'un volume
partagé, cette modification devient néanmoins visible immédiatement au
container, sans avoir besoin de reconstruire l'image :

```shell
$ docker run -v $(pwd):/inside_container hello-cow
  ______________________________
| Hello TELUQ, today is Monday! |
  ==============================
                                \
                                 \
                                   ^__^
                                   (oo)\_______
                                   (__)\       )\/\
                                       ||----w |
                                       ||     ||
```

La syntaxe de l'argument passé à `-v` est en deux parties (séparées par un `:`):
à gauche le chemin complet (absolu) d'un répertoire sur l'hôte qu'on veut
partager (déterminé ici dynamiquement avec la commande Bash `pwd`), à droite
l'endroit correspondant, dans le container.

#### Gérer un groupe de containers : docker compose

Nous allons maintenant décrire un scénario où nous voulons créer une application
qui nécessite plusieurs containers. L'outil `docker compose` permet de créer et
orchestrer un groupe de containers de manière très conviviale, toujours avec la
ligne de commande, à l'aide d'un seul fichier de configuration. Docker compose
ne remplace pas l'outil Docker tout court, il en enrichit seulement l'interface :
tout ce que fait docker compose pourrait être accompli avec Docker seulement.

Créons un nouveau répertoire de travail :

```shell
$ mkdir app
$ cd app
```

Notre application est constituée de deux serveurs : un serveur _applicatif_,
écrit en Python avec Flask, un framework web. L'autre est basé sur Redis, une
base de données de type "key/value" (dont le rôle est simplement d'associer une
valeur quelconque à une clé). Étant donné qu'il s'agit ici d'un _service_, censé
fonctionner de manière continue, sans interruption, le comportement des
containers sera différent de celui de l'utilitaire que nous avons créé dans la
section précédente, dont la durée de vie était très courte. Dans ce scénario on
veut démarrer des containers qui vont rouler jusqu'à nouvel ordre, quand on
décidera de les terminer explicitement.

Voici tout d'abord le `Dockerfile` pour l'application Flask, encore
une fois basée sur une image `python` officielle :

```dockerfile
FROM python

RUN pip install flask redis
```

Cette application est entièrement contenue dans le fichier `main.py` :

```python
from flask import Flask
import redis

app = Flask(__name__)

red = redis.Redis("db")
KEY = "some_key"

@app.route("/set/<val>")
def set_value(val):
    red.set(KEY, val)
    return f"Your value ({val}) is now set in the database"

@app.route("/get")
def get_value():
    val = red.get(KEY)
    if val is None:
        return "No value was stored, use /set"
    return f"Your stored value is {val}"
```

Notre application web définit deux routes : `/set/<val>`, qui associe
une valeur à une clé Redis (par exemple `/set/123`, qui associe `123`
à la clé `some_key`) et `/get`, qui la retourne.

Le dernier fichier nécessaire est la configuration YAML pour `docker compose` :

```yaml
services:

  web:
    build: .
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: development
      FLASK_APP: main
    working_dir: /app
    command: "flask run --host 0.0.0.0"

  db:
    image: redis
```

Les clés `web` et `db` (de l'objet parent `services`) correspondent aux deux
containers qui composent notre application. Le container `web` est notre
programme Python, donc défini par le `Dockerfile`, via la clé
`services.web.build`.

La clé `db` correspond à un deuxième container qui ne nécessite aucune phase de
build (donc de `Dockerfile`) car nous utilisons l'image officielle, `redis`,
telle quelle, sans modification particulière.

On peut maintenant démarrer notre application avec la commande `docker compose
up`, qui est un amalgame des commandes `docker build` et `docker run`, opérant
dans le contexte du groupe d'images et de containers défini par le fichier YAML :

```shell
$ docker compose up -d
Creating network "app_default" with the default driver
Building web
Sending build context to Docker daemon   7.68kB
Step 1/2 : FROM python
 ---> cba42c28d9b8
Step 2/2 : RUN pip install flask redis
 ---> Using cache
 ---> 8f66deffb444
Successfully built 8f66deffb444
Successfully tagged app_web:latest
Creating app_web_1 ... done
Creating app_db_1  ... done
```

Le fait d'avoir utilisé l'option `-d` fait en sorte que les deux containers de
l'application sont démarrés en "background", comme on peut le constater en
utilisant la commande `docker compose ps` :

```shell
$ docker compose ps
  Name    Command               State  Ports
-------------------------------------------------------------
app_db_1  docker-entrypoint.sh  Up     6379/tcp
app_web_1 flask run --host ...  Up     0.0.0.0:8080->5000/tcp
```

On remarque tout d'abord que le container `web` exécute la commande `flask run`,
spécifiée dans le fichier YAML (`services.web.command`), tandis que le container
`db` exécute une commande par défaut définie dans l'image `redis`. Le
comportement de la commande `flask run` est modulé par la valeur de certaines
variables d'environnement propres à Flask, également définies dans le fichier de
configuration (`services.web.environment`). Un volume partagé
(`services.web.volume`) permet de rendre le développement encore une fois plus
convivial.

Docker compose crée un réseau privé interne qui permet aux containers de
communiquer entre eux, en utilisant simplement leur nom en tant que nom de
domaine. Un exemple de ceci est utilisé dans `main.py` :

```python
red = redis.Redis("db")
```

où `db` correspond au nom du container Redis (défini dans notre
configuration YAML) qui est accessible au container Python (`web`).

Finalement, la configuration `8080:5000` pour `services.web.ports` est cruciale
pour notre application car elle permet de diriger le traffic du container `web`,
dont le serveur écoute sur le port interne 5000, vers le port 8080 de l'hôte.
Sans cette configuration, le URL `web:5000` serait _seulement_ accessible au
container `redis`, complètement isolé de l'extérieur donc.

Il est facile de tester ce mécanisme avec un outil local (présent sur
l'hôte), comme un navigateur ou `curl` :

```shell
$ curl localhost:8080/set/hello
Your value (hello) is now set in the database
$ curl localhost:8080/get
Your stored value is b'hello'
```

#### Exécuter un programme dans un container en marche : docker compose exec

Comme les containers de notre service roulent de manière continue, en attente de
servir des requêtes, il est possible d'exécuter un programme dans un container
en marche avec la commande `docker exec <container> <command>`. Ceci démarrera
un process _en plus_ de celui qui roule déjà dans le container. La seule
condition est que le programme désiré soit disponible dans le container, donc
qu'il fasse partie de son image. Docker compose rend l'usage d'`exec` légèrement
plus convivial, avec sa commande correspondante. Voici par exemple comment
utiliser `redis-cli`, un outil de ligne de commande qui permet d'interagir avec
Redis, et qui est disponible à même notre container `db` :

```shell
$ docker compose exec db redis-cli
127.0.0.1:6379>
127.0.0.1:6379>
127.0.0.1:6379> keys *
1) "some_key"
127.0.0.1:6379> get some_key
"123"
```

Cet exemple montre qu'il est facile et pratique d'examiner ou monitorer l'état
de notre application de manière "live", à l'aide de nos outils habituels. Pour
les images qui sont basées ultimement sur un système de type Linux (ce qu'il est
possible de déterminer en suivant la chaîne récursive de commandes `FROM`, de
`Dockerfile` en `Dockerfile`), il est également souvent possible de démarrer un
shell :

```shell
$ docker compose exec web bash
root@d84bfe7aef1f:/app# ls -al
total 24
drwxrwxr-x 3 1000 1000 4096 Nov  3 17:14 .
drwxr-xr-x 1 root root 4096 Nov  3 16:26 ..
-rw-rw-r-- 1 1000 1000   41 Nov  1 19:48 Dockerfile
drwxr-xr-x 2 root root 4096 Nov  3 17:14 __pycache__
-rw-rw-r-- 1 1000 1000  244 Nov  3 16:26 docker-compose.yml
-rw-rw-r-- 1 1000 1000  398 Nov  3 17:14 main.py
```

## L'orchestration

Docker compose, que nous venons de voir, permet de gérer un groupe de containers
sur une seule machine. Mais que se passe-t-il quand une application doit tourner
sur des dizaines ou des centaines de machines, avec des exigences de haute
disponibilité ? Si un container tombe, qui le redémarre ? Si la charge augmente,
qui décide de créer de nouvelles instances ? Comment répartir le trafic entre les
containers disponibles ? Ces questions définissent le problème de
l'*orchestration*.

Google a été confronté à ce problème très tôt. En interne, l'entreprise
utilisait depuis le milieu des années 2000 un système appelé Borg pour gérer des
millions de containers à travers ses datacenters. En 2014, Google a décidé de
publier une version open source des idées de Borg sous le nom de Kubernetes (du
grec "pilote" ou "timonier", souvent abrégé K8s). Le projet a rapidement été
adopté par l'industrie et est aujourd'hui le standard de facto pour
l'orchestration de containers.

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

### Tutoriel : de docker compose à Kubernetes

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

#### Préparation

Avant de commencer, adaptons légèrement notre application Flask. Kubernetes
attribue automatiquement un nom unique à chaque pod, accessible via la variable
d'environnement `HOSTNAME` à l'intérieur du container. Nous allons modifier
`main.py` pour afficher ce nom, ce qui nous sera utile plus tard pour observer
le comportement du cluster quand plusieurs instances de notre application
tournent en parallèle :

```python
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

#### Le deployment Redis

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

#### Le deployment Flask

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

#### Déploiement et vérification

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

On peut vérifier que l'application fonctionne :

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

#### Résilience : le moment Kubernetes

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
les ressources du cluster en temps réel. Par défaut, la vue affiche les pods.
On y voit nos deux pods (`redis` et `web`) en état `Running`. On peut naviguer
entre différentes vues avec les raccourcis clavier : `:deploy` pour voir les
deployments, `:svc` pour les services, `:ingress` pour les ingress. La touche
`d` affiche les détails d'une ressource, `l` ses logs, et `Escape` permet de
revenir en arrière.

<!-- ILLUSTRATION: capture d'écran de k9s montrant les pods redis et web en état Running -->

Sélectionnons le pod `web` et appuyons sur `Ctrl-k` pour le supprimer (*kill*).
Le pod disparait... et réapparait presque instantanément, avec un nouveau nom.
C'est le deployment qui a détecté que le nombre de pods réels (0) ne
correspondait plus à l'état désiré (`replicas: 1`), et qui en a immédiatement
créé un nouveau. Ce comportement est le coeur de la philosophie Kubernetes : les
pods sont *éphémères*, et c'est normal. Le système ne tente pas de réparer un
pod défaillant, il le remplace. C'est le même principe que l'*immutable
infrastructure* que nous avons évoqué plus haut : plutôt que de corriger, on
reconstruit.

#### Scaling

L'autre avantage fondamental de Kubernetes est la facilité avec laquelle on
peut ajuster le nombre d'instances d'un service. Dans k9s, naviguons vers la
vue des deployments en tapant `:deploy`. Sélectionnons le deployment `web` et
appuyons sur `s` pour *scale*. Changeons le nombre de répliques de 1 à 3.

On peut aussi le faire en ligne de commande :

```shell
$ kubectl scale deployment web --replicas=3
```

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

Le nom du pod change entre les requêtes : le load balancer (Traefik) répartit
le trafic entre nos trois instances. Chacune accède au même service Redis, donc
les données restent cohérentes. C'est exactement le type de *scaling horizontal*
que les architectures cloud-native sont conçues pour faciliter : plutôt que de
donner plus de ressources à une seule machine (scaling vertical), on ajoute des
instances identiques derrière un load balancer. Et grâce au modèle déclaratif,
cette opération est triviale : un seul chiffre à changer.

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

## L'infrastructure comme code

Jusqu'ici, nous avons traité l'infrastructure comme une donnée : le cluster
Kubernetes existe, les serveurs tournent, le réseau fonctionne. Mais d'où vient
cette infrastructure ? Concrètement, l'infrastructure d'un système logiciel,
c'est tout ce qui doit exister *avant* que le code puisse s'exécuter : les
serveurs (physiques ou virtuels), les réseaux (sous-réseaux, règles de
pare-feu, load balancers), le stockage (disques, espaces de stockage cloud),
les bases de données, les certificats SSL, les entrées DNS. Pendant longtemps,
cette infrastructure était créée et configurée manuellement : un administrateur
se connectait à une console cloud pour créer un serveur, puis en SSH pour
installer des paquets et modifier des fichiers de configuration. Le résultat
était ce qu'on appelle un *snowflake server* : une machine unique, configurée à
la main au fil du temps, dont personne ne sait exactement reproduire l'état. Si
elle tombe en panne, la reconstruire à l'identique relève de l'archéologie.

L'*infrastructure as code* (IaC) est la réponse à ce problème : décrire toute
l'infrastructure dans des fichiers de configuration versionnés, et laisser un
outil se charger de créer ou de modifier les ressources pour correspondre à
cette description. Le paradigme devrait nous être familier à ce stade du cours :
c'est exactement le modèle déclaratif que nous avons rencontré dans SQL
(décrire les données souhaitées, pas comment les chercher), dans les fichiers
YAML de Kubernetes (décrire l'état souhaité du cluster, pas les étapes pour y
arriver), et même dans le Dockerfile (décrire l'image souhaitée, pas comment la
construire pas à pas). À chaque fois, le même patron se répète : on décrit
*quoi*, pas *comment*, et un moteur se charge de la convergence. Et à chaque
fois, la même propriété en découle : l'idempotence. On peut réappliquer la même
description autant de fois qu'on veut, et si l'état réel correspond déjà à
l'état souhaité, rien ne se passe.

L'outil le plus influent dans ce domaine est Terraform, créé par HashiCorp en
2014. Terraform utilise un langage déclaratif appelé HCL (*HashiCorp
Configuration Language*) pour décrire des ressources cloud. Voici un exemple
minimal qui crée un serveur virtuel sur AWS :

```hcl
provider "aws" {
  region = "ca-central-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "web-server"
  }
}
```

La commande `terraform plan` compare cette description à l'état réel de
l'infrastructure et affiche les changements nécessaires, sans rien exécuter. La
commande `terraform apply` effectue ces changements. Si on relance
`terraform apply` sans modifier le fichier, Terraform ne fait rien : l'état
réel correspond déjà à l'état souhaité. Pour rendre cette comparaison possible,
Terraform maintient un fichier d'*état* (*state*) qui enregistre la
correspondance entre les ressources décrites dans le code et les ressources
réelles chez le fournisseur cloud. Ce fichier d'état est essentiel : sans lui,
Terraform ne saurait pas si le serveur `web` existe déjà ou s'il doit être
créé.

Terraform excelle au *provisioning* : créer et gérer les ressources
d'infrastructure elles-mêmes (serveurs, réseaux, bases de données). Mais une
fois qu'un serveur existe, il faut souvent le *configurer* : installer des
paquets, déployer des fichiers de configuration, démarrer des services. C'est
le domaine du *configuration management*, dont les pionniers furent Puppet
(2005) et Chef (2009). Ces outils installaient un agent sur chaque machine, qui
communiquait avec un serveur central pour maintenir la configuration souhaitée.
Ansible (Red Hat, 2012) a simplifié cette approche en éliminant l'agent : il se
connecte directement en SSH et exécute des tâches décrites dans des fichiers
YAML appelés *playbooks*. Un playbook Ansible pour installer et démarrer Nginx
ressemble à ceci :

```yaml
- hosts: webservers
  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present

    - name: Start Nginx
      service:
        name: nginx
        state: started
```

On retrouve le même vocabulaire déclaratif : `state: present` signifie
"assure-toi que ce paquet est installé", pas "installe ce paquet". Si Nginx est
déjà installé, Ansible ne fait rien. En pratique, Terraform et Ansible sont
souvent complémentaires : Terraform crée les machines, Ansible les configure.
Mais avec la montée des containers et de Kubernetes, la frontière entre
provisioning et configuration s'estompe : le Dockerfile *est* la configuration
de la machine, et Kubernetes *est* le provisioning de l'application.

Le mot "code" dans "infrastructure as code" n'est pas anodin. Puisque
l'infrastructure est décrite dans des fichiers texte, elle bénéficie de tous
les outils que nous avons étudiés dans ce cours : versioning avec git, revue
par les pairs via pull requests, tests automatisés dans un pipeline CI. On peut
voir l'historique complet des changements d'infrastructure, revenir à un état
antérieur, et reproduire un environnement identique à partir de zéro. C'est la
même idée que le Dockerfile qui rend un environnement de développement
reproductible, mais étendue à l'ensemble de l'infrastructure. Le terme *GitOps*,
popularisé par Weaveworks en 2017, désigne cette pratique poussée à son
extrême : le dépôt git devient la source de vérité unique pour l'état de tout
le système, et chaque changement, qu'il concerne le code applicatif ou
l'infrastructure, passe par le même processus de commit, revue et déploiement
automatisé.