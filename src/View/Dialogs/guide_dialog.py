import tkinter as tk

from Model.util import resource_path

class GuideDialog(tk.Toplevel):

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.title("Nutzerhandbuch")
        self.resizable(0,0)
        
        self.controller = controller

        self.text_frame = tk.Frame(self, width=130)
        self.text = tk.Text(self.text_frame, width=130)
        self.text.config(state=tk.DISABLED)
        self.text.pack()
        self.text_frame.pack(side=tk.TOP)
        self.file_to_text()

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)

        self.ok_button = tk.Button(button_frame, text="OK", width=15, command=self.on_ok)
        
        self.ok_button.pack()


    def on_ok(self, event=None):
        self.destroy()
        

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        
    def file_to_text(self):
        text = u""
        self.text.config(state=tk.NORMAL)
        guide = open(resource_path("View/text/guide.txt"), "r")
        for line in guide.readlines():
            text += line
        self.text.insert(tk.INSERT, text)
        self.text.config(state=tk.DISABLED)