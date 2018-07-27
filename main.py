import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as agg
import csv 
import simulator
import algo
import attack
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:14:47 2018

@author: Abigail Soward
A GUI for running one or more simulation. Has default parameters defined, or 
parameters can be set before running. After running, it plots and displays 
the results, and can export the result data to a CSV.
"""
class gui(object):
    def __init__(self, master):
        # DEFAULT SIMULATION PARAMETERS
        self.algos = [algo.dmcom(), algo.ccom()]
        self.attack = attack.burst(alpha=1/10, attack_size=3333, interval_fractions=(1/2, 1))
        self.data = "newdatadist.pickle"
        self.results = []
        
        self.draw_window(master)
        
    def define_algo(self, algos):
        # TODO accept input from user: checkboxes
        self.algos = algos
        
        
    def define_data(self, data):
        # TODO accept file path/name
        self.data = data
    
    def define_attack(self, alpha, size, fractions):
        # TODO accept input from user: radio buttons
        self.attack = attack.burst(alpha, size, fractions) # attack after first 1/4
    
    def start(self):
        # create and run expt.
        try:
            for alg in self.algos:
                print("running {} simulation...".format(alg.name))
                sim = simulator.simulation(pickled_changes=self.data, algo=alg, attack=self.attack)
                sim.run(verbose=False)
                g_cost, b_cost = sim.get_cumulative_results()
                self.results.append({'data': g_cost, 'label': alg.name+': cost to good ids'})
                self.results.append({'data': b_cost, 'label': alg.name+': cost to adversary'})
            self.plot_results()
        except AttributeError as e:
            print('Error in simulation: ', e)
            raise
        except FileNotFoundError as e:
            print('Unable to open data file ', self.data)
        except Exception as e:
            print("There was an error: ", e)
            raise
    
    def plot_results(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_yscale('log')
        for graph in self.results:
            ax.plot(graph.get('data'), label=graph.get('label'))
        plt.legend()
        results = agg.FigureCanvasTkAgg(fig, master=self.canvas)
        results.draw()
        results.get_tk_widget().pack()
        
    def export_results(self):
        with open('results.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            rows = []
            for graph in self.results:
                rows.append([graph.get('label')] + graph.get("data").tolist())
            rows = zip(*rows) # make rows into cols
            for row in rows:
                writer.writerow(row)
            csvfile.close()
    
    def draw_window(self, master):
        master.title("BOOTS")
        
        settings = tk.Frame(master)
        settings.pack(side=tk.TOP)      
        graph = tk.Frame(master)
        graph.pack(side=tk.BOTTOM)
        self.canvas = graph
    
        self.algo_b = tk.Button(settings, text="set algo", fg="green", command=self.define_algo)
        self.algo_b.pack(side=tk.LEFT)
        
        self.data_b = tk.Button(settings, text="set data", fg="green", command=self.define_data)
        self.data_b.pack(side=tk.LEFT)
        
        self.attack_b = tk.Button(settings, text="set attack", fg="green", command=self.define_attack)
        self.attack_b.pack(side=tk.LEFT)
        
        self.export_b = tk.Button(settings, text="export", fg="blue", command=self.export_results)
        self.export_b.pack(side=tk.LEFT)
        
        self.start_b = tk.Button(settings, text="start simulation", fg="green", command=self.start)
        self.start_b.pack(side=tk.LEFT)
        
        self.quit_b = tk.Button(settings, text="quit", fg="red", command=master.quit)
        self.quit_b.pack(side=tk.LEFT)
        

# running the gui
root = tk.Tk()
gui = gui(root)
root.mainloop()
root.destroy()
