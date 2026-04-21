---
title: "L'open source"
weight: 10
slug: "open-source"
---

# L'open source

Pratiquement tout le logiciel moderne repose sur de l'open source. Le noyau
Linux fait tourner la grande majorité des serveurs web, des téléphones Android et
des superordinateurs. Python, JavaScript, React, PostgreSQL, Docker,
Kubernetes : les outils que nous avons utilisés tout au long de ce cours sont
tous des projets open source. Quand un développeur crée une application
aujourd'hui, il écrit peut-être 5 à 10 % du code total ; le reste provient de
bibliothèques et de frameworks développés et maintenus par des communautés
ouvertes. Cette réalité est tellement omniprésente qu'on peut facilement oublier
qu'elle n'a rien de naturel. Elle est le résultat d'un mouvement qui a émergé
dans les années 1980, porté par des convictions idéologiques fortes, et qui a
profondément transformé non seulement la manière dont on produit du logiciel,
mais aussi son économie.

{{< image src="open-source.png" alt="" title="" loading="lazy" >}}

## Les origines du logiciel libre

Pour comprendre comment on en est arrivé là, il faut remonter au début des
années 1980, au laboratoire d'intelligence artificielle du MIT. À cette époque,
le partage du code source entre chercheurs et programmeurs était la norme. Quand
on recevait un logiciel, on recevait son code, et on pouvait le modifier,
l'améliorer, le redistribuer. Richard Stallman, programmeur au MIT et créateur
d'Emacs (un éditeur de texte extensible, toujours utilisé aujourd'hui, dont la
particularité est d'être programmable par ses utilisateurs via un dialecte de
Lisp), raconte souvent l'anecdote qui a cristallisé sa prise de conscience : le
laboratoire avait reçu une nouvelle imprimante Xerox qui avait la fâcheuse
habitude de coincer le papier. Avec l'ancienne imprimante, Stallman avait
modifié le logiciel pour qu'il envoie un message aux utilisateurs quand un
bourrage survenait. Mais le logiciel de la nouvelle imprimante était livré
uniquement sous forme binaire, sans code source. Impossible de le modifier.
Quand Stallman a demandé le code source à un chercheur de Carnegie Mellon qui
avait signé un accord de non-divulgation avec Xerox, celui-ci a refusé. Pour
Stallman, cet épisode illustrait un changement profond en cours dans
l'industrie : le logiciel, jusque-là partagé librement, devenait un produit
propriétaire verrouillé.

{{< image src="mit.png" alt="" title="" loading="lazy" >}}

En réponse, Stallman a lancé en 1983 le projet GNU (un acronyme récursif pour
"GNU's Not Unix"), avec l'objectif ambitieux de créer un système d'exploitation
entièrement libre. L'idée n'était pas simplement de produire du logiciel
gratuit, mais de garantir des libertés fondamentales aux utilisateurs. En 1985,
Stallman a fondé la Free Software Foundation (FSF) et formalisé sa philosophie
autour de quatre libertés : la liberté d'exécuter le programme (liberté 0), de
l'étudier et de le modifier en ayant accès au code source (liberté 1), de
redistribuer des copies (liberté 2), et de distribuer des versions modifiées
(liberté 3). Stallman insistait sur la distinction : "free as in freedom, not as
in free beer". Le logiciel libre n'est pas une question de prix, mais de droits.
Au fil des années 1980 et 1990, le projet GNU a produit des composants
essentiels qui sont toujours omniprésents aujourd'hui : le compilateur GCC, le
débogueur GDB, l'outil de build Make, et bien sûr Emacs. Il manquait cependant
une pièce cruciale : le noyau du système d'exploitation. C'est cette pièce qu'un
étudiant finlandais nommé Linus Torvalds allait fournir en 1991.

{{< image src="gnu.svg" alt="" title="" loading="lazy" >}}

Linux, que nous avons déjà rencontré dans le module 1, est né d'un message
modeste posté par Torvalds sur le groupe Usenet comp.os.minix en août 1991 :

```
From: torvalds@klaava.Helsinki.FI (Linus Benedict Torvalds)
Newsgroups: comp.os.minix
Subject: What would you like to see most in minix?
Summary: small poll for my new operating system
Message-ID:
Date: 25 Aug 91 20:57:08 GMT
Organization: University of Helsinki

Hello everybody out there using minix -

I'm doing a (free) operating system (just a hobby, won't be big and
professional like gnu) for 386(486) AT clones.  This has been brewing
since april, and is starting to get ready.  I'd like any feedback on
things people like/dislike in minix, as my OS resembles it somewhat
(same physical layout of the file-system (due to practical reasons)
among other things).

I've currently ported bash(1.08) and gcc(1.40), and things seem to work.
This implies that I'll get something practical within a few months, and
I'd like to know what features most people would want.  Any suggestions
are welcome, but I won't promise I'll implement them :-)

              Linus (torvalds@kruuna.helsinki.fi)

PS.  Yes - it's free of any minix code, and it has a multi-threaded fs.
It is NOT protable (uses 386 task switching etc), and it probably never
will support anything other than AT-harddisks, as that's all I have :-(.
```

