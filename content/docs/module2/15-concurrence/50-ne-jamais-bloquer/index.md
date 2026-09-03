---
title: "Ne jamais bloquer"
slug: "ne-jamais-bloquer"
weight: 50
---

# Ne jamais bloquer

## Dix mille clients

En 1999, un programmeur nommé Dan Kegel ouvre une page web par une question
faussement modeste&nbsp;: « Il est temps que les serveurs web servent dix mille
clients en même temps, vous ne trouvez pas&nbsp;? » Le problème a gardé le nom
qu'il lui a donné, **C10K**, dix mille connexions, et il est resté la page de
référence du sujet pendant quinze ans, remise à jour jusqu'en 2014. Ce qui le
rendait difficile n'était pas la puissance de calcul. Dix mille personnes qui
lisent un site ne demandent presque rien au processeur. Ce qui le rendait
difficile, c'est que la manière évidente de s'y prendre ne tient pas.

La manière évidente, c'est celle de tout ce qu'on a vu jusqu'ici&nbsp;: un thread
par client. Chaque connexion reçoit son fil d'exécution, qui attend la requête,
la lit, répond, et recommence. C'est simple, c'est lisible, et Kegel montre en
une division pourquoi cela s'effondre. Un thread a besoin d'une pile, deux
mégaoctets sur le Linux de l'époque, et un processus disposait d'un gigaoctet
de mémoire virtuelle. « On manque de mémoire virtuelle à
2^30 / 2^21 = 512 threads. » Un gigaoctet divisé par deux mégaoctets, cinq
cent douze. On en voulait dix mille.
Et même en réduisant les piles, chaque thread qui attend coûte un changement de
contexte à l'ordonnanceur pour rien, puisqu'il n'a rien à faire d'autre
qu'attendre. On retrouve le cuisinier planté devant sa casserole, sauf qu'ils
sont dix mille à attendre chacun devant la sienne, et que la cuisine n'a pas
la place.

La réponse de Kegel tient en une phrase, et elle est le programme de toute
cette sous-section&nbsp;: « servir beaucoup de clients avec chaque thread, et
utiliser des entrées-sorties non bloquantes et une notification de
disponibilité ». Autrement dit, un seul cuisinier pour toutes les casseroles,
à condition qu'il ne reste jamais planté devant aucune. Au lieu de demander au
réseau « donne-moi la requête » et d'attendre qu'elle arrive, on lui demande
« préviens-moi quand une requête est arrivée » et on passe à la casserole
suivante. Le système d'exploitation offre exactement cela, sous des noms qui
varient, `select` et `poll` partout, `epoll` sur Linux, `kqueue` sur les
systèmes BSD dont macOS&nbsp;: une fonction qui reçoit une liste de connexions
et rend la main quand l'une d'elles a quelque chose à dire. Un seul thread, dix
mille connexions, et une boucle qui demande sans cesse « laquelle est
prête&nbsp;? ». On l'appelle une **boucle d'événements** (*event loop*), et c'est
ce que vous avez vu tourner sans le savoir dans les deux millions de
connexions de WhatsApp, à la fin de la sous-section précédente.

## Le multitâche coopératif, revenu par la petite porte

Il faut être précis sur ce qui change, parce que sur une image fixe, rien ne
change. Un cuisinier devant trois casseroles qui cuisent, c'est la vignette
« Concurrence » de l'introduction de cette section, et elle décrit aussi bien
dix threads sur un seul coeur qu'une boucle d'événements. Dans les deux cas,
une seule chose avance à la fois, et dans les deux cas, les casseroles cuisent
pendant qu'on s'occupe d'une autre. La différence n'est pas dans l'image, elle
est dans qui déplace le cuisinier.

Avec les threads, c'est le système qui le déplace. Vous avez vu comment dans
la sous-section sur [les processus et les threads]({{< relref "/docs/module2/15-concurrence/20-processus-et-threads" >}})&nbsp;:
une minuterie interrompt le thread en cours sans lui demander son avis,
l'ordonnanceur range son état et en installe un autre à la place. Le cuisinier
peut donc rester planté devant sa casserole autant qu'il veut, quelqu'un
viendra le pousser. Mais chaque cuisinier planté est un cuisinier entier, avec
sa pile, et chaque poussée est un changement de contexte. Dix mille clients,
c'est dix mille cuisiniers debout dans la cuisine, et c'est le compte de
Kegel.

