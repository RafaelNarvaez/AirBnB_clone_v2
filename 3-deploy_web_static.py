#!/usr/bin/python3
""" Fabric file to deploy site """

from datetime import datetime
from fabric.api import local, put, run, env
import os.path

env.hosts = ['35.229.112.105', '54.198.54.180']


def do_pack():
    """ paking system over tgz """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(date)
    if os.path.isdir("versions") is False:
        local(" mkdir versions")
    local('tar -cvzf ' + file_path + ' web_static')
    if os.path.exists(file_path):
        return file_path
    return None


def do_deploy(archive_path):
    """ deploy archive to web servers """
    if os.path.exists(archive_path) is False:
        return False
    arch_name = archive_path.split('/')[1]
    arch_name_nex = arch_name.split(".")[0]
    re_path = "/data/web_static/releases/" + arch_name_nex
    up_path = '/tmp/' + arch_name
    put(archive_path, up_path)
    run('mkdir -p ' + re_path)
    run('tar -xzf /tmp/{} -C {}/'.format(arch_name, re_path))
    run('rm {}'.format(up_path))
    mv = 'mv ' + re_path + '/web_static/* ' + re_path + '/'
    run(mv)
    run('rm -rf ' + re_path + '/web_static')
    run('rm -rf /data/web_static/current')
    run('ln -s ' + re_path + ' /data/web_static/current')
    return True


def deploy():
    """ Driver of do_deploy and do_pack """
    path = do_pack()
    if (path is None):
        return False
    deploy = do_deploy(path)
    if (deploy is False):
        return False
    return deploy