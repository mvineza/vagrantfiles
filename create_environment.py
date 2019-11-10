#!/usr/bin/env python3

import os
from jinja2 import Template, Environment, FileSystemLoader
from argparse import ArgumentParser

work_dir='workdir'
template_dir='templates'
template_file='Vagrantfile.j2'
dump_file='Vagrantfile'

parser = ArgumentParser(description='Setups environment using Vagrant and Ansible')
parser.add_argument('-c', dest='count', default='1', help='number of VMs')
args = parser.parse_args()

vm_count = args.count

try:
    os.mkdir(work_dir)
except FileExistsError:
    pass


e = Environment(loader=FileSystemLoader(template_dir))
t = e.get_template(template_file)
t.stream(count=vm_count).dump(os.path.join(work_dir, dump_file))
