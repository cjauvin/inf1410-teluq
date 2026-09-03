---
title: "Ne pas partager"
slug: "ne-pas-partager"
weight: 40
---

# Ne pas partager

## S'il n'y a rien à protéger

Tout ce qui cassait dans la sous-section précédente cassait pour une seule
raison&nbsp;: deux threads touchaient à la même mémoire. La condition de course
vient d'une variable lue par l'un pendant que l'autre l'écrit. Le verrou existe
pour empêcher cela. L'interblocage vient de deux verrous. Retirez le partage,
et toute la chaîne disparaît avec lui&nbsp;: sans mémoire commune il n'y a rien à
protéger, sans rien à protéger il n'y a pas de verrou, et sans verrou il n'y a
pas d'interblocage possible. C'est la réponse à la question de Lee, et elle est
plus radicale que toutes les règles de discipline&nbsp;: ne pas avoir à poser de
verrous, c'est ne rien avoir en commun. En cuisine, c'est le poste de travail.
Chaque cuisinier a son couteau, sa planche, ses casseroles, et personne ne
prend rien sur le poste d'un autre. Quand un plat doit passer de l'un à
l'autre, il est posé sur le passe, et l'autre le prend. Rien n'est jamais tenu
à deux.

{{< illustration src="postes.svg" legende="Tant que deux mains peuvent saisir le même couteau, il faut un cadenas, et le cadenas remet tout le monde en file. Donnez à chacun son poste, et le cadenas n'a plus de raison d'être&nbsp;: ce qui doit changer de mains passe par le passe, et n'est jamais tenu à deux." >}}

L'idée a été formalisée en 1978 par Tony Hoare, que vous avez croisé dans
« Pourquoi la concurrence » à propos de Rob Pike, dans un article intitulé
*Communicating Sequential Processes*, que le domaine désigne par ses initiales,
**CSP**. Hoare y décrit des processus qui, chacun, sont de simples programmes
séquentiels, et qui ne partagent rien&nbsp;: aucune variable, aucune mémoire.
Leur seul moyen d'interagir est d'envoyer et de recevoir des **messages** sur
des **canaux** nommés, et l'envoi est lui-même un point de rendez-vous, celui
qui envoie attend que l'autre ait reçu. Cette contrainte a une conséquence
que Hoare a vue avant tout le monde&nbsp;: dans un tel système, une condition de
course ne peut pas se produire, parce qu'elle ne peut même pas s'écrire. Il n'y
a pas de variable à lire pendant qu'un autre l'écrit. L'exclusion mutuelle,
que Dijkstra avait dû inventer, vient gratuitement avec le canal.

## Des acteurs qui ne se voient pas

Hoare n'était pas le premier. Cinq ans plus tôt, en 1973, Carl Hewitt et deux
étudiants du laboratoire d'intelligence artificielle du MIT, Peter Bishop et
Richard Steiger, avaient proposé une idée voisine sous un autre nom, dans un
article présenté à la conférence IJCAI. Ils ne cherchaient pas à écrire des
systèmes d'exploitation, mais à modéliser l'intelligence comme une foule
d'agents indépendants qui se parlent. Leur unité de base est l'**acteur**&nbsp;: un
objet qui possède un état que lui seul peut lire ou modifier, et une **boîte
aux lettres** (*mailbox*) où les autres déposent des messages. Quand un acteur
traite un message, il peut faire exactement trois choses, envoyer des messages
à d'autres acteurs, en créer de nouveaux, et décider de son propre
comportement pour le message suivant. Rien d'autre. Personne ne touche jamais
à l'état d'un acteur autrement qu'en lui écrivant.

La différence avec Hoare tient à un mot, et elle compte. Dans CSP, l'envoi
est un rendez-vous&nbsp;: celui qui envoie attend que l'autre ait reçu. Chez
Hewitt, on dépose le message dans la boîte et on repart sans attendre,
l'autre le lira quand il y viendra. Les messages des acteurs sont
**asynchrones**, et c'est ce qui les rend naturels dès que les interlocuteurs
sont loin l'un de l'autre, sur une autre machine, ou simplement occupés. En
cuisine, l'acteur est le cuisinier à son poste, et la boîte aux lettres est le
rail où s'accrochent les bons de commande&nbsp;: la salle y pique un ticket et
retourne à ses tables sans attendre que le plat soit parti, le cuisinier les
prend dans l'ordre, et personne ne vient tourner ses casseroles à sa place.

