---
title: "Monopoles et régulation"
weight: 30
slug: "monopoles"
---

# Monopoles et régulation

Le logiciel possède une propriété économique qui favorise naturellement la
concentration : les effets de réseau. Plus un produit a d'utilisateurs, plus il
devient utile pour chaque utilisateur. Un réseau social sans vos amis ne sert à
rien. Un système d'exploitation sans applications n'intéresse personne. Cette
dynamique, combinée au coût de reproduction quasi nul que nous avons vu dans la
section précédente, crée une logique de "winner takes all" où un petit nombre
d'entreprises finit par dominer des marchés entiers. Le phénomène n'est pas
nouveau : l'industrie informatique a connu plusieurs vagues de concentration, et
à chaque fois, les gouvernements ont tenté d'intervenir, avec des résultats
mitigés. Cette section retrace l'histoire des monopoles logiciels, les
mécanismes qui les rendent possibles, et les tentatives de régulation qui
cherchent à préserver la concurrence et à protéger les utilisateurs.

## L'histoire de la concentration

L'histoire de l'industrie informatique est jalonnée de monopoles successifs, et
à chaque époque, c'est l'entreprise dominante qui a défini les règles du jeu. Le
premier grand monopole fut celui d'IBM. Dans les années 1960 et 1970, IBM
contrôlait environ 70 % du marché des ordinateurs centraux (*mainframes*). Sa
domination était si complète que l'industrie se décrivait comme "IBM and the
Seven Dwarfs" (les sept nains étant Burroughs, UNIVAC, NCR, Control Data,
Honeywell, General Electric et RCA). Le gouvernement américain avait déjà
contraint IBM en 1956 avec un *consent decree* qui l'obligeait, entre autres, à
vendre ses machines (pas seulement les louer) et à licencier ses brevets à des
conditions raisonnables. C'est la décision d'*unbundling* de 1969, que nous avons
mentionnée dans la section précédente, qui a eu l'impact le plus durable : en
séparant la tarification du matériel et du logiciel, IBM a involontairement créé
les conditions d'une industrie logicielle indépendante, ouvrant la porte à des
entreprises comme SAP, Oracle et Microsoft.

{{< image src="ibm.jpg" alt="" title="" loading="lazy" >}}

Le cas d'AT&T est peut-être encore plus révélateur de l'impact qu'un
démantèlement peut avoir sur l'innovation. AT&T détenait un monopole sur les
télécommunications aux États-Unis depuis le début du 20e siècle. Ses Bell Labs,
le laboratoire de recherche de l'entreprise, avaient produit des inventions
fondamentales : le transistor (1947), la théorie de l'information de Claude
Shannon (1948), le langage C et le système d'exploitation Unix (années 1970).
Mais un consent decree de 1956 interdisait à AT&T de commercialiser des produits
en dehors des télécommunications, ce qui explique pourquoi Unix a été distribué
quasi gratuitement aux universités, semant les graines de toute une culture de
partage du code qui allait mener au mouvement du logiciel libre. En 1982, le
département de Justice américain a forcé le démantèlement d'AT&T en sept
compagnies régionales (les "Baby Bells"). Libérée de ses restrictions, AT&T a pu
entrer sur le marché de l'informatique, mais elle a aussi commencé à
commercialiser Unix de manière plus agressive, ce qui a paradoxalement fragmenté
l'écosystème Unix (les fameuses "Unix wars" entre différentes versions
incompatibles) et ouvert un espace que Linux allait finir par occuper.

{{< image src="att.png" alt="" title="" loading="lazy" >}}

Le monopole le plus marquant pour l'industrie du logiciel est sans doute celui
de Microsoft dans les années 1990. Windows équipait plus de 90 % des ordinateurs
personnels, et Microsoft utilisait cette position dominante de manière
agressive. L'épisode le plus connu est la "guerre des navigateurs" : en
intégrant Internet Explorer directement dans Windows et en imposant des accords
d'exclusivité aux fabricants de PC, Microsoft a écrasé Netscape, qui détenait
pourtant la majorité du marché des navigateurs en 1995. Le département de
Justice américain a intenté un procès antitrust en 1998, et le juge Thomas
Penfield Jackson a conclu en 2000 que Microsoft avait abusé de sa position de
monopole. Le jugement initial ordonnait le démantèlement de Microsoft en deux
entreprises distinctes (une pour le système d'exploitation, une pour les
applications), mais cette décision a été renversée en appel, et l'affaire s'est
conclue par un accord à l'amiable en 2001. Microsoft a dû ouvrir certaines de
ses APIs et permettre aux fabricants de PC d'installer des logiciels
concurrents. L'impact réel du procès est débattu : certains estiment qu'il a
freiné les pratiques les plus agressives de Microsoft juste assez longtemps pour
que Google, Firefox et d'autres puissent émerger. D'autres soutiennent que c'est
le web lui-même, en déplaçant la valeur du système d'exploitation vers le
navigateur et les services en ligne, qui a véritablement brisé le monopole de
Microsoft.

