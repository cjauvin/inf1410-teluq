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

Les exemples précédents montrent comment stocker et interroger des données, mais
ils passent sous silence un problème fondamental : que se passe-t-il quand
plusieurs opérations doivent réussir ou échouer ensemble ? Prenons un cas
concret : inscrire Alice à un cours implique au minimum deux vérifications (le
cours existe-t-il ? l'étudiante est-elle déjà inscrite ?) et une insertion. Si
le système tombe entre la vérification et l'insertion, ou si deux processus
tentent la même inscription simultanément, les données peuvent se retrouver dans
un état incohérent. Dans un programme simple, on gère ça avec des conditions et
des verrous. Dans un SGBD, on utilise une *transaction*.

Jim Gray, chercheur chez IBM puis chez Microsoft Research, a formalisé dans les
années 70 et 80 les propriétés fondamentales des transactions, un travail qui
lui a valu le prix Turing en 1998. Ces propriétés sont connues sous l'acronyme
ACID :

- **Atomicité** (*Atomicity*) : une transaction est tout ou rien. Soit toutes
  ses opérations réussissent (`COMMIT`), soit aucune n'a d'effet (`ROLLBACK`).
  Il n'y a pas d'état intermédiaire visible.
- **Cohérence** (*Consistency*) : une transaction amène la base d'un état valide
  à un autre état valide. Toutes les contraintes du schéma (clés primaires, clés
  étrangères, unicité) sont respectées à la fin de la transaction.
- **Isolation** (*Isolation*) : les transactions concurrentes ne se voient pas
  mutuellement. Tout se passe *comme si* elles s'exécutaient l'une après
  l'autre, même si en pratique le SGBD les entrelace pour la performance.
- **Durabilité** (*Durability*) : une fois qu'une transaction est validée
  (`COMMIT`), ses effets survivent aux pannes, même un crash immédiat du
  serveur.

Illustrons ces propriétés avec notre base universitaire. On tente d'inscrire
Alice à un cours auquel elle est déjà inscrite, ce qui viole la clé primaire de
la table d'inscription :

{{< sql >}}

-- ============================================================
-- Les transactions — atomicite en action
-- ============================================================

-- Tentative d'inscription qui viole une contrainte
BEGIN;

INSERT INTO inscription VALUES ('TRAA01', 'INF3080');
-- ERREUR : la paire (TRAA01, INF3080) existe deja (cle primaire)
-- La transaction est automatiquement annulee

ROLLBACK;

-- La base est intacte — c'est l'atomicite en action
SELECT * FROM inscription WHERE matricule = 'TRAA01';

{{< /sql >}}

Kleppmann consacre une partie importante de *Designing Data-Intensive
Applications* aux niveaux d'isolation, montrant que la propriété I d'ACID est en
réalité un spectre. L'isolation totale (*serializable*) est coûteuse en
performance, et la plupart des SGBD offrent par défaut un niveau plus faible
(*read committed* ou *repeatable read*) qui autorise certaines anomalies en
échange de la concurrence. Comprendre ces compromis est essentiel dès qu'un
système a plus d'un utilisateur simultané, ce qui est, en pratique, presque
toujours le cas.

### Les ORMs (object-relational mappers)

Le modèle relationnel organise les données en tables, avec des lignes et des
colonnes. Les langages de programmation, eux, manipulent des objets, des classes,
des dictionnaires. Entre les deux, il y a un décalage structurel que la
communauté a baptisé l'*impedance mismatch*, par analogie avec l'électronique :
deux systèmes qui ne « parlent pas le même langage » perdent de l'énergie à
l'interface. En pratique, cela se traduit par du code de conversion répétitif :
transformer les lignes d'un résultat SQL en objets Python, et inversement,
convertir des objets en requêtes `INSERT` ou `UPDATE`.

Les ORMs (*Object-Relational Mappers*) tentent de résoudre ce problème en créant
une correspondance automatique entre les classes d'un langage et les tables d'une
base de données. L'idée a émergé progressivement dans les années 90, mais c'est
avec Hibernate (Java, 2001) puis ActiveRecord (Ruby on Rails, 2004) qu'elle
s'est imposée dans la pratique courante. En Python, SQLAlchemy, créé par Mike
Bayer en 2006, est devenu la référence. Il offre deux niveaux d'abstraction : un
*Core* qui fournit une API Python pour construire des requêtes SQL sans écrire de
SQL brut, et un ORM complet qui permet de définir des classes Python mappées
directement sur des tables.

```python
from sqlalchemy import create_engine, Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

# Table de jointure pour la relation M:N
inscription = Table('inscription', Base.metadata,
    Column('matricule', String, ForeignKey('etudiant.matricule'), primary_key=True),
    Column('sigle', String, ForeignKey('cours.sigle'), primary_key=True),
)

class Etudiant(Base):
    __tablename__ = 'etudiant'
    matricule = Column(String, primary_key=True)
    nom       = Column(String, nullable=False)
    cours     = relationship('Cours', secondary=inscription, back_populates='etudiants')

class Cours(Base):
    __tablename__ = 'cours'
    sigle     = Column(String, primary_key=True)
    titre     = Column(String, nullable=False)
    etudiants = relationship('Etudiant', secondary=inscription, back_populates='cours')

# Utilisation — on manipule des objets Python, pas du SQL
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

with Session(engine) as session:
    alice = Etudiant(matricule='TRAA01', nom='Alice')
    bd    = Cours(sigle='INF3080', titre='Bases de données')
    algo  = Cours(sigle='INF3105', titre='Structures de données')

    alice.cours.append(bd)
    alice.cours.append(algo)

    session.add(alice)
    session.commit()

    # La question « à quels cours Alice est-elle inscrite ? »
    # s'écrit comme en Python natif :
    for cours in alice.cours:
        print(f"  {cours.sigle} — {cours.titre}")
```

Le contraste avec le SQL brut est frappant : on ne voit plus aucune requête SQL,
et les relations entre entités se manipulent comme des listes Python ordinaires.
Mais cette abstraction a un coût. L'ORM génère du SQL en coulisse, et ce SQL
n'est pas toujours celui qu'un développeur expérimenté écrirait. Le problème
classique est le *N+1 query* : charger une liste d'étudiants puis accéder aux
cours de chacun peut déclencher une requête par étudiant, au lieu d'une seule
jointure. C'est un compromis récurrent en génie logiciel : l'abstraction
simplifie le cas courant, mais elle peut masquer des inefficacités que seule la
compréhension de la couche sous-jacente permet de diagnostiquer.

## La révolution NoSQL

Le modèle relationnel a dominé le paysage des bases de données pendant plus de
trente ans, et il reste aujourd'hui le choix par défaut pour une majorité
d'applications. Mais à partir du milieu des années 2000, un ensemble de
pressions convergentes a commencé à remettre en question son hégémonie. Les
géants du web (Google, Amazon, Facebook) faisaient face à des volumes de données
et des niveaux de trafic que les bases relationnelles traditionnelles peinaient à
absorber, même sur du matériel coûteux. Parallèlement, beaucoup de développeurs
trouvaient que le modèle relationnel imposait une rigidité excessive pour des
données dont la structure évoluait rapidement ou ne se prêtait pas naturellement
aux tables.

Le terme « NoSQL » a été popularisé en 2009, lors d'un meetup organisé à San
Francisco par Johan Oskarsson. Le nom est un peu trompeur : il ne signifie pas
« pas de SQL » mais plutôt « Not Only SQL », l'idée étant que le modèle
relationnel n'est pas la seule réponse à tous les problèmes de stockage.
Kleppmann, dans *Designing Data-Intensive Applications*, montre que derrière ce
label se cachent des motivations très différentes : le besoin de scalabilité
horizontale (répartir les données sur plusieurs machines), le désir de schémas
plus flexibles, ou la recherche de modèles de données mieux adaptés à certains
cas d'usage.

En pratique, le mouvement NoSQL a donné naissance à plusieurs familles de bases
de données, chacune optimisée pour un type de problème particulier :

- Les bases **clé-valeur** (Redis, Memcached) : le modèle le plus simple, un
  dictionnaire distribué. Idéal pour le caching et les sessions.
- Les bases **orientées documents** (MongoDB, CouchDB) : chaque enregistrement est un
  document (typiquement JSON) avec une structure libre. Naturel pour des données
  hétérogènes ou des schémas qui évoluent vite.
- Les bases **orientées colonnes** (Cassandra, HBase) : optimisées pour
  l'écriture massive et les requêtes analytiques sur de grands volumes. Inspirées
  de Bigtable de Google (2006).
- Les bases **orientées graphes** (Neo4j, Amazon Neptune) : conçues pour les
  données fortement interconnectées, où les relations entre entités sont aussi
  importantes que les entités elles-mêmes.

Ce qui est frappant, comme le note Kleppmann, c'est que certains de ces modèles
rappellent des paradigmes qu'on croyait dépassés. Les bases orientées documents
stockent des données hiérarchiques (des arbres JSON), comme le faisait IMS en
1966. Les bases orientées graphes modélisent des réseaux de liens, comme le
faisait CODASYL en 1969. L'histoire ne se répète pas, mais elle rime.

### Les bases clé-valeur

La base clé-valeur est le modèle NoSQL le plus simple : elle associe une clé
unique à une valeur opaque, exactement comme un dictionnaire Python ou une table
de hachage. Le système ne connaît pas la structure de la valeur ; il sait
seulement la stocker, la retrouver et la supprimer par sa clé. Cette simplicité
radicale est aussi sa force : en renonçant aux jointures, aux schémas et aux
requêtes complexes, une base clé-valeur peut offrir des performances et une
scalabilité que le modèle relationnel atteint difficilement.

L'exemple le plus emblématique est Redis, créé en 2009 par Salvatore Sanfilippo.
Redis stocke toutes ses données en mémoire vive, ce qui lui permet des temps de
réponse de l'ordre de la microseconde. Mais il va au-delà du simple
dictionnaire : il supporte des structures de données riches (listes, ensembles,
hachages, compteurs), ce qui en fait un outil polyvalent utilisé aussi bien
comme cache que comme file de messages ou comme base de sessions utilisateur.

Le cas d'usage le plus courant des bases clé-valeur est le *caching* : stocker
temporairement des résultats coûteux à calculer pour éviter de les recalculer à
chaque requête. Le principe est simple, mais le défi principal est
l'**invalidation** : s'assurer que le cache reste cohérent avec la source de
vérité. Les stratégies courantes incluent le TTL (*time-to-live*, expiration
après un délai fixe), le *write-through* (mise à jour simultanée du cache et de
la source) et le *cache-aside* (le code vérifie d'abord le cache, puis
interroge la source en cas d'absence). Python offre `functools.lru_cache`, un
décorateur qui implémente un cache LRU (*Least Recently Used*) directement sur
les appels de fonction :

{{< pyodide >}}
import functools
import time

# --- Cache LRU intégré à Python ---

@functools.lru_cache(maxsize=128)
def requete_couteuse(utilisateur_id):
    """Simule une requête lente vers une base de données."""
    print(f"  [BD] Requête pour utilisateur {utilisateur_id}...")
    time.sleep(0.01)  # Simule la latence
    return {"id": utilisateur_id, "nom": f"Utilisateur_{utilisateur_id}", "score": utilisateur_id * 17 % 100}

# --- Démonstration : avec et sans cache ---

print("=== Premier appel (cache vide — miss) ===\n")
for uid in [42, 7, 42, 13, 7, 42]:
    t0 = time.time()
    resultat = requete_couteuse(uid)
    duree = (time.time() - t0) * 1000
    source = "MISS → BD" if duree > 5 else "HIT  → cache"
    print(f"  utilisateur {uid:2d} → {resultat['nom']:16s} (score={resultat['score']:2d})  [{source}]")

print(f"\n=== Statistiques du cache ===\n")
info = requete_couteuse.cache_info()
print(f"  Hits   : {info.hits}")
print(f"  Misses : {info.misses}")
print(f"  Taille : {info.currsize}/{info.maxsize}")
print(f"  Taux   : {info.hits / (info.hits + info.misses) * 100:.0f}%")

# --- Invalidation manuelle ---

print(f"\n=== Invalidation du cache ===\n")
requete_couteuse.cache_clear()
print(f"  Cache vidé. Nouvelle taille : {requete_couteuse.cache_info().currsize}")
{{< /pyodide >}}

### Les bases orientées documents

Les bases orientées documents poussent l'idée un cran plus loin que les bases
clé-valeur : la valeur n'est plus opaque, c'est un document structuré
(généralement en JSON) que la base sait interroger. On peut chercher par
n'importe quel champ à l'intérieur du document, sans avoir besoin de connaître
sa structure à l'avance. C'est un modèle naturel pour des données hétérogènes :
un catalogue de produits où chaque catégorie a des attributs différents, des
profils utilisateur dont les champs varient, des événements avec des charges
utiles variables.

MongoDB, créé en 2009 par Dwight Merriman et Eliot Horowitz, est devenu le
représentant le plus connu de cette famille. Son modèle est celui de
« collections » de documents JSON (techniquement BSON, une variante binaire).
Là où une base relationnelle aurait besoin de plusieurs tables liées par des clés
étrangères, MongoDB permet d'imbriquer directement les données dans un seul
document :

```json
{
  "matricule": "TRAA01",
  "nom": "Alice",
  "cours": [
    {"sigle": "INF3080", "titre": "Bases de données", "session": "H2026"},
    {"sigle": "INF3105", "titre": "Structures de données", "session": "H2026"}
  ]
}
```

On retrouve ici une structure d'arbre, exactement comme dans le modèle
hiérarchique d'IMS. L'avantage est la localité des données : tout ce qui
concerne Alice est au même endroit, ce qui rend les lectures rapides. Le
désavantage est le même qu'en 1966 : si Bob et Alice partagent le même cours,
l'information du cours est dupliquée. Le modèle orienté documents fait le pari
que cette duplication est acceptable pour la plupart des cas d'usage, en échange
de la simplicité et de la performance en lecture.

Kleppmann souligne que le choix entre un modèle relationnel et un modèle orienté
documents dépend fondamentalement de la nature des relations dans les données.
Si les données sont principalement des agrégats autonomes (un utilisateur avec
ses préférences, une commande avec ses lignes), le modèle orienté documents est
naturel. Si les données sont fortement interconnectées (des relations
plusieurs-à-plusieurs omniprésentes), le modèle relationnel reste plus adapté.

### Les bases orientées colonnes

Les bases de données que l'on a vues jusqu'ici (relationnelles, clé-valeur,
orientées documents) sont optimisées pour le traitement transactionnel : insérer
une commande, mettre à jour un profil, lire un enregistrement par sa clé. On
parle de charges de travail OLTP (*Online Transaction Processing*). Mais il
existe une autre catégorie de besoins, fondamentalement différente : l'analyse.
« Quel est le chiffre d'affaires par région et par trimestre ? », « Quels
produits ont vu leurs ventes baisser de plus de 10 % ce mois-ci ? ». Ce sont
des requêtes OLAP (*Online Analytical Processing*), qui balaient des millions de
lignes mais ne consultent que quelques colonnes.

Dans une base relationnelle classique, les données sont stockées ligne par
ligne : toutes les colonnes d'un enregistrement sont physiquement côte à côte
sur le disque. C'est idéal pour lire ou écrire un enregistrement complet, mais
inefficace pour une requête analytique qui ne s'intéresse qu'à deux colonnes sur
vingt. L'idée du stockage orienté colonnes est d'inverser l'organisation : on
stocke ensemble toutes les valeurs d'une même colonne. Pour une requête « somme
des montants par région », le moteur ne lit que les colonnes `region` et
`montant`, en ignorant complètement toutes les autres. En plus de réduire les
lectures disque, ce regroupement permet une compression spectaculaire, car les
valeurs d'une même colonne sont souvent similaires (beaucoup de répétitions dans
une colonne `region` ou `pays`).

L'article fondateur est le papier de Google sur Bigtable (2006), suivi de
Dremel (2010) qui a inspiré BigQuery. Dans le monde open source, Apache
Cassandra (2008, initialement développé chez Facebook) et HBase (2007, une
implémentation open source de Bigtable) ont été les premiers systèmes orientés
colonnes à grande échelle. Aujourd'hui, des moteurs comme ClickHouse, Apache
Parquet (un format de fichier orienté colonnes) et DuckDB rendent cette
approche accessible même pour des analyses locales.

Cette distinction OLTP / OLAP a donné naissance à une architecture classique :
le *data warehouse* (entrepôt de données). Les données transactionnelles vivent
dans une base OLTP (PostgreSQL, MySQL), puis sont périodiquement copiées et
transformées vers un entrepôt orienté colonnes via un processus appelé ETL
(*Extract, Transform, Load*). Les analystes interrogent l'entrepôt sans risquer
de ralentir le système transactionnel. C'est une application directe du principe
de séparation des préoccupations : les deux charges de travail ont des besoins
si différents qu'il vaut mieux les servir avec des systèmes distincts.

En Python, on peut illustrer la différence entre les deux approches de
stockage :

{{< pyodide >}}
import random

# --- Génération de données de ventes ---

random.seed(42)
regions = ["Montréal", "Québec", "Sherbrooke", "Gatineau"]
produits = ["Café", "Thé", "Jus", "Eau"]
trimestres = ["T1", "T2", "T3", "T4"]

N = 10_000  # nombre de transactions

# Stockage en LIGNES (style OLTP) : chaque ligne est un dict
lignes = [
    {
        "region": random.choice(regions),
        "produit": random.choice(produits),
        "trimestre": random.choice(trimestres),
        "montant": round(random.uniform(5.0, 50.0), 2),
    }
    for _ in range(N)
]

# Stockage en COLONNES (style OLAP) : chaque colonne est une liste
colonnes = {
    "region":     [r["region"] for r in lignes],
    "produit":    [r["produit"] for r in lignes],
    "trimestre":  [r["trimestre"] for r in lignes],
    "montant":    [r["montant"] for r in lignes],
}

print(f"=== {N} transactions générées ===\n")

# --- Requête analytique : ventes par région ---
# En mode colonnes, on ne touche que les colonnes nécessaires

def ventes_par_region_lignes(lignes):
    """Agrégation en parcourant les lignes (OLTP-style)."""
    totaux = {}
    for ligne in lignes:
        r = ligne["region"]        # accède à TOUTE la ligne
        totaux[r] = totaux.get(r, 0) + ligne["montant"]
    return totaux

def ventes_par_region_colonnes(colonnes):
    """Agrégation en parcourant les colonnes (OLAP-style)."""
    totaux = {}
    regions = colonnes["region"]   # ne lit QUE cette colonne
    montants = colonnes["montant"] # et celle-ci
    for i in range(len(regions)):
        r = regions[i]
        totaux[r] = totaux.get(r, 0) + montants[i]
    return totaux

# Comparer les résultats
res_lignes = ventes_par_region_lignes(lignes)
res_colonnes = ventes_par_region_colonnes(colonnes)

print("Ventes totales par région :\n")
for region in sorted(res_colonnes):
    print(f"  {region:12s} : {res_colonnes[region]:10,.2f} $")

print(f"\n  Total       : {sum(res_colonnes.values()):10,.2f} $")

# --- Requête multidimensionnelle (cube OLAP simplifié) ---

print(f"\n=== Cube OLAP : ventes par région × trimestre ===\n")

cube = {}
for i in range(N):
    cle = (colonnes["region"][i], colonnes["trimestre"][i])
    cube[cle] = cube.get(cle, 0) + colonnes["montant"][i]

# Affichage en tableau croisé
print(f"  {'':12s}", end="")
for t in trimestres:
    print(f"  {t:>10s}", end="")
print()

for region in sorted(regions):
    print(f"  {region:12s}", end="")
    for t in trimestres:
        val = cube.get((region, t), 0)
        print(f"  {val:10,.2f}", end="")
    print()
{{< /pyodide >}}

### Les bases orientées graphes

Certaines données sont fondamentalement des réseaux de relations. Un réseau
social, une carte routière, une ontologie, les dépendances entre les composants
d'un système logiciel. Dans ces cas, ce qui importe n'est pas tant les entités
elles-mêmes que les connexions entre elles. Les requêtes typiques sont des
traversées : « Qui sont les amis des amis d'Alice ? », « Quel est le plus court
chemin entre Montréal et Vancouver ? », « Quels services dépendent
transitoirement de ce composant ? ». En SQL, ces requêtes se traduisent par des
cascades de JOIN qui deviennent rapidement illisibles dès que la profondeur de
traversée augmente. Les bases orientées graphes sont conçues précisément pour
ce type de navigation.

Le modèle réseau CODASYL des années 1970 permettait exactement ce genre de
navigation, mais avec une rigidité qui l'a condamné : il fallait déclarer à
l'avance tous les types de relations et naviguer de manière procédurale, pointeur
par pointeur. Les bases orientées graphes modernes reprennent l'intuition de
CODASYL (les données forment un réseau navigable) mais avec la flexibilité du
monde NoSQL : on peut ajouter de nouveaux types de nœuds et de relations sans
modifier un schéma global, et les requêtes sont déclaratives plutôt que
procédurales. Neo4j (2007, Emil Eifrem et Johan Svensson) est la plus connue.
Son langage de requête, Cypher, est au graphe ce que SQL est aux tables.

En Python, un graphe peut se représenter simplement comme un dictionnaire
d'adjacence. Voici un exemple de traversée en largeur (*breadth-first search*,
BFS) qui trouve tous les nœuds accessibles depuis un point de départ :

