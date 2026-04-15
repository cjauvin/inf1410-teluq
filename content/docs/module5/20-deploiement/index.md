---
title: "Le déploiement continu (CD)"
weight: 20
slug: "deploiement"
---

# Comment je le déploie ?

Dans le module 2, nous avons mis en place un pipeline d'intégration continue
(CI) : à chaque commit poussé sur GitHub, une série de vérifications
automatiques (tests, linting, typage) s'exécutent pour détecter les problèmes le
plus tôt possible. Mais la CI s'arrête à la vérification. Elle répond à la
question "est-ce que ce code est correct ?", pas à la question "comment est-ce
que ce code arrive en production ?". Ce passage de la vérification au
déploiement est le sujet de cette section.

Pendant longtemps, le déploiement était un événement. Dans beaucoup
d'organisations, il avait lieu une fois par mois, voire une fois par trimestre,
selon un calendrier rigide. Il impliquait des procédures manuelles, des listes
de vérification sur papier, et souvent une fenêtre de maintenance nocturne
pendant laquelle l'application était indisponible. Les déploiements étaient
stressants précisément parce qu'ils étaient rares : chaque release accumulait des
semaines de changements, ce qui rendait le diagnostic des problèmes difficile
quand quelque chose tournait mal. Le livre *Continuous Delivery* de Jez Humble et
David Farley (2010) a proposé une inversion radicale de cette logique. Leur
argument central : si les déploiements sont douloureux, la solution n'est pas de
les faire moins souvent, mais *plus souvent*. Un déploiement qui contient un seul
changement est facile à comprendre, facile à tester, et facile à annuler si
quelque chose ne va pas. La clé est l'automatisation complète du chemin entre le
commit et la production, ce que Humble et Farley appellent le *deployment
pipeline*.

Il faut ici clarifier une ambiguïté terminologique qui crée beaucoup de
confusion. Le sigle "CD" désigne en fait deux pratiques distinctes. Le
*continuous delivery* (livraison continue) signifie que le code est toujours dans
un état déployable : chaque commit qui passe le pipeline de vérification produit
un artefact prêt à être mis en production, mais le déploiement lui-même est
déclenché manuellement, par un humain qui appuie sur un bouton. Le *continuous
deployment* (déploiement continu) va un cran plus loin : chaque commit qui passe
les vérifications est automatiquement déployé en production, sans intervention
humaine. La différence est subtile mais importante. En continuous delivery, le
dernier rempart est une décision humaine ("on déploie maintenant"). En continuous
deployment, cette décision est éliminée : si les tests passent, le code est en
production. Des entreprises comme GitHub ou Netflix pratiquent le continuous
deployment, avec parfois des dizaines de déploiements par jour. La plupart des
organisations commencent par le continuous delivery, qui offre déjà un gain
considérable par rapport aux déploiements manuels, avant d'éventuellement
évoluer vers le continuous deployment lorsque la confiance dans le pipeline est
suffisante.

## Le pipeline de déploiement avec GitHub Actions

Dans le module 2, notre workflow GitHub Actions avait un seul job (`tests`) qui
installait les dépendances et exécutait pytest. Pour passer de la CI au CD, il
suffit conceptuellement d'ajouter un deuxième job qui se déclenche après la
réussite du premier. Voici à quoi pourrait ressembler un workflow CI/CD complet
pour notre application Flask déployée sur Kubernetes (que nous avons construite
dans la section précédente) :

```yaml
name: CI/CD

on:
  push:
    branches: ["main"]

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Installer Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Installer uv
        uses: astral-sh/setup-uv@v3

      - name: Installer les dépendances
        run: uv sync

      - name: Exécuter les tests
        run: uv run pytest

  deploy:
    runs-on: ubuntu-latest
    needs: tests
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Construire l'image Docker
        run: docker build -t flask-app:${{ github.sha }} .

      - name: Pousser l'image vers le registre
        run: |
          echo "${{ secrets.REGISTRY_PASSWORD }}" | \
            docker login -u "${{ secrets.REGISTRY_USER }}" --password-stdin
          docker push flask-app:${{ github.sha }}

      - name: Déployer sur Kubernetes
        run: |
          kubectl set image deployment/web \
            web=flask-app:${{ github.sha }}
```

