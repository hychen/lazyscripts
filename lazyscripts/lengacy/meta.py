#!/usr/bin/env python
# -*- encoding=utf8 -*-
# @author '2009 Hsin Yi Chen (陳信屹) <ossug.hychen@gmail.com>'
"""reserved words list. these words used to document 
the metadata of the script."""
__reserved_words__ = [
    'category',
    'maintainer',
    'author',
    'ubuntu',
    'debian',
    'platform',
    'license',
    'child',
    'hide'
]

"""these words has i18n way."""
__i18n_words__ = ['name','desc','warn']

__reserved_words__.extend(__i18n_words__)

def make_meta(word, value):
    """
    make a meta.

    @param world str the name of the reserved word.
    @param value str the value of the reserved word.
    @return (key,value)
    """
    if not word: 
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
def debian_mark(value):
    return ('debian', True)

def ubuntu_mark(value):
    return ('ubuntu', True)

def hide_mark(value):
    return ('hide', True)

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

def maintainer_mark(value):
    """
    the parser of the reserved word maintaner.

    @param str value string.
    @reutrn (key, (value))
    """
    return ('maintainers', (value,))

def platform_mark(value):
    """
    the parser of the reserved word platform.

    @param str value string.
    @reutrn (key, [value])
    """
    return ('platform', value.split(' '))

def child_mark(value):
    """
    the parser of the reserved word child.

        @child Customize/ie6_after.sh Customize/ie6_bal.sh

    @param str value string.
    @reutrn (key, [value])
    """
    ret = []
    splited = value.split(' ')
    for e in splited:
        splited_e = e.split('/')

        count = len(splited_e)
        se = {}
        try:
            if count == 1:
                se['id'] = splited_e[0]
            elif count == 2:
                se['id'] = splited_e[1]
                se['category'] = splited_e[0]
            else:
                print "[DEBUG] count: %d" % count
                print "[DEBUG] string value: %s" % value
                print "[DEBUG] string e: %s" % e
                raise "Meta Data Child Syntax Error" 
        except IndexError:
            continue
        ret.append(se)
    return ('childs', ret)
    

if __name__ == '__main__':
    make_meta('desc_zhTW', """
# hihihi
""")

