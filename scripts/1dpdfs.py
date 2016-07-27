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

def chirp_mass(r):
    return (r.mass1 * r.mass2)**(3./5) / (r.mass1 + r.mass2)**(1./5)

def spin_tilt1(r):
    a1 = spin_mag1(r)
    return np.arccos(r.spin1z / a1)

def spin_tilt2(r):
    a2 = spin_mag2(r)
    return np.arccos(r.spin2z / a2)

def spin_mag1(r):
    return np.sqrt(r.spin1x**2+r.spin1y**2+r.spin1z**2)

def spin_mag2(r):
    return np.sqrt(r.spin2x**2+r.spin2y**2+r.spin2z**2)

# FIXME: The *injected* range for mc in 2 -- 7 ish.
# The posteriors go way beyond this -- this leads to everything concentrated in
# a bin
RANGES = {
    #"mc": (0.87, 27), # 1+1 -> 30+30
    "mc": (1, 10), # 1+1 -> 30+30
    "q": (0, 1),
    "tilt1": (0, np.pi),
    "tilt2": (0, np.pi),
    "a1": (0, 1),
    "a2": (0, 1),
    "theta_jn": (0, np.pi),
    "distance": (1, 1000),
    "ra": (0, 2*np.pi),
    "dec": (-np.pi/2, np.pi/2)
}

GET_PARAM = {
    "mc": lambda r: r.mchirp,
    "q": lambda r: r.mass2 / r.mass1,
    "tilt1": spin_tilt1,
    "tilt2": spin_tilt2,
    "a1": spin_mag1,
    "a2": spin_mag2,
    "theta_jn": lambda r: r.inclination, # FIXME: NOT RIGHT
    "distance": lambda r: r.distance,
    "ra": lambda r: r.longitude,
    "dec": lambda r: r.latitude
}


parser = argparse.ArgumentParser(description='Freezing param analysis: histogram and cdf for specified parameter combos at 67,90,95 or 99%/ confidence')
parser.add_argument("-p", '--param1', type=str, help='first parameter of interest')
parser.add_argument("-b", '--basepath', type=str, help='base path to search for results')
parser.add_argument("-i", '--inj-xml', type=str, help='Injection XML used (optional)')
# parser.add_argument('confidence', type=int, nargs='?', default=90, help='confidence region(67,90,95,99)')
arg = parser.parse_args()
param1 = arg.param1
bpath = arg.basepath
# confidence = arg.confidence

def paths_to_files(combo, bpath):
    # all you need is combo bc that determines path
    path = os.path.join(bpath, '*/{0}/post/posterior_samples.dat'.format(combo))
    paths = glob.glob(path)
    return paths

def split_up_lines(textfile):
    with open(textfile,'r') as conf:
        splitted = map(str.split, conf.readlines())
    return splitted

# FIXME: Change this to default to true once we've got consistent parameters
def extracting_data(textfile, param1, combo, error=False, verbose=False):
    pos_samps = np.genfromtxt(textfile, names=True)
    return pos_samps[param1]

def parse_run_string(path):
    run_n, combo = path.split("/")[-4:-2]
    return run_n, combo

def collect_all_conflevels(param1, combo, bpath):
    paths = paths_to_files(combo, bpath)
    data = dict([(parse_run_string(path), extracting_data(path, param1, combo)) for path in paths])
    return data

def conf_intrv(hist, bins):
    dx = bins[1] - bins[0]
    srt = hist.argsort()
    idx = np.searchsorted(hist[srt].cumsum() * dx, 0.1)
    intr = bins[srt[idx:]]
    # FIXME: This is actually off by a bin width
    return (intr.min(), intr.max())

def conf_intrv2(hist, bins):
    from glue.segments import segment, segmentlist
    dx = bins[1] - bins[0]
    srt = hist.argsort()
    bins = map(segment, list(zip(bins[:-1], bins[1:])))
    idx = np.searchsorted(hist[srt].cumsum() * dx, 0.1)
    intrv = segmentlist()
    for bidx in srt[idx:]:
        intrv.append(bins[bidx])
    return intrv.coalesce()

print "-------- Plotting PDFs for param %s" % param1

#plotting the cdfs
data_none = collect_all_conflevels(param1,'none',bpath)
data_skyloc = collect_all_conflevels(param1,'skyloc', bpath)
data_skyloc_dist = collect_all_conflevels(param1,'skyloc_dist', bpath)
data_skyloc_thetajn = collect_all_conflevels(param1,'skyloc_thetajn', bpath)
data_skyloc_thetajn_dist = collect_all_conflevels(param1,'skyloc_thetajn_dist', bpath)

