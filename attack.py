import math
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 14:18:48 2018

@author: freya

Attack class must have the following methods to work with the simulator:
    add_sybil(network, time): given the time and state of the network, add the 
    determined amount of sybils to the network, with network.add_sybils(amount).
        
"""

# burst attack adds a large amount of sybil ids every 5 seconds.
class burst(object):
    def __init__(self, alpha, attack_size):
        # todo other variables?
        self.alpha = alpha
        self.size = attack_size
    def add_sybil(self, network, time):
        network.add_sybils(self.changes_at(time))
    def changes_at(self, i):
        if i%5 == 0:
            return math.ceil(self.size)
        else:
            return 0
        
# trickle adds a small amount of ids every second.
class trickle(object):
    def __init__(self, alpha, attack_size):
        self.alpha = alpha
        self.size = attack_size
    def add_sybil(self, network, time):
        network.add_sybils(self.changes_at(time))
    def changes_at(self, i):
        return math.ceil(self.alpha * self.size)
    
# Another attack would be sudden short bursts at rates which require purges more frequently than 5 seconds, 
# distributed over a period of time. 