#!/usr/bin/env python
# -*- encoding=utf8 -*-
# @author '2009 Hsin Yi Chen (陳信屹) <ossug.hychen@gmail.com>'
import cPickle
import re
import sys
import os

from lazyscripts.lengacy.repo import git, \
                            create_scriptrepo, \
                            sign_repopath, \
                            get_repo_for_distro
from lazyscripts.lengacy import meta
from lazyscripts.lengacy.category import Category
from lazyscripts.lengacy.info import get_distro
from lazyscripts.lengacy.util import osapi
from StringIO import StringIO
from os import path as os_path

def _get_root_path ():
    dir = os_path.dirname (__file__) + '/../'
    root = os_path.abspath (dir)
    return root

class ScriptMeta(object):

    """
    the script_meta of the script.
    """
    def __init__(self, settings):
        self.__dict__['datas'] = settings
        self.lang = 'zhTW'

    def __getattr__(self, key):
        try:
            try:
                return self.datas[key][self.lang]
            except:
                return self.datas[key]
        except KeyError:
            return ''

    @classmethod
    def from_file(cls, file):
        "get the script meta from a file."
        return cls.from_string( file.read() )

    @classmethod
    def from_string(cls, string):
        """
        get the script script_meta from string.

        @parma str string.
        @return ScriptMeta
        """
        if not string:
            return None

        return cls(cls.parse_string(string))

    @staticmethod
    def parse_string(string):
        attrs = {}
        import re
        founds = re.findall('\s*@(.*?)\s+(\'(.*|.*\n.*)\')?', \
                    string ,\
                    re.MULTILINE)
        for found in founds:
            meta_entry = ()
            if len(found) == 3:
                meta_entry = meta.make_meta(found[0],found[2])
            elif len(found) == 1:
                meta_entry = meta.make_meta(found[0],None)
            # skip line of the script content with wrong meta sytax.
            if not meta_entry:
                continue

            # @FIXME: dirty hack.
            if not attrs.get(meta_entry[0]):
                attrs.setdefault(meta_entry[0], meta_entry[1])
            else:
                if type(attrs[meta_entry[0]]) == dict:
                    attrs[meta_entry[0]].update(meta_entry[1])
                elif type(attrs[meta_entry[0]]) == list:
                    attrs[meta_entry[0]].extend(meta_entry[1])
                elif type(attrs[meta_entry[0]]) == tuple:
                    attrs[meta_entry[0]] = attrs[meta_entry[0]] +\
                                            meta_entry[1]
        return attrs

class Script(object):

    def __init__(self, backend, script_meta):
        self.backend = backend
        self.desc= script_meta.desc
        self.author = script_meta.author
        self.website = script_meta.website
        self.name = script_meta.name or self.backend.name
        self.id = script_meta.id or self.backend.name
        self.childs = script_meta.childs
        self.hide = script_meta.hide
        self.debian = script_meta.debian
        self.ubuntu = script_meta.ubuntu
        # is it selected?
        self.selected = False

    def __getattr__(self, key):
        try:
            return getattr(self.backend, key)
        except AttributeError:
            return getattr(self, key)

    def get_subscripts(self):
        """
        get sub scripts depency.

        @return list Script
        """
        ret = []
        for script_meta in self.childs:
            if script_meta.has_key('category'):
                set = self.repo.get(script_meta.get('category'))
            else:
                set = self.repo

            script = Script.from_blob(set.get(script_meta.get('id')))
            if script:
                ret.append(script)
        return ret

    def save(self, dir_path):
        """
        create a excutabel file.
        """
        path = dir_path+self.id
        osapi.create_excuteablefile(path, self.data)

        for subscript in self.get_subscripts():
            subscript.save(dir_path)

    @classmethod
    def from_listentry(cls, repo, list_entry):
        """get a script from a entry in script.list ."""
        cat_tree = repo.get(list_entry['category'])
        if not cat_tree:
            raise "%s is not exists scripts.list out of date." % \
                list_entry['category']

        blob = cat_tree.get(list_entry['id'])
        if not blob:
            raise "script %s is not exists, scripts.list may out of date." % \
                            list_entry['id']

        script =  cls.from_blob(cat_tree.get(list_entry['id']))
        script.selected = list_entry.get('selected', False)

        return script

    @classmethod
    def from_tree(cls, tree):
        """get a script from git tree."""
        #@FIXME: unused code here.
        blob = tree.get('__init__.py')

        if not blob:
            raise MissingScriptInitFile(tree.name)

        script_meta = ScriptMeta.from_string(blob.data)
        if not script_meta:
            return script_meta

        return cls(tree, script_meta)

    @classmethod
    def from_blob(cls, blob):
        """get a script from git blob"""
        script_meta = ScriptMeta.from_string(blob.data)
        if not script_meta:
            # @TODO: log the script has no metadata.
            return None

        return cls(blob, script_meta)

class ScriptsBuilder(object):

    def __init__(self, repos):
        self.repos = repos
        self.entries = []

    def make_scripts(self):
        ret = {}
        for entry in self.entries:
            repo = self.repos.get(entry['repo'])
            script = Script.from_listentry(repo, entry)
            if not script.hide:
                ret[script.id] = script
        return ret

