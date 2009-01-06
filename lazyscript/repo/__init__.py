# -*- encoding=utf8 -*-
"""version manager repositry binding

@author Hisn Yi Chen 陳信屹 (hychen) <ossug.hychen AT gmail.com>
"""
from md5 import md5
from os import path as os_path

from lazyscript.repo import git

class NoScriptPoll(IOError):
	pass

def sign_repopath(path, dest):
	"""
	create a signed repositery path to ensure the repositery path
	is unique in the operation system.

	@param path str the repositry path.
	@param path str the parent dir of the repositry.
	"""
	if not os_path.isdir(dest):
		raise NoScriptPoll('%s not exists.' % dest)

	sign = md5(path+dest).hexdigest()
	return dest+sign

def get_scriptrepo(origin_path, dest):
	"""
	get script repositry.

	@param path str the repositry path.
	@param path str the parent dir of the repositry.
	"""
	newpath = sign_repopath(origin_path, dest)
	repo = git.Repo(newpath)
	return repo

def create_scriptrepo(origin_path, dest):
	"""
	create a script repositry from origin repostiry.

	@param path str the repositry path.
	@param path str the parent dir of the repositry.
	"""
	newpath = sign_repopath(origin_path, dest)
	repo = git.Repo(origin_path)
	newrepo = repo.fork_index(newpath)
	return newrepo
