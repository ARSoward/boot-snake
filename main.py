import tkinter as tk
import simulator
from algo.sybil_control import sybil_control
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
        frame = tk.Frame(master)
        frame.pack()
        
        self.hello = tk.Label(frame, text="there's a snake in my root!")
        self.hello.pack(side=tk.TOP)
        
        self.start_b = tk.Button(frame, text="test simulation", fg="green", command=self.start)
        self.start_b.pack(side=tk.LEFT)
        
        self.quit_b = tk.Button(frame, text="quit", fg="red", command=frame.quit)
        self.quit_b.pack(side=tk.RIGHT)
        
    def start(self):
        # instantiate algo. 
        # TODO: offer list from algo folder
        algorithm = sybil_control()
        # run expt. 
        # TODO: accept file name
        results = simulator.run("data.pickle",algorithm)
        # TODO: graph results
        # TODO: export results
        print("results: ", results)
        


root = tk.Tk()
gui = gui(root)
root.mainloop()
root.destroy()