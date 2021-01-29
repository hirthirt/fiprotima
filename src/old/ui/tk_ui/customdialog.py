from tkinter import *


class CustomDialog(Toplevel):
    """Custom class to handle dialogs"""

    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)

        # Make dialog transient = on top of master, hidden together with master, dialog not in task bar
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        # Build dialog frame and buttons
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.grid(padx=5, pady=5)
        self.buttonbox()

        # When dialog visible, steal and keep focus from parent
        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx() + 5, parent.winfo_rooty() + 5))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        """Main dialog body, Override!"""
        pass

    def buttonbox(self):
        """Add Button Box below body"""

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.grid(row=0, column=0, padx=5, pady=5)
        w = Button(box, text="Abbrechen", width=10, command=self.cancel)
        w.grid(row=0, column=1, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid()

    def ok(self, event=None):
        """Handles ok button"""

        # Check if user entered valid data, if not, don't close
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        # Hide dialog, apply entered data and close dialog
        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        """Handles closing of dialog"""

        # Put focus back to main window and destroy dialog
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        """Validate from user entered data. Override!"""
        return True

    def apply(self):
        """Apply entered data, so that main window can grab the data. Override!"""
        pass
