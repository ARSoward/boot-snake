import math
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 14:18:48 2018

@author: Abigail Soward

An attack is called at each times step, and calculates how many
sybil ids should be added at that time.
"""

"""
Attack class must extend this base class and override the following 
methods to work with the simulator:
    sybils_added_at(time): given the time and state of the network, return
    the number of sybil ids the adversary creates.
    
    set_interval(end time of simulation): uses the fractions it was passed in
    init to set the start and end timestamps of the attack.     
"""
class attack(object):
    def __init__(self, alpha, attack_size, interval_fractions):
        self.start_fraction, self.end_fraction = interval_fractions
        self.alpha = alpha
        self.size = attack_size
    def sybils_added_at(self, i):
        return 0
    def set_interval(self, time):
        self.start = self.start_fraction * time
        self.end = self.end_fraction * time
        
# burst attack adds a large amount of sybil ids every 5 seconds.
class burst(attack):
    def sybils_added_at(self, i):
        if i%5 == 0 and i > self.start and i < self.end:
            # print("adding sybils at", i)
            return math.ceil(self.size)
        else:
            return 0

    
    
# Another attack would be sudden short bursts at rates which require purges more frequently than 5 seconds, 
# distributed over a period of time.
        