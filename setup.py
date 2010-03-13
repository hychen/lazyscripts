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
import glob
import os
import pkg_resources

#@FIXME: very ugly for localization.
PO_DIR = pkg_resources.resource_filename('lazyscripts', '../data/po')
DESKTOP_FILE = pkg_resources.resource_filename('lazyscripts', '../data/lazyscripts.desktop')

#{{{def build_local():
def build_local():
    for file in os.listdir(PO_DIR):
        if not file.endswith('.po'):
            break
        lang = file[:-3]
        mopath = "/usr/share/locale/%s/LC_MESSAGES/lazyscripts.mo" % lang
        os.system("msgfmt -o %s %s" % (mopath, os.path.join(PO_DIR,file)))
#}}}

def install_desktop_file():
    os.system("cp %s /usr/share/applications/" % DESKTOP_FILE)

try:
    from setuptools import *
except ImportError:
    print "please install setuptools first"

setup(
    name = 'Lazyscripts',
    version = '0.2rc3',
    description = 'The stupid scripts manager in Linux.',
    long_description = """
Lazyscripts is just a stupid script distrubtion tool and quick-installer in linux, which aims to provide a easy way to setup your working enviroment for people who need to install a new distrubution such as Debian,Ubuntu, or who want to have much better experiences in linux.

The original idea is from LazyBuntu, made by PCman in Taiwan. we usually need the script to customize to get somthing better, but theses customization may very hard to end users who new to linux, even the experienced end users. so that is why the lazyscript project starts.
""",
    author = 'Hsin Yi Chen 陳信屹 (hychen)',
    author_email = 'ossug.hychen@gmail.com',
    license = 'GPLv2',
    url = 'http://www.lazyscripts.org',
    packages = find_packages(exclude=['tests']),

    test_suite = 'tests.suite',
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['config']
    },
    data_files = [
        ('share/lazyscripts/po',glob.glob('data/po/*.po'))
    ],

    zip_safe = False,

    entry_points = """
    [console_scripts]
    lzs = lazyscripts.console:run
    lzs-debinstall = lazyscripts.console:debinstall
    glzs = lazyscripts.console:gui_run
    lzs-pcvt = lazyscripts.lengacy:run
    """
)

# Extra actions.
build_local()
install_desktop_file()
