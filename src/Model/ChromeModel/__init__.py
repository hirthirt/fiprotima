from Model.ChromeModel.JSON import DataSourcesJSON
from Model.ChromeModel.SQLite import DataSourcesSQLite
from Model.ChromeModel.Cache import DataSourcesCache

from Model.ChromeModel.SQLite.history import VISITED

class ChromeModel:

    def __init__(self, profile_path: str = None):
        if profile_path is None:
            return

        self.sources = {}

        self.sources["SQLite"] = DataSourcesSQLite(profile_path)
        self.sources["JSON"] = DataSourcesJSON(profile_path)
        #self.sources["Cache"] = DataSourcesCache(cache_path)

        self.data_dict = self.get_data()
        

    def get_data(self):
        data_dict = {}
        for source in self.sources:
            data_dict.update(self.sources[source].get_data())
        return data_dict
    
    def get_history(self):
        histroy_tree = {}
        for entry in self.data_dict["VisitsHandler"]:
            if entry.from_visit == 0:
                histroy_tree[entry] = []
            else:
                for tree_entry in histroy_tree:
                    if entry.from_visit == tree_entry.id or entry.from_visit in [sube.id for sube in histroy_tree[tree_entry]]:
                        histroy_tree[tree_entry].append(entry)
        return histroy_tree

    def get_history_last_time(self):
        history_last_time = None#
        last_history_item = self.data_dict["VisitsHandler"][-1]
        for attr in last_history_item.attr_list:
            if attr.name == VISITED:
                history_last_time = attr.value
        
        return history_last_time

    def get_additional_info(self, data_type, identifier):
        if data_type == "history":
            data_dict = {
                "Cookies" : [],
                "Favicons" : [],
                "ContentPrefs" : [],
                "Downloads" : []
            }
            for cookie in self.data_dict["CookieHandler"]:
                if identifier in cookie.host:
                    data_dict["Cookies"].append(cookie)

            for favico in self.data_dict["FaviconHandler"]:
                if identifier in favico.urls.url:
                    data_dict["Favicons"].append(favico)

            for downl in self.data_dict["DownloadHandler"]:
                if identifier in downl.referrer:
                    data_dict["Downloads"].append(downl)

        return data_dict

    def get_form_history(self):
        return self.data_dict["FormHistoryHandler"]

    def get_addons(self):
        return self.data_dict["AddonsHandler"]

    def get_bookmarks(self):
        return self.data_dict["BookmarkHandler"]

    def get_profile(self):
        return self.data_dict["ProfileHandler"]

    def get_keywords(self):
        return self.data_dict["KeywordHandler"]

    def edit_all_data(self, delta):
        for source in self.data_dict:
            for item in self.data_dict[source]:
                item.update(delta)

    def edit_selected_data(self, delta, selection):
        for selected in selection:
            for item in self.data_dict[selected[0]]:
                if item.id == selected[1]:
                    item.update(delta)

    def rollback(self, name: str = None):
        for source in self.sources:
            self.sources[source].rollback(name)
        if name:
            for item in self.data_dict[name]:
                item.is_date_changed = False
        else:
            for source in self.data_dict:
                for item in self.data_dict[source]:
                    item.is_date_changed = False

    def commit(self, name: str = None):
        for source in self.sources:
            self.sources[source].commit(name)
        if name:
            for item in self.data_dict[name]:
                item.is_date_changed = False
        else:
            for source in self.data_dict:
                for item in self.data_dict[source]:
                    item.is_date_changed = False

    def close(self):
        for source in self.sources:
            self.sources[source].close()