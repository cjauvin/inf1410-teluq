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
prête&nbsp;? ». On l'appelle une **boucle d'événements** (*event loop*).

## Le multitâche coopératif, revenu par la petite porte

Il faut être précis sur ce qui change, parce que sur une image fixe, rien ne
change. Un cuisinier devant trois casseroles qui cuisent, c'est la vignette
« Concurrence » de l'introduction de cette section, et elle décrit aussi bien
dix threads sur un seul coeur qu'une boucle d'événements. Dans les deux cas,
une seule chose avance à la fois, et dans les deux cas, les casseroles cuisent
pendant qu'on s'occupe d'une autre. La différence n'est pas dans l'image, elle
est dans qui déplace le cuisinier.

Avec les threads, c'est le système qui le déplace. Vous avez vu comment dans
la sous-section sur [les processus et les threads]({{< relref "/docs/module2/concurrence/20-processus-et-threads" >}})&nbsp;:
une minuterie interrompt le thread en cours sans lui demander son avis,
l'ordonnanceur range son état et en installe un autre à la place. Le cuisinier
peut donc rester planté devant sa casserole autant qu'il veut, quelqu'un
viendra le pousser. Mais chaque cuisinier planté est un cuisinier entier, avec
sa pile, et chaque poussée est un changement de contexte. Dix mille clients,
c'est dix mille cuisiniers debout dans la cuisine, et c'est le compte de
Kegel. Notez que le cuisinier a changé de sens au passage&nbsp;: dans
l'introduction de la section il représentait un coeur, ici il représente un
thread, et dix mille threads se partagent quelques coeurs.

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
| Mémoire | la sienne, isolée par l'unité de gestion mémoire | celle du processus, partagée avec les autres threads | celle du processus, un seul thread |
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
trop longtemps, ou qui lit un fichier de manière **synchrone**, c'est-à-dire
en attendant sur place que la lecture finisse, et tout le serveur retient son
souffle. C'est la panne du Mac classique, sauf qu'elle
n'arrive plus à une machine, elle arrive à tous vos clients à la fois. La
règle en découle, et elle est absolue&nbsp;: dans une boucle d'événements, on
ne bloque jamais. Ni calcul long, ni attente synchrone. Tout ce qui prend du
temps est confié à quelqu'un d'autre, et la boucle ne fait que poser des
notes et les relire. Reste à savoir à quoi ressemble du code qui ne bloque
jamais, et il a changé trois fois de visage en quinze ans.

## Le même code, trois fois

Prenons une tâche minuscule et refaisons-la trois fois, une par génération.
Il faut lire trois fichiers l'un après l'autre et additionner leurs tailles.
La lecture est simulée par une minuterie de 100 millisecondes, ce qui la
rend exécutable ici, mais rien ne changerait avec un vrai disque ou un vrai
réseau, c'est justement le point&nbsp;: pendant ces 100 millisecondes, la boucle
est libre.

### Première génération, la fonction de rappel

C'est le style de Node à ses débuts, et sa convention est restée&nbsp;: la
fonction de rappel reçoit l'erreur en premier argument, puis le résultat. La
documentation de Node le dit encore, « la plupart des méthodes asynchrones qui
acceptent une fonction de rappel lui passeront un objet Error en premier
argument ».

{{< js >}}
// Une lecture simulée : le résultat arrive plus tard, par une fonction de rappel.
function lire(fichier, rappel) {
  setTimeout(() => rappel(null, fichier.length * 10), 100);
}
lire("entrée.txt", (err, a) => {
  if (err) return console.error(err);
  lire("plat.txt", (err, b) => {
    if (err) return console.error(err);
    lire("dessert.txt", (err, c) => {
      if (err) return console.error(err);
      console.log("total :", a + b + c);
    });
  });
});
{{< /js >}}

Ça marche, et ça ne bloque jamais. Mais regardez la forme. Trois lectures en
séquence donnent trois niveaux d'indentation, l'erreur est traitée trois
fois, et le résultat ne peut jamais être *retourné*, seulement passé plus
loin. Une fonction qui lit ne rend rien, elle promet d'appeler quelqu'un.
Avec dix lectures, le code se couche sur le côté, et le nom que la
communauté a donné à cette forme dit tout, l'**enfer des fonctions de
rappel** (*callback hell*).

