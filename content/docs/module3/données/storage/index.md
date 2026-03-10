---
title: "Les bases de données"
weight: 20
---

# L'évolution des bases de données

La section précédente a montré comment les données sont représentées : encodées
en bits, sérialisées en formats textuels ou binaires, structurées par des
schémas. Mais représenter des données ne suffit pas. Dès qu'un système doit
conserver des données au-delà de l'exécution d'un programme, les retrouver
efficacement, et garantir leur cohérence même en cas de panne ou d'accès
concurrent, on entre dans le domaine des bases de données.

L'histoire des bases de données est une des plus riches de l'informatique. Elle
s'étend sur plus de soixante ans et reflète, à chaque étape, les tensions
fondamentales du génie logiciel : simplicité contre expressivité, performance
contre flexibilité, cohérence contre disponibilité. Martin Kleppmann, dans
*Designing Data-Intensive Applications*, montre que comprendre cette histoire
n'est pas un exercice académique : les compromis qui ont guidé la conception
d'IMS en 1966 sont les mêmes qui orientent aujourd'hui le choix entre une base
relationnelle et une base NoSQL.

Nous allons parcourir cette évolution d'une manière un peu particulière : au
lieu de décrire chaque modèle de manière abstraite, nous allons les
implémenter. Le même scénario universitaire (départements, professeurs, cours,
étudiants) sera modélisé successivement dans le modèle hiérarchique, le modèle
en réseau, puis le modèle relationnel, ce qui permettra de voir concrètement ce
que chaque paradigme gagne et ce qu'il perd par rapport au précédent. On
poursuivra ensuite avec les transactions, les ORMs, la révolution NoSQL et les
bases spécialisées.

## Le modèle hiérarchique (IBM, années 60)

Le modèle hiérarchique est le premier modèle de base de données à avoir été
formalisé. Son incarnation la plus célèbre, IMS (*Information Management
System*) d'IBM, a été développée à partir de 1966 pour le programme Apollo de
la NASA : il fallait gérer la nomenclature de millions de pièces qui composaient
le vaisseau spatial, et cette nomenclature avait naturellement une structure
d'arbre (un module contient des sous-systèmes, qui contiennent des composants,
qui contiennent des pièces). Le modèle hiérarchique généralise cette intuition :
toutes les données sont organisées en arbre, où chaque enregistrement a
exactement un parent (sauf la racine). L'accès aux données est navigationnel :
on descend dans l'arbre en suivant les branches.

Pour comprendre concrètement ce que cela implique, implémentons un modèle
hiérarchique simplifié en Python.

{{< pyodide >}}

"""
Modèle hiérarchique — illustration en Python
==============================================

Le modèle hiérarchique (IMS d'IBM, 1966) organise les données
en arbre : chaque enregistrement a exactement un parent,
et on navigue de haut en bas dans l'arbre.

Ce programme illustre les idées centrales :
  1. La structure est un ARBRE (pas un graphe quelconque)
  2. Chaque nœud a UN SEUL parent (sauf la racine)
  3. L'accès aux données est NAVIGATIONNEL (on descend dans l'arbre)
  4. La duplication est inévitable pour les relations M:N
"""

class Noeud:
    """Un enregistrement dans la base hiérarchique."""

    def __init__(self, type_segment: str, donnees: dict):
        self.type_segment = type_segment  # le « type de segment » (≈ type d'entité)
        self.donnees = donnees
        self.enfants: list["Noeud"] = []

    def ajouter_enfant(self, type_segment: str, donnees: dict):
        enfant = Noeud(type_segment, donnees)
        self.enfants.append(enfant)
        return enfant                     # pratique pour le chaînage

    def __repr__(self):
        return f"{self.type_segment}({self.donnees})"

{{< /pyodide >}}

