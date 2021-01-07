import tkinter as tk
from tkinter import ttk

class Info(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self)
        self.parent = parent

        self.body()

    
    def body(self):
        tabControl = ttk.Notebook(self) 
  
        tab1 = ttk.Frame(tabControl) 
        tab2 = ttk.Frame(tabControl) 
        
        tabControl.add(tab1, text ='Cookies') 
        tabControl.add(tab2, text ='Formulare') 
        tabControl.pack(expand=True, fill=tk.BOTH) 
        
        ttk.Label(tab1,  
                text ="""Welcome to  
                GeeksForGeeks""").grid(column = 0,  
                                    row = 0, 
                                    padx = 30, 
                                    pady = 30)   
        ttk.Label(tab2, 
                text ="""Lets dive into the  
                world of computers""").grid(column = 0, 
                                            row = 0,  
                                            padx = 30, 
                                            pady = 30) 