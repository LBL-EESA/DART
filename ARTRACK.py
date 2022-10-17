import numpy as np
from netCDF4 import Dataset  
import matplotlib.pyplot as plt
import scipy.io as sio
from itertools import groupby
from operator import itemgetter
import time
import math
import scipy.ndimage.measurements as measure
import pickle
import glob
import xarray as xr

class ARNode:
    def __init__(self, AR, time, parent, lifetime, ifLast): 
        self.AR = AR  # Assign data 
        self.time = time
        self.parent = parent
        self.ifLast = ifLast
        self.lifetime = lifetime

def TRACK(t_index, ar_t, parent_node, ARfield, Overlapping_threshold, lifetime_threshold, 
          count_split, split_threhold):
    
    """
    Output: Final List [end_node_list1, end_node_list2]
    (end_node_list: [ARNode1, ARNode2])
    """
    
    #t_index: current timestamp 
    #ar_t: AR genesis array at 't_index' timestamp: [[0,0,0,1,1,0,0], [0,0,0,0,0,2,2]]
    #parent_node: 0 or previous ARnode
    #ARfield: array of labeled mask of all time steps

    FinalList = []
    set_0 = set([0])
    num_ar_obj = list(set(np.unique(ar_t)) - set_0)
    
    if len(num_ar_obj) == 0:
        return FinalList
    
    else:
        end_node_list = []
        for i in range(len(num_ar_obj)):
            ar_now = ar_t.copy()
            ar_now_label = num_ar_obj[i]
            
            # keep only the current AR obj
            ar_now[ar_now != ar_now_label] = 0 

            # parent_node of next step
            a = ARNode(ar_now, t_index, parent_node, 0, 0)  
            
            if a.parent!=0:
                a.lifetime = a.parent.lifetime+1;
            else: 
                a.lifetime = 0
                
            # get the map from the next timestamp
#             ar_next = ARfield[t_index+1].copy() 
            s = [[1,1,1],[1,1,1],[1,1,1]]
            labeled_array, num_features = measure.label(ARfield[t_index+1].copy(),structure=s)
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
            ar_next = new_labeled_array.copy()
            
            # Initialize ar_t for next timestamp
            ar_t_1 = np.zeros(np.shape(ar_next)) 

            # find the overlap
            ar_next[ar_now != ar_now_label] = 0 

            # get all the labels in the overlap
            labels_in_next = list(set(np.unique(ar_next)) - set_0)
            
            cur_object_grid = np.count_nonzero(ar_now)
            
            num_labels_in_overlap = len(labels_in_next)

            if num_labels_in_overlap>0:  
                if num_labels_in_overlap>1:
                    count_split = count_split+1
                    
                if count_split > split_threhold:
                    range_for_loop = [0]
                else:
                    range_for_loop = range(0,num_labels_in_overlap)
                
                for n in range_for_loop:
                    temp_next = ar_next.copy()
                    temp_next[temp_next != labels_in_next[n]] = 0
                    
                    temp_next_label = new_labeled_array.copy()
                    temp_next_label[temp_next_label != labels_in_next[n]] = 0
                
                    overlap_grid = np.count_nonzero(temp_next)

                    if overlap_grid / cur_object_grid >= Overlapping_threshold:
                        ar_t_1 += temp_next_label
                        
                        end_node_list += TRACK(t_index+1, ar_t_1, a, ARfield, 
                                               Overlapping_threshold, lifetime_threshold, 
                                               count_split, split_threhold)
            
            else:       
                a.ifLast = 1
                if a.lifetime >=lifetime_threshold:
                    end_node_list.append(a)
                    # end_node_list = [a]
            FinalList += end_node_list   
            FinalList = list(set(FinalList))
        return FinalList
