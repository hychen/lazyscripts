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
import commands
import unittest
import tempfile
import shutil

from lazyscripts import utils
from lazyscripts import env

class EnvTestCase(unittest.TestCase):

    #{{{def setUp(self):
    def setUp(self):
        pass
    #}}}

    #{{{def tearDown(self):
    def tearDown(self):
        pass
    #}}}

    #{{{def test_storagedenv():
    def test_storagedenv(self):
        tfile = os.path.join(tempfile.gettempdir(), 'lzs_testenv')
        utils.create_executablefile(tfile,
                        ['#!/bin/bash',
                        'source /tmp/lzs_storagedenv',
                        'echo $REAL_USER $REAL_HOME'])

        filename = env.storageenv(tempfile.gettempdir())
        self.assertEquals("%s %s" % (os.getenv('USER'), os.getenv('HOME')),
                                 commands.getoutput(tfile))
    #}}}

    #{{{def test_resource_name(self):
    def test_resource_name(self):
        mywps = os.path.join(tempfile.gettempdir(), '.lazyscripts')
        env.register_workspace(mywps)
        self.assertEquals(mywps, env.resource_name())
        self.assertEquals(
            os.path.join(mywps, 'config'),
            env.resource_name('config'))
        shutil.rmtree(mywps)
    #}}}
pass

def suite():
    return unittest.makeSuite(EnvTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
