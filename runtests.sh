#!/bin/bash

green='\033[0;32m'
red='\033[0;31m'
NC='\033[0m'
for f in tests/*.py
  do
    if [ ! -z $1 ]
      then f=$1
    fi
    rm ${f%.*}".s"
    rm "test"
    if [ ! -z $1 ]
      then 
        python compile.py "$f"
      else
        python compile.py "$f" >/dev/null 2>&1
    fi
    gcc ${f%.*}".s" hashtable.o hashtable_itr.o hashtable_utility.o runtime.o -m32 -lm -o test
    COMPILED=$(./test <${f%.*}.in)
    SCRIPTED=$(python $f <${f%.*}.in)
    #echo $COMPILED
    #echo $SCRIPTED
    if [ "$COMPILED" = "$SCRIPTED" ]
      then
        printf ${green}$f${NC}"\n"
      else
        printf ${red}$f${NC}"\n"
    fi

    if [ ! -z $1 ]
      then break
    fi
done
