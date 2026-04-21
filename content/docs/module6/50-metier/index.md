---
title: "Le métier de développeur"
weight: 50
slug: "metier"
---

# Le métier de développeur

Les sections précédentes de ce module ont porté un regard large sur le logiciel :
son économie, sa régulation, ses catastrophes. Cette section change de
perspective pour s'intéresser aux personnes qui le construisent. Le métier de
développeur logiciel est jeune, mal défini, et en mutation constante. Il n'existe
pas de parcours unique pour y accéder, pas de consensus sur ce qu'il faut savoir,
et même pas d'accord sur le nom qu'on devrait lui donner. Programmeur,
développeur, ingénieur logiciel, artisan du code : chaque terme porte une vision
différente de ce que signifie écrire du logiciel pour gagner sa vie. Cette
section explore ces tensions, les réalités quotidiennes du métier, et les idées
qui ont façonné la manière dont la profession se perçoit elle-même.

## Le mythe du 10x developer

L'une des idées les plus persistantes dans la culture du développement logiciel
est celle du "10x developer" : un programmeur qui serait dix fois plus productif
que ses collègues. L'idée trouve son origine dans une étude de Sackman, Erikson
et Grant publiée en 1968, qui avait mesuré, comme résultat secondaire d'une
recherche sur les modes de programmation, des écarts de performance considérables
entre programmeurs sur des tâches identiques. L'étude avait des failles
méthodologiques (notamment le mélange de langages de niveaux différents), mais
même après correction, les écarts restaient significatifs. L'idée a été reprise
et amplifiée au fil des décennies, notamment par Brooks dans *The Mythical
Man-Month* et par McConnell dans *Code Complete*. La variance de productivité
entre développeurs est réelle : certaines personnes comprennent plus vite,
écrivent du code plus propre, déboguent plus efficacement. Mais le mythe du 10x
developer pose problème quand il se transforme en culture. Dans sa version
toxique, il valorise le "génie" solitaire qui code 18 heures par jour, méprise
la documentation et les processus, et considère que le talent individuel prime
sur tout le reste. Cette culture, répandue dans certaines startups de la Silicon
Valley, ignore que la plupart des logiciels sont construits en équipe (module 4),
que la lisibilité du code compte plus que sa brillance, et que le développeur le
plus "productif" peut aussi être celui qui génère le plus de dette technique. À
l'inverse, l'industrie a vu émerger des pathologies opposées : le syndrome de
l'imposteur (*impostor syndrome*), le sentiment persistant de ne pas être à la
hauteur malgré des compétences réelles, est remarquablement répandu chez les
développeurs, en partie parce que le domaine évolue si vite qu'on a toujours
l'impression de ne pas en savoir assez. Le burnout, lui, touche particulièrement
les développeurs dans des environnements à haute pression (startups financées par
le capital de risque, périodes de "crunch" dans le jeu vidéo), et rejoint les
préoccupations éthiques que nous avons abordées dans la section précédente : à
quel point est-il acceptable de sacrifier la santé des personnes qui construisent
le logiciel ?

{{< image src="10x.jpg" alt="" title="" loading="lazy" >}}

## Craft vs engineering

Le développement logiciel est-il un métier d'ingénieur ou un métier d'artisan ?
La question peut sembler abstraite, mais elle a des conséquences concrètes sur
la manière dont on forme les développeurs, dont on organise les équipes, et dont
on évalue la qualité du travail. Le terme "génie logiciel" (*software
engineering*), comme nous l'avons vu dans le module 1, a été proposé délibérément
à la conférence de Garmisch en 1968 pour donner au développement logiciel la
rigueur et la respectabilité de l'ingénierie traditionnelle. Mais dès les années
1990, des voix se sont élevées pour contester cette analogie. Le logiciel n'est
pas un pont : on ne peut pas le spécifier entièrement à l'avance, les exigences
changent en cours de route, et la "bonne" solution dépend souvent du jugement et
de l'expérience du développeur, pas d'un calcul. En 2009, un groupe de
développeurs influents a publié le Manifesto for Software Craftsmanship, conçu
comme un complément au Manifeste Agile de 2001. Là où le Manifeste Agile se
concentrait sur les processus et la collaboration, le Software Craftsmanship
mettait l'accent sur la fierté du travail bien fait : "pas seulement du logiciel
qui fonctionne, mais du logiciel bien conçu" (*not only working software, but
also well-crafted software*). L'idée centrale est que le développement logiciel
s'apprend par la pratique, le mentorat et l'amélioration continue, comme un
métier d'artisan, plutôt que par l'application mécanique de méthodes formelles.
Ce mouvement a inspiré des pratiques comme le *pair programming*, les *code
katas* (des exercices de programmation répétés pour développer des réflexes), et
une attention renouvelée au *clean code*. Mais il a aussi été critiqué : le terme
"artisan" peut devenir une forme d'élitisme déguisé, et l'insistance sur la
qualité du code peut parfois perdre de vue que le but du logiciel est de résoudre
un problème pour des utilisateurs, pas d'être élégant pour les développeurs.

