import sys
import itertools
import subprocess

bpath = reduce(lambda s, arg: s + ["--basepath", arg], sys.argv[1:], [])

parameters = [x for x in itertools.combinations(['mc', 'q', 'a1', 'a2', 'tilt1', 'tilt2'], 2)]
for pair in parameters:
    call_args = ["python", "2dcdfs.py", "--param1", pair[0], "--param1", pair[1], "--errors", "bounded"]
    call_args.extend(bpath)
    print " ".join(call_args)
    subprocess.call(call_args)

