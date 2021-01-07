import tkinter as tk

class Toolbar(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, bd=1, relief=tk.RAISED)
        self.parent = parent
        
        self.body()

    def body(self):

        exitButton = tk.Button(self, text="Beenden", relief=tk.FLAT, command=self.parent.quit)
        exitButton.pack(side=tk.LEFT, padx=2, pady=2)