from Model.ChromeModel.JSON import DataSourcesJSON
from Model.ChromeModel.SQLite import DataSourcesSQLite
from Model.ChromeModel.Cache import DataSourcesCache

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

    def get_additional_info(self, data_type, identifier):
        if data_type == "history":
            data_dict = {
                "Cookies" : [],
                "Favicons" : [],
                "ContentPrefs" : [],
                "Downloads" : []
            }
            for cookie in self.data_dict["CookieHandler"]:
                if sitename in cookie.host:
                    data_dict["Cookies"].append(cookie)

            for favico in self.data_dict["FaviconsHandler"]:
                if sitename in favico.urls.url:
                    data_dict["Favicons"].append(favico)

            for downl in self.data_dict["DownloadHandler"]:
                if sitename in downl.referrer:
                    data_dict["Downloads"].append(downl)

        return data_dict

    def get_form_history(self):
        return self.data_dict["FormHistoryHandler"]

    def get_addons(self):
        return self.data_dict["AddonsHandler"]

    def get_bookmarks(self):
        return self.data_dict["BookmarkHandler"]

    def get_data_header(self):
        data_header = []
        for source in self.sources:
            for header in source.get_data_header():
                data_header.append(header)

        return data_header

    def get_profile(self):
        return self.data_dict["ProfileHandler"]

    def get_names(self):
        name_list = []
        for source in self.sources:
            for name in source.get_names():
                name_list.append(name)
        return name_list

    def rollback(self, name: str = None):
        for source in self.sources:
            source.rollback(name)

    def commit(self, name: str = None):
        for source in self.sources:
            source.commit(name)

    def init_obj(self, list_=None):
        if list_ is None:
            return

        for data in list_:
            for obj in data:
                obj.init()

    def close(self):
        for source in self.sources:
            source.close()