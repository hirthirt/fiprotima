import getpass
import platform
import datetime

from Config import Config
from View import View
from Model import Model

class Controller:

    def __init__(self):
        self.config = Config()
        self.config.set_current_username(getpass.getuser())
        self.config.set_current_os(platform.system())

        self.model = Model()
        self.view = View(self)
        self.view.sidebar.insert_profiles_to_treeview()


    def main(self):
        self.view.main()

    
    def load_profiles(self):
        profiledict, messages = self.model.search_profiles(current_username=self.config.current_username, current_os=self.config.current_os)
        if messages:
            for message in messages:
                self.view.sidebar.insert_message(message)
        return profiledict

    def load_profile(self, browser, name):
        data, messages = self.model.load_profile(browser,name)
        if messages:
            for message in messages:
                self.view.sidebar.insert_message(message)
        return data

    def get_history(self):
        data = self.model.get_history()
        return data

    def get_additional_info(self, sitename):
        data = self.model.get_additional_info(sitename)
        return data

    def get_session_info(self, window_id):
        data = self.model.get_session_info(window_id)
        return data

    def change_data_view(self, data_view):
        if data_view == "formhistory":
            data = self.model.get_form_history()
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
        elif data_view == "history":
            data = self.model.get_history()
            if data:
                self.view.content.fillHistroyData(data)
                self.view.content.dataview_mode = data_view
        elif data_view == "addons":
            data = self.model.get_addons()
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
        elif data_view == "bookmarks":
            data = self.model.get_bookmarks()
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
        elif data_view == "extensions":
            data = self.model.get_extensions()
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
        elif data_view == "session":
            data = self.model.get_session()
            if data:
                self.view.content.fill_dataview(data, True)
                self.view.content.dataview_mode = data_view
        elif data_view == "profile":
            data = self.model.get_profile()
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view

    def edit_all_data(self):
        # Ask for timedelta with dialog, then change all data based on this timedelta
        years = 20
        months = 0
        days = 0
        minutes = 0
        seconds = 0

        delta = int(years*365.24*24*60*60) + int(months*30*24*60*60) + int(days*24*60*60) + int(minutes*60) + seconds
        self.model.edit_all_data(delta)

# TODO: Implement LoggerClass to log events directly to text console