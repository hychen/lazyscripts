from commands import getoutput

def get_distro():
	"""
	get distrobution name and version code.

	@return tuple (distrobution name, distrobution version code)
	"""
	cmd = 'lsb_release'
	name = getoutput(cmd+' -is')
	code = getoutput(cmd+' -cs')
	return (name,code)