Le job `tests` devrait être familier : c'est essentiellement le même workflow que
celui du module 2, avec les mêmes commandes (`uv sync` pour installer les
dépendances, `uv run pytest` pour exécuter les tests). La nouveauté est le job
`deploy`, qui enchaîne trois commandes que nous connaissons déjà de la section
précédente : `docker build` pour construire l'image de notre application,
`docker push` pour la pousser vers un registre d'images (l'équivalent distant de
ce que faisait `k3d image import` dans notre tutoriel local), et `kubectl set
image` pour dire à Kubernetes d'utiliser cette nouvelle version.

Plusieurs éléments nouveaux méritent qu'on s'y attarde. D'abord, la directive
`needs: tests` sur le job `deploy` crée une dépendance explicite : le
déploiement ne s'exécute que si les tests ont réussi. C'est le mécanisme
fondamental qui connecte la CI au CD dans un même workflow. Sans cette directive,
les deux jobs s'exécuteraient en parallèle, ce qui n'aurait aucun sens (on ne
veut pas déployer du code qui n'a pas passé les tests).

Ensuite, la directive `environment: production` active un mécanisme de GitHub
appelé *environments*. Un environment est un contexte de déploiement nommé
(typiquement `staging`, `production`) auquel on peut associer des règles de
protection. Par exemple, on peut exiger qu'un ou plusieurs réviseurs approuvent
le déploiement avant qu'il s'exécute, ce qui transforme notre pipeline en
continuous delivery (avec approbation humaine) plutôt qu'en continuous deployment
(entièrement automatique). On peut aussi restreindre quelles branches ont le
droit de déployer vers un environment donné.

La syntaxe `${{ secrets.REGISTRY_PASSWORD }}` fait référence aux *secrets*
GitHub : des variables chiffrées, configurées dans les paramètres du dépôt, qui
ne sont jamais visibles dans les logs ni dans le code source. C'est le mécanisme
qui permet au pipeline d'accéder à des informations sensibles (mots de passe,
clés d'API, certificats) sans les exposer. Ce principe rejoint directement le
facteur III de la Twelve-Factor App : la configuration sensible doit vivre dans
l'environnement, pas dans le code.

Enfin, `${{ github.sha }}` est le hash du commit qui a déclenché le workflow.
En l'utilisant comme tag de l'image Docker (`flask-app:abc123def...`), on crée
un lien direct et traçable entre un commit précis dans git et l'image qui tourne
en production. Si quelque chose ne va pas après un déploiement, on peut
immédiatement identifier quel commit est en cause. C'est une pratique
fondamentale du CD : chaque artefact déployé doit être traçable jusqu'à son
code source.

## Stratégies de déploiement

Avoir un pipeline automatisé, c'est bien. Mais *comment* le déploiement
lui-même se déroule-t-il ? Quand on met à jour une application qui est en train
de servir des utilisateurs, on ne peut pas simplement arrêter l'ancienne version
et démarrer la nouvelle : pendant la transition, les utilisateurs verraient des
erreurs. Et si la nouvelle version contient un bug, on voudrait pouvoir revenir
en arrière rapidement, sans que tous les utilisateurs aient été affectés.
Plusieurs stratégies existent pour résoudre ce problème, chacune avec ses
compromis.

### Rolling update

La stratégie la plus courante est le *rolling update* (mise à jour progressive).
Le principe est simple : on remplace les instances de l'ancienne version une par
une, plutôt que toutes en même temps. Si on a trois instances de notre
application Flask derrière un load balancer (comme dans notre tutoriel
Kubernetes), un rolling update commencerait par arrêter la première instance,
la remplacer par la nouvelle version, vérifier qu'elle fonctionne, puis passer
à la deuxième, et ainsi de suite. Pendant toute la durée de la mise à jour, les
instances restantes continuent de servir le trafic : il n'y a jamais d'arrêt
complet.

<!-- ILLUSTRATION: schéma d'un rolling update avec 3 instances, montrant le remplacement progressif v1→v2 -->

C'est exactement ce que fait Kubernetes par défaut quand on modifie un
deployment. La commande `kubectl set image` de notre pipeline CI/CD déclenche un
rolling update : Kubernetes crée un nouveau pod avec la nouvelle image, attend
qu'il soit prêt, puis termine un ancien pod, et répète jusqu'à ce que toutes les
instances soient à jour. On peut contrôler la vitesse de cette transition avec
deux paramètres : `maxUnavailable` (combien d'instances peuvent être
indisponibles simultanément) et `maxSurge` (combien d'instances supplémentaires
peuvent être créées temporairement). Le rolling update est la stratégie par
défaut parce qu'elle est simple et ne nécessite pas de ressources
supplémentaires importantes. Sa limite principale est que pendant la transition,
l'ancienne et la nouvelle version coexistent : certains utilisateurs voient la
v1, d'autres la v2. Si les deux versions sont incompatibles (par exemple un
changement dans le format des données), cela peut poser problème.

