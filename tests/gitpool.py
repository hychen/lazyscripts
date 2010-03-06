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
import shutil
import tempfile
import unittest

from lazyscripts import git
from lazyscripts import pool as lzspool

class GitScriptsPoolTestCase(unittest.TestCase):

    #{{{def setUp(self):
    def setUp(self):
        self.poolname = os.path.join(tempfile.gettempdir(), 'fakepool')
        os.mkdir(self.poolname)

        self.upspoolname = os.path.join(tempfile.gettempdir(),
                                                'upstreampool')
        lzspool.init_gitpool_bare(self.upspoolname)
        self.mypoolname = os.path.join(tempfile.gettempdir(), 'mypool')
        lzspool.init_gitpool_bare(self.mypoolname)
    #}}}

    #{{{def tearDown(self):
    def tearDown(self):
        shutil.rmtree(self.poolname)
        shutil.rmtree(self.upspoolname)
        shutil.rmtree(self.mypoolname)
        pass
    #}}}

    #{{{def _write(self, filename, lines):
    def _write(self, filename, lines):
        with open(os.path.join(self.poolname, filename), 'w') as fileobj:
            fileobj.write('\n'.join(lines + ['']))
    #}}}

    #{{{def _load_pool(self):
    def _load_pool(self):
        return lzspool.GitScriptsPool(self.poolname)
    #}}}

    #{{{def test_init_pool(self):
    def test_init_pool(self):
        self.pool = lzspool.GitScriptsPool.init_pool(
                                    self.poolname,
                                    upstream=self.upspoolname)
        result = self.pool.gitapi.remote('show').split()
        self.assertEquals(['upstream'], result)
        result = self.pool.gitapi.branch('-a').split()
        self.assertEquals(['master','*', 'stable', 'remotes/upstream/master',
                            'remotes/upstream/stable'], result)
        result = self.pool.checkout('remotes/upstream/master')
    #}}}

def suite():
    return unittest.makeSuite(GitScriptsPoolTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