class ScriptSet(object):

    def __init__(self):
        self._repo_table= {}
        self._repos = {}
        self._categories = {}

    def categories(self, name=None):
        """
        get categories in set.

        @param str category name.
        """
        self._mk_scripts()
        if name:
            return self._categories.get(name)
        return self._categories.values()

    def _mk_scripts(self):
        "lazy make script instance in set. "
        # repo table is created when getting script set from
        # scripts list.
        for repo_path, list_entries in self._repo_table.items():
            for list_entry in list_entries:
                if not self._categories.get(list_entry['category']):
                    self._categories[list_entry['category']] = \
                                    Category(name=list_entry['category'],
                                             scripts_builder=ScriptsBuilder(self._repos))
                self._categories[list_entry['category']].add_entry(list_entry)

    def get_repo(self, repo_path):
        return self._repos.get(repo_path)

    @classmethod
    def from_scriptslist(cls, scripts_list, testmode=False):
        """
        get script set from source list.

        @param ScriptsList scripts_list
        @param boolean testmode to make diffrent  \
                    scriptspool directory.
        @return ScriptSet
        """
        # get last version.
        scripts_list.update()
        set =  cls()
        if not scripts_list.items():
            return None

        for item in scripts_list.items():
            if not set._repos.has_key(item.get('repo')):
                # clone the repostiry if the repositry is not exists.
                if testmode:
                    local_dir = _get_root_path()+'/t/datas/scriptspoll'
                else:
                    local_dir = _get_root_path() + '/scriptspoll'
                set._repos[item.get('repo')] = create_scriptrepo(item.get('repo'), local_dir)

            if not set._repo_table.get(item.get('repo')):
                set._repo_table[item.get('repo')] = []
            set._repo_table[item.get('repo')].append(item)
        return set

    @classmethod
    def from_repo(cls, repo_path):
        """
        get script set from repository.

        @param repo_path str repository path.
        @return ScriptSet
        """
        set = cls(repo=git.Repo(repo_path))
        return set

class ScriptsList(object):

    def __init__(self, path=None):
        if path:
            self.path = path
        else:
            self.path = 'scripts.list'
        self.content = ''
        self._items = []

    def items(self):
        return self._items

    def save(self, items=None):
        if items:
            self._items = items
        cPickle.dump(self._items, open(self.path,'w'))

    def update(self):
        #@TODO:refacotry me!!!!! by hychen
        if type(self.path) is str:
            self.content = self._load_from_file(self.path)
        else:
            if not self.content:
                self.content = self.path.read()
        self._items = self._unserilize(self.content)

    def _load_from_file(self, path):
        return open(path, 'r').read()

    def _unserilize(self, string):
        return cPickle.loads(string)

    @classmethod
    def get_by_detect(cls, testmode=False):
        """
        get SctipsList instance by detection automatically.

        @param boolean testmode
        @return obj ScriptsList
        """
        scripts_repo = get_repo_for_distro(get_distro(), testmode)
        scripts_repo.rebase()
        if not scripts_repo:
            raise "can not get repositry automatically."

        blob = scripts_repo.get('scripts.list')
        if not blob:
            raise "script.list is not exists in %s" % \
                                            scripts_repo.path
        return cls.from_blob(blob)

    @classmethod
    def from_blob(cls, blob):
        """
        make a scripts list file from git blob instance.

        @param Git.Blob blob
        @return ScritpsList
        """
        return cls(StringIO(blob.data))

    @classmethod
    def from_repo(cls, repo_path, local_dir=None):
        """
        make a script list from given repositry path.

        @param str repo_path repositry path.
        @return obj ScriptsList
        """
        list = ScriptsList()
        if local_dir:
            repo = git.Repo(local_dir+'/'+sign_repopath(repo_path))
        else:
            repo = git.Repo(repo_path)
        # update scripts.
        repo.rebase()

        for category in repo.categories:
            # @TODO: refactory -> category.scripts()
            for script_name,script_blob in category.items():
                script = Script.from_blob(script_blob)
                entry = {
                        'repo':repo_path,
                        'category':category.name,
                         'name':script.name,
                         'id':script_name,
                         'selected':False}
                list._items.append(entry)
        return list

class ScriptsRunner:

    def __init__(self, ui):
        self.tmp_dirname = '/tmp/lzs_run'
        self.startup_filename = 'lazybuntu_apply.sh'
        self.startup_path = "%s/%s" % (self.tmp_dirname,
                                        self.startup_filename)
        self.ui = ui

    def run_scripts(self, scripts):
        self.checkout_scripts(scripts)
        #@TODO:generic UI class interface.
        self.ui.pid = self.ui.final_page.term.fork_command(self.startup_path)

    def checkout_scripts(self, scripts):
        """
        storage the content of the scripts to temp dir, and write
        the script fiel path down to startup file will excute.

        @param scripts Script
        """
        self._init_tmpdir()
        self._copy_env_files()
        excute_entries = [
            '#!/bin/bash\n'
            'set -x\n'
            'cd '+self.tmp_dirname+'\n'
            'apt-get update\n\n'
            'source global_env.sh\n'
            'source user_env.sh\n' ]

        for script in scripts:
            excute_entries.append("%s/%s\n" %
                                    (self.tmp_dirname, script.id))
            script.save(self.tmp_dirname+'/')
        excute_entries.append("chown -R $REAL_USER: $REAL_HOME &> /dev/null\n")

        startup_file = osapi.create_excuteablefile(path=self.startup_path)
        startup_file.writelines(excute_entries)

    def _init_tmpdir(self):
        """
        create a clear temp dir.
        """
        if os.path.exists(self.tmp_dirname):
            import shutil
            shutil.rmtree(self.tmp_dirname)
        os.mkdir(self.tmp_dirname, 0777)

    def _copy_env_files(self):
        "copy environment variables export file"
        root_path = _get_root_path()
        if os.path.exists(self.tmp_dirname):
            import shutil
            shutil.copy(root_path + "/bin/global_env.sh", self.tmp_dirname)
            shutil.copy(root_path + "/tmp/user_env.sh", self.tmp_dirname)
