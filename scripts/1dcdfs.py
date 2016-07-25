# 1d anal

import glob
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Freezing param analysis: histogram and cdf for specified parameter combos at 67,90,95 or 99%/ confidence')
parser.add_argument('param1', type=str, help='first parameter of interest')
# parser.add_argument('confidence', type=int, nargs='?', default=90, help='confidence region(67,90,95,99)')
arg = parser.parse_args()
param1 = str(arg.param1)
# confidence = arg.confidence


def paths_to_files(combo):
	# all you need is combo bc that determines path
	paths = glob.glob('/projects/b1011/spinning_runs/freezingparams_20160402/*/{0}/post/confidence_levels.txt'.format(combo))
	return paths


def split_up_lines(textfile):
	with open(textfile,'r') as conf:
		splitted = []
		conf = conf.readlines()
		for element in conf:
			splitted.append(element.split())
		return splitted

def extracting_data(textfile,param1,combo):
	for item in split_up_lines(textfile):
		if item[0] == param1:
			conf90 = float(item[2])
			return conf90


def collect_all_conflevels(param1,combo):
	paths = paths_to_files(combo)
	datapoints = []
	for path in paths:
		datapoint = extracting_data(path,param1,combo)
		datapoints.append(datapoint)
	datapoints = np.sort(datapoints)
	return datapoints



#plotting the cdfs
data_none = collect_all_conflevels(param1,'none')
data_skyloc = collect_all_conflevels(param1,'skyloc')
data_skyloc_dist = collect_all_conflevels(param1,'skyloc_thetajn')
data_skyloc_thetajn = collect_all_conflevels(param1,'skyloc_thetajn')
data_skyloc_thetajn_dist = collect_all_conflevels(param1,'skyloc_thetajn_dist')
y_axis = np.linspace(0,len(data_none)/float(len(data_none)),num=len(data_none))

plt.plot(data_none,y_axis,label='none')
plt.plot(data_skyloc,y_axis,label='skyloc')
plt.plot(data_skyloc_dist,y_axis,label='skyloc_dist')
plt.plot(data_skyloc_thetajn,y_axis,label='skyloc_thetajn')
plt.plot(data_skyloc_thetajn_dist,y_axis,label='skyloc_thetajn_dist')
plt.xlabel('{0}'.format(param1))
plt.ylabel('Cumulative Probability')
plt.legend(loc=4)
plt.savefig('{0}_1Dcdf'.format(param1))






