# -*- encoding=utf8 -*-
"""version manager repositry binding

@author Hisn Yi Chen 陳信屹 (hychen) <ossug.hychen AT gmail.com>
"""
from hashlib import md5
from os import path as os_path

from lazyscripts.lengacy.repo import git
from lazyscripts.lengacy.config import Config

def _get_root_path ():
    dir = os_path.dirname (__file__) + '/../../'
    root = os_path.abspath (dir)
    return root

def sign_repopath(path):
    """
    create a signed repositery path to ensure the repositery path
    is unique in the operation system.

    @param path str the repositry path.
    """
    return md5(path).hexdigest()

def get_repo_for_distro(distro, testmode=False):
    """
    get a default scripts list file by distrobution.

    @param tuple distro
    """
    default_repo = None
    if not distro:
        raise "need distrobution information"
    # @FIXME: hard code here.
    if testmode:
        dest = _get_root_path()+'/t/datas/scriptspoll'
    else:
        dest = _get_root_path()+'/scriptspoll'
        conf = Config(_get_root_path()+'/conf/repository.conf')
        if conf.default_repo:
          default_repo = conf.default_repo

    if not default_repo:
      if distro[0] in ('Ubuntu','Debian'):
          default_repo = \
            "git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git"

    return create_scriptrepo(default_repo,dest)

def get_scriptrepo(origin_path, dest):
    """
    get script repositry.

    @param path str the repositry path.
    """
    newpath = dest+'/'+sign_repopath(origin_path)
    repo = git.Repo(newpath)
    return repo

def create_scriptrepo(origin_path, dest):
    """
    create a script repositry from origin repostiry.

    @param path str the repositry path.
    @param path str the parent dir of the repositry.
    """
    newpath = dest+'/'+sign_repopath(origin_path)
    if not git.is_git_dir(newpath+'/.git'):
        git.clone_repo(origin_path, newpath)
    newrepo = git.Repo(newpath)
    return newrepo
