from dataTypes import network_changes
import scipy.io as spio
import pickle

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 13:43:03 2018
@author: freya

Data Converter
1. Takes data in various formats and spits out objects that simulator can accept
2. Export/save objects so it doesn't need to run before every simulation
Supported Formats:
    list of {id, entry, exit} events
    another format which involves a probability curve
    
Output data shape:
    [
      [in @ time 0, out @ time 0]
      . . .
      [in @ time n, out @ time n]
    ]
    
"""

# TODO use command line args
# take arg for index in array of enter/exit timestamps.
# filename.mat will be opened, filename.dat and filename.pickle will be saved.   
filename = "newdatadist"  

def convert_curve(session_curve):
    print("I don't know what this entails.")
    return 0;

def convert_list(session_list, name, min_t, max_t, initial):
    print("Converting list data...")
    data = network_changes(name, min_t, max_t)
    
    print("Creating initial state...")
    data.add_initial(initial)
    
    print("Adding network events:")
    for i in range(9212, len(session_list)-1):
        entry = session_list[i]
        if entry[0]%100000 == 0:
            print("\tfinished {} entries...".format(entry[0]))
        # at time 1496010924 the normal mixture of connect and disconnect events begin.
        data.add_arrival(entry[1]) 
        data.add_departure(entry[2])
    
    print("done.")
    data.close_events()
    return data;

def find_time_range(array, index):
    max = 0
    min = array[0][index-1] # pick arbitrary element as initial min
    for item in array:
        if item[index - 1] < min:
            min = item[index - 1]
        if item[index] > max:
            max = item[index]
    print("smallest time stamp: ", min)
    print("largest time stamp:  ", max)
    # at time 1496010924 the normal mixture of connect and disconnect events begin.
    return 1496010924, max
    
def export(result, filename="data"):
    filename += '.pickle'
    print("saving result to", filename)
    # Store data (serialize)
    with open(filename, 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
         
print("reading matlab file...")
mat_dict = spio.loadmat("./mat/"+filename+".mat", variable_names=["x", "n_id"])
min_t, max_t = find_time_range(mat_dict["x"], 2)
#TODO find real initial size of network
sim_dict = convert_list(mat_dict["x"], filename, min_t, max_t, initial=9212) 
export(sim_dict, filename)
