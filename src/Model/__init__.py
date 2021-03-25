import os
import configparser
import json
import platform
from time import sleep
from pubsub import pub
from datetime import datetime, timedelta

from Model.FirefoxModel import FirefoxModel
from Model.EdgeModel import EdgeModel
from Model.ChromeModel import ChromeModel
from Model.util import change_file_time, log_message

class Model:

    def __init__(self):
        self.profiledict = {}
        self.browsermodel = None
        self.filesystem_changed = False

    def has_profil_loaded(self):
        if self.browsermodel:
            return True
        else:
            return False
    
    def load_profile(self, browser, name, config):
        if self.browsermodel:
            self.browsermodel.close()
        if browser == "Firefox":
            config.set_profile_path(self.profiledict[browser][name][0])
            config.set_cache_path(self.profiledict[browser][name][1]) 
            try:
                self.browsermodel = FirefoxModel(config.profile_path, config.cache_path)
                config.set_startup_history_last_time(self.browsermodel.get_history_last_time())
            except:
                self.browsermodel = None
                pub.sendMessage("logging",
                                 message="Firefox Daten konnten nicht geladen werden!", 
                                 lvl="error")
            if self.browsermodel:
                pub.sendMessage("logging",
                                 message="Profildaten erfolgreich geladen!", 
                                 lvl="info")
                return self.browsermodel.get_history()
            else:
                return None
        elif browser == "Edge":
            config.profile_path = self.profiledict[browser][name]
            try:
                self.browsermodel = EdgeModel(config.profile_path)
                config.set_startup_history_last_time(self.browsermodel.get_history_last_time())
            except:
                self.browsermodel = None
                pub.sendMessage("logging",
                                 message="Edge Daten konnten nicht geladen werden!", 
                                 lvl="error")
            if self.browsermodel:
                pub.sendMessage("logging",
                                 message="Profildaten erfolgreich geladen", 
                                 lvl="info")
                return self.browsermodel.get_history()
            else:
                return None
        elif browser == "Chrome":
            config.set_profile_path(self.profiledict[browser][name])
            try:
                self.browsermodel = ChromeModel(config.profile_path)
                config.set_startup_history_last_time(self.browsermodel.get_history_last_time())
            except:
                self.browsermodel = None
                pub.sendMessage("logging",
                                 message="Chrome Daten konnten nicht geladen werden!", 
                                 lvl="error")
            if self.browsermodel:
                pub.sendMessage("logging",
                                 message="Profildaten erfolgreich geladen", 
                                 lvl="info")
                return self.browsermodel.get_history()
            else:
                return None

    
    def get_saved_handlers(self):
        if self.browsermodel:
            saved_handler  = self.browsermodel.get_saved_handlers()
        else:
            log_message("Kein Profil geladen!", "info")
            saved_handler = None
        return saved_handler

    def get_unsaved_handlers(self):
        if self.browsermodel:
            unsaved_handler  = self.browsermodel.get_unsaved_handlers()
        else:
            log_message("Kein Profil geladen!", "info")
            unsaved_handler = None
        return unsaved_handler
    
    # Get additional infos (cookies, permissions, etc.) for a given website
    def get_additional_info(self, data_type, indentifier):
        data = self.browsermodel.get_additional_info(data_type, indentifier)
        return data

    def get_specific_data(self, id):
        if self.browsermodel:
            data = self.browsermodel.get_specific_data(id)
        else:
            data = None
        return data

    def get_form_history(self):
        if self.browsermodel:
            data = self.browsermodel.get_form_history()
        else:
            data = None
        return data

    def get_history(self):
        if self.browsermodel:
             data = self.browsermodel.get_history()
        else:
            data = None
        return data

    def get_addons(self):
        if self.browsermodel:
            data = self.browsermodel.get_addons()
        else:
            data = None
        return data

    def get_bookmarks(self):
        if self.browsermodel:
            data = self.browsermodel.get_bookmarks()
        else:
            data = None
        return data
    
    def get_extensions(self):
        if self.browsermodel:
            data = self.browsermodel.get_extensions()
        else:
            data = None
        return data
    
    def get_session(self):
        if self.browsermodel:
            data = self.browsermodel.get_session()
        else:
            data = None
        return data

    def get_session_info(self, window_id):
        if self.browsermodel:
            data = self.browsermodel.get_session_info(window_id)
        else:
            data = None
        return data
    
    def get_profile(self):
        if self.browsermodel:
            data = self.browsermodel.get_profile()
        else:
            data = None
        return data

    def get_keywords(self):
        if self.browsermodel:
            data = self.browsermodel.get_keywords()
        else:
            data = None
        return data

    def get_cache(self):
        if self.browsermodel:
            data = self.browsermodel.get_cache()
        else:
            data = None
        return data
    
    def edit_all_data(self, delta):
        if self.browsermodel:
            self.browsermodel.edit_all_data(delta)
        else:
            pub.sendMessage("logging",
                                 message="Kein Profil ausgewählt!", 
                                 lvl="info")

    def edit_selected_data_delta(self, delta, selection):
        if self.browsermodel:
            self.browsermodel.edit_selected_data_delta(delta, selection)
        else:
            pub.sendMessage("logging",
                                 message="Kein Profil ausgewählt!", 
                                 lvl="info")
    
    def edit_selected_data_date(self, date, selection):
        if self.browsermodel:
            self.browsermodel.edit_selected_data_date(date, selection)
        else:
            pub.sendMessage("logging",
                                 message="Kein Profil ausgewählt!", 
                                 lvl="info")

    def commit(self, name: str = None):
        if self.browsermodel:
            self.browsermodel.commit(name)
        else:
            pub.sendMessage("logging",
                                 message="Kein Profil ausgewählt!", 
                                 lvl="info")
    
    def rollback(self, name: str = None):
        if self.browsermodel:
            self.browsermodel.rollback(name)
        else:
            pub.sendMessage("logging",
                                 message="Kein Profil ausgewählt!", 
                                 lvl="info")

    # Rollback the changes on file timestamps
    def rollback_filesystem_time(self, config):
        if not self.filesystem_changed:
            pub.sendMessage("logging",
                            message="Dateisystem wurde noch nicht verändert!", 
                            lvl="info")
            return
        delta = config.file_system_rollback_delta
        self.browsermodel.close()
        sleep(1)
        config.set_file_system_rollback_delta(0)

        paths = [config.profile_path]
        if config.cache_path:
            paths.append(config.cache_path)

        for path in paths:
                # recursivly iterate through the dirs and files and change time
                for root, dir, files in os.walk(path):
                    for d in dir:
                        path = os.path.join(root, d)
                        try:
                            change_file_time(path, delta)
                        except:
                            pub.sendMessage("logging",
                                            message="Datei " + 
                                            path + 
                                            " konnten nicht editiert werden!", 
                                            lvl="info")
                    for f in files:
                        path = os.path.join(root, f)
                        try:
                            change_file_time(path, delta)
                        except:
                            pub.sendMessage("logging",
                                            message="Datei " + 
                                            path + 
                                            " konnten nicht editiert werden!", 
                                            lvl="info")
        self.filesystem_changed = False
        self.browsermodel.get_data()
    
    # Change timestamps of the profile files
    def change_filesystem_time(self, config):
        now_history_last_time = self.browsermodel.get_history_last_time()
        self.browsermodel.close()
        sleep(1)
        if not now_history_last_time:
            pub.sendMessage("logging",
                            message="Konnte keine History finden", 
                            lvl="error")
        paths = [config.profile_path]
        if config.cache_path:
            paths.append(config.cache_path)
        start_timestamp = config.startup_history_last_time.timestamp()
        end_timestamp = now_history_last_time.timestamp()
        delta = start_timestamp - end_timestamp
        rollback_delta = -1 * delta
        config.set_file_system_rollback_delta(rollback_delta)
        
        for path in paths:
                # recursivly iterate through the dirs and files and change time
                for root, dir, files in os.walk(path):
                    for d in dir:
                        path = os.path.join(root, d)
                        try:
                            change_file_time(path, delta)
                        except:
                            pub.sendMessage("logging",
                                            message="Datei " + 
                                            path + 
                                            " konnten nicht editiert werden!", 
                                            lvl="info")
                    for f in files:
                        path = os.path.join(root, f)
                        change_file_time(path, delta)
                        try:
                            pass
                        except:
                            pub.sendMessage("logging",
                                            message="Datei " + 
                                            path + 
                                            " konnten nicht editiert werden!", 
                                            lvl="info")
        self.filesystem_changed = True



    #This searches for installations of Firefox, Edge and Chrome
    #Then stores the profiles of them to the profiledict
    def search_profiles(self, current_username, current_os):
        firepath = None
        firecachepath = None
        chromepath = None
        edgepath = None


        if not current_username:
            pub.sendMessage("logging",
                            message="Der Nutzername konnte nicht ermittelt werden!", 
                            lvl="error")
            return None

        if current_os == "Windows":
            firepath = "C:/Users/" + current_username + "/AppData/Roaming/Mozilla/Firefox/"
            firecachepath = "C:/Users/" + current_username  + "/AppData/Local/Mozilla/Firefox/"
            edgepath = "C:/Users/" + current_username + "/AppData/Local/Microsoft/Edge/User Data/"
            chromepath = "C:/Users/" + current_username + "/AppData/Local/Google/Chrome/User Data/"
        elif current_os == "Linux":
            firepath = "/home/" + current_username + "/.mozilla/firefox/"
            firecachepath = "/home/" + current_username  + "/.cache/mozilla/firefox/"
            chromepath = "/home/" + current_username + "/.config/google-chrome/"
            edgepath = ""
            pass
        elif current_os == "Darwin":
            firepath = "Users/" + current_username + "/Library/Application Support/Firefox/"
            firecachepath = "Users/" + current_username + "/Library/Caches/Firefox/"
            chromepath = "Users/" + current_username + "/Library/Application Support/Google/Chrome/"
            edgepath = ""
        else:
            pub.sendMessage("logging",
                            message="Kein kompatibles OS gefunden!", 
                            lvl="error")
            return None
        
        if os.path.exists(firepath):
            self.profiledict["Firefox"] = {}
            config_parser = configparser.ConfigParser()
            config_parser.read(firepath + "profiles.ini")

            for section in config_parser.sections():
                if "Profile" in section:
                    self.profiledict["Firefox"][config_parser[section].get("Name")] = [firepath + config_parser[section].get("Path")]
                    if os.path.exists(firecachepath):
                        self.profiledict["Firefox"][config_parser[section].get("Name")].append(firecachepath + config_parser[section].get("Path"))
                    
            
        else:
            pub.sendMessage("logging",
                            message="Firefox scheint nicht installiert zu sein!", 
                            lvl="info")
            pass

        if os.path.exists(chromepath):
            self.profiledict["Chrome"] = {}
            for file in os.listdir(chromepath):
                if ("Profile " in file) or ("Default" in file):
                    path = chromepath + file 
                    if os.path.isfile(path + "/Preferences"):
                        data = json.load(open(path + "/Preferences", "r"))
                        if data["profile"]["name"]:
                            self.profiledict["Chrome"][data["profile"]["name"]] = path
                        else:
                            self.profiledict["Chrome"][file] = path
                    else:
                        pub.sendMessage("logging",
                            message="Preferences-Datei für Profil " + file + " in Chrome wurde nicht gefunden!", 
                            lvl="info")
            if not self.profiledict["Chrome"]:
                pub.sendMessage("logging",
                            message="Keine Profile für Chrome gefunden", 
                            lvl="info")
        else:
            pub.sendMessage("logging",
                            message="Chrome scheint nicht installiert zu sein!", 
                            lvl="info")
            pass

        if os.path.exists(edgepath):
            self.profiledict["Edge"] = {}
            for file in os.listdir(edgepath):
                if ("Profile " in file) or ("Default" in file):
                    path = edgepath + file 
                    if os.path.isfile(path + "/Preferences"):
                        data = json.load(open(path + "/Preferences", "r"))
                        if data["profile"]["name"]:
                            self.profiledict["Edge"][data["profile"]["name"]] = path
                        else:
                            self.profiledict["Edge"][file] = path
                    else:
                        pub.sendMessage("logging",
                            message="Preferences-Datei für Profil " + file +  " in Edge wurde nicht gefunden!", 
                            lvl="info")
            if not self.profiledict["Edge"]:
                pub.sendMessage("logging",
                            message="Keine Profile für Edge gefunden", 
                            lvl="info")
        else:
            pub.sendMessage("logging",
                            message="Edge scheint nicht installiert zu sein!", 
                            lvl="info")
            pass
        return self.profiledict