import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as agg 
import simulator
import algo
import attack
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:14:47 2018

@author: freya
"""
class gui(object):
    def __init__(self, master):
        # can't start simulation until these have been defined
        self.algo1 = False
        self.algo2 = False
        self.attack = False
        self.data = False
        
        self.draw_window(master)
        
    def define_algo(self, algos):
        # TODO accept input from user: checkboxes
        self.algos = algos
        
        
    def define_data(self, data):
        # TODO accept file path/name
        self.data = data
    
    def define_attack(self, alpha, size, fractions):
        # TODO accept input from user: radio buttons
        # self.attack = attack.burst(alpha=1/4, attack_size=3333, interval_fractions=(1, 1)) # no attack
        self.attack = attack.burst(alpha, size, fractions) # attack after first 1/4

    def quick_start(self):
        self.define_data("small.pickle")
        self.define_data("newdatadist.pickle")
        self.define_algo([algo.ccom(), algo.sybil_control()])
        self.define_attack(alpha=1/10, size=3000, fractions=(1/2, 1))
        self.start()
    
    def start(self):
        # create and run expt.
        try:
            results = []
            for alg in self.algos:
                print("running {} simulation...".format(alg.name))
                sim = simulator.simulation(pickled_changes=self.data, algo=alg, attack=self.attack)
                sim.run(verbose=True)
                g_cost, b_cost = sim.get_cumulative_results()
                results.append({'data': g_cost, 'label': alg.name})
            results.append({'data': b_cost, 'label': 'cost to adversary'})
            self.plot_results(results)
            # TODO: export results
        except AttributeError as e:
            print('must define parameters')
        except FileNotFoundError as e:
            print('unable to open data file')
        except Exception as e:
            # TODO handle errors properly
            raise
    
    def plot_results(self, graphs):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_yscale('log')
        for graph in graphs:
            ax.plot(graph.get('data'), label=graph.get('label'))
        plt.legend()
        results = agg.FigureCanvasTkAgg(fig, master=self.canvas)
        results.draw()
        results.get_tk_widget().pack()
    
    def draw_window(self, master):
        master.title("BOOTS")
        
        settings = tk.Frame(master)
        settings.pack(side=tk.TOP)
        left = tk.Frame(settings)
        left.pack(side=tk.LEFT)
        right = tk.Frame(settings)
        right.pack(side=tk.RIGHT)
        
        graph = tk.Frame(master)
        graph.pack(side=tk.BOTTOM)
        self.canvas = graph
        
        
    
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
