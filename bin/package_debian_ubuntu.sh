#!/bin/bash
# -*- coding: utf-8 -*-
# Copyright (C) 2008 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>
# Last Midified : 1 Apr 2009
# This is a simple bash shell script use to install the packages 
# which need by lazyscripts. This script is use for debian and ubuntu
# with all architecture.
# Please run as root.


function install_require_packages () {
    TOPDIR=`pwd`
    TMPDIR="/tmp"
    cd $TMPDIR

    echo "正在下載並安裝Lazyscripts執行所需的套件...."
    source /etc/profile

    apt-get update
    apt-get -y --force-yes install git-core python-setuptools python-nose make
    easy_install GitPython

    cd $TOPDIR

    echo "執行完畢！即將啟動Lazyscripts..."
}

echo "Check for required packsges..."
if dpkg -l python-nose python-setuptools git-core ; then
    echo "Require packages installed."
else
    #FIXME: please don't add any command to env-export.sh
    echo "Require packages not installed."
    install_require_packages
fi

#END
