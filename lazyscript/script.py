import cPickle
import re
import sys

from lazyscript.repo import git
from lazyscript import meta

class MissingScriptInitFile(IOError):
	pass

class ScriptMeta(object):

	"""
	the script_meta of the script.
	"""
	def __init__(self, settings):
		self.__dict__['datas'] = settings
		self.lang = 'zhTW'

	def __getattr__(self, key):
		try:
			return getattr(self.datas,key)
		except:
			return getattr(self,key)

	@property
	def name(self, lang=None):
		if not lang:
			return self.datas['name'][self.lang]
		return self.datasp['name'][lang]

	@property
	def desc(self, lang=None):
		if not lang:
			return self.datas['desc'][self.lang]
		return self.datasp['desc'][lang]

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
			if attrs.get(meta_entry[0]):
				try:
					attrs[meta_entry[0]].update(meta_entry[1])
					attrs[meta_entry[0]].extend(meta_entry[1])
					attrs[meta_entry[0]] = attrs[meta_entry[0]] +\
											meta_entry[1]
				except AttributeError:
					pass
			else:
				attrs.setdefault(meta_entry[0], meta_entry[1])
		return attrs		

class Script(object):

	def __init__(self, backend, script_meta):
		self.backend = backend
		self.desc= script_meta.desc
		self.author = script_meta.author
		self.website = script_meta.website
		self.name = script_meta.name or self.backend.name
		self.runfile = script_meta.runfile or self.backend.name

	def __getattr__(self, key):
		try:
			return getattr(self, key)
		except AttributeError:
			return getattr(self.backend, key)

	@classmethod
	def from_tree(cls, tree):
		"""get script from git tree."""
		blob = tree.get('__init__.py')

		if not blob:
			raise MissingScriptInitFile(tree.name)

		script_meta = ScriptMeta.from_string(blob.data)
		if not script_meta:
			return script_meta

		return cls(tree, script_meta)
	
	@classmethod
	def from_blob(cls, blob):
		"""get script from git blob"""
		script_meta = ScriptMeta.from_string(blob.data)
		if not script_meta:
			return script_meta
		
		return cls(tree, script_meta)
			
class ScriptSet(object):

	def __init__(self, repo=None):
		self.repo = repo
		self._repo_table= {}
		self._categories = {}

	@property
	def is_root(self):
		"checks if it is a root set."
		if not self.repo:
			return True

	def categories(self, name):
		"""
		get categories in set.
		
		@param str category name.
		"""
		self._mk_scripts()
		return self._categories.get(name)

	def _mk_scripts(self):
		"lazy make script instance in set. "
		# repo table is created when getting script set from
		# source list.
		for repo, queries in self._repo_table.items():
			set = ScriptSet.from_repo(repo)
			# queries is a lot settings from the soure entry in 
			# source list. see source entry formate.
			for query in queries:
				script = set.get(query['name'])
				if not self._categories.get(query['category']):
					self._categories[query['category']] = []
				self._categories[query['category']].append(script)

	@classmethod
	def from_sourcelist(cls, source_list):
		"""
		get script set from source list.
		"""
		# get last version.
		source_list.update()
		set =  cls()
		if not source_list.items():
			return None

		for item in source_list.items():
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

	def get(self, script_name, ver=None):
		"""
		get script.

		@param script_name str script name.
		@param ver str version id (means commit id in git.)
		@return Script
		"""
		obj = self.repo.get_blob(script_name, ver)

		if git.is_tree(obj):
			script = Script.from_tree(obj)
		else:
			script = Script.from_blob(obj)
		return script

class SourceList(object):

	def __init__(self, path):
		self.path = path
		self.content = ''
		self._items = []

	def items(self):
		return self._items

	def save(self, items):
		self._items = items
		cPickle.dump(self._items, open(self.path,'w'))

	def update(self):
		self.content = self._load_from_file(self.path)
		self._items = self._unserilize(self.content)
		

	def _load_from_file(self, path):
		return open(path, 'r').read()

	def _unserilize(self, string):
		return cPickle.loads(string)
