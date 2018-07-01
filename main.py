import tkinter as tk
import simulator
import algo
import attack
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:14:47 2018

@author: freya

inputs:
    n_initial (scalar, number of IDs in the network initially.)
    alpha (computational power of the adversary)
    new_arrival = arrival (??? passed to sybil stump)
    
    # 2 x n_initial list containing session time of initial IDs
    # used to generate list which is passed to both simulations
    initial_session_time = session_list
    

    new_session_time = session_new_list
    
    T (time, size of resulting ccost and sybil arrays)
    nat (probability of good ID joining???)
    s (scalar: time steps after which tests need to be performed )
    returns ccost 1,2 and sybil 1,2

# initialize list of IDs initally in the system
# is ids from initial_session_time's second row, w ones in top row
list = 2x n_initial array of ones
for each entry in list:
    list(i,2) = initial_session_time(i,2)

# the experiment
ccost1, sybil1 = simulation(n_initial, alpha, session_list, list, arrival, s, nat, T)
ccost2, sybil2 = sybilstump(n_initial, alpha, session_list, list, new_session_time, new_arrival, T, nat)

# build charts   
"""
class gui(object):
    def __init__(self, master):
        # can't start simulation until these have been defined
        self.algo = False
        self.attack = False
        self.data= False
        
        # set up window
        master.title("simulator")
        left = tk.Frame(master)
        left.pack(side=tk.LEFT)
        right = tk.Frame(master)
        right.pack(side=tk.RIGHT)
    
        self.hello = tk.Label(right, text="there's a snake in my root!")
        self.hello.pack(side=tk.TOP)
        
        self.algo_b = tk.Button(left, text="set algo", fg="green", command=self.define_algo)
        self.algo_b.pack(side=tk.TOP)
        
        self.data_b = tk.Button(left, text="set data", fg="green", command=self.define_data)
        self.data_b.pack(side=tk.TOP)
        
        self.attack_b = tk.Button(left, text="set attack", fg="green", command=self.define_attack)
        self.attack_b.pack(side=tk.TOP)
        
        self.start_b = tk.Button(right, text="start simulation", fg="green", command=self.start)
        self.start_b.pack(side=tk.TOP)
        
        self.quit_b = tk.Button(right, text="quit", fg="red", command=master.quit)
        self.quit_b.pack(side=tk.BOTTOM)
    
    def define_algo(self):
        # TODO accept input from user
        self.algo = algo.ccom()
        
    def define_data(self):
        # TODO accept file name
        self.data = "data.pickle"
    
    def define_attack(self):
        # TODO accept inut from user
        self.attack = attack.burst(1/10, 30)
        
    def start(self):
        # create and run expt.
        if not self.algo or not self.data or not self.attack:
            print("must define parameters")
            return
        try:
            sim = simulator.simulation(pickled_changes=self.data, algo=self.algo, attack=self.attack)
            results = sim.run(verbose=False)
            # TODO: graph results
            # TODO: export results
            print("results: ", results)
        except Exception as e:
            # TODO handle errors properly
            raise Exception(e)

# running the gui
root = tk.Tk()
gui = gui(root)
root.mainloop()
root.destroy()