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
import pkg_resources
import shutil

from lazyscripts import config
from lazyscripts import utils

class WorkspaceDupplicationError(Exception):
    "raise exception when workspace dupliication."

#{{{def init_workspace(root):
def init_workspace(root):
    if os.path.isdir(root):
        raise WorkspaceDupplicationError()

    os.mkdir(root)
    os.mkdir(os.path.join(root, 'pools'))
    os.mkdir(os.path.join(root, 'log'))
    os.mkdir(os.path.join(root, 'caches'))
    templateconf = pkg_resources.resource_filename(
                            'lazyscripts.template', 'config')
    shutil.copy(templateconf, os.path.join(root, 'config'))
#}}}
