#!/bin/bash

ABSPATH=$(pwd)

for dir in $(ls)
do
	if [ -d $dir ]; then
	cd $dir
	git add .
	git status
	git commit -a -m "Pushing all tasks"
	git push origin master
	sleep 8
	cd $ABSPATH;
	fi
done