{{< pyodide >}}
from collections import deque

# Graphe d'adjacence : qui connaît qui ?
graphe = {
    "Alice":   ["Bob", "Charlie"],
    "Bob":     ["Alice", "Diana"],
    "Charlie": ["Alice", "Eve"],
    "Diana":   ["Bob"],
    "Eve":     ["Charlie", "Frank"],
    "Frank":   ["Eve"],
}

def bfs(graphe, depart, profondeur_max):
    """Trouve tous les nœuds accessibles en au plus `profondeur_max` sauts."""
    visites = {depart}
    file = deque([(depart, 0)])
    resultats = []

    while file:
        noeud, profondeur = file.popleft()
        if profondeur > 0:
            resultats.append((noeud, profondeur))
        if profondeur < profondeur_max:
            for voisin in graphe.get(noeud, []):
                if voisin not in visites:
                    visites.add(voisin)
                    file.append((voisin, profondeur + 1))

    return resultats

# Amis et amis d'amis d'Alice (profondeur 2)
print("Réseau d'Alice (jusqu'à 2 sauts) :\n")
for personne, distance in bfs(graphe, "Alice", 2):
    relation = "ami direct" if distance == 1 else "ami d'ami"
    print(f"  {personne:10s} ({relation})")
{{< /pyodide >}}

