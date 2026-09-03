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

{{< illustration src="postes.svg" legende="Tant que deux mains peuvent saisir le même couteau, il faut un cadenas, et le cadenas remet tout le monde en file. Donnez à chacun son poste, et le cadenas n'a plus de raison d'être : ce qui doit changer de mains passe par le passe, et n'est jamais tenu à deux." >}}

L'idée a été formalisée en 1978 par Tony Hoare, dans un article intitulé
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
d'exploitation, ceux de la sous-section précédente, lourds et rares. C'en est
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
vingt-quatre coeurs sous FreeBSD, tenant **2 277 845 connexions** simultanées.
Le logiciel derrière était écrit en Erlang, un processus par connexion, et
c'est ce qui permettait à une équipe minuscule de servir des centaines de
millions de personnes. On y reviendra dans la dernière sous-section, parce que
tenir deux millions de connexions n'est pas d'abord une question de
parallélisme, c'est une question d'attente.

## La formule de Go

Si Erlang a fait vivre les acteurs de Hewitt, c'est Go qui a rendu les canaux
de Hoare ordinaires. On a vu dans
[la première sous-section]({{< relref "/docs/module2/15-concurrence/10-pourquoi" >}})
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
en une phrase&nbsp;: **« Ne communiquez pas en partageant la mémoire&nbsp;; partagez
la mémoire en communiquant. »** Ce qu'elle demande est concret. Au lieu d'une
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
