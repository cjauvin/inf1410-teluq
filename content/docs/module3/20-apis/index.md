---
title: "Les APIs"
slug: "apis"
weight: 20
---

# Les APIs

Le terme API (*Application Programming Interface*) est omniprésent dans le vocabulaire du développement logiciel moderne. Mais ce qu'on entend par "API" aujourd'hui n'est pas ce qu'on entendait il y a trente ans. Le mot a traversé plusieurs incarnations, et chacune reflète un changement profond dans la manière dont on conçoit les systèmes logiciels. Comprendre cette évolution, c'est comprendre comment le génie logiciel est passé du programme monolithique au système distribué.

## L'API comme concept évolutif

À l'origine, le terme API désigne simplement l'ensemble des fonctions, classes et méthodes qu'une bibliothèque expose à ses utilisateurs. Quand on consulte la documentation de la bibliothèque standard Python et qu'on découvre que le module `json` offre les fonctions `dumps()` et `loads()`, on consulte une API. Quand on apprend qu'un objet `list` possède les méthodes `append()`, `sort()` et `pop()`, c'est aussi une API. À ce niveau, l'API est un contrat entre un morceau de code et un autre morceau de code qui l'utilise, à l'intérieur du même programme, du même processus. L'appel est direct, instantané, et s'il échoue, on obtient une exception immédiate. C'est le sens qu'avait le mot dans les années 80 et 90, et c'est encore un sens parfaitement valide.

Le virage se produit quand les systèmes commencent à communiquer entre eux à travers le réseau. L'API n'est plus un contrat entre deux modules dans le même processus, mais entre deux programmes qui s'exécutent sur des machines différentes. Ce changement est plus profond qu'il n'y paraît. Un appel de fonction local prend quelques nanosecondes, ne peut pas échouer "à moitié", et ne nécessite aucune conversion de données. Un appel réseau prend des millisecondes (voire des secondes), peut échouer pour des raisons qui n'ont rien à voir avec la logique du programme (un câble débranché, un serveur surchargé, un timeout), et nécessite de sérialiser les données dans un format que les deux parties comprennent. L'API réseau hérite de toutes les contraintes du réseau, et ces contraintes changent fondamentalement la manière dont on doit concevoir les interactions entre composants.

Plus récemment, un troisième sens du mot API est apparu : l'API comme *produit*. Des entreprises comme Stripe (paiements), Twilio (SMS et téléphonie) ou SendGrid (courriels) ne vendent pas un logiciel qu'on installe, mais un service qu'on consomme à travers une API. Leur documentation n'est pas un détail technique relégué dans un wiki interne : c'est leur vitrine, leur interface principale avec leurs clients. Ces APIs ont du versioning (pour ne pas casser les intégrations existantes), des SLAs (des garanties de disponibilité), des tableaux de bord pour suivre l'utilisation, et même des modèles de tarification basés sur le nombre d'appels. L'API est devenue un produit commercial à part entière, et la qualité de sa conception est un avantage concurrentiel. C'est ce qu'on appelle parfois l'*API economy* : un écosystème où les logiciels se construisent en assemblant des services exposés par d'autres logiciels, chacun accessible par son API.

## Les paradigmes d'APIs réseau

La première réponse au problème de la communication entre systèmes a été de nier le problème. L'idée du *Remote Procedure Call* (RPC), formulée dès les années 1980, est séduisante par sa simplicité : faire en sorte qu'un appel de fonction à travers le réseau ressemble exactement à un appel de fonction local. Le programmeur écrit `getUser(42)`, et le système sous-jacent se charge de sérialiser les arguments, de les envoyer au serveur distant, d'attendre la réponse et de la désérialiser. L'illusion est que le réseau n'existe pas.

Cette idée a donné naissance à plusieurs technologies au fil des décennies. CORBA (Common Object Request Broker Architecture), poussée par un consortium industriel dans les années 1990, promettait de faire communiquer des objets écrits dans n'importe quel langage, sur n'importe quelle machine. XML-RPC (1998) a simplifié l'approche en utilisant XML et HTTP comme transport. SOAP (Simple Object Access Protocol) a pris le relais avec des enveloppes XML encore plus élaborées, des schémas de validation (WSDL) et tout un écosystème d'outils de génération de code. Ces technologies ont été massivement adoptées dans le monde de l'entreprise, notamment dans les architectures dites SOA (*Service-Oriented Architecture*).

