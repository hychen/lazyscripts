#!/bin/bash

function get_distro_info () {
if which lsb_release ; then
    export DISTRIB_ID=`lsb_release -is`
    export DISTRIB_CODENAME=`lsb_release -cs`
    export DISTRIB_VERSION=`lsb_release -rs`
    if [ "$DISTRIB_ID" == "SUSE LINUX" ] ; then
        case "$DISTRIB_VERSION" in
            "11.1"|"11.0")
                export DISTRIB_ID="openSUSE"
            ;;
        esac
    fi
    echo "export DISTRIB_CODENAME=`lsb_release -cs`" >> "$ENV_EXPORT_SCRIPT"
    echo "export DISTRIB_VERSION=`lsb_release -rs`" >> "$ENV_EXPORT_SCRIPT"
    echo "export DISTRIB_ID=`lsb_release -is`" >> "$ENV_EXPORT_SCRIPT"
else
    echo "Sorry, Lazyscripts can't distinguish your Linux distribution."
    echo "Please choice your distribution in the list."
    zenity --info --text "Sorry, Lazyscripts can't distinguish your Linux distribution. Please choice your distribution in the list by your self.\n      \nNote: If you can't find your Linux distribution in the list, It means Lazyscripts not support your distribution. Please contact develpers. http://code.google.com/p/lazyscripts/"
    DISTRIB_ID=`zenity --list --title="Choice your linux distribution" --radiolist --column "" --column "Linux Distribution" FALSE Fedora FALSE others`
    export DISTRIB_ID=${DISTRIB_ID}
    echo "export DISTRIB_ID=${DISTRIB_ID}" >> "$ENV_EXPORT_SCRIPT"
fi
}

function init_export_script () {
    mkdir -p tmp
    ENV_EXPORT_SCRIPT="tmp/env-export.sh"
    if [ -f ${ENV_EXPORT_SCRIPT} ];then
        rm $ENV_EXPORT_SCRIPT
    fi

    touch "$ENV_EXPORT_SCRIPT"
    chmod a+x "$ENV_EXPORT_SCRIPT"
    echo "#!/bin/bash" > "$ENV_EXPORT_SCRIPT"
}

function choice_repo () {
#    if [ "$DISTRIB_ID" == "SUSE LINUX" ] ; then
#        DISTRIB_NAME="openSUSE"
#    else
#        DISTRIB_NAME="$DISTRIB_ID"
#    fi
    DISTRIB_NAME="$DISTRIB_ID"
    AVAILABLE_REPO=($(cat distrib/repository.conf  | grep "${DISTRIB_NAME}" | cut -d " " -f 1 | grep "^[git].*[git]$"))
    SHOW_REPO=$(for uri in ${AVAILABLE_REPO[*]} ; do echo -n "FALSE $uri " ; done)
    USE_REPO=`zenity --list --title="Choice Scripts Repository You Want to Use" --radiolist --column "" --column "Repository URL" ${SHOW_REPO}`
    REPO_URL=($(echo ${USE_REPO/|/ }))
    export REPO_URL
    export REPO_NUM=${#REPO_URL[@]}
    echo "REPO_URL=($(echo ${USE_REPO/|/ }))" >> $ENV_EXPORT_SCRIPT
    echo "export REPO_URL" >> $ENV_EXPORT_SCRIPT
    echo "export REPO_NUM=${#REPO_URL[@]}" >> $ENV_EXPORT_SCRIPT
    for ((num=0;num<${REPO_NUM};num=$num+1)); do 
        echo "REPO_DIR[$num]=\"./scriptspoll/\`./lzs repo sign ${REPO_URL[${num}]}\`\"" >> $ENV_EXPORT_SCRIPT 
        echo "git clone ${REPO_URL[$num]} \${REPO_DIR[$num]}" >> $ENV_EXPORT_SCRIPT
    done
    echo "export REPO_DIR" >> $ENV_EXPORT_SCRIPT
}
            
DIR=`dirname $0`
cd "$DIR"

init_export_script
get_distro_info


case "$DISTRIB_ID" in
    "Ubuntu" | "Debian")
        export PLAT_NAME="`uname -a | cut -d " " -f 12`"
        echo "export PLAT_NAME=\"`uname -a | cut -d " " -f 12`\"" >> $ENV_EXPORT_SCRIPT
        echo "Check for required packsges..."
        if dpkg -l python-nose python-setuptools git-core ; then
            echo "Require packages installed."
        else
            echo "Require packages not installed."
            echo "distrib/package_debian_ubuntu.sh" >> $ENV_EXPORT_SCRIPT
        fi
        
    ;;
    "openSUSE")
    export PLAT_NAME="`uname -i`"
    echo "export PLAT_NAME=\"`uname -i`\"" >> $ENV_EXPORT_SCRIPT
    case $WINDOWMANAGER in
        '/usr/bin/gnome')
        export WIN_MGR='Gnome'
        echo "export WIN_MGR=\"Gnome\"" >> $ENV_EXPORT_SCRIPT
        ;;
        '/usr/bin/startkde')
        export WIN_MGR='KDE'
        echo "export WIN_MGR=\"KDE\"" >> $ENV_EXPORT_SCRIPT
        ;;
        *)
        echo "Lazysciprs can't identified your window manager"
        export WIN_MGR=''
        echo "export WIN_MGR=\"\"" >> $ENV_EXPORT_SCRIPT
        ;;
    esac
    if rpm -q python-nose python-setuptools git-core ; then 
        echo "Require packages installed."
    else
        echo "Require packages not installed."
        echo "distrib/package_opensuse.sh" >> $ENV_EXPORT_SCRIPT
    fi 
    ;;
    
    "Fedora")
    export PLAT_NAME="`uname -i`"
    echo "export PLAT_NAME=\"`uname -i`\"" >> $ENV_EXPORT_SCRIPT

    DISTRIB_VERSION=`zenity --list --title="Choice your linux distribution version" --radiolist --column "" --column "Linux Distribution Version" FALSE "Fedora 10"`
    case $DISTRIB_VERSION in
        "Fedora 10")
        export DISTRIB_VERSION="10"
        ;;
    esac
    echo "export DISTRIB_VERSION=${DISTRIB_VERSION}" >> $ENV_EXPORT_SCRIPT

    WIN_MGR=`zenity --list --title="Choice your window manager" --radiolist --column "" --column "Linux Distribution Version" FALSE "Gnome" FALSE "KDE"`
    export WIN_MGR=${WIN_MGR}
    echo "export WIN_MGR=${WIN_MGR}" >> $ENV_EXPORT_SCRIPT
    case $DISTRIB_VERSION in 
         "Fedora 10")
         DISTRIB_VERSION="10"
         ;;
    esac 
