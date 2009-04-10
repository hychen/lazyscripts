#!/bin/bash
#
# YUMBACK_PID=`pgrep -fl PackageKit | cut -d " " -f 1`
# if [ -z $YUMBACK_PID ]; then
#     echo "Kill yumBackend to unlock yum"
#     kill $YUMBACK_PID
# fi

echo "正在下載與安裝Lazyscripts執行行所需的套件....."

yum install git-core python-nose python-setuptools

easy_install GitPython

echo "執行完畢！即將啟動Lazyscripts..."


