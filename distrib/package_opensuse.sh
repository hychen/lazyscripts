#!/bin/bash
# -*- coding: utf-8 -*-
# Copyright (C) 2008 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>
# Last Midified : 5 Mar 2008
# This is a simple bash shell script use to install the packages 
# which need by lazyscripts. This script is use for opensuse with
# i586 architecture.
# Please run as root.


export ARCH_NAME="`uname -i`"

echo "正在下載並安裝lazyscripts執行所需的套件...."

zypper install git git-core python-setuptools

case $ARCH_NAME in

i386)

zypper install http://lazyscripts.googlecode.com/files/python-nose-0.10.4-3.1.i586.rpm

zypper install http://lazyscripts.googlecode.com/files/python-git-0.1.6-3.1.i586.rpm
;;

x86_64)

zypper install http://lazyscripts.googlecode.com/files/python-nose-0.10.4-3.1.x86_64.rpm

zypper install http://lazyscripts.googlecode.com/files/python-git-0.1.6-3.1.x86_64.rpm
;;

*)

echo "抱歉，lazyscripts並不支援 ${ARCH_NAME} 作業系統平台。"
;;
esac

echo "執行完畢！即將啟動lazyscripts..."

#END
