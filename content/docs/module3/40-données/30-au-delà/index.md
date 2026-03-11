---
title: "Au-delà des bases de données"
slug: "au-delà"
weight: 30
---

# Au-delà des bases de données

Les bases de données, qu'elles soient relationnelles ou NoSQL, répondent à un
besoin fondamental : stocker des données structurées et les retrouver par des
requêtes. Mais dans un système réel, les données vivent aussi ailleurs. Elles
sont indexées pour la recherche en texte intégral, archivées dans des lacs de
données sous forme d'objets, répliquées entre appareils qui ne sont pas toujours
connectés, ou inscrites dans des registres immuables où chaque modification est
tracée à jamais. Ces paradigmes ne remplacent pas les bases de données : ils les
complètent, chacun répondant à un besoin que les bases traditionnelles servent
mal.

## La recherche et l'indexation

La recherche d'information (*information retrieval*) est un domaine qui précède
l'informatique moderne. Dès les années 1960, Gerard Salton et son équipe à
Cornell développent le système SMART (*System for the Mechanical Analysis and
Retrieval of Text*), qui introduit les concepts fondamentaux encore utilisés
aujourd'hui : la pondération des termes (TF-IDF), le modèle vectoriel de
similarité entre documents, et l'évaluation de la pertinence par précision et
rappel. Le mécanisme central est l'index inversé (*inverted index*) : plutôt que
de parcourir chaque document pour y chercher un mot, on construit à l'avance une
table qui associe chaque terme à la liste des documents qui le contiennent,
exactement comme l'index à la fin d'un livre. Google, à sa fondation en 1998,
n'est fondamentalement rien d'autre qu'un index inversé à l'échelle du web,
enrichi par l'algorithme PageRank pour classer les résultats.

