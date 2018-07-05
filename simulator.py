import pickle
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 14:00:03 2018

@author: freya

Simulator is created with a pickled data file (see converter.py), an 
initialized attack object, and an initialized algorithm object. It uses these to
create a network object to run the simulation. The run method runs the given 
attack and algoritm on the simulated network, and returns an array that represents 
the costs to the users over the length of the simulated network.

"""

# initializer needs more variables
class network(object):
    def __init__(self, initial_state = 0):
        self.sybil = 0
        self.good = initial_state
        
    def update_good_ids(self, number):
        self.good += number
        
    def sybil_count(self):
        return self.sybil
    
    def good_count(self):
        return self.good
    
    def total_count(self):
        return self.good + self.sybil
    
    def add_sybils(self, number):
        self.sybil += number
        
    def reduce_sybils_to(self, number):
        self.sybil =  number

# accepts a pickle file of data from the converter,
# and an attack & defencse algo to run on the simulated network.
class simulation(object):
    def __init__(self, pickled_changes, algo, attack):
        print("initializing network")
        with open(pickled_changes, 'rb') as handle:
            changes = pickle.load(handle)
        changes.open_events()
        self.changes = changes
        self.algo = algo
        self.attack = attack
        self.results = []
        self.network = network(self.changes.at_time(0))
        
    def run(self, verbose=False):
        print("initializing algorithm")
        self.algo.set_vars(self.changes, self.attack, verbose)
        print("starting simulation")
        for i in range(1, self.changes.end_time):
            # add bad ids at time i
            self.attack.add_sybil(self.network, i)
                
            # update the network at time i
            self.network.update_good_ids(self.changes.at_time(i))
                    
            # evaluate costs at time i
            #TODO results array should also go in a memmap
            #TODO algo is returning an array when not 0?
            self.results.append(self.algo.evaluate(self.network, i))
        return self.results
    def get_results(self):
        return self.results