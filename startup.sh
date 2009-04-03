#!/bin/bash




mkdir -p tmp
ENV_EXPORT_SCRIPT="tmp/env-export.sh"
if [ -f ${ENV_EXPORT_SCRIPT} ];then
      rm $ENV_EXPORT_SCRIPT
fi

touch "$ENV_EXPORT_SCRIPT"
chmod a+x "$ENV_EXPORT_SCRIPT"
echo "#!/bin/bash" > "$ENV_EXPORT_SCRIPT"
            
            
DIR=`dirname $0`
cd "$DIR"


export DISTRIB_CODENAME=`lsb_release -cs`
echo "export DISTRIB_CODENAME=`lsb_release -cs`" >> "$ENV_EXPORT_SCRIPT"

export DISTRIB_VERSION=`lsb_release -rs`
echo "export DISTRIB_VERSION=`lsb_release -rs`" >> "$ENV_EXPORT_SCRIPT"

export DISTRIB_ID=`lsb_release -is`
echo "export DISTRIB_ID=`lsb_release -is`" >> "$ENV_EXPORT_SCRIPT"

case "$DISTRIB_ID" in
    "Ubuntu")
    export PLAT_NAME="`uname -a | cut -d " " -f 12`"
    echo "export PLAT_NAME=\"`uname -a | cut -d " " -f 12`\"" >> $ENV_EXPORT_SCRIPT
    echo "Check for required packsges..."
    if dpkg -l python-nose python-git ; then
        echo "Require packages installed."
    else
        echo "Require packages not installed."
        cat distrib/package_debian_ubuntu.sh >> $ENV_EXPORT_SCRIPT
    fi
    ;;
    "Debian")
    export PLAT_NAME="`uname -a | cut -d " " -f 12`"
    echo "export PLAT_NAME=\"`uname -a | cut -d " " -f 12`\"" >> $ENV_EXPORT_SCRIPT
    echo "Check for required packsges..."
    if dpkg -l python-nose python-git ; then
        echo "Require packages installed."
    else
        echo "Require packages not installed."
        cat distrib/package_debian_ubuntu.sh >> $ENV_EXPORT_SCRIPT
    fi
    ;;
    "SUSE LINUX")
    export PLAT_NAME="`uname -i`"
    echo "export PLAT_NAME=\"`uname -i`\"" 
    cat distrib/package_opensuse.sh >> $ENV_EXPORT_SCRIPT
    ;;
    *)
    echo "Sorry, Lazyscripts does not supoort $DISTRIB_ID"
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
echo './lzs list build git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git' >> $ENV_EXPORT_SCRIPT
echo './lzs $@'  >> $ENV_EXPORT_SCRIPT
