
__author__ = 'Hsin Yi, Chen (hychen) <ossug.hychen@gmail.com>'
__version__ = '0.1.1'
__date__ = '2009-01-04'


def get_version():
	return __version__

def get_settings_from_string(string):
	"""
	get settings from string with python syntax.

	>>> string =\"\"\"
	... name='hello'
	... \"\"\"
	>>> get_settings_from_string(string)
	{name:'hello'}

	@param string 
	@return dict
	"""
	if not string:
		return {}

	# FIXME: dirty way to load script config.
	exec(string)
	settings = {}
	settings['desc'] = desc
	settings['author'] =  author
	# optional.
	try:
		settings['name'] = name
		settings['run_file'] = run_file
		settings['website'] = website
	except NameError, e:
		if e.message == "name 'name' is not defined":
			settings['name'] = None
		if e.message == "name 'run_file' is not defined":
			settings['run_file'] = None
		if e.message == "name 'website' is not defined":
			settings['website'] = None
	return settings