On peut observer ce mécanisme concrètement en reprenant notre cluster k3d de la
section précédente. Assurons-nous d'abord que notre deployment `web` tourne avec
3 répliques :

```shell
$ kubectl scale deployment web --replicas=3
```

Modifions maintenant notre application Flask pour ajouter un endpoint `/version`
qui identifie la version du code :

```python
from flask import Flask
import redis
import os

app = Flask(__name__)

red = redis.Redis("redis")
KEY = "some_key"
POD_NAME = os.environ.get("HOSTNAME", "unknown")
VERSION = "v2"

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

@app.route("/version")
def version():
    return f"[{POD_NAME}] {VERSION}"
```

La seule différence avec notre version précédente est l'ajout de la constante
`VERSION = "v2"` et de la route `/version`. Reconstruisons l'image et
importons-la dans le cluster :

```shell
$ docker build -t flask-app:v2 .
$ k3d image import flask-app:v2 -c demo
```

Avant de déclencher la mise à jour, ouvrons un second terminal et lançons une
boucle qui interroge `/version` toutes les secondes, ce qui nous permettra
d'observer la transition en temps réel :

```shell
$ while true; do curl -s localhost:8080/version; echo; sleep 1; done
```

Pour l'instant, toutes les réponses sont des erreurs 404, puisque la route
`/version` n'existe pas encore dans la version en cours. Déclenchons maintenant
le rolling update :

```shell
$ kubectl set image deployment/web web=flask-app:v2
```

Dans le terminal où tourne notre boucle, on voit progressivement les réponses
changer :

```
404 Not Found
404 Not Found
[web-6f8b9d4c7-x2k9m] v2
404 Not Found
[web-6f8b9d4c7-x2k9m] v2
[web-6f8b9d4c7-r7j3n] v2
[web-6f8b9d4c7-x2k9m] v2
[web-6f8b9d4c7-r7j3n] v2
[web-6f8b9d4c7-q4w8p] v2
```

On observe la transition : les 404 (ancienne version, qui ne connait pas
`/version`) se mélangent avec les réponses v2 (nouvelle version), puis
finissent par disparaitre complètement. Chaque réponse v2 provient d'un pod
différent (les noms changent), ce qui confirme que le load balancer distribue
le trafic entre les nouvelles instances au fur et à mesure qu'elles deviennent
disponibles. Dans k9s, on peut aussi observer les pods se remplacer un par un :
les anciens passent en état `Terminating` pendant que les nouveaux apparaissent
en `Running`.

### Blue-green deployment

Le *blue-green deployment* est une stratégie qui élimine complètement la période
de coexistence entre les deux versions. Le principe : on maintient deux
environnements de production identiques, appelés par convention "blue" et
"green". À tout moment, un seul des deux environnements reçoit le trafic réel
(disons blue). Pour déployer une nouvelle version, on la déploie sur
l'environnement inactif (green), on la teste, et quand on est satisfait, on
bascule le routeur (ou le load balancer) pour diriger tout le trafic vers green.
La transition est instantanée : il n'y a pas de période où les deux versions
coexistent. Et si un problème survient, le rollback est tout aussi instantané :
on rebascule vers blue, qui est encore intact avec l'ancienne version.

<!-- ILLUSTRATION: schéma blue-green avec un routeur/load balancer qui bascule entre deux environnements -->

L'avantage est la simplicité du modèle mental : à tout instant, 100% des
utilisateurs voient la même version. Le rollback est une simple reconfiguration
du routeur, sans aucune reconstruction ou redéploiement. L'inconvénient
principal est le coût : il faut maintenir deux environnements complets, ce qui
double les ressources nécessaires (au moins temporairement). Dans un
environnement cloud où les ressources sont élastiques, ce coût est plus facile à
absorber que dans un datacenter où les serveurs physiques sont fixes. Le terme
"blue-green" a été popularisé par Martin Fowler et, de manière indépendante, par
le livre *Continuous Delivery* de Humble et Farley.