### Deuxième génération, la promesse

L'idée est plus vieille que JavaScript. En 1988, Barbara Liskov et Liuba
Shrira proposent, pour les systèmes distribués, un objet qui représente un
résultat pas encore arrivé, et elles l'appellent une *promise*. JavaScript
l'a redécouverte par ses bibliothèques, puis la communauté a fixé un
standard, Promises/A+, dont la première phrase est la définition qu'il faut
retenir&nbsp;: « une promesse représente le résultat éventuel d'une opération
asynchrone ». Le langage l'a intégrée en juin 2015, dans ECMAScript 2015.

{{< js >}}
// La même lecture, qui rend une promesse au lieu de prendre une fonction de rappel.
function lire(fichier) {
  return new Promise((resoudre) => setTimeout(() => resoudre(fichier.length * 10), 100));
}
let total = 0;
lire("entrée.txt")
  .then((a) => { total += a; return lire("plat.txt"); })
  .then((b) => { total += b; return lire("dessert.txt"); })
  .then((c) => { total += c; console.log("total :", total); })
  .catch((err) => console.error(err));
{{< /js >}}

La fonction qui lit rend de nouveau quelque chose, une promesse, sur
laquelle on accroche la suite avec `then`. La pyramide devient une chaîne,
et une seule clause `catch` à la fin attrape l'erreur d'où qu'elle vienne.
Ce que la boucle fait n'a pas changé d'un iota. La note posée sur la
casserole s'appelle maintenant une promesse, et c'est elle qui va dans la
file des microtâches que vous avez vue tourner plus haut.

### Troisième génération, écrire comme si on bloquait

La dernière étape n'est pas venue de JavaScript. Elle est venue de Microsoft,
dans F#, à la fin des années 2000, sous le nom de *workflows asynchrones*,
puis dans C# 5.0 en août 2012, où « presque tout l'effort de cette version »,
dit Microsoft, « est allé au modèle `async` et `await` ». Python l'a adoptée
en 2015 avec la version 3.5, par un document de conception de Yury Selivanov
qui voulait faire des **coroutines**, ces fonctions capables de se suspendre
puis de reprendre, « une fonctionnalité native du langage ». JavaScript l'a
eue en 2017. Quatre langages, moins de dix ans, deux mots-clés.

{{< js >}}
// La même lecture, écrite comme si elle bloquait. Elle ne bloque pas.
function lire(fichier) {
  return new Promise((resoudre) => setTimeout(() => resoudre(fichier.length * 10), 100));
}
const a = await lire("entrée.txt");
const b = await lire("plat.txt");
const c = await lire("dessert.txt");
console.log("total :", a + b + c);
{{< /js >}}

Lisez-le comme du code séquentiel, c'est exactement ce qu'il est. Chaque
`await` est le moment où le cuisinier rend la main&nbsp;: la fonction se
suspend, la boucle est libre pendant 100 millisecondes, et quand la promesse
est tenue, la fonction reprend à la ligne suivante, avec sa valeur. La note
sur la casserole, c'est le reste de la fonction. Les erreurs redeviennent des
exceptions ordinaires, qu'on attrape avec un `try` ordinaire. Trois
versions, un seul total, 290, et surtout un seul modèle&nbsp;: rien n'a changé
dans la boucle entre 2009 et 2017, seulement la manière d'écrire ce qu'on
lui confie. Python a suivi exactement ce chemin, et c'est là qu'on va.

## Python a sa boucle aussi

Elle s'appelle **asyncio**, et elle est plus vieille que les mots-clés qui
la rendent agréable. Guido van Rossum l'a proposée en décembre 2012, dans
un document de conception qui décrit une boucle d'événements pour la
bibliothèque standard, à une époque où Python n'avait encore ni `async` ni
`await`. Les deux mots sont arrivés trois ans plus tard, et c'est depuis ce
moment que la documentation peut la présenter en une phrase&nbsp;: « asyncio
est une bibliothèque pour écrire du code concurrent avec la syntaxe
`async`/`await` ». Elle ajoute, et c'est la phrase à retenir, qu'asyncio
« convient souvent parfaitement au code I/O-bound ». Vous savez maintenant
pourquoi&nbsp;: c'est le cuisinier qui ne se plante devant aucune casserole,
et il n'a rien à offrir à celui qui doit hacher pendant une heure.