Avec la boucle d'événements, personne ne pousse personne. Il n'y a qu'un
cuisinier, et c'est lui qui décide quand changer de casserole. Il n'a le droit
de le faire qu'à un moment précis, celui où il a demandé à être prévenu, et il
ne se plante jamais, parce que la casserole a une sonnette. Un plat en attente
n'est plus une personne, c'est une note posée sur la casserole, l'état du plat
et quoi faire quand elle sonnera.

{{< illustration src="sonnette.svg" legende="La même cuisine, les mêmes casseroles. À gauche, un cuisinier par casserole, et c'est l'ordonnanceur qui décide lequel avance, en poussant l'un pendant que les autres restent plantés, chacun avec sa pile. À droite, un seul cuisinier et une sonnette par casserole&nbsp;: il ne se plante devant aucune, et il change de casserole quand l'une sonne." >}}

Si cela vous rappelle quelque chose, c'est normal. Un programme qui rend la
main de lui-même, à des moments qu'il choisit, c'est le multitâche coopératif
que vous avez rencontré avec l'ordonnanceur, celui du Mac OS classique et de
Windows 3.x, que la préemption avait remplacé parce qu'un seul programme qui
oubliait de céder son tour figeait la machine entière. Il revient ici par la
petite porte, à l'intérieur d'un seul processus, et il revient avec sa
fragilité intacte. Si le cuisinier unique reste planté devant une casserole,
ne serait-ce qu'une seconde, les dix mille autres brûlent. C'est de là que
cette sous-section tient son titre.

Le tableau rassemble les trois modèles rencontrés jusqu'ici, sur les quatre
lignes qui les séparent vraiment.

| | Processus | Thread | Boucle d'événements |
|---|---|---|---|
| Mémoire | la sienne, isolée par la MMU | celle du processus, partagée avec les autres threads | celle du processus, un seul thread |
| Qui décide de changer de tâche | le système, par préemption | le système, par préemption | le programme lui-même, aux moments où il a demandé à être prévenu |
| Ce que coûte une tâche qui attend | un processus entier | un thread entier, avec sa pile, et un changement de contexte | une note, l'état du plat et quoi faire ensuite |
| Ce qui casse | rien n'est partagé, mais se parler coûte cher | les conditions de course | un seul appel bloquant fige tout |

## Un langage de navigateur devient un serveur

En novembre 2009, à Berlin, un programmeur nommé Ryan Dahl présente à la
première JSConf EU un projet qui applique la recette de Kegel à un langage qui
ne l'avait jamais connue en dehors du navigateur, JavaScript. Le projet
s'appelle **Node.js**, et sa page d'accueil le décrit encore aujourd'hui dans
des termes qui sont presque ceux de Kegel&nbsp;: « un environnement d'exécution
JavaScript asynchrone et piloté par les événements, conçu pour construire des
applications réseau qui passent à l'échelle ». Puis, à propos du petit serveur
donné en exemple&nbsp;: « à chaque connexion, la fonction de rappel est
déclenchée, mais s'il n'y a rien à faire, Node.js dort ». La **fonction de
rappel** (*callback*), c'est la note posée sur la casserole, ce qu'il faut
faire quand elle sonnera. Et un serveur qui dort quand il n'a rien à faire,
c'est un cuisinier qui n'est planté devant rien.

{{< image src="node.webp" alt="Le logo de Node.js : le mot node en gris foncé, dont le o est un hexagone vert, suivi d'un petit hexagone vert marqué JS" title="Le logo de Node.js, marque déposée, depuis la page de marque de nodejs.org" loading="lazy" >}}

Le choix de JavaScript n'a rien d'un hasard. C'est un langage qui n'avait
jamais eu de threads, parce que dans le navigateur il n'y en a jamais eu&nbsp;: un
seul fil, une boucle d'événements, et du code qui réagit aux clics et aux
réponses du réseau sans jamais bloquer, faute de quoi la page entière se
figerait. Les programmeurs JavaScript pratiquaient le multitâche coopératif
depuis plus de dix ans sans le savoir, et ils n'avaient aucune bibliothèque
de threads à désapprendre. La page de Node reconnaît d'ailleurs ses aînés,
Twisted en Python et EventMachine en Ruby, qui offraient la même boucle mais
comme une bibliothèque, qu'il fallait choisir puis démarrer par un appel
bloquant. Node, dit-elle, « présente une boucle d'événements comme une
construction de l'environnement d'exécution plutôt que comme une
bibliothèque ». Il n'y a pas de fonction pour lancer la boucle. Elle tourne
dès que le programme commence, et le programme se termine quand il n'y a plus
rien à attendre.

