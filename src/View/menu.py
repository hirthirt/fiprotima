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

        viewmenu = tk.Menu(self, tearoff=0)
        viewmenu.add_command(label="Historie", command=lambda: self.parent.content.change_data_view("history"))
        viewmenu.add_command(label="Addons", command=lambda: self.parent.content.change_data_view("addons"))
        viewmenu.add_command(label="Formular-Historie", command=lambda: self.parent.content.change_data_view("formhistory"))
        viewmenu.add_command(label="Lesezeichen", command=lambda: self.parent.content.change_data_view("bookmarks"))
        self.add_cascade(label="Ansicht", menu=viewmenu)

        helpmenu = tk.Menu(self, tearoff=0)
        helpmenu.add_command(label="Hilfe")
        helpmenu.add_command(label="Über...")
        self.add_cascade(label="Hilfe", menu=helpmenu)