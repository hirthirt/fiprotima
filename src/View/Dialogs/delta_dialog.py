import datetime
import tkinter as tk

from dateutil.relativedelta import *
from tkcalendar import DateEntry

class TimedeltaDialog(tk.Toplevel):

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.title("Änderung via Zeitverschiebung")
        self.resizable(0,0)
        
        self.controller = controller
        self.return_value = None
        self.mode = tk.IntVar() # 0 for backwards and 1 for forward
        
        self.labels = {
            "Jahre" : None,
            "Monate" : None,
            "Tage" : None,
            "Stunden" : None,
            "Minuten" : None,
            "Sekunden" : None
        }


        tk.Label(self, text="Zeitverscheibung auswählen:").pack(side=tk.TOP, pady=8)

        radio_frame = tk.Frame(self)
        radio_frame.pack(pady=3)

        tk.Radiobutton(radio_frame, text="Vor", value=1, variable=self.mode).pack(side=tk.LEFT, padx=4)
        back_button = tk.Radiobutton(radio_frame, text="Zurück", value=0, variable=self.mode)
        back_button.select()
        back_button.pack(side=tk.LEFT)

        values_frame = tk.Frame(self)
        values_frame.pack(pady=5)
        for label in self.labels:
            frame = tk.Frame(values_frame)
            frame.pack(side=tk.LEFT, padx=2)
            tk.Label(frame, text=label).pack(side=tk.LEFT)
            self.labels[label] = tk.Spinbox(frame, from_=0, to=99, width=5)
            self.labels[label].pack(side=tk.RIGHT, padx=2)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=5)

        self.ok_button = tk.Button(button_frame, text="OK", width=10, command=self.on_ok)
        self.cancle_button = tk.Button(button_frame, text="Abbrechen", width=10, command=self.on_cancle)
        
        self.ok_button.pack(side=tk.LEFT, padx=5)
        self.cancle_button.pack(side=tk.RIGHT, padx=5)

    def on_ok(self, event=None):
        if self.mode.get() == 0:
            self.return_value = relativedelta(
                        years=int(self.labels["Jahre"].get()),
                        months=int(self.labels["Monate"].get()),
                        days=int(self.labels["Tage"].get()),
                        hours=int(self.labels["Stunden"].get()),
                        minutes=int(self.labels["Minuten"].get()),
                        seconds=int(self.labels["Sekunden"].get())
                    )
        else:
            self.return_value = relativedelta(
                        years=int(self.labels["Jahre"].get())*(-1),
                        months=int(self.labels["Monate"].get())*(-1),
                        days=int(self.labels["Tage"].get())*(-1),
                        hours=int(self.labels["Stunden"].get())*(-1),
                        minutes=int(self.labels["Minuten"].get())*(-1),
                        seconds=int(self.labels["Sekunden"].get())*(-1)
                    )

        self.destroy()
        
    
    def on_cancle(self, event=None):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.return_value
        