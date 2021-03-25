import logging
import tkinter as tk
from datetime import datetime

class Console(logging.Handler):

    def __init__(self, textfield):
        logging.Handler.__init__(self)
        self.textfield = textfield
        self.textfield.config(state=tk.DISABLED)
        
        
        self.textfield.tag_config("INFO", foreground="black")
        self.textfield.tag_config("DEBUG", foreground="grey")
        self.textfield.tag_config("WARNING", foreground="orange")
        self.textfield.tag_config("ERROR", foreground="red")
        self.textfield.tag_config("CRITICAL", foreground="red", underline=1)
        

    
     # Insert a message into the console
    def emit(self, record):
        self.textfield.config(state=tk.NORMAL)

        time = datetime.now().strftime("%H:%M:%S")
        message = time + "\n" + self.format(record) + "\n\n"
        
        self.textfield.insert(tk.INSERT, message, record.levelname)
        self.textfield.see(tk.END)
        self.textfield.config(state=tk.DISABLED)