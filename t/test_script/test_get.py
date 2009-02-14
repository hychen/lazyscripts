from lazyscript.script import ScriptSet, ScriptsList
from t import get_repodir, get_datadir

set = ScriptSet.from_scriptslist(
            ScriptsList(get_datadir()+'/scripts.list'))

def test_get_categories():
    'test to get categories form scripts list'
    set = ScriptSet.from_scriptslist(
                ScriptsList(get_datadir()+'/scripts.list'))
    # checks all items are Category class.
    for category in set.categories():
        assert 'Category' == category.__class__.__name__, category.__class__

    # checks get Category Instance by spefied category name.
    ast_cats = ['Networking', 'Graphic', 'Localization', 
                'Productivity', 'Entertain', 'Customize','Game', 
                'Multimedia']
    for ast_category in ast_cats:
        cat = set.categories(ast_category)
        assert ast_category == cat.name, cat.name

def test_get_sccript_from_category():
    'test to get scripts form category.'
    cat = set.categories('Game')
    script = cat.get('PCSX.sh')
    assert 'Script' == script.__class__.__name__
