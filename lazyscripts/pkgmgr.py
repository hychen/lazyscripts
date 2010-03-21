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
class PackagesCommandNotSupport(Exception): pass

class AbstractPkgManager(object):
    #{{{def make_cmd(self, act, argv=None):
    def make_cmd(self, act, argv=None):
        """make a command of package by action.

        @param str act action name, ex. install, remove
        @param str pkgs packages name.
        @return str package system command.
        """
        attr = "CMDPREFIX_%s" % act.upper()
        if not hasattr(self, attr):
            raise PackagesCommandNotSupport()
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
        dest = "%s/%s" % (self.SOURCELISTS_DIR, os.path.basename(src))
        if not os.path.exists(src) or newer(src, dest):
            shutil.copy(src, dest)
    #}}}
pass

class DebManager(AbstractPkgManager):
    """Deb Package System Manager(Debian, Ubuntu, LinuxMint)
    """
    #{{{attrs
    CMDPREFIX_DETECT = 'dpkg -l'
    CMDPREFIX_UPDATE = 'apt-get update'
    CMDPREFIX_INSTALL = 'apt-get -y --force-yes install'
    CMDPREFIX_REMOVE = 'apt-get -y --force-yes --purge remove'
    SOURCELISTS_DIR = '/etc/apt/source.list.d'
    #}}}
pass

class ZypperManager(AbstractPkgManager):
    """Zypper Package System Manager(openSUSE)
    """
    #{{{attrs
    CMDPREFIX_DETECT = 'rpm -q'
    CMDPREFIX_UPDATE = 'zypper refresh'
    CMDPREFIX_INSTALL = 'zypper -n install'
    CMDPREFIX_REMOVE = 'zypper -n refresh'
    SOURCELISTS_DIR = '/ect/zypp/repos.d'
    #}}}
pass

class YumManager(AbstractPkgManager):
    """Yum Package System Manager(Fedora, CentOS)
    """
    #{{{attrs
    CMDPREFIX_DETECT = 'rpm -q'
    CMDPREFIX_UPDATE = 'yum check-update'
    CMDPREFIX_INSTALL = 'yum -y install'
    CMDPREFIX_REMOVE = 'yum -y remove'
    SOURCELISTS_DIR = '/etc/yum.repo.d'
    #}}}
pass

class UrpmiManager(AbstractPkgManager):
    """Urpmi Package System Manager(Mandriva)
    """
    #{{{attrs
    CMDPREFIX_DETECT = 'rpm -q'
    CMDPREFIX_UPDATE = 'urpmi.update --update'
    CMDPREFIX_INSTALL = 'urpmi --auto'
    CMDPREFIX_REMOVE = 'urpme --auto'
    SOURCELISTS_DIR = '/etc/urpmi'
    #}}}
pass

class PkgManager(AbstractPkgManager):
    """Image Packaging System Manager(OpenSolaris)
    """
    #{{{attrs
    CMDPREFIX_DETECT = 'pkg search -l'
    CMDPREFIX_UPDATE = 'pkg refresh'
    CMDPREFIX_INSTALL = 'pkg install'
    CMDPREFIX_REMOVE = 'pkg uninstall'
    SOURCELISTS_DIR = '/var/pkg/catalog'
    #}}}
pass

class PacmanManager(AbstractPkgManager):
    """Pacman Package System Manager(Arch)
    """
    #{{{attrs
    CMDPREFIX_DETECT = 'pacman --noconfirm -Qs'
    CMDPREFIX_UPDATE = 'pacman --noconfirm -Syy'
    CMDPREFIX_INSTALL = 'pacman --noconfirm -S --needed'
    CMDPREFIX_REMOVE = 'pacman --noconfirm -R'
    SOURCELISTS_DIR = '/etc/pacman.d'
    #}}}
pass

#{{{def get_pkgmgr(distro):
def get_pkgmgr(distro):
    """get package system manager.

    @param str distro distrobution name.
    @return PackageManager
    """
    distro = distro.lower()
    if distro in ('debian','ubuntu','linuxmint'):
        return DebManager()
    elif distro in ('suse linux','suse'):
        return ZypperManager()
    elif distro in ('fedora','centos','redhat'):
        return YumManager()
    elif distro in ('mandrake','mandriva'):
        return UrpmiManager()
    elif distro == 'arch':
        return PacmanManager()
    elif distro == 'opensolaris':
        return PkgManager()
    raise PackageSystemNotFound()
#}}}