Cypher, le langage de requête de Neo4j, rend la structure du graphe visible
directement dans la syntaxe. Les nœuds sont représentés par des parenthèses et
les relations par des flèches, ce qui donne des requêtes dont la forme épouse
celle des données. Reprenons notre exemple universitaire pour comparer avec les
requêtes SQL vues plus haut :

```cypher
// Créer des nœuds et des relations
CREATE (alice:Etudiant {matricule: "TRAA01", nom: "Alice"})
CREATE (bob:Etudiant {matricule: "MORB02", nom: "Bob"})
CREATE (bd:Cours {sigle: "INF3080", titre: "Bases de données"})
CREATE (algo:Cours {sigle: "INF3105", titre: "Structures de données"})

CREATE (alice)-[:INSCRIT_A]->(bd)
CREATE (alice)-[:INSCRIT_A]->(algo)
CREATE (bob)-[:INSCRIT_A]->(bd)

// À quels cours Alice est-elle inscrite ?
MATCH (e:Etudiant {nom: "Alice"})-[:INSCRIT_A]->(c:Cours)
RETURN c.sigle, c.titre

// Quels étudiants partagent au moins un cours avec Alice ?
MATCH (alice:Etudiant {nom: "Alice"})-[:INSCRIT_A]->(c)<-[:INSCRIT_A]-(autre)
RETURN DISTINCT autre.nom
```

