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
"""useful functions.
"""

import os

#{{{def create_executablefile(path, lines)
def create_executablefile(path, lines):
    """create a excuteable file.

    @param str filename file name
    @param list lines file content
    """
    with open(path, 'w') as f:
        f.write("\n".join(lines+['']))
        os.chmod(path, 0755)
#}}}

#{{{def ext_ospath_join(*paths):
def ext_ospath_join(*paths):
    root = ''
    for e in paths:
        root = os.path.join(root,e)
    return root
#}}}