Mais l'illusion du RPC transparent a un prix, et ce prix a été magistralement identifié par Peter Deutsch et ses collègues de Sun Microsystems dans un texte devenu célèbre : les *Fallacies of Distributed Computing* (1994). Deutsch liste huit hypothèses que les développeurs font implicitement quand ils conçoivent des systèmes distribués, et qui sont toutes fausses :

1. Le réseau est fiable
2. La latence est nulle
3. La bande passante est infinie
4. Le réseau est sécuritaire
5. La topologie ne change pas
6. Il y a un seul administrateur
7. Le coût du transport est nul
8. Le réseau est homogène

Chacune de ces "erreurs de raisonnement" (*fallacies*) est une source de bugs subtils dans les systèmes distribués. CORBA et SOAP essayaient de cacher ces réalités derrière des couches d'abstraction, mais les problèmes finissaient toujours par remonter à la surface : timeouts inexpliqués, messages perdus, désérialisation qui échoue parce que le serveur a été mis à jour mais pas le client. L'excès de complexité de ces technologies (les fichiers WSDL de SOAP pouvaient faire des centaines de lignes pour décrire un simple service) a fini par provoquer une réaction.

### REST

En 2000, Roy Fielding publie sa thèse de doctorat à l'Université de Californie à Irvine. Fielding n'est pas un inconnu : il est l'un des auteurs principaux de la spécification HTTP/1.1 et un co-fondateur du serveur web Apache. Dans sa thèse, il propose un style architectural pour les systèmes distribués qu'il appelle REST (*Representational State Transfer*). L'idée centrale est une rupture avec la philosophie RPC. Au lieu de concevoir des APIs comme des collections de fonctions qu'on appelle à distance (`getUser`, `createOrder`, `deleteProduct`), REST propose de concevoir des APIs comme des collections de *ressources* qu'on manipule avec un vocabulaire uniforme. Une ressource, c'est n'importe quoi qui peut être nommé : un utilisateur, une commande, un produit, un article de blog. Chaque ressource est identifiée par une URL, et on interagit avec elle en utilisant les verbes standard du protocole HTTP.

Ce qui rend REST particulier, c'est que Fielding n'a presque rien inventé. Les verbes HTTP (`GET`, `POST`, `PUT`, `DELETE`) et les codes de statut (`200 OK`, `404 Not Found`, `500 Internal Server Error`) existaient déjà dans la spécification HTTP/1.1, que Fielding avait lui-même co-écrite. Mais personne ne les utilisait comme prévu. SOAP, par exemple, envoyait toutes ses requêtes par `POST`, retournait toujours un code `200`, et enfouissait toute la sémantique dans des enveloppes XML. HTTP était traité comme un simple tuyau de transport, un câble réseau glorifié. La contribution de Fielding a été de rappeler que HTTP est un protocole *applicatif*, conçu dès le départ avec un vocabulaire riche pour manipuler des ressources. REST n'ajoute pas une couche par-dessus HTTP : il dit simplement d'utiliser HTTP comme il a été conçu.

En pratique, cela signifie qu'une API REST utilise les verbes HTTP pour exprimer l'intention de chaque requête :

| Verbe | Signification | Exemple |
|-------|--------------|---------|
| `GET` | Lire une ressource | `GET /users/42` |
| `POST` | Créer une nouvelle ressource | `POST /users` |
| `PUT` | Remplacer une ressource | `PUT /users/42` |
| `PATCH` | Modifier partiellement une ressource | `PATCH /users/42` |
| `DELETE` | Supprimer une ressource | `DELETE /users/42` |

Et les réponses utilisent les codes de statut pour signaler le résultat : `200 OK` pour une requête réussie, `201 Created` pour une création, `404 Not Found` si la ressource n'existe pas, `400 Bad Request` si la requête est mal formée, `500 Internal Server Error` si le serveur a un problème. Ce vocabulaire partagé entre tous les services du monde est l'un des atouts majeurs de REST : un développeur qui connaît HTTP sait déjà comment interagir avec n'importe quelle API REST, sans avoir besoin de lire un schéma WSDL ou de générer du code client.

On peut tester une API REST directement depuis la ligne de commande avec `curl` :

