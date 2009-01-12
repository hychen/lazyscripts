
"""reserved words list. these words used to document 
the metadata of the script."""
__reserved_words__ = [
	'category',
	'maintaner',
	'author',
	'ubuntu',
	'debian',
	'platform',
	'license'
]

"""these words has i18n way."""
__i18n_words__ = ['name','desc']

__reserved_words__.extend(__i18n_words__)

def make_meta(word, value):
	"""
	make a meta.

	@param world str the name of the reserved word.
	@param value str the value of the reserved word.
	@return (key,value)
	"""
	if not word or not value:
		return None
	# process the value with basic i18n.
	try:
		(keyword, lang) = word.split('_')
		if keyword not in __reserved_words__:
			return None
		return _call_parser(keyword, value, lang)
	# process no-i18n value.
	except ValueError:
		if word in __i18n_words__:
			return None
		if word not in __reserved_words__:
			return None
		return _call_parser(word, value)

def _call_parser(word, value, lang=None):
	"""
	if the word has a parser, the parse the value.

	@param word str mark word.
	@param value str the value of the mark word.
	@param lang str the language of the value.(optional)
	"""
	try:
		fn = eval(word+'_mark')
	except NameError:
		fn = None

	if callable(fn):
		(word, value) = fn(value)
	
	if not lang:
		return (word, value)
	else:
		return (word,{lang:value})

## parsers of each mark words.
#
# if the function has `_mark` extention, it is a parser.
# for instance, the parser of the mark @author is author_mark 
# function in this module.
def desc_mark(value):
	ret = []
	for row in value.splitlines():
		if not row.startswith('#'):
			ret.append(row)
		else:
			ret.append(row.replace('#', ' ').strip())
	return ('desc', '\n'.join(ret))

def author_mark(value):
	"""
	the parser of the reserved word author.

	@param str value string.
	@reutrn (key, (value))
	"""
	return ('authors', (value,))

def maintaner_mark(value):
	"""
	the parser of the reserved word maintaner.

	@param str value string.
	@reutrn (key, (value))
	"""
	return ('mantainers', (value,))

def platform_mark(value):
	"""
	the parser of the reserved word platform.

	@param str value string.
	@reutrn (key, [value])
	"""
	return ('platform', value.split(' '))

if __name__ == '__main__':
	make_meta('desc_zhTW', """
# hihihi
""")

