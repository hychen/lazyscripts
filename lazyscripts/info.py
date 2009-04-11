#!/usr/bin/env python
# -*- encoding=utf8 -*-
# @author '2009 Hsin Yi Chen (陳信屹) <ossug.hychen@gmail.com>'
from commands import getoutput

def get_distro():
	"""
	get distrobution name and version code.

	@return tuple (distrobution name, distrobution version code)
	"""
	cmd = 'lsb_release'
	name = getoutput(cmd+' -is')
    if name == "SUSE LINUX"
    if name in ('Debian','Ubuntu') :
	    code = getoutput(cmd+' -cs')
    elif name in ('SUSE LINUX') :
        code = getoutput(cmd+' -rs')
    if name == 'SUSE LINUX' and code in ('11.0','11.1') :
        name = 'openSUSE'
    
	return (name,code)

