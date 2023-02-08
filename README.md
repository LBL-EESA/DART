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