```shell
# Lire un utilisateur
$ curl https://api.example.com/users/42
{"id": 42, "name": "Alice", "email": "alice@example.com"}

# Créer un utilisateur
$ curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob", "email": "bob@example.com"}'
{"id": 43, "name": "Bob", "email": "bob@example.com"}

# Supprimer un utilisateur
$ curl -X DELETE https://api.example.com/users/43
```

La simplicité de ces interactions est frappante comparée aux enveloppes XML de SOAP. C'est cette simplicité, combinée à l'omniprésence de HTTP, qui a fait le succès de REST dans les années 2000 et 2010.

Mais toutes les APIs qui se disent "REST" ne le sont pas au même degré. Leonard Richardson a proposé un modèle de maturité qui classe les APIs en quatre niveaux, du moins au plus fidèle à la vision de Fielding :

- **Niveau 0** : un seul endpoint, tout passe par POST. C'est essentiellement du RPC avec du JSON au lieu du XML. Exemple : `POST /api` avec un corps `{"action": "getUser", "id": 42}`.
- **Niveau 1** : des ressources distinctes (des URLs différentes pour chaque entité), mais un seul verbe. On a `POST /users/42` au lieu de `POST /api`, mais on n'utilise pas `GET`, `PUT` ou `DELETE`.
- **Niveau 2** : des ressources *et* des verbes HTTP. C'est le niveau où se situent la grande majorité des APIs dites "REST" dans l'industrie. On fait `GET /users/42` pour lire, `POST /users` pour créer, `DELETE /users/42` pour supprimer, et on utilise les codes de statut correctement.
- **Niveau 3** : HATEOAS (*Hypermedia As The Engine Of Application State*). Les réponses contiennent des liens vers les actions possibles, comme une page web contient des liens vers d'autres pages. Par exemple :

```json
{
  "id": 42,
  "name": "Alice",
  "email": "alice@example.com",
  "links": [
    {"rel": "self", "href": "/users/42"},
    {"rel": "orders", "href": "/users/42/orders"},
    {"rel": "delete", "href": "/users/42", "method": "DELETE"}
  ]
}
```

Le niveau 3 est la vision originale de Fielding : une API qui se comporte comme le web lui-même, où chaque réponse contient les liens nécessaires pour naviguer vers les actions suivantes. Fielding a d'ailleurs publié un billet de blog assez cinglant en 2008, intitulé *REST APIs must be hypertext-driven*, dans lequel il se plaignait que la plupart des APIs qui se disaient "REST" n'implémentaient pas HATEOAS et ne méritaient donc pas cette appellation. En pratique, le niveau 3 reste rare. La plupart des développeurs jugent que le niveau 2 est suffisant pour leurs besoins, et que la complexité supplémentaire de HATEOAS ne se justifie pas. C'est un cas où YAGNI l'emporte sur la pureté théorique.

Pour rendre ces concepts concrets, voici une API REST complète implémentée avec FastAPI, un framework Python moderne. L'exemple gère une collection de livres :

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    year: int

# Base de données en mémoire (un simple dictionnaire)
books = {
    1: Book(title="The Mythical Man-Month", author="Fred Brooks", year=1975),
    2: Book(title="The Pragmatic Programmer", author="Hunt & Thomas", year=1999),
}
next_id = 3

@app.get("/books")
def list_books():
    return {id: book for id, book in books.items()}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return books[book_id]

@app.post("/books", status_code=201)
def create_book(book: Book):
    global next_id
    books[next_id] = book
    next_id += 1
    return {"id": next_id - 1, **book.model_dump()}

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    del books[book_id]
```

Pour lancer ce serveur, on peut utiliser `uv` pour installer les dépendances et exécuter le tout sans configuration préalable :

```shell
# Installer les dépendances et lancer le serveur en une seule commande
$ uv run --with fastapi --with uvicorn uvicorn main:app
INFO:     Uvicorn running on http://127.0.0.1:8000
```

L'option `--with` de `uv run` installe les paquets nécessaires dans un environnement temporaire, sans polluer le système. Une fois le serveur lancé, on peut interagir avec depuis un autre terminal :

```shell
# Lister tous les livres
$ curl http://localhost:8000/books
{"1":{"title":"The Mythical Man-Month","author":"Fred Brooks","year":1975}, ...}

