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

import ConfigParser
import os
import shutil
import tempfile
import unittest

from lazyscripts import pool as lzspool

class ScriptsPoolTestCase(unittest.TestCase):

    #{{{def setUp(self):
    def setUp(self):
        self.poolname = os.path.join(tempfile.gettempdir(), 'fakepool')
        os.mkdir(self.poolname)
    #}}}

    #{{{def tearDown(self):
    def tearDown(self):
        shutil.rmtree(self.poolname)
    #}}}

    #{{{def _write(self, filename, lines):
    def _write(self, filename, lines):
        with open(os.path.join(self.poolname, filename), 'w') as fileobj:
            fileobj.write('\n'.join(lines + ['']))
    #}}}

    #{{{def _load_pool(self):
    def _load_pool(self):
        return lzspool.ScriptsPool(self.poolname)
    #}}}

    #{{{def test_default(self
    def test_default(self):
        # is directory.
        self.assertFalse(lzspool.is_scriptspool(self.poolname))
        self._write('desc.ini',
        ['[info]','maintainers=Jabba <jabba@jabamo.org>']
        )
        self.pool = self._load_pool()
        self.assertTrue(lzspool.is_scriptspool(self.poolname))
        self.assertEquals('Jabba <jabba@jabamo.org>', self.pool.maintainers)
    #}}}

    #{{{def _mk_categories(self, categories):
    def _mk_categories(self, categories):
        for cat in categories:
            os.mkdir(os.path.join(self.poolname,cat))
    #}}}

    #{{{def test_load_and_get_catogory_list(self):
    def test_load_and_get_catogory_list(self):
        self._write('desc.ini', [])
        self._write('recommand.ini', [])
        self._mk_categories(('Network','Game','noncat'))
        pool = self._load_pool()
        self.assertEquals(['Network','Game'], pool.categories())
    #}}}

    #{{{def test_load_and_get_i18n(self):
    def test_load_and_get_i18n(self):
        self._write('desc.ini', [
            '[info]',
            'name[en_US] = Fake Script Pool',
            'name[zh_TW] = 假腳本源',
            'desc[en_US] = a fake pool for programe self testing',
            'desc[zh_TW] = 供自我測試的假腳本源',
            '[category]',
            'Networking[zh_TW] = 網路',
            'Game[zh_TW] = 遊戲'
        ])
        pool = self._load_pool()
        self.assertEquals('Fake Script Pool', pool.get_i18n('info', 'name'))
        self.assertEquals('Fake Script Pool', pool.get_i18n('info', 'name', 'en_US'))
        self.assertEquals('假腳本源', pool.get_i18n('info', 'name', 'zh_TW'))
        self.assertEquals('name', pool.get_i18n('info', 'name', 'nothislan'))
        self.assertEquals('Game', pool.get_i18n('category', 'Game'))
        self.assertEquals('Game', pool.get_i18n('category', 'Game', 'en_US'))
        self.assertEquals('網路', pool.get_i18n('category', 'Networking', 'zh_TW'))
        self.assertEquals('Networking', pool.get_i18n('category', 'Networking', 'nothislan'))

        self.assertRaises(lzspool.NoI18nSectionError,
                         pool.get_i18n,'nothissection', 'Networking', 'nothislan')
    #}}}

    #{{{def test_load_and_get_recommands(self):
    def test_load_and_get_recommands(self):
        self._write('recommands.ini', [
        '[Networking]',
        'flash=',
        '[好工作]',
        '錢多=',
        '事少=',
        '離家近='
        ])
        self._mk_categories(('Networking','Game','noncat'))
        pool = self._load_pool()
        self.assertEquals(['flash'], pool.get_recommands('Networking'))

        # these are both not catgory.
        self.assertEquals([], pool.get_recommands('好工作'))
        self.assertEquals([], pool.get_recommands('UnDefinedCatgory'))
    #}}}

    #{{{def test_init_localpool(self):
    def test_init_localpool(self):
        self.pool = lzspool.ScriptsPool.init_pool(self.poolname,
                            maintainers='Jabba <jabba@jabamo.org>')
        self.assertRaises(lzspool.DirectoryIsAScriptPoolError,
                    lzspool.ScriptsPool.init_pool,self.poolname,
                            maintaners='Jabba <jabba@jabamo.org>')
     #}}}

    #{{{def test_add_and_remove_category(self):
    def test_add_and_remove_category(self):
        pool = lzspool.ScriptsPool.init_pool(self.poolname,
                             maintainers='Jabba <jabba@jabamo.org>')
        pool.add_category('Game')
        pool.add_category('Networking', {'zh_TW':'網路'})
        pool.save()
        self.assertEquals(['Game','Networking'], pool.categories())
        self.assertEquals('網路', pool.get_i18n('category','Networking', 'zh_TW'))
        pool.remove_category('Networking')
        pool.save()
        self.assertEquals(['Game'], pool.categories())
        self.assertRaises(ConfigParser.NoOptionError, pool.parser.get,
                                         'category','Networking[zh_TW]')
        pool.add_category('me')
        self.assertEquals(['Game'], pool.categories())
        pool.remove_category('me')
   #}}}
pass

def suite():
    return unittest.makeSuite(ScriptsPoolTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
