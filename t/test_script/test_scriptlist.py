from lazyscripts.script import ScriptsList
from t import get_repodir, get_datadir, remote_repo

scripts_list = ScriptsList(get_datadir()+'/scripts.list')
repo_path = get_repodir()

def test_save_list():
	"test to save scripts list."
	list = []
	list.append({'name':'firstscript',
			   'tag':'vim',
			   'category':'editor',
			   'repo':repo_path,
			   'ver':''})
	
	scripts_list.save(list)

def test_load_list():
	"test to load scripts list."
	scripts_list.update()
	assert scripts_list.items()[0]['name'] == 'firstscript',\
			"can not load source."

def test_from_repo():
	"test to create a source list from a git repositry."
	list = ScriptsList.from_repo(remote_repo, get_repodir())
	list.path = get_datadir()+'/scripts.list'
	list.save()
