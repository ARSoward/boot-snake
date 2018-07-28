import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as agg
import inspect
import csv 
import simulator
import algo
import attack
import dialog
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
        self.init_algos()
        # DEFAULT SIMULATION PARAMETERS
        self.define_algo(["sybil_control"])
        self.define_attack(alpha=1/10, size=3333, fractions=(1/2, 1))
        self.data = "newdatadist.pickle"
        self.root = master
        self.draw_window()
    
    def start(self):
        # create and run expt.
        self.results = []
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
            print('Error in simulation:', e)
            raise
        except FileNotFoundError as e:
            print('Unable to open data file', self.data)
        except Exception as e:
            print("There was an error:", e)
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
        results.get_tk_widget().pack(side=tk.LEFT)
        
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
            
    def data_dialog(self):
        window = dialog.dataDialog(self.root, self.data)
        self.data = window.data
        
    def init_algos(self):
        self.options = []
        for name, obj in inspect.getmembers(algo):
            if inspect.isclass(obj) and name is not "defense_algorithm": 
                self.options.append(name)
                
    def define_algo(self, selected):
        # dynamically create algo objects
        self.algos = []
        self.selected = selected
        for name in selected:
            if name in self.options: self.algos.append(getattr(algo, name)())
       
    def algo_dialog(self):
        w = dialog.algoDialog(self.root, self.options, self.selected)
        self.define_algo(w.selected)
        
    def define_attack(self, alpha, size, fractions):
        self.alpha = alpha
        self.size = size
        self.fractions=fractions
        self.attack = attack.burst(alpha, size, fractions) # attack after first 1/4
        
    def attack_dialog(self):
        w = dialog.attackDialog(self.root, self.alpha, self.size, self.fractions)
        self.define_attack(w.alpha, w.size, (w.start, w.end))
        
    def draw_window(self):
        self.root.title("BOOTS")
        self.root.configure(bg="#f4fffd")
        settings = tk.Frame(self.root, bg="#f4fffd")
        settings.grid(row=0, sticky="N")
        
        actions = tk.Frame(self.root, bg="#f4fffd")
        actions.grid(row=2, sticky="S")
        
        graph = tk.Frame(self.root, width=420, height=280, bg="#f4fffd")
        graph.grid(row=1)
        self.canvas = graph
    
        self.algo_b = tk.Button(settings, text="set algo", bg="#d9e2e1", command=self.algo_dialog)
        self.algo_b.grid(row=0, column=0, sticky=tk.E, padx=10)
        
        self.data_b = tk.Button(settings, text="set data", bg="#d9e2e1", command=self.data_dialog)
        self.data_b.grid(row=0, column=1, padx=10)
        
        self.attack_b = tk.Button(settings, text="set attack", bg="#d9e2e1", command=self.attack_dialog)
        self.attack_b.grid(row=0, column=2, sticky=tk.W, padx=10)
        
        self.start_b = tk.Button(actions, text="start simulation", bg="#d9e2e1", fg="#6ac417", command=self.start)
        self.start_b.grid(row=0, column=0, padx=10)
        
        self.export_b = tk.Button(actions, text="export", bg="#d9e2e1", fg="#42a1f4", command=self.export_results)
        self.export_b.grid(row=0, column=1, padx=10)
        
        
        self.quit_b = tk.Button(actions, text="quit", bg="#d9e2e1", fg="#c43117", command=self.root.quit)
        self.quit_b.grid(row=0, column=2, padx=10)
    
        
# running the gui
root = tk.Tk()
gui = gui(root)
root.mainloop()
root.destroy()
