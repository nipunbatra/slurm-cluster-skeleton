import os
import time

import delegator
from subprocess import Popen

# Enter your username on the cluster
username = 'nb2cz'

# Location of .out and .err files
SLURM_OUT = "../../slurm_out"

# Create the SLURM out directory if it does not exist
if not os.path.exists(SLURM_OUT):
	os.makedirs(SLURM_OUT)

# Max. num running processes you want. This is to prevent hogging the cluster
MAX_NUM_MY_JOBS = 50
# Delay between jobs when we exceed the max. number of jobs we want on the cluster
DELAY_NUM_JOBS_EXCEEDED = 10

for i in range(1, 10):
	for j in range(1, 10):
		for k in range(1, 10):
			# Location of output files/. This
			OFILE = "%s/%d_%d_%d.out" % (SLURM_OUT, i, j, k)
			# Location of error files. This is where the error occuring are captured.
			EFILE = "%s/%d_%d_%d.err" % (SLURM_OUT, i, j, k)
			SLURM_SCRIPT = "%d_%d_%d.pbs" % (i, j, k)
			# Calling out "called" script
			CMD = 'python called.py %d_%d_%d.pbs' % (i, j, k)
			# Creating the SBTACH script telling time and memory requirements, and location of error and output files
			lines = list()
			lines.append("#!/bin/sh\n")
			lines.append('#SBATCH --time=0-32:0:00\n')
			lines.append('#SBATCH --mem=16\n')
			lines.append('#SBATCH -o ' + '"' + OFILE + '"\n')
			lines.append('#SBATCH -e ' + '"' + EFILE + '"\n')
			lines.append(CMD + '\n')

			with open(SLURM_SCRIPT, 'w') as f:
				f.writelines(lines)
			command = ['sbatch', SLURM_SCRIPT]

			# Check our running processes to be less than max., else sleep
			while len(delegator.run('squeue -u %s' % username).out.split("\n")) > MAX_NUM_MY_JOBS + 2:
				time.sleep(DELAY_NUM_JOBS_EXCEEDED)

			Popen(command)
			print SLURM_SCRIPT
