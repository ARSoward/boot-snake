from dataTypes import network_changes
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
"""
def convert_curve(session_curve):
    print("I don't know what this entails.")
    return 0;

def convert_list(session_list, time):
    print("Converting list data")
    data = network_changes(time)
    for entry in session_list:
        data.add_arrival(entry[0], entry[1])
        data.add_departure(entry[0], entry[2])
    return data;
    
def export(result, filename="data"):
    filename += '.pickle'
    print("saving result to", filename)
    # Store data (serialize)
    with open(filename, 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
# TODO take input from a file
session_list = [[1, 0, 4], [2, 6, 10], [3, 4, 14], [4, 0, 5], [5, 2, 8], [6, 3, 14]]
result = convert_list(session_list, 10)
print(result.net)
export(result)