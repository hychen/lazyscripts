import sys
import os
import shutil
import ConfigParser

from lazyscripts import pool
from lazyscripts import utils
from lazyscripts import script as lzsscript

from lazyscripts.lengacy.repo import git as lengacygit
from lazyscripts.lengacy.category import _i18n_name, icon_path_name
from lazyscripts.lengacy import script as lengacyscript

#{{{ get i18n
def _i18nopt(name, local):
    local = "%s_%s" % (local[0:2], local[2:4].upper())
    return "%s[%s]" % (name, local)
#}}}

def run():
    #{{{ sys
    try:
        old = sys.argv[1]
        new = sys.argv[2]
    except IndexError:
        print "oldpool dest"
        exit()
    #}}}

    #{{{create new-style repo template.
    if os.path.exists(new):
        shutil.rmtree(new)
    os.mkdir(new)
    mypool = pool.GitScriptsPool.init_pool(new)
    print "Start to creating new pool:%s" % mypool.path
    #}}}

    #{{{desc.ini
    # add local and icon path into desc.ini
    print "Filling information of desc.ini"
    path = os.path.join(mypool.path,'desc.ini')
    iniparser = ConfigParser.ConfigParser()
    iniparser.read(path)

    print "\t[Icon]"
    for k,v in icon_path_name.items():
        print "\tadd %s - %s" % (k,v)
        iniparser.set('icon_path', k.capitalize(), v)
    print "\t[Local]"

    for k,v in _i18n_name.items():
        print "\tadd %s" % k
        for name, loc_val in v.items():
            iniparser.set('category',_i18nopt(name, k), loc_val)

    iniparser.write(open(path,'w'))
    del(iniparser)
    #}}}

    print "\nConverting category..."
    # load set from lengacy repo.
    repo = lengacygit.Repo(old)
    for cat in repo.categories:
        print "\t[%s]" % cat.name
        mypool.add_category(cat.name)
        # convert script
        for script_blob in cat.items():
            # get new script id
            newscriptpath = utils.ext_ospath_join(mypool.path, cat.name, script_blob[0].lower())
            if newscriptpath.endswith('.sh'):
                newscriptpath = newscriptpath.replace('.sh', '')

            #print "\tconvering %s to %s" % (script_blob[0], newscriptpath)

            oldscript =  lengacyscript.ScriptMeta.from_string(script_blob[1].data)
            meta = oldscript.datas
            # create script  template.
            script = lzsscript.Script.init_script(newscriptpath, oldscript.name, oldscript.authors, True)

            # convert metadata
            path = os.path.join(newscriptpath,'desc.ini')
            _parser = ConfigParser.ConfigParser()
            _parser.read(path)
            _parser.set('info', 'license', meta.get('license'))
            def _t(parser, meta, k):
                for loc_k, loc_v in meta[k].items():
                    _i18name = _i18nopt(k, loc_k)
                    _parser.set('info', _i18name, loc_v)

            #info
            if 'name' in meta:
                _t(_parser, meta, 'name')
            if 'name' in meta:
                _t(_parser, meta, 'desc')
            if 'warn' in meta:
                _t(_parser, meta, 'warn')
            #
            #
            _filter = ['hide', 'debian', 'ubuntu']
            for attrname in _filter:
                v = False
                if meta.has_key(attrname):
                    v = True
                _parser.set('attrs', attrname, v)
            # platform
            platforms =  meta.get('platform')
            if platforms:
                for plat in platforms:
                    plat = plat.lower()
                    _parser.set('attrs', plat, True)
            _parser.write(open(path, 'w'))

    print "\n-------\nDone."