# Lire un livre spécifique
$ curl http://localhost:8000/books/1
{"title":"The Mythical Man-Month","author":"Fred Brooks","year":1975}

# Créer un nouveau livre
$ curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert Martin", "year": 2008}'
{"id":3,"title":"Clean Code","author":"Robert Martin","year":2008}

# Tenter de lire un livre qui n'existe pas
$ curl -i http://localhost:8000/books/99
HTTP/1.1 404 Not Found
{"detail":"Livre introuvable"}

# Supprimer un livre
$ curl -X DELETE http://localhost:8000/books/2
```

Quelques points méritent d'être soulignés. D'abord, FastAPI utilise les type hints de Python (et le modèle Pydantic `Book`) pour valider automatiquement les données entrantes : si on envoie un JSON sans le champ `year`, le serveur retourne un `422 Unprocessable Entity` sans qu'on ait écrit une seule ligne de validation. C'est un lien direct avec la notion de schéma qu'on a vue dans la section sur les données. Ensuite, chaque endpoint correspond à une combinaison verbe + ressource, exactement comme le prescrit REST au niveau 2 du modèle de Richardson. Enfin, FastAPI génère automatiquement une documentation interactive (accessible à `http://localhost:8000/docs`) qui décrit tous les endpoints, leurs paramètres et leurs réponses possibles. On reviendra sur cette documentation générée quand on parlera d'OpenAPI dans la section sur le design d'API.

### GraphQL

En 2015, Facebook rend public GraphQL, un langage de requêtes pour APIs qu'ils utilisaient en interne depuis 2012. GraphQL est né d'un problème concret : l'application mobile de Facebook devait afficher des données provenant de dizaines de sources différentes (profil utilisateur, fil d'actualité, amis, photos, notifications), et les APIs REST existantes n'étaient pas adaptées. Le problème tient en deux mots : *over-fetching* et *under-fetching*.

Prenons un exemple. On construit une page qui affiche le nom d'un auteur et les titres de ses livres. Avec une API REST classique, on a deux options. Soit on fait `GET /authors/1` et on reçoit *toutes* les informations de l'auteur (biographie, date de naissance, photo, adresse, etc.) alors qu'on n'a besoin que du nom : c'est l'over-fetching, on reçoit trop de données. Soit l'endpoint `/authors/1` ne contient pas la liste des livres, et il faut faire un deuxième appel `GET /authors/1/books` : c'est l'under-fetching, on ne reçoit pas assez de données en un seul appel. Sur un téléphone mobile avec une connexion lente, chaque requête supplémentaire coûte cher.

GraphQL résout ce problème en laissant le *client* décider de la forme exacte des données qu'il veut recevoir. Au lieu d'appeler des endpoints différents, on envoie une requête qui décrit précisément les champs souhaités :

```graphql
{
  author(id: 1) {
    name
    books {
      title
      year
    }
  }
}
```

Et le serveur répond avec exactement cette structure, rien de plus :

```json
{
  "data": {
    "author": {
      "name": "Fred Brooks",
      "books": [
        {"title": "The Mythical Man-Month", "year": 1975}
      ]
    }
  }
}
```

Un seul appel, exactement les données nécessaires. Si une autre page a besoin de l'adresse de l'auteur en plus, elle modifie sa requête sans que le serveur ait besoin de changer. Cette flexibilité a un coût : le serveur GraphQL est plus complexe à implémenter qu'un serveur REST, et il est plus difficile de mettre en cache les réponses (puisque chaque requête peut être différente). Mais pour les applications avec des besoins de données complexes et variés, le compromis en vaut la peine.

Le nom "GraphQL" et sa syntaxe déclarative peuvent évoquer SQL, et la comparaison est instructive. En SQL, le code serveur envoie une requête directement à la base de données : `SELECT name FROM authors WHERE id = 1`. La base de données fouille ses tables et retourne le résultat. En GraphQL, c'est le client (le navigateur, l'application mobile) qui envoie une requête au serveur, décrivant la *forme* souhaitée de la réponse. Mais le serveur est libre de satisfaire cette requête comme il veut : en exécutant du SQL, en appelant un autre service, en lisant un cache, ou les trois à la fois. SQL est un langage de requêtes sur les *données*, GraphQL est un langage de requêtes sur l'*API*. Les deux opèrent à des niveaux différents de l'architecture, et GraphQL n'expose jamais la base de données directement au client.