Le bloc qui suit tourne ici, dans la page. C'est le premier bloc Python de
cette section à pouvoir le faire, et ce n'est pas un hasard&nbsp;: les threads
et les processus étaient hors de portée de l'environnement Python du
navigateur, mais une boucle d'événements n'a besoin ni des uns ni des
autres. Vingt lectures simulées de 100 millisecondes, d'abord l'une après
l'autre, puis toutes en même temps.

{{< pyodide >}}
import asyncio, time

async def lire(fichier):
    await asyncio.sleep(0.1)          # une lecture simulée de 100 ms
    return len(fichier) * 10

async def principal():
    fichiers = [f"plat-{i}.txt" for i in range(20)]

    depart = time.perf_counter()
    tailles = []
    for f in fichiers:
        tailles.append(await lire(f))
    print(f"en séquence : {sum(tailles)} en {time.perf_counter() - depart:.2f} s")

    depart = time.perf_counter()
    tailles = await asyncio.gather(*(lire(f) for f in fichiers))
    print(f"en même temps : {sum(tailles)} en {time.perf_counter() - depart:.2f} s")

await principal()
{{< /pyodide >}}

Sur ma machine, 2,02 secondes en séquence, 0,10 seconde en même temps, et le
même total. Si vos chiffres sont dix fois plus grands, c'est que vous avez
changé d'onglet pendant l'exécution&nbsp;: les navigateurs ralentissent les
minuteries des onglets cachés, et la boucle d'asyncio, dans cette page, est
celle du navigateur. Le premier passage attend chaque lecture avant de lancer la
suivante, comme le cuisinier de la vignette « Séquentiel ». Le second met
les vingt casseroles sur le feu d'un coup, avec `asyncio.gather`, et n'a
plus qu'à attendre la plus lente, qui prend 100 millisecondes comme les
autres. Un seul thread, donc pas de verrou global qui gêne, et pas de
condition de course possible&nbsp;: la règle de la sous-section sur les threads,
« des threads pour l'I/O-bound », a maintenant une deuxième réponse, et
c'est souvent la meilleure.

La sonnette sous asyncio est d'ailleurs interchangeable. Une bibliothèque
nommée uvloop se présente comme « un remplacement direct de la boucle
d'événements intégrée d'asyncio », qui « utilise libuv sous le capot ». La
même libuv que Node, exactement celle dont on annonçait le retour. Et c'est
cette boucle, native ou libuv, qui fait tourner les serveurs web Python
d'aujourd'hui. Quand FastAPI, que vous retrouverez dans le module sur
[les APIs]({{< relref "/docs/module3/20-apis" >}}), vous dit d'écrire vos
fonctions avec `async def` dès qu'une bibliothèque « vous demande de
l'appeler avec `await` », c'est de ce cuisinier-là qu'il parle.

## Une boucle ne calcule pas plus vite

Il reste à dire ce que la boucle ne sait pas faire, et le bloc qui suit le
montre mieux qu'une phrase. Les vingt lectures de tout à l'heure sont là,
prêtes en 100 millisecondes. Mais cette fois un autre plat demande du
calcul pur, une somme de trente millions de carrés, et c'est le même
cuisinier qui s'en charge.

{{< pyodide >}}
import asyncio, time

async def lire(fichier):
    await asyncio.sleep(0.1)
    return len(fichier) * 10

def hacher():
    return sum(i * i for i in range(30_000_000))   # du calcul pur, rien à attendre

async def lectures(depart):
    tailles = await asyncio.gather(*(lire(f"plat-{i}.txt") for i in range(20)))
    print(f"lectures finies à {time.perf_counter() - depart:.2f} s")
    return sum(tailles)

