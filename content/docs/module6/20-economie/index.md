---
title: "L'économie du logiciel"
weight: 20
slug: "economie"
---

# L'économie du logiciel

Le logiciel est partout, mais comment génère-t-il de la valeur économique ? La
question peut sembler simple, mais elle cache une particularité fondamentale : le
logiciel a un coût de reproduction essentiellement nul. Copier un programme ne
coûte rien. C'est ce qui distingue radicalement l'économie du logiciel de celle
des biens physiques, et c'est ce qui explique pourquoi l'industrie a passé des
décennies à chercher le bon modèle. Comment faire payer quelque chose qui se
copie gratuitement ? Comme nous l'avons vu dans la section précédente, l'open
source a proposé une réponse radicale : ne pas faire payer le logiciel lui-même,
mais les services autour. Mais l'open source n'est qu'un modèle parmi d'autres.
Cette section retrace l'évolution des manières de vendre du logiciel, depuis les
premières licences propriétaires jusqu'aux abonnements cloud, en passant par le
shareware, le freemium et les marketplaces d'applications.

## Du logiciel en boîte au shareware

Avant que le logiciel ne devienne une industrie à part entière, il était
indissociable du matériel. Dans les années 1960 et 1970, les fabricants
d'ordinateurs comme IBM vendaient des machines, et le logiciel était inclus,
souvent avec le code source. C'est le consent decree de 1956, puis surtout la
décision d'IBM en 1969 de séparer la tarification du matériel et du logiciel (le
*unbundling*), qui a créé les conditions d'une industrie logicielle autonome.
Des entreprises comme SAP (fondée en 1972 par d'anciens employés d'IBM en
Allemagne) et Oracle (1977) ont bâti des empires sur la vente de licences
perpétuelles : le client payait un montant initial élevé pour le droit d'utiliser
le logiciel, puis un frais annuel de maintenance pour les mises à jour et le
support. Microsoft a poussé ce modèle encore plus loin avec Windows et Office,
vendus en boîte dans les magasins d'informatique, un modèle que les anglophones
appellent *shrink-wrap software* (du film plastique qui emballait la boîte). Au
Québec, des entreprises comme CGI (fondée à Québec en 1976) et DMR (fondée à
Montréal en 1973, acquise par Fujitsu en 2002) se sont positionnées sur un
créneau complémentaire : plutôt que de vendre des produits logiciels, elles
vendaient des services de développement sur mesure et de consultation, un modèle
qui reste dominant dans le secteur des TI au Québec.

{{< image src="cgi.jpg" alt="" title="" loading="lazy" >}}

Parallèlement au logiciel propriétaire vendu en boîte, le shareware a représenté
une expérimentation économique fascinante. Comme nous l'avons mentionné dans la
section sur l'open source, le shareware distribuait le programme gratuitement,
mais demandait un paiement volontaire après une période d'essai. Ce qui rendait
ce modèle possible, c'était la nature même du logiciel : un bien qui se copie
sans coût. Plutôt que de lutter contre la copie, le shareware l'utilisait comme
canal de distribution. Les disquettes circulaient de main en main, les fichiers
se retrouvaient sur les BBS (Bulletin Board Systems) et les CD-ROM de
compilation vendus en kiosque. Le modèle reposait sur la confiance et la bonne
foi : un écran de rappel au démarrage, parfois une fonctionnalité limitée, mais
rarement un vrai verrou. DOOM (id Software, 1993) a poussé cette logique à
l'extrême en distribuant gratuitement le premier épisode du jeu, puis en vendant
les suivants. Ce modèle, qu'on appellerait aujourd'hui *freemium*, a été un
succès commercial majeur. Le shareware a progressivement disparu avec l'arrivée
du web, qui a rendu la distribution numérique triviale et ouvert la voie à des
modèles plus sophistiqués. Mais il a laissé une idée durable : donner le produit
pour vendre autre chose. L'industrie du jeu vidéo a d'ailleurs été un
laboratoire pour pratiquement tous les modèles économiques du logiciel. Du
shareware de DOOM, elle est passée aux abonnements mensuels (World of Warcraft,
2004), puis au *free-to-play* financé par des microtransactions (Fortnite, League
of Legends), et enfin aux abonnements de type catalogue (Xbox Game Pass). Chaque
transition reflétait un changement technologique : l'arrivée du haut débit a
rendu le jeu en ligne viable, et les smartphones ont créé un marché de masse
pour les jeux gratuits.

{{< image src="doom.jpg" alt="" title="" loading="lazy" >}}

## Le logiciel comme service

