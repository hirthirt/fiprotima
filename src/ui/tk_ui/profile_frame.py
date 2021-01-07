import tkinter as tk


class Profileframe(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self)
        self.parent = parent

        self.body()

    def body(self):
        text = tk.Text(self)
        text.pack(expand=True)