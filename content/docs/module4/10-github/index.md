---
title: "Git distribué (GitHub)"
slug: "github"
weight: 10
---

# Au-delà du git local : git distribué

Avant d'aller plus loin, il est important de bien distinguer git et GitHub, car
la confusion entre les deux est fréquente. Git est un logiciel de versioning,
créé par Linus Torvalds en 2005, qui fonctionne entièrement en local sur votre
machine. GitHub est un service web, fondé en 2008 par Tom Preston-Werner, Chris
Wanstrath et PJ Hyett, qui héberge des dépôts git en ligne et ajoute par-dessus
une couche de fonctionnalités collaboratives : pull requests, code reviews,
gestion d'issues, et bien d'autres. Git peut fonctionner sans GitHub, et il
existe d'autres services similaires (GitLab, Bitbucket). Mais GitHub est devenu,
de loin, la plateforme dominante. Son rachat par Microsoft en 2018 pour 7,5
milliards de dollars témoigne de cette centralité. Aujourd'hui, GitHub n'est pas
seulement un hébergeur de code : c'est le lieu où se trouvent les projets open
source majeurs, où se discutent les décisions techniques, où se construisent les
réputations professionnelles. Comprendre GitHub, c'est comprendre comment les
développeurs collaborent.

Jusqu'ici nous avons utilisé git en mode local, c'est-à-dire que la totalité des
opérations que nous avons effectuées sont confinées dans le contexte particulier
de notre dépôt local, dans un endroit particulier de notre disque, sur un
ordinateur particulier. Mais le modèle de git est beaucoup plus puissant et
général, car il permet de synchroniser des versions différentes du même dépôt, à
travers le réseau internet. On dit que le modèle est _distribué_. Ce mode est
évidemment optionnel, et il est tout à fait possible d'utiliser git de manière
exclusivement locale, si ça correspond à notre besoin. Mais dans un contexte de
collaboration pour le développement logiciel, le mode distribué de git est
quasiment essentiel. Une bonne manière de commencer notre exploration de cette
nouvelle idée est en étendant notre modèle mental des trois "endroits" du git
local avec un quatrième "endroit", qui correspond à une autre version du même
depot, qui se trouve "ailleurs" :

{{< image src="git-4-places.png" alt="" title="" loading="lazy" >}}

Il est important de comprendre que cet "ailleurs" peut être en fait plusieurs types d'endroit :

1. Un autre répertoire sur le même ordinateur
2. Un autre ordinateur (par exemple un serveur en ligne)
3. Un service d'hébergement en ligne pour git, par exemple GitHub, qui est de loin le plus populaire.

Fondamentalement tous ces endroits fonctionnent de la même manière (pour
communiquer entre eux), mais nous allons nous concentrer sur l'usage avec
GitHub, qui est le plus courant et utile. Jusqu'ici nous avons travaillé dans
notre dépôt local, mais imaginons que nous aimerions collaborer avec d'autres
programmeurs. Pour cela, il est très courant d'utiliser GitHub. Créons tout
d'abord un nouveau dépôt dans notre compte GitHub :

{{< image src="git-gh-create-repo.png" alt="" title="" loading="lazy" >}}

GitHub nous offre ensuite deux scénarios :

{{< image src="git-gh-create-repo-2-options.png" alt="" title="" loading="lazy" >}}

1. Nous avons créé ce dépôt entièrement en ligne, et il est donc nouveau (nous en voudrions donc une copie locale, pour pouvoir y travailler)
2. Nous avons déjà un dépôt local existant, et nous aimerions que ce dépôt en ligne que nous venons de créer (sur GitHub) y soit associé

Dans notre scénario d'apprentissage, nous sommes dans l'option 2 (assurez-vous
de vous arrêter un moment pour y penser, et vous en convaincre, car les nuances
topologiques des dépôts git distribués peuvent devenir difficile à se
représenter).

Effectuons donc les commandes recommandées par GitHub, dans la ligne de commande
de notre dépôt local :

```shell
$ git remote add origin git@github.com:cjauvin/mon-premier-depot.git
```

Avec cette commande, nous avons créé un "remote", nommé `origin` qui est
simplement un lien (url), de notre dépôt local, vers un dépôt distant (remote
veut dire distant, souvent en ligne).

On peut constater l'ajout de ce lien dans le fichier `.git/config` de notre
dépôt local :

