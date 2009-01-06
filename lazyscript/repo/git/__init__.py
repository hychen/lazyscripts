import git

def is_tree(obj):
	return type(obj) == git.Tree

def is_blob(obj):
	return type(obj) == git.Blob

class Repo(git.Repo):

	def fork_index(self, path, **kwds):
		options = {'n':True}
		options.update(kwds)
		self.git.clone(self.path, path, **options)
		return Repo(path)

	def get_blob(self, blob_name, commit_id='', branch=''):
		"""
		get blob by commit.

		@commit_id str
		@blob_name str
		"""
		if not commit_id:
			commit_id = 'HEAD'

		if branch:
			commit_id += branch+'~'+commit_id

		try:
			tree = self.commits(commit_id)[0].tree
		except IndexError:
			return None

		return tree.get(blob_name)
