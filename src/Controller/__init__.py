import getpass
import platform
import datetime
import logging
import lz4

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
        if self.get_unsaved_handlers():
            answer = AskDialog(self.view, self, "Es wurden nicht alle Daten gespeichert!\n Trotzdem fortfahren?").show()
            if not answer:
                data = "keep"
                return data
        if self.model.has_profil_loaded():
            answer = AskDialog(self.view, self, "Möchten Sie das Profil wirklich wechseln?").show()
            if not answer:
                data = "keep"
                return data
        data = self.model.load_profile(browser,name, self.config)
        if browser in ["Edge", "Chrome"]:
            self.view.menu.chrome_edge_views()
        else:
            self.view.menu.firefox_views()
        return data

    def get_unsaved_handlers(self):
        unsaved_handlers = self.model.get_unsaved_handlers()
        return unsaved_handlers

    def get_saved_handlers(self):
        saved_handlers = self.model.get_saved_handler()
        return saved_handlers
    
    def get_history(self):
        data = self.model.get_history()
        return data

    def reload_data(self):
        self.change_data_view(self.view.content.dataview_mode)

    def change_data_view(self, data_view):
        if data_view == "FormHistory":
            data = self.model.get_specific_data("FormHistoryHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Formular-Eingaben")
        elif data_view == "History":
            data = self.model.get_history()
            if data:
                self.view.content.fillHistroyData(data)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Historie")
        elif data_view == "Addons":
            data = self.model.get_specific_data("AddonsHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Addons")
        elif data_view == "Bookmarks":
            data = self.model.get_specific_data("BookmarkHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Lesezeichen")
        elif data_view == "Extensions":
            data = self.model.get_specific_data("ExtensionsHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Erweiterungen")
        elif data_view == "Session":
            data = self.model.get_specific_data("WindowHandler")
            if data:
                self.view.content.fill_dataview(data, True)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Sessions")
        elif data_view == "Profile":
            data = self.model.get_specific_data("ProfileHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Profil")
        elif data_view == "Keywords":
            data = self.model.get_specific_data("KeywordHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Keywords")
        elif data_view == "Cache":
            data = self.model.get_specific_data("CacheEntryHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Cache")
        elif data_view == "Download":
            data = self.model.get_specific_data("DownloadHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Download")
        elif data_view == "Permission":
            data = self.model.get_specific_data("PermissionHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Berechtigungen")
        elif data_view == "Favicon":
            data = self.model.get_specific_data("FaviconHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Favicons")
        elif data_view == "Cookie":
            data = self.model.get_specific_data("CookieHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Cookies")
        elif data_view == "ContentPref":
            data = self.model.get_specific_data("ContentPrefHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Seiten-Präferenzen")
        elif data_view == "FireProfile":
            data = self.model.get_specific_data("TimesHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Profil")
        elif data_view == "Autofill":
            data = self.model.get_specific_data("AutofillHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Formular-Eingaben")
        elif data_view == "Login":
            data = self.model.get_specific_data("LoginHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Logins")
        elif data_view == "CompCred":
            data = self.model.get_specific_data("CompromisedCredentialHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Unsichere Anmeldedaten")
        elif data_view == "ExtCookies":
            data = self.model.get_specific_data("ExtensionCookieHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Erweiterungs-Cookies")
        elif data_view == "Media":
            data = self.model.get_specific_data("OriginHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Medien")
        

    def load_additional_info(self, a):
        if self.view.content.dataview_mode == "History":
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            parsed_uri = urlparse(item["text"])
            split = parsed_uri.hostname.split(".")
            if len(split) > 2:
                sitename = split[1]
            else:
                sitename = split[0]
            
            data = self.model.get_additional_info("history", sitename)
            self.view.content.fill_info_section(data)
        elif self.view.content.dataview_mode == "Session":
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            data = self.model.get_additional_info("session", item["values"][-1])
            self.view.content.fill_info_section(data)
        elif self.view.content.dataview_mode == "Media":
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            data = self.model.get_additional_info("media", item["values"][-1])
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

    def edit_selected_data(self, mode, all=False, infoview=False):
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
        if not all:
            if not infoview:
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
            else:
                selected_id = self.view.content.tab_control.select()
                selected_tab = self.view.content.tab_control.tab(selected_id, "text")
                for selected in self.view.content.info_views[selected_tab][0].selection():
                    item = self.view.content.info_views[selected_tab][0].item(selected)
                    selected_list.append([item["values"][-2], item["values"][-1]])
        else:
            if not infoview:
                for element in self.view.content.dataview.get_children():
                    children = self.view.content.dataview.get_children(element)
                    if children:
                        for child in children:
                            item = self.view.content.dataview.item(child)
                            selected_list.append([item["values"][-2], item["values"][-1]])
                    item = self.view.content.dataview.item(element)
                    selected_list.append([item["values"][-2], item["values"][-1]])
            else:
                selected_id = self.view.content.tab_control.select()
                selected_tab = self.view.content.tab_control.tab(selected_id, "text")
                for element in self.view.content.info_views[selected_tab][0].get_children():
                    item = self.view.content.info_views[selected_tab][0].item(element)
                    selected_list.append([item["values"][-2], item["values"][-1]])

        if not selected_list:
            self.logger.info("Keine Elemente ausgewählt!")
            return
            
        if mode == "date":
            try:
                self.model.edit_selected_data_date(date, selected_list)
            except:
                self.logger.error("Fehler beim editieren")
                return
        else:
            self.model.edit_selected_data_delta(delta, selected_list)
            try:
                pass
            except:
                self.logger.error("Fehler beim editieren")
                return
        if not infoview:
            self.reload_data()
        else:
            self.load_additional_info(None)

    def commit_all_data(self):
        self.model.commit()
        self.reload_data()
    
    # Only commit the selected table
    def commit_selected_data(self, infoview=False):
        if not infoview:
            data_handler_name = self.view.content.selected_treeview_handler
            self.model.commit(data_handler_name)
            self.reload_data()
        else:
            selected_id = self.view.content.tab_control.select()
            selected_tab = self.view.content.tab_control.tab(selected_id, "text")
            data_handler_name = self.view.content.info_views[selected_tab][1]
            self.model.commit(data_handler_name)
            self.load_additional_info(None)
        pass

    def rollback_all_data(self):
        self.model.rollback()
        self.model.rollback_filesystem_time(self.config)
        self.reload_data()
    
    # Only rollback the selected table
    def rollback_selected_data(self, infoview=False):
        if not infoview:
            data_handler_name = self.view.content.selected_treeview_handler
            self.model.rollback(data_handler_name)
            self.reload_data()
        else:
            selected_id = self.view.content.tab_control.select()
            selected_tab = self.view.content.tab_control.tab(selected_id, "text")
            data_handler_name = self.view.content.info_views[selected_tab][1]
            self.model.rollback(data_handler_name)
            self.load_additional_info(None)
        pass
    
    def change_filesystem_time(self):
        check = AskDialog(self.view, self, "Möchten Sie die Dateisystemzeit wirklich anpassen?\n Dies sollte erst dann gemacht werden wenn alle anderen Änderungen vollzogen und gespeichert wurden!").show()
        if not check:
            return
        if not self.model.has_profil_loaded():
            self.logger.info("Kein Profil geladen!")
        self.model.change_filesystem_time(self.config)
        try:
            pass
        except:
            self.logger.error("Fehler beim ändern der Dateisystem Zeit!")
    
    def rollback_filesystem_time(self):      
        try:
            self.model.rollback_filesystem_time(self.config)
        except:
            self.logger.error("Fehler beim Rollback der Dateisystem Zeit!")

    # The listener for the logging event of pubsub
    def log_listener(self, message, lvl):
        if lvl == "info":
            self.logger.info(message)
        else:
            self.logger.error(message)