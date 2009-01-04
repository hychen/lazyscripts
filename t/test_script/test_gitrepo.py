from lazyscript.repo import git
from t import get_repo

repo = git.Repo(get_repo())

def test_get_blob():
	"""get blob with spefied commit id."""
	blob = repo.get_blob('test_get.sh')
	assert blob.name == 'test_get.sh'

	blob = repo.get_blob('test_2.sh')
	assert blob.name == 'test_2.sh'

def test_get_diffrent_ver():
	"""get diffrent version content of the file."""
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
