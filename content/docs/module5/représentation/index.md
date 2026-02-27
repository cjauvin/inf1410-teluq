---
title: "La représentation des données"
weight: 10
---

# La représentation des données

## Données vs information vs connaissances

C'est une distinction classique et fondamentale en sciences de l'information.
Voici comment ces trois niveaux s'articulent :

Les données sont des faits bruts, sans contexte ni interprétation. Ce sont des
symboles, des chiffres, des mesures isolées. Par exemple : « 38,5 », « Montréal
», « 2026-02-27 ». En soi, une donnée ne veut rien dire — elle attend d'être
mise en relation avec autre chose.

L'information émerge lorsqu'on organise et contextualise des données pour leur
donner un sens. « La température du patient était de 38,5 °C ce matin » est de
l'information : on sait maintenant quoi, où, quand. L'information répond à une
question et peut être communiquée de manière structurée.

La connaissance, elle, naît quand un être humain (ou un système) intègre
l'information à son expérience, ses modèles mentaux et son jugement. Par
exemple, un médecin qui lit cette température sait que c'est une fièvre légère,
qu'il faut surveiller l'évolution, et quelles causes sont probables selon le
contexte clinique. La connaissance permet d'interpréter, de décider et d'agir.

On résume souvent cette hiérarchie ainsi — parfois appelée la [pyramide
DIKW](https://fr.wikipedia.org/wiki/Pyramide_DICS) (Données → Information →
Connaissances → Sagesse) :

* Donnée → « le quoi brut » (symboles sans contexte)
* Information → « le quoi structuré » (données + contexte + sens)
* Connaissance → « le comment et le pourquoi » (information + expérience + jugement)

La sagesse (wisdom), parfois ajoutée au sommet, serait la capacité de porter un
jugement éclairé sur quand et pourquoi appliquer ses connaissances.

## L'encodage et la sérialisation (et leur inverse)

Un ordinateur ne manipule que des bits (0 et 1). Tout le reste — lettres,
nombres, images, structures de données — doit être encodé, c'est-à-dire traduit
en séquences de bits selon des règles convenues. L'encodage est donc un contrat
de représentation entre celui qui écrit et celui qui lit. On peut distinguer
plusieurs couches d'encodage, chacune répondant à un besoin différent.

### L'encodage des nombres : le binaire

C'est la couche la plus basse. Un entier comme 42 se représente en base 2 :
`00101010`.

{{< pyodide >}}

n = 42
print(f"{n:08b}")

{{< /pyodide >}}

Pour les nombres négatifs, on utilise le complément à deux. Pour les
nombres à virgule, la norme IEEE 754 définit comment encoder le signe,
l'exposant et la mantisse en 32 ou 64 bits. L'essentiel ici : le même paquet de
bits peut signifier des choses complètement différentes selon l'interprétation
qu'on en fait. `01000001` peut être l'entier 65, le caractère `A`, ou une partie
d'un nombre flottant — tout dépend du contexte d'interprétation.

### L'encodage des caractères : ASCII, Latin-1, UTF-8…

Comment représenter du texte ? Il faut une table de correspondance entre des
caractères et des nombres.

* ASCII (1963) : 7 bits, 128 caractères. Suffisant pour l'anglais, mais pas pour
  "é", "ñ" ou "漢".
* Latin-1 / ISO 8859-1 : 8 bits, 256 caractères. Couvre les langues d'Europe
  occidentale, mais chaque région du monde avait sa propre table — d'où des
  problèmes d'interopérabilité constants.
* Unicode : un répertoire universel qui attribue un code point unique à chaque
  caractère de toutes les écritures (ex. : `U+00E9` = "é", `U+4E16` = "世").
  Mais Unicode n'est pas un encodage en soi, c'est un catalogue.
* UTF-8 : l'encodage le plus répandu d'Unicode. Il est à longueur variable — un
  caractère ASCII tient sur 1 octet, un accent sur 2, un idéogramme sur 3,
  certains emojis sur 4. Son génie est d'être rétrocompatible avec ASCII : tout
  fichier ASCII est déjà du UTF-8 valide.

La confusion classique qu'on retrouve partout : voir des `Ã©` au lieu de `é`,
c'est presque toujours un fichier UTF-8 lu comme s'il était en Latin-1 (ou
l'inverse). Comprendre l'encodage, c'est comprendre pourquoi ça arrive.

### La sérialisation des données structurées : JSON, XML, CSV…

Une fois qu'on sait représenter du texte, on peut s'en servir pour encoder des
structures — objets, listes, relations. Ce sont des formats de sérialisation
textuelle :

* CSV : simple, tabulaire, mais fragile (pas de types, ambiguïtés sur les délimiteurs).
* XML : hiérarchique, très explicite avec ses balises, mais verbeux.
* JSON : léger, lisible, naturellement aligné avec les structures des langages
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

Leur avantage commun : ils sont lisibles par un humain (human-readable). Leur
inconvénient : ils sont volumineux et lents à parser.

### Sérialisation binaire structurée : Protobuf, MessagePack, Avro…

Quand la performance compte (microservices à haut débit, stockage massif), on
passe à des formats de sérialisation binaire :

* Protocol Buffers (Protobuf) de Google : on définit un schéma (fichier
  `.proto`), puis un compilateur génère du code pour encoder/décoder. Les
  données sont compactes et rapides à traiter, mais illisibles sans le schéma.
* MessagePack : comme du JSON, mais encodé en binaire. Plus compact, pas besoin
  de schéma.
* Avro (écosystème Hadoop) : le schéma voyage avec les données, ce qui facilite
  l'évolution.

Le compromis est toujours le même : lisibilité humaine vs efficacité machine.

### Autres encodages spécialisés

* Base64 : encoder des données binaires (images, fichiers) en texte ASCII, pour
  les transporter dans des contextes qui n'acceptent que du texte (emails,
  JSON).
* Encodage URL : remplacer les caractères spéciaux dans une URL (espace → %20).
* Compression (gzip, zstd) : un encodage qui réduit la taille en exploitant la redondance.
* Encodage multimédia (JPEG, MP3, H.264) : représentations optimisées pour les
  images, le son et la vidéo, souvent avec perte.

### La vision d'ensemble

On peut voir ces couches comme un empilement :

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

À chaque niveau, encoder c'est choisir une convention de représentation, et
décoder c'est appliquer la même convention à l'envers. Quand l'émetteur et le
récepteur ne s'entendent pas sur la convention, on obtient des données
corrompues ou incompréhensibles — ce qui est, en pratique, la source d'une
quantité impressionnante de bugs.

