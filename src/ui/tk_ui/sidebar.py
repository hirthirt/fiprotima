import os
import configparser
import json

import tkinter as tk
from tkinter import ttk
from config import configuration



class SideBar(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, width=50, height=150, bg="blue")
        self.parent = parent
        self.tree = None
        self.console = None
        self.profiledict = {}

        self.body()
        self.insert_profiles_to_treeview()

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
        self.search_profiles()
        for browser in self.profiledict:
            parent = self.tree.insert('', "end",  text=browser)
            for profile in self.profiledict[browser]:
                self.tree.insert(parent, "end", text=profile) 
        



    #This searches for installations of Firefox, Edge and Chrome
    #Then stores the profiles of them to the profiledict
    def search_profiles(self):
        firepath = None
        firecachepath = None
        chromepath = None
        edgepath = None

        if not configuration.current_username:
            self.insert_message("Kein Nutzername gefunden!")

        if configuration.current_os == "Windows":
            firepath = "C:/Users/" + configuration.current_username + "/AppData/Roaming/Mozilla/Firefox/"
            firecachepath = "C:/Users/" + configuration.current_username  + "/AppData/Local/Mozilla/Firefox/"
            edgepath = "C:/Users/" + configuration.current_username + "/AppData/Local/Microsoft/Edge/User Data/"
            chromepath = "C:/Users/" + configuration.current_username + "/AppData/Local/Google/Chrome/User Data/"
        elif configuration.current_os == "Linux":
            firepath = "/home/" + configuration.current_username + "/.mozilla/firefox/"
            firecachepath = "/home/" + configuration.current_username  + "/.cache/mozilla/firefox/"
            chromepath = "/home/" + configuration.current_username + "/.config/google-chrome/"
            edgepath = ""
            pass
        elif configuration.current_os == "Darwin":
            firepath = "Users/" + configuration.current_username + "/Library/Application Support/Firefox/"
            firecachepath = "Users/" + configuration.current_username + "/Library/Caches/Firefox/"
            chromepath = "Users/" + configuration.current_username + "/Library/Application Support/Google/Chrome/"
            edgepath = ""
        else:
            self.insert_message("Kein kompatibles OS gefunden!")
            return
        
        if os.path.exists(firepath):
            self.profiledict["Firefox"] = {}
            config_parser = configparser.ConfigParser()
            config_parser.read(firepath + "profiles.ini")

            for section in config_parser.sections():
                if "Profile" in section:
                    self.profiledict["Firefox"][config_parser[section].get("Name")] = [firepath + config_parser[section].get("Path")]
                    if os.path.exists(firecachepath):
                        self.profiledict["Firefox"][config_parser[section].get("Name")].append(firecachepath + config_parser[section].get("Path"))
                    
            
        else:
            self.insert_message("Firefox scheint nicht installiert zu sein!")
            pass

        if os.path.exists(chromepath):
            self.profiledict["Chrome"] = {}
            for file in os.listdir(chromepath):
                if ("Profile" in file) or ("Default" in file):
                    path = chromepath + file 
                    if os.path.isfile(path + "/Preferences"):
                        data = json.load(open(path + "/Preferences", "r"))
                        if data["profile"]["name"]:
                            self.profiledict["Chrome"][data["profile"]["name"]] = path
                        else:
                            self.profiledict["Chrome"][file] = path
                    else:
                        self.insert_message("Preferences-Datei wurde nicht gefunden!")
            if not self.profiledict["Chrome"]:
                self.insert_message("Keine Profile für Chrome gefunden")
        else:
            self.insert_message("Chrome scheint nicht installiert zu sein!")
            pass

        if os.path.exists(edgepath):
            self.profiledict["Edge"] = {}
            for file in os.listdir(edgepath):
                if ("Profile" in file) or ("Default" in file):
                    path = edgepath + file 
                    if os.path.isfile(path + "/Preferences"):
                        data = json.load(open(path + "/Preferences", "r"))
                        if data["profile"]["name"]:
                            self.profiledict["Edge"][data["profile"]["name"]] = path
                        else:
                            self.profiledict["Edge"][file] = path
                    else:
                        self.insert_message("Preferences-Datei wurde nicht gefunden!")
            if not self.profiledict["Edge"]:
                self.insert_message("Keine Profile für Edge gefunden")
        else:
            self.insert_message("Edge scheint nicht installiert zu sein!")
            pass
    


    # Insert a message into the console
    def insert_message(self, message):
        message += "\n"
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.INSERT, message)
        self.console.config(state=tk.DISABLED)