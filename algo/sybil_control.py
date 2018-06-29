#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 21:46:03 2018

@author: freya
"""
# n = number of ids in the  system
# g = 0 good ids 
# ns = 0 bad ids
# alpha = computational power of adversary

# returns
# ccost = array with count of good ids at each time step?
# sybil = percentage of system that is controlled by adversary at each time step??

# appears to be counting the number of good/bad ids in the current system.
# number of good and bad ids will be tracked in simulation, so this part may be skipped?
# for each id in the system
    # if id has a good nature
        # increment g
    # if id has a bad nature
        # if ns <= g/alpha
            # increment ns
            # increment total
        # else
            # remove id from system??

# calculating cost of this algorithm at this point in time
# n1 = 0
# for each id
    # if nature is not 0 (ie if id is in system)
        # increment n1
# if n1 = 0 (nobody in system) 
    # cost is 0
# else cost = 100*ns/n1 (bad ids / total ids expressed as a percentage)
class sybil_control(object):
    def __init__(self):
        # TODO store local variables
        self.state = []
    def evaluate(self,network):
        return 100*network.sybil_count/network.total_count()

    

    