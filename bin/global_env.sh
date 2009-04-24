#!/bin/bash

export DISTRO_ID=`lsb_release -is`
export DISTRO_CODENAME=`lsb_release -cs`
export DISTRO_VERSION=`lsb_release -rs`
case $(getconf LONG_BIT) in
    "32")
    export PLAT_NAME="i386"
    ;;
    "64")
    export PLAT_NAME="x86_64"
    ;;
esac
export WGET="wget --tries=2 --timeout=120 -c"

