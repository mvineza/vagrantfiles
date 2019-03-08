#!/bin/bash

vagrant up
ansible-playbook -i inventory k8_kubeadm_setup.yml
