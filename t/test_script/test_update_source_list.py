from lazyscript.script import SourceList
from t import get_repodir, get_datadir

source_list = SourceList(get_datadir()+'/source.list')
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
