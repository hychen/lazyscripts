# -*- encoding=utf8 -*-
"""version manager repositry binding

@author Hisn Yi Chen 陳信屹 (hychen) <ossug.hychen AT gmail.com>
"""
from md5 import md5
from os import path as os_path

from lazyscript.repo import git

def sign_repopath(path):
    """
    create a signed repositery path to ensure the repositery path
    is unique in the operation system.

    @param path str the repositry path.
    """
    return md5(path).hexdigest()

def get_scriptrepo(origin_path):
    """
    get script repositry.

    @param path str the repositry path.
    """
    newpath = sign_repopath(origin_path)
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
