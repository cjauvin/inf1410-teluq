---
title: "Accueil"
---

{{< image src="open-space.webp" alt="Un vaste espace de travail ouvert où des centaines de développeurs travaillent côte à côte devant leurs écrans" title="Le logiciel moderne se construit à plusieurs" loading="lazy" >}}

# Bienvenue

Bienvenue dans ce nouveau cours d'introduction au génie logiciel (GL).

Ce cours adopte une approche qui se distingue de la présentation traditionnelle
du génie logiciel, souvent centrée sur les formalismes et les diagrammes. Trois
idées guident sa conception :

- **La culture générale technologique.** Le génie logiciel est un domaine vaste,
  et personne ne peut prétendre en maîtriser tous les aspects. Mais nous croyons
  qu'il est important de se construire un réseau d'idées et de connaissances, et
  d'avoir au moins un modèle mental de base pour la plupart des grands domaines
  et des grandes idées. Savoir qu'un concept existe, comprendre à quoi il sert
  et comment il se relie aux autres, c'est souvent suffisant pour poser les
  bonnes questions et approfondir au besoin. Ce cours vise à instiller ce goût
  et cette curiosité pour la culture technologique au sens large.

- **La perspective historique.** Nous croyons que les contextes historiques des
  idées et des innovations en informatique sont fascinants quand on prend le
  temps de s'y attarder : on découvre que certaines idées ont des vies
  étonnamment longues, que des problèmes qu'on croyait récents se posaient déjà
  il y a des décennies, et que comprendre ces origines éclaire la pratique
  actuelle. Cela permet également de faire des liens profonds entre des idées
  qui peuvent parfois apparaître assez éloignées, ou séparées dans le temps, et
  de constater que plusieurs thèmes importants reviennent sans cesse, sous
  différentes formes.

- **L'expérience directe.** Le cours contient de nombreux exemples et tutoriels
  détaillés, car il nous apparaît essentiel de vous donner une expérience
  directe des outils et des techniques importants, plutôt que de simplement les
  décrire. Le tutoriel est une forme d'apprentissage omniprésente dans la
  culture de l'internet, et ce cours se réclame particulièrement de cette
  culture, où le partage de connaissances pratiques est une valeur centrale.
  Nous vous encourageons d'ailleurs fortement à explorer par vous-mêmes et à
  faire vos propres expériences : les outils et les concepts présentés ici ne
  sont qu'un échantillon dans un vaste océan de possibilités, et la curiosité
  autonome est une compétence fondamentale en génie logiciel.

{{< image src="3-pillars.jpg" alt="" title="" loading="lazy" >}}

Ces trois idées convergent vers une seule. Apprendre quelque chose, c'est en
grande partie développer un sens de ce qui est possible&nbsp;: savoir qu'une chose
peut se faire, à quel prix et avec quoi, avant même de savoir la faire
soi-même. Ce sens compte aujourd'hui plus qu'il n'a jamais compté, et pour une
raison paradoxale. Les outils qui écrivent, exécutent et corrigent du code à
notre place nous donnent un pouvoir d'exécution que personne n'avait il y a
quelques années. Mais ce pouvoir ne vaut que ce que vaut le sens du possible de
celui qui le tient. On ne demande pas ce qu'on ne sait pas concevable, et on ne
reconnaît pas une bonne réponse dans un domaine où l'on n'a jamais mis les
pieds. C'est pourquoi ce cours est touffu, et l'assume&nbsp;: il contient beaucoup
d'idées, d'outils et d'histoires, choisis pour vous donner le meilleur **sens du
possible** avec le logiciel, celui qui fait la différence entre disposer d'un
pouvoir et savoir quoi en faire.

## Pourquoi ce cours, au temps de l'IA agentique&nbsp;?

La question mérite d'être posée franchement. Au moment où ce cours est écrit,
un agent de programmation peut, à partir d'une description en langage naturel,
produire une application entière, l'organiser, la tester et la déployer, et il
le fait mieux d'un mois à l'autre. Si la machine écrit le code, à quoi bon
apprendre le versioning, les tests, l'architecture, les bases de données et
tout ce qui suit&nbsp;? Ne suffirait-il pas d'apprendre à bien demander&nbsp;? La
réponse de ce cours tient en un critère, formulé en septembre 2026 par Mitchell
Hashimoto, cofondateur de HashiCorp, l'entreprise derrière Terraform que vous
croiserez au [module 5]({{< relref "/docs/module5/10-infrastructure/30-iac/index.md" >}}).

{{< image src="hashimoto-whiteboard-defense.webp" alt="Capture d'écran d'une publication de Mitchell Hashimoto (@mitchellh) sur X, datée du 16 septembre 2026, en thème sombre, qui définit la « whiteboard defense » comme critère d'un usage responsable de l'IA ; 465,9 k vues, 9,1 k mentions j'aime" title="La « défense au tableau blanc », telle que publiée par Mitchell Hashimoto le 16 septembre 2026" loading="lazy" >}}

Traduction&nbsp;:

