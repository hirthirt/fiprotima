
import datetime
import tkinter as tk

from dateutil.relativedelta import *
from tkcalendar import DateEntry

class DateDialog(tk.Toplevel):

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.title("Änderung via Datum")
        self.resizable(0,0)
        
        self.controller = controller
        self.return_value = None
        self.date = datetime.datetime.now()

        tk.Label(self, text="Datum auswählen:").pack(side=tk.TOP, pady=8)

        values_frame = tk.Frame(self)
        values_frame.pack(pady=4)

        self.calendar = DateEntry(
            values_frame,
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            locale="de_DE",
        )
        self.calendar.bind("<<DateEntrySelected>>", self.set_new_date)
        self.calendar.pack(pady=6)

        self.labels = {
            "Stunde" : None,
            "Minute" : None,
            "Sekunde" : None
        }

        for label in self.labels:
            frame = tk.Frame(values_frame)
            frame.pack(side=tk.LEFT, padx=2)
            tk.Label(frame, text=label).pack(side=tk.LEFT)
            if label == "Stunde":
                self.labels[label] = tk.Spinbox(frame, from_=0, to=23, width=5)
            else:
                self.labels[label] = tk.Spinbox(frame, from_=0, to=60, width=5)
            self.labels[label].pack(side=tk.RIGHT, padx=2)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)

        self.ok_button = tk.Button(button_frame, text="OK", width=10, command=self.on_ok)
        self.cancle_button = tk.Button(button_frame, text="Abbrechen", width=10, command=self.on_cancle)
        
        self.ok_button.pack(side=tk.LEFT, padx=5)
        self.cancle_button.pack(side=tk.RIGHT, padx=5)

    def set_new_date(self, e):
            self.date = self.calendar.get_date()

    def on_ok(self, event=None):
        self.return_value = datetime.datetime(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            hour=int(self.labels["Stunde"].get()), 
            minute=int(self.labels["Minute"].get()),
            second=int(self.labels["Sekunde"].get())
        )
        self.destroy()
        
    
    def on_cancle(self, event=None):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.return_value
        