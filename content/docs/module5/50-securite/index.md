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