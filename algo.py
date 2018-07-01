import math
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 14:15:14 2018

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
        # such as alpha
        self.name = "sybilControl"
    # sybilControl gives a purge test every 5 seconds.
    # purge will reduce the # of sybil ids.
    def evaluate(self,network,alpha,time):
        return 100*network.sybil_count()/network.total_count()
        
class ccom(object):
    def __init__(self):
        # TODO store local variables
        # such as alpha
        self.name = "ccom"
        self.epochs = []
    def evaluate(self, network, alpha, time):
        # TODO implement entry costs
        # this is just the purge cost
        if self.epochs.__contains__(time):
            new_sybil_count = math.ceil(alpha * network.sybil_count() / 3)
            network.reduce_sybils(new_sybil_count)    
            return network.total_count()
        return 0
    def get_epochs(self, changes, attack, verbose=False):
        # size of network at time 0
        initial_size = changes.net[0]
        current_size = initial_size
        sybil_count = 0
        if verbose: print("initial size: ", initial_size)
        for time in range(1, changes.time):
            # add up changes until size increases or decreases by 1/3
            sybil_count += attack.changes_at(time)
            current_size += (changes.net[time] + attack.changes_at(time))
            if verbose: print("current size: ", current_size)
            if abs(initial_size - current_size) >= initial_size/3:
                # save this time as an epoch
                if verbose:
                    print("new epoch at ", time)
                    print("\n")
                self.epochs.append(time)
                # purge and reset sybil count and initial size
                new_sybil_count = math.ceil(attack.alpha * sybil_count / 3)
                current_size -= (sybil_count - new_sybil_count)
                sybil_count = new_sybil_count
                initial_size = current_size
                if verbose: print("initial size: ", initial_size)
        if verbose: print("set epochs: ", self.epochs)
        
    