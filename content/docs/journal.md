---
title: "Journal des modifications"
weight: 17
slug: journal
---

# Journal des modifications

Ce cours n'est pas figé. Il est corrigé, complété et parfois réorganisé pendant
la session, et comme les inscriptions sont continues, deux étudiants peuvent
avoir lu deux versions différentes d'une même page. Cette page rassemble les
changements qui comptent pour un lecteur&nbsp;: les nouvelles sections, les
changements aux travaux notés, les corrections de faits et les adresses de pages
modifiées. Les retouches de forme, d'illustration ou d'outillage n'y figurent
pas. Elles restent dans l'[historique du dépôt git](https://github.com/cjauvin/inf1410-teluq/commits/main/)
du cours, qui est public.

La présentation suit la convention
[*Keep a Changelog*](https://keepachangelog.com/fr/1.1.0/) d'Olivier Lacan,
dont le premier principe veut que les changelogs soient « pour les êtres
humains, pas les machines ». Chaque entrée est datée, la plus récente en haut,
et ses changements sont regroupés en ajouts, modifications et corrections. Les
[livres PDF et EPUB]({{< relref "/docs/telecharger.md" >}}) étant produits à
chaque mise à jour du site, la date de leur page de titre dit à quelle entrée
de ce journal ils correspondent.

{{% hint warning %}}

**Les changements aux travaux notés sont signalés par la mention « Travaux
notés ».** Une exigence ajoutée après votre inscription ne s'applique pas à
vous&nbsp;: elle vous est recommandée, et son absence ne sera pas pénalisée. Une
exigence retirée ou assouplie s'applique à tous. En cas de doute, c'est la date
de votre inscription qui fait foi.

{{% /hint %}}

## 28 octobre 2026

### Corrigé

Dix erreurs factuelles, relevées par une vérification systématique des faits à
leur source. Chaque lien « avant et après » ouvre la modification exacte sur
GitHub, l'ancien texte en rouge et le nouveau en vert&nbsp;:

- [Lectures]({{< relref "/docs/lectures.md" >}}) et
  [Pourquoi la concurrence]({{< relref "/docs/module2/15-concurrence/10-pourquoi/index.md" >}})&nbsp;:
  l'article de Moore fait quatre pages, et il évoque la vitesse en passant
  (avant et après&nbsp;: [lectures](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-99db0ec4551f85464c027414dccb1eebfc7341f6d3931187cfed8c32801ab828),
  [concurrence](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-9328b32943f293fcddcf29fe7547c061da3e35e7cdcf70b40c140bca60ffc061)).
- [Environnements]({{< relref "/docs/environnements/index.md" >}})&nbsp;: Steve
  Ballmer a qualifié Linux de « cancer » en 2001, pas dans les années 1990
  ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-d6b55cdce6b0b722699bc2666b11fbc671ca2111c934ffc391354a2d659baad6)).
- [Les tests]({{< relref "/docs/module2/20-tests/index.md" >}})&nbsp;:
  coverage.py a été écrit par Gareth Rees, Ned Batchelder le maintient depuis
  2004 ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-01e1d80345def1c8ce7455ef0deb3a0ac028c09c449199ee26e30120e97bcc79)).
- [La gestion des dépendances]({{< relref "/docs/module2/40-gestion-des-deps/index.md" >}})&nbsp;:
  la PlayStation et la Mazda 3 illustrent la numérotation des versions, pas le
  versionnage sémantique, qui leur est postérieur. Le fichier `uv.lock` n'est
  jamais vide ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-b2473e39ab6653fb762e0b0c12d9e1040122e1675175b7ec5f7f7d267ae09e50)).
- [Le versioning]({{< relref "/docs/module2/30-versioning/index.md" >}})&nbsp;:
  le sous-répertoire d'un objet git porte le préfixe de son hash, pas son
  suffixe ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-ae82a2dc9568aedff49e8c85743cc222f8256ba01994ef97f0f5bf9a606f9d40)).
- [Les APIs]({{< relref "/docs/module3/20-apis/index.md" >}})&nbsp;: SOAP
  répondait `500` à toute erreur, et non toujours `200`
  ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-5fdab74eb4466fccaeee7874f7691e7cdab4aa541bd5e1cf1f2c3a499d1ac5e7)).
- [Perspective historique des interfaces]({{< relref "/docs/module3/30-interfaces/10-historique/index.md" >}})&nbsp;:
  la souris a été inventée en 1963-1964, et présentée au public en 1968
  ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-521a92ed1d549c3f22a580814162bd6df9100847686ae563f4cd54c8bcfcd5d6)).
- [Les frameworks JavaScript]({{< relref "/docs/module3/30-interfaces/30-frameworks/index.md" >}})&nbsp;:
  Vue s'appuie lui aussi sur un DOM virtuel
  ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-6c83c11b18ac1a4ae6f5030d6135cce8b4548313be554ea05549a82f89e45f01)).
- [Desktop, web et mobile]({{< relref "/docs/module3/30-interfaces/40-convergences/index.md" >}})&nbsp;:
  WebAssembly est arrivé dans les navigateurs en 2017, et le W3C l'a
  standardisé en 2019 ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-be019d9a8d83474a91675d3050bf821cd479d521563c53fca3a280222b076e94)).

## 11 octobre 2026

### Ajouté

- **Travaux notés**&nbsp;: [Un projet qui survit au cours]({{< relref "/docs/travaux-notés/index.md#un-projet-qui-survit-au-cours" >}}),
  une invitation à viser une application réelle, avec de vrais utilisateurs
  ou de vrais clients, et les conditions pour qu'elle reste évaluable, dont un
  environnement de démonstration pour les correcteurs.

### Modifié

