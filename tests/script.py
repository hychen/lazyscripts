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

from lazyscripts import script as lzsscript

class ScriptTestCase(unittest.TestCase):

    #{{{def setUp(self):
    def setUp(self):
        self.desc_baselines = [
        "[info]",
        "name[en_US] = Install Inkscape",
        "name[zh_TW] = 安裝 Inkscape 向量繪畫軟體 ",
        "desc[en_US] = Inkscape is a vector graphic tool.",
        "desc[zh_TW] = Inkscape 是一個向量繪圖軟體，支援SVG格式。(SVG 是 W3C 的標準格式) ",
        "warn[en_US] =",
        "warn[zh_TW] =",
        "",
        "license     = GPLv2",
        "maintainers = 王綱民 Kang-Min Wang (Aminzai,阿民) <lagunawang -AT- gmail.com>",
        "authors     = 王綱民 Kang-Min Wang (Aminzai,阿民) <lagunawang -AT- gmail.com>",
        '[attrs]']

        self.scriptname = os.path.join(tempfile.gettempdir(), 'lzs-testscript')
    #}}}

    #{{{def tearDown(self):
    def tearDown(self):
        shutil.rmtree(self.scriptname)
    #}}}

    #{{{def _load(self, lang=None):
    def _load(self, lang=None):
        if not lang:
            return lzsscript.Script(self.scriptname)
        else:
            return lzsscript.Script(self.scriptname, lang)
    #}}}

    #{{{def _write(self, filename, lines):
    def _write(self, filename, lines):
        os.mkdir(self.scriptname)
        with open(os.path.join(self.scriptname,filename),'w') as f:
            f.write("\n".join(lines+[""]))
    #}}}

    #{{{def test_conditioncheck(self):
    def test_conditioncheck(self):
        self._write('desc.ini', self.desc_baselines+
            ['debian=True',
            'amd64=True'])
        script = self._load()
        self.assertTrue(script.debian)
        self.assertTrue(script.amd64)
        self.assertTrue(script.is_avaliable({'debian':True,'amd64':True}))
        self.assertFalse(script.is_avaliable({'noattr':True,'amd64':True}))
    #}}}

    #{{{def test_desc(self):
    def test_desc(self):
        self._write('desc.ini', self.desc_baselines)
        script = self._load()
        self.assertEquals('Install Inkscape', script.name)
        script = self._load('zh_TW')
        self.assertEquals('安裝 Inkscape 向量繪畫軟體', script.name)
        self.assertEquals('GPLv2', script.license)
        self.assertEquals(
            '王綱民 Kang-Min Wang (Aminzai,阿民) <lagunawang -AT- gmail.com>', script.authors[0])
    #}}}

    #{{{def test_init_script(self):
    def test_init_script(self):
        script = lzsscript.Script.init_script(self.scriptname, 'A',['B'], True)
        self.assertEquals('A', script.name)
        self.assertEquals(['B'], script.authors)
        self.assertEquals('long description', script.desc)
        self.assertFalse(script.debian)
        self.assertFalse(script.amd64)
        self.assertRaises(lzsscript.DirectoryIsScriptDirError,
        lzsscript.Script.init_script, self.scriptname, 'A',['B'], False)
    #}}}
pass

def suite():
    return unittest.makeSuite(ScriptTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
