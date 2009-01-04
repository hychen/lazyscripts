from lazyscript.script import ScriptSet
from lazyscript import get_settings_from_string
from t import get_repo

set = ScriptSet.get_from(get_repo())

def test_load_settings():
	"get script settings."
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
	"get script."
	script = set.get('firstscript')
	assert script.name == 'firstscript', 'can not get dirbase script.'

#	script = set.get('onefilescript.sh')
#	assert script.name == 'onefirstscript.sh', 'can not get filebase script.'
