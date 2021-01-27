import tkinter as tk
from tkinter import ttk


class Content(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, width=200, height=150)
        self.parent = parent
        self.dataview = None
        self.info = None

        self.body()
        self.fillData()


    def body(self):
        # Treeview for main data
        self.dataview = ttk.Treeview(self, height=15)

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

    def fillData(self):
        

        self.dataview['columns'] = ('size', 'modified')
        self.dataview.column('size', width=50, anchor='center')
        self.dataview.heading('size', text='Size')
        self.dataview.heading('modified', text='Modified')

        self.dataview.insert('', 0, 'apps', text='Applications', values=("127KB", "Yesterday"))
        self.dataview.insert('', 'end', 'widgets', text='Widgets', values=("12KB", "Last week"))
        self.dataview.insert('', 'end', text='Canvas', values=('25KB Today'))
        self.dataview.insert('apps', 'end', text='Browser', values=('115KB Yesterday'))
