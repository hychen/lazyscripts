#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# Copyright © 2010 Hsin Yi Chen
#
# Lazyscripts is a free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This software is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this software; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
"""Handles Script Pool
"""

import ConfigParser
import os
import platform
import shutil
import tempfile

from lazyscripts import distro
from lazyscripts import git
from lazyscripts import utils
from lazyscripts import script as lzsscript

class DirectoryIsAScriptPoolError(Exception):
    "Raises exception when init a direcotry wich is a scripts pool."

class NoI18nSectionError(Exception):
    "Raises exception when get undefiend secion in pool/desc.ini"

#{{{def create_pooldescfile(dirpath, maintainers=''):
def create_pooldescfile(dirpath, maintainers=''):
    with open(os.path.join(dirpath, 'desc.ini'),'w') as f:
        f.write("\n".join([
        '[info]',
        'maintaners=%s' % maintainers,
        '[icon_path]',
        '[category]',
        '']))
#}}}

#{{{def is_scriptspool(dirpath):
def is_scriptspool(dirpath):
    """checks if the directory is a scriptspool.

    @param str dirpath directory path.
    @return bool
    """
    if os.path.isfile(os.path.join(dirpath,'desc.ini')):
        return True
    return False
#}}}

#{{{def init_gitpool_bare(path):
def init_gitpool_bare(path):
    os.mkdir(path)
    git.cmd.Git(path).init('--bare')
    # create a work tree.
    wkpath = os.path.join(tempfile.gettempdir(), 'tmppool')
    os.mkdir(wkpath)
    create_pooldescfile(wkpath)
    wkgit = git.cmd.Git(wkpath)
    wkgit.init()
    wkgit.add('.')
    wkgit.commit('-m init')
    wkgit.branch('stable')
    wkgit.remote('add', 'origin', path)
    wkgit.push('--all')
    shutil.rmtree(wkpath)
#}}}

class ScriptsPool(object):
    #{{{desc
    """
    ScriptPool - hold scripts.
    """
    #}}}

    #{{{attrs
    "A file describes script pool."
    DESC_DEFFILE = 'desc.ini'

    "A file defines i18n keywords"
    I18N_DEFFILE = 'i18n.ini'
    #}}}

    #{{{def current_pkgsourcelist(self):
    @property
    def current_pkgsourcelist(self):
        filename = utils.ext_ospath_join(self.path,
                                        'sources.d',
                                        self.dist.pkgsrc_name)
        if not os.path.exists(filename):    return None
        keylist = utils.ext_ospath_join(self.path,
                                        'sources.d',
                                        'keylist.txt')
        return filename, keylist
    #}}}

    #{{{def __init__(self, path, recommands_list=None):
    def __init__(self, path, recommands_list=None):
        self.path = path
        self.recommands_list = recommands_list
        self.dist = distro.Distribution()
        self.load()
    #}}}

    #{{{def _load(self):
    def load(self):
        self._set_ids = [ e for e in os.listdir(self.path)
                            if not e.startswith('.') and
                               os.path.isdir(os.path.join(self.path,e)) and
                               e.istitle()]
        self._scripts = {}
        self.script_filters = {}
        self.script_filters[self.dist.name] = True
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(os.path.join(self.path, 'desc.ini'))
        self.parser.read(os.path.join(self.path, 'recommands.ini'))
        self.maintainers = ''
        if self.parser.has_section('info') and \
           self.parser.has_option('info', 'maintainers'):
                self.maintainers = self.parser.get('info', 'maintainers')
    #}}}

    #{{{def save(self):
    def save(self):
        self.parser.write(open(os.path.join(self.path,'desc.ini'),'w'))
        self.load()
    #}}}

    #{{{def init_pool(dirpath, **kdws):
    @classmethod
    def init_pool(cls, dirpath, **kwds):
        "create a scripts pool."
        if is_scriptspool(dirpath):
            raise DirectoryIsAScriptPoolError(
                "The directory %s is a scriptspool already." % dirpath)
        create_pooldescfile(dirpath, kwds.get('maintainers'))
        return cls(dirpath)
    #}}}

    #{{{def get_iconpath(self, set_id):
    def get_iconpath(self, set_id):
        if set_id not in self._set_ids: return None
        if not self.parser.has_option('icon_path', set_id): return None
        return self.parser.get('icon_path', set_id)
    #}}}

    #{{{def get_i18n(self, type, set_id, lang):
    def get_i18n(self, section, set_id, lang='en_US'):
        """get other language name, if no others, return en_US.

        @param str section section name of desc.ini
        @param str set_id
        @param str lang Languange
        @return str i18n name
        """
        if not section in self.parser.sections():
            raise NoI18nSectionError
        query = '%s[%s]' % (set_id, lang)
        if self.parser.has_option(section, query):
            return self.parser.get(section, query)
        return set_id
    #}}}

    #{{{def get_recommands(self, set_id):
    def get_recommands(self, set_id):
        """get recommanded scripts.

        @param str set_id
        @param str lang Languange
        @return str i18n name
        """
        if set_id in self._set_ids and \
           self.parser.has_section(set_id):
            return self.parser.options(set_id)
        return []
    #}}}

    #{{{def recommand_script(self, category, script_id):
    def recommand_script(self, category, script_id):
        if not self.parser.has_section(category):
            return False
        return script_id in self.parser.options(category)
    #}}}

    #{{{def categories(self):
    def categories(self):
        """get categories.

        @return list which has name of categories.
        """
        return self._set_ids
    #}}}

    #{{{def add_category(self, categoryname, langdefs=None):
    def add_category(self, categoryname, langdefs=None):
        """add a category.

        @param str category name
        @langdefs dict a dict has lang-value paire.

            e.x {'zh_TW':'名稱'}
        """
        os.mkdir(os.path.join(self.path,categoryname))
        if langdefs:
            for lang, val in langdefs.items():
                q = '%s[%s]' % (categoryname, lang)
                self.parser.set('category', q, val)
            self.parser.write(open(os.path.join(self.path,'desc.ini'),'w'))
    #}}}

    #{{{def remove_category(self, categoryname):
    def remove_category(self, categoryname):
        """remove a category.

        @param str category name.
        """
        shutil.rmtree(os.path.join(self.path,categoryname))
        # find matched categories.
        #  remove all .
        for cat in self.parser.options('category'):
            if cat[0:-7] == categoryname.lower():
                self.parser.remove_option('category', cat)
    #}}}

    #{{{def scripts(self, set_id, lang):
    def scripts(self, set_id=None, lang=None):
        """get scripts by spefic set id.

        @param str set_id
        @return a dict contains many Script instance.
        """
        if not set_id:
            if not self._scripts:
                for set_id in self.categories():
                    self._scripts.setdefault(set_id, self._lazy_mk_set(set_id, lang))
            return self._scripts
        return self._scripts.setdefault(set_id, self._lazy_mk_set(set_id, lang))
    #}}}

    #{{{def _lazy_mk_set(self, set_id, lang):
    def _lazy_mk_set(self, set_id, lang=None):
        ret = []
        set_path = os.path.join(self.path,set_id)
        for script_id in os.listdir(set_path):
            script = lzsscript.Script(os.path.join(set_path,script_id), lang)

            # skip if script is not avaliable with distro and
            # platform.
            if not script.is_avaliable(self.script_filters):
                continue
            script.category = set_id
            ret.append(script)
        return ret
    #}}}
