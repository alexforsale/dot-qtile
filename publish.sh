#!/usr/bin/env sh

mkdir -pv ./content
ln -svf ../index.org ./content/index.org
emacs -Q --script build.el
