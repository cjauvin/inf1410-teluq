---
title: "Architecture et modularité"
weight: 10
---

# Architecture et modularité

Quand un programme est petit, sa structure importe peu. On peut tout mettre dans
un seul fichier, avec quelques fonctions, et ça fonctionne. Mais dès que le
programme grossit, cette approche atteint ses limites. Un fichier de 5000 lignes
devient difficile à naviguer. Deux développeurs qui modifient le même fichier se
marchent sur les pieds. Un changement dans une partie du code casse quelque
chose dans une autre. Le programme est devenu un système, mais sa structure ne
le reflète pas encore. La question n'est alors pas *s'il faut* découper le
système en parties, mais *comment* le découper. Et cette question est bien plus
subtile qu'elle n'y paraît.

## Parnas et l'information hiding (1972)

En 1972, l'informaticien américain David Parnas publie un court article qui va
devenir l'un des plus influents de l'histoire du génie logiciel : *On the
Criteria To Be Used in Decomposing Systems into Modules*. Le titre est direct :
quels critères devrait-on utiliser pour découper un système en modules ? Pour
répondre, Parnas prend un exemple concret, un programme appelé KWIC (Key Word In
Context). Le principe de KWIC est simple : on lui donne une liste de titres, et
il produit un index de tous les mots-clés significatifs, chacun présenté dans
son contexte original. Par exemple, à partir du titre "The Pragmatic
Programmer", KWIC produirait les entrées "Pragmatic Programmer, The" et
"Programmer, The Pragmatic" (en ignorant les mots non significatifs comme
"The"). C'est un système qui était couramment utilisé pour indexer des articles
scientifiques.

L'idée vient du monde de la documentation scientifique. Dans les années 50 et
60, avant les moteurs de recherche, les bibliothécaires et les chercheurs
avaient besoin de trouver rapidement des articles par mots-clés. Un index KWIC
prend une liste de titres et produit une entrée pour chaque mot significatif du
titre, en le présentant dans son contexte original. Par exemple, à partir de ces
trois titres :

```
The Pragmatic Programmer
Clean Code
No Silver Bullet
```

Un index KWIC produirait (en ignorant les mots non significatifs comme "The",
"No") :

```
Silver Bullet              ← entrée pour "Bullet"
Clean Code                 ← entrée pour "Clean"
Code                       ← entrée pour "Code" (rotation de "Clean Code")
Pragmatic Programmer       ← entrée pour "Pragmatic"
Programmer The Pragmatic   ← entrée pour "Programmer"
Silver Bullet No           ← entrée pour "Silver"
```

Chaque titre est "tourné" (rotated) de manière à ce que le mot-clé apparaisse
en premier, et les entrées sont triées alphabétiquement. Le résultat est un
index compact qui permet de retrouver un titre à partir de n'importe lequel de
ses mots significatifs.

{{< hint info >}}
**L'utilitaire `ptx`**

L'idée de l'index KWIC a été suffisamment importante pour qu'un utilitaire Unix
lui soit dédié : `ptx` (permuted index), qui fait partie des GNU coreutils.
On peut l'essayer directement sur la ligne de commande :

```shell
$ echo -e "The Pragmatic Programmer\nClean Code\nNo Silver Bullet" | ptx -S '\n' -w 72
                           No Silver   Bullet
                                       Clean Code
                               Clean   Code
                                       No Silver Bullet
                                 The   Pragmatic Programmer
                       The Pragmatic   Programmer
                                  No   Silver Bullet
                                       The Pragmatic Programmer
```

Chaque ligne est formatée de manière à ce que le mot-clé apparaisse aligné au
début de la colonne de droite, avec son contexte à gauche. C'est un petit
vestige d'une époque où l'indexation automatique des textes était une
préoccupation centrale de l'informatique.
{{< /hint >}}

### Décomposition 1 : par flux de traitement

Parnas compare deux manières de découper ce même système KWIC en modules. La
première, qu'on pourrait qualifier de "naïve", suit le flux de traitement des
données : un module pour lire l'entrée, un module pour produire les rotations,
un module pour trier, un module pour afficher. C'est la décomposition la plus
intuitive, celle qu'on ferait naturellement si on pensait le programme comme une
séquence d'étapes. Voici à quoi elle ressemblerait en Python :

