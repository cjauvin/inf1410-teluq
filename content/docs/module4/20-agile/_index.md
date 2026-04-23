---
title: "L'agilité"
slug: "agile"
weight: 20
bookCollapseSection: true
---

# Le manifeste Agile

En quelque au début des années 2000, le mot "agile" est devenu omniprésent, dans
la culture technologique et même au-delà. Il représente en fait un phénomène
culturel dont la genèse est un petit groupe de professionnels, qui se sont
rassemblés pour mettre en commun leurs idées par rapport au changement de
paradigme dans la culture du développement logiciel, par rapport aux décennies
qui précédaient.

Voici les douze principes du [manifeste Agile](https://agilemanifesto.org/iso/fr/principles.html) :

1. Notre plus haute priorité est de satisfaire le client par la livraison rapide
et continue de fonctionnalités à forte valeur ajoutée.

2. Accueillez favorablement les changements, même tard dans le développement.
Les processus agiles exploitent le changement pour donner un avantage compétitif
au client.

3. Livrez fréquemment un logiciel opérationnel, avec des cycles de quelques
semaines à quelques mois, en privilégiant les plus courts.

4. Les utilisateurs ou représentants métier et les développeurs doivent
collaborer quotidiennement tout au long du projet.

5. Réalisez les projets avec des personnes motivées. Donnez-leur l'environnement
et le soutien dont elles ont besoin, et faites-leur confiance pour atteindre les
objectifs.

6. La méthode la plus simple et la plus efficace pour transmettre de
l'information à l'équipe de développement et au sein de celle-ci est la
conversation en face à face.

7. Un logiciel opérationnel est la principale mesure d'avancement.

8. Les processus agiles encouragent un rythme de développement soutenable. Les
commanditaires, les développeurs et les utilisateurs doivent pouvoir maintenir
indéfiniment un rythme constant.

9. Une attention continue à l'excellence technique et à une bonne conception
   renforce l'agilité.

10. La simplicité — l'art de maximiser la quantité de travail non effectué — est
    essentielle.

11. Les meilleures architectures, exigences et conceptions émergent d'équipes
    auto-organisées.

12. À intervalles réguliers, l'équipe réfléchit aux moyens de devenir plus
    efficace, puis ajuste et modifie son comportement en conséquence.

Avant le manifeste Agile, on traitait essentiellement la conception logicielle
comme on traite un projet de construction d'un nouveau pont : il est préférable
de tout prévoir et calculer d'avance, car ceci permettra d'éviter les surprises,
et d'avoir une idée précise du déroulement.

{{< image src="bridge.png" alt="" title="" loading="lazy" >}}

Avec le manifeste Agile, les mentalités changent, et on reconnaît qu'une
meilleure métaphore pour le développement logiciel est celle d'un jardin, un
objet moins prévisible, plus organique et changeant, auquel on doit accorder une
attention quotidienne et en constante évolution :

{{< image src="gardening.png" alt="" title="" loading="lazy" >}}

Plusieurs méthodes concrètes ont émergé du mouvement agile. Les deux plus
influentes, que nous allons explorer en détail dans les sections qui suivent,
sont Scrum et Kanban. Mais il faut aussi mentionner la *programmation extrême*
(Extreme Programming, ou XP), proposée par Kent Beck à la fin des années 1990.
XP n'est pas tant une méthode de gestion de projet qu'un ensemble de pratiques
d'ingénierie : le développement piloté par les tests (TDD), l'intégration
continue, le pair programming, le refactoring continu. Plusieurs de ces
pratiques sont devenues tellement courantes qu'on oublie parfois qu'elles
viennent d'XP. Nous les avons d'ailleurs déjà abordées dans ce cours : le TDD
et les tests au [module 2]({{< relref "/docs/module2/20-tests" >}}),
l'intégration continue dans la section sur la
[CI]({{< relref "/docs/module2/50-ci" >}}). Plutôt que de consacrer une section
séparée à XP, nous préférons souligner ici que ses idées sont tissées à travers
plusieurs parties du cours.

## L'agilité dévoyée

Il serait incomplet de présenter les méthodes agiles sans aborder les critiques
sérieuses qui leur sont adressées, souvent par les mêmes personnes qui les ont
créées. Le manifeste Agile de 2001 était un document radical dans sa
simplicité : une page, quatre valeurs, douze principes. Mais en l'espace de deux
décennies, le mot "agile" a subi une transformation remarquable. Ce qui était un
adjectif décrivant une qualité de travail est devenu un nom propre, puis une
marque commerciale, puis une industrie. Dave Thomas, un des dix-sept signataires
originaux du manifeste, a cristallisé ce malaise en 2014 dans un billet intitulé
"Agile is Dead (Long Live Agility)". Son argument est simple : le mot a été
détourné. On ne cherche plus à être agile, on "fait de l'Agile". La nuance est
fondamentale. Être agile, c'est s'adapter, itérer, répondre au changement. Faire
de l'Agile, c'est suivre un processus certifié, acheter des outils estampillés,
embaucher des consultants spécialisés. Thomas n'est pas le seul signataire à
avoir pris ses distances. Andy Hunt (coauteur de *The Pragmatic Programmer*) a
exprimé des frustrations similaires, constatant que l'agilité était devenue
exactement le type de bureaucratie rigide qu'elle était censée remplacer.

Scrum est la cible la plus fréquente de ces critiques, précisément parce que
c'est la méthode agile la plus adoptée. Ron Jeffries, un des créateurs
d'Extreme Programming et figure importante du mouvement agile, a forgé le terme
"Dark Scrum" pour décrire ce qu'il observe dans beaucoup d'organisations. Le
scénario est récurrent : le management découvre Scrum et y voit un outil de
contrôle. Les daily standups deviennent des rapports de statut adressés au chef
de projet. La vélocité, qui était un outil interne d'auto-calibration de
l'équipe, devient un indicateur de performance individuelle que le management
surveille et compare d'un sprint à l'autre. C'est un exemple classique de la loi
de Goodhart, formulée par l'économiste britannique Charles Goodhart en 1975 :
« Lorsqu'une mesure devient un objectif, elle cesse d'être une bonne mesure. »
La vélocité était utile tant qu'elle servait à l'équipe pour calibrer ses propres
engagements. Dès qu'elle devient un objectif imposé par le management, les
équipes apprennent à jouer le système : elles gonflent les estimations pour
afficher une vélocité impressionnante, et le chiffre ne reflète plus rien de
réel. Les sprints deviennent des mini-deadlines imposées d'en haut plutôt que
des engagements volontaires de l'équipe. L'auto-organisation, qui est pourtant
au cœur du Scrum Guide, disparaît au profit d'une micromanagement habillé de
vocabulaire agile. L'industrie des certifications a amplifié le problème. La
Scrum Alliance propose un titre de "Certified Scrum Master" obtenu en deux jours
de formation. Cela ne fait pas de quelqu'un un praticien expérimenté, pas plus
qu'un cours de deux jours sur le piano ne fait un pianiste. Mais ces
certifications créent l'illusion de compétence et alimentent un marché lucratif
de formations, de coaches et de consultants. Il y a une ironie profonde à voir
l'agilité, née d'un rejet de la bureaucratie et du formalisme, devenir
elle-même une bureaucratie formalisée avec ses titres, ses niveaux et ses tarifs
journaliers.

Le problème de fond est ce qu'on pourrait appeler une *dette organisationnelle*.
Beaucoup d'organisations adoptent Scrum en surface, en ajoutant les cérémonies
et le vocabulaire, sans remettre en question leurs structures de pouvoir. Le
résultat est un "cargo cult" agile : on reproduit les rituels observés chez les
équipes performantes sans comprendre les principes qui les rendent efficaces. On
fait des daily standups de quarante-cinq minutes. On rédige des user stories
mécaniquement, sans réflexion sur la valeur. On fait des rétrospectives où
personne n'ose rien dire parce que le manager est dans la salle.

{{% hint info %}}

Le terme "cargo cult" vient de l'anthropologie : après la Seconde Guerre
mondiale, des populations du Pacifique Sud construisaient des pistes
d'atterrissage en bambou dans l'espoir de faire revenir les avions de
ravitaillement. La forme était parfaite, mais la substance manquait. C'est
exactement ce qui arrive quand une organisation adopte les pratiques agiles sans
en adopter les valeurs.

{{% /hint %}}

{{< image src="cargo-cult.webp" alt="" title="" loading="lazy" >}}

Malgré ces dérives, il serait excessif de rejeter l'agilité en bloc. Les
principes fondamentaux du manifeste restent pertinents : livrer fréquemment,
s'adapter au changement, collaborer étroitement, réfléchir régulièrement à son
fonctionnement. Ce sont les principes 1, 2, 4, et 12, et ils ne nécessitent ni
certification, ni consultant, ni outil spécialisé. La leçon est peut-être que
les méthodes agiles fonctionnent mieux quand elles sont redécouvertes par
l'équipe elle-même, à partir de ses propres problèmes, plutôt qu'imposées de
l'extérieur comme une solution clé en main. C'est d'ailleurs ce que Dave Thomas
recommande : oublier le _nom_ "Agile" et revenir au verbe. Trouver où on en est.
Faire un petit pas vers où on veut aller. Évaluer le résultat. Ajuster. Répéter.