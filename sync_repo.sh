#!/bin/bash
# -*- coding: UTF-8 -*-
# Date: 2009/2/17
# Author: billy3321
# A simple script use to sync your repo with others.
#

function push_repo (){
while true
do
read -p "Pull success. Continue push to your repo?(Y/n)" PUSH_REPO
  case $PUSH_REPO in
   "Y"|"y"|"")
   git push && echo "Push success."
   break
   ;;
   "N"|"n")
   echo "Stop push."
   break
   ;;
   *)
   echo "Please enter a choice."
   ;;
  esac
done
}

function choice_branch(){
read -p "Enter the branch you want to merge or push enter to merge to master:" BRANCH
if [ -z $BRANCH ];then
  BRANCH="master"
fi
}

echo "Whos repo you want to sync?"
echo "1. hychen"
echo "2. yurenju"
echo "3. billy3321"
echo "4. mrmoneyc"
echo "Please enter your choice:"
read -p "What do you want to do now? Please enter the number:" ACT
  case $ACT in
   "1")
   choice_branch
   git pull git://github.com/hychen/lazyscript.git $BRANCH && push_repo
   ;;
   "2")
   choice_branch
   git pull git://github.com/yurenju/lazyscript.git $BRANCH && push_repo
   ;;
   "3")
   choice_branch
   git pull git://github.com/billy3321/lazyscript.git $BRANCH && push_repo
   ;;
   "4")
   choice_branch
   git pull git://github.com/mrmoneyc/lazyscript.git $BRANCH && push_repo
   ;;
   *)
   echo "Please enter a number."
   ;;
   esac


#END