```shell
$ cat .git/config
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
[remote "origin"]
        url = git@github.com:cjauvin/mon-premier-depot.git
        fetch = +refs/heads/*:refs/remotes/origin/*
```

La deuxième commande, `git branch -M main`, renomme simplement la branche
locale de `master` (le nom historique par défaut de git) à `main` (le nouveau
nom par défaut sur GitHub), pour que les deux soient synchronisés.

La troisième commande va envoyer (push) notre branche locale `main`
vers le remote `origin`, afin de synchroniser les deux dépôts :

```shell
$ git push -u origin main
Enumerating objects: 27, done.
Counting objects: 100% (27/27), done.
Delta compression using up to 10 threads
Compressing objects: 100% (16/16), done.
Writing objects: 100% (27/27), 2.23 KiB | 1.11 MiB/s, done.
Total 27 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (1/1), done.
To github.com:cjauvin/mon-premier-depot.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

L'option `-u` (pour "upstream") en particulier est cruciale, car elle permet de
faire une association directe entre la branche locale `main` et la branche en
ligne correspondante, `origin/main`. Donc dans le contexte de la branche locale
`main`, nous n'aurons pas à spécifier de quel remote en particulier on parle,
quand on voudra faire les commandes `git push` et `git pull`, car l'association
sera implicite.

Si on rafraîchit maintenant la page du dépôt sur GitHub, on devrait voir ceci :

{{< image src="git-gh-repo-ready.png" alt="" title="" loading="lazy" >}}

Et si on visite la section des commits en particulier, on peut voir l'historique
de notre dépôt local, qui se retrouve maintenant intégralement dans la version
du dépôt en ligne sur GitHub :

{{< image src="git-gh-commit-history.png" alt="" title="" loading="lazy" >}}

Nous allons maintenant explorer les possibilités qu'offre le fait d'avoir un
dépôt en ligne, dans le contexte d'un groupe de collaborateurs. Imaginons que
nous sommes Leila, jusqu'à maintenant, et qu'une deuxième collaboratrice, nommée
Sara, voudrait se joindre à notre projet, pour y contribuer. Pour simuler cela,
nous allons simplement imaginer que Sara voudrait travailler sur le même
ordinateur (local) que celui de Leila, mais dans un autre répertoire, ailleurs
sur le disque donc (ce que git permet très aisément, avec ou sans dépôt en ligne
d'ailleurs). Sara va donc "cloner" le dépôt en ligne, de GitHub vers un autre
endroit sur l'ordinateur local :

```shell
$ cd /espace/de/travail/de/sara/
$ git clone git@github.com:cjauvin/mon-premier-depot.git meme-depot-ailleurs
Cloning into 'meme-depot-ailleurs'...
remote: Enumerating objects: 27, done.
remote: Counting objects: 100% (27/27), done.
remote: Compressing objects: 100% (15/15), done.
remote: Total 27 (delta 1), reused 27 (delta 1), pack-reused 0 (from 0)
Receiving objects: 100% (27/27), done.
Resolving deltas: 100% (1/1), done.
```

Notons que quand on clone un dépôt, on peut choisir le nom que l'on veut pour le
répertoire qui le contient. Dans ce cas nous avons choisi `meme-depot-ailleurs`
pour réduire la confusion, mais si on avait utilisé la commande `git clone` sans
spécifier de nom, un nouveau répertoire `mon-premier-depot` serait
automatiquement créé et utilisé. C'est pourquoi il est préférable d'avoir
navigué au préalable vers `/un/autre/endroit/du/disque/`.

Nous nous retrouvons donc dans la situation suivante :

{{< image src="git-3-repos.png" alt="" title="" loading="lazy" >}}

Supposons maintenant que Sara souhaite faire un changement au code de son nouveau
dépôt :

```shell
$ echo "de Sara!" >> toto.txt
$ git commit -am "Neuvième commit (de Sara)"
[main 878933d] Neuvième commit (de Sara)
 1 file changed, 1 insertion(+)
```

Comment sera-t-il possible pour Leila de prendre connaissance de son travail? Il faut
passer par le dépôt en ligne, sur GitHub :

```shell
$ git push
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 10 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 330 bytes | 330.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To github.com:cjauvin/mon-premier-depot.git
   55f1243..878933d  main -> main
