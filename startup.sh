#!/bin/bash

DEB_SCRIPTS_REPO='git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git'
SUSE_SCRIPTS_REPO='git://github.com/mrmoneyc/lazyscripts_pool_opensuse.git'

function get_distro_info () {
    export DISTRIB_CODENAME=`lsb_release -cs`
    echo "export DISTRIB_CODENAME=`lsb_release -cs`" >> "$ENV_EXPORT_SCRIPT"

    export DISTRIB_VERSION=`lsb_release -rs`
    echo "export DISTRIB_VERSION=`lsb_release -rs`" >> "$ENV_EXPORT_SCRIPT"

    export DISTRIB_ID=`lsb_release -is`
    echo "export DISTRIB_ID=`lsb_release -is`" >> "$ENV_EXPORT_SCRIPT"
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
            
DIR=`dirname $0`
cd "$DIR"

init_export_script
get_distro_info


case "$DISTRIB_ID" in
    "Ubuntu" | "Debian")
        export PLAT_NAME="`uname -a | cut -d " " -f 12`"
        echo "export PLAT_NAME=\"`uname -a | cut -d " " -f 12`\"" >> $ENV_EXPORT_SCRIPT
	export SCRIPTS_REPO=$DEB_SCRIPTS_REPO
	echo "SCRIPTS_REPO='${SCRIPTS_REPO}'" >> $ENV_EXPORT_SCRIPT
        echo "Check for required packsges..."
        if dpkg -l python-nose python-git ; then
            echo "Require packages installed."
        else
            echo "Require packages not installed."
            echo "distrib/package_debian_ubuntu.sh" >> $ENV_EXPORT_SCRIPT
        fi
    ;;
    "SUSE LINUX")
    export PLAT_NAME="`uname -i`"
    echo "export PLAT_NAME=\"`uname -i`\"" $ENV_EXPORT_SCRIPT
	export SCRIPTS_REPO=$SUSE_SCRIPTS_REPO
	echo "SCRIPTS_REPO='${SCRIPTS_REPO}'" >> $ENV_EXPORT_SCRIPT
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

    ;;
    *)
    #Sample code for other distribution.
        echo "Sorry, Lazyscripts can't distinguish your Linux distribution."
        echo "Please choice your distribution in the list."
        zenity --info --text "Sorry, Lazyscripts can't distinguish your Linux distribution. Please choice your distribution in the list by your self.\n\nNote: If you can't find your Linux distribution in the list, It means Lazyscripts not support your distribution. Please contact develpers. http://code.google.com/p/lazyscripts/"
        DISTRIB_ID=`zenity --list --title="Choice your linux distribution" --radiolist --column "" --column "Linux Distribution" FALSE Fedora`
        case $DISTRIB_ID in
            Fedora)
            DISTRIB_VERSION=`zenity --list --title="Choice your linux distribution version" --radiolist --column "" --column "Linux Distribution Version" FALSE "Fedora 10"`
            WIN_MGR=`zenity --list --title="Choice your window manager" --radiolist --column "" --column "Linux Distribution Version" FALSE "Gnome" FALSE "KDE"`
            ;;
        esac
    ;;
esac

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

echo 'make fetch' >> $ENV_EXPORT_SCRIPT
echo 'rm -rf scripts.list' >> $ENV_EXPORT_SCRIPT
echo './lzs list build $SCRIPTS_REPO' >> $ENV_EXPORT_SCRIPT
echo './lzs $@'  >> $ENV_EXPORT_SCRIPT
