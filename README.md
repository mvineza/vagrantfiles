## Introduction

This repository contains a python script that uses Vagrant and Ansible to
bootstrap an environment. It relies on the host's /etc/hosts file to
determine what is the last VM created. Once determined, it will use the next
available IP to create any succeeding VMs. The /etc/hosts is updated
accordingly for every vm created by using the `vagrant-hostsupdater` plugin.

## Quickstart

Creates Vagrantfile and bootstrap environment:
```
./bootstrap.py -e nginx --create
```

Deletes environment:
```
./bootstrap.py -e svn_cluster --destroy
```

Creates a 3-node environment:
```
./bootstrap.py -e redis_ha_setup -n 3 --create
```

Creates Vagrantfile but don't bootstrap environment:
```
./bootstrap.py -e jenkins --create --render
```

Quick look on existing environments
```
ls environments
```

## Bootstrapping

Each environment will be created under `environment/` directory and a common
inventory file will be created under `common_playbooks/`. That inventory file
will contain the VMs you created. The group name of the VMs will be the same
as the environment name.

Since environments and common inventory varies in each user, both are added to
.gitignore. This makes the repo clean by avoiding changes that are not related
to the code.

## Destroying

When you destroy an environment, the corresponding directories will be deleted,
the VMs will be removed from host's /etc/hosts as well as from the common
inventory file.

## Networking

Each thay will VM created will consist of 2 network interfaces - the first is
the default interface created by vagrant and the second which is configured
and added via custom Vagrantfile which allows direct SSH connection from host
without using any port forwarding. That second interface mimics a real-world
setup on which the VM is located remotely on the network as if it doesn't
exist locally inside the host.

The VM hostnames will be in {{ env }}-vm{{ ipv4 address last octet }} for
easy identification.

## OS configuration

After creating the VM(s), ansible provisioner will run to copy the host's user
SSH public key to the VM(s). This alllows passwordless SSH making ansible
connections easy.

## Pre-requisites

```
Vagrant + vagrant-hostsupdater plugin
Ansible
Virtualbox
```

## Setup tested

Versions on the host:
```
OS: MacOS, Ubuntu, Centos, Fedora
Vagrant: 2.2.5
Ansible: 2.9.0
Python: 3.7.4
```

Versions on the VMs:
```
Boxes:
  centos/6
  centos/7
  iamseth/rhel-7.3
  ubuntu/trusty64
  debian/jessie64
```
