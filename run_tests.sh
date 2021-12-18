#!/usr/bin/env bash

TARGET_DIR=$(pwd)/data
rm -rf $TARGET_DIR
mkdir -p $TARGET_DIR
ROZKLADY_FILE=$TARGET_DIR/rozklady.zip
OBRAZY_FILE=$TARGET_DIR/obrazy.zip
curl --insecure https://zim.ire.pw.edu.pl/pages/koda/rozklady.zip > $ROZKLADY_FILE
curl --insecure https://zim.ire.pw.edu.pl/pages/koda/obrazy.zip > $OBRAZY_FILE

unzip -u $ROZKLADY_FILE -d $TARGET_DIR
unzip -u $OBRAZY_FILE -d $TARGET_DIR
rm -f $ROZKLADY_FILE
rm -f $OBRAZY_FILE

python3 tests.py