Ce choix a eu une conséquence que personne n'avait demandée. Le même langage
tournait désormais des deux côtés du réseau, dans le navigateur et sur le
serveur, et c'était celui que tout développeur web connaissait déjà. Node
n'était pas le premier à l'essayer, Netscape avait proposé du JavaScript côté
serveur dès 1996 avec LiveWire, mais c'est Node qui a tenu, parce qu'il
arrivait avec un moteur rapide et un modèle qui répondait au C10K. Un
gestionnaire de paquets, npm, a suivi dès janvier 2010, et avec lui un seul
écosystème de bibliothèques, partagé par les deux côtés. C'est ce qu'on
appelle aujourd'hui une **pile JavaScript complète** (*full-stack*), celle
des frameworks comme Next.js et Nuxt, que vous verrez dans le module sur
[les architectures web]({{< relref "/docs/module3/30-interfaces/20-architectures-web" >}}).
Et même ceux qui n'écriront jamais un serveur en JavaScript ont Node sur leur
machine, puisque tout l'outillage du front-end moderne, TypeScript, JSX, les
empaqueteurs, tourne dessus. Un projet fait pour servir dix mille clients est
devenu l'atelier de tout le web.

### Rien n'a été inventé, tout a été assemblé

{{< image src="v8.webp" alt="Le logo de V8 : un grand V gris anthracite, et devant lui un 8 bleu aux boucles bien rondes" title="Le logo de V8, marque de Google, publié sur v8.dev sous licence CC BY 3.0" loading="lazy" >}}

Ce qui frappe, quand on ouvre le dépôt de Node, c'est que presque rien n'y a
été écrit de zéro. Le cuisinier, c'est **V8**, le moteur JavaScript que Google
avait construit en 2008 pour Chrome, au moment où les navigateurs se livraient
une guerre de vitesse. V8 se présente comme « le moteur JavaScript et
WebAssembly open source et haute performance de Google, écrit en C++, utilisé
dans Chrome et dans Node.js ». Il n'a jamais été conçu pour un serveur, et il
n'a pas eu à l'être. Les sonnettes, c'est **libuv**, une bibliothèque C dont
la première ligne de présentation dit tout&nbsp;: « une bibliothèque de support
multiplateforme centrée sur les entrées-sorties asynchrones », et dont la
première fonctionnalité annoncée est « une boucle d'événements complète,
appuyée sur `epoll`, `kqueue`, IOCP et les ports d'événements ». Ce sont les
noms de la page de Kegel, plus celui de Windows, derrière une seule interface.
Et libuv est un morceau que Node a lui-même fait naître&nbsp;: elle a été
écrite pour lui, en 2011, quand Dahl a annoncé un portage vers Windows « visant l'API
IOCP », avec l'aide de Microsoft, parce que la bibliothèque utilisée jusque là
ne connaissait pas cette API. Depuis, libuv a quitté le nid&nbsp;: Julia s'en
sert, et Python aussi, à travers uvloop, dont on reparlera.

