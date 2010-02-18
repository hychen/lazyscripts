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
import tempfile
import shutil

from lazyscripts import console
from lazyscripts import env
from lazyscripts import pool
from lazyscripts import script as lzsscript

class LzsAdminrTestCase(unittest.TestCase):

    #{{{def setUp(self):
    def setUp(self):
        self._admin = console.LzsAdmin()
        self._admin.curdir = tempfile.gettempdir()
        self.mywps = os.path.join(tempfile.gettempdir(), '.lazyscripts')
        env.register_workspace(self.mywps)
        self.upspoolname = os.path.join(tempfile.gettempdir(),
                                                'upstreampool')
        pool.init_gitpool_bare(self.upspoolname)
    #}}}

    #{{{def tearDown(self):
    def tearDown(self):
        shutil.rmtree(self.upspoolname)
        shutil.rmtree(self.mywps)
    #}}}

    def test_default(self):
        self._admin.onecmd("")

    #{{{def test_create_script(self):
    def test_create_script(self):
        self._admin.onecmd("script")
        scriptpath = os.path.join(self._admin.curdir, 'zen')
        self._admin.onecmd("script create zen -u jabbamo@gmail.com")
        script = lzsscript.Script(scriptpath)
        self.assertEquals('zen', script.name)
        shutil.rmtree(scriptpath)
    #}}}

    #{{{def test_add_pool(self):
    def test_add_pool(self):
        self._admin.onecmd("pool")
        path = os.path.join(env.resource_name('pools'), 'zenpool')
        self._admin.onecmd("pool add zenpool")
        mypool = pool.GitScriptsPool(path)
        self.assertEquals(
           {'origin': '', 'rev': 'stable', 'upstream': ''},
            env.resource('config').get_pool('zenpool'))
        shutil.rmtree(path)
        self._admin.onecmd("pool add zenpool /tmp/upstreampool")
        mypool = pool.GitScriptsPool(path)
        self.assertEquals(
           {'origin': '', 'rev': 'stable', 'upstream': '/tmp/upstreampool'},
            env.resource('config').get_pool('zenpool'))
        shutil.rmtree(path)
    #}}}

    def test_show_script(self):
        path = os.path.join(tempfile.gettempdir(), 'fakescript')
        script = lzsscript.Script.init_script(path, 'test', 'test', True)
        self._admin.onecmd("script show %s" % path)
        shutil.rmtree(path)
pass

def suite():
    return unittest.makeSuite(LzsAdminrTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