L'idée est restée pendant plus de dix ans une affaire de laboratoire, une
belle théorie que peu de programmes utilisaient. Il aura fallu qu'une
compagnie de téléphone ait un problème que rien d'autre ne résolvait.

## Le langage d'une compagnie de téléphone

En 1986, au laboratoire d'informatique d'Ericsson, Joe Armstrong commence à
travailler sur un langage pour les centraux téléphoniques, bientôt rejoint par
Robert Virding et Mike Williams. Le problème d'un central est celui de Hewitt,
mot pour mot&nbsp;: des milliers d'appels en même temps, qui n'ont rien à voir
entre eux, un système qui ne doit jamais s'arrêter, et surtout, une erreur
dans un appel qui ne doit pas toucher les autres. Le langage s'appellera
**Erlang**, et chaque appel y devient ce que le langage nomme, un peu
trompeusement, un processus. Ce n'est pas un processus du système
d'exploitation, ceux de la sous-section sur les processus et les threads,
lourds et rares. C'en est
une version minuscule, gérée par le langage lui-même, dont une machine fait
tourner des centaines de milliers. Chacun a sa mémoire, que personne d'autre
ne voit, et sa boîte aux lettres. Ce sont les acteurs de Hewitt, dans un
langage sur lequel une entreprise a parié.

{{< image src="erlang.webp" alt="Le logo d'Erlang : le nom du langage en lettres noires, avec un e rouge" title="Le logo d'Erlang, marque d'Ericsson, via Wikimedia Commons" loading="lazy" >}}

De cette isolation découle la décision la plus surprenante d'Erlang, que
Armstrong résume par une formule devenue célèbre&nbsp;: **let it crash**, laissez
planter. Plutôt que de prévoir dans chaque processus tout ce qui pourrait mal
tourner, on le laisse mourir dès qu'il rencontre une erreur, et un autre
processus, le **superviseur**, dont c'est le seul rôle, s'en aperçoit et le
relance. Dans sa thèse de 2003, Armstrong pose la distinction qui rend cela
raisonnable&nbsp;: une exception est une situation que le système ne sait pas
traiter, une erreur est une situation que le programmeur ne sait pas traiter,
et pour la seconde, la seule réponse honnête est de laisser un autre processus
réparer. En cuisine, le cuisinier qui rate sa sauce la jette et recommence, le
chef le remarque et réaffecte le poste, et les quarante autres plats n'en
sauront jamais rien. Cela ne fonctionne que parce que rien n'est partagé. Un
processus qui meurt en tenant un verrou emporterait tout le monde avec lui.
Un processus Erlang ne tient rien.

Vous retrouverez cette philosophie, presque mot pour mot, à une tout autre
échelle. Dans la section sur
[Kubernetes]({{< relref "/docs/module5/10-infrastructure/20-kubernetes" >}}),
vous tuerez un conteneur de vos propres mains et le verrez réapparaître
aussitôt, parce qu'une boucle de contrôle compare sans cesse l'état désiré à
l'état réel et remplace ce qui manque. Le texte y dit que le système « ne
tente pas de réparer un pod défaillant, il le remplace ». C'est le superviseur
d'Erlang, avec des conteneurs à la place des processus et un centre de données
à la place d'un central téléphonique. Aucune filiation directe entre les deux,
mais la même conclusion, tirée deux fois à trente ans d'écart&nbsp;: quand rien
n'est partagé, laisser mourir et relancer coûte moins cher que prévoir.

Le résultat s'est vu sur un produit. En 1998, Ericsson livre l'AXD301, un
commutateur qui, au moment où Armstrong écrit sa thèse, compte 1,7 million de
lignes d'Erlang, et qu'il décrit comme « l'un des produits les plus fiables
jamais faits par Ericsson ». On lit partout à son sujet une disponibilité de
99,9999999&nbsp;%, les fameux neuf neuf, soit trente et une millisecondes
d'arrêt par an. Il vaut la peine de lire ce qu'Armstrong lui-même en dit&nbsp;: la
seule source de ce chiffre était « une présentation PowerPoint montrant des
chiffres selon lesquels un client important avait fait tourner un système de
onze noeuds avec une fiabilité de 99,9999999&nbsp;%, sans que la façon dont ces
chiffres avaient été obtenus soit documentée ». Le chiffre le plus cité sur
Erlang est ainsi désavoué par son auteur, dans le texte même qu'on cite pour
l'étayer. Ce que la thèse affirme est plus modeste et bien mieux établi.

