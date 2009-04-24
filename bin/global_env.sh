#!/bin/bash

export DISTRO_ID=`lsb_release -is`
export DISTRO_CODENAME=`lsb_release -cs`
export DISTRO_VERSION=`lsb_release -rs`
export PLAT_NAME="`uname -a | cut -d " " -f 12`"
export WGET="wget --tries=2 --timeout=120 -c"
