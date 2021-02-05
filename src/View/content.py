import tkinter as tk
from tkinter import ttk

from datetime import datetime

class Content(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, width=200, height=150)
        self.parent = parent
        self.dataview = None
        self.info = None
        self.dataview_mode = "history"

        self.body()


    def body(self):
        # Treeview for main data
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        self.dataview = ttk.Treeview(self, height=15, style="mystyle.Treeview")

        tabControl = ttk.Notebook(self) 
  
        tab1 = ttk.Frame(tabControl) 
        tab2 = ttk.Frame(tabControl) 
        
        tabControl.add(tab1, text ='Cookies') 
        tabControl.add(tab2, text ='Formulare')


        self.dataview.pack(expand=True, fill="both")
        tabControl.pack(side=tk.BOTTOM, expand=True, fill="both") 
        

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

    def fillHistroyData(self, history_data):
        for child in self.dataview.get_children():
            self.dataview.delete(child)

        self.dataview["columns"]=("id","visit","l_visit","object")
        self.dataview["displaycolumns"] = ("id","visit","l_visit")
        self.dataview.heading("#0",text="URL",anchor=tk.W)
        self.dataview.heading("id", text="ID",anchor=tk.W)
        self.dataview.heading("visit", text="Besucht",anchor=tk.W)
        self.dataview.heading("l_visit", text="Letzter Besuch",anchor=tk.W)

        for entry in history_data:
            v_date = None
            lv_date = None
            for attr in entry.attr_list:
                if attr.name == "Zuletzt besucht":
                    lv_date = attr.value.strftime("%d.%m.%Y %H:%M")
                elif attr.name == "Besucht am":
                    v_date = attr.value.strftime("%d.%m.%Y %H:%M")
            parent = self.dataview.insert("", "end",  text=entry.place.url, tags=("bg"), values=(entry.id,v_date,lv_date, entry))
            if history_data[entry]:
                for sube in history_data[entry]:
                    v_date = None
                    lv_date = None
                    for attr in entry.attr_list:
                        if attr.name == "Zuletzt besucht":
                            lv_date = attr.value.strftime("%d.%m.%Y %H:%M")
                        elif attr.name == "Besucht am":
                            v_date = attr.value.strftime("%d.%m.%Y %H:%M")
                    self.dataview.insert(parent, "end",  text=sube.place.url, values=(sube.id,v_date,lv_date, sube))
        
        self.dataview.tag_configure('bg', background='#DFDFDF')