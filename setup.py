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

from setuptools import setup, find_packages

setup(
    name = 'Lazyscripts',
    version = '0.2dev',
    description = 'The stupid scripts manager',
    long_description = """
Lazyscripts is a script management tools.
""",
    author = 'Hsin Yi Chen 陳信屹 (hychen)',
    author_email = 'ossug.hychen@gmail.com',
    license = 'GPLv2',
    url = 'http://www.lazyscripts.org',
    packages = find_packages(exclude=['tests']),

    test_suite = 'tests.suite',

    zip_safe = False,

    entry_points = """
    [console_scripts]
    lzs = lazyscripts.console:run
    lzs-debinstall = lazyscripts.console:debinstall
    glzs = lazyscripts.console:gui_run
    """
)
