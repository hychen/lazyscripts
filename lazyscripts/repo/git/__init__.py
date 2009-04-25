import git
from os import system

def is_tree(obj):
    return type(obj) == git.Tree

def is_blob(obj):
    return type(obj) == git.Blob

def clone_repo(path, dest_dir):
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

    def rebase(self):
        s = "cd %s && git pull" % self.path.replace('.git','')
        system(s)

    def get(self, obj_name, head="origin/stable"):
        """
        get object by commit.

        @param str obj_name git blob/tree name
        @param str head git commit id
        """
        if not head:
            head = "origin/stable"

        try:
           tree = self.commits(head)[0].tree
        except IndexError:
            return None

        return tree.get(obj_name)
