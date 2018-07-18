#!/bin/bash

# this script assumes an alias o link `freecad` in the path
# the freecad should use the Assembly3 workbench

freecad `readlink -f ../Toyota_Yaris_-_freecad_assembly/create_assembly.py` `pwd`/cardboard_car___________________________PID0



echo "deleting all fcstd1 files in: `pwd` ... since I do not want them in version control!"

find -iname "*.fcstd1" | xargs -i rm -vrf {}
find -iname "assembly.fcstd" | xargs -i rm -vrf {}

