import cPickle
import re
import sys
import os

from lazyscript.repo import git
from lazyscript import meta
from lazyscript.category import Category

class ScriptMeta(object):

    """
    the script_meta of the script.
    """
    def __init__(self, settings):
        self.__dict__['datas'] = settings
        self.lang = 'zhTW'

    def __getattr__(self, key):
        try:
            return self.datas[key]
        except KeyError:
            return None

    @property
    def name(self, lang=None):
        try:
            if not lang:
                return self.datas['name'][self.lang]
            return self.datasp['name'][lang]
        except KeyError:
            return None

    @property
    def desc(self, lang=None):
        try:
            if not lang:
                return self.datas['desc'][self.lang]
            return self.datasp['desc'][lang]
        except KeyError:
            return None

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
        founds = re.findall('\s*@(.*?)\s+\'(.*|.*\n.*)\'', \
                    string ,\
                    re.MULTILINE) 
        for found in founds:
            meta_entry = meta.make_meta(found[0],found[1])
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

    def __getattr__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            return getattr(self.backend, key)

    @classmethod
    def from_listentry(cls, repo, list_entry):
        """get a script from a entry in script.list ."""
        cat_tree = repo.get(list_entry['category'])
        if not cat_tree:
            return None
        return cls.from_blob(cat_tree.get(list_entry['id']))

    @classmethod
    def from_tree(cls, tree):
        """get a script from git tree."""
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
    def from_scriptslist(cls, scripts_list):
        """
        get script set from source list.
        """
        # get last version.
        scripts_list.update()
        set =  cls()
        if not scripts_list.items():
            return None

        for item in scripts_list.items():
            if not set._repos.has_key(item.get('repo')):
                set._repos[item.get('repo')] = git.Repo(item.get('repo'))

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
            self.path = 'script.list'
        self.content = ''
        self._items = []

    def items(self):
        return self._items

    def save(self, items=None):
        if items:
            self._items = items
        cPickle.dump(self._items, open(self.path,'w'))

    def update(self):
        self.content = self._load_from_file(self.path)
        self._items = self._unserilize(self.content)
        

    def _load_from_file(self, path):
        return open(path, 'r').read()

    def _unserilize(self, string):
        return cPickle.loads(string)

    @classmethod
    def from_repo(cls, repo_path):
        """
        make a script list from given repositry path.

        @param str repo_path repositry path.
        @return obj ScriptsList
        """
        list = ScriptsList()
        repo = git.Repo(repo_path)
    
        for category in repo.categories:
            # @TODO: refactory -> category.scripts()
            for script_name,script_blob in category.items():
                script = Script.from_blob(script_blob)
                entry = {
                        'repo':repo_path,
                        'category':category.name,
                         'name':script.name,
                         'id':script_name}
                list._items.append(entry)
        return list
