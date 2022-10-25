#!/bin/sh
set -e

# wget https://binarycontrol.debian.net/cache/unstable.tar.xz

find unstable/ -name clilibs -delete
find unstable/ -name control -delete
find unstable/ -name shlibs -delete
find unstable/ -name starlibs -delete
find unstable/ -name symbols -delete
find unstable/ -name templates -delete
find unstable/ -name triggers -delete
find unstable/ -type d -empty -delete
du unstable/ --max-depth 0 -h

find unstable/ -type f -printf "%f\n" | sort | uniq -c