La dernière requête est particulièrement révélatrice. En SQL, trouver les
étudiants qui partagent un cours avec Alice nécessitait deux jointures sur la
table `inscription` et une condition d'exclusion. En Cypher, le motif
`(alice)-[:INSCRIT_A]->(c)<-[:INSCRIT_A]-(autre)` exprime la même idée en une
ligne, et la structure de la requête dessine littéralement le chemin qu'on
cherche dans le graphe. C'est cette correspondance entre la forme de la requête
et la forme des données qui fait la force des langages de graphe.

## Les bases de données de séries temporelles

Les séries temporelles (*time series*) sont des séquences de points de données
indexés par le temps : température toutes les minutes, cours boursier toutes les
secondes, nombre de requêtes par heure sur un serveur, fréquence cardiaque d'un
patient. Ce type de données est omniprésent dans la surveillance
d'infrastructure (monitoring), l'Internet des objets (IoT), la finance et les
sciences. Le concept de série temporelle est ancien, il remonte aux travaux
fondateurs de l'économétrie et des statistiques dans les années 1920 (Yule,
Slutsky). Mais les bases de données spécialisées pour ce type de données sont
récentes : Prometheus (2012, développé chez SoundCloud par Matt Proud et Julius
Volz) a montré que le monitoring d'infrastructure nécessitait un modèle de
données dédié, suivi d'InfluxDB (2013) et de TimescaleDB (2017, une extension
de PostgreSQL).

