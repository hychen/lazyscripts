import git

def is_tree(obj):
    return type(obj) == git.Tree

def is_blob(obj):
    return type(obj) == git.Blob

def clone_repo(path, dest_dir):
    from os import system
    system("git clone %s %s" % (path,dest_dir) )

def is_git_dir(d):
    return git.utils.is_git_dir(d)

class Repo(git.Repo):
    
    @property
    def categories(self):
        dir = []
        try:
            dirs = self.commits('HEAD')[0].tree.items()
        except IndexError:
            return None
        # the items of the tree element is a tuple. e.x ('name', obj)
        # so we know the type by second element in tuple.
        return [ dir[1] for dir in dirs if is_tree(dir[1]) ]

    def fork_index(self, path, **kwds):
        options = {'n':True}
        options.update(kwds)
        self.git.clone(self.path, path, **options)
        return Repo(path)

    def get(self, name):
        return self.get_blob(name)

    def get(self, obj_name, commit_id='', branch=''):
        """
        get object by commit.

        @commit_id str
        @obj_name str
        """
        if not commit_id:
            commit_id = 'HEAD'

        if branch:
            commit_id += branch+'~'+commit_id

        try:
            tree = self.commits(commit_id)[0].tree
        except IndexError:
            return None

        return tree.get(obj_name)
