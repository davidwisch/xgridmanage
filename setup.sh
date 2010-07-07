#!/bin/bash

#Author: David Wischhusen
#Date Created: September 14, 2009

#--------------------------------
#
# Script to 'install' the xgrid manager into PATH
#
# Use this script at your own risk - it's my first BASH script, might be horrible
#
#--------------------------------

path_dir=$HOME/"path"
deploy_script="xgridmanage"

GREEN='\033[0;32m'
RED='\033[0;31m'
END='\033[0m'


echo Checking for $deploy_script...'\c'
if (test -e ./$deploy_script); then
	echo $GREEN Found.$END
else
	echo $RED Not Found... exiting. $END
	exit
fi

echo Checking if $path_dir exists...'\c'
if (test -d $path_dir); then
	echo $GREEN Found. $END
else
	echo Attempting to create $path_dir...'\c'
	mkdir $path_dir >> /dev/null
	if (test -w $path_dir); then
		echo $GREEN Created. $END
	else
		echo $RED Failed.  Check Permissions. $END
		exit
	fi
fi

if (test -e ./$deploy_script); then
	cp ./$deploy_script $path_dir/$deploy_script >> /dev/null
	chmod 755 $path_dir/$deploy_script >> /dev/null
fi

echo Checking for .profile...
if (test -w ~/.profile); then
	echo $GREEN Found .profile $END
	echo PATH=$PATH:$path_dir >> ~/.profile
	echo export PATH >> ~/.profile
	PATH=$PATH:$path_dir >> /dev/null
	export PATH >> /dev/null
	echo $path_dir successfully added to path and exported to .profile.
else
	echo $RED Failed. $END
	echo Insert \"PATH=\$PATH:$path_dir\; export PATH\" somewhere
	exit
fi

echo Compmeted setup, $deploy_script is now in your PATH
