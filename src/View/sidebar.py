import os
import configparser
import json

import tkinter as tk
from tkinter import ttk



class SideBar(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, width=50, height=150, bg="blue")
        self.parent = parent
        self.tree = None
        self.console = None

        self.body()

    def body(self):

        # Profile Treeview
        self.tree = ttk.Treeview(self)

        # Load Profile Button
        subbutton = tk.Button(self, text="Laden", relief=tk.FLAT, width=30)

        # Console
        self.console = tk.Text(self, width=30, height=5)
        self.console.config(state=tk.DISABLED)
        
        # Pack Items
        self.tree.pack(fill="both", expand=True)
        subbutton.pack(fill="both")
        self.console.pack(side=tk.BOTTOM, fill="x")


    def insert_profiles_to_treeview(self):
        profiles = self.parent.controller.load_profiles()
        if profiles:
            for browser in profiles:
                parent = self.tree.insert('', "end",  text=browser)
                for profile in profiles[browser]:
                    self.tree.insert(parent, "end", text=profile)
        else:
            pass

        


    # Insert a message into the console
    def insert_message(self, message):
        message += "\n"
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.INSERT, message)
        self.console.config(state=tk.DISABLED)