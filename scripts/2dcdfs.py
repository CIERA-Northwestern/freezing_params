from __future__ import division

import numpy as np
import glob
import matplotlib
import matplotlib.axes as ax
matplotlib.use('Agg')
import matplotlib.pyplot as plt   
import pylab
import argparse
import scipy.stats
import math

import common

parser = argparse.ArgumentParser(description='Freezing param analysis: histogram and cdf for specified parameter combos at 67,90,95 or 99%/ confidence')
parser.add_argument('--param1', type=str, help='first parameter of interest')
parser.add_argument('--param2', type=str, help='second paramter of interest')
parser.add_argument("-e", '--errors', type=str, default='bounded', help='Plot these types of error bars')
parser.add_argument("-b", '--basepath', type=str, help="base path to search for results")
parser.add_argument('--confidence', type=int, default=90, help='confidence region(67,90,95,99)')
arg = parser.parse_args()
if arg.errors not in ('none', 'bounded', 'poisson', 'binomial'):
	raise ArgumentError("Invalid error bound selection.")

param1 = arg.param1
param2 = arg.param2
bpath = arg.basepath
confidence = arg.confidence

print param1, param2

def paths_to_files(combo, param1, param2, bpath):
        # for a given combination, find all paths to those files.
	paths = glob.glob('/{3}/*/{0}/post/2Dbins/{1}_{2}_greedy_stats.txt'.format(combo, param1, param2, bpath))
        return paths


def get_area(textfile, confidence):
        with open(textfile, 'r') as ppoutput:
                data = np.genfromtxt(ppoutput)
                if confidence in [67, 90, 95, 99]:
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


def list_areas(combo, param1, param2, confidence, bpath):
	areas = []
	pathareasorter = {}
	for path in paths_to_files(combo, param1, param2, bpath):
		area = get_area(path, confidence)
		areas.append(area)
		pathareasorter[path] = area
	areas = np.sort(areas)
	#print pathareasorter
	return areas


data_none = list_areas('none', param1, param2, confidence, bpath)

# !!!! - I changed the second parameter of all y_axis to be 1 isntead of len(data)/float(len(data))

y_axis = np.linspace(0, 1, num=len(data_none))
print "length data_none ", len(data_none)
plt.step(data_none, y_axis, label='none', color='k')

# Add error bars based on the case where no parameters are constrained
if arg.errors == 'bounded':
	alpha = 0.95
	error_width = math.sqrt(1./2/len(data_none) * math.log(2./alpha))
	error_width = np.ones(len(data_none)) * error_width
	
	# Clip the error bounds to fit the domain of the CDF
	error_width = np.clip(error_width, 0, 1)
	# !!! - compare to Chris's 1D code for edits
	plt.fill_between(data_none, y_axis - error_width, y_axis + error_width, color='k', alpha=0.3, interpolate=False)

elif arg.errors == 'poisson':
	error_width = 1. / np.sqrt(range(1, len(y_axis) + 1))
	plt.fill_between(data_none, y_axis - error_width, y_axis + error_width, color='k', alpha=0.3)

elif arg.errors == 'binomial':
	error_width = np.sqrt((y_axis * (1 - y_axis) / range(1, len(y_axis) + 1)))
	plt.fill_between(data_none, y_axis - error_width, y_axis + error_width, color='k', alpha=0.3)





data_skyloc = list_areas('skyloc', param1, param2, confidence, bpath)
stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc)
y_axis = np.linspace(0, 1, num=len(data_skyloc))
print "length data_skyloc ", len(data_skyloc)
print "KS test between none and skyloc: %1.2e" % ks_val
plt.step(data_skyloc, y_axis, label='skyloc (KS: %1.2e)' % ks_val)

data_skyloc_dist = list_areas('skyloc_dist', param1, param2, confidence, bpath)
stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_dist)
y_axis = np.linspace(0, 1, num=len(data_skyloc_dist))
print "length data_skyloc_dist ", len(data_skyloc_dist)
print "KS test between none and skyloc_dist: %1.2e" % ks_val
plt.step(data_skyloc_dist, y_axis, label='skyloc_dist (KS: %1.2e)' % ks_val)

data_skyloc_thetajn = list_areas('skyloc_thetajn', param1, param2, confidence, bpath)
stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_thetajn)
y_axis = np.linspace(0, 1, num=len(data_skyloc_thetajn))
print "length data_skyloc_thetajn", len(data_skyloc_thetajn)
print "KS test between none and skyloc_thetajn: %1.2e" % ks_val
plt.step(data_skyloc_thetajn, y_axis, label='skyloc_thetajn (KS: %1.2e)' % ks_val)

data_skyloc_thetajn_dist = list_areas('skyloc_thetajn_dist', param1, param2, confidence, bpath)
stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_thetajn_dist)
y_axis = np.linspace(0, 1, num=len(data_skyloc_thetajn_dist))
print "length data_skyloc_thetajn_dist", len(data_skyloc_thetajn_dist)
print "KS test between none and skyloc_thetajn_dist: %1.2e" % ks_val
plt.step(data_skyloc_thetajn_dist, y_axis, label='skyloc_thetajn_dist (KS: %1.2e)' % ks_val)

plt.xlabel('{0},{1}'.format(param1, param2))
plt.ylabel('Cumulative Probability')
print common.range_from_param(param1) * common.range_from_param(param2)
plt.xlim(0, common.range_from_param(param1) * common.range_from_param(param2))
#plt.xlim(0, data_none[-1])
plt.ylim(0, 1)
plt.grid()
plt.legend(loc=4)

# Add normalized axis
ax2 = plt.twiny()
ax2.set_xlim(0, 1)
plt.xlabel('{0} normalized interval'.format(param1))

plt.savefig('2Dcdfs/{0}_{1}_{2}_cdf'.format(param1, param2, arg.errors))
