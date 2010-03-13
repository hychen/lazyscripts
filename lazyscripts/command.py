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
import optparse

from lazyscripts import config
from lazyscripts import env
from lazyscripts import pool
from lazyscripts import script as lzsscript
from lazyscripts import gui
from lazyscripts import git

class Command(object):
    #{{{def __init__(self, args=None):
    def __init__(self, args=None):
        self.args = args.split(' ')
        self.argc = len(self.args)
        self.optparser = optparse.OptionParser()
        self.curdir = os.path.abspath(os.path.curdir)
        self.conf = env.resource('config')
    #}}}

    #{{{def execute(self, curdir=None):
    def execute(self, curdir=None):
        if not self.args:   return False
        method = self.args[0]
        try:
            fn = getattr(self, method)
        except AttributeError:
            print "[LZS command help] ...TBD..."
            return False

        if curdir:
            self.curdir = curdir

        if callable(fn):
            return fn()
        return False
    #}}}

    #{{{def _getopts(self, opt_exprs):
    def _getopts(self, opt_exprs):
        """get parsered options.

        @param list opt_expr [optparse.make_option()]
        @return dict
        """
        self.optparser.add_options(opt_exprs)
        return self.optparser.parse_args(self.args)
    #}}}
pass

class ScriptCmd(Command):

    """
    script create [script name]

        -u/--user   author email.
    """
    #{{{def create(self):
    def create(self):
        if self.argc < 2:
            print "script id is required."
            return False
        id = self.args[1]
        path = os.path.join(self.curdir, id)

        if self.argc == 3:
            scriptname = self.args[2]
        else:
            scriptname = id

        opts = self._getopts([optparse.make_option('-u', '--user', dest='user', default='')])
        print "Creating %s script template" % id
        return lzsscript.Script.init_script(path, scriptname, opts[0].user, True)
    #}}}

    #{{{def info(self):
    def info(self):
        root = env.resource_name('pools')
        if self.argc <=  1:
            script_path = os.path.curdir;
        else:
            if pool.is_scriptspool(os.path.curdir):
                script_path = self.args[1]
            else:
                script_path = os.path.join(root, self.args[1])

        if not lzsscript.is_scriptdir(script_path):
            print "fetal: %s is not a script detectory." % script_path
            return False

        script = lzsscript.Script(script_path)
        # get attritubte.
        attrs = []
        for attr in script.parser.options('attrs'):
           if not getattr(script, attr):    continue
           attrs.append(attr)
        # get package info.
        pkginfo = script.get_pkginfo()
        _pkgs = ['-%s' % e for e in pkginfo['remove']] + \
                  ['+%s' % e for e in pkginfo['install']]
        msg_pkg = ' '.join(_pkgs)
        msg = ["Script Name: %s" % script.name,
               "Package Info: %s" % msg_pkg,
               "Support With: %s" % " ".join(attrs),
               "Script Maintaner: %s" % '\n'.join(script.maintainers),
               "Script Author: %s " % '\n'.join(script.authors),
               "Description: \n%s" % script.desc]

        print "\n".join(msg)
    #}}}

    #{{{def info(self):
    def info(self):
        if self.argc <=  1:
            script_path = os.path.curdir;
        else:
            script_path = self.args[1]

        if not lzsscript.is_scriptdir(script_path):
            print "fetal: %s is not a script detectory." % script_path
            return False

        script = lzsscript.Script(script_path)
        # get attritubte.
        attrs = []
        for attr in script.parser.options('attrs'):
           if not getattr(script, attr):    continue
           attrs.append(attr)
        # get package info.
        pkginfo = script.get_pkginfo()
        _pkgs = ['-%s' % e for e in pkginfo['remove']] + \
                  ['+%s' % e for e in pkginfo['install']]
        msg_pkg = ' '.join(_pkgs)
        msg = ["Script Name: %s" % script.name,
               "Package Info: %s" % msg_pkg,
               "Support With: %s" % " ".join(attrs),
               "Script Maintaner: %s" % '\n'.join(script.maintainers),
               "Script Author: %s " % '\n'.join(script.authors),
               "Description: \n%s" % script.desc]

        print "\n".join(msg)
    #}}}
pass

class PoolCmd(Command):

    """
    pool add [pool name] [remote repo url]
    pool list
    pool info [pool name]
    pool pull [pool name]
    """

    #{{{def add(self):
    def add(self):
        dirname = self.args[1]
        path = os.path.join(env.resource_name('pools'), dirname)
        if not os.path.isdir(path):
            os.mkdir(path)
        msg = "Creating pool %s" % dirname
        if self.argc == 3:
            msg += " remote:%s" % self.args[2]
            pool.GitScriptsPool.init_pool(path, upstream=self.args[2])
            self.conf.set_pool(dirname, upstream=self.args[2])
        else:
            pool.GitScriptsPool.init_pool(path)
            self.conf.set_pool(dirname)
        self.conf.save()
        print msg
    #}}}

    #{{{def list(self):
    def list(self):
        current = ' '
        for pool in self.conf.pools():
            if pool == self.conf.get_default('pool'):
                current = '*'
            data = self.conf.get_pool(pool)
            msg = "%s  %s (%s)" % (current, pool, data['rev'])
            if data['upstream']:
                msg += ' - %s' % data['upstream']
            print msg
    #}}}

    #{{{def info(self):
    def info(self):
        if self.argc <= 1:
            return False
        conf = env.resource('config')
        poolname = self.args[1]
        poolobj = self._load_pool(poolname)
        pooldata = self.conf.get_pool(poolname)
        pooldata = self.conf.get_pool(poolname)
        msgs = [
            "Pool Name: %s" % poolobj.get_i18n('info', 'name'),
            "Upstream Repo: %s" %  pooldata.get('upstream','None'),
            "Remote Repo: %s" %  pooldata.get('origin','None'),
            "Maintainers: %s" %  poolobj.maintainers,
            "Description: %s" % poolobj.get_i18n('info', 'desc'),
        ]
        print '\n'.join(msgs)
    #}}}

    #{{{def sync(self):
    def sync(self):
        (opts, args) = self._getopts([optparse.make_option('-r', '--rev', dest='rev')])
        if len(args) <= 1:
            poolname = self.conf.get_default('pool')
        else:
            poolname = args[1]
        print "Syncing pool %s" % poolname
        poolobj = self._load_pool(poolname)
        try:
            poolobj.gitapi.pull('upstream')
            if opts.rev:
                want_rev = opts.rev
            else:
                want_rev = self.conf.get_pool(poolname)['rev']
            poolobj.gitapi.checkout(want_rev)
        except git.errors.GitCommandError, e:
            print "fetal:sync %s faild." % poolobj.path
            print e
    #}}}

    #{{{def _load_pool(self, poolname):
    def _load_pool(self, poolname):
        path = os.path.join(env.resource_name('pools'), poolname)
        if not os.path.isdir(path):
            data = self.conf.get_pool(poolname)
            os.mkdir(path)
            poolobj = pool.GitScriptsPool.init_pool(path, upstream=data['upstream'])
        else:
            poolobj = pool.GitScriptsPool(path)
        return poolobj
    #}}}
pass

class GuiCmd(Command):

    """
    gui run [recommands.ini]
    """

    #{{{def run(self):
    def run(self):
        if self.argc > 1:
            gui.startgui(self.args[1])
        else:
            gui.startgui()
    #}}}
