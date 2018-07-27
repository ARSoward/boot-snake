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

This converter will really only work for the specific matlab file I was provided,
but it could be adapted to any matlab file by changing some of the hard-coded values
or changing them into command line args.
Input Data Shape:
"x":
[
    [id_1, arrival_time, departure_time]    
    ...
]    
Output data shape:
    [
      {
        'arrivals':[id a, id b, id c...]
        'departures':[id d, id e, id f...]   
      }
      ...
    ]
    
"""

# TODO use command line args instead of hard-coded
# take arg for index in array of enter/exit timestamps.
# filename.mat will be opened, filename.dat and filename.pickle will be saved.   
FILENAME = "newdatadist"
# first 9212 entries in dat file are the initial network
INITIAL_EVENTS = 9212  
# at time 1496010924 the normal mixture of connect and disconnect events begin.
FIRST_TIME_STAMP = 1496010924

def convert_list(session_list, name, min_t, max_t):
    print("Converting list data...")
    data = network_changes(name, min_t, max_t)
    
    print("adding initial events...")
    for i in range(0, INITIAL_EVENTS):
        entry = session_list[i]
        data.add_arrival(entry[0], min_t)
        data.add_departure(entry[0], entry[2])
    print("Adding network events...")
    for i in range(INITIAL_EVENTS, len(session_list)-1):
        entry = session_list[i]
        if entry[0]%100000 == 0:
            print("\tfinished {} entries...".format(entry[0]))
        data.add_arrival(entry[0], entry[1]) 
        data.add_departure(entry[0], entry[2])
    
    print("done.")
    return data;

def find_time_range(array, index):
    max = 0
    for item in array:
        if item[index] > max:
            max = item[index]
    print("largest time stamp:  ", max)
    return FIRST_TIME_STAMP, max
    
def export(result, filename="data"):
    filename += '.pickle'
    print("saving result to", filename)
    # Store data (serialize)
    with open(filename, 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
         
# running converter
print("reading matlab file...")
# TODO use command line args here too
mat_dict = spio.loadmat("./mat/"+FILENAME+".mat", variable_names=["x", "n_id"])
min_t, max_t = find_time_range(mat_dict["x"], 2)
sim_dict = convert_list(mat_dict["x"], FILENAME, min_t, max_t) 
export(sim_dict, FILENAME)
