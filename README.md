# freezing_params
Holding code and data products for the parameter freezing project

# Running the 1D CDF generator code (on quest)
```bash
#!/bin/bash
module load python

# Multiple data sets and parameters can be plotted simultaneously
python 1dcdfs.py --basepath IMRPhenomPv2=/projects/b1011/spinning_runs/freezingparams_20160402_IMR --basepath SpinTaylorT4=/projects/b1011/spinning_runs/freezingparams_20160402 --param1 mc --param1 q --param1 a1 --param1 a2 --param1 tilt1 --param1 tilt2
python 1dcdfs.py --basepath IMRPhenomPv2=/projects/b1011/spinning_runs/freezingparams_20160402_IMR --basepath SpinTaylorT4=/projects/b1011/spinning_runs/freezingparams_20160402 --param1 distance --param1 ra --param1 dec --param1 theta_jn
done
```

# Running the 1D PDF generator code (on quest)
```bash
#!/bin/bash
module load python
for p in mc q a1 a2 tilt1 tilt2; do
    python 1dpdfs.py --param1 ${p} --basepath /projects/b1011/spinning_runs/freezingparams_20160402 --inj-xml /projects/b1011/spinning_runs/STT2injections.xml
done
```
