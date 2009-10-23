#!/usr/bin/env/ python

"""
Author: David Wischhusen
Date Created: October 23, 2009

Purpose of this script is to create a custom deploy solution for a professsor in the dept.

Use at your own risk

If you modify/redistribute the script, please keep my name at the top
"""

import sys
import os
import shutil
import subprocess as sp
import re
from optparse import OptionParser

class CustomDeploy:
	HOSTNAME = None
	PASSWORD = None

	def __init__(self):
		pass

if __name__ == "__main__":
	if len(sys.argv) == 1:
		sys.argv.append('-h')

	parser = OptionParser()

	parser.add_option('-f', '--file',
			dest="paramfile",
			help="File containing the initial parameters",
			metavar="PARAMFILE"
			)
	parser.add_option('-s', '--servername',
			dest="hostname",
			help="Hostname of the Xgrid Manager",
			metavar="HOSTNAME"
			)
	parser.add_option('-p', '--password',
			dest="password",
			help="Password to access the xgrid",
			metavar="PASSWORD"
			)
	parser.add_option('-r', '--retrieve',
			dest="jobfile",
			help="File containing submitted job ids",
			metavar="JOBFILE"
			)

	options, args = parser.parse_args()

	cd = CustomDeploy()
