---
title: "L'infrastructure comme code (Terraform)"
weight: 30
slug: "iac"
---

# L'infrastructure comme code (Terraform)

Jusqu'ici, nous avons traité l'infrastructure comme une donnée : le cluster
Kubernetes existe, les serveurs tournent, le réseau fonctionne. Mais d'où vient
cette infrastructure ? Concrètement, l'infrastructure d'un système logiciel,
c'est tout ce qui doit exister *avant* que le code puisse s'exécuter : les
serveurs (physiques ou virtuels), les réseaux (sous-réseaux, règles de
pare-feu, load balancers), le stockage (disques, espaces de stockage cloud),
les bases de données, les certificats SSL, les entrées DNS. Pendant longtemps,
cette infrastructure était créée et configurée manuellement : un administrateur
se connectait à une console cloud pour créer un serveur, puis en SSH pour
installer des paquets et modifier des fichiers de configuration. Le résultat
était ce qu'on appelle un *snowflake server* : une machine unique, configurée à
la main au fil du temps, dont personne ne sait exactement reproduire l'état. Si
elle tombe en panne, la reconstruire à l'identique relève de l'archéologie.

L'*infrastructure as code* (IaC) est la réponse à ce problème : décrire toute
l'infrastructure dans des fichiers de configuration versionnés, et laisser un
outil se charger de créer ou de modifier les ressources pour correspondre à
cette description. Le paradigme devrait nous être familier à ce stade du cours :
c'est exactement le modèle déclaratif que nous avons rencontré dans SQL
(décrire les données souhaitées, pas comment les chercher), dans les fichiers
YAML de Kubernetes (décrire l'état souhaité du cluster, pas les étapes pour y
arriver), et même dans le Dockerfile (décrire l'image souhaitée, pas comment la
construire pas à pas). À chaque fois, le même patron se répète : on décrit
*quoi*, pas *comment*, et un moteur se charge de la convergence. Et à chaque
fois, la même propriété en découle : l'idempotence. On peut réappliquer la même
description autant de fois qu'on veut, et si l'état réel correspond déjà à
l'état souhaité, rien ne se passe.

L'outil le plus influent dans ce domaine est Terraform, créé par HashiCorp en
2014. Terraform utilise un langage déclaratif appelé HCL (*HashiCorp
Configuration Language*) pour décrire des ressources cloud. Voici un exemple
minimal qui crée un serveur virtuel sur AWS :

```hcl
provider "aws" {
  region = "ca-central-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "web-server"
  }
}
```

La commande `terraform plan` compare cette description à l'état réel de
l'infrastructure et affiche les changements nécessaires, sans rien exécuter. La
commande `terraform apply` effectue ces changements. Si on relance
`terraform apply` sans modifier le fichier, Terraform ne fait rien : l'état
réel correspond déjà à l'état souhaité. Pour rendre cette comparaison possible,
Terraform maintient un fichier d'*état* (*state*) qui enregistre la
correspondance entre les ressources décrites dans le code et les ressources
réelles chez le fournisseur cloud. Ce fichier d'état est essentiel : sans lui,
Terraform ne saurait pas si le serveur `web` existe déjà ou s'il doit être
créé.

Terraform excelle au *provisioning* : créer et gérer les ressources
d'infrastructure elles-mêmes (serveurs, réseaux, bases de données). Mais une
fois qu'un serveur existe, il faut souvent le *configurer* : installer des
paquets, déployer des fichiers de configuration, démarrer des services. C'est
le domaine du *configuration management*, dont les pionniers furent Puppet
(2005) et Chef (2009). Ces outils installaient un agent sur chaque machine, qui
communiquait avec un serveur central pour maintenir la configuration souhaitée.
Ansible (Red Hat, 2012) a simplifié cette approche en éliminant l'agent : il se
connecte directement en SSH et exécute des tâches décrites dans des fichiers
YAML appelés *playbooks*. Un playbook Ansible pour installer et démarrer Nginx
ressemble à ceci :

```yaml
- hosts: webservers
  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present

    - name: Start Nginx
      service:
        name: nginx
        state: started
```

On retrouve le même vocabulaire déclaratif : `state: present` signifie
"assure-toi que ce paquet est installé", pas "installe ce paquet". Si Nginx est
déjà installé, Ansible ne fait rien. En pratique, Terraform et Ansible sont
souvent complémentaires : Terraform crée les machines, Ansible les configure.
Mais avec la montée des containers et de Kubernetes, la frontière entre
provisioning et configuration s'estompe : le Dockerfile *est* la configuration
de la machine, et Kubernetes *est* le provisioning de l'application.

Le mot "code" dans "infrastructure as code" n'est pas anodin. Puisque
l'infrastructure est décrite dans des fichiers texte, elle bénéficie de tous
les outils que nous avons étudiés dans ce cours : versioning avec git, revue
par les pairs via pull requests, tests automatisés dans un pipeline CI. On peut
voir l'historique complet des changements d'infrastructure, revenir à un état
antérieur, et reproduire un environnement identique à partir de zéro. C'est la
même idée que le Dockerfile qui rend un environnement de développement
reproductible, mais étendue à l'ensemble de l'infrastructure. Le terme *GitOps*,
popularisé par Weaveworks en 2017, désigne cette pratique poussée à son
extrême : le dépôt git devient la source de vérité unique pour l'état de tout
le système, et chaque changement, qu'il concerne le code applicatif ou
l'infrastructure, passe par le même processus de commit, revue et déploiement
automatisé.
