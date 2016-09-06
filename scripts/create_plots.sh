#!/bin/bash

# directory structure
mkdir -p IMRPhenomPv2/plots
mkdir -p SpinTaylorT4/plots
mkdir -p comp/plots

# IMRPhenomPv2 -- all PDFs
for p in mc q a1 a2 tilt1 tilt2 distance ra dec theta_jn; do
    python 1dpdfs.py --param1 ${p} --basepath /projects/b1011/spinning_runs/freezingparams_20160402_IMR --inj-xml /projects/b1011/spinning_runs/IMRfreezinginj.xml
done
mv *pdf*.png IMRPhenomPv2/plots/

# SpinTaylorT4 -- all PDFs
for p in mc q a1 a2 tilt1 tilt2 distance ra dec theta_jn; do
    python 1dpdfs.py --param1 ${p} --basepath /projects/b1011/spinning_runs/freezingparams_20160402 --inj-xml /projects/b1011/spinning_runs/STT2injections.xml
done
mv *pdf*.png SpinTaylorT4/plots/

# CDFs are all comparisons now
# Individual CDFs
for p in mc q a1 a2 tilt1 tilt2 distance ra dec theta_jn; do
    python 1dcdfs.py --basepath IMRPhenomPv2=/projects/b1011/spinning_runs/freezingparams_20160402_IMR --basepath SpinTaylorT4=/projects/b1011/spinning_runs/freezingparams_20160402 --param1 ${p}
done
mv *cdf*.png comp/plots/

# Full comparison
python 1dcdfs.py --basepath IMRPhenomPv2=/projects/b1011/spinning_runs/freezingparams_20160402_IMR --basepath SpinTaylorT4=/projects/b1011/spinning_runs/freezingparams_20160402 --param1 mc --param1 q --param1 a1 --param1 a2 --param1 tilt1 --param1 tilt2
mv 1Dcdf_all.png comp/plots/1dcdf_intrinsic.png

python 1dcdfs.py --basepath IMRPhenomPv2=/projects/b1011/spinning_runs/freezingparams_20160402_IMR --basepath SpinTaylorT4=/projects/b1011/spinning_runs/freezingparams_20160402 --param1 distance --param1 ra --param1 dec --param1 theta_jn
mv 1Dcdf_all.png comp/plots/1dcdf_extrinsic.png

tar zcf freezing_plots.tgz comp SpinTaylorT4 IMRPhenomPv2
