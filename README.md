# Depth-first Atmospheric River lifecycle Tracking (DART)

## Overview <br>
DART is an python algorithm that can track the lifecycle of atmospheric rivers (ARs). <br>
Please see more details about the algorithm in the following papers:

- Zhou, Y., Kim, H., & Guan, B. (2018). Life Cycle of Atmospheric Rivers: Identification and Climatological Characteristics. Journal of Geophysical Research: Atmospheres, 123. https://doi.org/10.1029/2018JD029180 <br>
- Zhou, Y., & Kim, H. (2019). Impact of Distinct Origin Locations on the Life Cycles of Landfalling Atmospheric Rivers Over the U.S. West Coast. Journal of Geophysical Research: Atmospheres, 124. https://doi.org/10.1029/2019JD031218 <br>

### Input: <br>
Data sets of AR binary masks. Tested on most of the global AR detections in [ARTMIP](https://www.cgd.ucar.edu/projects/artmip/algorithms).  
See results in [Zhou et al. 2021](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020JD033711).

### Example steps:
1. Define the genesis of an AR lifecycle using [FindGenesis.py](https://github.com/LBL-EESA/DART/blob/main/FindGenesis.py). <br> 
2. Track AR lifecycle using [ARTRACK.py](https://github.com/LBL-EESA/DART/blob/main/ARTRACK.py). <br>

### Output
The output of [FindGenesis.py](https://github.com/LBL-EESA/DART/blob/main/FindGenesis.py) is a array of binary masks of AR genesis.  
The output of [ARTRACK.py](https://github.com/LBL-EESA/DART/blob/main/ARTRACK.py) is AR lifecycle tracked with given thresholds of overlapping ratio, split counts, lifetime. The output has linked list data structure, where each node represent one instananeus time slice and the parent node represent the successive time slice, and so on. The first node would be the last time step of AR lifecycle of the trakcing starts with AR genesis (alternately, one can apply the FindGenesis.py to find the termination of AR events, in this case, the first node would be the first time step (genesis) of AR lifecycle of the trakcing starts with AR termination).

### Example
```
from ARTRACK import TRACK
TotalList = TRACK(i, totalARmask, 0, ARmask, 0.1, 3, 0, 3)
```
*i* represents the *i*th time step, *totalARmask* is the array of all binary AR masks, *ARmask* is the genesis array, *0.1* is the overlapping ratio, *3* is the lifetime threshold (example data is hourly, 3 means minimum lifetime of 12 hours), *0* is the counts of splits, this is always 0 when one start the tracking. (The second) *3* is the threholds for spliting. ARs that splits more than 3 times in its lifecycle will be excluded.   

### Copyright Notice
Depth-First Atmospheric River lifecycle Tracking (DART) Copyright (c) 2023,
The Regents of the University of California, through Lawrence Berkeley
National Laboratory (subject to receipt of any required approvals from the
U.S. Dept. of Energy). All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit others to do so.
