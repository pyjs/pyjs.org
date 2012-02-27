#!/bin/sh
# you will need to read the top level README, and run boostrap.py
# and buildout in order to make pyjsbuild

options="$*"
if [ -z $options ] ; then options="--strict -d --no-keep-lib-files --no-compile-inplace";fi

# please stop changing this to run solely and exclusively on windows
# please stop changing it to python pyjsbuild.py because that is exclusive
# to windows.
../../bin/pyjsbuild --print-statements $options website
cp -R output/* ../
