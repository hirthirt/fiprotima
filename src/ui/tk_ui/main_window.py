from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from dateutil.relativedelta import relativedelta
from tksheet import Sheet

from ui.tk_ui.enterdate_dialog import EnterDateTimeDialog
from ui.tk_ui.profile_dialog import ProfileSelectionDialog

import controller as control


def make_table(num_rows, num_cols):
    """static helper function to build list in lists for the tables"""
    table = [[j for j in range(num_cols)] for i in range(num_rows)]
    return table


def make_table_from_dbclass(dbclass):
    """static helper function to get table from a class"""
    return make_table(len(dbclass.attr_names), len(dbclass.attr_names))


class MainWindow(Tk):
    """Main window class"""

    sheets = []
    table_data = []
    table_data_header = []
    data_lists = []
    sessions = []

    # If entering new day, month or year results in impossible date, rollback changes and skip
    # or just skip the faulty entry and continue with the other values
    rollback_skip_on_datetime_error: bool = True

    def __init__(self):
        Tk.__init__(self)
        self.title("FiProTiMa")
        self.protocol("WM_DELETE_WINDOW", self.popup_close_app)

        # Main Window
        self.body()

        # Get Paths from user
        if not self.popup_get_config():
            self.close()

        # Get Data from DBs
        self.get_data()

        # Create and fill tables:
        # Note: Pack seems better at getting a resizable UI in which elements fill the whole window.
        # Grid is a little bit clunky for that
        self.fill_tab_content(self.tabs_bar)
        self.tabs_bar.pack(expand=1, fill=BOTH)

        for sheet in self.sheets:
            sheet.pack(fill=BOTH, expand=1)

    # GUI
    def body(self):
        """Build body of main window"""
        main_separator = Frame(self, height=2, bd=1, relief=SUNKEN)

        # Button Bar
        frame_buttons = Frame(self)
        self.button_bar(frame_buttons)

        # Main Frame
        self.frame_table = Frame(self, borderwidth=1)
        self.frame_table.grid_columnconfigure(0, weight=1)
        self.frame_table.grid_rowconfigure(0, weight=1)

        # Tabs
        self.tabs_bar = ttk.Notebook(self.frame_table)

        # Build main window
        frame_buttons.pack(side=TOP, anchor=NW)
        main_separator.pack(fill=X, padx=5, pady=5)
        self.frame_table.pack(side=BOTTOM, anchor=S, fill=BOTH, expand=1)

    def button_bar(self, master):
        """Build buttons and add them to the button frame"""
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        button_profileswitch = Button(
            master, text="Profil wechseln", command=self.popup_switch_config
        )
        button_editmarked = Button(
            master, text="Markierte bearbeiten", command=self.popup_edit_single_cell
        )
        button_edit_all = Button(
            master, text="Alle Tabellen editieren", command=self.popup_edit_all_cells
        )
        button_changecommit = Button(master, text="Änderungen akzeptieren", command=self.submit)
        button_changediscard = Button(master, text="Änderungen verwerfen", command=self.cancel)
        button_quit = Button(master, text="Beenden", command=self.popup_close_app)

        button_profileswitch.pack(side=LEFT, anchor=NW)
        button_editmarked.pack(side=LEFT, anchor=N)
        button_edit_all.pack(side=LEFT, anchor=N)
        button_changecommit.pack(side=LEFT, anchor=NW)
        button_changediscard.pack(side=LEFT, anchor=N)
        button_quit.pack(side=LEFT, anchor=N)

    # Dialogs
    def popup_edit_all_cells(self, *args):
        """Open popup-dialog for user to enter date, apply to all tables"""
        dialog = EnterDateTimeDialog(self)
        row = 0
        col = 0

        # Try to apply changes to every date in every table
        for i, data_list in enumerate(self.data_lists):
            for j, data in enumerate(data_list):
                for k, attr in enumerate(data.attr_list):
                    highlight = "green"
                    # Skip non-date data
                    if attr.is_other():
                        continue

                    old_day = attr.value.day
                    old_month = attr.value.month
                    old_year = attr.value.year

                    if dialog.dirty:
                        if dialog.day is not None:
                            try:
                                attr.value = attr.value.replace(day=dialog.day)
                            except ValueError:
                                attr.value = attr.value.replace(day=old_day)
                                highlight = "yellow"
                                if self.rollback_skip_on_datetime_error:
                                    highlight = "red"
                                    continue

                        if dialog.month is not None:
                            try:
                                attr.value = attr.value.replace(month=dialog.month)
                            except ValueError:
                                attr.value = attr.value.replace(month=old_month)
                                highlight = "yellow"
                                if self.rollback_skip_on_datetime_error:
                                    attr.value = attr.value.replace(day=old_day)
                                    highlight = "red"
                                    continue

                        if dialog.year is not None:
                            try:
                                attr.value = attr.value.replace(year=dialog.year)
                            except ValueError:
                                attr.value = attr.value.replace(year=old_year)
                                highlight = "yellow"
                                if self.rollback_skip_on_datetime_error:
                                    attr.value = attr.value.replace(day=old_day)
                                    attr.value = attr.value.replace(month=old_month)
                                    hightlight = "red"
                                    continue

                        if dialog.hour is not None:
                            attr.value = attr.value.replace(hour=dialog.hour)
                        if dialog.minute is not None:
                            attr.value = attr.value.replace(minute=dialog.minute)
                        if dialog.second is not None:
                            attr.value = attr.value.replace(second=dialog.second)
                        if dialog.millisecond is not None:
                            attr.value = attr.value.replace(microsecond=(dialog.millisecond * 1000))
                        if dialog.microsecond is not None:
                            attr.value = attr.value.replace(microsecond=dialog.microsecond)

                        delta_microseconds = (
                            dialog.millisecond_diff * 1000
                        ) + dialog.microsecond_diff

                        # Relativdelta also works with months and years, timedelta only days
                        delta = relativedelta(
                            days=dialog.day_diff,
                            months=dialog.month_diff,
                            years=dialog.year_diff,
                            hours=dialog.hour_diff,
                            minutes=dialog.minute_diff,
                            seconds=dialog.second_diff,
                            microseconds=delta_microseconds,
                        )

                        attr.value = attr.value + delta

                        # Calculate date to timestamp and save it in data_source classes
                        attr.date_to_timestamp()
                        data.update()

                        self.sheets[i].highlight_cells(row=j, column=k, bg=highlight)

                self.fill_table()
                self.sheets[i].set_sheet_data(self.table_data[i][1:], verify=True, redraw=False)

    def popup_edit_single_cell(self, *args):
        """Open popup-dialog for user to enter date, apply only to marked rows or cells in single table"""

        # Get active table
        active_tab = self.tabs_bar.index(self.tabs_bar.select())
        sheet = self.sheets[active_tab]
        data_list = self.data_lists[active_tab]
        table_data = self.table_data[active_tab]
        table_data_header = self.table_data_header[active_tab]

        row = 0
        col = 0
        dialog = EnterDateTimeDialog(self)

        # Check if rows are marked. If not, get marked cells
        elements = []
        if sheet.get_selected_rows():
            for row in sheet.get_selected_rows():
                for i, column in enumerate(table_data_header):
                    elements.append(tuple((row, i)))
        else:
            elements = list(sheet.get_selected_cells())

        for element in elements:
            highlight = "green"
            row = element[0]
            col = element[1]
            obj = data_list[row]
            attr = obj.attr_list[col]

            # Skip non-date data
            if attr.is_other():
                continue

            old_day = attr.value.day
            old_month = attr.value.month
            old_year = attr.value.year

            if dialog.dirty:
                if dialog.day is not None:
                    try:
                        attr.value = attr.value.replace(day=dialog.day)
                    except ValueError:
                        attr.value = attr.value.replace(day=old_day)
                        highlight = "yellow"
                        if self.rollback_skip_on_datetime_error:
                            highlight = "red"
                            continue

                if dialog.month is not None:
                    try:
                        attr.value = attr.value.replace(month=dialog.month)
                    except ValueError:
                        attr.value = attr.value.replace(month=old_month)
                        highlight = "yellow"
                        if self.rollback_skip_on_datetime_error:
                            attr.value = attr.value.replace(day=old_day)
                            highlight = "red"
                            continue

                if dialog.year is not None:
                    try:
                        attr.value = attr.value.replace(year=dialog.year)
                    except ValueError:
                        attr.value = attr.value.replace(year=old_year)
                        highlight = "yellow"
                        if self.rollback_skip_on_datetime_error:
                            attr.value = attr.value.replace(day=old_day)
                            attr.value = attr.value.replace(month=old_month)
                            hightlight = "red"
                            continue

                if dialog.hour is not None:
                    attr.value = attr.value.replace(hour=dialog.hour)
                if dialog.minute is not None:
                    attr.value = attr.value.replace(minute=dialog.minute)
                if dialog.second is not None:
                    attr.value = attr.value.replace(second=dialog.second)
                if dialog.millisecond is not None:
                    attr.value = attr.value.replace(microsecond=(dialog.millisecond * 1000))
                if dialog.microsecond is not None:
                    attr.value = attr.value.replace(microsecond=dialog.microsecond)

                delta_microseconds = (dialog.millisecond_diff * 1000) + dialog.microsecond_diff
                delta = relativedelta(
                    days=dialog.day_diff,
                    months=dialog.month_diff,
                    years=dialog.year_diff,
                    hours=dialog.hour_diff,
                    minutes=dialog.minute_diff,
                    seconds=dialog.second_diff,
                    microseconds=delta_microseconds,
                )

                attr.value = attr.value + delta

                # Calculate date to timestamp and update data_source classes
                attr.date_to_timestamp()
                obj.update()

                sheet.highlight_cells(row=row, column=col, bg="green")

            self.fill_table()
            sheet.set_sheet_data(table_data[1:], verify=True)
            sheet.set_all_cell_sizes_to_text()

    def popup_get_config(self) -> bool:
        """Open popup to user to enter paths and apply to config"""
        dialog = ProfileSelectionDialog(self)
        if not dialog.return_state:
            return False

        profile_path = dialog.profile_path
        cache_path = dialog.cache_path

        control.set_paths(profile_path, cache_path)
        return True

    def popup_switch_config(self):
        """If user wants to switch config, clear data, open dialog, apply config and rebuild main window tables"""
        quitbox = messagebox.askokcancel(
            title="Verzeichnis ändern?",
            message="Wollen Sie die Verzeichnisse ändern? Nicht gespeicherte Änderungen gehen verloren!",
        )

        if quitbox:

            for sheet in self.sheets:
                # Delete tables, if left over bindings don't work in new tables
                sheet.disable_bindings()
                sheet.pack_forget()
                sheet = None

            # Clear tabs
            self.tabs_bar.pack_forget()

            # Rollback data and close connections
            control.undo()
            control.close()

            if self.popup_get_config():
                # Reinit data_source with new config and get data
                control.init()
                self.get_data()

                # Rebuild tabs and tables
                self.tabs_bar = ttk.Notebook(self.frame_table)
                self.fill_tab_content(self.tabs_bar)
                self.tabs_bar.pack(expand=1, fill=BOTH)

                for sheet in self.sheets:
                    sheet.pack(fill=BOTH, expand=1)
            else:
                self.close()

    def popup_close_app(self):
        """Confirm, if user wants to close program"""
        quitbox = messagebox.askokcancel(
            title="Anwendung beenden",
            message="Anwendung beenden? Nicht gespeicherte Änderungen gehen verloren!",
        )
        if quitbox:
            self.close()

    # Functions, interacting with controller
    def get_data(self):
        """Fetches data from controller, prepares tables and fill those tables with data"""
        control.init()

        self.data_lists = control.get_data_lists()

        self.table_names = control.get_source_names()
        self.table_data_header = control.get_data_headers()

        self.table_data = []
        for i, data in enumerate(self.table_names):
            self.table_data.append(
                make_table(
                    num_rows=len(self.data_lists[i]) + 1,
                    num_cols=len(self.table_data_header[i]) + 1,
                )
            )

        self.fill_table()

    def submit(self):
        """Send signal to controller to save data"""
        active_tab = self.tabs_bar.index(self.tabs_bar.select())
        name = self.table_names[active_tab]
        control.save()
        self.dehightlight_sheet()

    def cancel(self):
        """Send signal to controller to rollback data"""
        active_tab = self.tabs_bar.index(self.tabs_bar.select())
        name = self.table_names[active_tab]

        control.undo()

        control.reinit_list(self.data_lists)

        self.fill_table()
        self.dehightlight_sheet()

    def close(self):
        """Close the main window and program"""
        control.undo()
        control.close()
        self.destroy()
        sys.exit()

    # Functions, interaction with GUI
    def fill_tab_content(self, master):
        """Create tabs and tables and add them to notebool"""
        for i, name in enumerate(self.table_names):
            frame = ttk.Frame(master)
            master.add(frame, text=name)
            self.sheets.append(
                Sheet(
                    frame,
                    data=self.table_data[i][1:],
                    headers=self.table_data_header[i],
                    set_all_heights_and_widths=True,
                )
            )

            self.sheets[i].enable_bindings(
                (
                    "single_select",
                    "row_select",
                    "drag_select",
                    "column_drag_and_drop",
                    "column_width_resize",
                )
            )
            self.sheets[i].bind("<Double-Button-1>", self.popup_edit_single_cell)

    def fill_table(self):
        """Fill tables with data"""
        for i, list_ in enumerate(self.data_lists):
            for j, obj in enumerate(list_, start=1):
                self.table_data[i][j] = obj.get_value_list()

    def dehightlight_sheet(self):
        """Remove all highlights from table"""
        active_tab = self.tabs_bar.index(self.tabs_bar.select())
        self.sheets[active_tab].dehighlight_cells(row="all")
        self.sheets[active_tab].set_sheet_data(
            self.table_data[active_tab][1:], verify=True,
        )
