from lazyscripts.category import Category
from lazyscripts.script import ScriptSet, ScriptsList, ScriptsBuilder
from lazyscripts.repo import git, sign_repopath
from t import get_repodir, get_datadir, remote_repo

set = ScriptSet.from_scriptslist(
            ScriptsList(get_datadir()+'/scripts.list'), True)

_repos = {remote_repo:git.Repo(get_repodir()+'/'+sign_repopath(remote_repo))}
_cat = Category(name='Networking', scripts_builder=ScriptsBuilder(_repos))
e = {'repo': remote_repo, 
    'category': 'Networking',
    'name': 'ie6', 
    'id': 'ie6',
    'selected':False}
_cat.add_entry(e)

def test_get_script_from_category():
    "test to get script form a category."
    assert 'Script' == _cat.get('ie6').__class__.__name__

def test_get_categories():
    'test to get categories form scripts list'
    # checks all items are Category class.
    for category in set.categories():
        assert 'Category' == category.__class__.__name__, category.__class__

    # checks get Category Instance by spefied category name.
    ast_cats = ['Networking', 'Graphic', 'Localization', 
                'Productivity', 'Entertain', 'Customize','Game', 
                'Multimedia']
    for ast_category in ast_cats:
        cat = set.categories(ast_category)
        cat.lang = 'enUS'
        assert ast_category == cat.name, cat.name

def test_get_sccript_from_category():
    'test to get scripts form category.'
    cat = set.categories('Game')
    script = cat.get('PCSX.sh')
    assert 'Script' == script.__class__.__name__

def test_get_subscript():
    subscripts = _cat.get('ie6').get_subscripts()
    assert subscripts[0].name == 'add-apt-sources', subscripts[0].name
