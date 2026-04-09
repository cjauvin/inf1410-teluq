---
title: "La représentation des données"
slug: "représentation"
weight: 10
---

# La représentation des données

## Données vs information vs connaissances

C'est une distinction classique et fondamentale en sciences de l'information.
Martin Kleppmann consacre une partie importante de *Designing Data-Intensive
Applications* à ces questions de représentation, en montrant que le choix d'un
format d'encodage et d'un schéma sont parmi les premières décisions
architecturales qu'on prend quand on conçoit un système distribué. Voici
comment ces trois niveaux s'articulent&nbsp;:

Les **données** sont des **faits** bruts, sans contexte ni interprétation. Ce sont des
symboles, des chiffres, des mesures isolées. Par exemple&nbsp;: « 38,5 », « Montréal
», « 2026-02-27 ». En soi, une donnée ne veut rien dire, elle doit être mise en
relation avec autre chose.

L'**information** émerge lorsqu'on organise et contextualise des données pour leur
donner un sens. « La température du patient était de 38,5 °C ce matin » est de
l'information&nbsp;: on sait maintenant quoi, où, quand. L'information répond à une
question et peut être communiquée de manière structurée.

La **connaissance**, elle, naît quand un être humain (ou un système) intègre
l'information à son expérience, ses modèles mentaux et son jugement. Par
exemple, un médecin qui lit cette température sait que c'est une fièvre légère,
qu'il faut surveiller l'évolution, et quelles causes sont probables selon le
contexte clinique. La connaissance permet d'interpréter, de décider et d'agir.

On résume souvent cette hiérarchie ainsi — parfois appelée la [pyramide
DICS](https://fr.wikipedia.org/wiki/Pyramide_DICS) (Données → Information →
Connaissances → Sagesse)&nbsp;:

* Donnée → « le quoi brut » (symboles sans contexte)
* Information → « le quoi structuré » (données + contexte + sens)
* Connaissance → « le comment et le pourquoi » (information + expérience +
  jugement)

La sagesse (wisdom), parfois ajoutée au sommet, serait la capacité de porter un
jugement éclairé sur quand et pourquoi appliquer ses connaissances.

{{< image src="pyramide-dics.png" alt="Pyramide DICS" title="Pyramide DICS" loading="lazy" >}}

## L'encodage et la sérialisation (et leur inverse)

Un ordinateur ne manipule que des bits (0 et 1). Tout le reste (lettres,
nombres, images, structures de données) doit être encodé, c'est-à-dire traduit
en séquences de bits selon des règles convenues. L'encodage est donc un contrat
de représentation entre celui qui écrit et celui qui lit. On peut distinguer
plusieurs couches d'encodage, chacune répondant à un besoin différent.

### L'encodage des nombres&nbsp;: le binaire

C'est la couche la plus basse. Un entier comme 42 se représente en base 2&nbsp;:
`00101010`.

{{< pyodide >}}

n = 42
print(f"{n:08b}")

{{< /pyodide >}}

