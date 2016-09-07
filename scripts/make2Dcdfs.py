import sys
import itertools
import subprocess

bpath = sys.argv[1]

parameters = [x for x in itertools.combinations(['mc', 'q', 'a1', 'a2', 'tilt1', 'tilt2'], 2)]
for pair in parameters:
	subprocess.call(["python", "2dcdfs.py", "--param1", pair[0], "--param2", pair[1], "--basepath", bpath, "--errors", "bounded", "--confidence", "90"])

