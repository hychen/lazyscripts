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
import cmd
import os
import platform
import sys

from lazyscripts import command as lzscmd
from lazyscripts import env

class LzsAdmin(cmd.Cmd):

    #{{{def __init__(self):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.curdir = os.path.abspath(os.path.curdir)
    #}}}

    def do_update(self, lines):
        #@XXX update package source.
        self.do_pool('sync')

    def do_script(self, lines):
        lzscmd.ScriptCmd(lines).execute(self.curdir)

    def do_pool(self, lines):
        lzscmd.PoolCmd(lines).execute(self.curdir)

    def do_gui(self, lines):
        lzscmd.GuiCmd(lines).execute(self.curdir)

#{{{def run(args=None):
def run(args=None):
    if not args:
        args = sys.argv[1:]

    argc = len(args)
    if argc < 1:
        print "USAGE:\n\t...TBD..."
        sys.exit()

    env.register_workspace()
    env.prepare_runtimeenv()

    admin = LzsAdmin()
    admin.onecmd(' '.join(args))
#}}}

#{{{def gui_run():
def gui_run():
    if os.getuid() == 0:
        print "please do not run as root."
        sys.exit()

    env.register_workspace()
    env.storageenv()
    distro = platform.dist()
    if not distro:
        print "distrobution no supported."
        sys.exit()

    os.system('lzs pool sync')

    message_sudo="\"執行'Lazyscripts 懶人包' 會修改系統設定，並會安裝新軟體，所以需要系統管理員權限。 請輸入系統管理密碼，才能繼續執行。(在 Lazyscripts 下，預設這就是你登入系統時所用的密碼。)\""

    prefix = 'gksu --message %s' % message_sudo
    cmd = "%s lzs gui run &" % prefix
    os.system(cmd)
#}}}

#{{{def debinstall():
def debinstall():
    import re
    class Package:
        def __init__(self, filename):
            self.filename=filename
            stdo=os.popen('dpkg --info %s' % filename )
            output=stdo.read()
            stdo.close()
            match=re.search('Package:(.*)', output)
            if match:
                self.name=match.group(1).strip()
            else:
                self.name=''

            self.depends=[]

            match=re.search('Depends:(.*)', output)
            if match:
                dep_line=match.group(1).strip()
                deps=dep_line.split( ',' )
                for dep in deps:
                    if dep:
                        self.depends.append( dep.split()[0] )

    def find_package(pkgs, name):
        for pkg in pkgs:
            if pkg.name == name:
                return True
        return False

    def get_all_depends(packages):
        deps=[]
        for pkg in packages:
            for dep in pkg.depends:
                if not dep in deps and not find_package(packages, dep):
                    deps.append(dep)
        return deps


    n=len(sys.argv)
    if n < 2:
        exit(1)

    filenames=sys.argv[1:]
    packages=[]

    for filename in filenames:
        packages.append( Package(filename) )

    all_deps=get_all_depends(packages)
    print '正在嘗試安裝相依套件...'
    os.system( 'apt-get -y --force-yes install %s' % ' '.join( all_deps ) )
    print '開始安裝套件...'
    os.system( "dpkg -i %s" % ' '.join(filenames) )
#}}}