### Canary deployment

Le *canary deployment* (déploiement canari) est un compromis entre le rolling
update et le blue-green. L'idée est de déployer la nouvelle version sur un
petit sous-ensemble de l'infrastructure (par exemple 5% des instances), puis
d'observer son comportement avant de l'étendre progressivement. Le nom vient
des canaris que les mineurs emportaient dans les mines de charbon : si le canari
mourait, c'était le signe que l'air était toxique, et les mineurs rebroussaient
chemin avant d'être affectés eux-mêmes.

<!-- ILLUSTRATION: schéma canary avec 1 instance v2 parmi 9 instances v1, avec une flèche montrant l'augmentation progressive -->

Concrètement, un canary deployment fonctionne ainsi : on déploie la nouvelle
version sur une ou quelques instances, le load balancer y dirige une fraction du
trafic, et on surveille attentivement les métriques (taux d'erreurs, latence,
utilisation mémoire). Si tout va bien, on augmente progressivement la proportion
de trafic vers la nouvelle version (10%, 25%, 50%, 100%). Si une anomalie est
détectée, on retire les instances canary et tout le trafic retourne vers
l'ancienne version. Le rayon d'impact d'un bug est limité : seuls les
utilisateurs qui ont été routés vers le canary sont affectés.

Le canary est particulièrement utile pour les changements qui sont difficiles à
tester complètement en pré-production. Les tests automatisés et les
environnements de staging peuvent attraper beaucoup de bugs, mais certains
problèmes n'apparaissent qu'avec du vrai trafic, à vraie échelle : des
problèmes de performance sous charge, des cas limites dans les données réelles,
des interactions avec d'autres services en production. Le canary permet
d'exposer la nouvelle version à ces conditions réelles tout en limitant le
risque. Netflix, avec ses centaines de millions d'utilisateurs, a été un
pionnier de cette approche : il serait impensable d'exposer tous les
utilisateurs simultanément à une version non testée en production.

Ces trois stratégies ne sont pas mutuellement exclusives. On peut combiner un
canary avec un blue-green : déployer la nouvelle version dans l'environnement
inactif, y diriger une fraction du trafic pour validation, puis basculer
complètement. Le choix dépend du contexte : le rolling update convient à la
plupart des cas, le blue-green est préférable quand on ne peut pas tolérer la
coexistence de versions, et le canary est indiqué quand le risque d'un
déploiement est élevé et qu'on veut le mitiger progressivement.

## Feature flags

Les stratégies de déploiement que nous venons de voir opèrent au niveau de
l'infrastructure : on contrôle *quelles instances* reçoivent le trafic. Les
*feature flags* (aussi appelés *feature toggles*) abordent le problème sous un
angle différent : on contrôle *quel code s'exécute* à l'intérieur d'une même
version déployée. L'idée est de découpler le déploiement du code et l'activation
d'une fonctionnalité. On peut déployer du code en production sans que les
utilisateurs en voient les effets, puis l'activer (ou le désactiver) à volonté,
sans redéployer.

Dans sa forme la plus simple, un feature flag est un `if` :

```python
ENABLE_NEW_SEARCH = os.environ.get("ENABLE_NEW_SEARCH", "false") == "true"

@app.route("/search")
def search():
    if ENABLE_NEW_SEARCH:
        return new_search_engine(request.args["q"])
    else:
        return old_search_engine(request.args["q"])
```

La fonctionnalité `new_search_engine` est présente dans le code déployé, mais
elle n'est accessible que si la variable d'environnement `ENABLE_NEW_SEARCH` est
définie à `"true"`. On peut déployer ce code en production avec le flag désactivé,
vérifier que rien n'est cassé, puis activer le flag en modifiant la variable
d'environnement, sans aucun redéploiement. C'est un mécanisme puissant : il
permet par exemple de fusionner du code incomplet dans la branche principale
sans affecter les utilisateurs. Les développeurs travaillent sur la nouvelle
fonctionnalité en continu, derrière un flag, et ne l'exposent que quand elle
est prête. Cela évite les branches de longue durée qui divergent et deviennent
difficiles à fusionner, un problème que nous avons abordé dans le module 4.

