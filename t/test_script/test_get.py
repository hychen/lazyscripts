from lazyscript.script import ScriptSet
from lazyscript import get_settings_from_string
from t import get_repodir, get_datadir

set = ScriptSet.from_repo(get_repodir())

def test_load_settings():
	"test to get script settings."
	def t(string, msg=''):
		settings = get_settings_from_string(string)
		assert settings['name'] == 'h1', msg

	full = """
name='h1'
desc='hello'
author='bob'
run_file=''
website=''
"""
	few = """
name='h1'
desc='hello'
author='bob'
"""
	t(full)
	t(few, 'faild if optionl variable not assign.')

	del(t)

def test_get_script():
	"test to get script."
	script = set.get('firstscript')
	assert script.name == 'firstscript', 'can not get dirbase script.'

#	script = set.get('onefilescript.sh')
#	assert script.name == 'onefirstscript.sh', 'can not get filebase script.'

def test_get_categories():
	'test to get categories form source list'
	set = ScriptSet.from_sourcelist(get_datadir()+'/source.list')
	assert set.categories('editor')[0].name == 'firstscript', set.categories
