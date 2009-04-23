#!/bin/bash
# -*- coding: utf-8 -*-
# This is a simple bash shell script use to install the packages 
# which need by lazyscripts. This script is use for debian and ubuntu
# with all architecture.
# Please run as root.


function install_require_packages () {
    show_text="正在下載並安裝Lazyscripts執行所需的套件...."
    if [ "$1"!="gui" ]; then
        echo "$show_text"
    fi

    # Debian will lost all PATH after sudo, source /etc/profile can get default PATH
    source /etc/profile

    #use zenity if use gui flag
    if [ "$1"="gui" ]; then
        (echo 30;
        apt-get update > /dev/null 2>&1;

        echo 60;
        apt-get -y --force-yes install \
            git-core python-setuptools \
            python-nose make > /dev/null 2>&1;

        echo 90;
        easy_install GitPython > /dev/null 2>&1;
        echo 100;
        ) | zenity --auto-close --auto-kill --progress --text="$show_text"
    else #if slzs console, use console mode
        apt-get update
        apt-get -y --force-yes install \
            git-core python-setuptools \
            python-nose make > /dev/null
        easy_install GitPython > /dev/null
    fi
    echo "執行完畢！即將啟動Lazyscripts..."
}

echo "Check for required packsges..."
if dpkg -l python-nose python-setuptools git-core > /dev/null 2>&1 ; then
    echo "Require packages installed."
else
    echo "Require packages not installed."
    install_require_packages
fi

#END
