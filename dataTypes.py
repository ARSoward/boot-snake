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
# network simulation takes a list of ids and generates nodes with them.
# nature is set by the network on creation.
class network_node(object):
    def __init__(self, sid=0, is_good=True):
        self.sid = sid
        self.is_good = is_good
    def set_id(self, sid):
        self.sid = sid 
    def set_nature(self, nature):
        self.is_good = nature
    
# marks the arrival or departure of a user in the network.
# simulation accepts a list of these events at each time point,
# and uses it to create and delete nodes from the network.
class network_event(object):
    def __init__(self, sid, is_arrival=True):
        self.sid = sid
        self.is_arrival = is_arrival
    def __str__(self):
        return ("arrival" if self.is_arrival else "departure")+" event from sid "+str(self.sid)
        
# Organizes network events by time. Each integer 0 - T has a list
# of events that should occur at that point in time in the simulated network.
class network_changes(object):
    def __init__(self, time):
        self.events = {n: [] for n in range(time+1)}
        self.time = time+1
    def add_event(self, time, sid, is_arrival):
        if time < self.time:
            event = network_event(sid, is_arrival)
            self.events[time].append(event)
    def add_departure(self, sid, time):
        self.add_event(time, sid, False)
    def add_arrival(self, sid, time):
        self.add_event(time, sid, True)
    def at_time(self,time):
        return self.events.get(time)
        
        