{{< image src="ns-vs-ie.webp" alt="" title="" loading="lazy" >}}

Si les monopoles précédents étaient relativement simples à identifier (une
entreprise, un marché), la concentration actuelle est plus diffuse et plus
difficile à réguler. Les GAFAM (Google, Apple, Facebook/Meta, Amazon, Microsoft)
ne dominent pas un seul marché chacun : ils en dominent plusieurs
simultanément, et ces marchés sont interconnectés. Google contrôle environ 90 %
de la recherche web, mais aussi le navigateur dominant (Chrome), le système
d'exploitation mobile dominant (Android), la principale plateforme vidéo
(YouTube) et une infrastructure cloud majeure. Amazon domine le commerce en
ligne, mais aussi l'hébergement cloud (AWS représente environ un tiers du marché
mondial). Apple contrôle un écosystème matériel-logiciel fermé où elle est à la
fois fabricante, distributrice (App Store) et de plus en plus fournisseuse de
services. Meta possède les principaux réseaux sociaux (Facebook, Instagram,
WhatsApp). Et Microsoft, loin d'avoir décliné après le procès antitrust, s'est
réinventé comme géant du cloud (Azure), de la productivité (Microsoft 365) et,
plus récemment, de l'IA (via son investissement massif dans OpenAI). Une
stratégie commune à ces entreprises est l'acquisition comme arme
concurrentielle : Google a acheté YouTube (2006) et Android (2005), Facebook a
acheté Instagram (2012) et WhatsApp (2014), Microsoft a acheté LinkedIn (2016)
et GitHub (2018). Dans chaque cas, un concurrent potentiel a été absorbé avant
de pouvoir menacer la position dominante.

## Les mécanismes de monopole propres au logiciel

Ces concentrations ne sont pas le fruit du hasard. Le logiciel possède des
caractéristiques économiques qui favorisent naturellement la formation de
monopoles, et les comprendre aide à expliquer pourquoi la situation actuelle est
si difficile à corriger. Le premier mécanisme est l'effet de réseau, déjà
mentionné en introduction : la valeur d'un produit augmente avec le nombre de
ses utilisateurs. Un réseau social est inutile si vos proches n'y sont pas. Un
système d'exploitation attire les développeurs d'applications, et les
applications attirent les utilisateurs, dans une boucle de rétroaction que les
économistes appellent un *marché biface* (*two-sided market*). Ce concept,
formalisé par les économistes Jean Tirole (prix Nobel 2014) et Jean-Charles
Rochet, explique pourquoi les plateformes comme l'App Store ou Google Play sont
si difficiles à concurrencer : il ne suffit pas d'offrir un meilleur produit, il
faut simultanément attirer les deux côtés du marché.

Le deuxième mécanisme est le verrouillage (*lock-in*) et les coûts de changement
(*switching costs*). Une fois qu'un utilisateur ou une entreprise a investi du
temps, des données et des habitudes dans un écosystème, en changer devient
coûteux, même si une alternative supérieure existe. Une entreprise qui utilise
Microsoft 365 a ses documents en format Office, ses flux de travail dans Teams,
ses données dans OneDrive, ses scripts dans Excel. Migrer vers Google Workspace
ne signifie pas seulement apprendre de nouveaux outils : c'est convertir des
milliers de documents, reformer les employés, adapter les processus internes. Ce
coût est souvent invisible au moment du choix initial, mais il devient une
barrière considérable par la suite. Le même phénomène opère au niveau des
développeurs : une application construite sur AWS utilise des services
spécifiques (Lambda, DynamoDB, S3) dont les équivalents chez Google Cloud ou
Azure ne sont pas directement compatibles. Le choix d'un fournisseur cloud est
en pratique un engagement à long terme, ce que les fournisseurs savent très
bien, et c'est pourquoi ils offrent souvent des crédits généreux aux startups
pour les attirer dans leur écosystème dès le départ.

