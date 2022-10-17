import numpy as np
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import matplotlib.pyplot as plt
import scipy.io as sio
import math
import scipy.ndimage.measurements as measure
import pickle
import glob
import xarray as xr

def genesis(ARmask):
    ARgen = np.zeros(np.shape(ARmask)) 
    OverlappingRatio = []
    for i in range(0,np.shape(ARmask)[0]):
        s = [[1,1,1],[1,1,1],[1,1,1]]
        labeled_array, num_features = measure.label(ARmask[i,:,:],structure=s)
        new_labeled_array=labeled_array.copy()
        set_0 = set([0])
        west = labeled_array[:,0].copy()
        east = labeled_array[:,-1].copy()
        branches = list(set(west) - set_0)
        flag_branch = np.zeros(len(west))
        for branch in branches:
            ab_intersect = list(set(east[west == branch]) - set_0)
            if len(ab_intersect) > 0:
                for i_intersect in ab_intersect:
                    if all(v == 0 for v in flag_branch[east == i_intersect]):
                        new_labeled_array[labeled_array == i_intersect] = branch
                        flag_branch[east == i_intersect] = branch
                    else:
                        new_labeled_array[labeled_array == i_intersect] = \
                        flag_branch[east == i_intersect][0]

        object_num = np.unique(new_labeled_array)

        if i!=0 :
            for k in np.arange(0,len(object_num)):
                ar_laststep = ARmask[i-1].copy()
                ar_laststep[new_labeled_array != object_num[k]] = 0
                ar_thisstep = new_labeled_array.copy()
                ar_thisstep[ar_thisstep != object_num[k]] = 0

                overlap_grid = np.count_nonzero(ar_laststep)
                object_grid = np.count_nonzero(new_labeled_array == object_num[k])

                OverlappingRatio.append(overlap_grid/object_grid)

                if overlap_grid == 0:
                    ARgen[i] = ARgen[i] + ar_thisstep/object_num[k]
    return ARgen
