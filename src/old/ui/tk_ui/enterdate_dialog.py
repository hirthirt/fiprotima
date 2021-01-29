from datetime import datetime
from tkinter import *
from tkinter import messagebox


from tkcalendar import DateEntry

from ui.tk_ui.customdialog import CustomDialog


class EnterDateTimeDialog(CustomDialog):
    """Dialog popup where the user can enter fixed time or relative time"""

    class TimeAttribute:
        """Helper class to make handling of datetime a little bit easier"""

        def __init__(self, value, temp=None, old=None, dirt=0):
            self.value = value
            self.dirty = IntVar(value=dirt)

            self.temp = temp if temp is not None else value
            self.old = old if old is not None else value

    def __init__(self, parent, title=None):
        parent.resizable(False, False)

        # Init fixed date and time
        now = datetime.now()
        self.date = self.TimeAttribute(now)
        self.day = self.TimeAttribute(StringVar(value=str(now.day).zfill(2)))
        self.month = self.TimeAttribute(StringVar(value=str(now.month).zfill(2)))
        self.year = self.TimeAttribute(StringVar(value=str(now.year).zfill(2)))
        self.hour = self.TimeAttribute(StringVar(value=str(now.hour).zfill(2)))
        self.minute = self.TimeAttribute(StringVar(value=str(now.minute).zfill(2)))
        self.second = self.TimeAttribute(StringVar(value=str(now.second).zfill(2)))
        self.millisecond = self.TimeAttribute(StringVar(value=str(0).zfill(3)), old=0)
        self.microsecond = self.TimeAttribute(StringVar(value=str(0).zfill(3)), old=0)

        # Init relative date and time
        self.day_diff = self.TimeAttribute(StringVar(value=0), temp=0)
        self.month_diff = self.TimeAttribute(StringVar(value=0), temp=0)
        self.year_diff = self.TimeAttribute(StringVar(value=0), temp=0)
        self.hour_diff = self.TimeAttribute(StringVar(value=0), temp=0)
        self.minute_diff = self.TimeAttribute(StringVar(value=0), temp=0)
        self.second_diff = self.TimeAttribute(StringVar(value=0), temp=0)
        self.millisecond_diff = self.TimeAttribute(StringVar(value=0), temp=0)
        self.microsecond_diff = self.TimeAttribute(StringVar(value=0), temp=0)

        self.mode = IntVar(value=0)

        self.dirty = False

        self.current_row = 0
        self.current_col = 0

        super().__init__(parent, title)

    def col(self, set_to: int = None):
        """Helper function to automate handling of grid-column"""
        if set_to is not None:
            self.current_col = set_to
        self.current_col = self.current_col + 1
        return self.current_col

    def row(self, new_row: bool = False, reset: bool = False):
        """Helper function to automate handling of grid-row"""
        if new_row:
            self.current_row = self.current_row + 1
            self.current_col = 0
        if reset:
            self.current_col = 0
            self.current_row = 0
        return self.current_row

    def set_new_date(self, e):
        self.date.value = self.calendar.get_date()

    def body(self, master):

        frame_fixeddate = LabelFrame(master, text="Festes Datum")
        frame_datediff = LabelFrame(master, text="Zeitdifferenz festlegen")

        # Row: Enter day, month and/or hour
        frame_fixeddate_date = Frame(frame_fixeddate)

        Radiobutton(frame_fixeddate_date, variable=self.mode, value=0).grid(sticky=W, row=0)
        Checkbutton(frame_fixeddate_date, variable=self.day.dirty).grid(
            row=self.row(reset=True), column=self.col(), sticky=E
        )
        day_entry = Spinbox(
            frame_fixeddate_date,
            width=2,
            textvariable=self.day.value,
            from_=0,
            to=31,
            wrap=True,
            format="%02.0f",
        )
        self.day.value.trace("w", self.validate_day)
        day_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_fixeddate_date, text="Tag").grid(row=self.row(), column=self.col())

        Checkbutton(frame_fixeddate_date, variable=self.month.dirty).grid(
            row=self.row(), column=self.col(), sticky=E
        )
        month_entry = Spinbox(
            frame_fixeddate_date,
            width=2,
            textvariable=self.month.value,
            from_=0,
            to=31,
            wrap=True,
            format="%02.0f",
        )
        self.day.value.trace("w", self.validate_day)
        month_entry.grid(row=self.row(), column=self.col())
        Label(frame_fixeddate_date, text="Monat").grid(row=self.row(), column=self.col(), sticky=W)

        Checkbutton(frame_fixeddate_date, variable=self.year.dirty).grid(
            row=self.row(), column=self.col(), sticky=E
        )
        year_entry = Spinbox(
            frame_fixeddate_date,
            width=4,
            textvariable=self.year.value,
            from_=0,
            to=9999,
            wrap=True,
            format="%04.0f",
        )
        self.day.value.trace("w", self.validate_day)
        year_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_fixeddate_date, text="Jahr").grid(row=self.row(), column=self.col())

        # Row: Note to User, use on or the other
        frame_fixeddate_label = Frame(frame_fixeddate)
        Label(frame_fixeddate_label, text="Oder").grid(
            row=self.row(reset=True), column=self.col(1), columnspan=3, sticky=W
        )

        # Row: Enter date with calendar widget
        frame_fixeddate_date_widget = Frame(frame_fixeddate)

        Radiobutton(frame_fixeddate_date_widget, variable=self.mode, value=1).grid(sticky=W, row=0)
        self.calendar = DateEntry(
            frame_fixeddate_date_widget,
            year=self.date.value.year,
            month=self.date.value.month,
            day=self.date.value.day,
            locale="de_DE",
        )
        self.calendar.bind("<<DateEntrySelected>>", self.set_new_date)
        self.calendar.grid(row=self.row(), column=self.col(), sticky=W, columnspan=20, pady=5)

        # Row: Enter hour, minute, second
        frame_fixeddate_time = Frame(frame_fixeddate)

        Checkbutton(frame_fixeddate_time, variable=self.hour.dirty).grid(
            row=self.row(reset=True), column=self.col(), sticky=E
        )
        hour_entry = Spinbox(
            frame_fixeddate_time,
            width=2,
            textvariable=self.hour.value,
            from_=0,
            to=23,
            wrap=True,
            format="%02.0f",
        )
        self.hour.value.trace("w", self.validate_hour)
        hour_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_fixeddate_time, text="Stunde").grid(row=self.row(), column=self.col(), sticky=W)

        Checkbutton(frame_fixeddate_time, variable=self.minute.dirty).grid(
            row=self.row(), column=self.col(), sticky=E
        )
        minute_entry = Spinbox(
            frame_fixeddate_time,
            width=2,
            textvariable=self.minute.value,
            from_=0,
            to=59,
            wrap=True,
            format="%02.0f",
        )
        self.minute.value.trace("w", self.validate_minute)
        minute_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_fixeddate_time, text="Minute").grid(row=self.row(), column=self.col(), sticky=W)

        Checkbutton(frame_fixeddate_time, variable=self.second.dirty).grid(
            row=self.row(), column=self.col(), sticky=E
        )
        second_entry = Spinbox(
            frame_fixeddate_time,
            width=2,
            textvariable=self.second.value,
            from_=0,
            to=59,
            wrap=True,
            format="%02.0f",
        )
        self.second.value.trace("w", self.validate_second)
        second_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_fixeddate_time, text="Sekunde").grid(
            row=self.row(), column=self.col(), sticky=W
        )

        # Row: Enter microsecond
        frame_fixeddate_micro = Frame(frame_fixeddate)

        Checkbutton(frame_fixeddate_micro, variable=self.millisecond.dirty).grid(
            row=self.row(reset=True), column=self.col(), sticky=E
        )
        milli_entry = Spinbox(
            frame_fixeddate_micro,
            width=3,
            textvariable=self.millisecond.value,
            from_=0,
            to=999,
            wrap=True,
            format="%03.0f",
        )
        self.millisecond.value.trace("w", self.validate_millisecond)
        milli_entry.grid(row=self.row(), column=self.col(), columnspan=2, sticky=W, pady=5)
        Label(frame_fixeddate_micro, text="Millisekunden").grid(
            row=self.row(), column=self.col(5), columnspan=1, sticky=W, pady=5
        )

        Label(frame_fixeddate_micro, text="Hinweis: Wird nicht für alle Daten umgesetzt").grid(
            row=self.row(), column=self.col(6), sticky=N, rowspan=2
        )

        Checkbutton(frame_fixeddate_micro, variable=self.microsecond.dirty).grid(
            row=self.row(new_row=True), column=self.col(), sticky=E
        )
        micro_entry = Spinbox(
            frame_fixeddate_micro,
            width=3,
            textvariable=self.microsecond.value,
            from_=0,
            to=999,
            wrap=True,
            format="%03.0f",
        )
        self.microsecond.value.trace("w", self.validate_microsecond)
        micro_entry.grid(row=self.row(), column=self.col(), columnspan=2, sticky=W, pady=5)
        Label(frame_fixeddate_micro, text="Mikrosekunden").grid(
            row=self.row(), column=self.col(5), columnspan=1, sticky=W, pady=5
        )

        # Row: Enter day diff, month diff and/or year diff
        frame_datediff_date = Frame(frame_datediff)

        day_diff_entry = Spinbox(
            frame_datediff_date, width=3, textvariable=self.day_diff.value, from_=-999, to=999
        )
        self.day_diff.value.trace("w", self.validate_day_diff)
        day_diff_entry.grid(row=self.row(reset=True), column=self.col(), sticky=W)
        Label(frame_datediff_date, text="Tage").grid(row=self.row(), column=self.col(), sticky=W)

        month_diff_entry = Spinbox(
            frame_datediff_date, width=3, textvariable=self.month_diff.value, from_=-999, to=999
        )
        self.month_diff.value.trace("w", self.validate_month_diff)
        month_diff_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_datediff_date, text="Monate").grid(row=self.row(), column=self.col(), sticky=W)

        year_diff_entry = Spinbox(
            frame_datediff_date, width=3, textvariable=self.year_diff.value, from_=-999, to=999
        )
        self.year_diff.value.trace("w", self.validate_year_diff)
        year_diff_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_datediff_date, text="Jahre").grid(row=self.row(), column=self.col(), sticky=W)

        # Row: Enter hour diff, minute diff and/or second diff
        frame_datediff_time = Frame(frame_datediff)

        hour_diff_entry = Spinbox(
            frame_datediff_time, width=3, textvariable=self.hour_diff.value, from_=-999, to=999
        )
        self.hour_diff.value.trace("w", self.validate_hour_diff)
        hour_diff_entry.grid(row=self.row(reset=True), column=self.col(), sticky=W)
        Label(frame_datediff_time, text="Stunden").grid(row=self.row(), column=self.col(), sticky=W)

        minute_diff_entry = Spinbox(
            frame_datediff_time, width=3, textvariable=self.minute_diff.value, from_=-999, to=999
        )
        self.minute_diff.value.trace("w", self.validate_minute_diff)
        minute_diff_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_datediff_time, text="Minuten").grid(row=self.row(), column=self.col(), sticky=W)

        second_diff_entry = Spinbox(
            frame_datediff_time, width=3, textvariable=self.second_diff.value, from_=-999, to=999
        )
        self.second_diff.value.trace("w", self.validate_second_diff)
        second_diff_entry.grid(row=self.row(), column=self.col(), sticky=W)
        Label(frame_datediff_time, text="Sekunden").grid(
            row=self.row(), column=self.col(), sticky=W
        )

        # Row: Enter microsecond diff
        frame_datediff_micro = Frame(frame_datediff)

        millisecond_diff_entry = Spinbox(
            frame_datediff_micro,
            width=3,
            textvariable=self.millisecond_diff.value,
            from_=-999,
            to=999,
        )
        self.millisecond_diff.value.trace("w", self.validate_millisecond_diff)
        millisecond_diff_entry.grid(row=self.row(reset=True), column=self.col(), sticky=W)
        Label(frame_datediff_micro, text="Millisekunden").grid(
            row=self.row(), column=self.col(), sticky=W, columnspan=2
        )

        Label(frame_datediff_micro, text="Hinweis: Wird nicht für alle Daten umgesetzt").grid(
            row=self.row(), column=self.col(6), sticky=N, rowspan=2
        )

        microsecond_diff_entry = Spinbox(
            frame_datediff_micro,
            width=3,
            textvariable=self.microsecond_diff.value,
            from_=-999,
            to=999,
        )
        self.microsecond_diff.value.trace("w", self.validate_microsecond_diff)
        microsecond_diff_entry.grid(row=self.row(new_row=True), column=self.col(), sticky=W)
        Label(frame_datediff_micro, text="Mikrosekunden").grid(
            row=self.row(), column=self.col(), sticky=W, columnspan=2
        )

        frame_fixeddate_date.grid(sticky=NW + E)
        frame_fixeddate_label.grid(sticky=NW + E)
        frame_fixeddate_date_widget.grid(sticky=NW + E)
        frame_fixeddate_time.grid(sticky=NW + E)
        frame_fixeddate_micro.grid(sticky=NW + E)

        frame_datediff_date.grid(sticky=NW + E)
        frame_datediff_time.grid(sticky=NW + E)
        frame_datediff_micro.grid(sticky=NW + E)

        frame_fixeddate.grid(sticky=NW + E)
        frame_datediff.grid(sticky=NW + E)

    def apply(self):
        self.dirty = True

        if self.mode.get() == 0:
            self.day = int(self.day.value.get()) if self.day.dirty.get() == 1 else None
            self.month = int(self.month.value.get()) if self.month.dirty.get() == 1 else None
            self.year = int(self.year.value.get()) if self.year.dirty.get() == 1 else None

        elif self.mode.get() == 1:
            new_date = self.date.value
            old_date = self.date.old
            if new_date != old_date:
                self.day = self.date.value.day
                self.month = self.date.value.month
                self.year = self.date.value.year
            else:
                self.day = None
                self.month = None
                self.year = None

        self.hour = int(self.hour.value.get()) if self.hour.dirty.get() == 1 else None
        self.minute = int(self.minute.value.get()) if self.minute.dirty.get() == 1 else None
        self.second = int(self.second.value.get()) if self.second.dirty.get() == 1 else None
        self.millisecond = (
            int(self.millisecond.value.get()) if self.millisecond.dirty.get() == 1 else None
        )
        self.microsecond = (
            int(self.microsecond.value.get()) if self.microsecond.dirty.get() == 1 else None
        )  #

        self.day_diff = int(self.day_diff.value.get())
        self.month_diff = int(self.month_diff.value.get())
        self.year_diff = int(self.year_diff.value.get())
        self.hour_diff = int(self.hour_diff.value.get())
        self.minute_diff = int(self.minute_diff.value.get())
        self.second_diff = int(self.second_diff.value.get())
        self.millisecond_diff = int(self.millisecond_diff.value.get())
        self.microsecond_diff = int(self.microsecond_diff.value.get())

    def validate(self):
        """Check if entered data is int and in range. Does not check for valid date, that happens in main"""
        try:
            if self.mode.get() == 0:
                if self.day.dirty.get() == 1:
                    day = int(self.day.value.get())
                if self.month.dirty.get() == 1:
                    month = int(self.month.value.get())
                if self.year.dirty.get() == 1:
                    year = int(self.year.value.get())

            if self.hour.dirty.get() == 1:
                hour = int(self.hour.value.get())
            if self.minute.dirty.get() == 1:
                minute = int(self.minute.value.get())
            if self.second.dirty.get() == 1:
                second = int(self.second.value.get())
            if self.millisecond.dirty.get() == 1:
                millisecond = int(self.millisecond.value.get())
            if self.microsecond.dirty.get() == 1:
                mikrosecond = int(self.microsecond.value.get())

            day_diff = int(self.day_diff.value.get())
            month_diff = int(self.month_diff.value.get())
            year_diff = int(self.year_diff.value.get())
            hour_diff = int(self.hour_diff.value.get())
            minute_diff = int(self.minute_diff.value.get())
            second_diff = int(self.second_diff.value.get())
            millisecond = int(self.millisecond_diff.value.get())
            microsecond_diff = int(self.microsecond_diff.value.get())
        except ValueError:
            messagebox.showerror("Fehler", "Ein der Eingaben ist nicht gültig")
            return False

        return True

    def validate_time_int(self, var, temp_var, r_from=None, r_to=None):
        """Check if int and in range"""
        try:
            local_var = int(var.get())
        except ValueError:
            if not var.get():
                temp_var = var.get()
                return temp_var
            else:
                var.set(temp_var)
                return temp_var

        if r_from is not None or r_to is not None:
            if r_from <= local_var < r_to:
                temp_var = var.get()
            else:
                var.set(temp_var)
        else:
            temp_var = var.get()
        return temp_var

    # Helper methods because we cannot use arguments in callbacks
    def validate_day(self, *args):
        self.day.temp = self.validate_time_int(self.day.value, self.day.temp, 0, 32)

    def validate_month(self, *args):
        self.month.temp = self.validate_time_int(self.month.value, self.month.temp, 0, 13)

    def validate_year(self, *args):
        self.year.temp = self.validate_time_int(self.year.value, self.year.temp, 1970, 3000)

    def validate_hour(self, *args):
        self.hour.temp = self.validate_time_int(self.hour.value, self.hour.temp, 0, 24)

    def validate_minute(self, *args):
        self.minute.temp = self.validate_time_int(self.minute.value, self.minute.temp, 0, 60)

    def validate_second(self, *args):
        self.second.temp = self.validate_time_int(self.second.value, self.second.temp, 0, 60)

    def validate_millisecond(self, *args):
        self.millisecond.temp = self.validate_time_int(
            self.millisecond.value, self.millisecond.temp, 0, 1000
        )

    def validate_microsecond(self, *args):
        self.microsecond.temp = self.validate_time_int(
            self.microsecond.value, self.microsecond.temp, 0, 1000
        )

    def validate_day_diff(self, *args):
        self.day_diff.temp = self.validate_time_int(self.day_diff.value, self.day_diff.temp)

    def validate_month_diff(self, *args):
        self.month_diff.temp = self.validate_time_int(self.month_diff.value, self.month_diff.temp)

    def validate_year_diff(self, *args):
        self.year_diff.temp = self.validate_time_int(self.year_diff.value, self.year_diff.temp)

    def validate_hour_diff(self, *args):
        self.hour_diff.temp = self.validate_time_int(self.hour_diff.value, self.hour_diff.temp)

    def validate_minute_diff(self, *args):
        self.minute_diff.temp = self.validate_time_int(
            self.minute_diff.value, self.minute_diff.temp
        )

    def validate_second_diff(self, *args):
        self.second_diff.temp = self.validate_time_int(
            self.second_diff.value, self.second_diff.temp
        )

    def validate_millisecond_diff(self, *args):
        self.millisecond_diff.temp = self.validate_time_int(
            self.millisecond_diff.value, self.millisecond_diff.temp
        )

    def validate_microsecond_diff(self, *args):
        self.microsecond_diff.temp = self.validate_time_int(
            self.microsecond_diff.value, self.microsecond_diff.temp
        )
