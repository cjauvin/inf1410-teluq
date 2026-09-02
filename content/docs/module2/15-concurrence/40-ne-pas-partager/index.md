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
