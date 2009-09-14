import sys
import os
import subprocess as sp

class Deploy:
	def __init__(self, file):
		if os.path.exists(file):
			dep_cmd = "xgrid -job submit "+file+" -in . -out ."
			#dep_cmd = "ls -la"
			proc = sp.Popen(dep_cmd, stdout=sp.PIPE, shell=True);
			print proc.communicate()[0]
		else:
			print "File does not exist"
		pass

if __name__ == "__main__":
	file = sys.argv[1]
	Deploy(file)
