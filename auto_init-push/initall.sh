#!/bin/bash

ABSPATH=$(pwd)
STATIC_FILE=".git"

for dir in $(ls)
do
	if [ -d $dir ]; then
	cd $dir
		if test "$STATIC_FILE"; then
			echo "$STATIC_FILE already exists in : $ABSPATH/$dir"
		else
			git init
			git remote add origin git@gitlab.com:<url>$dir.git
		fi
	git remote -v
	cd $ABSPATH;
	fi
done