Pour les nombres négatifs, on utilise le [complément à
deux](https://fr.wikipedia.org/wiki/Compl%C3%A9ment_%C3%A0_deux). Pour les
nombres à virgule, la norme IEEE 754 définit comment encoder le signe,
l'exposant et la mantisse en 32 ou 64 bits. L'essentiel ici&nbsp;: le même paquet de
bits peut signifier des choses complètement différentes selon l'interprétation
qu'on en fait. `01000001` peut être l'entier 65, le caractère `A`, ou une partie
d'un nombre flottant, tout dépend du contexte d'interprétation.

### L'encodage des caractères&nbsp;: ASCII, Latin-1, UTF-8…

Comment représenter du texte ? Il faut une table de correspondance entre des
caractères et des nombres.

* ASCII (1963)&nbsp;: 7 bits, 128 caractères. Suffisant pour l'anglais, mais pas pour
  "é", "ñ" ou "漢".
* Latin-1 / ISO 8859-1&nbsp;: 8 bits, 256 caractères. Couvre les langues d'Europe
  occidentale, mais chaque région du monde avait sa propre table — d'où des
  problèmes d'interopérabilité constants.
* Unicode&nbsp;: un répertoire universel qui attribue un code point unique à chaque
  caractère de toutes les écritures (ex.&nbsp;: `U+00E9` = "é", `U+4E16` = "世").
  Mais Unicode n'est pas un encodage en soi, c'est un catalogue.
* UTF-8&nbsp;: l'encodage le plus répandu d'Unicode. Il est à longueur variable — un
  caractère ASCII tient sur 1 octet, un accent sur 2, un idéogramme sur 3,
  certains emojis sur 4. Son génie est d'être rétrocompatible avec ASCII&nbsp;: tout
  fichier ASCII est déjà du UTF-8 valide.

La confusion classique qu'on retrouve partout&nbsp;: voir des `Ã©` au lieu de `é`,
c'est presque toujours un fichier UTF-8 lu comme s'il était en Latin-1 (ou
l'inverse). Comprendre l'encodage, c'est comprendre pourquoi ça arrive.

{{< image src="encodage-décodage.png" alt="" title="" loading="lazy" >}}

### La sérialisation des données structurées&nbsp;: JSON, XML, CSV…

Une fois qu'on sait représenter du texte, on peut s'en servir pour encoder des
structures&nbsp;: objets, listes, relations. Ce sont des formats de sérialisation
textuelle&nbsp;:

* CSV&nbsp;: simple, tabulaire, mais fragile (pas de types, ambiguïtés sur les délimiteurs).
* XML&nbsp;: hiérarchique, très explicite avec ses balises, mais verbeux.
* JSON&nbsp;: léger, lisible, naturellement aligné avec les structures des langages
  de programmation (dictionnaires, listes). C'est devenu le standard de facto
  pour les API web.

{{< pyodide >}}

# Structure en mémoire
import json

etudiant = {
    "nom": "Tremblay",
    "cours": ["GL1", "GL2"],
    "actif": True
}

# Sérialisation → chaîne JSON
donnees_serie = json.dumps(etudiant)
print(donnees_serie)
# '{"nom": "Tremblay", "cours": ["GL1", "GL2"], "actif": true}'

# Désérialisation → retour en dictionnaire Python
etudiant_copie = json.loads(donnees_serie)
print(etudiant_copie['nom'])

{{< /pyodide >}}

Leur avantage commun&nbsp;: ils sont lisibles par un humain (human-readable). Leur
inconvénient&nbsp;: ils sont volumineux et lents à parser.

### Sérialisation binaire structurée&nbsp;: Protobuf, MessagePack, Avro…

Quand la performance compte (microservices à haut débit, stockage massif), on
passe à des formats de sérialisation binaire&nbsp;:

* Protocol Buffers (Protobuf) de Google&nbsp;: on définit un schéma (fichier
  `.proto`), puis un compilateur génère du code pour encoder/décoder. Les
  données sont compactes et rapides à traiter, mais illisibles sans le schéma.
* MessagePack&nbsp;: comme du JSON, mais encodé en binaire. Plus compact, pas besoin
  de schéma.
* Avro (écosystème Hadoop)&nbsp;: le schéma voyage avec les données, ce qui facilite
  l'évolution.

Le compromis est toujours le même&nbsp;: lisibilité humaine vs efficacité machine.

### Autres encodages spécialisés

* Base64&nbsp;: encoder des données binaires (images, fichiers) en texte ASCII, pour
  les transporter dans des contextes qui n'acceptent que du texte (emails,
  JSON).

```python
import base64, textwrap

with open("image.png", "rb") as f:
    donnees = f.read()

encoded = base64.b64encode(donnees).decode("utf-8")
print(textwrap.fill(encoded, width=64))
```

Par exemple l'encodage base64 de cette image&nbsp;:

{{< image src="arrow.png" alt="" title="" loading="lazy" >}}

est&nbsp;:

```
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
v6IQAAAAAElFTkSuQmCC
```

* Encodage URL&nbsp;: remplacer les caractères spéciaux dans une URL (espace → `%20`).

{{< pyodide >}}
from urllib.parse import urlencode

base = "https://www.teluq.ca/recherche"
params = {"q": "génie logiciel", "page": 2, "lang": "fr"}

url = base + "?" + urlencode(params)
print(url)
# https://www.teluq.ca/recherche?q=g%C3%A9nie+logiciel&page=2&lang=fr
{{< /pyodide >}}

* Compression (gzip, zstd)&nbsp;: un encodage qui réduit la taille en exploitant la redondance.
* Encodage multimédia (JPEG, MP3, H.264)&nbsp;: représentations optimisées pour les
  images, le son et la vidéo, souvent avec perte.

### La vision d'ensemble

On peut voir ces couches comme un empilement&nbsp;:

```
┌──────────────────────────────────┐
│  Sémantique (schémas, ontologies)│  ← le sens, l'information
├──────────────────────────────────┤
│  Structures (JSON, Protobuf, XML)│  ← l'organisation (sérialisation)
├──────────────────────────────────┤
│  Caractères (UTF-8, ASCII)       │  ← le texte (encodage)
├──────────────────────────────────┤
│  Nombres (binaire, IEEE 754)     │  ← les valeurs (encodage)
├──────────────────────────────────┤
│  Bits (0 et 1)                   │  ← le support (encodage)
└──────────────────────────────────┘
```

À chaque niveau, encoder (ou sérialiser) c'est choisir une convention de
représentation, et décoder (ou désérialiser) c'est appliquer la même convention
à l'envers. Quand l'émetteur et le récepteur ne s'entendent pas sur la
convention, on obtient des données corrompues ou incompréhensibles, ce qui est,
en pratique, la source d'une quantité impressionnante de bugs.

## La notion de schéma

On a vu qu'encoder c'est choisir une convention de représentation, et que
sérialiser c'est transformer une structure vivante en séquence linéaire. Le
schéma, c'est la pièce manquante&nbsp;: la description formelle de la structure
elle-même — quels champs existent, de quels types ils sont, quels sont
obligatoires, quelles relations les lient.

Un schéma, c'est un contrat sur la forme des données. Il dit&nbsp;: « voici ce à quoi
une donnée valide ressemble ».

Imaginez qu'on vous fournisse ce JSON sans aucune explication&nbsp;:

```json
{
  "n": "Tremblay",
  "c": [1, 2],
  "a": true,
  "x": null
}
```


Il est possible de le désérialiser sans problème, car JSON est auto-descriptif
au niveau syntaxique. Mais on ne sait pas ce que ces champs signifient, si `c`
devrait contenir exactement 2 éléments ou peut en avoir 10, si `x` a le droit
d'être `null`, ni si un champ `courriel` est manquant par erreur ou parce qu'il
est optionnel.

Le schéma, c'est ce qui comble ce vide. Il formalise les attentes structurelles
sur les données, indépendamment des données elles-mêmes.

### Les rôles d'un schéma

Un schéma remplit plusieurs fonctions simultanément&nbsp;:

* Validation. C'est le rôle le plus immédiat. Le schéma permet de vérifier
  automatiquement qu'une donnée est conforme&nbsp;: les champs requis sont présents,
  les types sont respectés, les valeurs sont dans les bornes acceptables. Sans
  schéma, la validation est ad hoc, éparpillée dans le code sous forme de "if"
  défensifs.
* Documentation. Un bon schéma est la documentation de la structure de données.
  Il dit précisément ce qu'un système attend et ce qu'il produit. C'est un
  contrat lisible à la fois par les humains et par les machines.
* Communication entre équipes. Quand un service envoie des données à un autre,
  le schéma est le terrain d'entente. L'équipe qui produit et l'équipe qui
  consomme s'accordent sur le schéma ; ensuite chacune peut travailler
  indépendamment.
* Génération de code. À partir d'un schéma Protobuf ou Avro, on peut générer
  automatiquement des classes dans le langage cible (Python, Java, Go…). Le
  schéma devient la source de vérité dont dérive le code, pas l'inverse.
* Optimisation du stockage. Dans un format binaire avec schéma, il n'est pas
  nécessaire de répéter les noms des champs dans chaque enregistrement — le
  schéma les connaît déjà. C'est ce qui rend Protobuf beaucoup plus compact que
  JSON.
* Évolution contrôlée. Un schéma versionné permet de faire évoluer une structure
  (ajouter un champ, en déprécier un autre) tout en gardant la compatibilité
  avec les données existantes.

### Les schémas dans différents contextes

La notion de schéma apparaît partout en informatique, sous des formes
différentes mais avec la même idée fondamentale.

#### Bases de données relationnelles — DDL

C'est le schéma le plus classique. En SQL, le `CREATE TABLE` définit la structure (comme nous allons le voir plus en profondeur dans la prochaine section, sur les bases de
données)&nbsp;:
```sql
CREATE TABLE etudiants (
    matricule  CHAR(8)      PRIMARY KEY,
    nom        VARCHAR(100)  NOT NULL,
    courriel   VARCHAR(255)  UNIQUE,
    actif      BOOLEAN       DEFAULT TRUE,
    programme_id INTEGER     REFERENCES programmes(id)
);
```

