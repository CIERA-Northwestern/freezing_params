# 1d anal

import math
import os
import glob
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats
# FIXME: need dvipng to conver latex to image format
#import plotutils
#plotutils.latexify()

parser = argparse.ArgumentParser(description='Freezing param analysis: histogram and cdf for specified parameter combos at 67,90,95 or 99%/ confidence')
parser.add_argument("-p", '--param1', type=str, help='first parameter of interest')
parser.add_argument("-b", '--basepath', type=str, help='base path to search for results')
# parser.add_argument('confidence', type=int, nargs='?', default=90, help='confidence region(67,90,95,99)')
arg = parser.parse_args()
param1 = arg.param1
bpath = arg.basepath
# confidence = arg.confidence

def paths_to_files(combo, bpath):
    # all you need is combo bc that determines path
    path = os.path.join(bpath, '*/{0}/post/confidence_levels.txt'.format(combo))
    paths = glob.glob(path)
    return paths

def split_up_lines(textfile):
    with open(textfile,'r') as conf:
        splitted = map(str.split, conf.readlines())
    return splitted

# FIXME: Change this to default to true once we've got consistent parameters
def extracting_data(textfile, param1, combo, error=False, verbose=False):
    if verbose:
        print "-------- " + textfile
        print filter(lambda s: s[0] == param1, split_up_lines(textfile))
    confreg = [float(item[2]) for item in split_up_lines(textfile) \
             if item[0] == param1]
    if len(confreg) != 1:
        if error:
            raise ValueError("Parameter %s not found in %s" % (param1, textfile))
        else:
            return float("nan")
    return confreg[0]

def collect_all_conflevels(param1, combo, bpath):
    paths = paths_to_files(combo, bpath)
    data = np.asarray([extracting_data(path, param1, combo) for path in paths])
    data.sort()
    return data

print "-------- Plotting CDFs for param %s" % param1

#plotting the cdfs
data_none = collect_all_conflevels(param1,'none', bpath)
y_axis = np.linspace(0,len(data_none)/float(len(data_none)),num=len(data_none))
plt.plot(data_none,y_axis,label='none',color='k')

# "Error bars" on the ECDF vs the "true" CDF
# See:
# https://stats.stackexchange.com/questions/15891/what-is-the-proper-way-to-estimate-the-cdf-for-a-distribution-from-samples-taken
# and
# https://en.wikipedia.org/wiki/Dvoretzky%E2%80%93Kiefer%E2%80%93Wolfowitz_inequality
alpha = 0.95
error_width = math.sqrt(1./2/len(data_none) * math.log(2/alpha))
plt.fill_between(data_none, y_axis - error_width, y_axis + error_width, color='k', alpha=0.3)

data_skyloc = collect_all_conflevels(param1,'skyloc', bpath)
y_axis = np.linspace(0,len(data_skyloc)/float(len(data_skyloc)),num=len(data_skyloc))
plt.plot(data_skyloc,y_axis,label='skyloc')

stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc)
print "KS test between none and skyloc: %1.2e" % ks_val

data_skyloc_dist = collect_all_conflevels(param1,'skyloc_thetajn', bpath)
y_axis = np.linspace(0,len(data_skyloc_dist)/float(len(data_skyloc_dist)),num=len(data_skyloc_dist))
plt.plot(data_skyloc_dist,y_axis,label='skyloc_dist')

stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_dist)
print "KS test between none and skyloc_dist: %1.2e" % ks_val

data_skyloc_thetajn = collect_all_conflevels(param1,'skyloc_thetajn', bpath)
y_axis = np.linspace(0,len(data_skyloc_thetajn)/float(len(data_skyloc_thetajn)),num=len(data_skyloc_thetajn))
plt.plot(data_skyloc_thetajn,y_axis,label='skyloc_thetajn')

stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_thetajn)
print "KS test between none and skyloc_thetajn: %1.2e" % ks_val

data_skyloc_thetajn_dist = collect_all_conflevels(param1,'skyloc_thetajn_dist', bpath)
y_axis = np.linspace(0,len(data_skyloc_thetajn_dist)/float(len(data_skyloc_thetajn_dist)),num=len(data_skyloc_thetajn_dist))
plt.plot(data_skyloc_thetajn_dist,y_axis,label='skyloc_thetajn_dist')

stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_thetajn_dist)
print "KS test between none and skyloc_thetajn_dist: %1.2e" % ks_val

plt.xlabel('{0}'.format(param1))
plt.ylabel('Cumulative Probability')
plt.ylim(0, 1)
plt.grid()
plt.legend(loc=4)
plt.savefig('{0}_1Dcdf'.format(param1))
