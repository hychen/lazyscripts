from lazyscript.script import ScriptList
from t import get_repodir, get_datadir

source_list = ScriptList(get_datadir()+'/source.list')
repo_path = get_repodir()

def test_save_list():
	"test to save source list."
	list = []
	list.append({'name':'firstscript',
			   'tag':'vim',
			   'category':'editor',
			   'repo':repo_path,
			   'ver':''})
	
	source_list.save(list)

def test_load_list():
	"test to load source list."
	source_list.update()
	assert source_list.items()[0]['name'] == 'firstscript',\
			"can not load source."

def test_from_repo():
	"test to create a source list from a git repositry."
	list = ScriptList.from_repo(get_datadir()+'scriptspoll/7796c33a9348485b055f671c686568b0/')
	assert len(list.items()) == 31
	list.path = get_datadir()+'/scripts.list'
	list.save()