async def cuisinier_qui_hache(depart):
    resultat = hacher()                            # bloque la boucle
    print(f"hachage fini à {time.perf_counter() - depart:.2f} s")
    return resultat

async def principal():
    depart = time.perf_counter()
    await asyncio.gather(cuisinier_qui_hache(depart), lectures(depart))

await principal()
{{< /pyodide >}}

Sur ma machine, le hachage finit à 0,83 seconde, et les lectures à 0,93.
Elles étaient prêtes depuis 100 millisecondes, leurs sonnettes avaient
sonné, mais le cuisinier hachait, et rien dans une boucle ne peut le pousser.
`await` ne sert à rien ici, puisqu'il n'y a rien à attendre. C'est la
minuterie de 100 millisecondes qui sonnait après deux secondes, en Python
cette fois, et c'est la limite de tout ce que cette sous-section a
construit&nbsp;: une boucle d'événements fait attendre sans coûter, elle ne
fait pas calculer plus vite. Pour le calcul, il faut des bras, et on revient
aux threads et aux processus des sous-sections précédentes.

Les deux réponses tiennent chacune en une ligne, et elles ne peuvent pas
s'exécuter dans la page, pour la raison donnée dans la sous-section sur les
processus et les threads&nbsp;: Pyodide n'a ni les uns ni les autres.

```python
# La même fonction cuisinier_qui_hache, en deux variantes. Le reste ne change pas.

# 1. Confié à un thread : la boucle est libre, mais le verrou global reste.
async def cuisinier_qui_hache(depart):
    resultat = await asyncio.to_thread(hacher)
    print(f"hachage fini à {time.perf_counter() - depart:.2f} s")
    return resultat

# 2. Confié à un processus : un autre coeur, un autre interpréteur, pas de verrou.
from concurrent.futures import ProcessPoolExecutor

async def cuisinier_qui_hache(depart):
    with ProcessPoolExecutor() as bassin:
        resultat = await asyncio.get_running_loop().run_in_executor(bassin, hacher)
    print(f"hachage fini à {time.perf_counter() - depart:.2f} s")
    return resultat
```

Avec le thread, les lectures finissent à 0,14 seconde et le hachage à 0,85.
La boucle a retrouvé sa liberté, mais le hachage n'a pas gagné une
milliseconde, parce que le verrou global de Python est toujours là&nbsp;: le
thread qui hache et la boucle se relaient sur un seul coeur, et c'est
seulement parce que la boucle a très peu à faire qu'elle passe entre les
gouttes. Avec le processus, 0,11 et 0,90. Le hachage a pris un autre coeur,
la boucle n'en a rien su, et les 0,07 seconde de plus sont le prix du
bassin de processus, un interpréteur par coeur à démarrer, dix sur cette
machine, à sept millisecondes chacun d'après la mesure de la sous-section sur
les processus. Node dit exactement la même chose de ses threads&nbsp;:
« utiles pour les opérations JavaScript intensives en calcul », et « peu
utiles pour le travail intensif en entrées-sorties », où sa boucle fait
mieux.

Vous tenez maintenant la règle complète, et elle referme la section. Ce qui
attend va dans une boucle, ou dans des threads, et ne coûte presque rien. Ce
qui calcule va dans des processus, un par coeur, et ne partage rien. Et rien
n'interdit de combiner, une boucle par coeur dans des processus séparés qui
ne se parlent que par messages, ce qui est très exactement la cuisine de la
sous-section sur le partage, avec le passe. Relisez la formule de Pike avec
ça en tête&nbsp;: la boucle, c'est de la concurrence sans parallélisme, une
structure qui fait attendre proprement. Les processus, c'est du
parallélisme, une exécution sur plusieurs coeurs. Le triangle de
l'introduction est complet, et quand la question deviendra « combien de
machines, et non plus combien de coeurs », vous la retrouverez dans le
module sur [la scalabilité]({{< relref "/docs/module5/60-scalabilite" >}}).
Amdahl, lui, n'aura pas bougé&nbsp;: ce qui est vraiment séquentiel le reste,
quel que soit le nombre de cuisiniers.

