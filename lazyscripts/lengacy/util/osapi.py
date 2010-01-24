#!/usr/bin/env python
# -*- encoding=utf8 -*-
# @author '2009 Hsin Yi Chen (陳信屹) <ossug.hychen@gmail.com>'
import os

def create_excuteablefile(path, content=None):
    """
    create a excuteable file.

    @param str content
    @param str path file path
    """
    file = open(path, 'w')
    if content:
        file.write(content)
    os.chmod(path, 0755)
    return file
