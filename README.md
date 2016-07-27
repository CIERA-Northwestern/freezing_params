# freezing_params
Holding code and data products for the parameter freezing project

# Running the 1D CDF generator code (on quest)
```bash
#!/bin/bash
module load python

for p in mc q a1 a2 tilt1 tilt2; do
    python 1dcdfs.py --param1 ${p} --basepath /projects/b1011/spinning_runs/freezingparams_20160402
done
```

# Running the 1D PDF generator code (on quest)
```bash
#!/bin/bash
module load python
for p in mc q a1 a2 tilt1 tilt2; do
    python 1dpdfs.py --param1 ${p} --basepath /projects/b1011/spinning_runs/freezingparams_20160402
done
```
