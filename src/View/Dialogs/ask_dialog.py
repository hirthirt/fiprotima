import tkinter as tk


class AskDialog(tk.Toplevel):

    def __init__(self, parent, controller, text):
        tk.Toplevel.__init__(self, parent)
        self.title("Achtung!")
        self.resizable(0,0)
        
        self.controller = controller
        self.return_value = None
        
        tk.Label(self, text=text).pack(side=tk.TOP, pady=10, padx=10)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)

        self.ok_button = tk.Button(button_frame, text="OK", width=10, command=self.on_ok)
        self.cancle_button = tk.Button(button_frame, text="Abbrechen", width=10, command=self.on_cancle)
        
        self.ok_button.pack(side=tk.LEFT, padx=5)
        self.cancle_button.pack(side=tk.RIGHT, padx=5)

    def on_ok(self, event=None):
        self.return_value = True
        self.destroy()
        
    
    def on_cancle(self, event=None):
        self.return_value = False
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.return_value
        