#!/bin/bash

export VM_COUNT="$1"
[ -z $VM_COUNT ] && { echo "Usage: $0 VM_COUNT"; exit 1; }
vagrant up
