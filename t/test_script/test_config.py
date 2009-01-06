from lazyscript.script import ScriptConfig
from t import get_repodir, get_datadir

def test_form_str():
	content = """
 @brief script brief
 @name installvim
 @author hychen
 @license Apache v2
"""
	config = ScriptConfig.from_string(content)
	assert config.name == 'installvim', config.name
	assert config.author == 'hychen', config.author
	assert config.license == 'Apache v2', config.license
	assert config.brief == \
			'script brief',config.brief
