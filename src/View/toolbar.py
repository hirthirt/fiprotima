import tkinter as tk

class Toolbar(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, bd=1, relief=tk.RAISED)
        self.parent = parent
        
        self.body()

    def body(self):

        exitButton = tk.Button(self, text="Beenden", relief=tk.FLAT, command=self.parent.quit)
        load_profiles_button = tk.Button(self, text="Profile landen", relief=tk.FLAT, command=self.parent.sidebar.insert_profiles_to_treeview)
        form_history_button = tk.Button(self, text="FormHistory", relief=tk.FLAT, command=lambda: self.parent.content.change_data_view("formhistory"))
        history_button = tk.Button(self, text="History", relief=tk.FLAT, command=lambda: self.parent.content.change_data_view("history"))
        addons_button = tk.Button(self, text="Addons", relief=tk.FLAT, command=lambda: self.parent.content.change_data_view("addons"))
        bookmarks_button = tk.Button(self, text="Bookmarks", relief=tk.FLAT, command=lambda: self.parent.content.change_data_view("bookmarks"))


        exitButton.pack(side=tk.LEFT, padx=2, pady=2, fill="both")
        load_profiles_button.pack(side=tk.LEFT, padx=2, pady=2, fill="both")
        form_history_button.pack(side=tk.LEFT, padx=2, pady=2, fill="both")
        history_button.pack(side=tk.LEFT, padx=2, pady=2, fill="both")
        addons_button.pack(side=tk.LEFT, padx=2, pady=2, fill="both")
        bookmarks_button.pack(side=tk.LEFT, padx=2, pady=2, fill="both")