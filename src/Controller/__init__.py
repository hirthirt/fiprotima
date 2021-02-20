import getpass
import platform
import datetime

from urllib.parse import urlparse
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
        data, messages = self.model.load_profile(browser,name, self.config)
        if messages:
            for message in messages:
                self.view.sidebar.insert_message(message)
        return data

    def get_history(self):
        data = self.model.get_history()
        return data

    def reload_data(self):
        self.change_data_view(self.view.content.dataview_mode)

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

    def load_additional_info(self, a):
        if self.view.content.dataview_mode == "history":
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            parsed_uri = urlparse(item["text"])
            split = parsed_uri.hostname.split(".")
            if len(split) > 2:
                sitename = split[1]
            else:
                sitename = split[0]
            
            data = self.model.get_additional_info("history", sitename)
            self.view.content.fill_info_section(data)
        elif self.view.content.dataview_mode == "session":
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            data = self.model.get_additional_info("session", item["values"][-1])
            self.view.content.fill_info_section(data)

    
    def edit_all_data(self):
        # Ask for timedelta with dialog, then change all data based on this timedelta
        years = 2
        months = 0
        days = 0
        minutes = 0
        seconds = 0

        delta = int(years*365.24*24*60*60) + int(months*30*24*60*60) + int(days*24*60*60) + int(minutes*60) + seconds
        self.model.edit_all_data(delta)

    def edit_selected_data(self):
        # Ask for timedelta with dialog, then change all data based on this timedelta
        years = 2
        months = 0
        days = 0
        minutes = 0
        seconds = 0

        delta = int(years*365.24*24*60*60) + int(months*30*24*60*60) + int(days*24*60*60) + int(minutes*60) + seconds
        selected_list = []
        for selected in self.view.content.dataview.selection():
            item = self.view.content.dataview.item(selected)
            selected_list.append([item["values"][-2], item["values"][-1]])
        try:
            self.model.edit_selected_data(delta, selected_list)
        except:
            print("Fehler beim edititeren!")
            return
        self.reload_data()

    def change_filesystem_time(self):
        self.model.change_filesystem_time(self.config)
        try:
            pass
        except:
            print("Felher beim ändern der Dateisystem Zeit!")

# TODO: Implement LoggerClass to log events directly to text console