Le reste de la liste est du même ordre. OpenSSL pour le chiffrement, zlib pour
la compression, c-ares pour les requêtes DNS sans bloquer, llhttp pour
découper les requêtes HTTP, ICU pour Unicode. Le fichier de maintenance du
dépôt en compte une trentaine. Ce que Node a écrit lui-même, c'est la colle
en C++ entre V8 et libuv, et une bibliothèque standard en JavaScript par-dessus.
C'est un cas d'école de ce que vous verrez dans le module sur
[l'architecture]({{< relref "/docs/module3/10-architecture" >}}), et une
démonstration de ce que permet l'open source&nbsp;: un projet qui a changé la
manière d'écrire des serveurs a commencé comme un assemblage de pièces que
d'autres avaient déjà faites, et bien faites.

Voici à quoi ressemble un serveur Node, en entier. Il compte les requêtes
qu'il reçoit.

```javascript
// serveur.js, à lancer avec : node serveur.js
const { createServer } = require("node:http");

let requetes = 0;

createServer((requete, reponse) => {
  requetes += 1;
  reponse.end(`Vous êtes la requête numéro ${requetes}\n`);
}).listen(3210);
```

La fonction passée à `createServer` est la fonction de rappel. Elle n'est pas
appelée par le programme, qui se termine en apparence dès la dernière ligne,
mais par la boucle, à chaque fois qu'une connexion arrive. Et regardez le
compteur. C'est celui de la sous-section sur les processus et les threads,
celui qui perdait trois millions d'incréments sans verrou, et ici il n'y a
toujours pas de verrou. Il est pourtant juste, quel que soit le nombre de
clients. Il n'y a qu'un seul thread, donc deux incréments ne peuvent jamais
se croiser. C'est la dernière ligne du tableau, prise à l'envers&nbsp;: la boucle
ne connaît pas la condition de course. Elle a un autre ennemi, et il arrive
maintenant.

## Regarder la boucle tourner

Le navigateur a exactement la même boucle que Node, c'est même de lui qu'elle
vient, et vous pouvez la regarder tourner ici, sans rien installer. Le bloc
qui suit s'exécute dans votre navigateur quand vous cliquez sur « Exécuter ».
Avant de le lancer, essayez de prédire l'ordre des quatre lignes.

{{< js >}}
console.log("1 : début du script");
setTimeout(() => console.log("4 : la minuterie, pourtant à 0 ms"), 0);
Promise.resolve().then(() => console.log("3 : la promesse"));
console.log("2 : fin du script");
{{< /js >}}

L'ordre est 1, 2, 3, 4, et non 1, 4, 3, 2 comme la lecture du code le
suggère. La ligne `setTimeout` avec un délai de zéro ne dit pas « fais ceci
maintenant », elle dit « pose une note, et quand tu auras fini ce que tu fais,
fais ceci ». Le script court jusqu'à sa dernière ligne sans être interrompu,
ce qui est très exactement la règle du coopératif&nbsp;: personne ne prend la
main au cuisinier, il la rend quand il a fini. Alors seulement la boucle
regarde ses notes, et elle en tient deux piles. La **promesse** (*promise*),
que vous verrez de près dans un instant, va dans une pile prioritaire, la
**file des microtâches**, qui est vidée entièrement avant qu'on touche à
l'autre. La minuterie va dans la **file des tâches**, avec les clics, les
réponses du réseau et tout ce que libuv, ou le navigateur, rapporte du
dehors. D'où le 3 avant le 4, même avec zéro milliseconde.

### Deux secondes de calcul, et tout le monde attend

Voici maintenant la fragilité promise depuis le titre. Le bloc pose une
minuterie de 100 millisecondes, puis se met à calculer pendant deux secondes
sans jamais rendre la main.

{{< js >}}
const depart = performance.now();
setTimeout(() => {
  console.log(`la minuterie de 100 ms a sonné après ${Math.round(performance.now() - depart)} ms`);
}, 100);
let n = 0;
while (performance.now() - depart < 2000) { n += 1; }
console.log(`la boucle a tourné ${n} fois, pendant 2000 ms, sans jamais rendre la main`);
{{< /js >}}

Sur ma machine, la minuterie de 100 millisecondes a sonné après 2001. Elle
était prête depuis longtemps, sa note était posée, mais le cuisinier avait le
dos tourné et personne ne pouvait le pousser. Dans un serveur Node, remplacez
la minuterie par dix mille connexions&nbsp;: pendant ces deux secondes, aucune
n'est servie, aucune n'est même lue. Une seule fonction qui calcule un peu
trop longtemps, ou qui lit un fichier de manière synchrone, et tout le
serveur retient son souffle. C'est la panne du Mac classique, sauf qu'elle
n'arrive plus à une machine, elle arrive à tous vos clients à la fois. La
règle en découle, et elle est absolue&nbsp;: dans une boucle d'événements, on
ne bloque jamais. Ni calcul long, ni attente synchrone. Tout ce qui prend du
temps est confié à quelqu'un d'autre, et la boucle ne fait que poser des
notes et les relire. Reste à savoir à quoi ressemble du code qui ne bloque
jamais, et il a changé trois fois de visage en quinze ans.

<!-- MESURÉ le 2 septembre 2026 dans la page, Pyodide 3.12.7 : threading.Thread
     -> RuntimeError: can't start new thread ; os.fork et multiprocessing ->
     OSError 52 Function not implemented ; MAIS `await asyncio.sleep(0.1)` via
     runPythonAsync fonctionne (737 ms au premier appel, chauffe de la boucle
     comprise). Donc l'exemple asyncio de cette sous-section PEUT être un bloc
     exécutable dans la page, par le shortcode pyodide,, contrairement aux exemples de
     threads de la sous-section 20. À exploiter&nbsp;: ce serait l'exemple Python le
     plus fort de la section, l'étudiant le lance lui-même. Vérifier que le
     shortcode pyodide passe par runPythonAsync (ou l'adapter). -->
