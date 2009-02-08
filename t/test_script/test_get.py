from lazyscript.script import ScriptSet, ScriptList
from t import get_repodir, get_datadir

set = ScriptSet.from_repo(get_repodir())

def test_get_categories():
	'test to get categories form source list'
	set = ScriptSet.from_sourcelist(
				ScriptList(get_datadir()+'/scripts.list'))
	assert set.categories('Network')[0].name == 'hellovim', set.categories
