# -*- encoding=utf8 -*
from lazyscripts import meta
from lazyscripts.script import ScriptMeta

def test_author():
    "test to parse author mark."
    e = ('author', '2007 billy')
    ameta = meta.make_meta(e[0],e[1])
    assert ameta[0] == 'authors'
    assert ameta[1] == ('2007 billy',)

def test_platform():
    "test to parse platform mark."
    e = ('platform', 'i386 adm64')
    ameta = meta.make_meta(e[0],e[1])
    assert ameta[0] == 'platform'
    assert ameta[1] == ['i386','adm64']

def test_i18n():
    "test to i18n process of the meta mark."
    e = ('name_zhTW', '我是中文')
    ameta = meta.make_meta(e[0],e[1])
    assert ameta[0] == 'name'
    assert ameta[1] == {'zhTW':'我是中文'}

    e = ('desc_zhTW', '我是中文')
    ameta = meta.make_meta(e[0],e[1])
    assert ameta[0] == 'desc'
    assert ameta[1] == {'zhTW':'我是中文'}

    ameta = meta.make_meta('name','no_lang')
    assert ameta is None,ameta
    
def test_get_script_meta():
    """
    test to get the metadata of the script.
    """
    s = """#
# @name_zhTW '中文script名。'
# @name_enUS 'english script name.'
# @desc_zhTW '中文script說明
#             第2行'
# @debian ''
# @hide 
# @category 'Custonmize'
# @maintainer 'billy'
# @author '2007 bob'
# @author '2007 john'
# @author '2008 hou'
"""
    metas = ScriptMeta.from_string(s)
    metas.lang = 'zhTW'
    assert metas.name == '中文script名。', metas.name
    assert metas.desc == """中文script說明
第2行""", metas.desc
    metas.lang = 'enUS'
    assert metas.name == 'english script name.'
    assert metas.authors == ('2007 bob','2007 john', '2008 hou'), metas.authors
    assert metas.maintainers == ('billy',), metas.maintainers
    assert metas.category == 'Custonmize', metas.category
    assert metas.debian == True, metas.debian
    assert metas.hide == True, metas.hide