- [Historique du génie logiciel]({{< relref "/docs/module1/10-historique/index.md" >}})&nbsp;:
  Margaret Hamilton, morte le 30 septembre 2026, reçoit ses dates.

### Corrigé

- [Historique du génie logiciel]({{< relref "/docs/module1/10-historique/index.md" >}})&nbsp;:
  trois erreurs, sur Grace Hopper, qui n'a pas inventé le mot « bug », sur le
  principe de Liskov, énoncé en 1987 et formulé avec Jeannette Wing en 1994,
  et sur Python, qui précède Java de quatre ans
  ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/e9f8221388831e537dd0d3f6d8205884c5fb4982)). Neuf précisions aussi, sur
  le programme stocké, l'ENIAC, FORTRAN, COBOL, l'A-0, C et Unix, le modèle en
  spirale et AWS ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/e2331bdd261cbf36bf3fc96cab021728e7b185cf)).
- [L'économie du logiciel]({{< relref "/docs/module6/20-economie/index.md" >}})&nbsp;:
  Tobias Lütke n'a pas créé Ruby on Rails, il a fait partie de son équipe
  principale ([avant et après](https://github.com/cjauvin/inf1410-teluq/commit/c7e5a2c9b2e0638e82bdde452c504de56cb0b5e8)).

## 1er octobre 2026

### Ajouté

- Le cours en [livres PDF et EPUB]({{< relref "/docs/telecharger.md" >}}),
  produits à chaque mise à jour du site.

## 24 septembre 2026

### Ajouté

- [Accueil]({{< relref "/_index.md#pourquoi-ce-cours-au-temps-de-lia-agentique" >}})&nbsp;:
  une section « Pourquoi ce cours, au temps de l'IA agentique&nbsp;? », bâtie
  sur la défense au tableau blanc de Mitchell Hashimoto, que l'entretien de
  suivi des travaux notés met en pratique. Le principe rejoint la
  [page des principes]({{< relref "/docs/principes.md" >}}).

## 18 septembre 2026

### Modifié

- **Travaux notés**&nbsp;: la [remise officielle]({{< relref "/docs/travaux-notés/index.md#la-remise-officielle" >}})
  se fait dans l'ENA, dans la section Évaluations du cours, et chaque jalon et
  chaque entretien porte le lien direct de son activité.

## 16 septembre 2026

### Ajouté

- **Travaux notés**&nbsp;: [Montrer en vidéo]({{< relref "/docs/travaux-notés/index.md#montrer-en-vidéo" >}}).
  Les vidéos sont encouragées, pour faire voir l'application, parcourir le code
  ou raconter un bogue. Elles ne sont pas obligatoires.

## 8 septembre 2026

### Ajouté

- **Travaux notés**&nbsp;: [Les problèmes, et la manière dont vous les avez réglés]({{< relref "/docs/travaux-notés/index.md#les-problèmes-et-la-manière-dont-vous-les-avez-réglés" >}}).
  Les problèmes rencontrés et leur résolution font désormais partie de la
  documentation attendue, et chacun devrait avoir son issue GitHub.
- [Scrum]({{< relref "/docs/module4/20-agile/10-scrum/index.md" >}})&nbsp;: les
  mots-clés de fermeture, comme `Fixes #12`, qui relient une issue au commit
  qui la règle.

### Modifié

- **Travaux notés**&nbsp;: le [jalon 3]({{< relref "/docs/travaux-notés/index.md#jalon-3--développement-15" >}})
  exige désormais un problème de programmation réglé par une technique de
  débogage, et un problème de gestion du code source réglé avec git. Le
  [jalon 4]({{< relref "/docs/travaux-notés/index.md#jalon-4--livraison-finale-25" >}})
  demande un bilan des problèmes de toute la session.
- Les adresses des sections Interfaces utilisateur, Données, Agilité et
  Infrastructure ne contiennent plus de préfixe numérique, par exemple
  `module4/agile/scrum/` au lieu de `module4/20-agile/scrum/`. Les anciens
  liens ne fonctionnent plus.

## 4 au 7 septembre 2026

### Ajouté

- Une nouvelle section au module 2, [Le débogage]({{< relref "/docs/module2/25-debogage/index.md" >}})&nbsp;:
  l'histoire du mot, le `print`, le débogueur pdb, et une chasse au bogue pas à
  pas dans VS Code.
- Des encarts « Dans VS Code » dans les sections sur
  [les tests]({{< relref "/docs/module2/20-tests/index.md" >}}),
  [le versioning]({{< relref "/docs/module2/30-versioning/index.md" >}}) et
  [la gestion des dépendances]({{< relref "/docs/module2/40-gestion-des-deps/index.md" >}}).
- [Environnements]({{< relref "/docs/environnements/index.md" >}})&nbsp;: la
  boucle interactive (REPL), IPython et les notebooks.
- **Travaux notés**&nbsp;: le jalon 3 suggère de documenter une activité de
  débogage. C'est devenu une exigence le 8 septembre.

## 1er au 3 septembre 2026

### Ajouté

- Une nouvelle section au module 2, [Concurrence et parallélisme]({{< relref "/docs/module2/15-concurrence/_index.md" >}}),
  en cinq sous-sections, reliée au reste du cours.
- [Accueil]({{< relref "/_index.md" >}})&nbsp;: pourquoi le cours est touffu,
  et ce qu'on y appelle le sens du possible.
- [Survol rapide de la programmation]({{< relref "/docs/module2/10-programmation/index.md" >}})&nbsp;:
  une mise en garde de Daniel Lemire, professeur à la TÉLUQ, sur le temps
  constant des tables de hachage.
- [Environnements]({{< relref "/docs/environnements/index.md" >}})&nbsp;: VS
  Code présenté comme une vue sur les outils.
