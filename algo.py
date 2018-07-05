import math
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 14:15:14 2018

@author: freya

Control algorithms must have the following methods to work with the simulator:
    set_vars(changes, attack, [verbose]): 
        save any variables that the algorithm needs for determining costs, purge times, etc
        
    evaluate(network, time): based on the state of the network at this time,
        purge bad IDs if necessary using network.reduce_sybils(value)
        and return the cost to users at this time.
        
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
def purge(good, bad, alpha):
    new_sybil_count = math.ceil(good / (1 - alpha))
    return min(bad, new_sybil_count) 
"""
sybilControl gives a purge test every 5 seconds.
"""
class sybil_control(object):
    def __init__(self):
        self.name = "sybilControl"
        self.alpha = 0
        
    def set_vars(self, changes, attack, verbose):
        self.alpha = attack.alpha
        
    def evaluate(self,network,time):
        if time % 5 == 0:
            new_count = purge(network.good_count(), network.sybil_count(), self.alpha)
            network.reduce_sybils_to(new_count)
            return 100*network.sybil_count()/network.total_count() # from matlab file
        return 0
        
class ccom(object):
    def __init__(self):
        self.name = "ccom"
        self.epochs = []
        self.alpha = 0
        
    def evaluate(self, network, time):
        # TODO implement entry costs
        # this is just the purge cost
        if self.epochs.__contains__(time):
            new_count = purge(network.good_count(), network.sybil_count(), self.alpha)
            network.reduce_sybils_to(new_count)
            return network.total_count()
        return 0
    
    def set_vars(self, changes, attack, verbose):
        self.get_epochs(changes, attack, verbose)
        self.alpha = attack.alpha
        
    # helper functions
    def get_epochs(self, changes, attack, verbose=False):
        # size of network at time 0
        initial_size = changes.at_time(0)
        good_count = initial_size
        sybil_count = 0
        # if verbose: print("initial size: ", initial_size)
        for time in range(0, changes.end_time):
            # add up changes until size increases or decreases by 1/3
            sybil_count += attack.changes_at(time)
            good_count += changes.at_time(time)
            if abs(initial_size - sybil_count - good_count) >= initial_size/3:
                # save this time as an epoch
                self.epochs.append(time)
                # purge and reset sybil count and initial size
                sybil_count = purge(good_count, sybil_count, attack.alpha)
                initial_size = good_count + sybil_count
        if verbose: print("set epochs: ", self.epochs)
        
    