```

On remarque que Sara (qui vient de faire la commande `git push` dans son dépôt)
n'a pas eu à se préoccuper de la configuration du remote `origin`, ni de
l'association de sa branche locale `main` avec la branche `origin/main`, car le
fait d'avoir utilisé `clone` effectue cette configuration initiale,
automatiquement.

Si on rafraîchit maintenant la page des commits de notre dépôt en ligne sur GitHub,
on devrait voir apparaître le commit de Sara, qu'elle vient de "pousser" (`push`) :

{{< image src="git-gh-commit-sara.png" alt="" title="" loading="lazy" >}}

À ce point dans notre histoire, le nouveau commit de Sara (`8789`, pour être précis)
se trouve dans deux dépôts : le sien, et celui de GitHub. Pour que Leila puisse l'obtenir,
elle doit faire `git pull` dans son propre dépôt :

```shell
$ git pull
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 310 bytes | 62.00 KiB/s, done.
From github.com:cjauvin/mon-premier-depot
   55f1243..878933d  main       -> origin/main
Updating 55f1243..878933d
Fast-forward
 toto.txt | 1 +
 1 file changed, 1 insertion(+)
 ```

 Les trois dépôts sont maintenant synchronisés :

{{< image src="git-3-repos-synced.png" alt="" title="" loading="lazy" >}}

## Collaborer avec git et GitHub

Nous allons finalement explorer une variation plus réaliste d'un mécanisme de
collaboration rendu possible par git et GitHub : la "pull request".

Supposons que Sara veuille encore une fois collaborer au projet, mais cette fois
elle aimerait le faire d'une manière qui impliquerait Leila de manière plus
active, en lui "demandant la permission" (dans un certain sens), d'effectuer une
modification. Sara pourrait commencer en créant une branche dans son dépôt local :

```shell
$ git switch -c proposition
Switched to a new branch 'proposition'
```

Elle pourrait alors effectuer son travail, le commiter, et pousser sa nouvelle
branche vers le dépôt en ligne GitHub :

```shell
$ echo "c'est nouveau!" >> sara.txt
$
$ git add sara.txt
$
$ git commit -m "Dixième commit (de Sara)"
[proposition 5998c71] Dixième commit (de Sara)
 1 file changed, 1 insertion(+)
 create mode 100644 sara.txt
$
$ git push --set-upstream origin proposition
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 10 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 336 bytes | 336.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
remote:
remote: Create a pull request for 'proposition' on GitHub by visiting:
remote:      https://github.com/cjauvin/mon-premier-depot/pull/new/proposition
remote:
To github.com:cjauvin/mon-premier-depot.git
 * [new branch]      proposition -> proposition
branch 'proposition' set up to track 'origin/proposition'.
```

Après avoir fait cela, Sara devrait voir une option apparaître dans le dépôt GitHub,
après l'avoir rafraîchi :

{{< image src="git-gh-pr-offer.png" alt="" title="" loading="lazy" >}}

Elle peut ensuite préparer sa pull request (PR), en faisant une description et
en expliquant le contexte (peut-être qu'il s'agit d'un bogue qu'elle a remarqué,
et pour lequel elle aimerait proposer une correction). Elle peut souvent
assigner un "reviewer", qui sera en charge de faire l'évaluation de la PR, et de
déterminer si elle sera acceptée ou non. Imaginons que ce reviewer devrait être
Leila.

{{< image src="git-gh-pr.png" alt="" title="" loading="lazy" >}}

Leila pourra ensuite entrer en jeu : elle recevra la PR, pourra examiner les
changements, commenter, demander des changements supplémentaires, et finalement
l'accepter ou la refuser :

{{< image src="git-gh-pr-suite.png" alt="" title="" loading="lazy" >}}

Notez qu'une PR est souvent un lieu de conversation, parfois très longue, et qui
peut être particulièrement animée !

Si Leila accepte le travail effectué par Sara (donc la PR), la branche
`proposition` sera "mergée" dans la branche `main` (tout cela se passe toujours
dans le dépôt en ligne GitHub) :

{{< image src="git-gh-pr-merged.png" alt="" title="" loading="lazy" >}}

Après le merge de la PR, si on consulte la page des commits (de la branche `main`), on constate qu'un
nouveau commit, est apparu, en plus du commit correspondant au travail de Sara à
proprement parlé :

{{< image src="git-gh-pr-merge-commit.png" alt="" title="" loading="lazy" >}}

Notez qu'un nouveau commit correspondant au merge est parfois nécessaire dans
certains contextes (quand git ne peut pas effecter un merge de type
"fast-forward", qui est le type le plus simple).

Pour avoir la version la plus récente du travail effectué (sur la branche
`main`), Leila doit faire un pull dans son dépôt local :

```shell
$ git pull
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 1), reused 2 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (4/4), 1.08 KiB | 158.00 KiB/s, done.
From github.com:cjauvin/mon-premier-depot
   878933d..e58cc7a  main        -> origin/main
 * [new branch]      proposition -> origin/proposition
