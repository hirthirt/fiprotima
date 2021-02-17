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

    def get_form_history(self):
        data = self.model.get_form_history()
        return data
    
    def get_addons(self):
        data = self.model.get_addons()
        return data
    
    def get_bookmarks(self):
        data = self.model.get_bookmarks()
        return data
    
    def get_extensions(self):
        data = self.model.get_extensions()
        return data
    
    def get_session(self):
        data = self.model.get_session()
        return data

    def get_session_info(self, window_id):
        data = self.model.get_session_info(window_id)
        return data

    def get_profile(self):
        data = self.model.get_profile()
        return data

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