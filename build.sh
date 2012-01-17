#!/bin/sh
# you will need to read the top level README, and run boostrap.py
# and buildout in order to make pyjsbuild

options="$*"
if [ -z $options ] ; then options="--strict -d --no-keep-lib-files --no-compile-inplace";fi
python ../../bin/pyjsbuild.py --print-statements $options website
cp -R output/* ../