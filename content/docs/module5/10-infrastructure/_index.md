---
title: "L'infrastructure"
weight: 10
slug: "infrastructure"
---

# L'infrastructure

Pour qu'un logiciel soit accessible à ses utilisateurs, il doit s'exécuter
quelque part. Cette question, en apparence triviale, a donné lieu à l'une des
transformations les plus profondes de l'histoire du génie logiciel. En l'espace
de deux décennies, nous sommes passés de serveurs physiques installés dans des
placards à des plateformes cloud capables de provisionner des milliers de
machines virtuelles en quelques secondes. Cette évolution n'est pas seulement
technique : elle a fondamentalement changé la manière dont on conçoit, déploie et
opère les applications. Comprendre cette trajectoire, des machines physiques
jusqu'aux containers et à l'orchestration, est essentiel pour saisir le contexte
dans lequel les pratiques DevOps modernes ont émergé.

{{< image src="homemade-server.jpg" alt="" title="" loading="lazy" >}}

## L'ère du serveur physique

Jusqu'au milieu des années 2000, déployer une application signifiait, de manière
très concrète, installer un serveur. Une entreprise qui voulait mettre un site
web ou une application interne en ligne devait acheter une machine physique (ou
plusieurs), l'installer dans une salle serveur climatisée, la brancher au
réseau, installer un système d'exploitation, configurer les logiciels
nécessaires, et maintenir le tout. Ce processus pouvait prendre des semaines,
voire des mois. Si la demande augmentait et que le serveur n'arrivait plus à
suivre, il fallait commander une nouvelle machine, attendre sa livraison, et
répéter le processus. Pour les organisations qui n'avaient pas les moyens de
maintenir leur propre salle serveur, la *colocation* offrait une alternative : on
achetait le serveur, mais on le plaçait dans un centre de données (datacenter)
géré par un tiers, qui fournissait l'alimentation électrique, la climatisation et
la connectivité réseau. Pour les projets plus modestes, l'*hébergement web*
mutualisé (shared hosting) permettait de louer un espace sur un serveur partagé
entre plusieurs clients, typiquement avec un accès FTP pour déposer ses fichiers
PHP ou HTML. Des entreprises comme OVH (fondée en 1999 en France) ou GoDaddy ont
bâti des empires sur ce modèle. C'était simple et abordable, mais rigide : on
avait peu de contrôle sur l'environnement, et les ressources étaient limitées et
partagées.

{{< image src="data-center.jpg" alt="" title="" loading="lazy" >}}

## La virtualisation

Le premier grand saut vers l'abstraction de l'infrastructure a été la
virtualisation. L'idée, qui remonte en fait aux mainframes IBM des années 1960,
consiste à faire tourner plusieurs systèmes d'exploitation "invités" sur une
seule machine physique, chacun croyant disposer de sa propre machine dédiée. Un
logiciel appelé *hyperviseur* s'interpose entre le matériel et les systèmes
invités pour gérer ce partage de manière transparente. VMware, fondée en 1998, a
démocratisé cette technologie pour les serveurs x86, suivie par Xen (un projet
open source issu de l'Université de Cambridge en 2003) et KVM (intégré
directement au noyau Linux à partir de 2007). La virtualisation a transformé la
gestion des serveurs de plusieurs manières. D'abord, elle a permis de consolider
plusieurs serveurs physiques sous-utilisés en un seul, réduisant les coûts
matériels et énergétiques. Ensuite, elle a rendu possible la création de
nouvelles machines en minutes plutôt qu'en semaines : il suffisait de créer une
nouvelle machine virtuelle (VM) à partir d'une image préexistante. Enfin, elle a
introduit l'idée fondamentale que l'infrastructure pouvait être manipulée comme
une ressource logicielle, créée, copiée, déplacée et détruite à la demande.
C'est cette idée qui allait rendre le cloud possible.

## Le cloud