> La « **défense au tableau blanc** »&nbsp;: je devrais pouvoir vous prendre à
> part à n'importe quel moment et vous demander d'expliquer n'importe quel
> système que vous avez livré à des clients. Vous devriez pouvoir expliquer
> clairement comment il fonctionne et défendre les décisions que vous avez
> prises. C'est mon critère pour un usage responsable de l'IA.
>
> Je n'attends pas une connaissance du code ligne par ligne. Peu m'importe que
> vous vous souveniez du nom exact d'une fonction ou d'un détail
> d'implémentation. Vous pourriez même ne pas le savoir. Ça m'est égal.
>
> Mais si je demande « pourquoi avoir fait X plutôt que Y&nbsp;? », « que se
> passe-t-il si cet acteur se comporte de façon malveillante&nbsp;? », « quelle
> structure de données avez-vous utilisée ici, et pourquoi&nbsp;? » ou « où
> est-ce que ça casse&nbsp;? », vous devriez pouvoir répondre avec assurance.
>
> Pour les preuves de concept, les démos, les expériences, peu importe&nbsp;: je
> m'en fiche. Générez-en 100 % et n'en comprenez rien. La vitesse avant la
> qualité, chaque fois, dans ces cas précis.
>
> Mais si vous livrez du travail destiné à des clients, vous ne pouvez pas
> livrer des choses que vous ne comprenez pas, au moins dans les grandes lignes.
>
> Mitchell Hashimoto, [sur X](https://x.com/mitchellh/status/2100249348345057389), 16 septembre 2026

Ce critère est celui de ce cours, et il explique son contenu. Chaque question
de la liste renvoie à un module&nbsp;: « pourquoi X plutôt que Y » est une
question d'[architecture]({{< relref "/docs/module3/10-architecture/index.md" >}})
et de décisions documentées, « quelle structure de données et pourquoi » une
question de [représentation des données]({{< relref "/docs/module3/40-données/10-représentation/index.md" >}}),
« où est-ce que ça casse » une question de
[tests]({{< relref "/docs/module2/20-tests/index.md" >}}), de
[concurrence]({{< relref "/docs/module2/15-concurrence/_index.md" >}}) et de
[fiabilité]({{< relref "/docs/module5/40-incidents/index.md" >}}), « que se
passe-t-il si cet acteur est malveillant » une question de
[sécurité]({{< relref "/docs/module5/50-securite/index.md" >}}). Aucune ne
demande d'écrire du code, toutes demandent de le comprendre. L'agent qui
produit une application ne vous dispense pas de pouvoir la défendre, il rend
cette capacité plus rare, donc plus précieuse, parce qu'il devient facile de
livrer ce qu'on ne comprend pas. Le sens du possible décrit plus haut est ce qui
permet de demander la bonne chose&nbsp;; la défense au tableau blanc est ce qui
permet de répondre de ce qu'on a obtenu.

Ce cours vous fera passer cette défense, pour de vrai. Les
[entretiens de suivi]({{< relref "/docs/travaux-notés/index.md#lentretien-de-suivi" >}})
qui ponctuent les travaux notés en sont l'application directe&nbsp;: une
conversation sur ce que vous avez livré, où l'on vous demande pourquoi,
comment, et ce qui arriverait si. L'IA y est la bienvenue partout ailleurs,
dans le code, dans les documents, dans les transcriptions que vous publierez,
et le cours vous encourage à vous en servir sans retenue. Mais la conversation,
elle, se tient sans assistance, et c'est elle qui fait la note.

## Les modules

Le cours est divisé en six modules, qui couvrent les grands domaines du génie
logiciel :

{{< modules >}}

1. **Le génie logiciel** : une introduction au domaine, à sa problématique
   centrale, et à l'histoire des idées qui l'ont façonné.

2. **Concevoir un programme correct**&nbsp;: ce que le programmeur individuel doit
   savoir et savoir faire&nbsp;: la concurrence et le parallélisme, les tests, le
   versioning avec git, la gestion des dépendances et l'intégration continue.

3. **Passer du programme au système** : le passage du programme individuel au
   système logiciel, avec ses multiples composantes en interaction. On y aborde
   l'architecture, les APIs, les interfaces utilisateur et les données.

4. **Construire un logiciel en équipe** : la collaboration à l'aide de GitHub,
   les méthodes agiles et la gestion de projet.

5. **Faire vivre un logiciel** : l'opération d'un logiciel en production, le
   déploiement, l'infonuagique, l'observabilité et la sécurité.

6. **Le logiciel dans le monde** : la culture de l'open source, l'économie du
   logiciel, et le développement assisté par l'IA.

Le nuage ci-dessous rassemble les mots les plus fréquents de l'ensemble du
cours, tous modules confondus, la taille de chacun étant proportionnelle au
nombre de ses occurrences. C'est un portrait grossier, mais assez fidèle, de ce
dont il sera question.

{{< wordcloud >}}

## Les travaux

Tout au long du cours, vous serez amenés à développer une application web
complète, de la conception au déploiement. Vous devrez d'abord imaginer une
application transactionnelle, suffisamment complexe, intéressante et novatrice,
puis en extraire les spécifications, produire un document de conception, et la
développer progressivement en mettant en pratique les concepts et les techniques
vus dans chaque module : versioning avec git, gestion de projet, base de
données, authentification, paiement en ligne (optionnel) et déploiement
automatisé sur une plateforme d'infonuagique. Le travail peut se faire
individuellement ou en petites équipes. Les détails complets se trouvent dans la
section [Travaux notés](docs/travaux-notés).