Les bases relationnelles classiques peuvent stocker des séries temporelles, mais
elles ne sont pas optimisées pour leurs particularités. Les données arrivent
principalement en mode *append* (on ajoute sans modifier), les requêtes portent
presque toujours sur des intervalles de temps, et le volume peut être
considérable (des millions de points par capteur par jour). Les bases
spécialisées exploitent ces propriétés pour offrir une compression agressive
(les horodatages successifs se compressent très bien car ils sont régulièrement
espacés), des fonctions d'agrégation temporelle natives (*downsample*, *rollup*)
et des politiques de rétention automatiques (supprimer les données de plus de 90
jours, par exemple).

En Python, on peut illustrer les opérations fondamentales sur les séries
temporelles (rééchantillonnage, moyenne mobile, détection d'anomalies) avec les
structures de données de base :

{{< pyodide >}}
import random
import math
from datetime import datetime, timedelta

# --- Génération d'une série temporelle : température d'un capteur IoT ---

random.seed(42)
debut = datetime(2025, 6, 1, 0, 0)
n_points = 288  # 1 point toutes les 5 min × 24h = 288

serie = []
for i in range(n_points):
    t = debut + timedelta(minutes=5 * i)
    heure = t.hour + t.minute / 60
    # Température sinusoïdale (cycle jour/nuit) + bruit
    base = 20 + 8 * math.sin((heure - 6) * math.pi / 12)
    bruit = random.gauss(0, 1.5)
    # Injection d'une anomalie à 14h30
    anomalie = 15 if (t.hour == 14 and t.minute == 30) else 0
    serie.append({"temps": t, "valeur": round(base + bruit + anomalie, 2)})

print(f"=== Série temporelle : {n_points} points (5 min) sur 24h ===\n")
print(f"  Début : {serie[0]['temps']}")
print(f"  Fin   : {serie[-1]['temps']}")
print(f"  Min   : {min(s['valeur'] for s in serie):.1f} °C")
print(f"  Max   : {max(s['valeur'] for s in serie):.1f} °C")

# --- Rééchantillonnage (downsample) : moyenne horaire ---

print(f"\n=== Downsample : moyenne par heure ===\n")
par_heure = {}
for s in serie:
    h = s["temps"].hour
    par_heure.setdefault(h, []).append(s["valeur"])

for h in sorted(par_heure):
    vals = par_heure[h]
    moy = sum(vals) / len(vals)
    print(f"  {h:02d}h : {moy:5.1f} °C  ({len(vals)} points)")

# --- Moyenne mobile (rolling average) ---

def moyenne_mobile(serie, fenetre):
    """Calcule la moyenne mobile sur une fenêtre de N points."""
    resultats = []
    for i in range(len(serie)):
        debut_f = max(0, i - fenetre + 1)
        vals = [serie[j]["valeur"] for j in range(debut_f, i + 1)]
        resultats.append({
            "temps": serie[i]["temps"],
            "brut": serie[i]["valeur"],
            "lissé": round(sum(vals) / len(vals), 2),
        })
    return resultats

lisse = moyenne_mobile(serie, fenetre=12)  # fenêtre d'1 heure

# --- Détection d'anomalies (seuil sur l'écart à la moyenne mobile) ---

print(f"\n=== Détection d'anomalies (écart > 10 °C vs moyenne mobile) ===\n")
anomalies = []
for pt in lisse:
    ecart = abs(pt["brut"] - pt["lissé"])
    if ecart > 10:
        anomalies.append(pt)
        print(f"  ⚠ {pt['temps'].strftime('%H:%M')} : brut={pt['brut']:.1f} °C, "
              f"lissé={pt['lissé']:.1f} °C, écart={ecart:.1f} °C")

if not anomalies:
    print("  Aucune anomalie détectée.")
else:
    print(f"\n  {len(anomalies)} anomalie(s) détectée(s).")
{{< /pyodide >}}

On retrouvera les séries temporelles dans le module 5, lorsqu'on abordera
l'observabilité et le monitoring. Les métriques collectées par des outils comme
Prometheus et Grafana sont précisément des séries temporelles, et les concepts
de rétention, d'agrégation et d'alerting sur seuil sont au cœur de la
surveillance d'un système en production.

## Les bases de données vectorielles

Les bases de données vectorielles sont un paradigme de stockage et de recherche
conçu pour manipuler des *vecteurs d'embedding*, des représentations numériques
de haute dimension (typiquement 256 à 4096 dimensions) produites par des modèles
d'apprentissage automatique pour encoder le « sens » d'un texte, d'une image,
d'un son ou de toute autre donnée. Le concept de *word embedding* remonte à
Word2Vec (Mikolov et al., Google, 2013), qui a montré qu'on pouvait représenter
des mots comme des vecteurs dans un espace où les relations sémantiques
deviennent des opérations géométriques (le fameux exemple : « roi » - « homme »
\+ « femme » ≈ « reine »). Mais c'est l'explosion des grands modèles de langage
en 2022-2023 qui a créé un besoin massif de bases vectorielles dédiées, car le
pattern RAG (*Retrieval-Augmented Generation*), qui consiste à chercher des
documents pertinents pour enrichir le contexte d'un LLM, repose entièrement sur
la recherche vectorielle.

L'opération fondamentale est la recherche par similarité : plutôt que de
chercher une correspondance exacte (comme en SQL avec `WHERE nom = 'Alice'`), on
cherche les vecteurs les plus *proches* d'un vecteur requête selon une mesure de
distance (cosinus, euclidienne, produit scalaire). C'est cette capacité qui rend
possible la recherche sémantique (trouver des documents qui *parlent* de la même
chose, même avec des mots différents), les systèmes de recommandation, et le RAG
qui alimente les assistants IA modernes.
[Pinecone](https://www.pinecone.io/) (2019),
[Weaviate](https://weaviate.io/), [Milvus](https://milvus.io/) et
[Qdrant](https://qdrant.tech/) sont des bases vectorielles spécialisées, tandis
que [pgvector](https://github.com/pgvector/pgvector) ajoute cette capacité à
PostgreSQL. Le défi technique principal est la recherche approximative des plus
proches voisins (*ANN, Approximate Nearest Neighbors*), car une recherche exacte
en haute dimension est prohibitivement lente. Des algorithmes comme HNSW
(*Hierarchical Navigable Small World*) permettent des recherches quasi
instantanées même sur des millions de vecteurs, au prix d'une approximation
contrôlée.

En Python, on peut illustrer les concepts fondamentaux (embedding, distance
cosinus, recherche par similarité) avec des vecteurs simplifiés :

{{< pyodide >}}
import math
import random

# --- Similarité cosinus ---

def similarite_cosinus(a, b):
    """Mesure la similarité entre deux vecteurs (1 = identiques, 0 = orthogonaux)."""
    produit = sum(x * y for x, y in zip(a, b))
    norme_a = math.sqrt(sum(x * x for x in a))
    norme_b = math.sqrt(sum(x * x for x in b))
    if norme_a == 0 or norme_b == 0:
        return 0.0
    return produit / (norme_a * norme_b)

# --- Simulacre d'embedding : vecteur thématique simplifié ---
# Dimensions : [informatique, cuisine, sport, musique, science]

def embedding(themes):
    """Crée un vecteur d'embedding simplifié à partir de scores thématiques."""
    random.seed(hash(tuple(themes)) % 2**32)
    # Ajouter du bruit pour simuler un vrai modèle
    return [v + random.gauss(0, 0.1) for v in themes]

# --- Base de données vectorielle minimale ---

class BaseVectorielle:
    def __init__(self):
        self.documents = []  # [{"id": ..., "texte": ..., "vecteur": [...]}]

    def inserer(self, id_doc, texte, vecteur):
        self.documents.append({"id": id_doc, "texte": texte, "vecteur": vecteur})

    def rechercher(self, vecteur_requete, k=3):
        """Recherche les k documents les plus similaires (force brute)."""
        scores = []
        for doc in self.documents:
            sim = similarite_cosinus(vecteur_requete, doc["vecteur"])
            scores.append((doc, sim))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]

# --- Construction de la base ---

db = BaseVectorielle()

corpus = [
    ("doc1", "Introduction à Python et aux algorithmes",         [0.9, 0.0, 0.0, 0.0, 0.3]),
    ("doc2", "Recette de gâteau au chocolat",                    [0.0, 0.9, 0.0, 0.0, 0.0]),
    ("doc3", "Les réseaux de neurones en intelligence artificielle", [0.8, 0.0, 0.0, 0.0, 0.9]),
    ("doc4", "Entraînement de marathon et nutrition sportive",   [0.0, 0.3, 0.9, 0.0, 0.1]),
    ("doc5", "Théorie musicale et composition assistée par IA",  [0.4, 0.0, 0.0, 0.9, 0.2]),
    ("doc6", "Analyse de données avec pandas et matplotlib",     [0.8, 0.0, 0.0, 0.0, 0.5]),
    ("doc7", "Cuisine moléculaire et science des aliments",      [0.0, 0.8, 0.0, 0.0, 0.7]),
    ("doc8", "Statistiques sportives et apprentissage automatique", [0.6, 0.0, 0.7, 0.0, 0.5]),
]

print("=== Insertion des documents ===\n")
for id_doc, texte, themes in corpus:
    vecteur = embedding(themes)
    db.inserer(id_doc, texte, vecteur)
    print(f"  {id_doc}: {texte[:50]}...")

# --- Recherches par similarité ---

requetes = [
    ("Programmation et science",     [0.8, 0.0, 0.0, 0.0, 0.7]),
    ("Recettes et alimentation",     [0.0, 0.9, 0.0, 0.0, 0.1]),
    ("Sport et données",             [0.4, 0.0, 0.8, 0.0, 0.3]),
]

for description, themes_requete in requetes:
    vecteur_q = embedding(themes_requete)
    resultats = db.rechercher(vecteur_q, k=3)

    print(f"\n=== Recherche : '{description}' ===\n")
    for doc, score in resultats:
        print(f"  {score:.3f}  {doc['id']}: {doc['texte'][:55]}...")
{{< /pyodide >}}

On retrouvera les bases vectorielles et le RAG dans le module 6, lorsqu'on
abordera le développement assisté par l'IA et l'écosystème des grands modèles de
langage. Les embeddings et la recherche par similarité sont devenus des briques
fondamentales de l'infrastructure logicielle moderne, au même titre que les
bases relationnelles l'étaient une génération plus tôt.