# Optionally load injections
sim_data = None
if arg.inj_xml:
    from glue.ligolw import lsctables, ligolw, utils
    lsctables.use_in(ligolw.LIGOLWContentHandler)
    xmldoc = utils.load_filename(arg.inj_xml, contenthandler=ligolw.LIGOLWContentHandler)
    sim_data = lsctables.SimInspiralTable.get_table(xmldoc)
    print "Loaded %d injections" % len(sim_data)

# Number of columns
spread_factor = 4
# number of rows * columns
nruns = len(data_none)
print "Collected %d runs, dividing into %d columns" % (nruns, spread_factor)

#plt.figure(figsize=(8,15))
i, ncat, nbins = 1, 5, 20
# Iterate through data and form posteriors
for (run, combo), samples in data_none.iteritems():
    ax = plt.subplot(nruns/spread_factor+1, spread_factor, i)

    hist = np.empty((nbins, ncat))

    hist[:,0], b = np.histogram(samples, bins=nbins, range=RANGES[param1], normed=True)
    if any((RANGES[param1][0] > samples) | (RANGES[param1][1] < samples)):
        print "(%s) Warning some samples are outside the range." % run

    samples = data_skyloc[(run, "skyloc")]
    if any((RANGES[param1][0] > samples) | (RANGES[param1][1] < samples)):
        print "(%s) Warning some samples are outside the range." % run

    hist[:,1], _ = np.histogram(samples, bins=b, range=RANGES[param1], normed=True)
    samples = data_skyloc_dist[(run, "skyloc_dist")]
    if any((RANGES[param1][0] > samples) | (RANGES[param1][1] < samples)):
        print "(%s) Warning some samples are outside the range." % run

    hist[:,2], _ = np.histogram(samples, bins=b, range=RANGES[param1], normed=True)
    samples = data_skyloc_thetajn[(run, "skyloc_thetajn")]
    if any((RANGES[param1][0] > samples) | (RANGES[param1][1] < samples)):
        print "(%s) Warning some samples are outside the range." % run

    hist[:,3], _ = np.histogram(samples, bins=b, range=RANGES[param1], normed=True)
    samples = data_skyloc_thetajn_dist[(run, "skyloc_thetajn_dist")]
    if any((RANGES[param1][0] > samples) | (RANGES[param1][1] < samples)):
        print "(%s) Warning some samples are outside the range." % run

    hist[:,4], _ = np.histogram(samples, bins=b, range=RANGES[param1], normed=True)

    ax.locator_params(axis='x', nbins=3)
    # FIXME: plot disappears?
    xx, yy = np.meshgrid(b, range(6))
    plt.pcolormesh(xx, yy, hist.T, cmap=matplotlib.cm.Reds)

    # Set the number of ticks so its consistent across all plots
    plt.xlim(RANGES[param1])
    # Turn off tick marks where not necessary
    if i <= (nruns - spread_factor):
        ax.set_xticklabels([])
    # Y ticks are not necessary at all
    ax.yaxis.set_major_locator(plt.NullLocator())

    # Plot confidence band
    for j, h in enumerate(hist.T):
        ymin, ymax = j / float(ncat), (j+1) / float(ncat)

        #intrv = conf_intrv(h, b)
        for intrv in conf_intrv2(h, b):
            # FIXME: Use hatching or something
            plt.axvspan(intrv[0], intrv[1], ymin, ymax, facecolor='none', edgecolor='g')
            plt.axvspan(intrv[0], intrv[1], ymin, ymax, facecolor='g', edgecolor='none', alpha=0.3)

    intrv = conf_intrv2(h, b)
    if len(intrv) != 1:
        print "Actual confidence interval disjoint for %s, %s" % (run, combo)

    if sim_data:
        inj_val = GET_PARAM[param1](sim_data[int(run)])
        plt.axvline(inj_val, color='c')

    # We could do SNR or something here...
    # FIXME: the space at the end is a hack to stop the label from clipping
    plt.ylabel(run + " ", rotation='horizontal', verticalalignment='center', fontsize=10, labelpad=10)

    i += 1

plt.tight_layout()
plt.subplots_adjust(hspace=0)
plt.savefig("%s_1Dpdf" % param1)
