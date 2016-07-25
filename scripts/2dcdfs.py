import numpy as np
import glob
import matplotlib
import matplotlib.axes as ax
matplotlib.use('Agg')
import matplotlib.pyplot as plt   
import pylab
import argparse

parser = argparse.ArgumentParser(description='Freezing param analysis: histogram and cdf for specified parameter combos at 67,90,95 or 99%/ confidence')
parser.add_argument('param1', type=str, help='first parameter of interest')
parser.add_argument('param2', type=str, help='second paramter of interest')
parser.add_argument('--confidence', type=int, default=90, help='confidence region(67,90,95,99)')
arg = parser.parse_args()
param1 = arg.param1
param2 = arg.param2
confidence = arg.confidence


def paths_to_files(combo,param1,param2):
        # for a given combination, find all paths to those files.
	paths = glob.glob('/projects/b1011/spinning_runs/freezingparams_20160402/*/{0}/post/2Dbins/{1}_{2}_greedy_stats.txt'.format(combo,param1,param2))
        return paths


def get_area(textfile,confidence):
        with open(textfile,'r') as ppoutput:
                data = np.genfromtxt(ppoutput)
                if confidence in [67,90,95,99]:
                        if confidence == 67:
                                area = data[0][1]
                        elif confidence == 90:
                                area = data[1][1]
                        elif confidence == 95:
                                area = data[2][1]
                        elif confidence == 99:
                                area = data[3][1]
                        return area
                else:
                        print "can only calculate confidence regions of 67,90,95,99%"


def list_areas(combo,param1,param2,confidence):
	areas = []
	pathareasorter = {}
	for path in paths_to_files(combo,param1,param2):
		area = get_area(path,confidence)
		areas.append(area)
		pathareasorter[path] = area
	areas = np.sort(areas)
	#print pathareasorter
	return areas


data_none = list_areas('none',param1,param2,confidence)
print "length data_none ",len(data_none)
data_skyloc = list_areas('skyloc',param1,param2,confidence)
print "length data_skyloc ",len(data_skyloc)
data_skyloc_dist = list_areas('skyloc_dist',param1,param2,confidence)
print "length data_skyloc_dist ",len(data_skyloc_dist)
data_skyloc_thetajn = list_areas('skyloc_thetajn',param1,param2,confidence)
print "length data_skyloc_thetajn ",len(data_skyloc_thetajn)
data_skyloc_thetajn_dist = list_areas('skyloc_thetajn_dist',param1,param2,confidence)
print "length data_skyloc_thetajn_dist ",len(data_skyloc_thetajn_dist)
y_axis = np.linspace(0,len(data_none)/float(len(data_none)),num=len(data_none))


plt.plot(data_none,y_axis,label='none')
plt.plot(data_skyloc,y_axis,label='skyloc')
plt.plot(data_skyloc_dist,y_axis,label='skyloc_dist')
plt.plot(data_skyloc_thetajn,y_axis,label='skyloc_thetajn')
plt.plot(data_skyloc_thetajn_dist,y_axis,label='skyloc_thetajn_dist')
plt.xlabel('{0},{1}'.format(param1,param2))
plt.ylabel('Cumulative Probability')
plt.legend(loc=4)
plt.savefig('{0}_{1}_cdf'.format(param1,param2))