cat >> ${ENV_EXPORT_SCRIPT} << EOF
YUMBACK_PID=`pgrep -fl PackageKit | cut -d " " -f 1`
if [ -z "$YUMBACK_PID" ]; then
    echo "Kill yumBackend to unlock yum"
    kill $YUMBACK_PID
fi  
EOF
    if rpm -q python-nose python-setuptools git-core ; then
        echo "Require packages installed."
    else
        echo "Require packages not installed."
        echo "distrib/package_fedora.sh" >> $ENV_EXPORT_SCRIPT
    fi

    ;;
    *)
    zenity --info --text "Sorry, Lazyscripts not support your Distribution. The program will exit"
    rm $ENV_EXPORT_SCRIPT
    exit
    ;;
esac

choice_repo

# check the path of desktop dir
XDG_USER_DIRS=~/.config/user-dirs.dirs
if [ -f "$XDG_USER_DIRS" ]; then
    . ~/.config/user-dirs.dirs
fi

if [ -z "$XDG_DESKTOP_DIR" ]; then
    export DESKTOP_DIR=$HOME/Desktop

else
    export DESKTOP_DIR=$XDG_DESKTOP_DIR
fi
                                        
# Ensure there is a desktop dir, if this doesn't exist, that's a bug of ubuntu.
if [ ! -e "$DESKTOP_DIR" ]; then
    mkdir -p  "$DESKTOP_DIR"
fi
                                                        
# symlink desktop dir to ~/Desktop for compatibility
if [ "$DESKTOP_DIR" != "$HOME/Desktop"  -a  ! -e "$HOME/Desktop" ]; then
    ln -s "$DESKTOP_DIR" "$HOME/Desktop"
fi
                                                                            
# Preserve the user name
export REAL_USER="$USER"
export REAL_HOME="$HOME"
echo "export REAL_USER=\"$USER\"" >> $ENV_EXPORT_SCRIPT
echo "export REAL_HOME=\"$HOME\"" >> $ENV_EXPORT_SCRIPT
                                                                   
# wget command used to download files
export WGET="wget --tries=2 --timeout=120 -c"
echo "export WGET=\"wget --tries=2 --timeout=120 -c\"" >> $ENV_EXPORT_SCRIPT


echo  >> $ENV_EXPORT_SCRIPT
echo 'rm -rf scripts.list' >> $ENV_EXPORT_SCRIPT
echo "./lzs list build ${REPO_URL}" >> $ENV_EXPORT_SCRIPT
echo './lzs $@'  >> $ENV_EXPORT_SCRIPT