Le noyau Linux, combiné aux outils GNU, a formé le premier système
d'exploitation entièrement libre et fonctionnel, souvent appelé GNU/Linux (une
appellation sur laquelle Stallman insiste, mais que la plupart des gens
raccourcissent simplement à "Linux"). Ce qui distinguait Linux des projets qui
l'avaient précédé, c'était moins sa qualité technique initiale que son modèle de
développement. Torvalds acceptait les contributions de quiconque voulait
participer, publiait des versions fréquemment, et laissait les utilisateurs
eux-mêmes identifier et corriger les bogues. Ce modèle, chaotique en apparence,
allait se révéler remarquablement efficace.

Il faut noter que le logiciel libre de Stallman n'était pas la seule alternative
au modèle propriétaire dominant. Durant les années 1980 et 1990, le *shareware*
offrait un compromis populaire : le logiciel était distribué gratuitement
(souvent sur des disquettes, puis via des BBS et des CD-ROM), mais l'utilisateur
était invité à payer après une période d'essai. Des logiciels comme DOOM (id
Software, 1993), WinZip ou WinRAR ont été distribués de cette manière. Le
shareware partageait le programme, mais pas le code source : c'était un modèle
de distribution commerciale, pas un mouvement pour la liberté du logiciel. Nous y
reviendrons dans la section sur l'économie du logiciel. Le mouvement du logiciel
libre, lui, allait prendre une direction très différente, portée par une
réflexion sur le *processus* de développement lui-même.

## De "libre" à "open source"

En 1997, Eric Raymond a publié *The Cathedral and the Bazaar*, un essai qui
allait redéfinir la manière dont on parlait du logiciel libre. Raymond y opposait
deux modèles de développement. Le modèle de la *cathédrale*, celui de GNU et de
la plupart des projets logiciels traditionnels, où le code est développé par un
petit groupe d'architectes entre les releases, dans un processus soigneusement
contrôlé. Et le modèle du *bazar*, celui de Linux, où le code est ouvert en
permanence, les versions sont fréquentes, et la coordination émerge de manière
organique d'une communauté large et décentralisée. La conclusion de Raymond
était contre-intuitive : le bazar fonctionnait mieux. Il a formulé ce constat
sous la forme de la "loi de Linus" : "given enough eyeballs, all bugs are
shallow" (avec suffisamment d'yeux, tous les bogues sont superficiels). L'idée
est que plus il y a de personnes qui lisent et testent le code, plus les erreurs
sont détectées rapidement. C'est un argument qui fait écho au concept de code
review que nous avons vu dans le module 4, mais poussé à l'échelle d'une
communauté entière.

L'essai de Raymond a eu un impact concret et immédiat, et c'est dans le monde
des navigateurs web qu'il s'est d'abord manifesté. En janvier 1998, Netscape, en
difficulté face à Internet Explorer de Microsoft dans la "guerre des
navigateurs", a annoncé qu'elle allait libérer le code source de son navigateur.
La décision était directement inspirée par *The Cathedral and the Bazaar*. C'est
le projet qui deviendra Mozilla, puis Firefox (2004), et qui démontrera qu'un
navigateur open source pouvait rivaliser avec le produit d'une des plus grandes
entreprises au monde. Ce précédent a eu des répercussions durables :
aujourd'hui, pratiquement tous les navigateurs majeurs reposent sur des moteurs
open source. Chrome utilise Chromium (Google, 2008), qui est lui-même basé sur
WebKit, un projet issu de KHTML, le moteur du navigateur Konqueror développé par
la communauté KDE. Edge de Microsoft, après des années à maintenir son propre
moteur, a adopté Chromium en 2019. Safari utilise WebKit. Seul Firefox, avec son
moteur Gecko (et plus récemment Servo, écrit en Rust), maintient une base de
code véritablement indépendante. Cette convergence vers Chromium inquiète
d'ailleurs certains observateurs, qui y voient un risque de monoculture : quand
un seul moteur domine le web, c'est Google qui dicte de facto les standards, une
tension que nous retrouverons dans la section sur les monopoles.

