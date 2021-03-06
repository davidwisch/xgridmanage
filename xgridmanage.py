#!/usr/bin/env python

"""
Author: David Wischhusen
Date Created: September 12, 2009

Purpose of this script is to provide a more friendly interface to OSX xgrid.
"""

import sys
import os
import shutil
import subprocess as sp
import re
from optparse import OptionParser

class Xgrid:
	HOSTNAME = None
	PASSWORD = None

	def __init__(self):
		try:
			HOME = os.environ.get('HOME')
			config_file = open(HOME+"/.xgridmanagerc")
		except:
			print "Unable to Locate Config file...exiting"
			exit()
		config_content = config_file.read()
		host_regex = "^HOSTNAME[ ]+(?P<hostname>\S+)[ ]*$"
		password_regex = "^PASSWORD[ ]+(?P<password>\S+)[ ]*$"
		host_regex = re.compile(host_regex, re.MULTILINE)
		password_regex = re.compile(password_regex, re.MULTILINE)
		try:
			self.HOSTNAME = host_regex.search(config_content).group('hostname')
			self.PASSWORD = password_regex.search(config_content).group('password')
		except:
			print "Unable to locate hostname/password information....exiting"
			exit()

	def deploy(self, file, num_comps):
		if os.path.exists(file):
			if not os.path.exists("SUBMIT"):
				os.mkdir("SUBMIT")
			shutil.copy(file, "SUBMIT/"+file)
			dep_cmd = "-job submit "+file+" -in ./SUBMIT"
			log = open("submit_ids", "w")
			for i in range(num_comps):
				output = self.exec_cmd(dep_cmd)
				regex = "jobIdentifier\ =\ (?P<jobid>\d+);"
				regex = re.compile(regex)
				match = regex.search(output)
				job_id = match.group('jobid')
				print "Job "+str(i+1)+" Submitted - XGrid Job ID: "+str(job_id)
				log.write(str(job_id)+"\n")
			print "All Jobs Submitted"
			shutil.rmtree("SUBMIT")
			log.close()
		else:
			print "File does not exist"

	def list(self):
		print self.exec_cmd('-job list')

	def detail(self, job_id):
		print self.exec_cmd("-job attributes -id "+str(job_id))

	def project_detail(self, job_file):
		if not os.path.exists(job_file):
			print "File Does Not Exist"
			exit()
		f = open(job_file)
		lines = f.readlines()
		for line in lines:
			job_id = line.strip()
			stats = self.exec_cmd("-job attributes -id "+str(job_id))
			regex = "jobStatus\ =\ (?P<status>\w+);"
			regex = re.compile(regex)
			results = regex.search(stats)
			print "Job ID: "+str(job_id)+"\t----"+results.group('status')
			#print stats
		f.close()

	def kill_id(self, job_id):
		self.exec_cmd("-job delete -id "+str(job_id))
		print "Job "+str(job_id)+" Deleted"

	def kill_job(self, job_file):
		if not os.path.exists(job_file):
			print "File Does Not Exist"
			exit()
		f = open(job_file)
		lines = f.readlines()
		for line in lines:
			job_id = line.strip()
			self.kill_id(job_id)
		f.close()
		print "All ID's in file: "+job_file+" are deleted"

	def result_id(self, job_id):
		stats = self.exec_cmd("-job attributes -id "+str(job_id))
		if stats.find('Finished') == -1:
			print "Job Not Complete - Job ID: "+str(job_id)
			return
		if not os.path.exists("RESULTS"):
			os.mkdir("RESULTS")
		std_out = open("RESULTS/id_"+str(job_id)+"_stdout", 'w')
		prog_std_out = self.exec_cmd('-job results -id '+str(job_id))
		print prog_std_out
		std_out.write(prog_std_out)
		std_out.close()
		self.exec_cmd('-job results -id '+str(job_id)+" -out RESULTS/id_"+str(job_id)+'/')

	def result_job(self, job_file):
		if not os.path.exists(job_file):
			print "File Does Not Exist"
			exit()
		f = open(job_file)
		lines = f.readlines()
		for line in lines:
			job_id = line.strip()
			self.result_id(job_id)
		f.close()
		print "Finished Fetching Results"
	
	def exec_cmd(self, cmd):
		cmd = "xgrid -h "+self.HOSTNAME+" -p "+self.PASSWORD+" "+cmd
		proc = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
		return proc.communicate()[0]

if __name__ == "__main__":
	if(len(sys.argv) == 1):
		print "No Options Specified\n"
		sys.argv.append('-h')
	parser = OptionParser()
	parser.add_option("-d", "--deploy",
			dest="deploy",
			help="Deploy a file to xgrid, use with -n",
			metavar="FILE"
			)
	parser.add_option("-l", "--list",
			dest="list",
			action="store_true",
			help="List ALL jobs in the xgrid queue"
			)
	parser.add_option("-n", "--num",
			dest="num",
			help="Number of of computers to deploy to",
			type="int",
			default=1
			)
	parser.add_option("-k", "--kill",
			dest="kill",
			help="Kill a  particular job on the xgrid",
			type="int",
			metavar="JOB_ID"
			)
	parser.add_option('-f', '--killfile',
			dest="killfile",
			help="Kill all ids in file, deliniated by \"\\n\"",
			metavar="FILE"
			)
	parser.add_option('-i', '--info',
			dest="info",
			type="int",
			help="Get job progress on job id",
			metavar="JOB_ID"
			)
	parser.add_option('-r', '--result',
			dest="result",
			type="int",
			help="Retrieve results for a job id",
			metavar="JOB_ID"
			)
	parser.add_option('-b', '--backfile',
			dest="backfile",
			help="Get results for all ids in file, deliniated by \"\\n\"",
			metavar="FILE"
			)
	parser.add_option('-s', '--status',
			dest="statusfile",
			help="Get status for all ids in file, delinieated by \"\\n\"",
			metavar="FILE"
			)
	(options, args) = parser.parse_args()

	xgrid = Xgrid()
	if options.info:
		xgrid.detail(options.info)
	if options.deploy:
		print "Deploying on "+str(options.num)+" machines"
		xgrid.deploy(options.deploy, options.num)
	if options.killfile:
		xgrid.kill_job(options.killfile)
	if options.list:
		xgrid.list()
	if options.backfile:
		xgrid.result_job(options.backfile)
	if options.kill:
		xgrid.kill_id(options.kill)
	if options.result:
		xgrid.result_id(options.result)
	if options.statusfile:
		xgrid.project_detail(options.statusfile)
