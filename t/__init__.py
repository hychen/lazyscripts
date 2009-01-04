from sys import path as python_path
from os import path as os_path

libdir = 'lazyscript'
testcase = 't'

def get_root():
	dir = os_path.dirname(__file__)+'/../'
	root= os_path.abspath(dir)
	return root


def get_repo():
	return get_root()+'/'+testcase+'/datas/'+'singlerepo'

def init_devenv():
	# set up lib dir.
	python_path.insert(0,get_root()+libdir)
	# set up test dir.
	python_path.insert(0,get_root()+testcase)

init_devenv()