La virtualisation a rendu l'infrastructure manipulable comme du logiciel. Le
cloud a poussé cette logique à sa conclusion naturelle : pourquoi posséder des
serveurs quand on peut en louer à la demande ? Le moment fondateur est le
lancement d'Amazon Web Services (AWS) en 2006, avec son service EC2 (Elastic
Compute Cloud), qui permettait à n'importe qui de créer une machine virtuelle en
quelques minutes, via une API, et de payer uniquement pour le temps
d'utilisation. L'origine d'AWS est elle-même révélatrice : Amazon avait développé
une infrastructure massive pour faire fonctionner son site de commerce en ligne,
et a réalisé qu'elle pouvait la revendre comme service. Google Cloud Platform
(GCP, 2008) et Microsoft Azure (2010) ont suivi, créant un oligopole qui domine
encore aujourd'hui le marché.

{{< image src="aws-data-center.jpg" alt="" title="" loading="lazy" >}}

Le cloud est généralement décrit en trois niveaux d'abstraction, souvent
représentés sous forme de couches. L'*Infrastructure as a Service* (IaaS) est la
couche la plus basse : on loue des machines virtuelles, du stockage et du réseau,
et on gère soi-même le système d'exploitation et les logiciels (c'est le modèle
d'EC2). La *Platform as a Service* (PaaS) monte d'un cran : le fournisseur gère
l'infrastructure et le runtime, et le développeur ne déploie que son code. Heroku
(2007), la plateforme dont est issue la Twelve-Factor App, est l'exemple
emblématique de ce modèle : un simple `git push heroku main` suffisait pour
déployer une application. Enfin, le *Software as a Service* (SaaS) est la couche
la plus abstraite : l'utilisateur final consomme un logiciel complet sans se
soucier de l'infrastructure (Gmail, Slack, Salesforce). Ces trois niveaux ne sont
pas mutuellement exclusifs : une même organisation peut utiliser du IaaS pour
certains composants et du PaaS pour d'autres.

{{< image src="iaas-paas-saas.jpg" alt="" title="" loading="lazy" >}}

L'adoption du cloud a été rapide et massive. Netflix, après une panne majeure de
son datacenter en 2008, a entrepris une migration complète vers AWS qui est
devenue un cas d'étude en architecture cloud (et a produit au passage de nombreux
outils open source que nous retrouverons plus loin). Airbnb est sur AWS depuis
ses débuts, un exemple emblématique de startup qui n'a jamais possédé de serveur
physique. Spotify a migré de ses propres serveurs vers Google Cloud Platform en
2016. À l'inverse, Dropbox a fait le chemin inverse en 2016, quittant AWS pour
construire sa propre infrastructure, estimant qu'à son échelle les économies
justifiaient l'investissement. Ce dernier cas illustre que le cloud n'est pas une
fin en soi : c'est un compromis entre flexibilité, coût et contrôle, et la bonne
réponse dépend du contexte.

## Le serverless

Le modèle PaaS a ouvert la voie à une abstraction encore plus radicale : le
*serverless*, ou plus précisément le *Function as a Service* (FaaS). L'idée est
simple : au lieu de déployer une application qui tourne en permanence sur un
serveur (même virtuel), on déploie des fonctions individuelles qui sont exécutées
à la demande, en réponse à des événements. AWS Lambda, lancé en 2014, a
popularisé ce modèle. On écrit une fonction (par exemple en Python), on la
déploie sur Lambda, et elle est exécutée uniquement quand un événement
déclencheur survient : une requête HTTP, un message dans une file d'attente, un
fichier déposé dans un bucket S3. On ne paie que pour le temps d'exécution réel,
mesuré à la milliseconde. Google Cloud Functions et Azure Functions offrent des
services équivalents.

Le nom "serverless" est bien sûr trompeur : il y a toujours des serveurs quelque
part, mais le développeur n'a plus à s'en soucier. C'est l'aboutissement logique
de la trajectoire d'abstraction que nous avons suivie, du serveur physique à la
VM, de la VM au PaaS, du PaaS à la fonction. Mais cette abstraction a un coût.
Le *cold start* (le délai de démarrage quand une fonction n'a pas été appelée
récemment) peut poser des problèmes de latence. Le débogage et le monitoring
deviennent plus difficiles quand la logique est dispersée dans des dizaines de
fonctions. Et le risque de *vendor lock-in* (dépendance au fournisseur cloud) est
maximal, puisque chaque plateforme a ses propres conventions et services. Le
serverless est donc particulièrement adapté à certains cas d'usage (traitement
d'événements, tâches ponctuelles, backends légers), mais ne remplace pas les
architectures plus traditionnelles pour des systèmes complexes.

