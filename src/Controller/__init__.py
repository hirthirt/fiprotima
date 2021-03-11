import getpass
import platform
import datetime
import logging

from pubsub import pub
from dateutil.relativedelta import *
from urllib.parse import urlparse
from Config import Config
from Controller.console import Console
from View import View
from View.Dialogs.delta_dialog import TimedeltaDialog
from View.Dialogs.date_dialog import DateDialog
from View.Dialogs.ask_dialog import AskDialog
from Model import Model


class Controller:

    def __init__(self):
        self.config = Config()
        self.config.set_current_username(getpass.getuser())
        self.config.set_current_os(platform.system())

        self.view = View(self)

        self.console = Console(self.view.sidebar.console)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.console)

        self.model = Model() 

        pub.subscribe(self.log_listener, 'logging')

        self.view.sidebar.insert_profiles_to_treeview()

    def main(self):
        self.view.main()

    
    def load_profiles(self):
        profiledict = self.model.search_profiles(current_username=self.config.current_username, current_os=self.config.current_os)
        return profiledict

    def load_profile(self, browser, name):
        data = None
        if self.model.has_profil_loaded():
            answer = AskDialog(self.view, self, "Möchten Sie das Profil wirklich wechseln?").show()
            if not answer:
                data = "keep"
                return data
        data = self.model.load_profile(browser,name, self.config)
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
        elif data_view == "keywords":
            data = self.model.get_keywords()
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
        delta = TimedeltaDialog(self.view, self).show()
        if delta:
            now = datetime.datetime.now()
            delta = now  - delta
            try:
                delta = now.timestamp() - delta.timestamp()
            except:
                self.log_listener("Zeitdelta zu groß!", "error")
                return
        else:
            self.logger.error("Kein Delta angegeben!")
            return
        self.model.edit_all_data(delta)
        self.reload_data()

    def edit_selected_data(self, mode):
        # Ask for timedelta with dialog, then change all data based on this timedelta 
        if mode == "date":
            date = DateDialog(self.view, self).show()
            if not date:
                self.logger.error("Kein Datum angegeben!")
                return
        else:
            delta = TimedeltaDialog(self.view, self).show()
            if delta:
                now = datetime.datetime.now()
                delta = now  - delta
                try:
                    delta = now.timestamp() - delta.timestamp()
                except:
                    self.log_listener("Zeitdelta zu groß!", "error")
                    return
            else:
                self.logger.error("Kein Delta angegeben!")
                return


        selected_list = []
        already_selected_list = []
        for selected in self.view.content.dataview.selection():
            if selected in already_selected_list:
                continue
            item = self.view.content.dataview.item(selected)
            children = self.view.content.dataview.get_children(selected)
            children_list = []
            if children:
                for child in children:
                    if child in already_selected_list:
                        continue
                    c_item = self.view.content.dataview.item(child)
                    children_list.append([c_item["values"][-2], c_item["values"][-1]])
                    already_selected_list.append(child)
            selected_list.append([item["values"][-2], item["values"][-1], children_list])
            already_selected_list.append(selected)
        
        
        for info_view in self.view.content.info_views:
            for selected in info_view.selection():
                item = info_view.item(selected)
                selected_list.append([item["values"][-2], item["values"][-1]])
        if mode == "date":
            self.model.edit_selected_data_date(date, selected_list)
            try:
                pass
            except:
                self.logger.error("Fehler beim editieren")
                return
        else:
            try:
                self.model.edit_selected_data_delta(delta, selected_list)
            except:
                self.logger.error("Fehler beim editieren")
                return
        self.reload_data()

    def commit_all_data(self):
        self.model.commit()
    
    #TODO: Get selected Dataname from View and commit only this data
    def commit_selected_data(self):
        pass
    
    def change_filesystem_time(self):      
        try:
            self.model.change_filesystem_time(self.config)
        except:
            self.logger.error("Felher beim ändern der Dateisystem Zeit!")
    
    def rollback_filesystem_time(self):      
        try:
            self.model.rollback_filesystem_time(self.config)
        except:
            self.logger.error("Felher beim Rollback der Dateisystem Zeit!")

    # The listener for the logging event of pubsub
    def log_listener(self, message, lvl):
        if lvl == "info":
            self.logger.info(message)
        else:
            self.logger.error(message)