import os
import sys
import configparser

from tkinter import *
from tkinter import messagebox, filedialog
from ui.tk_ui.customdialog import CustomDialog
from config import configuration
import controller


class ProfileSelectionDialog(CustomDialog):
    """Dialog for user to enter profile and/or config path"""

    return_state: bool = False

    def __init__(self, parent, title=None):
        self.profile_path = StringVar(value="")
        self.cache_path = StringVar(value="")
        self.profile_name = StringVar(value="")

        super().__init__(parent, title)

    def body(self, master):
        self.resizable(False, False)

        button_firefox  = Button(master, text="Firefox", command=lambda: self.select_firefox(master) )
        button_chrome  = Button(master, text="Chrome", state=DISABLED, command=self.select_chrome )
        button_edge  = Button(master, text="Edge", state=DISABLED, command=self.select_edge )

        button_firefox.grid(row=0, column=0, padx=10, pady=10)
        button_chrome.grid(row=0, column=1, padx=10, pady=10)
        button_edge.grid(row=0, column=2, padx=10, pady=10)

        


    def select_firefox(self, master):
        for widget in master.winfo_children():
            widget.destroy()

        controller.set_browser("Firefox")
        config_parser = configparser.ConfigParser()
        if configuration.current_os == "Windows":
            path = "C:/Users/" + configuration.current_username + "/AppData/Roaming/Mozilla/Firefox/"
        elif configuration.current_os == "Linux":
            path = "/home/" + configuration.current_username + "/.mozilla/firefox/"
        config_parser.read(path + "profiles.ini")

        i = 0
        for section in config_parser.sections():
            if "Profile" in section:
                Radiobutton(master, text=config_parser[section].get("Name"), variable=self.profile_name, value=config_parser[section].get("Path")).grid(row=i, column=0)
                self.profile_name.set(config_parser[section].get("Name"))
                i += 1
        return

    def select_chrome(self):
        return

    def select_edge(self):
        return

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

        self.set_paths()

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()
        self.return_state = True

        self.parent.focus_set()
        self.destroy()

    def set_paths(self):
        if configuration.current_browser == "Firefox":
            if configuration.current_os == "Windows":
                self.profile_path.set("C:/Users/" + configuration.current_username + "/AppData/Roaming/Mozilla/Firefox/" + self.profile_name.get())
                self.cache_path.set("C:/Users/" + configuration.current_username  + "/AppData/Local/Mozilla/Firefox/" + self.profile_name.get())
            elif configuration.current_os == "Linux":
                self.profile_path.set("/home/" + configuration.current_username + "/.mozilla/firefox/" + self.profile_name.get())
                self.cache_path.set("/home/" + configuration.current_username  + "/.cache/mozilla/firefox/" + self.profile_name.get())


        elif configuration.current_browser == "Chrome":
            pass

        elif configuration.current_browser == "Edge":
            pass

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
