#!/bin/bash
# -*- coding: utf-8 -*-
# Copyright (C) 2008 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>
# Last Midified : 1 Apr 2009
# This is a simple bash shell script use to install the packages 
# which need by lazyscripts. This script is use for opensuse with
# i586 architecture.
# Please run as root.


export ARCH_NAME="`uname -i`"

echo "正在下載並安裝lazyscripts執行所需的套件...."

zypper ref
zypper install git git-core python-setuptools

case $ARCH_NAME in

i386)

zypper install http://lazyscripts.googlecode.com/files/python-nose-lastest.i586.rpm

# zypper install http://lazyscripts.googlecode.com/files/python-git-lastest.i586.rpm
easy_install GitPython

;;

x86_64)

zypper install http://lazyscripts.googlecode.com/files/python-nose-lastest.x86_64.rpm

# zypper install http://lazyscripts.googlecode.com/files/python-git-lastest.x86_64.rpm
easy_install GitPython

;;

*)

echo "抱歉，Lazyscripts並不支援 ${ARCH_NAME} 作業系統平台。"
;;
esac

echo "執行完畢！即將啟動Lazyscripts..."

#END
