---
title: "Journal des modifications"
weight: 17
slug: journal
---

# Journal des modifications

Ce cours n'est pas figé. Il est corrigé, complété et parfois réorganisé pendant
la session, et comme les inscriptions sont continues, deux étudiants peuvent
avoir lu deux versions différentes d'une même page. Cette page rassemble tout ce
qui change dans ce que vous lisez&nbsp;: les nouvelles sections, les changements
aux travaux notés, les corrections de faits, les adresses de pages modifiées, et
jusqu'aux coquilles et aux retouches d'images. Seul l'outillage qui produit le
site, sans rien changer à ce qu'il affiche, n'y figure pas. Les entrées
antérieures au 28 octobre 2026, reconstituées après coup, ne retiennent que les
changements principaux.

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

### Ajouté

- [Architecture et modularité]({{< relref "/docs/module3/10-architecture/index.md#dessiner-une-conception--uml" >}})&nbsp;:
  une section sur UML, réduite aux deux diagrammes qui ont survécu à l'usage,
  celui de classes et celui de séquence, écrits en texte avec Mermaid. Les
  livres PDF et EPUB les reproduisent en images.

### Modifié

- [Journal des modifications]({{< relref "/docs/journal.md" >}})&nbsp;: la page
  consigne désormais tout ce qui change dans ce que vous lisez, jusqu'aux
  coquilles et aux retouches d'images.

### Corrigé

Trente-cinq erreurs factuelles, relevées par une vérification systématique des
faits à leur source. Chaque lien « voir le diff » ouvre sur GitHub la différence exacte
entre l'ancien texte, en rouge, et le nouveau, en vert, ce que `git diff`
affiche au terminal&nbsp;:

- [Lectures]({{< relref "/docs/lectures.md" >}}) et
  [Pourquoi la concurrence]({{< relref "/docs/module2/15-concurrence/10-pourquoi/index.md" >}})&nbsp;:
  l'article de Moore fait quatre pages, et il évoque la vitesse en passant
  (voir le diff&nbsp;: [lectures](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-99db0ec4551f85464c027414dccb1eebfc7341f6d3931187cfed8c32801ab828),
  [concurrence](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-9328b32943f293fcddcf29fe7547c061da3e35e7cdcf70b40c140bca60ffc061)).
- [Environnements]({{< relref "/docs/environnements/index.md" >}})&nbsp;: Steve
  Ballmer a qualifié Linux de « cancer » en 2001, pas dans les années 1990
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-d6b55cdce6b0b722699bc2666b11fbc671ca2111c934ffc391354a2d659baad6)).
- [Ce qui casse]({{< relref "/docs/module2/15-concurrence/30-ce-qui-casse/index.md" >}})&nbsp;: le projet
  Ptolemy d'Edward Lee existe depuis 1993, et c'est Ptolemy II qui commence en
  2000 ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/e7d857a2be3130812ed4c4d3b3121c9b6cc2bd99#diff-bb551026e378da5b319a377f382aaabde10e8435f6b8adc40a6e94a2e848791d)).
- [Ne pas partager]({{< relref "/docs/module2/15-concurrence/40-ne-pas-partager/index.md" >}})&nbsp;: dans
  l'article de Hoare de 1978, les processus se désignent par leur nom, et les
  canaux ne viennent qu'ensuite ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/e7d857a2be3130812ed4c4d3b3121c9b6cc2bd99#diff-a639373f05f92b24b5f24239248484daf9097ae0b1e68d0cdee89618e6433e64)).
- [Ne jamais bloquer]({{< relref "/docs/module2/15-concurrence/50-ne-jamais-bloquer/index.md" >}})&nbsp;: le
  bassin de processus de l'exemple ne lance qu'un interpréteur, pas un par
  coeur, parce qu'il démarre ses processus à la demande
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/e7d857a2be3130812ed4c4d3b3121c9b6cc2bd99#diff-3c70995dc7891c57f40474caf3a441ed2ac3b75b8f5374401af65b9229bf00b6)).
- [Les tests]({{< relref "/docs/module2/20-tests/index.md" >}})&nbsp;:
  coverage.py a été écrit par Gareth Rees, Ned Batchelder le maintient depuis
  2004 ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-01e1d80345def1c8ce7455ef0deb3a0ac028c09c449199ee26e30120e97bcc79)).
- [La gestion des dépendances]({{< relref "/docs/module2/40-gestion-des-deps/index.md" >}})&nbsp;:
  la PlayStation et la Mazda 3 illustrent la numérotation des versions, pas le
  versionnage sémantique, qui leur est postérieur. Le fichier `uv.lock` n'est
  jamais vide ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-b2473e39ab6653fb762e0b0c12d9e1040122e1675175b7ec5f7f7d267ae09e50)).
