import numpy as np
import math
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 14:15:14 2018

@author: Abigail Soward

At each time step of the simulation, a defense algorithm will calculate the 
entry costs for users and evaluate the network. If it determines the network
needs to purge(reduce sybil ids) it will do so.
"""
"""
New algorithms must extend this base class and override init, set_vars, evaluate,
and get_entry_costs to work with the simulator.    
"""
class defense_algorithm(object):
    def __init__(self):
        self.name = "Base Algorithm"
        self.alpha = 0
    
    def set_vars(self, changes, attack, verbose=True):
        # set and save any variables that the algorithm needs for determining costs, purge times, etc
        return
    
    def evaluate(self, network, time):
        # based on the state of the network at this time,
        # purge bad IDs if necessary using network.reduce_sybils(value)
        # and return the cost to good ids, bad ids at this time.
        new_sybil_count = self.purge(good=0, bad=0, alpha=self.alpha)
        network.reduce_sybils_to(new_sybil_count)
        return 0, 0
    
    def get_entry_costs(self, joins):
        # calculate and returns the total entry cost for X joins
        return 0
    
    def purge(self, good, bad, alpha):
        # this calculation is for persistent sybils
        # new_sybil_count =  math.ceil(good * alpha) # math.ceil(good / (1 - alpha)) # 
        # return min(bad, new_sybil_count)
        
        # assume lazy sybils
        return 0
 
"""
sybilControl gives a purge test every 5 seconds.
"""
class sybil_control(defense_algorithm):
    def __init__(self):
        self.name = "sybilControl"
        
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
class ccom(defense_algorithm):
    def __init__(self):
        self.name = "ccom"
        self.initial_size = 0
        self.initial_id_set = {}
        self.initial_sybils = 0
        self.verbose = False
        self.sym_diff = 0
        
    def set_vars(self, changes, attack, verbose):
        self.initial_id_set = set(changes.arrivals_at_time(0))
        self.initial_size = changes.net_at_time(0)
        self.alpha = attack.alpha
        self.verbose = verbose
        
    def evaluate(self, network, time):
        # if the network has changed enough for a new epoch,
        # calculate how many sybils will be left after the purge and apply this
        # number to the network. Then, update the initial size to the size
        # of the network after the purge.
        
        # this is not quite right - if an id joins and leaves in the same
        # epoch (in between purges) it will be counted twice. 
        
        if self.is_new_epoch(network):
            if(self.verbose): print("new epoch at", time)
            new_count = self.purge(network.good_count(), network.sybil_count(), self.alpha)
            network.reduce_sybils_to(new_count)
            self.initial_id_set = set(network.good)
            self.initial_size = network.total_count()
            return network.good_count(), network.sybil_count()
        return 0, 0
        
    def get_entry_costs(self, joins):
        return joins
        
    # helper functions
    def is_new_epoch(self, network):
        current_ids = network.good
        current_sybils = network.sybil_count()
        # symmetric difference is ids who are in initial set XOR current set,
        # plus difference in intitial and current sybil count
        self.sym_diff = len(self.initial_id_set.symmetric_difference(current_ids))
        self.sym_diff += abs(current_sybils - self.initial_sybils)
        
        if self.sym_diff >= self.initial_size/3:
            if(self.verbose):
                print("symmetric difference is {} initial size is {}"
                      .format(self.sym_diff, len(self.initial_id_set)))
            return True
        return False
        
"""
Similar to ccom, gives a purge test when it detects a new 'epoch' - when the number of ids 
in the system has increased or decreased by 1/3.
This improved algorithm also calculates the entry cost based on the amount of 
churn that occured in the previous epoch.
""" 
class dmcom(ccom):
    def __init__(self):
        super().__init__()
        self.name = "dmcom"
        self.joins_since_epoch = 0
        self.time_since_epoch = 0
        self.chi_hat = 10000 # TODO ???
           
    def evaluate(self, network, time):
        # joins_since_epoch is updated AFTER getting entry costs,
        # because we need joins at t - 1 to calculate 
        self.joins_since_epoch += network.current_arrivals
        self.time_since_epoch += 1
        
        # update chi hat & reset variables if it's a new epoch
        if self.is_new_epoch(network):
            self.chi_hat = self.calc_chi_hat()
            if(self.verbose): print("new chi_hat: ", self.chi_hat)
            self.joins_since_epoch = 0
            self.time_since_epoch = 0
        
        # after chi hat is updated, evaluate costs to network same as ccom would
        return super().evaluate(network, time)
        
    
    def get_entry_costs(self, n):
        # sums up entry costs for all ids joining at this time step.
        # important that this is called BEFORE evaluate, 
        # which will update current_churn to the end of the time step
        # and possibly change chi hat.
        if n == 0: return 0
        # time is updated in evaluate, this is called first.
        t = self.time_since_epoch + 1 
        x = self.chi_hat
        i = self.joins_since_epoch
        m = math.ceil(max(0, x*t - i))
        try:
            if self.verbose: print("n={} t={} x={} i={} m={}".format(n, t, x, i, m))
            # for one join, use plain entry formula
            if n == 1:
                return max(1, (i+n-1)/x*t)
            # indicates all entry costs are rounded up to 1
            if n <= m:
                return n
            # else calculate sum of entry costs
            return m + ((n-m)*i + np.sum(range(m + 1, n - 1)))/(x*t)
        except np.core._internal.AxisError:
            print("n={} t={} x={} i={} m={}".format(n, t, x, i, m))
            raise
    
    # helper functions
    def calc_chi_hat(self):
        return self.sym_diff / self.time_since_epoch
    
    def calc_entry_cost(self, current_joins):
        return current_joins/self.chi_hat*self.time_since_epoch
        
        
        
    