La structure est simple : un noeud contient un type, des données et une liste
d'enfants. C'est précisément cette simplicité qui a rendu le modèle hiérarchique
attrayant dans les années 60. Créons maintenant une petite base de données
universitaire pour voir comment les données s'organisent dans cet arbre :

```
Université
  └── Département
        ├── Professeur
        └── Cours
              └── Étudiant
```

{{< pyodide >}}

# Racine
uqam = Noeud("Université", {"nom": "UQAM"})

# Départements
info = uqam.ajouter_enfant("Département", {"nom": "Informatique", "code": "INFO"})
math = uqam.ajouter_enfant("Département", {"nom": "Mathématiques", "code": "MATH"})

# Professeurs
info.ajouter_enfant("Professeur", {"nom": "Tremblay", "bureau": "PK-4150"})
info.ajouter_enfant("Professeur", {"nom": "Gagnon",   "bureau": "PK-4920"})
math.ajouter_enfant("Professeur", {"nom": "Lavoie",   "bureau": "PK-5230"})

# Cours
bd   = info.ajouter_enfant("Cours", {"sigle": "INF3080", "titre": "Bases de données"})
algo = info.ajouter_enfant("Cours", {"sigle": "INF3105", "titre": "Structures de données"})
stat = math.ajouter_enfant("Cours", {"sigle": "MAT2080", "titre": "Statistiques"})

# Étudiants inscrits aux cours
bd.ajouter_enfant("Étudiant", {"matricule": "TRAA01", "nom": "Alice"})
bd.ajouter_enfant("Étudiant", {"matricule": "MORB02", "nom": "Bob"})
algo.ajouter_enfant("Étudiant", {"matricule": "TRAA01", "nom": "Alice"})  # ⚠ DUPLICATION
stat.ajouter_enfant("Étudiant", {"matricule": "MORB02", "nom": "Bob"})    # ⚠ DUPLICATION

{{< /pyodide >}}

Pour explorer cette base, il nous faut des outils de navigation. Dans IMS,
l'opération fondamentale était le *Get Next* (GN) : on parcourait l'arbre en
profondeur, segment par segment. Notre fonction `afficher_arbre` reproduit cette
logique :

{{< pyodide >}}

def afficher_arbre(noeud: Noeud, niveau: int = 0):
    """Parcours en profondeur — la façon naturelle de lire une base hiérarchique."""
    indent = "    " * niveau
    print(f"{indent}📂 {noeud.type_segment} : {noeud.donnees}")
    for enfant in noeud.enfants:
        afficher_arbre(enfant, niveau + 1)

afficher_arbre(uqam)
{{< /pyodide >}}

On peut aussi naviguer vers un type de segment particulier en spécifiant un
chemin dans l'arbre, l'équivalent simplifié de la commande GN d'IMS :

{{< pyodide >}}

def naviguer(noeud: Noeud, *chemin: str) -> list[Noeud]:
    """
    Navigation descendante par types de segments.

    Exemple : naviguer(uqam, "Département", "Cours")
    → retourne tous les Cours de tous les Départements.

    C'est l'équivalent simplifié de la commande GN (Get Next)
    d'IMS : on spécifie le chemin dans l'arbre.
    """
    if not chemin:
        return [noeud]

    type_cherche, *reste = chemin
    resultats = []
    for enfant in noeud.enfants:
        if enfant.type_segment == type_cherche:
            resultats.extend(naviguer(enfant, *reste))
    return resultats

for cours in naviguer(uqam, "Département", "Cours"):
    print(f"  → {cours.donnees}")
{{< /pyodide >}}

Et si on veut chercher un enregistrement par sa valeur plutôt que par sa
position dans l'arbre, il faut parcourir toute la structure :

{{< pyodide >}}
def chercher(noeud: Noeud, type_segment: str, cle: str, valeur) -> list[Noeud]:
    """
    Recherche par type + valeur — toujours en descendant dans l'arbre.
    """
    resultats = []
    if noeud.type_segment == type_segment and noeud.donnees.get(cle) == valeur:
        resultats.append(noeud)
    for enfant in noeud.enfants:
        resultats.extend(chercher(enfant, type_segment, cle, valeur))
    return resultats

