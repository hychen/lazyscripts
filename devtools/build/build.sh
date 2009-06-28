#!/bin/bash

relative_path="`dirname $0`"

cd "$relative_path"
CURRENT_PWD="`pwd`"

read -p "Please type version: " VERSION
filename="lazyscripts-$VERSION.tar.gz"

# build tarball
cd ../..
REPO=$(cat conf/repository.conf)
REPO_SIGN=$(./bin/lzs repo sign $REPO |grep -v Check | grep -v Requ)

git archive --format=tar $VERSION | gzip -9 > "lazyscripts.tar.gz"
mv "lazyscripts.tar.gz" "$CURRENT_PWD"
cd "$CURRENT_PWD"

mkdir -p "temp"
cd "temp"
tar zxf ../lazyscripts.tar.gz
cp -a ../../../scriptspoll/$REPO_SIGN scriptspoll/
tar czf lazyscripts.tar.gz *
cp lazyscripts.tar.gz ..
cd ..
rm -rf temp

# build self-extracting file from tarball
gcc `pkg-config gtk+-2.0 --cflags --libs` -o sfx sfx.c
strip sfx
echo '_DATA_BEGIN_' | cat sfx - lazyscripts.tar.gz > lazyscripts
chmod +x lazyscripts
rm -f *.tar.gz
tar -czf "$filename" lazyscripts

rm sfx lazyscripts
