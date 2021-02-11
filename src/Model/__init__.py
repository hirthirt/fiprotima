import os
import configparser
import json

from Model.FirefoxModel import FirefoxModel
from Model.EdgeModel import EdgeModel
from Model.ChromeModel import ChromeModel

class Model:

    def __init__(self):
        self.profiledict = {}
        self.browsermodel = None

    
    def load_profile(self, browser, name):
        if browser == "Firefox":
            messages = []
            profile_path = self.profiledict[browser][name][0]
            cache_path = self.profiledict[browser][name][1]
            try:
                self.browsermodel = FirefoxModel(profile_path, cache_path)
            except:
                self.browsermodel = None
                messages.append("Firefox Daten konnten nicht geladen werden!")
            if self.browsermodel:
                messages.append("Profildaten erfolgreich geladen!")
                return self.browsermodel.get_history(), messages
            else:
                return None, messages
        elif browser == "Edge":
            messages = []
            profile_path = self.profiledict[browser][name]
            try:
                self.browsermodel = EdgeModel(profile_path)
            except:
                self.browsermodel = None
                messages.append("Edge Daten konnente nicht geladen werden!")
            if self.browsermodel:
                messages.append("Profildaten erfolgreich geladen")
                return self.browsermodel.get_history(), messages
            else:
                return None, messages
        elif browser == "Chrome":
            messages = []
            profile_path = self.profiledict[browser][name]
            try:
                self.browsermodel = ChromeModel(profile_path)
            except:
                self.browsermodel = None
                messages.append("Edge Daten konnente nicht geladen werden!")
            if self.browsermodel:
                messages.append("Profildaten erfolgreich geladen")
                return self.browsermodel.get_history(), messages
            else:
                return None, messages

    # Get additional infos (cookies, permissions, etc.) for a given website
    def get_additional_info(self, sitename):
        data = self.browsermodel.get_additional_info(sitename)
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

    #This searches for installations of Firefox, Edge and Chrome
    #Then stores the profiles of them to the profiledict
    def search_profiles(self, current_username, current_os):
        firepath = None
        firecachepath = None
        chromepath = None
        edgepath = None
        messages = []

        if not current_username:
            messages.append("Der Nutzername konnte nicht ermittelt werden!")
            return None, messages

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
            messages.append("Kein kompatibles OS gefunden!")
            return None, messages
        
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
            messages.append("Firefox scheint nicht installiert zu sein!")
            pass

        if os.path.exists(chromepath):
            self.profiledict["Chrome"] = {}
            for file in os.listdir(chromepath):
                if ("Profile" in file) or ("Default" in file):
                    path = chromepath + file 
                    if os.path.isfile(path + "/Preferences"):
                        data = json.load(open(path + "/Preferences", "r"))
                        if data["profile"]["name"]:
                            self.profiledict["Chrome"][data["profile"]["name"]] = path
                        else:
                            self.profiledict["Chrome"][file] = path
                    else:
                        messages.append("Preferences-Datei für Profil " + file + " in Chrome wurde nicht gefunden!")
            if not self.profiledict["Chrome"]:
                messages.append("Keine Profile für Chrome gefunden")
        else:
            messages.append("Chrome scheint nicht installiert zu sein!")
            pass

        if os.path.exists(edgepath):
            self.profiledict["Edge"] = {}
            for file in os.listdir(edgepath):
                if ("Profile" in file) or ("Default" in file):
                    path = edgepath + file 
                    if os.path.isfile(path + "/Preferences"):
                        data = json.load(open(path + "/Preferences", "r"))
                        if data["profile"]["name"]:
                            self.profiledict["Edge"][data["profile"]["name"]] = path
                        else:
                            self.profiledict["Edge"][file] = path
                    else:
                        messages.append("Preferences-Datei für Profil " + file +  " in Edge wurde nicht gefunden!")
            if not self.profiledict["Edge"]:
                messages.append("Keine Profile für Edge gefunden")
        else:
            messages.append("Edge scheint nicht installiert zu sein!")
            pass
        return self.profiledict, messages