from dataTypes import network_node
import pickle
from importlib import import_module
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 14:00:03 2018

@author: freya
"""

# initializer needs more variables
class network_simulation(object):
    def __init__(self, initial_state = []):
        self.sybil_count = 0
        self.network_nodes = {} # dictionary so sessions can be looked up by id
        self.test_interval = 1 # time interval where algo should be called
        for session in initial_state:
            self.add(session)
    def add(self, event):
        session = network_node(event.sid, self.decide_nature()) 
        self.network_nodes[event.sid] = session 
        if session.is_good == False:
            self.sybil_count += 1
    def remove(self, event):
        node = self.network_nodes.pop(event.sid)
        if node.is_good == False:
            self.sybil_count -= 1
    def good_count(self):
        return self.total_count - self.sybil_count
    def total_count(self):
        return len(self.network_nodes)
    def decide_nature(self):
        # TODO decide nature of node
        return True

# accepts a pickle file of data from the converter,
# and a list of algorithms to run on the simulated network.
def run(pickled_changes, algo, verbose=False):
    results = []
    with open(pickled_changes, 'rb') as handle:
        changes = pickle.load(handle)
    # TODO initialize list of algos objects to call during simulation
    print("initializing network")
    network = network_simulation(changes.at_time(0))
    print("starting simulation")
    for i in range(1, changes.time):
        # update the network at time i
        for event in changes.at_time(i):
            if verbose:
                print(event)
            network.add(event) if event.is_arrival else network.remove(event)
        # call algorithms to evaluate work needed for state of network
        if i % network.test_interval == 0:
            if verbose:
                print("bad ids: "+str(network.sybil_count))
                print("total ids: "+str(network.total_count()))
            results.append(algo.evaluate(network))
    return results