# -*- encoding=utf8 -*-
from lazyscript.repo import git, create_scriptrepo, sign_repopath, NoScriptPoll
from t import get_repodir,get_datadir

repo = git.Repo(get_repodir())

def test_create_scriptrepo():
	"test to create an ensure the local repositery is unique."
	try:
		signed_repopath = sign_repopath(get_repodir(), get_datadir()+'unexist/')
	except NoScriptPoll, e:
		assert 1 != 2, 'can not avoid the script poll not exists.'

	signed_repopath = sign_repopath(get_repodir(), get_datadir()+'scriptpoll/')
	want_path = signed_repopath+'/.git'

	repo = create_scriptrepo(get_repodir(), get_datadir()+'scriptpoll/')
	assert repo.path == signed_repopath+'/.git', repo.path

	# clean
	import os
	os.system('rm -rf '+signed_repopath)

def test_get_blob():
	"test to get blob with spefied commit id."
	repo = git.Repo(get_repodir())
	blob = repo.get_blob('test_get.sh')
	assert blob.name == 'test_get.sh'

	blob = repo.get_blob('test_2.sh')
	assert blob.name == 'test_2.sh'

def stest_get_diffrent_ver():
	"test to get diffrent version content of the file."
	wants = {
		# ver 2
		'a8e7a099d227b0670962644b0407cf436b6cb01d':
		"""#/usr/bin/env bash
echo 'I am test script. v2'
"""
		,
		# ver 1
		'3472eb6f525ac63902777919d78fc973f29e4054':
"""#/usr/bin/env bash
echo 'I am test script.'
"""
}
	for ver, want_txt in wants.items():
		file = repo.get_blob('test_get.sh',ver)
		assert file.name == 'test_get.sh'
		assert file.data == want_txt, want_txt
