#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
Copyright © 1995-2014 by Fredrik Lundh

By obtaining, using, and/or copying this software and/or its associated documentation, you agree that you have read, understood, and will comply with the following terms and conditions:

Permission to use, copy, modify, and distribute this software and its associated documentation for any purpose and without fee is hereby granted, provided that the above copyright notice appears in all copies, and that both that copyright notice and this permission notice appear in supporting documentation, and that the name of Secret Labs AB or the author not be used in advertising or publicity pertaining to distribution of the software without specific, written prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import tkinter as tk
import tkinter.filedialog

class dialog(tk.Toplevel):

    def __init__(self, parent, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w =tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override
        
        
class attackDialog(dialog):
    def __init__(self, master, alpha, size, intervals):
        self.alpha = alpha
        self.size = size
        self.start, self.end = intervals
        super().__init__(master, "set attack parameters")

    def body(self, master):
        
        tk.Label(master, text="Alpha:").grid(row=0)
        tk.Label(master, text="Attack Size:").grid(row=1)
        tk.Label(master, text="Attack start and end intervals:").grid(row=2)

        self.alpha_entry = tk.Entry(master)
        self.alpha_entry.insert(tk.END, self.alpha)
        self.alpha_entry.grid(row=0, column=1)
        
        self.size_entry = tk.Entry(master)
        self.size_entry.insert(tk.END, self.size)
        self.size_entry.grid(row=1, column=1)
        
        self.start_entry = tk.Entry(master)
        self.start_entry.insert(tk.END, self.start)
        self.start_entry.grid(row=2, column=1)
        
        self.end_entry = tk.Entry(master)
        self.end_entry.insert(tk.END, self.end)
        self.end_entry.grid(row=2, column=2)
        
        return self.alpha_entry # initial focus

    def validate(self):
        if not self.alpha: return False
        return True
        
    def apply(self):
        self.alpha = float(self.alpha_entry.get())
        self.size = float(self.size_entry.get())
        self.start = float(self.start_entry.get())
        self.end = float(self.end_entry.get())
        
class dataDialog(dialog):
    def __init__(self, master, value):
        self.data = value
        super().__init__(master, "select pickle file")

    def body(self, master):
        self.data_entry = tk.Entry(master)
        self.data_entry.insert(0, self.data)
        self.data_entry.pack()
        self.button = tk.Button(self, text="browse", command=self.open_file)
        self.button.pack()
        
        return self.data_entry # initial focus
    
    def open_file(self):
        self.data = tk.filedialog.askopenfile().name
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0,self.data)
        
    def validate(self):
        if not self.data_entry: return False
        return True
        
    def apply(self):
        self.data = str(self.data_entry.get())
        
class algoDialog(dialog):
    def __init__(self, master, options, selected):
        self.options = options
        self.selected = selected
        self.vars = {}
        super().__init__(master, "select algorithms")

    def body(self, master):
        row = 0
        for option in self.options:
            row += 1
            self.vars[option] = tk.BooleanVar()
            self.vars[option].set(1) if option in self.selected else self.vars[option].set(0)
            tk.Checkbutton(master, text=option, variable=self.vars.get(option)).grid(row=row, sticky="W")
        
    def validate(self):
        for key in self.vars:
            if self.vars[key].get(): return True
        return False
        
    def apply(self):
        selected = []
        for key in self.vars:
            if self.vars[key].get(): 
                selected.append(key)
        self.selected = selected
            
            