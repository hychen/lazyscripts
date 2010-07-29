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

    >>> pkgmgr = get_pkgmgr("ubuntu")
    >>> pkgmgr.make_cmd('install', 'foo')
    "apt-get install foo"
"""

import commands
import ConfigParser
import os
import shutil

from distutils.dep_util import newer

class APTSourceListIsEmptyFile(Exception):  pass
class PackageSystemNotFound(Exception): pass
class PackagesCommandNotSupport(Exception): pass
class PackageManagerRequiresKeyManager(Exception):  pass

class AbstractPkgManager(object):
    """DO NOT USED DIRECTLY"""
    #{{{attrs
    "GPG Key Manager"
    keymgr = None

    "Requires GPG Key Manager to Add key for verifying."
    requires_keymgr = False
    #}}}

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
    def update_sources_by_file(self, pool):
        (src, keylist) = pool.current_pkgsourcelist
        if not src: return False
        self.addkeys(keylist)
        dest = "%s/%s" % (self.SOURCELISTS_DIR, os.path.basename(src))
        if not os.path.exists(src) or newer(src, dest):
            shutil.copy(src, dest)
    #}}}

    #{{{def update_sources_by_cmd(self, pool):
    def update_sources_by_cmd(self, pool):
        (src,keylist) = pool.current_pkgsourcelist
        if not src: return False
        self.addkeys(keylist)
        os.system(src)
    #}}}

    #{{{def addkeys(self, keylist):
    def addkeys(self, keylist):
        """Add GPG key of package repo to verify packages.

        @param str keylist a .ini file
        """
        if not self.keymgr and self.requires_keymgr:
            return False

        key_config = ConfigParser.ConfigParser()
        key_config.read(keylist)
        for section in key_config.sections():
            if section == 'Download':
                key_urls = key_config.get('Download', 'urls').split('\n')
                for url in key_urls:
                    if not url: continue
                    self.keymgr.import_keyfile(url)
            elif section[:9] == 'keyserver':
                keysrv_url = key_config.get(section, 'url')
                key_ids = key_config.get(section, 'id').split('\n')
                for key in key_ids:
                    if not key: continue
                    self.keymgr.import_key_from_keyserver(keysrv_url, key)
    #}}}
pass

class DebKeyManager(object):
    """APT Key Manager(Debian, Ubuntu, LinuxMint)
    """
    #{{{def has_key(self, key):
    def has_key(self, key):
        """check is key already imported

        @param str key key string
        @return bool True if the key exists
        """
        if commands.getoutput('apt-key list | grep -w %s' % key):
            return True
    #}}}

    #{{{def import_key_from_keyserver(self, keysrv_url, keyid):
    def import_key_from_keyserver(self, keysrv_url, keyid):
        if not self.has_key(keyid):
            os.system('apt-key adv --keyserver %s --recv-keys %s' % (keysrv_url, keyid))
    #}}}

    #{{{def import_keyfile(self, path):
    def import_keyfile(self, path):
        """Add key from http or file.

        @param str path http url or file path (file is default)
        """
        if path.startswith('http://') or \
           path.startswith('https://') or \
           path.startswith('ftp://'):
            os.system('wget -q %s -O- | apt-key add -' % path)
        else:
            os.system('apt-key add %s' % path)
    #}}}

    #{{{def remove_key(self, keyid):
    def remove_key(self, keyid):
        os.system('apt-key del %s' % keyid)
    #}}}

class DebManager(AbstractPkgManager):
    """Deb Package System Manager(Debian, Ubuntu, LinuxMint)
    """
    #{{{attrs
    CMDPREFIX_DETECT = 'dpkg -l'
    CMDPREFIX_UPDATE = 'apt-get update'
    CMDPREFIX_INSTALL = 'apt-get -y --force-yes install'
    CMDPREFIX_REMOVE = 'apt-get -y --force-yes --purge remove'
    CMDPREFIX_ADDREPO = ''
    SOURCELISTS_DIR = '/etc/apt/sources.list.d'
    SOURCELISTS_CFG = '/etc/apt/sources.list'
    #}}}

    #{{{def __init__(self):
    def __init__(self):
        self.update_sources = self.update_sources_by_file
        self.requires_keymgr = True
        self.keymgr = DebKeyManager()
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
    CMDPREFIX_ADDREPO = 'zypper -n ar'
    SOURCELISTS_DIR = '/ect/zypp/repos.d'
    SOURCELISTS_CFG = '/etc/zypp/zypper.conf'
    #}}}

    #{{{def __init__(self):
    def __init__(self):
        self.update_sources = self.update_sources_by_cmd
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
    CMDPREFIX_ADDREPO = ''
    CMDPREFIX_ADDKEY = 'rpm --import'
    SOURCELISTS_DIR = '/etc/yum.repo.d'
    SOURCELISTS_CFG = '/etc/yum.conf'
    #}}}

    #{{{def __init__(self):
    def __init__(self):
        self.requires_keymgr = True
        self.update_sources = self.update_sources_by_file
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
    CMDPREFIX_ADDREPO = 'urpmi.addmedia '
    SOURCELISTS_DIR = ''
    SOURCELISTS_CFG = '/etc/urpmi/urpmi.cfg'
    #}}}

    #{{{def __init__(self):
    def __init__(self):
        self.update_sources = self.update_sources_by_cmd
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
    CMDPREFIX_ADDREPO = 'pkg set-publisher -O'
    SOURCELISTS_DIR = ''
    SOURCELISTS_CFG = '/var/pkg/cfg_cache'
    #}}}

    #{{{def __init__(self):
    def __init__(self): self.update_sources = self.update_sources_by_cmd
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
    CMDPREFIX_ADDREPO = ''
    SOURCELISTS_DIR = '/etc/pacman.d'
    SOURCELISTS_CFG = '/etc/pacman.conf'
    #}}}

    #{{{def __init__(self):
    def __init__(self): self.update_sources = self.update_sources_by_cmd
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
    elif distro in ('suse linux','suse', 'opensuse'):
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
