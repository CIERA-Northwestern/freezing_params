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

import common

parser = argparse.ArgumentParser(description='Freezing param analysis: histogram and cdf for specified parameter combos at 67,90,95 or 99%/ confidence')
parser.add_argument("-p", '--param1', type=str, help='first parameter of interest')
parser.add_argument("-b", '--basepath', type=str, help='base path to search for results')
parser.add_argument("-e", '--errors', type=str, default='bounded', help='Plot these types of error bars. Valid choices are: none, bounded, poisson, binomial. Default is \'bounded\'')
# parser.add_argument('confidence', type=int, nargs='?', default=90, help='confidence region(67,90,95,99)')
arg = parser.parse_args()
if arg.errors not in ('none', 'bounded', 'poisson', 'binomial'):
    raise ArgumentError("Invalid error bound selection.")

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
    data = np.asarray([0] + [extracting_data(path, param1, combo) for path in paths])
    data.sort()
    return data

print "-------- Plotting CDFs for param %s" % param1

#plotting the cdfs
data_none = collect_all_conflevels(param1,'none', bpath)
y_axis = np.linspace(0,len(data_none)/float(len(data_none)),num=len(data_none))
#plt.plot(data_none,y_axis,label='none',color='k')
plt.step(data_none,y_axis,label='none',color='k')

if arg.errors == "bounded":
    # "Error bars" on the ECDF vs the "true" CDF
    # See:
    # https://stats.stackexchange.com/questions/15891/what-is-the-proper-way-to-estimate-the-cdf-for-a-distribution-from-samples-taken
    # and
    # https://en.wikipedia.org/wiki/Dvoretzky%E2%80%93Kiefer%E2%80%93Wolfowitz_inequality
    # and
    # http://web.as.uky.edu/statistics/users/pbreheny/621/F10/notes/8-26.pdf
    alpha = 0.95
    error_width = math.sqrt(1./2/len(data_none) * math.log(2/alpha))
    error_width = np.ones(len(data_none)) * error_width
    # Clip the error bounds to fit the domain of the CDF
    error_width = np.clip(error_width, 0, 1)
    # FIXME: fill_between interpolates rather than using steps
    plt.fill_between(data_none, y_axis - error_width, y_axis + error_width, color='k', alpha=0.3, interpolate=False)
# Poisson
elif arg.errors == "poisson":
    error_width = 1 / np.sqrt(range(1, len(y_axis)+1))
    plt.fill_between(data_none, y_axis - error_width, y_axis + error_width, color='k', alpha=0.3)
# Bunomial
elif arg.errors == "binomial":
    error_width = np.sqrt((y_axis * (1-y_axis)) / range(1, len(y_axis)+1))
    plt.fill_between(data_none, y_axis - error_width, y_axis + error_width, color='k', alpha=0.3)

"""
# Jacknife -- only used for diagnostics
else:
    for j in range(len(data_none)):
        cpy = np.concatenate((data_none[:j], data_none[(j+1):]))
        y_axis = np.linspace(0,len(cpy)/float(len(cpy)),num=len(cpy))
        plt.plot(cpy,y_axis,color='m',alpha=0.3)
"""

data_skyloc = collect_all_conflevels(param1,'skyloc', bpath)
stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc)
print "KS test between none and skyloc: %1.2e" % ks_val

y_axis = np.linspace(0,len(data_skyloc)/float(len(data_skyloc)),num=len(data_skyloc))
plt.step(data_skyloc,y_axis,label='skyloc (KS: %1.2e)' % ks_val)

data_skyloc_dist = collect_all_conflevels(param1,'skyloc_thetajn', bpath)
stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_dist)
print "KS test between none and skyloc_dist: %1.2e" % ks_val

y_axis = np.linspace(0,len(data_skyloc_dist)/float(len(data_skyloc_dist)),num=len(data_skyloc_dist))
plt.step(data_skyloc_dist,y_axis,label='skyloc_dist (KS: %1.2e)' % ks_val)

data_skyloc_thetajn = collect_all_conflevels(param1,'skyloc_thetajn', bpath)
stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_thetajn)
print "KS test between none and skyloc_thetajn: %1.2e" % ks_val

y_axis = np.linspace(0,len(data_skyloc_thetajn)/float(len(data_skyloc_thetajn)),num=len(data_skyloc_thetajn))
plt.step(data_skyloc_thetajn,y_axis,label='skyloc_thetajn (KS: %1.2e)' % ks_val)

data_skyloc_thetajn_dist = collect_all_conflevels(param1,'skyloc_thetajn_dist', bpath)
stat, ks_val = scipy.stats.ks_2samp(data_none, data_skyloc_thetajn_dist)
print "KS test between none and skyloc_thetajn_dist: %1.2e" % ks_val

y_axis = np.linspace(0,len(data_skyloc_thetajn_dist)/float(len(data_skyloc_thetajn_dist)),num=len(data_skyloc_thetajn_dist))
plt.step(data_skyloc_thetajn_dist,y_axis,label='skyloc_thetajn_dist (KS: %1.2e)' % ks_val)

plt.xlabel('{0} confidence interval'.format(param1))
plt.ylabel('Cumulative Probability')
plt.xlim(common.RANGES[param1])
plt.ylim(0, 1)
plt.grid()
plt.legend(loc=4)

# Add normalized axis
ax2 = plt.twiny()
ax2.set_xlim(0, 1)
plt.xlabel('{0} normalized interval'.format(param1))

plt.savefig('{0}_1Dcdf'.format(param1))
