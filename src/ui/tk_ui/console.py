import tkinter as tk


class Console(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self)
        self.parent = parent
        self.textbox = None

        self.body()

    
    def body(self):
        self.textbox = tk.Text(self)
        self.textbox.pack(expand=True)

    def insert_message(self, message):
        message += "\n"
        self.textbox.insert(tk.INSERT, message)