GraphQL offre aussi quelque chose que HATEOAS promettait mais que REST en pratique n'a jamais vraiment livré : la découvrabilité. Le schéma GraphQL est *introspectable* : on peut interroger le serveur pour lui demander quels types de données il expose, quels champs chaque type possède, et quelles requêtes sont possibles. Des outils comme GraphiQL exploitent cette propriété pour offrir un explorateur interactif avec autocomplétion, ce qui facilite considérablement le travail des développeurs qui consomment l'API.

Pour rendre ces concepts concrets, voici un serveur GraphQL complet implémenté avec Strawberry, un framework GraphQL pour Python qui s'intègre naturellement avec FastAPI. On réutilise le même domaine des livres que dans l'exemple REST, ce qui permet de comparer directement les deux approches :

```python
# graphql_main.py
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Book:
    title: str
    author: str
    year: int

@strawberry.type
class Author:
    name: str
    books: list[Book]

# Données en mémoire
authors_db = {
    1: Author(
        name="Fred Brooks",
        books=[Book(title="The Mythical Man-Month", author="Fred Brooks", year=1975)],
    ),
    2: Author(
        name="Hunt & Thomas",
        books=[Book(title="The Pragmatic Programmer", author="Hunt & Thomas", year=1999)],
    ),
}

@strawberry.type
class Query:
    @strawberry.field
    def author(self, id: int) -> Author | None:
        return authors_db.get(id)

    @strawberry.field
    def books(self) -> list[Book]:
        return [book for author in authors_db.values() for book in author.books]

schema = strawberry.Schema(query=Query)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
```

```shell
# Lancer le serveur
$ uv run --with 'strawberry-graphql[fastapi]' --with uvicorn uvicorn graphql_main:app
INFO:     Uvicorn running on http://127.0.0.1:8000
```

On peut maintenant envoyer des requêtes GraphQL avec `curl`. La différence avec REST saute aux yeux : au lieu de choisir un endpoint et un verbe HTTP, on envoie une requête qui décrit la forme exacte des données souhaitées :

```shell
# Demander seulement le nom d'un auteur
$ curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ author(id: 1) { name } }"}'
{"data": {"author": {"name": "Fred Brooks"}}}

# Demander le nom ET les livres (avec seulement le titre)
$ curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ author(id: 1) { name books { title } } }"}'
{"data": {"author": {"name": "Fred Brooks", "books": [{"title": "The Mythical Man-Month"}]}}}

# Demander tout : nom, livres avec titre et année
$ curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ author(id: 1) { name books { title year } } }"}'
{"data": {"author": {"name": "Fred Brooks", "books": [{"title": "The Mythical Man-Month", "year": 1975}]}}}
```

Les trois requêtes vont au même endpoint (`/graphql`), mais chacune retourne une structure de données différente, dictée par le client. Avec REST, il aurait fallu soit trois endpoints différents, soit un seul endpoint qui retourne tout et laisse le client ignorer ce dont il n'a pas besoin. Strawberry génère aussi une interface interactive (accessible à `http://localhost:8000/graphql`) qui exploite l'introspection du schéma pour offrir autocomplétion et documentation, exactement comme GraphiQL.

### gRPC

En 2015, Google rend public gRPC, un framework RPC open source. Le nom peut surprendre : après avoir longuement expliqué pourquoi le RPC transparent était une illusion dangereuse, pourquoi y revenir ? Parce que gRPC n'est pas un retour naïf au passé. C'est un RPC qui a intégré les leçons des *fallacies* de Deutsch. Là où CORBA et SOAP essayaient de cacher le réseau, gRPC l'assume explicitement : les appels sont asynchrones par défaut, les timeouts et les codes d'erreur réseau font partie intégrante de l'API, et le développeur est encouragé à gérer les cas de panne dès la conception.

La différence la plus visible avec REST et GraphQL est le format de sérialisation. Là où ces derniers utilisent JSON (un format texte, lisible par un humain), gRPC utilise Protocol Buffers (Protobuf), un format binaire développé par Google. Les données sont plus compactes, la sérialisation et la désérialisation sont plus rapides, mais le contenu n'est pas lisible sans outil de décodage. Le contrat entre client et serveur est défini dans un fichier `.proto` :

