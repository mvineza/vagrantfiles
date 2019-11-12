#!/usr/bin/env python3

import os
import re
import sys
import subprocess
from jinja2 import Environment, FileSystemLoader
from argparse import ArgumentParser

base_env_dir = 'environments'
template_dir = 'templates'
template_file = 'Vagrantfile.j2'
dump_file = 'Vagrantfile'
subnet = '192.168.50'
host_file = '/etc/hosts'
playbooks_dir = 'playbooks'

parser = ArgumentParser(description='Setups environment using Vagrant/Ansible')
parser.add_argument('-c', dest='count', default='1', help='number of VMs')
parser.add_argument('-e', dest='env', required=True,
                    help='name for your environment')
args = parser.parse_args()

count = args.count
env = args.env


def get_vagrant_cmd():
    cmd = 'vagrant'
    cmd_path = os.popen("which {}".format(cmd)).read().strip()
    if cmd_path:
        return cmd_path
    else:
        print('Unable to find {} command'.format(cmd))
        sys.exit(1)


def get_last_ip():
    ip_list = []
    with open(host_file) as f:
        for line in f.readlines():
            ip_list.extend(re.findall(subnet + '.[0-9]+', line.strip()))
    try:
        last_ip = sorted(ip_list)[-1:][0]
        last_host = last_ip.split('.')[-1:][0]
    except IndexError:
        last_host = '1'
    return last_host


def setup_playbooks():
    for file in os.listdir(playbooks_dir):
        orig_file = os.path.abspath(os.path.join(playbooks_dir, file))
        link_file = os.path.abspath(os.path.join(work_dir, file))
        if os.path.isfile(orig_file):
            os.symlink(orig_file, link_file)


def render_template():
    global work_dir
    work_dir = os.path.join(base_env_dir, env)
    try:
        os.makedirs(work_dir)
    except FileExistsError:
        print('{} already exists'.format(work_dir))
        sys.exit(1)
    last_host = get_last_ip()
    e = Environment(loader=FileSystemLoader(template_dir))
    t = e.get_template(template_file)
    t.stream(count=count, subnet=subnet, last_host=last_host).dump(
        os.path.join(work_dir, dump_file))


def bootstrap_environment():
    os.chdir(work_dir)
    bootstrap = subprocess.call([vagrant_cmd, "up"])
    if bootstrap != 0:
        print('Erorr bootstrapping environment')
        sys.exit(1)


def check_requirements():
    global vagrant_cmd
    vagrant_cmd = get_vagrant_cmd()
    vagrant_host_updater = 'vagrant-hostsupdater'
    plugins = os.popen("{} plugin list".format(vagrant_cmd)).read()
    if not re.search(vagrant_host_updater, plugins):
        print('{} plugin not found.'.format(vagrant_host_updater))
        sys.exit(1)


check_requirements()
render_template()
setup_playbooks()
bootstrap_environment()
