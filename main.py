import tkinter as tk
import matplotlib.pyplot as plt
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
        self.algo1 = False
        self.algo2 = False
        self.attack = False
        self.data= False
        
        self.draw_window(master)
        
    
    def define_algo(self):
        # TODO accept input from user
        self.algo1 = algo.ccom()
        self.algo2 = algo.sybil_control()
        
        
    def define_data(self):
        # TODO accept file name
        self.data= "small.pickle"
        self.data = "newdatadist.pickle"
    
    def define_attack(self):
        # TODO accept input from user
        # self.attack = attack.burst(alpha=1/4, attack_size=3333, interval_fractions=(1, 1)) # no attack
        self.attack = attack.burst(alpha=1/4, attack_size=3333, interval_fractions=(1/2, 1)) # attack after first 1/4

    def quick_start(self):
        self.define_data()
        self.define_algo()
        self.define_attack()
        self.start()
    
    def start(self):
        # create and run expt.
        if not self.algo1 or not self.data or not self.attack:
            print("must define parameters")
            return
        try:
            print("running {} simulation...".format(self.algo1.name))
            sim = simulator.simulation(pickled_changes=self.data, algo=self.algo1, attack=self.attack)
            sim.run(verbose=True)
            
            if self.algo2:
                print("running {} simulation...".format(self.algo2.name))
                sim2 = simulator.simulation(pickled_changes=self.data, algo=self.algo2, attack=self.attack)
                sim2.run(verbose=True)
                sim1cost, bad = sim.get_cumulative_results()
                sim2cost, bad = sim2.get_cumulative_results()
                self.plot_results(data=[sim1cost, sim2cost, bad], labels=[self.algo1.name, self.algo2.name, "cost to adversary"])
                
            else:  
                self.plot_results(data=sim.get_changes(), labels=["symmetric difference","net changes"])
                self.plot_results(data=sim.get_cumulative_results(), labels=[self.algo1.name, "cost to adversary"])
            # TODO: export results
        except Exception as e:
            # TODO handle errors properly
            raise
    
    # TODO accept 1 or more data,label pairs
    def plot_results(self, data, labels):
        line1, line2, line3 = data
        label1, label2, label3 = labels
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(line1, label=label1)
        ax.plot(line2, label=label2)
        ax.plot(line3, label=label3)
        ax.set_yscale('log')
        plt.legend()
        plt.show()
    
    def draw_window(self, master):
        master.title("BOOTS")
        left = tk.Frame(master)
        left.pack(side=tk.LEFT)
        right = tk.Frame(master)
        right.pack(side=tk.RIGHT)
    
        self.algo_b = tk.Button(left, text="set algo", fg="green", command=self.define_algo)
        self.algo_b.pack(side=tk.TOP)
        
        self.data_b = tk.Button(left, text="set data", fg="green", command=self.define_data)
        self.data_b.pack(side=tk.TOP)
        
        self.attack_b = tk.Button(left, text="set attack", fg="green", command=self.define_attack)
        self.attack_b.pack(side=tk.TOP)
        
        self.quick_b = tk.Button(right, text="quick start", fg="yellow", command=self.quick_start)
        self.quick_b.pack(side=tk.TOP)
        
        self.start_b = tk.Button(right, text="start simulation", fg="green", command=self.start)
        self.start_b.pack(side=tk.TOP)
        
        self.quit_b = tk.Button(right, text="quit", fg="red", command=master.quit)
        self.quit_b.pack(side=tk.BOTTOM)
        

# running the gui
root = tk.Tk()
gui = gui(root)
root.mainloop()
root.destroy()