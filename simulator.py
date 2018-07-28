import pickle
from dataTypes import network 
import numpy as np
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 14:00:03 2018

@author: Abigail Soward

Simulator is created with a pickled data file (see converter.py), an 
initialized attack object, and an initialized algorithm object. It uses these to
create a network object to run the simulation. The run method runs the given 
attack and algorithm on the simulated network, and returns an array that represents 
the costs to the users over the length of the simulated network.

"""
# accepts a pickle file of data from the converter,
# and an attack & defense algo to run on the simulated network.
class simulation(object):
    def __init__(self, pickled_changes, algo, attack):
        print("\tinitializing network")
        with open(pickled_changes, 'rb') as handle:
            changes = pickle.load(handle)
        self.changes = changes
        self.algo = algo
        self.attack = attack
        self.good_costs = []
        self.bad_costs = []
        self.net_changes = []
        self.total_changes = []
        self.network = network(self.changes.arrivals_at_time(0))
        
    def run(self, verbose=False):
        print("\tinitializing attack")
        self.attack.set_interval(self.changes.end_time)
        print("\tinitializing algorithm")
        self.algo.set_vars(self.changes, self.attack, verbose)

        print("\tstarting simulation")
        for i in range(1, self.changes.end_time):
            # bookkeeping for defense algos
            self.network.current_arrivals = len(self.changes.arrivals_at_time(i))+self.attack.sybils_added_at(i)
            
            # add bad ids to network at time i
            bad_entry_cost = self.algo.get_entry_costs(self.attack.sybils_added_at(i))
            self.network.add_sybils(self.attack.sybils_added_at(i))
            
            # add/remove good ids to network at time i
            arrivals, departures = self.changes.at_time(i)
            if verbose: print(arrivals, " new arrivals")
            good_entry_cost = self.algo.get_entry_costs(len(arrivals))
            
            self.network.add_good_ids(arrivals)
            self.network.remove_good_ids(departures)
            
            # evaluate purge costs to good ids and adversary at time i
            good_cost, bad_cost = self.algo.evaluate(self.network, i)
            
            # append to results array
            self.good_costs.append(good_cost + good_entry_cost)
            self.bad_costs.append(bad_cost + bad_entry_cost)
            self.net_changes.append(self.changes.net_at_time(i) + bad_entry_cost)
            self.total_changes.append(self.changes.total_at_time(i) + bad_entry_cost)
            if verbose: print("good pays {} for purge and {} entry cost. current size: {}"
                              .format(good_cost, good_entry_cost, self.network.good_count()))
        self.changes.close_events()
        
    def get_results(self):
        return self.good_costs, self.bad_costs
    
    def get_cumulative_results(self):
        return np.cumsum(self.good_costs), np.cumsum(self.bad_costs)
    
    def get_changes(self):
        return self.total_changes, self.net_changes
    
    def get_cumulative_changes(self):
        return np.cumsum(self.total_changes), np.cumsum(self.net_changes)