- [Le versioning]({{< relref "/docs/module2/30-versioning/index.md" >}})&nbsp;:
  le sous-répertoire d'un objet git porte le préfixe de son hash, pas son
  suffixe ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-ae82a2dc9568aedff49e8c85743cc222f8256ba01994ef97f0f5bf9a606f9d40)).
- [Les APIs]({{< relref "/docs/module3/20-apis/index.md" >}})&nbsp;: SOAP
  répondait `500` à toute erreur, et non toujours `200`
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-5fdab74eb4466fccaeee7874f7691e7cdab4aa541bd5e1cf1f2c3a499d1ac5e7)).
- [Perspective historique des interfaces]({{< relref "/docs/module3/30-interfaces/10-historique/index.md" >}})&nbsp;:
  la souris a été inventée en 1963-1964, et présentée au public en 1968
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-521a92ed1d549c3f22a580814162bd6df9100847686ae563f4cd54c8bcfcd5d6)).
- [Les frameworks JavaScript]({{< relref "/docs/module3/30-interfaces/30-frameworks/index.md" >}})&nbsp;:
  Vue s'appuie lui aussi sur un DOM virtuel
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-6c83c11b18ac1a4ae6f5030d6135cce8b4548313be554ea05549a82f89e45f01)).
- [Desktop, web et mobile]({{< relref "/docs/module3/30-interfaces/40-convergences/index.md" >}})&nbsp;:
  WebAssembly est arrivé dans les navigateurs en 2017, et le W3C l'a
  standardisé en 2019 ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/cc185a9e55326a5fdfa50a5303bc4b113dfbf4fd#diff-be019d9a8d83474a91675d3050bf821cd479d521563c53fca3a280222b076e94)).
