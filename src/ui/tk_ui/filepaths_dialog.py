import os
import sys

from tkinter import *
from tkinter import messagebox, filedialog
from ui.tk_ui.customdialog import CustomDialog


class FilePathDialog(CustomDialog):
    """Dialog for user to enter profile and/or config path"""

    return_state: bool = False

    def __init__(self, parent, title=None):
        self.profile_path = StringVar(value="")
        self.cache_path = StringVar(value="")

        super().__init__(parent, title)

    def body(self, master):
        self.resizable(False, False)

        Label(master, text="Firefox Profil-Pfad").grid(row=0, sticky=W)
        Label(master, text="Firefox Cache-Pfad").grid(row=2, sticky=W)

        self.profile_entry = Entry(
            master, textvariable=self.profile_path, width=80, disabledforeground="black"
        )
        self.profile_entry.config(state=DISABLED)

        self.cache_entry = Entry(
            master, textvariable=self.cache_path, width=80, disabledforeground="black"
        )
        self.cache_entry.config(state=DISABLED)

        button_profile = Button(master, text="Profil-Ordner", command=self.open_profile_dialog)
        button_cache = Button(master, text="Cache-Ordner", command=self.open_cache_dialog)

        self.profile_entry.grid(row=1, column=0, columnspan=2)
        self.cache_entry.grid(row=3, column=0, columnspan=2)
        button_profile.grid(row=1, column=2)
        button_cache.grid(row=3, column=2)
        return self.profile_entry  # initial focus

    def open_path_dialog(self, variable, entry):
        """Opens tkinters ask-for-directory dialog"""
        path = filedialog.askdirectory()
        variable.set(path)

    # Helper methods because arguments are not possible in callbacks
    def open_profile_dialog(self, event=None):
        self.open_path_dialog(self.profile_path, self.profile_entry)

    def open_cache_dialog(self, event=None):
        self.open_path_dialog(self.cache_path, self.cache_entry)

    def cancel(self, event=None):
        """Asking, if dialog and therfore program should be closed, handles closing if needed"""
        quitbox = messagebox.askyesno("Programm beenden?", "Wollen sie das Programm beenden?")
        if quitbox:
            self.return_state = False
            self.parent.focus_set()
            self.destroy()

    def ok(self, event=None):
        """Overridig ok method because cancel-method kills the program"""
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()
        self.return_state = True

        self.parent.focus_set()
        self.destroy()

    def validate(self) -> bool:
        """Check if at least one path was entered and if paths are valid paths in system"""
        if self.cache_path.get() == "" and self.profile_path.get() == "":
            messagebox.showerror("Fehler", "Es wurde kein gültiger Pfad angegeben")
            return False
        if self.cache_path.get() != "" and not os.path.exists(self.cache_path.get()):
            messagebox.showerror("Fehler", "Kein gültiger Pfad für den Cache")
            self.cache_path.set("")
            return False
        if self.profile_path.get() != "" and not os.path.exists(self.profile_path.get()):
            messagebox.showerror("Fehler", "Kein gültiger Pfad für das Profil")
            self.profile_path.set("")
            return False
        return True  # override

    def apply(self):
        self.profile_path = self.profile_path.get()
        self.cache_path = self.cache_path.get()