```python
# Décomposition 1 : par flux de traitement
# Chaque module correspond à une étape du pipeline

# Les données partagées entre les modules
lines = []
rotations = []
sorted_rotations = []

STOP_WORDS = {"the", "a", "an", "of", "in", "to", "and", "is", "for"}

def read_input(titles):
    """Étape 1 : lire les titres"""
    lines.clear()
    lines.extend(titles)

def make_rotations():
    """Étape 2 : produire toutes les rotations de chaque titre"""
    rotations.clear()
    for line in lines:
        words = line.split()
        for i, word in enumerate(words):
            if word.lower() not in STOP_WORDS:
                rotated = words[i:] + words[:i]
                rotations.append(" ".join(rotated))

def sort_rotations():
    """Étape 3 : trier les rotations alphabétiquement"""
    sorted_rotations.clear()
    sorted_rotations.extend(sorted(rotations, key=str.lower))

def display_output():
    """Étape 4 : afficher le résultat"""
    for rotation in sorted_rotations:
        print(rotation)

# Utilisation
read_input(["The Pragmatic Programmer", "Clean Code", "No Silver Bullet"])
make_rotations()
sort_rotations()
display_output()
```

Le problème de cette décomposition est que tous les modules partagent les mêmes
données globales (`lines`, `rotations`, `sorted_rotations`). Si on décide de
changer la manière dont les lignes sont stockées, par exemple en passant d'une
liste à un fichier, il faut modifier *tous* les modules. Le découpage par flux
de traitement crée un couplage fort autour de la représentation interne des
données.

### Décomposition 2 : par information hiding (Parnas)

Parnas propose une autre décomposition, fondée sur un principe différent :
chaque module doit cacher une *décision de conception* susceptible de changer.
Au lieu de découper par étapes de traitement, on découpe par *responsabilité*.
Le module de stockage des lignes ne sait rien du tri ; le module de rotation ne
sait rien de la manière dont les lignes sont stockées. Chaque module expose une
interface simple et cache ses détails internes. Parnas appelle ce principe
l'*information hiding* (masquage de l'information).

```python
# Décomposition 2 : par information hiding (Parnas)
# Chaque module cache une décision de conception

class LineStorage:
    """Cache la décision : comment les lignes sont stockées en mémoire."""
    def __init__(self):
        self._lines = []

    def add(self, line):
        self._lines.append(line)

    def get(self, index):
        return self._lines[index]

    def count(self):
        return len(self._lines)


class Rotator:
    """Cache la décision : comment les rotations sont calculées."""
    STOP_WORDS = {"the", "a", "an", "of", "in", "to", "and", "is", "for"}

    def rotations(self, line):
        words = line.split()
        result = []
        for i, word in enumerate(words):
            if word.lower() not in self.STOP_WORDS:
                result.append(words[i:] + words[:i])
        return result


class Sorter:
    """Cache la décision : comment le tri est effectué."""
    def sort(self, items):
        return sorted(items, key=lambda words: [w.lower() for w in words])


class KWICSystem:
    """Assemble les modules sans connaître leurs détails internes."""
    def __init__(self):
        self.storage = LineStorage()
        self.rotator = Rotator()
        self.sorter = Sorter()

    def process(self, titles):
        for title in titles:
            self.storage.add(title)

        all_rotations = []
        for i in range(self.storage.count()):
            line = self.storage.get(i)
            all_rotations.extend(self.rotator.rotations(line))

        for words in self.sorter.sort(all_rotations):
            print(" ".join(words))


kwic = KWICSystem()
kwic.process(["The Pragmatic Programmer", "Clean Code", "No Silver Bullet"])
```

La différence est subtile mais profonde. Si on décide demain de stocker les
lignes dans un fichier plutôt qu'en mémoire, il suffit de modifier
`LineStorage`. Si on change l'algorithme de tri, seul `Sorter` est touché. Si on
veut ajouter des règles de filtrage des stop words, seul `Rotator` est concerné.
Chaque changement est *local* à un module. C'est exactement ce que Parnas
voulait démontrer : le bon critère de décomposition n'est pas "quelle étape du
traitement", mais "quelle décision pourrait changer".

## Couplage et cohésion

