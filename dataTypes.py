import numpy as np
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 14:05:44 2018

@author: freya

Simulation Data Shape
    ID objects that know their nature and session id
    session_arrivals: array of size T + 1. At 0 is a list of the initial session IDs.
    1-T holds the sessions that are added to the network at that time.
"""
        
# Organizes network events by time. Each integer 0 - T has a list
# of events that should occur at that point in time in the simulated network.
class network_changes(object):
    def __init__(self, name, min_t, max_t):
        self.end_time = max_t - min_t # end time holds the interval from start to finish
        self.start_time = min_t # start time holds the beginning time stamp
        self.name = name #name of the data file that holds events array
        self.events = np.memmap(name+'.dat', dtype=np.int32, mode='w+', shape=(self.end_time + 1, 2))
        
    def add_departure(self, time):
        self.add_event(time, False)
    def add_arrival(self, time):
        self.add_event(time, True)
        
    def add_initial(self, size):
        self.save_event(0, [size, 0])
    
    # this function is used by the converter, which uses the unadjusted time stamps.    
    def add_event(self, time, is_arrival):
        t = self.adjust(time)
        if t >= 0 and t <= self.end_time:
            # get current event at adjusted time
            arrivals, departures = self.at_time(t)
            # update dictionary and save
            if is_arrival: arrivals += 1
            else: departures += 1
            self.save_event(t, [arrivals, departures])
            
    def save_event(self, time, entry):
        self.events[time] = entry
        if time == 0: print("initial size: ",entry)
    

    def at_time(self, time):
        try:
            arrivals = self.events[time][0]
        except TypeError:
            return 0, 0
        try:
            departures = self.events[time][1]
        except:
            return arrivals, 0
        return arrivals, departures
    def arrivals_at_time(self, time):
        return self.at_time(time)[0]
    
    def departures_at_time(self, time):
        return self.at_time(time)[1]
    
    def total_at_time(self, time):
        arrivals, departures = self.at_time(time)
        return arrivals + departures
        
    def net_at_time(self, time):
        arrivals, departures = self.at_time(time)
        return arrivals - departures
        
    def initial_size(self):
        return self.at_time(0)

    def close_events(self):
        del self.events
        
    def open_events(self):
        self.events = np.memmap(self.name+'.dat', dtype=np.int32, shape=(self.end_time + 1, 2))
        
    def adjust(self, time):
        # add 1 to the adjustment so they start appearing at 1 instead of 0
        return  1 + time - self.start_time
        
        