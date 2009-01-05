from lazyscript.script import ScriptSet, SourceList
from lazyscript import get_settings_from_string
from t import get_repodir, get_datadir

set = ScriptSet.from_repo(get_repodir())

def test_get_script():
	"test to get script."
	script = set.get('firstscript')
	assert script.name == 'hellovim', 'can not get dirbase script.'

#	script = set.get('onefilescript.sh')
#	assert script.name == 'onefirstscript.sh', 'can not get filebase script.'

def test_get_categories():
	'test to get categories form source list'
	set = ScriptSet.from_sourcelist(
				SourceList(get_datadir()+'/source.list'))
	assert set.categories('editor')[0].name == 'hellovim', set.categories