```protobuf
// books.proto
syntax = "proto3";

service BookService {
  rpc GetBook (GetBookRequest) returns (Book);
  rpc ListBooks (Empty) returns (BookList);
}

message GetBookRequest {
  int32 id = 1;
}

message Book {
  int32 id = 1;
  string title = 2;
  string author = 3;
  int32 year = 4;
}

message BookList {
  repeated Book books = 1;
}

message Empty {}
```

À partir de ce fichier, des outils de génération de code produisent automatiquement les classes client et serveur dans le langage de son choix (Python, Go, Java, C++, etc.). Le fichier `.proto` devient la source unique de vérité pour le contrat d'API, un lien direct avec le principe DRY : au lieu de maintenir séparément une documentation, un schéma de validation et du code de sérialisation, tout découle d'un seul fichier.

L'autre innovation majeure de gRPC est son utilisation de HTTP/2 comme protocole de transport. HTTP/2 supporte le multiplexage (plusieurs requêtes simultanées sur une seule connexion) et le streaming bidirectionnel, ce qui permet des patterns impossibles avec REST : un client peut envoyer un flux continu de données au serveur, le serveur peut pousser des résultats au client au fur et à mesure, ou les deux peuvent communiquer simultanément. Ces capacités font de gRPC un choix naturel pour la communication entre microservices, où la performance et l'efficacité du protocole comptent plus que la lisibilité humaine des messages.

En pratique, gRPC occupe une niche différente de REST et GraphQL. REST domine les APIs publiques, celles qu'on expose à des développeurs externes, parce que sa simplicité et son utilisation de HTTP/JSON le rendent universellement accessible. GraphQL excelle pour les applications avec des besoins de données complexes et variés, typiquement les applications mobiles avec de multiples vues. gRPC est le choix privilégié pour la communication interne entre services, là où la performance prime et où les deux parties du contrat sont contrôlées par la même organisation.

### Webhooks

