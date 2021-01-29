import tkinter as tk
from tkinter import ttk

from View.menu import MainMenu
from View.toolbar import Toolbar
from View.sidebar import SideBar
from View.content import Content

class View(tk.Tk):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.menu = None
        self.toolbar = None
        self.sidebar = None
        self.content = None

        self.body()

    
    def main(self):
        self.mainloop()

    def body(self):      
        self.content = Content(self)
        self.sidebar = SideBar(self)
        self.menu = MainMenu(self)
        self.toolbar = Toolbar(self)
        
        self.config(menu=self.menu)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="we")
        self.sidebar.grid(row=1, column=0, sticky="ns")
        self.content.grid(row=1, column=1, sticky="wens")

        self.sidebar.insert_message("Fertig geladen...")
        self.sidebar.insert_message("Legen Sie los!")