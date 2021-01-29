import os
import configparser

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
        self.fillProfiles()

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

    #Load existing profiles into treeview
    def fillProfiles(self):
        firepath = None
        firecachepath = None
        chromepath = None
        edgepath = None

        if not configuration.current_username:
            self.insert_message("Kein Nutzername gefunden!")

        if configuration.current_os == "Windows":
            firepath = "C:/Users/" + configuration.current_username + "/AppData/Roaming/Mozilla/Firefox/"
            firecachepath = "C:/Users/" + configuration.current_username  + "/AppData/Local/Mozilla/Firefox/"
            edgepath = "C:/Users/" + configuration.current_username + "/AppData/Local/Microsoft/Edge/User Data"
            chromepath = "C:/Users/" + configuration.current_username + "/AppData/Local/Google/Chrome/User Data"
        elif configuration.current_os == "Linux":
            firepath = "/home/" + configuration.current_username + "/.mozilla/firefox/"
            firecachepath = "/home/" + configuration.current_username  + "/.cache/mozilla/firefox/"
            chromepath = "/home/" + configuration.current_username + "/.config/google-chrome/"
            edgepath = ""
            pass
        elif configuration.current_os == "Darwin":
            firepath = "Users/" + configuration.current_username + "/Library/Application Support/Firefox/"
            firecachepath = "Users/" + configuration.current_username + "/Library/Caches/Firefox/"
            chromepath = "Users/" + configuration.current_username + "/Library/Application Support/Google/Chrome"
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
            for file in os.listdir(chromepath):
                if ("Profile" in file) or ("Default" in file):
                    print(os.path.join("/mydir", file))
        else:
            self.insert_message("Chrome scheint nicht installiert zu sein!")
            pass

        if os.path.exists(edgepath):
            pass
        else:
            self.insert_message("Edge scheint nicht installiert zu sein!")
            pass
        
        print(self.profiledict)
    
    # Insert a message into the console
    def insert_message(self, message):
        message += "\n"
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.INSERT, message)
        self.console.config(state=tk.DISABLED)