Raymond et d'autres figures du mouvement ont vu dans la décision de Netscape une
opportunité de repositionner le logiciel libre pour le rendre plus acceptable
aux yeux des entreprises. Le problème, selon eux, c'était le mot "free" : il
effrayait les dirigeants d'entreprise, soit parce qu'ils l'associaient à
"gratuit" (donc sans valeur), soit parce que le discours moral de Stallman sur
les libertés leur semblait radical. En février 1998, lors d'une réunion à Palo
Alto, le terme "open source" a été proposé par Christine Peterson et rapidement
adopté par Raymond, Tim O'Reilly et d'autres. L'Open Source Initiative (OSI) a
été fondée peu après pour promouvoir cette nouvelle étiquette. Pour Stallman, ce
renommage était une trahison : en évacuant la dimension éthique au profit d'un
argument purement pragmatique (l'open source produit du meilleur logiciel), on
perdait l'essentiel. Cette tension entre "logiciel libre" et "open source"
persiste encore aujourd'hui, même si dans la pratique quotidienne, la plupart
des développeurs utilisent "open source" sans se soucier de la distinction.

## Les licences open source

La philosophie du logiciel libre et de l'open source se matérialise concrètement
dans les licences. C'est la licence qui détermine ce qu'on a le droit de faire
avec un logiciel, et c'est là que se manifeste la tension entre les deux camps.
L'outil juridique inventé par Stallman pour protéger le logiciel libre est le
*copyleft*, incarné par la GNU General Public License (GPL). L'idée du copyleft
est astucieuse : on utilise le droit d'auteur, non pas pour restreindre la
redistribution, mais pour garantir que le code reste libre. Toute personne qui
modifie un logiciel sous GPL et distribue sa version modifiée doit également la
distribuer sous GPL, avec le code source. Le copyleft est donc "viral" : il se
propage aux œuvres dérivées. Linux est sous GPL, ce qui signifie que toute
distribution Linux (Ubuntu, Fedora, etc.) doit rendre son code source
disponible.

{{< image src="gpl.png" alt="" title="" loading="lazy" >}}

Face à cette approche, les licences dites *permissives* adoptent une philosophie
différente : elles imposent très peu de contraintes. La licence MIT, la licence
BSD et la licence Apache permettent à quiconque d'utiliser, de modifier et de
redistribuer le code, y compris dans un produit propriétaire, à condition de
conserver la mention de copyright originale. C'est ce qui permet à Apple
d'intégrer du code BSD dans macOS, ou à des entreprises d'utiliser React
(licence MIT) dans des applications commerciales sans aucune obligation de
partager leur propre code. Un épisode révélateur : en 2017, Facebook distribuait
React sous une licence BSD modifiée qui incluait une clause de brevet
controversée. Sous la pression de la communauté (et notamment d'Apache Foundation
qui avait interdit cette licence), Facebook a basculé React vers une licence MIT
standard. Ce genre de décision peut sembler abstrait, mais il a des conséquences
très concrètes pour quiconque construit un produit qui dépend de ces
bibliothèques.

Cette question des licences n'est pas qu'un sujet juridique abstrait : elle est
au cœur de tensions récurrentes entre les entreprises et les communautés open
source. Un pattern s'est répété plusieurs fois au cours des dernières années :
une entreprise construit un produit open source populaire, attire une large
communauté de contributeurs et d'utilisateurs, puis restreint sa licence quand
des fournisseurs cloud (en particulier AWS) commencent à offrir ce produit comme
service géré, captant les revenus sans contribuer en retour. MongoDB est passé de
la licence AGPL à la SSPL en 2018. Elasticsearch a quitté la licence Apache 2.0
en 2021 pour la même raison, ce qui a poussé AWS à créer un fork nommé
OpenSearch. HashiCorp a changé la licence de Terraform de MPL à BSL en 2023, et
la communauté a répondu en créant OpenTofu sous l'égide de la Linux Foundation.
Redis a suivi le même chemin en 2024, menant au fork Valkey. Dans chaque cas, le
même dilemme : l'entreprise estime que les cloud providers exploitent son travail
sans réciprocité, tandis que la communauté estime que le changement de licence
trahit la promesse originale de l'open source. Ext JS (Sencha) avait illustré ce
type de tension dès le début des années 2010, en passant progressivement d'une
licence permissive à un modèle commercial. Ces épisodes montrent que la licence
n'est pas un détail technique qu'on choisit une fois pour toutes : c'est un
contrat social qui peut devenir un champ de bataille.

## L'économie de l'open source

Si le code est gratuit, comment gagne-t-on sa vie ? Cette question, qui semblait
naïve dans les années 1990, est devenue l'un des problèmes les plus complexes de
l'industrie du logiciel. Stallman avait une réponse simple : on vend des services
(support, formation, personnalisation), pas le logiciel lui-même. Red Hat,
fondée en 1993, a été la première grande validation de ce modèle. L'entreprise
distribuait gratuitement sa distribution Linux, mais vendait du support, des
certifications et des garanties de stabilité aux entreprises. Le modèle a
fonctionné au point qu'IBM a acquis Red Hat pour 34 milliards de dollars en 2019,
la plus grande acquisition de l'histoire du logiciel à l'époque.

D'autres modèles ont émergé. Le *dual licensing* consiste à offrir le logiciel
sous une licence copyleft (GPL) pour l'usage communautaire, et sous une licence
commerciale pour les entreprises qui ne veulent pas être soumises aux obligations
du copyleft. MySQL (maintenant détenu par Oracle) a popularisé cette approche. Le
modèle *open core* propose un noyau open source gratuit, complété par des
fonctionnalités premium propriétaires. GitLab, Elastic (avant son changement de
licence) et Grafana utilisent ce modèle. Enfin, le modèle *SaaS* (Software as a
Service) consiste à offrir le logiciel open source comme service hébergé : le
code est ouvert, mais la commodité de ne pas avoir à le déployer et le maintenir
soi-même a une valeur que les clients sont prêts à payer. C'est le modèle de
GitHub (avant son rachat par Microsoft), de Automattic (WordPress.com) et de
nombreuses startups modernes. Nous approfondirons ces modèles économiques dans la
section suivante sur l'économie du logiciel.

## La fragilité cachée de l'open source

La "loi de Linus" affirme qu'avec suffisamment d'yeux, tous les bogues sont
superficiels. Mais que se passe-t-il quand personne ne regarde ? Derrière la
façade de projets massifs comme Linux ou Kubernetes, une grande partie de
l'infrastructure open source repose sur des bibliothèques modestes, maintenues
par une poignée de personnes, souvent bénévolement, dans leur temps libre.
Plusieurs incidents ont mis en lumière cette fragilité.

En 2014, la faille Heartbleed a révélé une vulnérabilité critique dans OpenSSL,
la bibliothèque de chiffrement utilisée par une grande partie du web. Le bogue,
présent dans le code depuis deux ans, permettait à un attaquant de lire la
mémoire des serveurs, exposant potentiellement des mots de passe, des clés
privées et d'autres données sensibles. La découverte a mis en lumière un fait
troublant : OpenSSL, dont dépendaient des millions de serveurs, était maintenu
essentiellement par deux développeurs, avec un budget annuel d'environ 2000
dollars en dons. L'incident a mené à la création de la Core Infrastructure
Initiative (Linux Foundation), puis de l'Open Source Security Foundation
(OpenSSF), pour tenter de financer les projets critiques.

En 2016, un développeur nommé Azer Koçulu a retiré du registre npm un paquet
appelé left-pad, une bibliothèque de 11 lignes de code qui ajoutait des espaces
à gauche d'une chaîne de caractères. Des milliers de projets en dépendaient,
directement ou indirectement, et leur build a instantanément cassé. L'incident a
révélé la fragilité de l'écosystème des dépendances : une pyramide immense
reposant parfois sur des micro-paquets maintenus par une seule personne. C'est le
problème de la chaîne d'approvisionnement logicielle que nous avons abordé dans
le module 2.

Le cas le plus inquiétant est peut-être celui de xz Utils en 2024. Un
contributeur opérant sous le pseudonyme "Jia Tan" a patiemment gagné la
confiance du mainteneur solitaire du projet xz, une bibliothèque de compression
utilisée dans pratiquement toutes les distributions Linux. Après des années de
contributions légitimes, Jia Tan a introduit une porte dérobée (backdoor)
sophistiquée qui aurait pu compromettre des millions de serveurs. La backdoor a
été découverte par accident, par un développeur de Microsoft qui a remarqué que
les connexions SSH étaient anormalement lentes. L'attaque exploitait précisément
la vulnérabilité sociale de l'open source : un mainteneur épuisé, soulagé de
recevoir enfin de l'aide, avait progressivement cédé les droits de commit à un
inconnu. C'est un sujet que nous avons également abordé dans la section sur la
sécurité du module 5.

Ces épisodes illustrent une tension fondamentale. L'open source a
spectaculairement réussi comme modèle de développement : il a produit les
logiciels les plus utilisés au monde. Mais il n'a pas résolu le problème de la
maintenance à long terme. Les développeurs créent et contribuent par passion,
mais la maintenance quotidienne (répondre aux issues, réviser les pull requests,
mettre à jour les dépendances, corriger les failles de sécurité) est un travail
ingrat qui mène à l'épuisement. Le dessin humoristique de xkcd intitulé
"Dependency" résume bien la situation :

{{< image src="xkcd-dependency.png" alt="" title="" loading="lazy" >}}

Toute l'infrastructure numérique moderne, représentée par un empilement de
blocs massifs, repose en fin de compte sur un projet maintenu bénévolement par
un inconnu quelque part. Pour certains projets open source, ceci n'est pas du tout
une exagération.