Tous les paradigmes qu'on a vus jusqu'ici partagent un même modèle d'interaction : le client envoie une requête, le serveur répond. C'est le modèle *pull* : le client tire l'information quand il en a besoin. Mais certains cas d'usage ne s'y prêtent pas. Comment savoir qu'un paiement Stripe a été confirmé ? Qu'un dépôt GitHub a reçu un nouveau commit ? Qu'un message Slack a été posté dans un canal ? On pourrait interroger le serveur toutes les 30 secondes (c'est le *polling*), mais c'est inefficace : la grande majorité des requêtes retourneront "rien de nouveau", gaspillant de la bande passante et de la puissance de calcul des deux côtés.

Les webhooks inversent le modèle. Au lieu que le client interroge le serveur, c'est le serveur qui appelle le client quand quelque chose se passe. Le mécanisme est simple : on enregistre une URL auprès du service (par exemple dans le tableau de bord de Stripe), et quand un événement survient (un paiement réussi, un remboursement, une tentative échouée), le service envoie une requête HTTP POST à cette URL avec les détails de l'événement. Le client devient un serveur, temporairement, le temps de recevoir la notification.

```python
# webhook_receiver.py
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhooks/stripe")
async def handle_stripe_webhook(request: Request):
    event = await request.json()

    if event["type"] == "payment_intent.succeeded":
        payment = event["data"]["object"]
        print(f"Paiement reçu : {payment['amount'] / 100:.2f} $")
        # Mettre à jour la commande dans la base de données...

    elif event["type"] == "payment_intent.payment_failed":
        print("Paiement échoué")
        # Notifier le client, réessayer...

    return {"status": "ok"}
```

Les webhooks sont un cas concret d'architecture événementielle (*event-driven*), un concept qu'on a vu dans la section sur les patterns architecturaux. La différence est que les webhooks utilisent HTTP comme mécanisme de livraison, ce qui les rend simples à implémenter mais fragiles : si le serveur qui reçoit le webhook est temporairement indisponible, l'événement peut être perdu. Les systèmes de messaging plus robustes (comme Kafka ou RabbitMQ, qu'on a aussi mentionnés dans la section sur l'architecture) offrent des garanties de livraison que les webhooks seuls ne peuvent pas fournir. Mais pour la majorité des intégrations entre services, la simplicité des webhooks est un compromis acceptable.

## Design d'API et schémas

Quel que soit le paradigme choisi (REST, GraphQL, gRPC), concevoir une API, c'est concevoir un contrat. Et comme tout contrat, la qualité de sa rédaction détermine la qualité de la relation entre les parties. Quelques principes de design reviennent constamment dans la littérature et la pratique.

Le **nommage** est le premier enjeu. En REST, les URLs doivent refléter des ressources (des noms), pas des actions (des verbes) : `/users/42/orders` plutôt que `/getUserOrders?id=42`. Les noms sont au pluriel par convention (`/books`, pas `/book`). En GraphQL, les noms de champs suivent le camelCase et décrivent ce qu'ils retournent. En gRPC, les noms de services et de méthodes suivent le PascalCase. Ces conventions semblent anecdotiques, mais elles réduisent la charge cognitive pour les développeurs qui consomment l'API : quand le nommage est prévisible, on devine la structure avant même de lire la documentation.

Le **versioning** est crucial dès qu'une API a des utilisateurs externes. Changer la structure d'une réponse ou supprimer un champ peut casser des centaines d'applications qui en dépendent. La stratégie la plus courante en REST est d'inclure la version dans l'URL (`/v1/users`, `/v2/users`). GraphQL adopte une approche différente : on ajoute de nouveaux champs sans supprimer les anciens, et on marque les champs obsolètes avec `@deprecated`. gRPC gère le versioning au niveau du fichier `.proto`, où les numéros de champs permettent d'ajouter des données sans casser la compatibilité arrière (un concept qu'on a vu dans la section sur l'évolution des schémas).

La **gestion des erreurs** est un domaine où les mauvaises APIs se distinguent immédiatement des bonnes. Une API qui retourne `500 Internal Server Error` avec un corps vide quand l'utilisateur oublie un champ obligatoire est inutilisable. Une bonne API REST utilise les codes de statut appropriés (`400` pour une requête invalide, `401` pour un accès non autorisé, `404` pour une ressource inexistante, `422` pour des données qui ne respectent pas le schéma) et accompagne chaque erreur d'un message qui explique le problème et, idéalement, comment le corriger.

L'**idempotence** est une propriété subtile mais fondamentale dans le contexte des APIs réseau. Une opération est idempotente si on peut l'exécuter plusieurs fois de suite et obtenir le même résultat qu'en l'exécutant une seule fois. `GET /users/42` est idempotent : lire un utilisateur dix fois donne le même résultat. `DELETE /users/42` est aussi idempotent : la première suppression fonctionne, les suivantes retournent `404`, mais l'état du système est le même. `POST /users`, en revanche, n'est pas idempotent : chaque appel crée un nouvel utilisateur. Pourquoi est-ce important ? Parce que le réseau est peu fiable (les *fallacies* de Deutsch, encore). Si une requête `POST` est envoyée mais que la réponse se perd dans un timeout, le client ne sait pas si la création a réussi ou non. Renvoyer la même requête risque de créer un doublon. Les APIs bien conçues offrent des mécanismes d'idempotence pour les opérations non idempotentes, typiquement en demandant au client de fournir une clé unique (*idempotency key*) avec chaque requête.

Ces principes de design s'incarnent concrètement dans les **schémas**, qui formalisent le contrat d'une API de manière lisible par les machines autant que par les humains. Chaque paradigme a son propre format de schéma, mais l'idée fondamentale est la même : une description formelle de ce que l'API accepte et de ce qu'elle retourne.

Pour REST, le standard dominant est OpenAPI (anciennement connu sous le nom de Swagger). Un fichier OpenAPI décrit chaque endpoint, ses paramètres, ses corps de requête et de réponse, ses codes d'erreur possibles, le tout dans un format YAML ou JSON. Mais OpenAPI va au-delà de la simple documentation statique : des outils comme Swagger UI (celui que FastAPI intègre automatiquement à `/docs`) génèrent une interface interactive où le développeur peut non seulement lire la documentation, mais aussi envoyer des requêtes directement depuis le navigateur, avec des formulaires pré-remplis pour les paramètres et une visualisation immédiate des réponses. On a vu que FastAPI génère cette spécification automatiquement à partir du code Python et des modèles Pydantic, sans qu'on ait besoin d'écrire ou de maintenir un fichier OpenAPI séparé. C'est un exemple parfait du principe DRY appliqué au design d'API : le schéma est dérivé du code, pas maintenu séparément.

Pour gRPC, le fichier `.proto` joue exactement le même rôle : il décrit les services, les méthodes et les structures de données, et le code client et serveur est généré à partir de ce fichier. Pour GraphQL, le schéma est intrinsèque au framework : il est défini par les types et les *resolvers* du serveur, et il est interrogeable par introspection.

Ce qui relie ces trois approches, c'est l'idée que le schéma est la **source unique de vérité** du contrat d'API. Au lieu de maintenir séparément une documentation (qui finit par diverger du code), un schéma de validation (qui finit par être incomplet), et du code de sérialisation (qui finit par avoir des cas particuliers non documentés), tout découle d'une seule source. C'est le principe DRY poussé à son expression la plus naturelle dans le contexte des APIs. Et c'est exactement la même logique qu'on a vue dans la section sur les données, quand on a parlé de la notion de schéma comme pont entre les types en programmation, les schémas de bases de données, et les formats de sérialisation. L'API est un point de jonction où toutes ces dimensions se rencontrent.

## Le pattern Backend For Frontend (BFF)

La discussion sur GraphQL a révélé un problème fondamental : différents clients ont des besoins différents. L'application mobile de Facebook avait besoin de données compactes et ciblées, tandis que l'application web pouvait se permettre des réponses plus riches. GraphQL résout ce problème en laissant chaque client décrire ses propres besoins. Mais il existe une autre approche, complémentaire : au lieu d'avoir une seule API générique que tous les clients consomment, on crée un backend *dédié* à chaque type de client. C'est le pattern **Backend For Frontend** (BFF), formalisé par Sam Newman en 2015 dans le contexte de son travail sur les microservices.

L'idée est simple. Plutôt qu'un seul serveur API qui tente de satisfaire à la fois l'application web, l'application mobile et peut-être une application desktop, on intercale une couche intermédiaire : un petit serveur backend spécifique à chaque type de client. Ce serveur BFF connaît les besoins exacts de "son" client. Le BFF de l'application mobile sait que l'écran d'accueil a besoin du nom de l'utilisateur, de ses trois dernières commandes et de son solde, et il agrège ces données en un seul appel optimisé. Le BFF de l'application web sait que la page de tableau de bord affiche des graphiques détaillés et peut se permettre des réponses plus volumineuses. Chaque BFF appelle les mêmes services en aval (le service utilisateurs, le service commandes, le service facturation), mais il façonne les réponses selon les contraintes de son client.

<!-- ILLUSTRATION: Diagramme montrant deux clients (mobile, web) connectés chacun à leur propre BFF, qui eux-mêmes appellent les mêmes microservices en aval -->

Ce pattern prend tout son sens quand on le met en relation avec la tension fondamentale qu'on a explorée dans la section sur les interfaces utilisateur : la fragmentation des plateformes. On a vu que le monde des interfaces est traversé par un conflit permanent entre l'idéal du "write once, run everywhere" et la réalité des contraintes spécifiques à chaque plateforme. Le BFF est la manifestation côté backend de cette même tension. Si on a un seul backend générique, on finit par y accumuler de la logique conditionnelle : "si le client est mobile, retourner une version compacte ; si c'est le web, inclure les détails supplémentaires". Cette logique devient vite ingérable. Le BFF reconnaît que la fragmentation des clients est un fait, et au lieu de la combattre dans un seul serveur, il l'embrasse en créant une couche d'adaptation dédiée.

Comme tout pattern, le BFF a un coût. Chaque backend supplémentaire est un service à maintenir, à déployer, à surveiller. Pour une application qui n'a qu'un seul type de client, ou dont les besoins de données sont relativement uniformes, le BFF est un cas classique de YAGNI : une complexité architecturale qui ne se justifie pas. GraphQL offre d'ailleurs une alternative élégante au même problème, puisqu'il permet à chaque client de formuler ses propres requêtes sans multiplier les backends. En pratique, les deux approches ne sont pas mutuellement exclusives : certaines architectures utilisent GraphQL *à l'intérieur* d'un BFF, combinant la flexibilité des requêtes côté client avec l'isolation des préoccupations côté serveur. Le choix dépend, comme souvent, de la complexité du système et du nombre de clients différents qu'il doit servir.