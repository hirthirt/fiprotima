import tkinter as tk
from PIL import Image, ImageTk
from View.Dialogs.ask_dialog import AskDialog
from Model.util import resource_path

class Toolbar(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, bd=1, relief=tk.RAISED)
        self.parent = parent
        
        self.body()

    def body(self):

        img_first = Image.open(resource_path('View/icons/Exit_Icon.png'))
        exit_img = ImageTk.PhotoImage(img_first)

        img_sec = Image.open(resource_path('View/icons/Rollback_Icon.png'))
        rollback_img = ImageTk.PhotoImage(img_sec)

        img_third = Image.open(resource_path('View/icons/Safe_Icon.png'))
        safe_img = ImageTk.PhotoImage(img_third)

        exitButton = tk.Button(self, image=exit_img, relief=tk.FLAT, command=self.quit)
        exitButton.image = exit_img

        safeButton = tk.Button(self, image=safe_img, relief=tk.FLAT, command=self.parent.controller.commit_all_data)
        safeButton.image = safe_img

        rollbackButton = tk.Button(self, image=rollback_img, relief=tk.FLAT, command=self.parent.controller.rollback_all_data)
        rollbackButton.image = rollback_img
        load_profiles_button = tk.Button(self, text="Profile aktualisieren", relief=tk.FLAT, command=self.parent.sidebar.insert_profiles_to_treeview)


        exitButton.pack(side=tk.LEFT, padx=4, pady=2, fill="both")
        safeButton.pack(side=tk.LEFT, padx=4, pady=2, fill="both")
        rollbackButton.pack(side=tk.LEFT, padx=4, pady=2, fill="both")
        
        load_profiles_button.pack(side=tk.LEFT, padx=4, pady=2, fill="both")

    def quit(self):
        if self.parent.controller.get_unsaved_handlers():
            answer = AskDialog(self.parent, self.parent.controller, "Es wurden nicht alle Daten gespeichert!\n Trotzdem fortfahren?").show()
            if not answer:
                return
        answer = AskDialog(self.parent, self.parent.controller, "Möchten Sie wirklich beenden?").show()
        if not answer:
            return
        self.parent.destroy()