pass

class GitScriptsPool(ScriptsPool):

    """
    Scripts Pool with git backend, version control support.
    """
    #{{{def __init__(self, path, recommands_list=None):
    def __init__(self, path, recommands_list=None):
        self.gitapi = git.cmd.Git(path)
        super(GitScriptsPool, self).__init__(path, recommands_list)
    #}}}

    #{{{def init_pool(dirpath, **kdws):
    @classmethod
    def init_pool(cls, dirpath, **kwds):
        """
        create a new scripts pool.

        @param str dirpath directory path.
        @param str upstream upstream git repository. (optional)
        @param str origin remote git repository. (optional)
        """
        if is_scriptspool(dirpath):
            raise DirectoryIsAScriptPoolError(
                "the directory %s is a scriptspool already." % dirpath)

        pool = cls(dirpath)
        pool.gitapi.init()

	# checkout local branch by each remote branch.
        for k in kwds:
            if k in ('upstream', 'origin') and kwds.has_key(k):
                pool.gitapi.remote('add', k, kwds[k])
                pool.gitapi.fetch(k)
		# get remote branch name.
		ret=pool.gitapi.branch('-r')
		branchs = [ e.replace('upstream/','').strip() for e in ret.split('\n')]
		for branch in branchs:
                	pool.gitapi.checkout('upstream/%s' % branch, b=branch)

        # if there is no desc.ini after pull remote respostiroy,
        # means this totally new, do initialization.
        if not os.path.exists(os.path.join(dirpath,'desc.ini')):
            create_pooldescfile(dirpath, kwds.get('maintainers'))
            pool.gitapi.add('.')
            pool.gitapi.commit('-m "init lazyscripts pool."')
        return cls(dirpath)
    #}}}

    #{{{def checkout(self, rev):
    def checkout(self, rev):
        """checkout content by rev

        @param str rev reversion of git.(tag/branch/commit)
        """
        self.gitapi.checkout(rev)
        self.gitapi.rebase(rev)
    #}}}
pass
