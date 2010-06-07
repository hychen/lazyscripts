#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# Copyright © 2009 Hsin Yi Chen
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
"""Handles Script Installation/Remove
"""

import commands
import ConfigParser
import os
import shutil
import time

from lazyscripts import env
from lazyscripts import distro

#{{{def find_pkginfo(scripts, distro, version=None):
def find_pkginfo(scripts, distro, version=None):
    """get packages defined in scripts by spefic distro.

    @param list scripts
    @param str distro
    @return tuple (install_pkgs_list, remove_pkgs_list)
    """
    paths = [script.path for script in scripts]
    # check the distrobution has another pkg info.
    distro = distro.lower()
    distro_dir = distro+'_def'
    if version:
        distro_ver_dir = os.path.join(distro, version)
        if os.path.isdir(distro_ver_dir):
            distro_dir = distro_ver_dir

    def cmd(action):
        return "find %s -name %s.txt | \
                grep -e '%s/%s.txt' | \
                xargs cat | \
                grep -v ^#" % \
                           (" ".join(paths),
                            action,
                            distro_dir,
                            action)

    installpkgs = []
    removepkgs = []
    ret =  commands.getoutput(cmd("install"))
    if ret:
      installpkgs =  ret.strip().split('\n')
    ret =  commands.getoutput(cmd("remove"))
    if ret:
      removepkgs = ret.strip().split('\n')

    del(cmd)
    return (installpkgs,removepkgs)
#}}}

class TaskScript(file):

    #{{{attrs
    header = ["#!/bin/bash",
              "export LIB_ROOT=/tmp/lzs_root/shlib",
              "cd /tmp/lzs_root",
              "source %s" % env.DEFAULT_STORAGED_ENV_FILE]

    footer = ['chown -R $REAL_USER:$REAL_HOME &> /dev/null',
              'echo DONE!']
    #}}}

    #{{{def __init__(self, cmd_queue=[]):
    def __init__(self, cmd_queue=[]):
        self.cmds = cmd_queue
        super(TaskScript, self).__init__('/tmp/lzs_root/taskscripts', 'w')
    #}}}

    #{{{def add_cmds(self, cmds):
    def add_cmds(self, cmds):
        self.cmds += cmds
    #}}}

    #{{{def save(self):
    def save(self):
        contents = self.header + self.cmds + self.footer
        self.write('\n'.join(contents+['']))
        os.chmod(self.name, 0755)
    #}}}
pass

class SelectionList(object):

    #{{{def __init__(self, scripts):
    def __init__(self, path, scripts=[]):
        self.parser = ConfigParser.ConfigParser()
        self.path = path
        self.parser.read(path)
        self._scripts = scripts
    #}}}

    #{{{def pool(self, key):
    def pool(self, key):
        return self.parser.get('pool', key)
    #}}}

    #{{{def has_script(self, category, script_name):
    def has_script(self, category, script_name):
        if not self.parser.has_section(category):
            return None
        return script_name in self.parser.options(category)
    #}}}

    #{{{def save(self):
    def save(self):
        self._convert()
        with open(self.path, 'w') as fp:
            self.parser.write(fp)
    #}}}

    #{{{def _convert(self):
    def _convert(self):
        for script in self._scripts:
            if not self.parser.has_section(script.category):
                self.parser.add_section(script.category)
            self.parser.set(script.category, script.id, '')
    #}}}
pass

class ScriptsRunner(object):

    #{{{def __init__(self, ui=None):
    def __init__(self, ui=None):
        # init runtime_root.
        env.prepare_runtimeenv()
        self.ui = ui
        self.cmd_queue = []
        self._scripts = []
        self.distro = distro.Distribution()
        self.pkgmgr = self.distro.pkgmgr
    #}}}

    #{{{def set_scripts(self, scripts):
    def set_scripts(self, scripts):
        self.cmd_queue = []
        self._scripts = scripts
    #}}}

    #{{{def select_pool(self, pool):
    def select_pool(self, pool):
        self.pool = pool

        self.pkgmgr.update_sources(self.pool)

        # copy shlib.
        self._cpone2root(os.path.join(self.pool.path,'shlib'))
    #}}}

    #{{{def _cpone2root(self, src):
    def _cpone2root(self, src):
        dest = os.path.join(env.DEFAULT_RUNTIME_ROOT_DIR, os.path.basename(src))
        if os.path.isdir(src):
            if os.path.exists(dest):
                shutil.rmtree(dest)
            cpfn = shutil.copytree
        else:
            cpfn = shutil.copy
        cpfn(src, dest)
    #}}}

    #{{{def run(self):
    def run(self):
        # prepare pkg command.
        self.prepare_pkgscmds()

        # prepare scripts command.
        self.prepare_scriptcmds()

        # create a taskscript.
        with TaskScript(self.cmd_queue) as t:
            t.save()

        # create a recommand.ini.
        self.save_selection()

        # real execute.
        cmd = "%s" % t.name
        if self.ui:
            self.ui.pid = self.ui.final_page.term.fork_command(cmd)
        else:
            return commands.getoutput(t.name)
    #}}}

    #{{{def save_selection(self):

    def save_selection(self):
        root = env.resource_name('log')
        filename = "%s_selection.ini" % time.time()
        sel = SelectionList(os.path.join(root, filename), self._scripts)
        sel.save()
    #}}}

    #{{{def prepare_cmds(self):
    def prepare_pkgscmds(self):
        "prepare commands."
        (self.install_pkgs, self.remove_pkgs) = \
                    find_pkginfo(self._scripts,self.distro.name)

        self.cmd_queue.append(self.pkgmgr.make_cmd('update'))

        if self.remove_pkgs:
            for pkg in self.remove_pkgs:
              self.cmd_queue.append(self.pkgmgr.make_cmd('remove',pkg))

        if self.install_pkgs:
            for pkg in self.install_pkgs:
              self.cmd_queue.append(self.pkgmgr.make_cmd('install',pkg))
    #}}}

    #{{{def prepare_scriptcmds(self):
    def prepare_scriptcmds(self):
        later = []
        for script in self._scripts:
            scriptfile = os.path.join(script.path, 'script')
            if not os.path.exists(scriptfile):
                continue
            # copy scripts.to running root.
            #@FIXME: the code is ugly.
            src = script.path
            dest = os.path.join(env.DEFAULT_RUNTIME_ROOT_DIR, script.category)
            os.system("mkdir -p %s" % dest)
            dest = os.path.join(dest, os.path.basename(src))
            os.system("cp -a %s %s" % (src, dest))
            if not script.interact:
                self.cmd_queue.append(self._exec_scriptcmd(script))
            else:
                later.append(self._exec_scriptcmd(script))
        self.cmd_queue.extend(later)
    #}}}

    #{{{def _exec_scriptcmd(self, script):
    def _exec_scriptcmd(self, script):
        return "cd %s/%s && ./script && cd -" % \
                (script.category, os.path.basename(script.path))
    #}}}
pass