L'idée a survécu à la téléphonie. Le 6 janvier 2012, WhatsApp, alors une
petite entreprise, publie un billet technique montrant un seul de ses serveurs,
vingt-quatre coeurs sous FreeBSD, tenant 2 277 845 connexions simultanées.
Le logiciel derrière était écrit en Erlang, un processus par connexion, et
c'est ce qui permettait à une équipe minuscule de servir des centaines de
millions de personnes. On y reviendra dans la dernière sous-section, parce que
tenir deux millions de connexions n'est pas d'abord une question de
parallélisme, c'est une question d'attente.

## La formule de Go

Si Erlang a fait vivre les acteurs de Hewitt, c'est Go qui a rendu les canaux
de Hoare ordinaires. On a vu dans
[la première sous-section]({{< relref "/docs/module2/concurrence/10-pourquoi" >}})
d'où vient le langage, de Newsqueak à Go en passant par Plan 9, trente ans de
Rob Pike à reconstruire la même idée. Ce qui a changé en 2009, c'est l'échelle
d'adoption. Une goroutine se lance avec un mot-clé et coûte si peu qu'on en
crée des milliers sans y penser, et un canal se déclare avec un type, `chan
int`, si bien qu'on y envoie et qu'on en reçoit avec la même flèche&nbsp;:
`ch <- 42` pour déposer, `x := <-ch` pour prendre. Par défaut, l'envoi attend
que quelqu'un reçoive, exactement comme chez Hoare. Go a donc pris le
rendez-vous de CSP là où Erlang avait pris la boîte aux lettres de Hewitt, et
les deux langages sont, cinquante ans plus tard, les deux branches vivantes
des deux articles de 1973 et 1978.

{{< image src="gopher.webp" alt="Le gopher de Go, la mascotte du langage : un petit rongeur bleu aux grands yeux ronds, dessiné au trait" title="Le gopher de Go, dessiné par Renée French, CC BY 3.0, via Wikimedia Commons" loading="lazy" >}}

Le mot d'ordre annoncé depuis le début de cette section vient d'un billet du
blogue officiel de Go, écrit par Andrew Gerrand le 13 juillet 2010, et il tient
en une phrase&nbsp;: « Ne communiquez pas en partageant la mémoire&nbsp;; partagez
la mémoire en communiquant. » Ce qu'elle demande est concret. Au lieu d'une
variable que plusieurs goroutines lisent et écrivent sous la garde d'un verrou,
une seule goroutine possède la donnée, et les autres lui envoient des messages
pour la consulter ou la modifier. Gerrand le résume ainsi&nbsp;: cette approche
garantit qu'une seule goroutine a accès à la donnée à un instant donné. C'est
le poste de travail et le passe, dits en Go. La donnée ne change jamais de
mains par une saisie à deux, seulement par un dépôt suivi d'une prise.

Voici le compteur de la sous-section précédente, réécrit ainsi. Il n'y a plus
de variable partagée ni de verrou&nbsp;: chaque goroutine compte pour elle-même,
puis dépose son résultat sur le passe, et le programme principal prend les
quatre plats un à un.

```go
package main

import "fmt"

// Chaque goroutine compte pour elle-même, sur son propre poste,
// puis dépose son résultat sur le passe. Rien n'est partagé.
func compter(n int, resultats chan<- int) {
	somme := 0
	for i := 0; i < n; i++ {
		somme++
	}
	resultats <- somme
}

func main() {
	resultats := make(chan int)
	for i := 0; i < 4; i++ {
		go compter(1_000_000, resultats) // quatre cuisiniers, chacun son poste
	}
	total := 0
	for i := 0; i < 4; i++ {
		total += <-resultats // on prend les quatre plats, un à un
	}
	fmt.Println("attendu :", 4_000_000)
	fmt.Println("obtenu  :", total)
}
```