Ici le schéma spécifie les colonnes, leurs types, les contraintes d'intégrité
(clé primaire, unicité, non-nullité, clé étrangère) et les valeurs par défaut.
Le SGBD refuse toute donnée non conforme — le schéma est appliqué strictement
(schema-on-write).

#### Types dans les langages de programmation

La notion de type dans un langage de programmation (dont la variation la plus
forte est pour les langages orientés-objet) est étroitement reliée à la notion
de schéma.

En Python par exemple on peut utiliser des type hints avec une classe, pour
créer un type `Etudiant`&nbsp;:

{{< pyodide >}}
from dataclasses import dataclass

@dataclass
class Etudiant:
    matricule: str
    nom: str
    cours: list[str]
    actif: bool = True

{{< /pyodide >}}

#### API

Au niveau d'une API complète, le schéma décrit non seulement les structures de
données mais aussi les opérations disponibles. Un fichier OpenAPI (anciennement
Swagger) spécifie les endpoints, les paramètres, les corps de requête et de
réponse, les codes d'erreur. Un schéma GraphQL décrit les types, les requêtes et
les mutations possibles. Dans les deux cas, le schéma devient le contrat
d'interface du service.

#### Sérialisation — Protobuf, Avro, Thrift

Ici le schéma est défini dans un fichier séparé. En Protobuf&nbsp;:
```protobuf

message Etudiant {
  string matricule = 1;
  string nom = 2;
  repeated string cours = 3;
  bool actif = 4;
}
```