{{< image src="artisan.jpg" alt="" title="" loading="lazy" >}}

## La réalité du code existant

Qu'il se considère comme ingénieur ou artisan, le développeur passe en pratique
la majeure partie de son temps à travailler sur du code qu'il n'a pas écrit.
Michael Feathers, dans *Working Effectively with Legacy Code* (2004), a proposé
une définition provocante mais utile du "code legacy" : c'est du code sans tests.
Pas du code vieux, pas du code mal écrit, mais du code qu'on ne peut pas
modifier en confiance parce qu'il n'y a aucun filet de sécurité pour vérifier
qu'on n'a rien cassé. Par cette définition, du code écrit la semaine dernière
peut déjà être du legacy code. Le livre de Feathers est devenu une référence
parce qu'il s'attaque à une réalité que les cours d'informatique évitent
souvent : la plupart des développeurs ne construisent pas des systèmes neufs à
partir de zéro. Ils héritent de bases de code existantes, partiellement
documentées, écrites par des personnes qui ne sont plus là, avec des décisions de
conception dont la logique s'est perdue. Le travail quotidien consiste à
comprendre ce code, à le modifier sans le casser, et à l'améliorer
progressivement. C'est un travail qui exige de la patience, de l'humilité et
exactement les compétences que nous avons abordées dans ce cours : les tests
comme filet de sécurité (module 2), le versioning pour pouvoir revenir en
arrière (module 2), le refactoring pour améliorer la structure sans changer le
comportement (module 3), et la compréhension de l'architecture pour savoir où
intervenir (module 3). Le concept de Peter Naur que nous avons introduit au début
du module 2, la programmation comme construction d'une théorie, prend ici tout
son sens : quand le développeur original quitte le projet, c'est sa théorie du
programme qui disparaît, et le nouveau développeur doit la reconstruire à partir
du code.

## L'évolution du rôle

Le titre qu'on donne aux personnes qui écrivent du logiciel a changé au fil des
décennies, et chaque changement reflète une transformation du métier lui-même.
Dans les années 1960 et 1970, on parlait de "programmeurs" : des spécialistes
qui traduisaient des spécifications en code, souvent dans un langage bas niveau,
sur des machines partagées. Le programmeur était un technicien, distinct de
l'analyste qui concevait la solution. À partir des années 1980 et 1990, le terme
"développeur" s'est imposé, reflétant un élargissement du rôle : on ne se
contentait plus de coder, on participait à la conception, aux choix
technologiques, aux interactions avec les utilisateurs. L'arrivée du web a
accéléré cette évolution en créant une distinction entre le *front-end*
(l'interface utilisateur, dans le navigateur) et le *back-end* (la logique
serveur, les bases de données). Le "développeur full-stack", capable de
travailler sur les deux, est devenu un profil recherché dans les startups des
années 2010, où les équipes réduites exigeaient des personnes polyvalentes. Puis
le mouvement DevOps (module 5) a brouillé une autre frontière, celle entre le
développement et l'exploitation : le développeur moderne est de plus en plus
responsable non seulement d'écrire le code, mais aussi de le déployer, de le
surveiller en production, et de répondre aux incidents. Le terme SWE (*Software
Engineer*) s'est imposé comme titre standard dans les grandes entreprises
technologiques, tandis que Google a inventé vers 2003 le rôle de SRE (*Site
Reliability Engineer*), un ingénieur qui applique les principes du développement
logiciel aux problèmes d'exploitation et de fiabilité, un concept formalisé dans
le livre *Site Reliability Engineering* (2016). Chaque élargissement du rôle a
rendu le métier plus complexe et plus exigeant, ce qui explique en partie le
syndrome de l'imposteur mentionné plus haut : le développeur d'aujourd'hui est
censé maîtriser un éventail de compétences qui aurait été réparti entre trois ou
quatre rôles distincts il y a vingt ans. La prochaine transformation, déjà en
cours, est celle du développeur "augmenté" par l'IA, un sujet que nous
aborderons dans la section suivante.

