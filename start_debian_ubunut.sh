#!/bin/bash
# -*- coding: utf-8 -*-
# Copyright (C) 2008 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>
# Last Midified : 5 Mar 2008
# This is a simple bash shell script use to install the packages 
# which need by lazyscripts. This script is use for debian and ubuntu
# with all architecture.
# Please run as root.


TOPDIR=`pwd`
TMPDIR="/tmp"

cd $TMPDIR

echo "正在下載並安裝lazyscripts執行所需的套件...."

if [ -f python-git_0.1.6-1_all.deb ];then
 rm -f python-git_0.1.6-1_all.deb
fi


wget http://lazyscripts.googlecode.com/files/python-git_0.1.6-1_all.deb

apt-get install git git-core python-setuptools python-nose

dpkg -i python-git_0.1.6-1_all.deb

cd $TOPDIR

echo "執行完畢！即將啟動lazyscripts..."




#END