L'exemple KWIC illustre un phénomène que les informaticiens Larry Constantine et
Edward Yourdon ont formalisé dans les années 1970 : la qualité d'un découpage se
mesure selon deux axes complémentaires. Le *couplage* mesure le degré de
dépendance entre les modules. La *cohésion* mesure le degré auquel les éléments
d'un même module sont reliés entre eux. Un bon découpage minimise le couplage
(les modules se connaissent peu) et maximise la cohésion (chaque module a une
responsabilité claire et unifiée). Dans la première décomposition de KWIC, le
couplage est fort : tous les modules dépendent des mêmes données globales. Dans
la deuxième, le couplage est faible : chaque module interagit avec les autres
uniquement à travers une interface étroite.

Ces deux axes sont faciles à illustrer. Prenons un exemple simple : un système
qui envoie des notifications aux utilisateurs.

```python
# Couplage fort, cohésion faible
class UserManager:
    def create_user(self, name, email):
        # Crée l'utilisateur dans la base de données
        db = sqlite3.connect("app.db")
        db.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        db.commit()

        # Envoie un email de bienvenue
        smtp = smtplib.SMTP("smtp.example.com")
        smtp.send_message(f"Bienvenue {name} !")

        # Écrit dans le journal
        with open("/var/log/app.log", "a") as f:
            f.write(f"Utilisateur {name} créé\n")
```

Cette classe fait trois choses : gérer la base de données, envoyer des emails et
écrire des logs. Sa cohésion est faible, car ses responsabilités n'ont rien en
commun. Son couplage est fort, car elle dépend directement de `sqlite3`, de
`smtplib` et du système de fichiers. Si on change de base de données, de service
d'email ou de système de logging, il faut modifier cette classe.

```python
# Couplage faible, cohésion forte
class UserRepository:
    def __init__(self, db):
        self.db = db

    def create(self, name, email):
        self.db.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))

class NotificationService:
    def __init__(self, sender):
        self.sender = sender

    def welcome(self, name):
        self.sender.send(f"Bienvenue {name} !")

class UserManager:
    def __init__(self, repo, notifications, logger):
        self.repo = repo
        self.notifications = notifications
        self.logger = logger

    def create_user(self, name, email):
        self.repo.create(name, email)
        self.notifications.welcome(name)
        self.logger.info(f"Utilisateur {name} créé")
```

Chaque classe a maintenant une seule responsabilité (cohésion forte), et
`UserManager` ne connaît pas les détails internes des modules qu'il utilise
(couplage faible). On retrouve exactement le même principe que Parnas défendait
avec KWIC : chaque module cache une décision susceptible de changer.

Le couplage et la cohésion sont aussi liés au principe DRY (Don't Repeat
Yourself), formulé par Andrew Hunt et David Thomas dans *The Pragmatic
Programmer* (1999). L'idée est simple : chaque élément de connaissance dans un
système devrait avoir une représentation unique et non ambiguë. La duplication de
code est souvent un symptôme de mauvais découpage. Quand on retrouve la même
logique à deux endroits, c'est souvent parce qu'une responsabilité n'a pas été
isolée dans son propre module. Éliminer la duplication revient alors à améliorer
la cohésion : on regroupe la logique qui va ensemble, et on l'expose à travers
une interface claire.

Mais DRY ne concerne pas seulement le code dupliqué au sens littéral. Il
s'applique aussi aux structures de données, aux configurations, à la
documentation. Si la même information existe à deux endroits et qu'elle peut
diverger, c'est une violation de DRY, et c'est une source de bugs. Le principe
nous force à nous demander : "est-ce que cette connaissance a un seul
propriétaire dans mon système ?"

## Les principes SOLID

L'acronyme SOLID, popularisé par Robert C. Martin (*Clean Code*, 2008), regroupe
cinq principes de conception orientée objet. Ils ne sont pas tous également
importants dans la pratique. Le **S** (Single Responsibility) et le **D**
(Dependency Inversion) sont de loin les plus influents et les plus utiles au
quotidien. Les trois autres (Open/Closed, Liskov Substitution, Interface
Segregation) sont plus situationnels : ils s'appliquent surtout dans des
contextes de hiérarchies de classes complexes, qu'on rencontre moins souvent en
Python qu'en Java ou C#. On les présentera tous, mais avec un niveau de détail
proportionnel à leur importance pratique.

### S : Single Responsibility Principle

