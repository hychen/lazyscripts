from lazyscript import get_settings_from_string
from lazyscript.repo import git

class MissingScriptInitFile(IOError):
	pass

class Script(object):

	def __init__(self, backend, kwds):
		self.backend = backend
		self.desc = kwds['desc']
		self.author = kwds['author']
		self.website = kwds.get('website')
		self.name = kwds.get('name') or self.backend.name
		self.run_file = kwds.get('run_file') or self.backend.name

	@classmethod
	def from_tree(cls, tree):
		"""get script from git tree."""
		blob = tree.get('__init__.py')

		if not blob:
			raise MissingScriptInitFile(tree.name)

		# FIXME: dirty way to load script config.
		attrs = get_settings_from_string(blob.data)
		if not attrs:
			return None

		script =  cls(tree, attrs)
		return script
	
	@classmethod
	def from_blob(cls, blob):
		"""get script from git blob"""
		raise NotImplemented
		
			
class ScriptSet(object):

	def __init__(self, repo):
		self.repo = repo

	@classmethod
	def get_from(cls, repo_path):
		"""
		get script set from repository.

		@param repo_path str repository path.
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
