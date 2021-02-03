import tkinter as tk

class MainMenu(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self)
        self.parent = parent
        self.body()

    def body(self):
        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Speichern")
        filemenu.add_command(label="Beenden", command=self.parent.quit)
        self.add_cascade(label="Datei", menu=filemenu)

        editmenu = tk.Menu(self, tearoff=0)
        editmenu.add_command(label="Undo")
        editmenu.add_command(label="Löschen")
        editmenu.add_command(label="Alle auswählen")
        self.add_cascade(label="Bearbeiten", menu=editmenu)

        helpmenu = tk.Menu(self, tearoff=0)
        helpmenu.add_command(label="Hilfe")
        helpmenu.add_command(label="Über...")
        self.add_cascade(label="Hilfe", menu=helpmenu)