Le principe de responsabilité unique dit qu'une classe (ou un module) ne devrait
avoir qu'une seule raison de changer. C'est essentiellement une reformulation du
concept de cohésion qu'on vient de voir, appliqué à la conception orientée objet.
L'exemple du `UserManager` monolithique illustre exactement une violation de ce
principe : la classe change si on modifie la base de données, si on change le
service d'email, ou si on change le système de logs. Trois raisons de changer,
donc trois responsabilités, donc il faudrait trois classes.

### D : Dependency Inversion Principle

L'inversion de dépendance est peut-être le principe SOLID le plus puissant.
L'idée est que les modules de haut niveau (la logique métier) ne devraient pas
dépendre des modules de bas niveau (les détails d'implémentation). Les deux
devraient dépendre d'abstractions. En pratique, cela signifie qu'au lieu de
créer ses propres dépendances, un module les *reçoit* de l'extérieur. C'est ce
qu'on appelle l'*injection de dépendances*.

On l'a déjà vu dans l'exemple du `UserManager` refactorisé : plutôt que de
créer lui-même sa connexion `sqlite3` et son client `smtplib`, il reçoit un
`repo`, un `notifications` et un `logger` dans son constructeur. Mais pour bien
comprendre la différence, comparons deux approches d'un système de paiement :

```python
# Sans inversion de dépendance
class OrderService:
    def checkout(self, order):
        payment = StripeClient("sk_live_xxx")
        payment.charge(order.total)

# Avec inversion de dépendance
class OrderService:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def checkout(self, order):
        self.payment_gateway.charge(order.total)
```

Dans la première version, `OrderService` *crée* directement un `StripeClient`.
Il est impossible de tester cette classe sans se connecter à Stripe, et si on
veut un jour passer à un autre fournisseur de paiement, il faut modifier la
logique métier. Dans la seconde version, `OrderService` ne sait même pas quel
fournisseur de paiement est utilisé. On peut lui passer un client Stripe en
production, un client PayPal dans un autre contexte, ou un mock dans les tests.
La direction de la dépendance est *inversée* : c'est le code appelant qui décide
de l'implémentation, pas le module lui-même.

### O : Open/Closed Principle

Un module devrait être *ouvert à l'extension* mais *fermé à la modification*. En
d'autres termes, on devrait pouvoir ajouter un nouveau comportement sans modifier
le code existant. Ce principe est surtout pertinent quand on conçoit des systèmes
avec des familles de comportements interchangeables.

```python
# Violation : il faut modifier la fonction pour chaque nouveau format
def export(data, format):
    if format == "json":
        return json.dumps(data)
    elif format == "csv":
        return to_csv(data)
    elif format == "xml":  # chaque nouveau format modifie cette fonction
        return to_xml(data)

# Conforme : on ajoute un exporteur sans toucher au code existant
exporters = {
    "json": JsonExporter(),
    "csv": CsvExporter(),
}

def export(data, format):
    return exporters[format].export(data)

# Ajouter un format XML = ajouter une ligne, pas modifier la logique
exporters["xml"] = XmlExporter()
```

### L : Liskov Substitution Principle

Formulé par Barbara Liskov en 1987, ce principe dit qu'un objet d'une
sous-classe devrait pouvoir remplacer un objet de la classe parente sans casser
le programme. C'est un garde-fou contre les hiérarchies d'héritage mal conçues.

```python
# Violation classique : un carré n'est pas un rectangle au sens du LSP
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    # Problème : si on modifie width, height ne suit pas
    # Le contrat de Rectangle est violé
```

L'exemple classique est celui du carré et du rectangle. En mathématiques, un
carré *est* un rectangle. Mais en programmation, si on hérite `Square` de
`Rectangle`, le contrat est brisé : modifier la largeur d'un carré devrait aussi
modifier sa hauteur, ce qui n'est pas le comportement attendu d'un rectangle. Ce
genre de piège est un argument en faveur de la composition plutôt que de
l'héritage.

```python
# Avec héritage : on crée une hiérarchie rigide
class Animal:
    def speak(self): ...

class FlyingAnimal(Animal):
    def fly(self): print("Je vole")

class SwimmingAnimal(Animal):
    def swim(self): print("Je nage")

# Problème : un canard vole ET nage. Héritage multiple?
class Duck(FlyingAnimal, SwimmingAnimal):  # fragile et confus
    def speak(self): print("Coin")
```

```python
# Avec composition : on assemble des capacités
class FlyAbility:
    def fly(self): print("Je vole")

class SwimAbility:
    def swim(self): print("Je nage")

class Duck:
    def __init__(self):
        self.flying = FlyAbility()
        self.swimming = SwimAbility()

    def speak(self): print("Coin")

donald = Duck()
donald.flying.fly()    # "Je vole"
donald.swimming.swim()  # "Je nage"
```

Avec l'héritage, on est forcé de modéliser les capacités dans une hiérarchie
d'ancêtres, ce qui devient vite un casse-tête quand un objet combine plusieurs
comportements. Avec la composition, on assemble des briques indépendantes :
chaque capacité est un objet qu'on *possède*, plutôt qu'un ancêtre dont on
*hérite*. Ce principe, connu sous le nom de *composition over inheritance*, a
été popularisé par le livre *Design Patterns* du Gang of Four (1994), qui
recommande de "favoriser la composition d'objets plutôt que l'héritage de
classes".

### I : Interface Segregation Principle

Un client ne devrait pas être forcé de dépendre de méthodes qu'il n'utilise pas.
Plutôt qu'une grosse interface qui fait tout, il vaut mieux plusieurs interfaces
spécialisées.

```python
# Interface trop large : tous les clients doivent implémenter toutes les méthodes
class Worker:
    def work(self): ...
    def eat(self): ...
    def sleep(self): ...

# Interfaces séparées : chaque client n'implémente que ce dont il a besoin
class Workable:
    def work(self): ...

class Feedable:
    def eat(self): ...
```

Ce principe est plus naturel en Python qu'en Java, grâce au *duck typing* : on
ne dépend pas d'une interface formelle, mais simplement des méthodes qu'on
appelle effectivement.

### SOLID et YAGNI : la tension créative

Ces cinq principes sont des guides utiles, mais il faut les appliquer avec
discernement. Le principe YAGNI (You Ain't Gonna Need It), issu de la culture
Extreme Programming de Kent Beck, sert de contrepoids. YAGNI dit : ne construis
pas d'abstraction pour un besoin qui n'existe pas encore. N'ajoute pas une
interface parce qu'un jour, peut-être, tu auras besoin d'une deuxième
implémentation. Ne découpe pas un module en trois parce que le principe de
responsabilité unique le suggère, si en pratique ce module est simple et ne
change jamais.

La tension entre SOLID et YAGNI est saine. SOLID pousse vers plus d'abstraction
et de découpage. YAGNI pousse vers la simplicité et le pragmatisme. Un
développeur expérimenté navigue entre les deux en se posant la bonne question :
"est-ce que cette complexité supplémentaire résout un problème réel, ou est-ce
que je me prépare à un problème imaginaire ?" Parnas nous rappelle que le bon
critère de découpage est "quelle décision pourrait changer". Si la réponse est
"aucune, pour l'instant", alors YAGNI l'emporte.

## Les couches (layers)

Les principes qu'on vient de voir (information hiding, couplage/cohésion, SOLID) nous disent *comment* découper un système en modules. Mais ils ne disent pas *selon quelle logique* organiser ces modules entre eux. En pratique, un pattern d'organisation revient constamment : le découpage en couches. L'idée est simple : on empile des niveaux d'abstraction, chaque couche ne communiquant qu'avec celle qui est directement en dessous. Ce pattern est si répandu qu'on le retrouve partout, du modèle OSI des réseaux (7 couches) aux applications web modernes. Dans le contexte d'une application, la forme la plus courante est le découpage en trois couches : présentation, logique métier (*business logic*) et accès aux données.

<!-- ILLUSTRATION: trois couches empilées (présentation → logique métier → données) avec flèches de dépendance vers le bas -->

Prenons une application simple de gestion de produits pour illustrer ce découpage :

```python
# Couche données : gère le stockage
class ProductRepository:
    def __init__(self, db):
        self.db = db

    def find_by_id(self, product_id):
        row = self.db.execute(
            "SELECT id, name, price, stock FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()
        if row:
            return {"id": row[0], "name": row[1], "price": row[2], "stock": row[3]}
        return None

    def update_stock(self, product_id, new_stock):
        self.db.execute(
            "UPDATE products SET stock = ? WHERE id = ?",
            (new_stock, product_id)
        )

# Couche logique métier : applique les règles d'affaires
class OrderService:
    def __init__(self, products):
        self.products = products

    def place_order(self, product_id, quantity):
        product = self.products.find_by_id(product_id)
        if product is None:
            raise ValueError("Produit introuvable")
        if product["stock"] < quantity:
            raise ValueError("Stock insuffisant")
        self.products.update_stock(product_id, product["stock"] - quantity)
        total = product["price"] * quantity
        return {"product": product["name"], "quantity": quantity, "total": total}

# Couche présentation : gère l'interaction avec l'utilisateur
class OrderHandler:
    def __init__(self, order_service):
        self.order_service = order_service

    def handle_request(self, request):
        try:
            result = self.order_service.place_order(
                request["product_id"], request["quantity"]
            )
            return {"status": 200, "data": result}
        except ValueError as e:
            return {"status": 400, "error": str(e)}
```

La règle fondamentale est que les dépendances vont dans un seul sens : la présentation dépend de la logique métier, qui dépend de l'accès aux données. Jamais l'inverse. Le `ProductRepository` ne sait pas qu'il est utilisé par un `OrderService`, et l'`OrderService` ne sait pas s'il est appelé depuis une API web, une interface en ligne de commande ou un script de test. Chaque couche peut évoluer indépendamment : on peut remplacer SQLite par PostgreSQL sans toucher à la logique métier, ou transformer le handler HTTP en interface CLI sans modifier les règles d'affaires.

## Monolithe vs microservices

Jusqu'ici, on a parlé de découpage *interne* : comment organiser les modules à l'intérieur d'une application. Mais il existe un autre niveau de découpage, qui concerne la manière dont on *déploie* le système. Un monolithe est une application déployée comme une seule unité : tout le code vit dans le même processus, partage la même base de données, et est livré en bloc. À l'opposé, une architecture en microservices découpe le système en petits services indépendants, chacun déployé séparément, avec sa propre base de données et ses propres API. Le débat entre ces deux approches est l'un des plus animés en génie logiciel moderne, et il mérite d'être abordé avec nuance.

L'intuition naturelle, surtout quand on a appris les vertus du découpage, est de vouloir tout séparer dès le départ. Mais l'expérience de l'industrie montre le contraire. Un monolithe bien structuré (avec des couches claires, des modules cohésifs et un couplage faible) est presque toujours le meilleur point de départ. Martin Fowler résume cette idée par la formule *monolith first* : commencer par un monolithe, et ne découper en services que lorsque la douleur le justifie. La raison est simple : les microservices résolvent des problèmes d'organisation et de passage à l'échelle, mais ils en créent d'autres. Chaque service a besoin de sa propre infrastructure de déploiement, de monitoring, de gestion des erreurs. La communication entre services passe par le réseau, ce qui introduit de la latence, des pannes partielles et des problèmes de cohérence des données. Déboguer un problème qui traverse cinq services est incomparablement plus difficile que de déboguer un appel de fonction dans un monolithe.

<!-- ILLUSTRATION: monolithe (un seul bloc avec modules internes) vs microservices (plusieurs blocs reliés par des flèches réseau) -->

Quand est-ce que le découpage en services devient pertinent ? Typiquement quand l'organisation grandit. Si plusieurs équipes travaillent sur le même monolithe et se marchent constamment sur les pieds, si les cycles de déploiement deviennent trop lents parce qu'il faut tout retester à chaque changement, ou si certaines parties du système ont des besoins de passage à l'échelle très différents (le moteur de recherche doit gérer 10 000 requêtes par seconde, mais le module de facturation n'en traite que 100), alors il peut être judicieux d'extraire certains composants en services indépendants.

Cette observation rejoint une idée formulée dès 1968 par Melvin Conway : "les organisations qui conçoivent des systèmes sont contraintes de produire des architectures qui sont des copies de leurs structures de communication." C'est la *loi de Conway*. Si trois équipes travaillent sur un projet, le système aura tendance à se structurer en trois composants, peu importe ce que dicterait la logique technique. Cette loi a une conséquence pratique importante : l'architecture d'un système ne peut pas être décidée indépendamment de l'organisation humaine qui le construit. C'est pourquoi la question du monolithe vs microservices n'est pas seulement technique, elle est aussi organisationnelle. On reviendra sur ces dimensions humaines et collaboratives dans le module 4.

## Patterns architecturaux

Les couches, le monolithe et les microservices décrivent comment *structurer* un système. Mais il existe aussi des patterns qui décrivent comment les parties d'un système *communiquent* entre elles. Ces patterns architecturaux ne sont pas mutuellement exclusifs : un même système peut en combiner plusieurs. Ils répondent chacun à des contraintes différentes, et le choix de l'un plutôt que l'autre dépend du problème qu'on cherche à résoudre.

Le pattern le plus fondamental est probablement le **client-server**. L'idée est simple : un composant (le client) envoie des requêtes, un autre (le serveur) les traite et renvoie des réponses. C'est le modèle qui sous-tend le web tout entier : un navigateur envoie une requête HTTP, un serveur web la traite et renvoie une page ou des données. Ce pattern est tellement omniprésent qu'on a tendance à l'oublier, mais il incarne une décision architecturale importante : la centralisation de la logique et des données côté serveur, avec des clients qui ne font qu'interagir avec cette logique à travers une interface (l'API). La section suivante de ce module sera entièrement consacrée à ces interfaces.

