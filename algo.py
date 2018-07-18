import math
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 14:15:14 2018

@author: freya

Control algorithms must extend this class and override init, set_vars, evaluate,
and get_entry_costs to work with the simulator    
"""
class control_algorithm(object):
    def __init__(self):
        self.name = "Undefined Algorithm"
    
    def set_vars(self, changes, attack, verbose=True):
        # set and save any variables that the algorithm needs for determining costs, purge times, etc
        return
    
    def evaluate(self, network, time):
        # based on the state of the network at this time,
        # purge bad IDs if necessary using network.reduce_sybils(value)
        # and return the cost to good ids, bad ids at this time.
        return 0
    
    def get_entry_costs(self, joins):
        # calculate and returns the total entry cost for X joins
        return 0
    
    def purge(self, good, bad, alpha):
        new_sybil_count =  math.ceil(good * alpha) # math.ceil(good / (1 - alpha)) # 
        return min(bad, new_sybil_count)

 
"""
sybilControl gives a purge test every 5 seconds.
"""
class sybil_control(control_algorithm):
    def __init__(self):
        self.name = "sybilControl"
        self.alpha = 0
        
    def set_vars(self, changes, attack, verbose=True):
        self.alpha = attack.alpha
        self.verbose = verbose
        
    def evaluate(self,network,time):
        if time % 5 == 0:
            new_count = self.purge(network.good_count(), network.sybil_count(), self.alpha)
            network.reduce_sybils_to(new_count)
            # return 100*network.sybil_count()/network.total_count() # from matlab file
            # all ids remaining in the system paid cost of 1 to solve purge test.
            return network.good_count(), network.sybil_count() 
        return 0, 0
    
    def get_entry_costs(self, joins):
        return joins

"""
ccom gives a purge test when it detects a new 'epoch' - when the number of ids 
in the system has increased or decreased by 1/3.
"""        
class ccom(control_algorithm):
    def __init__(self):
        self.name = "ccom"
        self.alpha = 0
        self.churn_since_epoch = 0
        self.initial_size = 0
        self.verbose = False
        
    def evaluate(self, network, time):
        # if the network has changed enough for a new epoch,
        # calculate how many sybils will be left after the purge and apply this
        # number to the network. Then, update the initial size to the size
        # of the network after the purge.
        
        # this is not quite right - if an id joins and leaves in the same
        # epoch (in between purges) it will be counted twice. 
        self.churn_since_epoch += network.current_churn
        if self.is_new_epoch():
            # print("new epoch at", time)
            self.churn_since_epoch = 0
            new_count = self.purge(network.good_count(), network.sybil_count(), self.alpha)
            network.reduce_sybils_to(new_count)
            self.initial_size = network.total_count()
            return network.good_count(), network.sybil_count()
        return 0, 0
    
    def set_vars(self, changes, attack, verbose):
        self.initial_size = changes.net_at_time(0)
        self.alpha = attack.alpha
        self.verbose = verbose
        
    def get_entry_costs(self, joins):
        return joins
        
    # helper functions
    def is_new_epoch(self):
        if self.churn_since_epoch >= self.initial_size/3:
            #print("symmetric difference is {} initial size is {}".format(self.churn_since_epoch, self.initial_size))
            return True
        return False
        
"""
improved ccom gives a purge test when it detects a new 'epoch' - when the number of ids 
in the system has increased or decreased by 1/3.
This improved algorithm also calculates the entry cost based on the amount of 
churn that occured in the previous epoch.
""" 
class improved_ccom(ccom):
    def __init__(self):
        self.name = "ccom"
        self.alpha = 0
        self.churn_since_epoch = 0
        self.joins_since_epoch = 0
        self.epoch_length = 0
        self.initial_size = 0
        self.entry_cost = 1 # TODO figure out initial churn
        self.verbose = False
        
    def get_entry_costs(self, joins):
        return self.entry_cost * joins 
    
    # helper functions
    def calculate_entry_cost(self):
        avg_churn = self.churn_since_epoch / self.epoch_length
        return self.joins_since_epoch / avg_churn
        
        
    