Le troisième mécanisme est le coût marginal quasi nul, que nous avons évoqué
dans la section sur l'économie du logiciel. Produire le premier exemplaire d'un
logiciel coûte cher, mais chaque copie supplémentaire ne coûte essentiellement
rien. Cette structure de coûts crée des économies d'échelle extrêmes : une fois
qu'une entreprise a investi dans le développement de son produit, chaque nouvel
utilisateur augmente ses revenus sans augmenter significativement ses coûts. Le
résultat est une dynamique de *winner takes all* où le premier acteur à
atteindre une masse critique d'utilisateurs peut réinvestir ses profits pour
améliorer son produit, ce qui attire encore plus d'utilisateurs, dans un cercle
vertueux pour le gagnant et vicieux pour ses concurrents. C'est ce qui explique
pourquoi tant de marchés logiciels convergent vers un ou deux acteurs dominants :
Google dans la recherche, Amazon dans le commerce en ligne, Spotify dans le
streaming musical. Les concurrents ne disparaissent pas nécessairement, mais ils
se retrouvent cantonnés à des niches ou à des marchés régionaux.

## Les tentatives de régulation

Face à cette concentration, les gouvernements ont multiplié les interventions au
cours des dernières années, avec une intensité qu'on n'avait pas vue depuis le
procès Microsoft. L'Union européenne a été la plus agressive. La Commission
européenne a infligé à Google plus de 8 milliards d'euros d'amendes entre 2017
et 2019 pour abus de position dominante : dans la recherche (favoriser ses
propres services de comparaison de prix), dans Android (imposer l'installation
de Chrome et Google Search aux fabricants de téléphones) et dans la publicité en
ligne. Plus structurellement, l'UE a adopté en 2022 le Digital Markets Act
(DMA), un règlement qui identifie des "contrôleurs d'accès" (*gatekeepers*) et
leur impose des obligations spécifiques : permettre l'installation
d'applications hors de leurs magasins officiels (*sideloading*), ne pas
favoriser leurs propres services dans les résultats de recherche, garantir
l'interopérabilité des services de messagerie, et permettre aux utilisateurs de
changer facilement leurs applications par défaut. Apple a été contrainte
d'autoriser les magasins d'applications alternatifs sur iOS en Europe, une
concession qu'elle n'avait jamais faite auparavant. Aux États-Unis, l'approche a
été plus judiciaire : le département de Justice a lancé un procès antitrust
contre Google en 2020, portant sur ses accords d'exclusivité pour être le moteur
de recherche par défaut (Google paie environ 26 milliards de dollars par an à
Apple pour cette position dans Safari). Un juge a statué en 2024 que Google
détenait un monopole illégal dans la recherche, une décision dont les
conséquences concrètes restent à déterminer.

{{< image src="ue.png" alt="" title="" loading="lazy" >}}

## La protection des données

