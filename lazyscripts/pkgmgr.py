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
"""Handles Linux Package Installation/Remove

get_pkgmgr - get package manager by distrobution name.

    >>> pkgmgr = get_pkgmgr("Ubuntu")
    >>> pkgmgr.make_cmd('install', 'foo')
    "apt-get install foo"
"""

import os
import shutil

class APTSourceListIsEmptyFile(Exception):    pass
class PackageSystemNotFound(Exception):    pass

class DebManager(object):
    """Deb Package System Manager
    """
    #{{{attrs
    CMDPREFIX_UPDATE = 'apt-get update'
    CMDPREFIX_INSTALL = 'apt-get -y --force-yes install'
    CMDPREFIX_REMOVE = 'apt-get -y --force-yes --purge remove'
    #}}}

    #{{{def make_cmd(self, act, argv=None):
    def make_cmd(self, act, argv=None):
        """make a command of package by action.

        @param str act action name, ex. install, remove
        @param str pkgs packages name.
        @return str package system command.
        """
        attr = "CMDPREFIX_%s" % act.upper()
        if not hasattr(self, attr):    return None
        cmdprefix = getattr(self, attr)
        if not cmdprefix:    return None
        if not argv:    return cmdprefix
        return "%s %s" % (cmdprefix, argv)
    #}}}

    #{{{def update_sources_by(self, pool):
    def update_sources_by(self, pool):
        from distutils.dep_util import newer
        src = pool.current_pkgsourcelist
        if not src: return False
        dest = "/etc/apt/sources.list.d/%s" % os.path.basename(src)
        if not os.path.exists(src) or newer(src, dest):
            shutil.copy(src, dest)
    #}}}
pass

#{{{def get_pkgmgr(distro):
def get_pkgmgr(distro):
    """get package system manager.

    @param str distro distrobution name.
    @return PackageManager
    """
    if distro in ('Debian','Ubuntu'):
        return DebManager()
    raise PackageSystemNotFound()
#}}}
