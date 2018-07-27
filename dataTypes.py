import numpy as np
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 14:05:44 2018

@author: Abigail Soward

Network abstracts the logic of adding and removing IDs to the network.

Network_changes abstracts the logic of reading and writing to the .dat file
where the converted bitcoin events are stored.
"""
class network(object):
    def __init__(self, initial_state = []):
        self.sybil = 0 # sybil is just a count
        self.good = initial_state # good is a list of current ids
        self.current_churn = 0
        
    def add_good_ids(self, new_ids_list):
        self.good = self.good + new_ids_list
        
    def remove_good_ids(self, remove_ids_list):
        self.good = [x for x in self.good if x not in remove_ids_list]
        
    def sybil_count(self):
        return self.sybil
    
    def good_count(self):
        return len(self.good)
    
    def total_count(self):
        return self.good_count() + self.sybil_count()
    
    def add_sybils(self, number):
        self.sybil += number
        
    def reduce_sybils_to(self, number):
        if number < self.sybil: 
            self.sybil = number
            
            
# Organizes network events by time. Each integer 0 - T has a list of arrivals and
# departures that should occur at that point in time in the simulated network.
class network_changes(object):
    def __init__(self, name, min_t, max_t):
        self.end_time = max_t - min_t # end time holds the interval from start to finish
        self.start_time = min_t # start time holds the beginning time stamp
        self.name = name #name of the data file that holds events array
        self.events = np.memmap(name+'.dat', dtype=dict, mode='w+', shape=(self.end_time + 1, 1))
        
    def add_departure(self, user, time):
        self.add_event(user, time, False)
        
    def add_arrival(self, user, time):
        self.add_event(user, time, True)
        
    def add_initial(self, size):
        self.save_event(0, [size, 0])
    
    # this function is used by the converter, which uses the unadjusted time stamps.    
    def add_event(self, user, time, is_arrival):
        t = self.adjust(time)
        if t >= 0 and t <= self.end_time:
            # get current event at adjusted time
            arrivals, departures = self.at_time(t)
            # update dictionary and save
            if is_arrival: arrivals.append(user)
            else: departures.append(user)
            self.save_event(t, {"arrivals":arrivals, "departures":departures})
            
    def save_event(self, time, entry):
        arrivals, departures = entry
        self.events[time] = entry
    

    def at_time(self, time):
        try:
            arrivals = self.events[time][0].get("arrivals")
        except (AttributeError, IndexError):
            arrivals = []
        try:
            departures = self.events[time][0].get("departures")
        except (AttributeError, IndexError):
            departures = []
        
        return arrivals, departures
    
    def arrivals_at_time(self, time):
        return self.at_time(time)[0]
    
    def departures_at_time(self, time):
        return self.at_time(time)[1]
    
    def total_at_time(self, time):
        arrivals, departures = self.at_time(time)
        return len(arrivals) + len(departures)
        
    def net_at_time(self, time):
        arrivals, departures = self.at_time(time)
        return len(arrivals) - len(departures)
        
    def initial_size(self):
        return len(self.at_time(0))

    def close_events(self):
        del self.events
        
    def open_events(self):
        self.events = np.memmap(self.name+'.dat', dtype=dict, shape=(self.end_time + 1, 1))
        
    def adjust(self, time):
        return  time - self.start_time
        
        