Updating 878933d..e58cc7a
Fast-forward
 sara.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 sara.txt
$
$ git log -1
commit e58cc7a8a34ccf66158cc05c98bfd2700e7fba04 (HEAD -> main, origin/main, origin/HEAD)
Merge: 878933d 5998c71
Author: Christian Jauvin <cjauvin@gmail.com>
Date:   Wed Jan 28 11:44:47 2026 -0500

    Merge pull request #1 from cjauvin/proposition

    Proposition d'une nouvelle fonction
```

Et finalement, Sara doit également rafraîchir son dépôt local, même si c'est
elle qui a fait le travail, car sa branche `main` locale ne contient pas encore
le commit final de merge, ajouté par git, dans le dépôt en ligne GitHub. Elle
doit tout d'abord switcher à sa branche locale `main` (de sa branche
`proposition`), et ensuite la rafraîchir :

```shell
$ git switch main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
$
$ git pull
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 1 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (1/1), 909 bytes | 454.00 KiB/s, done.
From github.com:cjauvin/mon-premier-depot
   878933d..e58cc7a  main       -> origin/main
Updating 878933d..e58cc7a
Fast-forward
 sara.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 sara.txt
$
$ git log -1
commit e58cc7a8a34ccf66158cc05c98bfd2700e7fba04 (HEAD -> main, origin/main, origin/HEAD)
Merge: 878933d 5998c71
Author: Christian Jauvin <cjauvin@gmail.com>
Date:   Wed Jan 28 11:44:47 2026 -0500

    Merge pull request #1 from cjauvin/proposition

    Proposition d'une nouvelle fonction
