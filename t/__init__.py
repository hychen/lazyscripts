from sys import path as python_path
from os import path as os_path

libdir = 'lazyscript'
testcase = 't'

# defult scriptspool repositry path for testing.
remote_repo = "git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git"

def get_root():
	dir = os_path.dirname(__file__)+'/../'
	root= os_path.abspath(dir)
	return root

def get_datadir():
	return get_root()+'/'+testcase+'/datas/'

def get_repodir():
	return get_datadir()+'scriptspoll'

def init_devenv():
	# set up lib dir.
	python_path.insert(0,get_root()+libdir)
	# set up test dir.
	python_path.insert(0,get_root()+testcase)

init_devenv()