Chaque champ a un numéro de tag (1, 2, 3…) qui est utilisé dans l'encodage
binaire à la place du nom. C'est ce qui permet la compacité et l'évolution&nbsp;: on
peut ajouter un champ 5 sans casser les anciens consommateurs qui ne le
connaissent pas.

#### Validation de données — JSON Schema

Pour les API REST et les échanges en JSON, JSON Schema permet de décrire formellement la structure attendue&nbsp;:
```json
{
  "type": "object",
  "required": ["matricule", "nom"],
  "properties": {
    "matricule": { "type": "string", "pattern": "^[A-Z]{4}\\d{4}$" },
    "nom":       { "type": "string", "minLength": 1 },
    "cours":     { "type": "array", "items": { "type": "string" } },
    "actif":     { "type": "boolean", "default": true }
  }
}
```

On retrouve le même principe que le DDL relationnel, mais appliqué au monde des
échanges JSON&nbsp;: types, contraintes, champs requis, motifs de validation.

### L'évolution des schémas

C'est un des problèmes les plus concrets et les plus sous-estimés en ingénierie
logicielle, et un exemple concret de complexité essentielle au sens de Brooks&nbsp;:
le changement est inévitable, et le schéma doit l'accommoder sans briser ce qui
existe déjà. Les structures de données changent — on ajoute un champ, on
renomme une colonne, on change un type. Mais les anciennes données (en base, en
cache, en transit) existent toujours sous l'ancien schéma.

On parle de **compatibilité ascendante** (*backward compatibility*) quand le
nouveau code peut lire les anciennes données, et de **compatibilité
descendante** (*forward compatibility*) quand l'ancien code peut lire les
nouvelles données.

Prenons un exemple concret. Voici un enregistrement produit par la version 1 d'un service&nbsp;:

```json
{
  "matricule": "TREM1234",
  "nom": "Tremblay",
  "actif": true
}
```

La version 2 ajoute un champ `courriel`. Un enregistrement v2 ressemble à ceci&nbsp;:

```json
{
  "matricule": "TREM1234",
  "nom": "Tremblay",
  "actif": true,
  "courriel": "tremblay@teluq.ca"
}
```

La **compatibilité ascendante** est assurée si le code v2 sait lire les anciens
enregistrements v1 — c'est-à-dire s'il tolère l'absence de `courriel` (en lui
donnant une valeur par défaut ou en l'acceptant comme optionnel). La
**compatibilité descendante** est assurée si le code v1 sait lire les nouveaux
enregistrements v2 — c'est-à-dire s'il ignore simplement le champ `courriel`
qu'il ne connaît pas. En revanche, si la v2 renomme `nom` en `nom_complet` ou
rend `courriel` obligatoire, l'une ou l'autre des compatibilités est brisée.

Les systèmes comme Protobuf et Avro ont des règles explicites pour maintenir ces
compatibilités&nbsp;: ne jamais réutiliser un numéro de champ supprimé, toujours
donner une valeur par défaut aux nouveaux champs, ne jamais rendre obligatoire
un champ qui était optionnel.

En SQL, l'évolution passe par les migrations (`ALTER TABLE`), souvent gérées par
des outils comme Alembic ou Flyway. Le défi est de modifier le schéma sans
interrompre le service ni perdre de données.

### La vision d'ensemble

Le schéma se situe au sommet de notre pile conceptuelle&nbsp;:
```
  Schéma           ← « quelle forme doivent avoir les données ? »
     │
  Sérialisation    ← « comment transformer la structure en octets ? »
     │
  Encodage         ← « comment représenter les caractères et les nombres ? »
     │
  Bits             ← « le support physique »
```

Sans schéma, on a des octets qu'on sait décoder en texte et en structures, mais
on ne sait pas si ce qu'on a reçu est correct. Le schéma ferme la boucle&nbsp;: il
donne une sémantique structurelle aux données et permet de distinguer une donnée
valide d'une donnée corrompue ou incomplète.

C'est aussi ce qui relie cette discussion à la toute première&nbsp;: les données
deviennent de l'information quand elles sont structurées selon un schéma qui
leur donne un sens.