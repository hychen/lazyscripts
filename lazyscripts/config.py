#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# Copyright © 2010 Hsin Yi Chen
#
# Lazyscripts is a free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This software is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this software; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
"""Handles the configuratoin file of Lazyscripts.

The formate of Lazyscripts config file is ini that the parser is built in
Python, it is easy to understand and write.
"""

import os
import re
import ConfigParser
import StringIO

class Configuration(object):
    """thin layer over `ConfigParser` from the Python standard library.

    In addition to providing some convenience methods, the class remembers
    the last modification time of the configuration file, and reparses it
    when the file has changed.
    """
    #{{{def __init__(self, filename):
    def __init__(self, filename):
        self.filename = filename
        self.parser = ConfigParser.ConfigParser()
        self._pools = {}
        self._lastmtime = 0
        self._is_dirty = False
        self.parse_if_needed()
    #}}}

    #{{{def parse_if_needed(self):
    def parse_if_needed(self):
        if not self.filename or \
           not os.path.isfile(self.filename):
            return False

        modtime = os.path.getmtime(self.filename)
        if modtime > self._lastmtime:
            self.parser._sections = {}
            self.parser.read(self.filename)
            self._lastmtime = modtime
            return True
        return False
    #}}}

    #{{{def set_default(self, **kwds):
    def set_default(self, **kwds):
        """set default option values.

        conf.set_default(pool='getgirl')

        @param dict **kwds
        """
        self._is_dirty = True
        if not self.parser.has_section('defaults'):
            self.parser.add_section('defaults')
        for key, val in kwds.items():
            self.parser.set('defaults', key, val)
    #}}}

    #{{{def get_default(self, key):
    def get_default(self, key):
        """get default setting by specified option name.

        @param str optname defautl option name.
        @return default option value.
        """
        return self.parser.get('defaults', key)
    #}}}

    #{{{def set_pool(self, poolname, **kwds):
    def set_pool(self, poolname, **kwds):
        """add pool setting.

        @param str poolname pool name.
        @param str rev git commit id/tag/branch
        @param str origin git repository url.
        """
        self._is_dirty = True
        default = {'rev':'stable'}
        section = self._pool_sectionname(poolname)
        if not self.parser.has_section(section):
            try:
                self.parser.add_section(section)
            except ConfigParser.DuplicateSectionError:
                raise DuplicatePoolError
        for k in ('origin','rev','upstream'):
            self.parser.set(section, k, kwds.get(k,default.get(k,'')))
    #}}}

    #{{{def get_pool(self, poolname):
    def get_pool(self, poolname):
        self._loadpools_if_needeed()
        return self._pools.get(poolname)
    #}}}

    #{{{def _pool_sectionname(self, poolname):
    def _pool_sectionname(self, poolname):
         return 'pool "%s"' % poolname
    #}}}

    #{{{def pools(self):
    def pools(self):
        """get all pool name

        @return list pool name
        """
        self._loadpools_if_needeed()
        return sorted(self._pools.keys())
    #}}}

    #{{{def _loadpools_if_needeed(self):
    def _loadpools_if_needeed(self):
        if not self._is_dirty and self._pools: return False
        for section in self.parser.sections():
            if not section.startswith('pool'):
                continue
            # variable section is 'pool "test"'', section[6:-1] is test
            attrs ={}
            for attr in self.parser.items(section):
                attrs[attr[0]] = attr[1]
            self._pools[section[6:-1]] = attrs
        return True
    #}}}

    #{{{def save(self):
    def save(self):
         if not self._is_dirty:
             return False
         os.rename(self.filename, self.filename+'.bak')
         with open(self.filename,'wb') as fp:
             self.parser.write(fp)
    #}}}

    #{{{def get_support_pools(self, distroname):
    def get_support_pools(self, distro_name, distro_ver, lang):
        poollist = []
        for section in self.parser.sections():
            if self.parser.has_option(section, distro_name)\
               and distro_ver in self.parser.get(section, distro_name).split(', ')\
               and lang in self.parser.get(section, 'lang').split(', '):
                poollist.append((section[6:-1], self.parser.get(section, 'desc')))
        return poollist

    #}}}
pass