Dans le contexte des applications web, le pattern le plus courant est le **MVC** (Model-View-Controller). Il a été conçu à l'origine par Trygve Reenskaug en 1979 pour les interfaces graphiques de Smalltalk, où il séparait les données (Model), leur affichage à l'écran (View) et la gestion des interactions souris et clavier (Controller). Les frameworks web modernes ont adopté le vocabulaire de MVC, mais en le réinterprétant : le "Model" représente les données et la logique métier, la "View" génère du HTML (ou du JSON), et le "Controller" route les requêtes HTTP vers la bonne logique. En pratique, ce découpage est une variante du pattern trois couches qu'on a vu plus haut, adapté aux spécificités du cycle requête-réponse du web.

{{< hint info >}}
**Frameworks web**

Un *framework* web est une bibliothèque qui fournit une structure prête à l'emploi pour construire des applications web : routage des requêtes HTTP, connexion à la base de données, rendu des pages, et organisation du code selon un pattern comme MVC. Parmi les plus connus, on trouve Ruby on Rails (Ruby), Django et Flask (Python), Laravel (PHP), et Express (JavaScript/Node.js). Django se décrit d'ailleurs comme MTV (Model-Template-View) plutôt que MVC, ce qui illustre bien le fait que le vocabulaire varie d'un framework à l'autre, mais que l'idée sous-jacente reste la même.
{{< /hint >}}

