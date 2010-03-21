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

from lazyscripts import pkgmgr as lzspkgmgr

class PackageManagerTestCase(unittest.TestCase):

    #{{{def setUp(self):
    def setUp(self):
        pass
    #}}}

    #{{{def tearDown(self):
    def tearDown(self):
        pass
    #}}}

    #{{{def test_getpkgmgr():
    def test_getpkgmgr(self):
        "test correct package manager getting function"
        for distro in ('Debian', 'Ubuntu', 'LinuxMint'):
            self.assertEquals(lzspkgmgr.DebManager,
                              lzspkgmgr.get_pkgmgr(distro).__class__)
        for distro in ('suse linux','suse'):
            self.assertEquals(lzspkgmgr.ZypperManager,
                              lzspkgmgr.get_pkgmgr(distro).__class__)
        for distro in ('fedora','centos','redhat'):
            self.assertEquals(lzspkgmgr.YumManager,
                              lzspkgmgr.get_pkgmgr(distro).__class__)
        for distro in ('mandrake','mandriva'):
            self.assertEquals(lzspkgmgr.UrpmiManager,
                              lzspkgmgr.get_pkgmgr(distro).__class__)
        self.assertEquals(lzspkgmgr.PacmanManager,
                              lzspkgmgr.get_pkgmgr('Arch').__class__)
        self.assertEquals(lzspkgmgr.PkgManager,
                              lzspkgmgr.get_pkgmgr('OpenSolaris').__class__)
        self.assertRaises(lzspkgmgr.PackageSystemNotFound,
                                          lzspkgmgr.get_pkgmgr, '')
    #}}}

    #{{{def test_debmgr():
    def test_debmgr(self):
        "test Debian package manager"
        pkgmgr = lzspkgmgr.DebManager()
        self.assertRaises(lzspkgmgr.PackagesCommandNotSupport,
                                pkgmgr.make_cmd, 'll', 'a b c')
        cmd = pkgmgr.make_cmd('install', 'a b c')
        self.assertEquals('apt-get -y --force-yes install a b c', cmd)

        cmd = pkgmgr.make_cmd('remove', 'a b c')
        self.assertEquals('apt-get -y --force-yes --purge remove a b c', cmd)
    #}}}
pass

def suite():
    return unittest.makeSuite(PackageManagerTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
