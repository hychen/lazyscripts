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

import os
import tempfile
import unittest

from lazyscripts import config as lzsconfig

class ConfigurationTestCase(unittest.TestCase):

    #{{{def setUp(self):
    def setUp(self):
        self.filename = os.path.join(tempfile.gettempdir(), 'config.ini')
        self._write([])
    #}}}

    #{{{def tearDown(self):
    def tearDown(self):
        os.remove(self.filename)
    #}}}

    #{{{def _read(self):
    def _read(self):
        return lzsconfig.Configuration(self.filename)
    #}}}

    #{{{def _write(self, lines):
    def _write(self, lines):
        with open(self.filename, 'w') as fileobj:
            fileobj.write('\n'.join(lines + ['']))
    #}}}

    #{{{def test_default(self):
    def test_default(self):
        self._write(['[defaults]',
        'pool='
        ])
        config = self._read()
        self.assertEquals('', config.get_default('pool'))
    #}}}

    #{{{def test_read_and_get_pool(self):
    def test_read_and_get_pool(self):
        self._write(
            ['[pool "local"]',
            "rev=stable",
            "upstream=git://upstream.git",
            "origin=git@user://myrepo.git"])
        config = self._read()
        self.assertEquals({'rev':'stable',
                            'origin':'git@user://myrepo.git',
                            'upstream':'git://upstream.git'},
                            config.get_pool('local'))
    #}}}

    #{{{def test_set_and_save(self):
    def test_set_and_save(self):
        config = self._read()
        config.set_default(pool='myrepo')
        self.assertEquals('myrepo', config.get_default('pool'))
        config.set_default(pool='new_myrepo')
        self.assertEquals('new_myrepo', config.get_default('pool'))

        config.set_pool('onlylocal_repo', rev='master')
        self.assertEquals('master', config.get_pool('onlylocal_repo')['rev'])
        config.save()

        configfile = open(self.filename, 'r')
        self.assertEquals(
                ['[pool "onlylocal_repo"]\n',
                 'origin = \n',
                 'rev = master\n',
                 'upstream = \n',
                 '\n',
                '[defaults]\n',
                'pool = new_myrepo\n',
                 '\n'],
                configfile.readlines())
        configfile.close()
        config2 = lzsconfig.Configuration(self.filename)
        self.assertEquals('master', config.get_pool('onlylocal_repo')['rev'])
        self.assertEquals('new_myrepo', config.get_default('pool'))
    #}}}
pass

def suite():
    return unittest.makeSuite(ConfigurationTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
