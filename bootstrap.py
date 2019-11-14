#!/usr/bin/env python3

import os
import re
import sys
import subprocess
from jinja2 import Environment, FileSystemLoader
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from shutil import rmtree

base_env_dir = 'environments'
template_dir = 'templates'
template_file = 'Vagrantfile.j2'
dump_file = 'Vagrantfile'
host_file = '/etc/hosts'
playbooks_dir = 'playbooks'
root_path = os.path.dirname(os.path.abspath(__file__))

parser = ArgumentParser(description='Setups environment using Vagrant/Ansible',
                        formatter_class=ArgumentDefaultsHelpFormatter)
group = parser.add_mutually_exclusive_group()
group.add_argument('--create', action='store_true', help='create env')
group.add_argument('--destroy', action='store_true', help='destroy env')
parser.add_argument('-n', dest='num', default='1', help='number of VMs')
parser.add_argument('-s', dest='net', default='192.168.50', help='VM subnet')
parser.add_argument('-b', dest='box', default='centos/7', help='vagrant box')
parser.add_argument('-v', dest='ver', default='latest', help='box version')
parser.add_argument('-e', dest='env', required=True,
                    help='name for your environment')
parser.add_argument('--render', action='store_true',
                    help='creates Vagrantfile only')
args = parser.parse_args()

count = args.num
env = args.env
subnet = args.net
create = args.create
destroy = args.destroy
box_type = args.box
box_version = args.ver
render = args.render
work_dir = os.path.join(base_env_dir, env)


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
    os.chdir(root_path)
    link_src = os.path.abspath(playbooks_dir)
    link_dst = os.path.abspath(os.path.join(work_dir, playbooks_dir))
    os.symlink(link_src, link_dst)


def render_template():
    try:
        os.makedirs(work_dir)
    except FileExistsError:
        print('{} already exists'.format(work_dir))
        sys.exit(1)
    last_host = get_last_ip()
    e = Environment(loader=FileSystemLoader(template_dir),
                    trim_blocks=True, lstrip_blocks=True)
    t = e.get_template(template_file)
    t.stream(count=count, subnet=subnet, last_host=last_host,
             box_type=box_type, box_version=box_version).dump(
                 os.path.join(work_dir, dump_file))


def destroy_environment():
    os.chdir(root_path)
    try:
        os.chdir(work_dir)
    except FileNotFoundError:
        print('{} doesn\'t exist'.format(work_dir))
        sys.exit(1)
    destroy_env = subprocess.call([vagrant_cmd, "destroy", "-f"])
    if destroy_env != 0:
        print('Erorr bootstrapping environment')
        sys.exit(1)
    else:
        os.chdir(os.pardir)
        rmtree(env)


def create_environment():
    os.chdir(work_dir)
    if render:
        print('{}/Vagrantfile created'.format(work_dir))
        sys.exit(1)
    else:
        create_env = subprocess.call([vagrant_cmd, "up"])
        if create_env != 0:
            print('Error bootstrapping environment')
            destroy_environment()
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
if create:
    render_template()
    setup_playbooks()
    create_environment()
if destroy:
    destroy_environment()