```shell
$ go run compteur.go
attendu : 4000000
obtenu  : 4000000
```

Le mot-clé `go` devant l'appel lance la fonction dans une goroutine et rend la
main aussitôt. Le canal `resultats` est le passe&nbsp;: `resultats <- somme` y
dépose, `<-resultats` y prend, et comme l'envoi attend qu'on reçoive, le
programme principal ne peut pas terminer avant d'avoir pris les quatre
résultats. Il n'y a rien à protéger, parce que `somme` n'existe que dans la
goroutine qui la calcule, et que le seul moment où une valeur change de mains
est un dépôt sur le canal. La justesse ne dépend plus de l'ordre dans lequel
les quatre goroutines finissent. Relancez-le mille fois, il donnera mille fois
4 000 000, et cette fois ce n'est pas une chance, c'est une propriété.

Il faut être honnête sur ce que Go promet et ce qu'il n'impose pas. Le
langage a toujours de la mémoire partagée et des verrous, dans son paquet
`sync`, et rien n'empêche d'écrire en Go le compteur faux de la sous-section
précédente. La formule est une discipline que le langage encourage par ce
qu'il rend facile, pas une règle qu'il fait respecter. Erlang, lui, ne laisse
pas le choix, puisque ses processus ne peuvent physiquement rien partager. Et
c'est Rust, en 2015, qui poussera l'idée jusqu'au bout dans l'autre direction,
en faisant vérifier par le compilateur qu'aucune donnée n'est accessible par
deux fils à la fois, de sorte que la condition de course y est refusée avant
même que le programme tourne. Trois langages, trois réponses à la question de
Lee&nbsp;: encourager, interdire, ou prouver.

## Un système d'exploitation qui ne partage rien

L'idée de Hoare ne s'est pas arrêtée aux langages. En 1980, à Kanata, en
banlieue d'Ottawa, deux étudiants de l'Université de Waterloo, Gordon Bell et
Dan Dodge, fondent Quantum Software Systems pour construire un système
d'exploitation sur ce principe. Leur premier produit, QUNIX, sort en 1982 sur
le processeur 8088 des premiers PC, et prend en 1984 le nom qu'il a gardé,
**QNX**. Il tourne aujourd'hui dans les voitures du monde entier, dans des
appareils médicaux et des équipements industriels, et il appartient depuis
avril 2010 à Research In Motion, l'entreprise de Waterloo derrière le
BlackBerry, qui en a fait depuis le coeur de son activité automobile.

Ce qui distingue QNX, c'est ce que son noyau ne fait pas. Un système
d'exploitation classique, Linux ou Windows, est un **noyau monolithique**&nbsp;:
l'ordonnanceur, les pilotes de périphériques, les systèmes de fichiers et la
pile réseau vivent dans le même espace mémoire, et se partagent tout. C'est
efficace, et c'est exactement pour cela qu'un pilote défaillant peut emporter
la machine entière, une panne de la même famille que l'écran bleu de la
sous-section sur les processus et les threads, celle où rien ne sépare le
fautif du reste. QNX est un **micronoyau**. Sa propre documentation décrit ce qu'il
contient en une phrase&nbsp;: le noyau « implémente les fonctions POSIX de base
utilisées dans les systèmes temps réel embarqués, ainsi que les services
fondamentaux d'échange de messages ». Rien d'autre. Les systèmes de fichiers,
les pilotes, le réseau, « s'exécutent hors du noyau », comme des processus
ordinaires, et les programmes les utilisent « en communiquant par messages ».
Le passage de messages n'est pas une option de QNX, il est, selon ses propres
mots, « la forme première de communication entre processus » de tout le
système.

La conséquence est celle d'Erlang, appliquée au système lui-même. Un pilote
qui plante est un processus qui meurt, et on le relance, pendant que le reste
de la machine continue. Un système de fichiers n'a aucun moyen d'écraser la
mémoire du réseau, parce qu'il ne la voit pas. C'est ce qui vaut à QNX sa
place dans les endroits où un redémarrage n'est pas une option. Et le choix de
QNX entre les deux branches de cette sous-section est net&nbsp;: sa documentation
précise que l'échange de messages « est synchrone et copie les données ».
C'est le rendez-vous de Hoare, pas la boîte aux lettres de Hewitt, avec un
prix qu'on reconnaît&nbsp;: chaque message est copié d'un espace d'adressage à
l'autre. On l'a vu dans la sous-section sur les processus, c'est ce coût-là
que les threads avaient été inventés pour éviter. QNX le paie volontairement,
parce que l'isolation vaut plus que la vitesse dans une voiture.