```

Ce scénario simple illustre le mécanisme de base de la collaboration avec git et
GitHub. Mais dans la pratique, une équipe doit répondre à des questions plus
larges : comment organiser ses branches ? Que devrait-on vérifier dans une code
review ? Comment s'assurer que le code qui arrive dans la branche principale est
toujours fonctionnel ? Ce sont ces questions que nous allons aborder maintenant.

## Les workflows git

Dans le scénario précédent, Sara a créé une branche, fait son travail, et ouvert
une pull request. C'est le patron de base. Mais quand une équipe de cinq, dix ou
cinquante développeurs travaille sur le même projet, il faut des conventions plus
précises : quand crée-t-on une branche ? Comment la nomme-t-on ? Qui a le droit
de merger dans `main` ? Plusieurs modèles de workflows ont émergé au fil des
années pour répondre à ces questions.

Le premier modèle formalisé est **Git Flow**, proposé par Vincent Driessen en
2010 dans un billet de blog devenu célèbre. Git Flow définit une structure de
branches rigide : une branche `main` qui contient uniquement le code en
production, une branche `develop` qui sert de branche d'intégration, des
branches `feature/*` pour chaque nouvelle fonctionnalité, des branches
`release/*` pour préparer les mises en production, et des branches `hotfix/*`
pour les correctifs urgents. Ce modèle avait le mérite de la clarté : chaque
branche a un rôle précis, et le flux de travail est entièrement prédéfini. Mais
dans la pratique, beaucoup d'équipes ont trouvé Git Flow trop lourd, avec trop
de branches à gérer et trop de cérémonies de merge. Driessen lui-même a ajouté
une note à son billet original, reconnaissant que ce modèle n'est pas adapté aux
équipes qui pratiquent le déploiement continu.

En réaction à cette complexité, GitHub a proposé un modèle beaucoup plus simple,
connu sous le nom de **GitHub Flow**. Le principe tient en quelques règles : la
branche `main` est toujours déployable, chaque travail commence par la création
d'une branche à partir de `main`, on ouvre une pull request dès que le travail
est prêt à être discuté, et on ne merge dans `main` qu'après une code review.
C'est essentiellement ce que nous avons fait avec Leila et Sara. La simplicité
de ce modèle le rend adapté à la majorité des projets, en particulier ceux qui
pratiquent le déploiement continu, où chaque merge dans `main` déclenche
automatiquement une mise en production.

Le **trunk-based development** pousse cette simplicité encore plus loin. Dans ce
modèle, les développeurs travaillent directement sur la branche principale (le
"trunk"), ou sur des branches très courtes qui ne vivent que quelques heures.
L'idée centrale est d'éviter les branches longues, qui divergent inévitablement
du tronc et créent des merges douloureux. Ce modèle exige en contrepartie une
discipline forte : des tests automatisés solides, de l'intégration continue, et
souvent l'usage de "feature flags" pour masquer les fonctionnalités en cours de
développement dans le code déployé. C'est le modèle utilisé par Google et
d'autres grandes entreprises technologiques.

<!-- ILLUSTRATION: comparaison visuelle des trois workflows git (Git Flow, GitHub Flow, trunk-based) -->

## Les code reviews

Nous avons vu que la pull request est le mécanisme par lequel un développeur
propose des changements à une base de code. Mais le vrai travail commence quand
un autre membre de l'équipe examine ces changements. La code review est une des
pratiques les plus importantes du développement en équipe, et pourtant elle est
souvent mal comprise. Il ne s'agit pas simplement de vérifier que le code
"fonctionne" : les tests automatisés s'en chargent. La code review est un acte
de communication. C'est un moment où deux personnes construisent une
compréhension partagée du code, de ses intentions, de ses compromis.

L'idée de faire relire le code par un pair n'est pas nouvelle. Michael Fagan,
chez IBM, a formalisé les "inspections de code" dès 1976, avec un processus
rigoureux impliquant des rôles définis et des réunions structurées. Les code
reviews modernes, facilitées par les outils comme GitHub, sont plus légères mais
poursuivent les mêmes objectifs. On y cherche plusieurs choses : la correction
logique (est-ce que ce code fait ce qu'il est censé faire ?), la lisibilité
(est-ce qu'un autre développeur comprendra ce code dans six mois ?), la
cohérence avec le reste du projet (conventions de nommage, patterns utilisés), et
les problèmes potentiels de performance ou de sécurité. Mais au-delà de cette
checklist, la code review est aussi un mécanisme de diffusion des
connaissances : en lisant le code des autres, on apprend le système, on découvre
des techniques, on reste au courant de ce qui change.

La code review est aussi un exercice humain délicat. Recevoir des critiques sur
son code peut être vécu comme une attaque personnelle, surtout quand on débute.
Et donner des commentaires constructifs sans être condescendant est une
compétence qui s'apprend. Les équipes qui pratiquent bien la code review
développent des conventions implicites ou explicites : formuler les commentaires
comme des questions plutôt que des jugements ("est-ce qu'on pourrait simplifier
cette boucle ?" plutôt que "cette boucle est mal écrite"), distinguer les
suggestions bloquantes des suggestions optionnelles, garder les PRs petites pour
que la review soit réaliste, et se rappeler que l'objectif est d'améliorer le
code, pas de démontrer sa supériorité. Google a publié ses pratiques de code
review internes, qui sont devenues une référence dans l'industrie. Un de leurs
principes clés : un reviewer devrait approuver une PR dès qu'elle améliore
l'état général du code, même si elle n'est pas parfaite.

Ces pratiques de collaboration trouvent leur aboutissement dans les mécanismes de
protection de branches offerts par GitHub. On peut configurer la branche `main`
pour qu'elle ne puisse pas recevoir de push direct : tout changement doit passer
par une pull request. On peut exiger qu'au moins une personne ait approuvé la
review avant le merge. Et on peut exiger que les tests de CI passent avec succès
avant que le merge soit autorisé. Ces règles, configurables dans les paramètres
du dépôt GitHub, transforment les conventions d'équipe en contraintes
automatisées. C'est la rencontre entre l'intégration continue que nous avons vue
au module 2 et la collaboration que nous explorons ici : la CI ne vérifie plus
seulement le code d'un programmeur individuel, elle devient le gardien de la
branche principale d'une équipe entière.