Parallèlement à la régulation de la concurrence, une autre forme de régulation a
émergé autour de la protection des données personnelles. Le modèle économique de
plusieurs géants du logiciel repose sur la collecte et la monétisation des
données de leurs utilisateurs : Google et Meta tirent l'essentiel de leurs
revenus de la publicité ciblée, rendue possible par le profilage détaillé des
comportements en ligne. Le Règlement général sur la protection des données
(RGPD), adopté par l'Union européenne en 2016 et entré en vigueur en 2018, a
été le premier cadre réglementaire à imposer des obligations strictes à
l'échelle d'un marché majeur : consentement explicite pour la collecte de
données, droit d'accès et de rectification, droit à l'effacement ("droit à
l'oubli"), obligation de notification en cas de fuite de données, et amendes
pouvant atteindre 4 % du chiffre d'affaires mondial. Le RGPD a eu un effet
d'entraînement mondial, inspirant des législations similaires dans plusieurs
pays. Au Canada, la loi fédérale PIPEDA (Personal Information Protection and
Electronic Documents Act, 2000) encadrait déjà la collecte de données dans le
secteur privé, mais elle est largement considérée comme dépassée. Le Québec a
pris les devants avec la Loi 25 (Loi modernisant des dispositions législatives
en matière de protection des renseignements personnels), adoptée en 2021 et mise
en œuvre progressivement entre 2022 et 2024. La Loi 25 impose entre autres la
nomination d'un responsable de la protection des renseignements personnels, des
évaluations d'impact pour les projets impliquant des données sensibles, et le
consentement explicite pour la collecte. Pour les développeurs, ces lois ont des
conséquences très concrètes : la manière dont on conçoit une base de données,
dont on gère les sessions utilisateur, dont on implémente un formulaire
d'inscription, tout cela est désormais encadré par la loi.

{{< image src="snowden.jpg" alt="" title="" loading="lazy" >}}

## Questions ouvertes

Ces régulations sont encore jeunes, et plusieurs questions fondamentales restent
ouvertes. L'interopérabilité, d'abord : devrait-on obliger les plateformes à
communiquer entre elles ? Le DMA impose déjà à Meta d'ouvrir la messagerie de
WhatsApp à d'autres applications, mais les détails techniques sont complexes
(comment garantir le chiffrement de bout en bout entre deux systèmes
différents ?). La portabilité des données, ensuite : le RGPD et la Loi 25
donnent aux utilisateurs le droit de récupérer leurs données, mais en pratique,
télécharger une archive ZIP de ses publications Facebook ne permet pas de les
importer ailleurs. La portabilité réelle exigerait des formats standardisés et
des APIs d'import, ce qui n'existe pas encore dans la plupart des domaines. Le
droit à la réparation, enfin, étend la question au-delà du logiciel : Apple,
John Deere et d'autres fabricants utilisent des verrous logiciels pour empêcher
la réparation de leurs appareils par des tiers, un sujet qui a mené à
l'adoption de lois sur le droit à la réparation dans plusieurs États américains
et en Europe.

L'écrivain et activiste Cory Doctorow a proposé en 2023 le terme
*enshittification* pour décrire le cycle de vie des plateformes numériques :
dans un premier temps, la plateforme offre un service de qualité pour attirer
les utilisateurs ; puis elle dégrade progressivement l'expérience pour extraire
de la valeur au profit des annonceurs et des partenaires commerciaux ; et enfin,
elle capture toute la valeur pour elle-même, au détriment de tous. L'argument de
Doctorow est que ce cycle n'est possible que grâce aux mécanismes de lock-in que
nous avons décrits : les utilisateurs restent parce que partir coûte trop cher,
pas parce que le service reste bon. Pour Doctorow, la solution passe par
l'interopérabilité obligatoire et le démantèlement des verrous numériques, des
positions qu'il défend activement au sein de l'Electronic Frontier Foundation.

{{< image src="enshittification.png" alt="" title="" loading="lazy" >}}

L'informaticien et philosophe Jaron Lanier, pionnier de la réalité virtuelle
dans les années 1980, porte une critique encore plus fondamentale. Dans *Who
Owns the Future?* (2013), Lanier soutient que le modèle économique dominant du
web, où les services sont "gratuits" en échange des données des utilisateurs, est
structurellement inéquitable. Les grandes plateformes, qu'il appelle les
"serveurs sirènes" (*siren servers*), captent et monétisent la valeur produite
par des millions de personnes sans les rémunérer. Quand un algorithme de
traduction s'améliore grâce aux textes que des humains ont écrits, ou quand un
modèle de recommandation devient plus précis grâce aux comportements de
navigation de millions d'utilisateurs, la valeur créée est réelle, mais elle est
entièrement captée par la plateforme. La proposition de Lanier, un système de
micro-paiements qui rémunérerait les individus pour l'usage de leurs données,
reste controversée et difficile à implémenter, mais elle pose une question que la
simple régulation de la concurrence ne résout pas : qui devrait bénéficier de la
valeur créée par les données collectives ?

{{< image src="jaron-lanier.jpg" alt="" title="" loading="lazy" >}}

Ces débats montrent que la régulation du logiciel est un chantier en cours, où
les réponses législatives peinent à suivre le rythme de l'innovation
technologique. C'est aussi un domaine où les ingénieurs logiciels ne sont pas de
simples spectateurs : les choix techniques qu'ils font (formats ouverts ou
propriétaires, APIs documentées ou fermées, collecte minimale ou maximale de
données) ont des conséquences directes sur la capacité des utilisateurs à
exercer leurs droits.
