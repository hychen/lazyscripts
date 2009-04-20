#!/bin/bash

set -x

DEB_SCRIPTS_REPO='git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git'
SUSE_SCRIPTS_REPO='git://github.com/mrmoneyc/lazyscripts_pool_opensuse.git'

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
        exit
    fi
}
            
# some workaround
DIR=`dirname $0`
cd "$DIR"

init_export_script
get_distro_info


case "$DISTRIB_ID" in
    "Ubuntu" | "Debian")
        #PLAT_NAME looks like "i686" or or other text
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

    #else
    *)
        echo "Sorry, Lazyscripts not support your Distribution. The program will exit"
        rm $ENV_EXPORT_SCRIPT
        exit
    ;;
esac

# get scripts from github
REPO_URL=`cat conf/repository.conf`
REPO_DIR="./scriptspoll/`./lzs repo sign $REPO_URL`"
git clone "$REPO_URL" "$REPO_DIR"

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

# a blank line
echo >> $ENV_EXPORT_SCRIPT

# FIXME: export-env just using to pass envirnoment variables, please don't use any command in it.
echo './lzs $@'  >> $ENV_EXPORT_SCRIPT