## Ne rien partager, ou ne partager que ce qui ne change pas

Tout ce qui précède peut maintenant se dire en une règle, plus précise que le
titre de cette sous-section. Ce qui casse n'est pas le partage. C'est le
partage d'un **état mutable**, une valeur que l'un peut lire pendant qu'un
autre l'écrit. De là, il y a deux stratégies, et non une. La première est de
ne rien partager du tout et de s'échanger des messages, c'est la voie de Hoare,
de Hewitt, d'Erlang, de Go et de QNX. La seconde est de partager librement des
valeurs qui ne changent jamais, parce qu'une valeur qu'on ne modifie pas ne
peut pas être lue pendant qu'on l'écrit, et qu'il n'y a donc rien sur quoi
courir. Un million de threads peuvent lire la même chaîne de caractères sans
verrou, à condition que personne ne la modifie jamais.

Cette seconde voie a un nom que vous connaissez déjà. La section sur
[la programmation]({{< relref "/docs/module2/10-programmation" >}}) présentait
l'immutabilité comme la première des deux idées centrales du paradigme
fonctionnel, et disait qu'elle « élimine toute une classe de bugs liés aux
modifications inattendues de l'état ». Vous savez maintenant de quelle classe
il s'agit. Ce n'est pas un hasard si, quelques lignes plus haut, cette section citait
Erlang&nbsp;: Erlang
est un langage fonctionnel précisément parce que ses processus s'envoient des
données, et qu'une donnée qui ne change pas peut être envoyée sans crainte.
Rich Hickey, le créateur de Clojure, que la même section nommait comme forme
moderne de Lisp, l'a dit sans détour dans le texte où il justifie son
langage&nbsp;: les objets à état mutable sont « le nouveau code spaghetti », un
« désastre pour la concurrence », et l'immutabilité « fait disparaître
l'essentiel du problème, partagez librement entre threads ». Les deux
stratégies se rejoignent donc, et les langages qui prennent la concurrence au
sérieux tendent à prendre les deux.

Python, lui, n'impose ni l'une ni l'autre, mais il offre la première dans sa
bibliothèque standard, et vous l'avez déjà utilisée sans le savoir. Voici le
programme Go de tout à l'heure, réécrit avec des processus et une file.

```python
from multiprocessing import Process, Queue

def compter(n, resultats):
    somme = 0
    for _ in range(n):
        somme += 1
    resultats.put(somme)          # dépose le résultat sur le passe

if __name__ == "__main__":
    resultats = Queue()
    ps = [Process(target=compter, args=(1_000_000, resultats)) for _ in range(4)]
    for p in ps: p.start()
    total = sum(resultats.get() for _ in range(4))   # prend les quatre plats
    for p in ps: p.join()
    print(f"attendu : {4_000_000}")
    print(f"obtenu  : {total}")
```

```shell
$ uv run --python 3.14t --no-project python file.py
attendu : 4000000
obtenu  : 4000000
```

Le résultat est juste sur l'interpréteur sans GIL comme sur l'autre, et cette
fois sans verrou, parce que chaque processus a sa propre mémoire et que la
seule chose qui la quitte est une valeur déposée dans la file. Le
`multiprocessing.Pool` de la sous-section sur les processus faisait déjà
exactement cela, en cachant la file. C'est le passe, en Python.

Reste une chose que ne pas partager ne règle pas. Les quatre processus
ci-dessus calculent. Mais la plupart des programmes, on l'a vu, n'ont pas ce
problème-là&nbsp;: ils attendent. Et pour un programme qui attend, la question
n'est pas comment répartir le travail entre plusieurs cuisiniers, c'est
comment un seul cuisinier peut ne jamais rester planté devant l'eau qui bout.
C'est le sujet de la dernière sous-section.