Dans le monde du logiciel d'entreprise,
[Elasticsearch](https://www.elastic.co/elasticsearch) (2010, Shay Banon) et
[Apache Solr](https://solr.apache.org/), tous deux construits sur la
bibliothèque [Apache Lucene](https://lucene.apache.org/), sont les moteurs de
recherche les plus utilisés. Ils offrent la tokenisation (découpage du texte en
termes), la racinisation (*stemming* : « chercher », « cherche », « cherché » →
« cherch »), le classement par pertinence (TF-IDF, BM25) et la recherche par
facettes. Elasticsearch est aussi au cœur de la pile ELK (Elasticsearch,
Logstash, Kibana) utilisée pour l'analyse de logs, qu'on retrouvera dans le
module 5.

En Python, on peut illustrer le concept d'index inversé avec un simple
dictionnaire, ce qui permet de comprendre le principe avant de passer à des
systèmes distribués :

{{< pyodide >}}
import re
from collections import defaultdict

# --- Construction d'un index inversé ---

documents = {
    1: "Le langage Python est utilisé en science des données et en intelligence artificielle",
    2: "Les bases de données relationnelles utilisent le langage SQL pour les requêtes",
    3: "Python permet de se connecter à des bases de données avec des bibliothèques comme SQLAlchemy",
    4: "L'intelligence artificielle utilise des modèles entraînés sur de grandes quantités de données",
    5: "La science des données combine statistiques, programmation Python et visualisation",
}

def tokeniser(texte):
    """Découpe un texte en tokens normalisés (minuscules, sans ponctuation)."""
    return re.findall(r"\b[a-zàâéèêëïîôùûüç]+\b", texte.lower())

# Construire l'index inversé
index = defaultdict(set)
for doc_id, texte in documents.items():
    for token in tokeniser(texte):
        index[token].add(doc_id)

print(f"=== Index inversé ({len(index)} termes) ===\n")
for terme in ["python", "données", "intelligence", "sql"]:
    print(f'  "{terme}" → documents {sorted(index[terme])}')

# --- Recherche avec classement par pertinence (TF simple) ---

def rechercher(requete, index, documents):
    """Recherche les documents correspondant à la requête, classés par pertinence."""
    termes = tokeniser(requete)
    scores = defaultdict(int)
    for terme in termes:
        for doc_id in index.get(terme, set()):
            scores[doc_id] += 1  # Score = nombre de termes trouvés
    resultats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return resultats

print(f"\n=== Recherche : 'Python données science' ===\n")
resultats = rechercher("Python données science", index, documents)
for doc_id, score in resultats:
    print(f"  [{score} terme(s)] Doc {doc_id}: {documents[doc_id][:70]}...")

print(f"\n=== Recherche : 'intelligence artificielle' ===\n")
resultats = rechercher("intelligence artificielle", index, documents)
for doc_id, score in resultats:
    print(f"  [{score} terme(s)] Doc {doc_id}: {documents[doc_id][:70]}...")
{{< /pyodide >}}

## Le stockage objet

Le stockage objet (*object storage*) est né d'un constat simple : les systèmes
de fichiers traditionnels, avec leur hiérarchie de répertoires, ne passent pas à
l'échelle du web. Quand on doit stocker des milliards de photos, de vidéos ou de
fichiers de logs, la métaphore du dossier et du sous-dossier devient un goulot
d'étranglement. Amazon S3 (*Simple Storage Service*), lancé en mars 2006, a
proposé une alternative radicale : un espace de noms plat (*flat namespace*) où
chaque objet est identifié par une clé unique (qui peut ressembler à un chemin,
comme `rapports/2025/ventes-q1.csv`, mais qui n'est qu'une chaîne de
caractères). Chaque objet contient les données brutes (*blob*), des métadonnées
descriptives et sa clé d'identification. L'API de S3 est devenue un standard de
facto, implémenté par des alternatives open source comme
[MinIO](https://min.io/).

Dans l'architecture des systèmes de données, le stockage objet joue souvent le
rôle de *data lake* (lac de données) : un réservoir brut où l'on déverse tout
(logs, exports CSV, images, modèles entraînés) sans imposer de structure a
priori. C'est l'opposé du *data warehouse* (entrepôt de données) vu dans la
section précédente, où les données sont nettoyées et structurées selon un schéma
rigide. Le pattern typique est de stocker les données brutes dans un lac (S3,
MinIO), puis de les extraire, transformer et charger (ETL) vers un entrepôt
orienté colonnes pour l'analyse. Cette complémentarité illustre un thème
récurrent : il n'y a pas un seul bon endroit pour les données, mais plusieurs,
chacun optimisé pour un usage différent.

En Python, on peut illustrer les concepts fondamentaux du stockage objet (espace
de noms plat, métadonnées, opérations CRUD par clé) avec un simple
dictionnaire :

{{< pyodide >}}
import datetime
import hashlib
import json

class StockageObjet:
    """Simulacre minimaliste d'un service de stockage objet (style S3)."""

    def __init__(self, nom_bucket):
        self.nom = nom_bucket
        self.objets = {}  # clé → {"donnees": bytes, "meta": dict}

    def put(self, cle, donnees, **meta):
        """Dépose un objet dans le bucket."""
        contenu = donnees.encode() if isinstance(donnees, str) else donnees
        self.objets[cle] = {
            "donnees": contenu,
            "meta": {
                "taille": len(contenu),
                "md5": hashlib.md5(contenu).hexdigest(),
                "date": datetime.datetime.now().isoformat(),
                **meta,
            },
        }
        print(f"  PUT  {cle}  ({len(contenu)} octets)")

    def get(self, cle):
        """Récupère un objet par sa clé."""
        obj = self.objets.get(cle)
        if obj is None:
            print(f"  GET  {cle}  → NON TROUVÉ")
            return None
        print(f"  GET  {cle}  → {obj['meta']['taille']} octets")
        return obj["donnees"]

    def head(self, cle):
        """Retourne uniquement les métadonnées (sans télécharger le contenu)."""
        obj = self.objets.get(cle)
        if obj is None:
            return None
        return obj["meta"]

    def ls(self, prefixe=""):
        """Liste les clés avec un préfixe donné (simule le flat namespace)."""
        return [c for c in sorted(self.objets) if c.startswith(prefixe)]

    def delete(self, cle):
        """Supprime un objet."""
        if cle in self.objets:
            del self.objets[cle]
            print(f"  DEL  {cle}")

# --- Démonstration ---

bucket = StockageObjet("mon-data-lake")

print("=== Dépôt d'objets ===\n")
bucket.put("rapports/2025/ventes-q1.csv", "produit,montant\nCafé,1200\nThé,800", type="text/csv")
bucket.put("rapports/2025/ventes-q2.csv", "produit,montant\nCafé,1350\nThé,920", type="text/csv")
bucket.put("images/logo.png", "<<données binaires PNG simulées>>", type="image/png")
bucket.put("modeles/classification-v2.pkl", "<<modèle sérialisé>>", type="application/octet-stream")

print(f"\n=== Liste par préfixe ===\n")
for prefixe in ["rapports/", "images/", ""]:
    cles = bucket.ls(prefixe)
    label = prefixe if prefixe else "(tout)"
    print(f'  "{label}" → {cles}')

print(f"\n=== Métadonnées (HEAD) ===\n")
meta = bucket.head("rapports/2025/ventes-q1.csv")
for k, v in meta.items():
    print(f"  {k:8s} : {v}")

print(f"\n=== Lecture et suppression ===\n")
contenu = bucket.get("rapports/2025/ventes-q1.csv")
print(f"  Contenu : {contenu.decode()[:50]}...")
bucket.delete("modeles/classification-v2.pkl")
print(f"  Objets restants : {bucket.ls()}")
{{< /pyodide >}}

## Les données répliquées et les CRDTs

Jusqu'ici, on a implicitement supposé que les données vivent dans un seul
endroit faisant autorité : un serveur de base de données, un bucket S3, un
moteur de recherche. Mais que se passe-t-il quand les données doivent exister
simultanément sur plusieurs appareils qui ne sont pas toujours connectés ? C'est
le défi de l'édition collaborative en temps réel (Google Docs, Figma) et des
applications *offline-first* (qui fonctionnent hors ligne et se synchronisent
plus tard). Le problème fondamental est la convergence : si Alice et Bob
modifient chacun leur copie locale des mêmes données, comment garantir qu'après
synchronisation, ils auront le même résultat, quel que soit l'ordre dans lequel
les modifications arrivent ?

La réponse théorique est venue en 2011, quand Marc Shapiro, Nuno Preguiça,
Carlos Baquero et Marek Zawirski ont formalisé les CRDT (*Conflict-free
Replicated Data Types*), des structures de données mathématiquement conçues pour
que la fusion de modifications concurrentes soit toujours possible sans conflit.
L'intuition est élégante : on conçoit des opérations qui sont commutatives
(l'ordre n'importe pas) et idempotentes (appliquer deux fois donne le même
résultat). Un G-Counter (compteur croissant), par exemple, donne à chaque nœud
son propre compteur ; la fusion prend le maximum de chaque compteur, et la
valeur globale est la somme. Peu importe l'ordre de synchronisation, le résultat
est toujours correct. Martin Kleppmann, l'auteur de *Designing Data-Intensive
Applications*, travaille activement sur ce sujet : il est l'un des créateurs
d'[Automerge](https://automerge.org/), une bibliothèque CRDT pour l'édition
collaborative. [Yjs](https://yjs.dev/) est l'autre bibliothèque de référence
dans ce domaine.

En Python, on peut implémenter deux CRDTs fondamentaux pour illustrer comment la
convergence automatique fonctionne :

{{< pyodide >}}
# --- G-Counter : compteur distribué (croissant seulement) ---

class GCounter:
    """
    Grow-only Counter — chaque nœud maintient son propre compteur.
    La valeur globale est la somme de tous les compteurs.
    La fusion prend le max de chaque compteur (idempotente et commutative).
    """

    def __init__(self, noeud_id, compteurs=None):
        self.noeud_id = noeud_id
        self.compteurs = dict(compteurs) if compteurs else {}

    def incrementer(self, n=1):
        self.compteurs[self.noeud_id] = self.compteurs.get(self.noeud_id, 0) + n

    def valeur(self):
        return sum(self.compteurs.values())

    def merge(self, autre):
        """Fusionne avec un autre G-Counter (max par nœud)."""
        tous_noeuds = set(self.compteurs) | set(autre.compteurs)
        fusionne = {}
        for n in tous_noeuds:
            fusionne[n] = max(self.compteurs.get(n, 0), autre.compteurs.get(n, 0))
        return GCounter(self.noeud_id, fusionne)

    def __repr__(self):
        return f"GCounter({self.compteurs}) = {self.valeur()}"

# Simulation : 3 serveurs comptent des visites indépendamment

print("=== G-Counter : compteur de visites distribué ===\n")

serveur_a = GCounter("A")
serveur_b = GCounter("B")
serveur_c = GCounter("C")

# Chaque serveur reçoit des visites indépendamment
serveur_a.incrementer(5)
serveur_b.incrementer(3)
serveur_c.incrementer(7)
serveur_a.incrementer(2)  # A reçoit encore des visites

print(f"  Serveur A (local) : {serveur_a}")
print(f"  Serveur B (local) : {serveur_b}")
print(f"  Serveur C (local) : {serveur_c}")

# Synchronisation : fusion des états
total = serveur_a.merge(serveur_b).merge(serveur_c)
print(f"\n  Après fusion      : {total}")

# --- OR-Set : ensemble avec ajout ET suppression ---

print(f"\n=== OR-Set : panier d'achat collaboratif ===\n")

class ORSet:
    """
    Observed-Remove Set — supporte ajout et suppression sans conflit.
    Chaque ajout reçoit un tag unique ; la suppression retire les tags observés.
    """

    def __init__(self, noeud_id):
        self.noeud_id = noeud_id
        self.elements = {}  # element → set(tags)
        self.compteur = 0

    def _tag(self):
        self.compteur += 1
        return f"{self.noeud_id}:{self.compteur}"

    def ajouter(self, element):
        tag = self._tag()
        self.elements.setdefault(element, set()).add(tag)
        print(f"  [{self.noeud_id}] + {element}  (tag={tag})")

    def supprimer(self, element):
        if element in self.elements:
            tags = self.elements.pop(element)
            print(f"  [{self.noeud_id}] - {element}  (tags supprimés: {tags})")

    def contenu(self):
        return {e for e, tags in self.elements.items() if tags}

    def merge(self, autre):
        """Fusionne : union des tags pour chaque élément."""
        resultat = ORSet(self.noeud_id)
        resultat.compteur = max(self.compteur, autre.compteur)
        tous = set(self.elements) | set(autre.elements)
        for e in tous:
            tags = self.elements.get(e, set()) | autre.elements.get(e, set())
            if tags:
                resultat.elements[e] = set(tags)
        return resultat

    def __repr__(self):
        return f"ORSet({sorted(self.contenu())})"

# Alice et Bob modifient le même panier hors ligne

alice = ORSet("Alice")
bob = ORSet("Bob")

alice.ajouter("Lait")
alice.ajouter("Pain")
alice.ajouter("Beurre")

print()
bob.ajouter("Lait")
bob.ajouter("Œufs")
bob.supprimer("Lait")  # Bob retire le lait

print(f"\n  Panier Alice : {alice}")
print(f"  Panier Bob   : {bob}")

# Synchronisation
fusionne = alice.merge(bob)
print(f"\n  Après fusion  : {fusionne}")
print(f"  → Le lait est présent car Alice l'a ajouté avec un tag")
print(f"    que Bob n'avait pas observé lors de sa suppression")
{{< /pyodide >}}

## Les registres immuables et la blockchain

Un *ledger* (grand livre) est un registre chronologique et immuable de
transactions, exactement comme le grand livre comptable utilisé depuis des
siècles, où chaque écriture est datée, signée et ne peut être ni effacée ni
modifiée après coup. En informatique, l'immuabilité est une propriété
puissante : plutôt que de mettre à jour un solde en écrasant l'ancienne valeur
(comme dans une base de données classique), un registre immuable conserve
l'historique complet de toutes les opérations, et l'état courant se déduit en
rejouant la séquence des transactions. C'est le principe de la comptabilité en
partie double, mais c'est aussi celui de l'*event sourcing*, un pattern
architectural décrit par Martin Fowler où l'on stocke les événements plutôt que
l'état courant. Git, d'ailleurs, fonctionne exactement sur ce principe : chaque
commit est un événement immuable, et l'état du code à un instant donné se
reconstitue en rejouant l'historique.

La blockchain pousse cette idée un cran plus loin en la rendant distribuée et
résistante à la falsification. Les transactions sont regroupées en blocs, chaque
bloc contenant le hash cryptographique du bloc précédent, formant une chaîne
dont toute modification rétroactive serait immédiatement détectable. Le livre
blanc de Satoshi Nakamoto (2008), qui a introduit Bitcoin, a montré qu'il était
possible de maintenir un tel registre sans autorité centrale, en utilisant un
mécanisme de consensus (*proof of work*). Au-delà des cryptomonnaies, le concept
de registre immuable avec vérification cryptographique trouve des applications en
traçabilité (chaînes d'approvisionnement), en audit financier et en
certification de documents. [Amazon QLDB](https://aws.amazon.com/qldb/) offre un
ledger centralisé (sans consensus distribué) avec vérification cryptographique,
utile quand on veut l'immuabilité sans la complexité d'une blockchain.

En Python, on peut implémenter un mini-ledger avec chaînage cryptographique pour
illustrer les principes fondamentaux :

{{< pyodide >}}
import hashlib
import json
from datetime import datetime

# --- Bloc : unité de base de la chaîne ---

class Bloc:
    def __init__(self, index, transactions, hash_precedent):
        self.index = index
        self.horodatage = datetime.now().isoformat()
        self.transactions = transactions
        self.hash_precedent = hash_precedent
        self.hash = self.calculer_hash()

    def calculer_hash(self):
        """Hash SHA-256 du contenu du bloc (immuabilité cryptographique)."""
        contenu = json.dumps({
            "index": self.index,
            "horodatage": self.horodatage,
            "transactions": self.transactions,
            "hash_precedent": self.hash_precedent,
        }, sort_keys=True)
        return hashlib.sha256(contenu.encode()).hexdigest()

# --- Ledger : chaîne de blocs ---

class Ledger:
    def __init__(self):
        # Bloc genesis (premier bloc, sans prédécesseur)
        genesis = Bloc(0, [{"type": "GENESIS", "description": "Création du ledger"}], "0" * 64)
        self.chaine = [genesis]
        self.transactions_en_attente = []

    def ajouter_transaction(self, transaction):
        """Ajoute une transaction au pool en attente."""
        transaction["horodatage"] = datetime.now().isoformat()
        self.transactions_en_attente.append(transaction)

    def miner_bloc(self):
        """Regroupe les transactions en attente dans un nouveau bloc."""
        if not self.transactions_en_attente:
            print("  Aucune transaction en attente.")
            return
        nouveau = Bloc(
            index=len(self.chaine),
            transactions=self.transactions_en_attente,
            hash_precedent=self.chaine[-1].hash,
        )
        self.chaine.append(nouveau)
        n = len(self.transactions_en_attente)
        self.transactions_en_attente = []
        print(f"  Bloc #{nouveau.index} miné ({n} transaction(s)), hash: {nouveau.hash[:16]}...")

    def verifier_integrite(self):
        """Vérifie que la chaîne n'a pas été altérée."""
        for i in range(1, len(self.chaine)):
            bloc = self.chaine[i]
            precedent = self.chaine[i - 1]
            # Vérifier le chaînage
            if bloc.hash_precedent != precedent.hash:
                return False, f"Bloc #{i} : hash_precedent ne correspond pas"
            # Vérifier l'intégrité du bloc lui-même
            if bloc.hash != bloc.calculer_hash():
                return False, f"Bloc #{i} : hash invalide (données altérées)"
        return True, "Chaîne intègre"

    def solde(self, compte):
        """Calcule le solde d'un compte en rejouant toutes les transactions."""
        total = 0.0
        for bloc in self.chaine:
            for tx in bloc.transactions:
                if tx.get("de") == compte:
                    total -= tx.get("montant", 0)
                if tx.get("a") == compte:
                    total += tx.get("montant", 0)
        return total

# --- Démonstration ---

ledger = Ledger()

print("=== Ajout de transactions ===\n")

# Dépôts initiaux
ledger.ajouter_transaction({"type": "DEPOT", "a": "Alice", "montant": 1000, "description": "Dépôt initial"})
ledger.ajouter_transaction({"type": "DEPOT", "a": "Bob", "montant": 500, "description": "Dépôt initial"})
ledger.miner_bloc()

# Transferts
ledger.ajouter_transaction({"type": "TRANSFERT", "de": "Alice", "a": "Bob", "montant": 150, "description": "Paiement facture"})
ledger.ajouter_transaction({"type": "TRANSFERT", "de": "Bob", "a": "Charlie", "montant": 75, "description": "Remboursement"})
ledger.miner_bloc()

ledger.ajouter_transaction({"type": "TRANSFERT", "de": "Alice", "a": "Charlie", "montant": 200, "description": "Achat service"})
ledger.miner_bloc()

print(f"\n=== État de la chaîne ({len(ledger.chaine)} blocs) ===\n")
for bloc in ledger.chaine:
    print(f"  Bloc #{bloc.index}  hash: {bloc.hash[:16]}...  prev: {bloc.hash_precedent[:16]}...")
    for tx in bloc.transactions:
        desc = tx.get("description", "")
        montant = tx.get("montant", "")
        print(f"    → {tx['type']:10s} {desc}  {f'{montant} $' if montant else ''}")

print(f"\n=== Soldes (calculés par replay) ===\n")
for compte in ["Alice", "Bob", "Charlie"]:
    print(f"  {compte:10s} : {ledger.solde(compte):8.2f} $")

print(f"\n=== Vérification d'intégrité ===\n")
valide, message = ledger.verifier_integrite()
print(f"  {message}")

# Tentative de falsification
print(f"\n=== Tentative de falsification ===\n")
ledger.chaine[1].transactions[0]["montant"] = 999999
print(f"  Bloc #1 modifié : montant changé à 999999 $")
valide, message = ledger.verifier_integrite()
print(f"  Vérification : {message}")
{{< /pyodide >}}

## Le web sémantique : une grande ambition inachevée

Au début des années 2000, Tim Berners-Lee, l'inventeur du World Wide Web, a
proposé une vision ambitieuse : le *web sémantique*. L'idée était de transformer
le web, conçu pour être lu par des humains, en un réseau de données structurées
lisibles par des machines. Plutôt que de publier des pages HTML dont le contenu
n'est compréhensible que visuellement, on décrirait les données avec des formats
standardisés (RDF, OWL) et on les relierait entre elles par des identifiants
universels (URI), créant un immense graphe de connaissances interrogeable par un
langage de requêtes dédié (SPARQL). La promesse était séduisante : un agent
logiciel pourrait, par exemple, trouver automatiquement un médecin disponible
près de chez vous en croisant des données médicales, géographiques et d'agenda,
toutes publiées dans des formats interopérables.

Dans la pratique, le web sémantique n'a jamais atteint la masse critique
espérée. Les standards RDF et OWL se sont avérés complexes à maîtriser pour les
développeurs ordinaires, et le coût d'annotation des données existantes était
prohibitif. Publier une page HTML est simple ; la décrire dans un graphe RDF
avec des ontologies formelles demande un effort considérable pour un bénéfice
souvent incertain. Le web "réel" a évolué dans une direction différente : plutôt
que des données sémantiquement riches et décentralisées, ce sont les grandes
plateformes centralisées (Google, Facebook, Amazon) qui ont structuré
l'information, chacune dans ses propres formats propriétaires. Le web sémantique
est devenu un cas d'étude intéressant en génie logiciel : une architecture
techniquement élégante qui n'a pas survécu au contact avec les réalités
économiques et la friction d'adoption. C'est une illustration du principe YAGNI
à l'échelle d'un écosystème : la complexité anticipée n'a pas trouvé preneur.

Certaines idées du web sémantique ont toutefois survécu sous des formes plus
pragmatiques. [Schema.org](https://schema.org/), lancé en 2011 par Google,
Microsoft, Yahoo et Yandex, propose un vocabulaire commun pour annoter les pages
web avec des métadonnées structurées : le type d'un contenu (recette, événement,
produit, personne), ses propriétés et ses relations. Ces annotations, encodées
en [JSON-LD](https://json-ld.org/) (*JSON for Linked Data*), sont invisibles
pour l'utilisateur mais exploitées par les moteurs de recherche pour afficher des
résultats enrichis (les "rich snippets" de Google : étoiles de notation,
horaires, prix). JSON-LD a réussi là où RDF avait échoué : il s'intègre
naturellement dans les pratiques existantes des développeurs web, puisqu'il
s'agit simplement de JSON avec quelques conventions supplémentaires. Le projet
[Wikidata](https://www.wikidata.org/), la base de connaissances structurée de
Wikipédia, est probablement la réalisation la plus fidèle de la vision originale
du web sémantique, avec plus de 100 millions d'éléments reliés entre eux dans un
graphe ouvert et interrogeable. L'héritage du web sémantique est donc réel, mais
il a pris une forme que ses concepteurs n'avaient pas tout à fait anticipée : des
standards légers adoptés par pragmatisme, plutôt qu'une infrastructure
universelle adoptée par conviction.