alices = chercher(uqam, "Étudiant", "nom", "Alice")
print(f"  Trouvé {len(alices)} occurrence(s) :")
for a in alices:
    print(f"    → {a.donnees}")
{{< /pyodide >}}

Alice est inscrite à INF3080 et INF3105. Dans le modèle hiérarchique, chaque
nœud a UN SEUL parent, donc Alice doit apparaître DEUX FOIS dans l'arbre :

```
    Cours INF3080
    └── Étudiant Alice  ← copie 1
    Cours INF3105
    └── Étudiant Alice  ← copie 2
```

Conséquences :
* Gaspillage d'espace
* Risque d'incohérence si on met à jour une copie mais pas l'autre
* Pas de moyen simple de poser la question :
    « À quels cours Alice est-elle inscrite ? »
    (il faut parcourir TOUT l'arbre)

## Le modèle en réseau (CODASYL, fin des années 60)

Le modèle hiérarchique avait un défaut structurel : la contrainte d'un seul
parent par enregistrement rendait les relations plusieurs-à-plusieurs impossibles
sans duplication. Le comité CODASYL (*Conference on Data Systems Languages*), le
même organisme qui avait standardisé COBOL, s'est attaqué à ce problème à la fin
des années 60. Son *Data Base Task Group* (DBTG) a proposé en 1969 le modèle en
réseau, qui généralise l'arbre en graphe : un enregistrement peut désormais avoir
plusieurs parents, grâce à des ensembles nommés (*sets*) qui relient un type
« propriétaire » (*owner*) à un type « membre » (*member*). La duplication
disparaît, mais l'accès aux données reste navigationnel.

{{< pyodide >}}

"""
Modèle réseau (CODASYL) — illustration en Python
==================================================

Le modèle réseau (CODASYL/DBTG, 1969) est une évolution du modèle
hiérarchique. L'idée clé : un enregistrement peut avoir PLUSIEURS
parents, grâce à des ensembles nommés (SETs) qui relient un type
« owner » à un type « member ».

Ce programme illustre les idées centrales :
  1. Les enregistrements (RECORDS) existent indépendamment
  2. Les liens sont des ENSEMBLES NOMMÉS (SETs) de type owner → member
  3. Un enregistrement peut être member de PLUSIEURS sets
     → résout le problème de duplication du modèle hiérarchique
  4. L'accès reste NAVIGATIONNEL (FIND, GET, FIND NEXT WITHIN SET…)
"""

# ============================================================
# 1. Définitions : Record, Set, et la base réseau
# ============================================================

class Record:
    """Un enregistrement dans la base réseau."""

    def __init__(self, type_record: str, donnees: dict):
        self.type_record = type_record
        self.donnees = donnees

    def __repr__(self):
        return f"{self.type_record}({self.donnees})"


class Set:
    """
    Un SET CODASYL : un lien nommé entre un owner et ses members.

    Contrainte fondamentale : chaque member ne peut appartenir
    qu'à UNE SEULE instance d'un set donné (un seul owner par set).
    Mais un record peut être member de PLUSIEURS sets différents.
    """

    def __init__(self, nom: str, owner: Record):
        self.nom = nom
        self.owner = owner
        self.members: list[Record] = []

    def inserer(self, member: Record):
        self.members.append(member)

    def __repr__(self):
        return f"Set '{self.nom}' : {self.owner} → {self.members}"


class BaseReseau:
    """
    Une base de données réseau simplifiée.

    Stocke tous les records et tous les sets,
    et fournit des opérations de navigation.
    """

    def __init__(self):
        self.records: list[Record] = []
        self.sets: list[Set] = []

    def creer_record(self, type_record: str, donnees: dict) -> Record:
        """STORE record — crée un enregistrement dans la base."""
        rec = Record(type_record, donnees)
        self.records.append(rec)
        return rec

    def creer_set(self, nom: str, owner: Record) -> Set:
        """Déclare une instance de set avec son owner."""
        s = Set(nom, owner)
        self.sets.append(s)
        return s

    # --- Navigation dans les sets ---

    def find_members(self, nom_set: str, owner: Record) -> list[Record]:
        """
        FIND NEXT WITHIN SET — retourne tous les members
        d'un owner dans un set nommé.
        """
        for s in self.sets:
            if s.nom == nom_set and s.owner is owner:
                return list(s.members)
        return []

    def find_owner(self, nom_set: str, member: Record) -> Record | None:
        """
        FIND OWNER WITHIN SET — navigation INVERSE.
        Étant donné un member, retrouve son owner dans un set nommé.
        """
        for s in self.sets:
            if s.nom == nom_set and member in s.members:
                return s.owner
        return None

    def find_all_owners(self, nom_set: str, member: Record) -> list[Record]:
        """
        Retrouve TOUS les owners d'un member dans un type de set.
        (Utile quand un record est member de plusieurs instances du même set.)
        """
        return [s.owner for s in self.sets
                if s.nom == nom_set and member in s.members]

    def find_records(self, type_record: str, cle: str, valeur) -> list[Record]:
        """FIND record by type + valeur."""
        return [r for r in self.records
                if r.type_record == type_record and r.donnees.get(cle) == valeur]

{{< /pyodide >}}

Remarquons que les enregistrements existent désormais indépendamment, sans être
imbriqués dans un arbre. Les liens entre eux sont explicites et nommés.
Reconstruisons notre scénario universitaire avec ce modèle :

{{< pyodide >}}

# ============================================================
# 2. Construction de la base — même scénario universitaire
# ============================================================
#
# Schéma réseau :
#
#   Département ──[DEPT_PROF]──→ Professeur
#   Département ──[DEPT_COURS]──→ Cours
#   Cours ────────[INSCRIPTION]──→ Étudiant   ← un étudiant peut
#   (plusieurs cours)                            être member de
#                                                PLUSIEURS sets
#                                                INSCRIPTION

db = BaseReseau()

# --- Records (existent indépendamment, pas dans un arbre) ---
info = db.creer_record("Département", {"nom": "Informatique", "code": "INFO"})
math = db.creer_record("Département", {"nom": "Mathématiques", "code": "MATH"})

tremblay = db.creer_record("Professeur", {"nom": "Tremblay", "bureau": "PK-4150"})
gagnon   = db.creer_record("Professeur", {"nom": "Gagnon",   "bureau": "PK-4920"})
lavoie   = db.creer_record("Professeur", {"nom": "Lavoie",   "bureau": "PK-5230"})

bd   = db.creer_record("Cours", {"sigle": "INF3080", "titre": "Bases de données"})
algo = db.creer_record("Cours", {"sigle": "INF3105", "titre": "Structures de données"})
stat = db.creer_record("Cours", {"sigle": "MAT2080", "titre": "Statistiques"})

alice = db.creer_record("Étudiant", {"matricule": "TRAA01", "nom": "Alice"})  # ← UNE SEULE fois !
bob   = db.creer_record("Étudiant", {"matricule": "MORB02", "nom": "Bob"})    # ← UNE SEULE fois !

# --- Sets : les liens nommés entre records ---

# Département → Professeurs
set_info_prof = db.creer_set("DEPT_PROF", info)
set_info_prof.inserer(tremblay)
set_info_prof.inserer(gagnon)

set_math_prof = db.creer_set("DEPT_PROF", math)
set_math_prof.inserer(lavoie)

# Département → Cours
set_info_cours = db.creer_set("DEPT_COURS", info)
set_info_cours.inserer(bd)
set_info_cours.inserer(algo)

set_math_cours = db.creer_set("DEPT_COURS", math)
set_math_cours.inserer(stat)

# Cours → Étudiants (INSCRIPTION)
# Alice est inscrite à BD et ALGO — même objet, deux sets différents
set_inscr_bd = db.creer_set("INSCRIPTION", bd)
set_inscr_bd.inserer(alice)
set_inscr_bd.inserer(bob)

set_inscr_algo = db.creer_set("INSCRIPTION", algo)
set_inscr_algo.inserer(alice)       # ✅ PAS de duplication !

set_inscr_stat = db.creer_set("INSCRIPTION", stat)
set_inscr_stat.inserer(bob)         # ✅ PAS de duplication !

{{< /pyodide >}}

Le résultat ressemble à ce qu'on obtenait avec le modèle hiérarchique, mais la
structure sous-jacente est fondamentalement différente : Alice et Bob n'existent
qu'une seule fois dans la base :

{{< pyodide >}}

print("=" * 60)
print("STRUCTURE DE LA BASE RÉSEAU")
print("=" * 60)
for dept in db.find_records("Département", "nom", "Informatique") + \
            db.find_records("Département", "nom", "Mathématiques"):
    print(f"\n📂 {dept}")
    profs = db.find_members("DEPT_PROF", dept)
    if profs:
        print("    Professeurs :")
        for p in profs:
            print(f"        → {p.donnees}")
    cours = db.find_members("DEPT_COURS", dept)
    if cours:
        print("    Cours :")
        for c in cours:
            etudiants = db.find_members("INSCRIPTION", c)
            noms = [e.donnees["nom"] for e in etudiants]
            print(f"        → {c.donnees}  [{', '.join(noms)}]")

{{< /pyodide >}}

La navigation avant fonctionne comme avant : trouver les étudiants inscrits à un
cours donné :

{{< pyodide >}}

print("\n" + "=" * 60)
print("NAVIGATION AVANT : étudiants inscrits à INF3080")
print("=" * 60)
for e in db.find_members("INSCRIPTION", bd):
    print(f"  → {e.donnees}")

{{< /pyodide >}}

Mais la vraie nouveauté, c'est la navigation inverse. La question « à quels
cours Alice est-elle inscrite ? », qui exigeait un parcours complet de l'arbre
dans le modèle hiérarchique, se résout maintenant directement :

{{< pyodide >}}

print("\n" + "=" * 60)
print("NAVIGATION INVERSE : cours d'Alice")
print("=" * 60)
cours_alice = db.find_all_owners("INSCRIPTION", alice)
for c in cours_alice:
    print(f"  → {c.donnees}")

{{< /pyodide >}}

Alice n'existe qu'UNE SEULE FOIS dans la base de données. Elle est membre de
deux sets INSCRIPTION (un par cours).

* Plus de duplication !
* La question « quels cours suit Alice ? » se résout
par navigation inverse (FIND OWNER WITHIN SET).

Mais il reste des problèmes :
* L'accès est toujours NAVIGATIONNEL : le programmeur doit connaître le schéma
    des sets et écrire des boucles pour traverser les liens.
* Ajouter un nouveau type de lien exige de modifier le schéma et le code de
    navigation.
* Pas de langage déclaratif : on dit COMMENT chercher, pas CE QU'ON cherche.

## Le modèle relationnel et SQL

En 1970, Edgar F. Codd, un mathématicien britannique travaillant chez IBM, publie
un article qui va transformer le domaine : *A Relational Model of Data for Large
Shared Data Banks*. Sa proposition est radicale : abandonner complètement la
navigation. Au lieu de dire au système *comment* trouver les données (en
descendant dans un arbre ou en suivant des liens), on lui dit *ce qu'on cherche*,
et c'est le système qui détermine la meilleure façon de l'obtenir. Les données
sont organisées en tables (que Codd appelle « relations », d'où le nom), et les
requêtes s'expriment dans un langage déclaratif : SQL. SQL est d'ailleurs souvent
considéré comme l'exemple le plus abouti d'un langage de quatrième génération
(4GL) : un langage où le programmeur décrit ce qu'il veut obtenir, pas comment y
arriver.

{{% hint info %}}
**Les générations de langages de programmation**

La classification des langages en « générations » est une grille de lecture
historique qui a été très influente dans les années 80 et 90 :

- **1GL** : le code machine, des séquences de 0 et de 1 directement exécutées
  par le processeur.
- **2GL** : l'assembleur, qui remplace les codes binaires par des mnémoniques
  lisibles (`MOV`, `ADD`, `JMP`), mais reste lié à une architecture matérielle
  spécifique.
- **3GL** : les langages procéduraux de haut niveau (FORTRAN, C, COBOL, Java,
  Python), où le programmeur écrit des algorithmes qui décrivent *comment*
  résoudre un problème, de manière indépendante du matériel.
- **4GL** : les langages déclaratifs spécialisés, où le programmeur décrit *ce
  qu'il veut* sans spécifier la procédure. SQL en est l'exemple canonique : on
  écrit `SELECT ... WHERE ...` et c'est l'optimiseur de requêtes qui choisit le
  plan d'exécution.

À l'époque, certains prédisaient l'avènement d'un 5GL qui permettrait de
programmer en langage naturel. Cette vision ne s'est pas concrétisée sous la
forme imaginée, mais on peut noter que les LLMs modernes réalisent en quelque
sorte cette promesse, d'une manière que personne n'avait anticipée.
{{% /hint %}}

C'est un changement de paradigme au sens propre du terme. Le modèle hiérarchique
et le modèle en réseau demandaient au programmeur de connaître la structure
physique des données et d'écrire des boucles de navigation. Le modèle relationnel
sépare la structure logique de l'implémentation physique, une application directe
du principe d'*information hiding* de Parnas que nous avons vu dans la section
sur l'architecture.

{{< sql >}}

-- ============================================================
-- Modele relationnel -- illustration en SQL
-- ============================================================
--
-- Le modele relationnel (Codd, 1970) remplace les arbres
-- et les liens navigationnels par des TABLES et des REQUETES
-- DECLARATIVES : on decrit CE QU'ON CHERCHE, pas COMMENT
-- le trouver.
--
-- Meme scenario universitaire que les programmes Python
-- pour le modele hierarchique et le modele reseau.
-- ============================================================


-- ============================================================
-- 1. Definition du schema : des TABLES plates
-- ============================================================
-- Plus d'arbre, plus de sets/owners/members.
-- Chaque entite a sa propre table, et les relations
-- sont exprimees par des CLES ETRANGERES.

CREATE TABLE departement (
    code  VARCHAR(10) PRIMARY KEY,
    nom   VARCHAR(50) NOT NULL
);

CREATE TABLE professeur (
    id     INTEGER     PRIMARY KEY,
    nom    VARCHAR(50) NOT NULL,
    bureau VARCHAR(20),
    dept   VARCHAR(10) REFERENCES departement(code)
);

CREATE TABLE cours (
    sigle  VARCHAR(10) PRIMARY KEY,
    titre  VARCHAR(80) NOT NULL,
    dept   VARCHAR(10) REFERENCES departement(code)
);

CREATE TABLE etudiant (
    matricule VARCHAR(10) PRIMARY KEY,    -- UNE SEULE FOIS
    nom       VARCHAR(50) NOT NULL
);

-- La relation M:N (cours <-> etudiants) est une TABLE DE JOINTURE.
-- Ni duplication (modele hierarchique),
-- ni navigation par sets (modele reseau) :
-- juste une table avec deux cles etrangeres.

CREATE TABLE inscription (
    matricule VARCHAR(10) REFERENCES etudiant(matricule),
    sigle     VARCHAR(10) REFERENCES cours(sigle),
    PRIMARY KEY (matricule, sigle)
);

{{< /sql >}}

Remarquons la différence fondamentale : plus d'arbre, plus de sets. Chaque
entité a sa propre table, et les relations plusieurs-à-plusieurs passent par une
table de jointure. Le schéma est déclaré une fois, et le SGBD se charge de
l'appliquer. Ajoutons nos données :

{{< sql >}}

-- ============================================================
-- 2. Insertion des donnees
-- ============================================================

INSERT INTO departement VALUES ('INFO', 'Informatique');
INSERT INTO departement VALUES ('MATH', 'Mathematiques');

INSERT INTO professeur VALUES (1, 'Tremblay', 'PK-4150', 'INFO');
INSERT INTO professeur VALUES (2, 'Gagnon',   'PK-4920', 'INFO');
INSERT INTO professeur VALUES (3, 'Lavoie',   'PK-5230', 'MATH');

INSERT INTO cours VALUES ('INF3080', 'Bases de donnees',        'INFO');
INSERT INTO cours VALUES ('INF3105', 'Structures de donnees',   'INFO');
INSERT INTO cours VALUES ('MAT2080', 'Statistiques',            'MATH');

INSERT INTO etudiant VALUES ('TRAA01', 'Alice');
INSERT INTO etudiant VALUES ('MORB02', 'Bob');

INSERT INTO inscription VALUES ('TRAA01', 'INF3080');   -- Alice -> BD
INSERT INTO inscription VALUES ('TRAA01', 'INF3105');   -- Alice -> Algo
INSERT INTO inscription VALUES ('MORB02', 'INF3080');   -- Bob   -> BD
INSERT INTO inscription VALUES ('MORB02', 'MAT2080');   -- Bob   -> Stat

{{< /sql >}}

C'est dans les requêtes que la puissance du modèle relationnel se révèle. Chaque
requête décrit *ce qu'on veut*, pas *comment le trouver*. Reprenons les mêmes
questions que dans les modèles précédents, plus une nouvelle qui aurait été quasi
impossible à formuler avant :

{{< sql >}}

-- ============================================================
-- 3. Requetes declaratives -- CE QU'ON CHERCHE, pas COMMENT
-- ============================================================

-- Equivalent de naviguer(uqam, "Departement", "Cours")
-- du modele hierarchique, mais sans connaitre aucun chemin :

SELECT d.nom AS departement, c.sigle, c.titre
  FROM departement d
  JOIN cours c ON c.dept = d.code;

-- Equivalent de find_members("INSCRIPTION", bd)
-- du modele reseau -- etudiants inscrits a INF3080 :

SELECT e.matricule, e.nom
  FROM etudiant e
  JOIN inscription i ON i.matricule = e.matricule
 WHERE i.sigle = 'INF3080';


-- La question qui etait penible dans le modele hierarchique
-- et qui necessitait une navigation inverse dans le modele reseau
-- "A quels cours Alice est-elle inscrite ?"
-- s'ecrit naturellement :

SELECT c.sigle, c.titre
  FROM cours c
  JOIN inscription i ON i.sigle = c.sigle
 WHERE i.matricule = 'TRAA01';


-- Une question impossible a poser simplement dans les
-- modeles precedents -- "Quels etudiants partagent
-- au moins un cours avec Alice ?"

SELECT DISTINCT e.nom
  FROM etudiant e
  JOIN inscription i1 ON i1.matricule = e.matricule
  JOIN inscription i2 ON i2.sigle = i1.sigle
 WHERE i2.matricule = 'TRAA01'
   AND e.matricule != 'TRAA01';

{{< /sql >}}

### Les transactions

### Les ORMs (object relational mappers)

## La révolution NoSQL

### Key-Value Stores

### Document Stores

### Columnar Stores

### Graph Databases

## Les bases de données de séries temporelles

## Les bases de données vectorielles