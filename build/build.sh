#!/bin/bash

set -x

CURRENT_PWD="`pwd`"
cd "$CURRENT_PWD"

read -p "Please type version: " VERSION
filename="lazyscripts-$VERSION.tar.gz"

# build tarball
git archive --format=tar master | gzip -9 > "lazyscripts.tar.gz"

# build self-extracting file from tarball
gcc `pkg-config gtk+-2.0 --cflags --libs` -o sfx sfx.c
strip sfx
echo '_DATA_BEGIN_' | cat sfx - lazyscripts.tar.gz > lazyscripts
chmod +x lazyscripts
rm -f *.tar.gz
tar -czf "$filename" lazyscripts

rm sfx lazyscripts