La transformation la plus profonde de l'économie du logiciel est venue d'une
idée simple : et si, au lieu de vendre un programme que le client installe sur sa
machine, on lui vendait l'accès à ce programme via Internet ? Salesforce, fondée
en 1999 par Marc Benioff (un ancien cadre d'Oracle), a été la première
entreprise à bâtir un empire sur cette proposition. Son slogan, "No Software"
(accompagné d'un logo montrant le mot "software" barré), résumait la promesse :
plus besoin d'installer, de configurer ou de mettre à jour quoi que ce soit. Le
logiciel tourne sur les serveurs du fournisseur, et le client y accède via son
navigateur web. Le modèle économique passe de la licence perpétuelle à
l'abonnement mensuel ou annuel, ce qui transforme un revenu ponctuel en revenu
récurrent. Pour le fournisseur, c'est une révolution : la prévisibilité du
revenu permet de planifier, d'investir, et de lever du capital. Pour le client,
c'est la fin des migrations douloureuses entre versions majeures, puisque tout le
monde utilise toujours la dernière version. Ce modèle, le SaaS (Software as a
Service), est devenu le modèle dominant de l'industrie logicielle. Microsoft
lui-même a pivoté : Office, autrefois vendu en boîte pour quelques centaines de
dollars, est devenu Microsoft 365, un abonnement. Adobe a fait de même avec
Creative Suite devenu Creative Cloud. Cette transition n'a pas été sans
friction : quand Adobe a annoncé en 2013 qu'il n'y aurait plus de version
perpétuelle de Photoshop, la communauté créative a protesté vigoureusement, mais
le modèle s'est imposé.

Le SaaS a aussi donné naissance à un phénomène plus large : les plateformes.
L'App Store d'Apple (2008) et Google Play ont créé un nouveau type
d'intermédiaire : le *marketplace*, un magasin numérique qui met en contact les
développeurs et les utilisateurs, et qui prélève une commission sur chaque
transaction. La commission de 30 % imposée par Apple est devenue un sujet de
controverse majeur, menant notamment au procès Epic Games v. Apple en 2021. Mais
au-delà des marketplaces destinées aux utilisateurs finaux, une autre forme de
plateforme a émergé : l'*API economy*. Des entreprises comme Stripe (paiements
en ligne), Twilio (communications) et Mapbox (cartographie) ne vendent pas de
logiciel au sens traditionnel. Elles vendent l'accès à des fonctionnalités via
des APIs, facturées à l'usage. Un développeur qui veut intégrer le paiement par
carte de crédit dans son application n'a plus besoin de négocier avec une banque
et d'implémenter un protocole complexe : quelques lignes de code suffisent pour
appeler l'API de Stripe. C'est le logiciel comme service au sens le plus
littéral, et c'est un modèle qui fait directement écho aux APIs que nous avons
étudiées dans le module 3. Shopify, fondée à Ottawa en 2006 par Tobias Lütke
(un développeur allemand qui avait d'abord créé le framework Ruby on Rails pour
ses propres besoins), illustre parfaitement cette convergence : l'entreprise est
à la fois une plateforme SaaS pour les commerçants, un marketplace
d'applications pour les développeurs tiers, et un fournisseur d'APIs pour
l'écosystème e-commerce. Son succès en a fait l'une des plus grandes entreprises
technologiques canadiennes.

{{< image src="shopify.webp" alt="" title="" loading="lazy" >}}

## La culture startup et le capital de risque

Le SaaS et les plateformes n'auraient pas connu une telle expansion sans un
carburant financier particulier : le capital de risque (*venture capital*, ou
VC). Le modèle est simple en apparence : un investisseur finance une jeune
entreprise en échange d'une part du capital, en pariant que la valeur de cette
part explosera si l'entreprise réussit. La plupart des investissements échouent,
mais un seul grand succès peut compenser des dizaines d'échecs. Ce modèle a
façonné la Silicon Valley depuis les années 1970, mais c'est à partir des années
2000 qu'il a transformé la culture même du développement logiciel. La logique du
VC favorise la croissance rapide au détriment de la rentabilité immédiate. Reid
Hoffman, cofondateur de LinkedIn, a formalisé cette approche dans *Blitzscaling*
(2018) : l'idée est de croître le plus vite possible pour conquérir un marché
avant les concurrents, quitte à perdre de l'argent pendant des années. "Move
fast and break things", le slogan interne de Facebook popularisé par Mark
Zuckerberg, résumait cette philosophie. Le résultat est un écosystème où des
entreprises comme Uber, WeWork ou Theranos ont pu lever des milliards de dollars
avant d'avoir prouvé la viabilité de leur modèle. Les critiques de cette culture
sont nombreuses : pression sur les développeurs, dette technique accumulée
volontairement, et une tendance à privilégier les métriques de croissance sur la
qualité du produit. Mais le modèle a aussi produit des entreprises qui ont
véritablement transformé leur industrie.

## Pourquoi le logiciel coûte cher

Si le logiciel ne coûte rien à copier, pourquoi coûte-t-il si cher à produire ?
La réponse tient dans une asymétrie fondamentale : le coût du logiciel est
presque entièrement un coût de conception. Il n'y a pas de matières premières,
pas de chaîne de montage, pas d'inventaire. Ce qu'on paie, c'est le temps de
personnes qualifiées qui réfléchissent à des problèmes complexes. C'est ce que
Fred Brooks avait identifié dès 1975 dans *The Mythical Man-Month* : ajouter des
développeurs à un projet en retard le retarde davantage, parce que la
communication entre les personnes croît plus vite que leur nombre. Le Standish
Group, dans ses rapports CHAOS publiés depuis 1994, a documenté l'ampleur du
problème : selon leurs données, une proportion importante de projets logiciels
dépasse leur budget ou leur échéancier, et certains sont purement abandonnés.
Ces chiffres, bien que contestés méthodologiquement, ont eu un impact durable
sur la perception de l'industrie. Le coût du logiciel n'est pas un problème
technique qu'on résout avec de meilleurs outils. C'est un problème humain et
organisationnel, ce qui explique pourquoi tant de sujets abordés dans ce cours
(les tests du module 2, l'architecture du module 3, les méthodes agiles du
module 4, l'automatisation du module 5) sont autant de tentatives de réduire ce
coût, ou du moins de le rendre plus prévisible.