Facebook a été l'un des pionniers de cette pratique, sous le nom de *dark
launching* : en 2008, l'entreprise déployait régulièrement de nouvelles
fonctionnalités en production, invisibles pour les utilisateurs, afin de tester
leur impact sur les performances du système sous charge réelle. L'idée était de
découvrir les problèmes de scalabilité *avant* que les utilisateurs ne soient
exposés à la fonctionnalité. C'est un complément naturel au canary deployment :
le canary teste une nouvelle version sur un sous-ensemble d'utilisateurs, le
dark launching teste une nouvelle fonctionnalité sur tout le trafic mais sans
que les utilisateurs en voient les résultats.

Au-delà du simple `if` avec une variable d'environnement, des plateformes
spécialisées comme LaunchDarkly, Unleash ou Flagsmith permettent de gérer les
feature flags de manière plus sophistiquée : activation par pourcentage
d'utilisateurs (comme un canary, mais au niveau applicatif), ciblage par
attributs (activer la fonctionnalité seulement pour les utilisateurs d'un
certain pays, ou les membres d'une équipe beta), et désactivation instantanée
(*kill switch*) en cas de problème. Ces outils offrent une interface web qui
permet aux équipes produit, et pas seulement aux développeurs, de contrôler
quelles fonctionnalités sont visibles.

Un mot de prudence : les feature flags ajoutent de la complexité au code. Chaque
flag crée un embranchement logique qu'il faut tester et maintenir. Si on ne
retire pas les flags une fois qu'une fonctionnalité est stabilisée, on accumule
de la dette technique sous forme de conditions mortes et de chemins de code
jamais exécutés. La discipline est importante : un feature flag devrait avoir une
durée de vie limitée et être nettoyé une fois que la fonctionnalité est
définitivement activée (ou abandonnée).

## Immutable infrastructure

Un fil conducteur traverse toutes les pratiques de cette section : l'idée qu'on
ne modifie pas ce qui est en production, on le remplace. Quand Kubernetes fait
un rolling update, il ne met pas à jour le code à l'intérieur d'un pod existant :
il crée un nouveau pod et détruit l'ancien. Quand on fait un blue-green
deployment, on ne modifie pas l'environnement actif : on en prépare un nouveau
et on bascule. Cette philosophie porte un nom : l'*immutable infrastructure*
(infrastructure immuable).

Le principe est simple : une fois qu'un artefact est construit (une image
Docker, une machine virtuelle, un package), il ne doit jamais être modifié. Si
un changement est nécessaire, on construit un nouvel artefact. C'est le même
raisonnement que l'immutabilité en programmation fonctionnelle, que nous avons
rencontrée dans le module 2 : plutôt que de modifier un objet en place (ce qui
rend difficile de savoir dans quel état il se trouve), on en crée un nouveau.
L'état du système est toujours le résultat d'un processus de construction
reproductible, jamais le produit d'une accumulation de modifications manuelles.
C'est l'opposé du *snowflake server* dont nous avons parlé dans la section sur
l'infrastructure as code.

La Twelve-Factor App de Wiggins capture cette idée dans son facteur V :
*build, release, run*. Ces trois phases doivent être strictement séparées. La
phase *build* transforme le code source en un artefact exécutable (compiler,
installer les dépendances, construire l'image Docker). La phase *release*
combine cet artefact avec la configuration spécifique à un environnement
(variables d'environnement, secrets). La phase *run* exécute la release dans
l'environnement cible. L'artefact produit par la phase build est le même qu'il
soit déployé en staging ou en production : seule la configuration change. C'est
exactement ce que fait notre pipeline CI/CD : le job `tests` vérifie le code, le
job `deploy` construit une image Docker (build), la combine avec les secrets de
l'environment GitHub (release), et l'applique au cluster Kubernetes (run).

Un autre facteur pertinent est le facteur X : *dev/prod parity* (parité entre
développement et production). L'idée est de réduire au maximum les écarts entre
l'environnement de développement et la production. Historiquement, ces écarts
étaient considérables : les développeurs travaillaient sur Windows avec une base
SQLite, tandis que la production tournait sur Linux avec PostgreSQL. Les bugs
qui n'apparaissaient qu'en production étaient fréquents et difficiles à
diagnostiquer. Docker et les containers ont considérablement réduit ce
problème : si l'application tourne dans le même container en développement et en
production, l'environnement est par définition le même. Le facteur III
(*config*), que nous avons déjà abordé avec les secrets GitHub et les variables
d'environnement Kubernetes, complète le tableau : la configuration est la seule
chose qui devrait varier entre les environnements. Le code, les dépendances et
le runtime sont identiques.