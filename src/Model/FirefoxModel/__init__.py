from datetime import datetime
from pubsub import pub

from Model.FirefoxModel.JSON import DataSourcesJSON
from Model.FirefoxModel.SQLite import DataSourcesSQLite
from Model.FirefoxModel.Cache import DataSourcesCache
from Model.util import log_message

from Model.FirefoxModel.SQLite.places import VISITED
from Model.FirefoxModel.SQLite.base import OTHER

class FirefoxModel:

    def __init__(self, profile_path: str = None, cache_path: str = None):
        if profile_path is None:
            return

        if cache_path is None:
            cache_path = profile_path

        self.sources = {}

        self.sources["SQLite"] = DataSourcesSQLite(profile_path, cache_path)
        self.sources["JSON"] = DataSourcesJSON(profile_path, cache_path)
        self.sources["Cache"] = DataSourcesCache(cache_path, cache_path)

        self.data_dict = self.get_data()
        self.save_state = {}
        for key in self.data_dict:
            self.save_state[key] = True


    def get_unsaved_handlers(self):
        return [self.save_state[handler] for handler in self.save_state if self.save_state[handler] == False ]

    def get_saved_handler(self):
        return [self.save_state[handler] for handler in self.save_state if self.save_state[handler] == True ]
        
    def get_data(self):
        data_dict = {}
        for source in self.sources:
            data_dict.update(self.sources[source].get_data())
        return data_dict
    
    def reload_data_attributes(self):
        for source in self.data_dict:
            for item in self.data_dict[source]:
                try:
                    item.reload_attributes()
                except:
                    pass
    
    def get_history(self):
        histroy_tree = {}
        for entry in self.data_dict["HistoryVisitHandler"]:
            if entry.from_visit == 0:
                histroy_tree[entry] = []
            else:
                for tree_entry in histroy_tree:
                    if entry.from_visit == tree_entry.id or entry.from_visit in [sube.id for sube in histroy_tree[tree_entry]]:
                        histroy_tree[tree_entry].append(entry)
        return histroy_tree

    def get_history_last_time(self):
        history_last_time = None
        try:
            last_history_item = self.data_dict["HistoryVisitHandler"][-1]
            for attr in last_history_item.attr_list:
                if attr.name == VISITED:
                    history_last_time = attr.value
        except:
            history_last_time = datetime.now()
        
        return history_last_time


    
    def get_additional_info(self, data_type, identifier):
        if data_type == "history":
            data_dict = {
                "Cookies" : [],
                "Favicons" : [],
                "Permissions" : [],
                "ContentPrefs" : [],
                "Downloads" : [],
                "Logins" : []
            }

            try:
                for cookie in self.data_dict["CookieHandler"]:
                    if identifier in cookie.host:
                        data_dict["Cookies"].append(cookie)
            except:
                pass

            try:
                for favico in self.data_dict["FaviconHandler"]:
                    if identifier in favico.icon_url:
                        data_dict["Favicons"].append(favico)
            except:
                pass
            
            try:
                for perm in self.data_dict["PermissionHandler"]:
                    if identifier in perm.origin:
                        data_dict["Permissions"].append(perm)
            except:
                pass

            try:
                for pref in self.data_dict["ContentPrefHandler"]:
                    if identifier in pref.group.name:
                        data_dict["ContentPrefs"].append(pref)
            except:
                pass
            
            try:
                for login in self.data_dict["LoginsHandler"]:
                    if identifier in login.hostname:
                        data_dict["Logins"].append(login)
            except:
                pass

            try:
                for site in self.data_dict["HistoryVisitHandler"]:
                    for downl in self.data_dict["DownloadHandler"]:
                        if identifier in site.place.url and downl.place.id == site.place.id:
                            data_dict["Downloads"].append(downl)
            except:
                pass
        
        elif data_type == "session":
            window = None
            for windows in self.data_dict["WindowHandler"]:
                if windows.id == identifier:
                    window = windows
            data_dict = {
                "Tabs" : window.tabs,
                "Session" : [window.session]
            }

        return data_dict

    def get_form_history(self):
        return self.data_dict["FormHistoryHandler"]

    def get_addons(self):
        return self.data_dict["AddonsHandler"]

    def get_bookmarks(self):
        return self.data_dict["BookmarkHandler"]
    
    def get_extensions(self):
        return self.data_dict["ExtensionsHandler"]
    
    def get_session(self):
        return self.data_dict["WindowHandler"]
    
    def get_profile(self):
        return self.data_dict["TimesHandler"]

    def get_cache(self):
        return self.data_dict["CacheEntryHandler"]

    def get_specific_data(self, id):
        if id in self.data_dict:
            if self.data_dict[id]:
                return self.data_dict[id]
            else:
                log_message("Keine Daten verfügbar!", "info")
                return None
        else:
            log_message("Daten nicht gefunden!", "info")
            return None

    def edit_all_data(self, delta):
        for source in self.data_dict:
            for item in self.data_dict[source]:
                item.update(delta)
        self.reload_data_attributes()
        for handler in self.save_state:
            self.save_state[handler] = False

    def edit_selected_data_delta(self, delta, selection):
        for selected in selection:
            for item in self.data_dict[selected[0]]:
                if item.id == selected[1]:
                    item.update(delta)
                    self.save_state[selected[0]] = False
                try:
                    for other_item in self.data_dict[selected[0]]:
                        if item.place.id == other_item.place.id:
                            other_item.reload_attributes()
                except:
                    pass
            if len(selected) > 2:
                for child in selected[2]:
                    for c_item in self.data_dict[child[0]]:
                        if c_item.id == child[1]:
                            c_item.update(delta)
                            try:
                                for other_item in self.data_dict[child[0]]:
                                    if other_item.place.id == c_item.place.id:
                                        other_item.reload_attributes()
                            except:
                                pass

    def edit_selected_data_date(self, date, selection):
        delta = None
        for selected in selection:
            for item in self.data_dict[selected[0]]:
                if item.id == selected[1]:
                    for attr in item.attr_list:
                        if attr.type != OTHER:
                            delta = attr.value.timestamp() - date.timestamp()
                            break  
                    item.update(delta)
                    self.save_state[selected[0]] = False
                    try:
                        for other_item in self.data_dict[selected[0]]:
                            if item.place.id == other_item.place.id:
                                other_item.reload_attributes()
                    except:
                        pass
            if len(selected) > 2:
                for child in selected[2]:
                    for c_item in self.data_dict[child[0]]:
                        if c_item.id == child[1]:
                            c_item.update(delta)
                            try:
                                for other_item in self.data_dict[child[0]]:
                                    if other_item.place.id == c_item.place.id:
                                        other_item.reload_attributes()
                            except:
                                pass

    def get_data_header(self):
        data_header = []
        for source in self.sources:
            for header in source.get_data_header():
                data_header.append(header)

        return data_header

    def get_names(self):
        name_list = []
        for source in self.sources:
            for name in source.get_names():
                name_list.append(name)
        return name_list

    def rollback(self, name: str = None):
        for source in self.sources:
            self.sources[source].rollback(name)
        if name:
            for item in self.data_dict[name]:
                item.is_date_changed = False
                item.init()
            self.save_state[name] = True
        else:
            for source in self.data_dict:
                for item in self.data_dict[source]:
                    item.is_date_changed = False
                    item.init()
            for handler in self.save_state:
                self.save_state[handler] = True

    def commit(self, name: str = None):
        for source in self.sources:
            self.sources[source].commit(name)
        if name:
            for item in self.data_dict[name]:
                item.is_date_changed = False
                item.init()
            self.save_state[name] = True
        else:
            for source in self.data_dict:
                for item in self.data_dict[source]:
                    item.is_date_changed = False
                    item.init()
            for handler in self.save_state:
                self.save_state[handler] = True

    def close(self):
        for source in self.sources:
            self.sources[source].close()