## La dette intellectuelle du domaine

Le génie logiciel est un domaine jeune, mais il a déjà accumulé une "dette
intellectuelle" fascinante : des idées qui ont été proposées, oubliées, puis
redécouvertes sous un nouveau nom. Les langages fonctionnels comme Lisp (1958)
et Smalltalk (1972) contenaient des concepts qui sont revenus en force des
décennies plus tard : les fonctions de première classe de Lisp se retrouvent
aujourd'hui dans JavaScript, Python et Rust ; le modèle MVC (Model-View-Controller)
inventé dans Smalltalk se retrouve, sous des formes évoluées, dans les
frameworks d'interfaces modernes comme React et Vue. Les types algébriques de ML
(années 1970) réapparaissent dans TypeScript et Kotlin. Le *pattern matching*,
présent dans Erlang depuis les années 1980, est arrivé dans Python en 2021. Ce
recyclage des idées n'est pas un signe d'immaturité : c'est plutôt que les idées
étaient en avance sur le matériel et les pratiques de leur époque. Mais cela
signifie aussi que l'ignorance de l'histoire conduit à réinventer la roue,
souvent en moins bien.

En 1989, Richard Gabriel, un informaticien spécialisé en Lisp, a écrit un essai
intitulé "Worse is Better" qui est devenu l'un des textes les plus débattus en
génie logiciel. Gabriel y opposait deux philosophies de conception. L'approche
"the right thing", incarnée par la tradition du MIT et de Lisp, qui vise la
correction et la complétude : le système doit être parfaitement conçu, gérer
tous les cas, et offrir une interface élégante, même si cela prend plus de
temps. Et l'approche "worse is better", incarnée par Unix et le langage C, qui
privilégie la simplicité d'implémentation : le système peut être incomplet ou
imparfait, tant qu'il est simple à comprendre, simple à porter sur d'autres
machines, et "suffisamment bon" pour être utile. La thèse provocante de Gabriel
était que l'approche "worse is better" gagne presque toujours, non pas parce
qu'elle produit de meilleurs systèmes, mais parce qu'elle produit des systèmes
qui se propagent plus vite. Unix, avec toutes ses incohérences et ses
limitations, a conquis le monde parce qu'il était portable et simple. Lisp,
malgré son élégance, est resté un langage de niche. L'essai de Gabriel résonne
encore aujourd'hui : JavaScript, un langage conçu en dix jours et truffé de
bizarreries, domine le web. PHP, régulièrement moqué pour ses incohérences, a
propulsé une part énorme du web (WordPress à lui seul fait tourner plus de 40 %
des sites). L'histoire du logiciel suggère que la diffusion et l'adoption
comptent souvent plus que la perfection technique, une leçon difficile à accepter
pour qui aspire à l'artisanat du code.

## A-t-on trouvé la silver bullet ?

Pour terminer cette réflexion sur le métier, revenons une dernière fois à Fred
Brooks. En 1986, dans son essai "No Silver Bullet", Brooks avait affirmé
qu'aucune technologie ou méthode ne permettrait, à elle seule, d'améliorer la
productivité du développement logiciel d'un ordre de grandeur en l'espace d'une
décennie. Sa distinction entre complexité essentielle (la difficulté inhérente au
problème qu'on résout) et complexité accidentelle (la difficulté ajoutée par les
outils et les processus) reste le cadre le plus utile pour penser le métier. Les
progrès des quarante dernières années ont considérablement réduit la complexité
accidentelle : les langages de haut niveau, les frameworks, les gestionnaires de
paquets, le cloud, le CI/CD, tout cela a éliminé des couches entières de travail
fastidieux qui ralentissaient les développeurs des années 1980. Mais la
complexité essentielle, elle, n'a pas diminué. Comprendre un domaine métier,
prendre les bonnes décisions d'architecture, anticiper les cas limites, concevoir
des interfaces qui font sens pour les utilisateurs : ces défis restent
fondamentalement humains. Brooks, revisitant son essai en 1995, maintenait son
diagnostic. Trente ans plus tard, force est de constater qu'il avait raison,
avec une nuance importante : si aucune technologie unique n'a été la silver
bullet, l'accumulation de petites améliorations a transformé ce qu'un
développeur peut accomplir. Un développeur seul, aujourd'hui, peut déployer un
service utilisé par des millions de personnes, quelque chose d'inimaginable en
1986. La question de savoir si l'IA générative sera enfin cette silver bullet est
ouverte, et c'est le sujet de notre dernière section.
