#!/bin/bash
# -*- coding: utf-8 -*-
# This is a simple bash shell script use to install the packages 
# which need by lazyscripts. This script is use for debian and ubuntu
# with all architecture.
# Please run as root.

function install_require_packages () {
    show_text="正在下載並安裝Lazyscripts執行所需的套件...."
    google_code_url="http://lazyscripts.googlecode.com"
    git_python_filename="python-git_0.1.6-1_all.deb"

    if [ "$1"!="gui" ]; then
        echo "$show_text"
    fi

    # Debian will lost all PATH after sudo, source /etc/profile can get default PATH
    source /etc/profile

    #use zenity if use gui flag
    if [ "$1"="gui" ]; then
        zenity --info --text="lazyscripts 懶人包執行需要下載相關軟體，按下確定後請稍待數分鐘"
        /usr/sbin/synaptic --hide-main-window \
        --non-interactive --update-at-startup

        echo -e "git-core\tinstall\n" > /tmp/package_list.txt
        /usr/sbin/synaptic --hide-main-window \
        --non-interactive -o Synaptic::closeZvt=true \
        --set-selections-file "/tmp/package_list.txt"

        (echo 10;
        wget -c "$google_code_url/files/$git_python_filename" > /dev/null 2>&1;
        dpkg -i "$git_python_filename" > /dev/null 2>&1;
        rm "$git_python_filename" > /dev/null 2>&1;
        echo 100;
        ) | zenity --progress --pulstate --auto-close --auto-kill --text="$show_text"
    else #if slzs console, use console mode
        apt-get update
        apt-get -y --force-yes install \
            git-core > /dev/null
        wget -c "$google_code_url/files/$git_python_filename"
        dpkg -i "$git_python_filename"
        rm "$git_python_filename"
    fi
    echo "執行完畢！即將啟動Lazyscripts..."
}

echo "Check for required packsges..."
if dpkg -l python-nose python-setuptools git-core python-git > /dev/null 2>&1 ; then
    echo "Require packages installed."
else
    echo "Require packages not installed."
    install_require_packages
fi

#END
