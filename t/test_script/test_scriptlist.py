from lazyscript.script import ScriptsList
from t import get_repodir, get_datadir

scripts_list = ScriptsList(get_datadir()+'/source.list')
repo_path = get_repodir()

def test_save_list():
	"test to save source list."
	list = []
	list.append({'name':'firstscript',
			   'tag':'vim',
			   'category':'editor',
			   'repo':repo_path,
			   'ver':''})
	
	scripts_list.save(list)

def test_load_list():
	"test to load source list."
	scripts_list.update()
	assert scripts_list.items()[0]['name'] == 'firstscript',\
			"can not load source."

def test_from_repo():
	"test to create a source list from a git repositry."
	list = ScriptsList.from_repo(get_datadir()+'scriptspoll/7796c33a9348485b055f671c686568b0/')
	list.path = get_datadir()+'/scripts.list'
	list.save()