- [Les bases de données]({{< relref "/docs/module3/40-données/20-stockage/index.md" >}})&nbsp;:
  les migrations de Rails datent de 2005, et sont une contribution de Tobias
  Lütke. Les bases colonnaires analytiques, comme Sybase IQ et C-Store, ne
  sont pas les *wide-column stores* comme Bigtable, Cassandra et HBase (voir le
  diff&nbsp;: [stockage](https://github.com/cjauvin/inf1410-teluq/commit/082e46f88bd4f3f57ae5b59ff394066eb122336a#diff-a71922fff3367cbe2eecf61cdb7ca2c458a727cbc1f94bcc57379ba28da3fc3f),
  [lectures](https://github.com/cjauvin/inf1410-teluq/commit/082e46f88bd4f3f57ae5b59ff394066eb122336a#diff-99db0ec4551f85464c027414dccb1eebfc7341f6d3931187cfed8c32801ab828)).
- [Au-delà des bases de données]({{< relref "/docs/module3/40-données/30-au-delà/index.md" >}})&nbsp;:
  Git stocke des instantanés, il ne rejoue pas un historique d'événements, et
  Amazon QLDB a été fermé en juillet 2025
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/082e46f88bd4f3f57ae5b59ff394066eb122336a#diff-2af882594e073a8f1b69b0819603516d3d1c63e7e5f24666dac444a13516a088)).
- [La conteneurisation (Docker)]({{< relref "/docs/module5/10-infrastructure/10-docker/index.md" >}})&nbsp;:
  le fichier Compose du tutoriel publie maintenant le port 8080 qu'utilisent
  les commandes qui suivent ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/082e46f88bd4f3f57ae5b59ff394066eb122336a#diff-662b990db7368d1855b1251b4e0dcf6e2645738c54df62bab00eb696c78d9e81)).
- [Le déploiement continu]({{< relref "/docs/module5/20-deploiement/index.md" >}})&nbsp;:
  le terme « blue-green » vient de Daniel Terhorst-North et Jez Humble, et
  c'est leur livre qui l'a popularisé ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/082e46f88bd4f3f57ae5b59ff394066eb122336a#diff-7114329235778678789bfbc838f1b5737e7240b821b08912c69ba85dc7b29536)).
- [L'observabilité]({{< relref "/docs/module5/30-observabilite/index.md" >}})&nbsp;:
  les ingénieurs de Google à l'origine de Prometheus n'ont pas fondé
  SoundCloud, ils l'ont rejoint, et l'intervalle de collecte par défaut de
  Prometheus est d'une minute ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/082e46f88bd4f3f57ae5b59ff394066eb122336a#diff-4b1fd7d91ea03d6c07781fae15bae7fc7cee97a6d6279bcbd8d05aba10d5c951)).
- [La fiabilité et les incidents]({{< relref "/docs/module5/40-incidents/index.md" >}})&nbsp;:
  le livre SRE de Google plafonne l'astreinte à 25&nbsp;% et le travail
  opérationnel à 50&nbsp;%, et John Allspaw n'est devenu CTO d'Etsy qu'en 2015
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/082e46f88bd4f3f57ae5b59ff394066eb122336a#diff-263a56310a1b1088c7c07fd670a935d93f00f1271ef027d6ff0e72910632abd7)).
- [La fiabilité et les incidents]({{< relref "/docs/module5/40-incidents/index.md" >}})&nbsp;:
  Netflix a publié les *Principles of Chaos Engineering* en 2015, pas en 2014
  (voir le diff&nbsp;: [incidents](https://github.com/cjauvin/inf1410-teluq/commit/b2d7f5096ec391685b1acb963aeafeb7d404512d#diff-263a56310a1b1088c7c07fd670a935d93f00f1271ef027d6ff0e72910632abd7),
  [lectures](https://github.com/cjauvin/inf1410-teluq/commit/b2d7f5096ec391685b1acb963aeafeb7d404512d#diff-99db0ec4551f85464c027414dccb1eebfc7341f6d3931187cfed8c32801ab828)).
- [La sécurité]({{< relref "/docs/module5/50-securite/index.md" >}})&nbsp;: la fuite chez
  Desjardins a touché près de 9,7 millions de personnes, dont ses 4,2 millions
  de membres particuliers, et l'outil d'audit des dépendances Python s'appelle
  `pip-audit` ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/b2d7f5096ec391685b1acb963aeafeb7d404512d#diff-81d82940a2114a01ed335681590ab1ef0cdd511d5901f161d4cc741584e0dc51)).
- [La scalabilité]({{< relref "/docs/module5/60-scalabilite/index.md" >}})&nbsp;: les
  marchands de Shopify ont vendu pour 9,3 milliards de dollars pendant le
  weekend du Black Friday 2023, et les navigateurs ne partagent plus leur cache
  entre les sites ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/b2d7f5096ec391685b1acb963aeafeb7d404512d#diff-f906f962c1f4a34a6b7b4b94ec0a34abbcbbfa53fcb75f7271803e92b437c88f)).
- [L'open source]({{< relref "/docs/module6/10-open-source/index.md" >}})&nbsp;: les quatre
  libertés du logiciel libre se sont formalisées après 1985, la licence d'Ext
  JS a changé en 2008, et GitHub n'est pas un logiciel open source offert en
  service ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/e7d857a2be3130812ed4c4d3b3121c9b6cc2bd99#diff-3d8dffcac940283e84b6e8e7da089af98f84d4233e561621262db974fe956c59)).
- [Monopoles et régulation]({{< relref "/docs/module6/30-monopoles/index.md" >}})&nbsp;: Google
  a payé environ 20 milliards de dollars à Apple en 2022, et non 26 milliards
  par an ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/b2d7f5096ec391685b1acb963aeafeb7d404512d#diff-43a27119f253f318492f5957275a6fc391beb0d8f71be1348a63d704bb331eff)).
- [Catastrophes, éthique et responsabilité]({{< relref "/docs/module6/40-catastrophes/index.md" >}})&nbsp;:
  Curam a été développé par l'entreprise irlandaise Cúram Software, et non par
  IBM ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/b2d7f5096ec391685b1acb963aeafeb7d404512d#diff-42621d9e9a200e9cda5073b77cd8f34b63c408f494f1a62f48da03ca9d218c88)).
- [Le métier de développeur]({{< relref "/docs/module6/50-metier/index.md" >}})&nbsp;:
  Smalltalk est un langage orienté objet, pas un langage fonctionnel
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/b2d7f5096ec391685b1acb963aeafeb7d404512d#diff-42f6ea02531b95348d2ae66709defb8725e84d2985864ca80d1a049edb9bb478)).
- [Le développement assisté par IA]({{< relref "/docs/module6/60-ia/index.md" >}})&nbsp;:
  GitHub rapportait en 2023 que Copilot écrivait 46&nbsp;% du code de ses
  utilisateurs, et non plus de la moitié du code de la plateforme
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/b2d7f5096ec391685b1acb963aeafeb7d404512d#diff-8ee98b94e8e8fa6fc165aab419eb00adc237474796f8972eb13db17dd25b3736)).

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
  ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/e9f8221388831e537dd0d3f6d8205884c5fb4982)). Neuf précisions aussi, sur
  le programme stocké, l'ENIAC, FORTRAN, COBOL, l'A-0, C et Unix, le modèle en
  spirale et AWS ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/e2331bdd261cbf36bf3fc96cab021728e7b185cf)).
- [L'économie du logiciel]({{< relref "/docs/module6/20-economie/index.md" >}})&nbsp;:
  Tobias Lütke n'a pas créé Ruby on Rails, il a fait partie de son équipe
  principale ([voir le diff](https://github.com/cjauvin/inf1410-teluq/commit/c7e5a2c9b2e0638e82bdde452c504de56cb0b5e8)).

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
