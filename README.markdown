# XGridManage - A Python interface to Xgrid

***

## Overview

xgridmanage is a script designed to create a more user friendly
nterface to the OSX xgrid command line utility.  I wrote this project to
help out one of my professors and a research student of his.

**NOTE** Program is in need of upgrading.

This project (at the time of writing is hosted on github)

[http://github.com/davidwisch/xgridmanage](http://github.com/davidwisch/xgridmanage)

## Usage

### Installation

xgridmanage does not need to be installed, however a simple script
is provided that copies it into a directory named '~/path' and
updates either your .bashrc file or .bash_profile file to include
that directory in your PATH.

To run the setup script, cd into the same directory as it and run:

**NOTE** The script is terrible, it's the first bash script I ever wrote.  I need to update it.

`sh ./setup.sh`

### Configuration

You can specify the xgrid server host and password via a configuration file.
These options are specified in a file named *.xgridmanagerc* and should be placed in
your home directory.  The syntax for this file is as follows:

	HOSTNAME localhost
	PASSWORD mysecretpassword

A sample config file is provided with the rest of the files.
The real config filename must be named **.xgridmanagerc**.

### Using

For a list of accepted commands run 'xgridmanage -h'
or 'xgridmanage --help' or just 'xgridmanage' with no options at all!

When you submit a job to the xgrid, a file called *submit_ids* is created.
This file is what stores the job ids for everything that was just
deployed - don't delete it.  This is the file you'll want to pass
back to xgridmanage to retrieve all your results (and to delete those
jobs from xgrid).

	//Submit program.bin to 10 machines
	xgridmanage -n 10 -d program.bin

	//find status of all program.bin jobs
	xgridmanage -s submit_ids

	//retrieve results for program.bin
	xgridmanage -b submit_ids

	//delete all program.bin jobs
	xgridmanage -f submit_ids

### RESULT folder

When you retrieve results from xgrid, they're placed in a folder named *RESULTS*.
This folder contains two types of files, text files that contain the
stdoutput for the jobs you retrieved and directories containing any output
files those jobs may have been created.

The files containing the stdout are of the form "id\_[job\_id]\_stdout".
The folders containing output files are of the form id\_[job\_id].

Where in both of the above examples '[job\_id]' is replaced by the actual job id.
