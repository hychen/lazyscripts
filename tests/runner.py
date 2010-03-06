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
import unittest
import shutil
import tempfile

from lazyscripts import runner as lzsrunner
from lazyscripts import pool as lzspool
from lazyscripts import script as lzsscript
from lazyscripts import env

class RunnerManagerTestCase(unittest.TestCase):

    #{{{def setUp(self):
    def setUp(self):
        self.mywps = os.path.join(tempfile.gettempdir(), '.lazyscripts')
        env.register_workspace(self.mywps)
        self.runner = lzsrunner.ScriptsRunner()
        self.scriptname = os.path.join(tempfile.gettempdir(), 'script4testrunner')
        self.poolname = os.path.join(tempfile.gettempdir(), 'pool4testrunner')
        os.mkdir(self.poolname)
    #}}}

    #{{{def tearDown(self):
    def tearDown(self):
        shutil.rmtree(self.poolname)
        if os.path.exists(self.scriptname):
            shutil.rmtree(self.scriptname)
        shutil.rmtree(os.path.join(tempfile.gettempdir(), 'lzs_root'))
        shutil.rmtree(self.mywps)
    #}}}

    #{{{def _create_scripts(self, script_content):
    def _create_scripts(self, script_content):
        script = lzsscript.Script.init_script(self.scriptname, True, 'a',['b'])
        path = os.path.join(self.scriptname, 'script')
        with open(path, 'w') as f:
            f.write("\n".join(script_content+['']))
        return lzsscript.Script(self.scriptname)
    #}}}

    #{{{def _load_pool(self):
    def _load_pool(self):
        pool = lzspool.ScriptsPool.init_pool(self.poolname)
        return pool
    #}}}

    #{{{def test_selectionlist(self):
    def test_selectionlist(self):
        listpath = os.path.join(tempfile.gettempdir(),'testsel.ini')
        with open(listpath, 'w') as f:
            f.write("\n".join([
            '[pool]',
            'name=test',
            'upstream=git://a',
            'rev=stable',
            '[Game]',
            'wow=',
            ''
            ]))
        list = lzsrunner.SelectionList(listpath)
        self.assertEquals('git://a',list.pool('upstream'))
        self.assertTrue(list.has_script('Game', 'wow'))
        list.pool_name = "deb"
        list.pool_upstream = "upstream"
        list.pool_rev = "upstream"
    #}}}
pass

def suite():
    return unittest.makeSuite(RunnerManagerTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
