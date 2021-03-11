import tkinter as tk

class MainMenu(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self)
        self.parent = parent
        self.body()

    def body(self):
        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Alle Änderungen speichern", command=self.parent.controller.commit_all_data)
        filemenu.add_command(label="Änderungen dieser Tabelle speichern", command=self.parent.controller.commit_selected_data)
        filemenu.add_command(label="Beenden", command=self.parent.quit)
        self.add_cascade(label="Datei", menu=filemenu)

        editmenu = tk.Menu(self, tearoff=0)
        editmenu.add_command(label="Undo")
        editmenu.add_command(label="Löschen")
        editmenu.add_command(label="Alle Daten editieren", command=self.parent.controller.edit_all_data)
        editmenu.add_command(label="Ausgewählte Daten editieren", command=self.parent.controller.edit_selected_data)
        editmenu.add_command(label="Dateisystem-Zeit anpassen", command=self.parent.controller.change_filesystem_time)
        editmenu.add_command(label="Dateisystem-Zeit zurücksetzten", command=self.parent.controller.rollback_filesystem_time)
        self.add_cascade(label="Bearbeiten", menu=editmenu)

        viewmenu = tk.Menu(self, tearoff=0)
        viewmenu.add_command(label="Historie", command=lambda: self.parent.controller.change_data_view("history"))
        viewmenu.add_command(label="Addons", command=lambda: self.parent.controller.change_data_view("addons"))
        viewmenu.add_command(label="Formular-Historie", command=lambda: self.parent.controller.change_data_view("formhistory"))
        viewmenu.add_command(label="Lesezeichen", command=lambda: self.parent.controller.change_data_view("bookmarks"))
        viewmenu.add_command(label="Extensions", command=lambda: self.parent.controller.change_data_view("extensions"))
        viewmenu.add_command(label="Session", command=lambda: self.parent.controller.change_data_view("session"))
        viewmenu.add_command(label="Profil", command=lambda: self.parent.controller.change_data_view("profile"))
        viewmenu.add_command(label="Keywords", command=lambda: self.parent.controller.change_data_view("keywords"))
        self.add_cascade(label="Ansicht", menu=viewmenu)

        helpmenu = tk.Menu(self, tearoff=0)
        helpmenu.add_command(label="Hilfe")
        helpmenu.add_command(label="Über...")
        self.add_cascade(label="Hilfe", menu=helpmenu)