Le pattern **pipes and filters** organise le traitement comme une chaîne d'étapes indépendantes. Chaque filtre (*filter*) reçoit des données en entrée, les transforme, et les passe au filtre suivant via un canal (*pipe*). Ce pattern est au coeur de la philosophie Unix, où de petits utilitaires spécialisés se combinent en pipelines :

```shell
cat access.log | grep "POST" | cut -d' ' -f1 | sort | uniq -c | sort -rn
```

Cette commande extrait les adresses IP qui ont fait des requêtes POST, les compte et les trie par fréquence. Chaque utilitaire fait une seule chose (cohésion forte), ne connaît pas les autres (couplage faible), et communique par un flux de texte standard. On retrouve d'ailleurs exactement ce pattern dans la première décomposition de KWIC qu'on a vue plus tôt : une séquence d'étapes où chacune consomme la sortie de la précédente. La différence avec la deuxième décomposition de Parnas, c'est que pipes and filters optimise la composabilité au prix d'un couplage plus fort au format des données qui transitent entre les étapes.

Le dernier pattern qu'on va aborder est l'**architecture événementielle** (*event-driven*). Plutôt que d'appeler directement un autre composant (comme dans client-server), un composant *émet* un événement, et d'autres composants qui se sont *abonnés* à ce type d'événement le reçoivent et réagissent. Le producteur de l'événement ne sait pas qui l'écoute, ni même si quelqu'un l'écoute. Ce découplage est puissant : on peut ajouter de nouveaux comportements sans modifier le code existant. Par exemple, quand un utilisateur passe une commande sur un site de commerce en ligne, l'événement `CommandePassée` peut déclencher l'envoi d'un courriel de confirmation, la mise à jour de l'inventaire, et la notification au système de livraison, le tout sans que le module de commande ait besoin de connaître l'existence de ces autres modules. Ce pattern est omniprésent dans les systèmes distribués modernes, où des outils comme Apache Kafka ou RabbitMQ servent de bus d'événements. On le retrouvera d'ailleurs dans la section sur les données, quand on parlera de messaging et de streaming.