---
title: "Concurrence et parallélisme"
slug: "concurrence"
weight: 15
bookCollapseSection: true
---

# Concurrence et parallélisme

Au moment d'écrire ces lignes, le portable qui sert à rédiger ce cours fait
tourner 722 programmes. Deux d'entre eux sont réellement en train de faire
quelque chose. Les 720 autres dorment, en attendant qu'il se passe quelque
chose, un clic, l'arrivée d'un paquet sur le réseau, la fin d'une lecture sur
le disque. Le processeur est inoccupé à 83&nbsp;%. Ce n'est pas un moment de calme,
c'est l'état normal d'un ordinateur&nbsp;: une salle d'attente où presque tout le
monde patiente, et où quelques-uns s'activent.

Une cuisine de restaurant fonctionne exactement ainsi, et c'est pour cette
raison qu'elle servira de fil conducteur à toute cette section. Un samedi soir,
trois cuisiniers sortent deux cents plats. Aucun ne prépare un plat du début à
la fin avant de passer au suivant. L'eau des pâtes met huit minutes à bouillir,
la sauce en met vingt à réduire, et un cuisinier qui resterait planté devant sa
casserole ferait fermer le restaurant. Tout le métier consiste à ne jamais rester
immobile pendant que quelque chose cuit. Il y a deux façons d'y parvenir, et
elles n'ont presque rien à voir l'une avec l'autre.

{{< illustration src="cuisine.svg" legende="Trois plats à faire, dans les trois cas. Le cuisinier peut les enchaîner l'un après l'autre. Il peut aussi les mener de front en passant de l'un à l'autre, et c'est la **concurrence** : rien n'a changé sinon son organisation. Ou trois cuisiniers peuvent s'y mettre, et c'est le **parallélisme** : cette fois ce sont les ressources qui ont changé." >}}

La première est de s'organiser pour mener plusieurs plats de front, seul. La
seconde est d'embaucher. Un logiciel dispose des deux&nbsp;: un programme peut être
écrit pour ne jamais attendre les bras croisés (c'est la **concurrence**), et une machine d'aujourd'hui ne
contient plus un seul processeur mais huit ou dix, autant de cuisiniers
supplémentaires (**parallélisme**). L'application que vous construirez cette session aura besoin
des deux. Elle devra répondre à plusieurs personnes à la fois sans faire
patienter la deuxième derrière la première, et elle ne devra pas figer l'écran
de quelqu'un pendant qu'un courriel de confirmation s'envoie.

Ce qui rend le sujet difficile, c'est ce qui se passe quand deux cuisiniers ont
besoin du même couteau au même instant. Ou quand l'un sale la soupe que l'autre
vient de saler. Rien ne s'effondre, aucun plat ne brûle. La soupe est simplement
trop salée, une fois sur cent, et personne ne sait dire pourquoi. Ces erreurs-là
ne se voient pas en goûtant une fois, et c'est ce qui les rend redoutables&nbsp;:
elles passent les tests, parce que les tests goûtent une fois. Une erreur de ce
genre ne fait pas planter le programme. Elle lui fait donner une mauvaise
réponse, de temps en temps, sans rien signaler, et c'est l'archétype du défaut
qu'un module intitulé « Concevoir un programme correct » se doit de traiter.

Le parcours suit cinq étapes. On commencera par **pourquoi** le sujet s'impose,
en remontant au moment où le matériel a cessé d'accélérer tout seul, et en
posant les deux distinctions qui organisent le reste. On verra ensuite ce que
le système d'exploitation offre réellement, avec les **processus et les
threads**, puis **ce qui casse** quand plusieurs d'entre eux touchent aux mêmes
données. On étudiera la réponse historique alternative, qui consiste à **ne pas
partager** du tout, avant de terminer sur la manière dont un seul fil
d'exécution peut servir des milliers de connexions à condition de **ne jamais
bloquer**.
