## Introduction

The usual way of bootstrapping a VM is creating a Vagrantfile and executing
`vagrant up`. But the VM create is very minimalistic. Like for example to
connect to it, you need to execute `vagrant ssh` on same directory as the
Vagrantfile because by default Vagrant connects to SSH via port forwarding.
But if you like to add another interface on the VM so you can connect to it
via `ssh` in any place of your laptop/PC, you need to do further configurations
by adding another interface on the Vagrantfile, select a subnet, update your
/etc/hosts to reflect that IP and on further VMs you will create you need to
make sure IPs are not overlapping. Then same for destroying the VMs, you need
to do such things in reverse to cleanup properly.

This repository contains a python script that uses Vagrant and Ansible to
bootstrap an environment. By default it uses `centos/7` box but can be
configured as command parameter. It relies on the host's /etc/hosts file to
determine what is the last VM created. Once determined, it will use the next
available IP to create any succeeding VMs. The /etc/hosts is updated
accordingly for every VM created by using the `vagrant-hostsupdater` plugin.

This mimics a real-world setup where you have a remote server on your network
which you can connect to and run ansible provisioning. This is not only
advantageous for multiple VM setup but also on other cases because this saves
you time configuring and cleaning up when no longer needed.

[![asciicast](https://asciinema.org/a/vtfeeFizXLhG4CajVFLwILynw.svg)](https://asciinema.org/a/vtfeeFizXLhG4CajVFLwILynw)

## Limitations

The default Vagrantfile template will not work on all kinds of boxes. You can
pass `--render` to the script to only create the Vagrantfile and configure it
the way you wanted.

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

Quick look on existing environments:
```
ls environments
```

Create a 4GB/2vCPU VM:
```
./bootstrap.py -e gitlab -c 2 -m 4096 --create
```

Rebuilding an existing environment (uses existing IP and hostname upon creation):
```
./bootstrap.py -e postgresql --rebuild
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

Version combintations on the host:
```
Mac:
 a.) Vbox 6.0.14 r133895 (QT5.6.3) / Vagrant 2.2.5 / Ansible 2.9.0 / Python 3.7.5 / vagrant-hostsupdater 1.1.1.160
```

Versions on the VMs:
```
Boxes:
  centos/6
  centos/7
  iamseth/rhel-7.3
  ubuntu/trusty64
  ubuntu/xenial64
  debian/jessie64
```
