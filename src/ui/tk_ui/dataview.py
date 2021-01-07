import tkinter as tk
from tkinter import ttk


class Dataview(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self)
        self.parent = parent

        self.body()


    def body(self):
        tree = ttk.Treeview(self)
        tree.insert('', 0, text='Item 1')
        tree.insert('', 'end', text='Item 2')

        id = tree.insert('', 5, text='Item 3')
        tree.insert(id, 0, text='sub-item 0')
        tree.insert(id, 1, text='sub-item 1')

        tree.pack(fill=tk.BOTH, expand=True)