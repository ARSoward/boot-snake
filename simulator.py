from dataTypes import network_node
import pickle
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 14:00:03 2018

@author: freya
"""

# initializer needs more variables
class network(object):
    def __init__(self, initial_state = []):
        self.sybil = 0
        self.network_nodes = {} # dictionary so sessions can be looked up by id
        for session in initial_state:
            self.add(session)
    def add(self, event):
        session = network_node(event.sid) 
        self.network_nodes[event.sid] = session 
    def remove(self, event):
        self.network_nodes.pop(event.sid)
    def sybil_count(self):
        return self.sybil
    def good_count(self):
        return len(self.network_nodes)
    def total_count(self):
        return self.good_count() + self.sybil_count()
    def add_sybils(self, number):
        self.sybil += number
    def reduce_sybils(self, number):
        self.sybil =  number

# accepts a pickle file of data from the converter,
# and an attack & defencse algo to run on the simulated network.
class simulation(object):
    def __init__(self, pickled_changes, algo, attack):
        print("initializing simulation")
        with open(pickled_changes, 'rb') as handle:
            changes = pickle.load(handle)
        self.changes = changes
        self.network = network(self.changes.at_time(0))
        self.algo = algo
        self.attack = attack
        self.alpha = attack.alpha
        self.results = []
    def run(self, verbose=False):
        if(self.algo.name is "ccom"):
            self.algo.get_epochs(self.changes, self.attack, verbose)
        # TODO initialize list of algos objects to call during simulation
        print("starting simulation")
        for i in range(1, self.changes.time):
            # add bad ids at time i
            self.attack.add_sybil(self.network, i)
            
            # update the network at time i
            for event in self.changes.at_time(i):
                self.network.add(event) if event.is_arrival else self.network.remove(event)
                if verbose:
                    print(event)
            # evaluate costs at time i
            self.results.append(self.algo.evaluate(self.network, self.alpha, i))
            if verbose:
                print("bad ids: ",self.network.sybil_count())
                print("total ids: ",self.network.total_count())
        return self.results
    def get_results(self):
        return self.results