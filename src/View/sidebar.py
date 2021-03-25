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
        self.tree = ttk.Treeview(self, selectmode="browse", height=25)

        # Load Profile Button
        subbutton = tk.Button(self, text="Laden", relief=tk.FLAT, width=30, command=self.load_profile)

        # Console
        self.console = tk.Text(self, width=30)
        self.console.config(state=tk.DISABLED)
        
        # Pack Items
        self.tree.pack(fill="both", expand=True)
        subbutton.pack(fill="both")
        self.console.pack(side=tk.BOTTOM, fill="x")


    def load_profile(self):
        selected = self.tree.focus()
        parent = self.tree.parent(selected)
        if self.tree.item(selected)["text"] in ["Firefox", "Chrome", "Edge"]:
            self.parent.controller.logger.error("Bitte Profil auswählen!")
            return
        if selected and parent and self.tree.item(selected):
            browser = self.tree.item(parent)["text"]
            profile_name = self.tree.item(selected)["text"]
            data = self.parent.controller.load_profile(browser, profile_name)
            if data and data != "keep":
                self.parent.content.fillHistroyData(data)
            elif data and data == "keep":
                return
            else:
                self.parent.content.fillHistroyData("None")

    def insert_profiles_to_treeview(self):
        for child in self.tree.get_children():
            self.tree.delete(child)

        profiles = self.parent.controller.load_profiles()
        if profiles:
            for browser in profiles:
                parent = self.tree.insert('', "end",  text=browser)
                for profile in profiles[browser]:
                    self.tree.insert(parent, "end", text=profile)
        else:
            pass
