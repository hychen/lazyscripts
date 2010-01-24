#!/usr/bin/env python
# -*- encoding=utf8 -*-
# @author '2009 Hsin Yi Chen (陳信屹) <ossug.hychen@gmail.com>'
import os

def getoutput (cmd):
    pipe = os.popen('{ ' + cmd + '; } 2>&1', 'r')
    text = pipe.read()
    sts = pipe.close()
    if sts is None: sts = 0
    if text[-1:] == '\n': text = text[:-1]
    return text

def get_distro():
    """
    get distrobution name and version code.

    @return tuple (distrobution name, distrobution version code)
    """
    cmd = 'lsb_release'
    name = getoutput(cmd+' -is')
    if name in ('Debian','Ubuntu') :
        code = getoutput(cmd+' -cs')
    elif name in ('SUSE LINUX') :
        code = getoutput(cmd+' -rs')
    if name == 'SUSE LINUX' and code in ('11.0','11.1') :
        name = 'openSUSE'
    
    return (name,code)
