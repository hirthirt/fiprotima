from data_source.cache import DataSourcesCache
from data_source.json import DataSourcesJSON
from data_source.sqlite import DataSourcesSQLite


class DataSources:
    def __init__(self, profile_path: str = None, cache_path: str = None):
        if profile_path is None:
            return

        if cache_path is None:
            cache_path = profile_path

        self.data_list = []
        self.sources = []

        self.sources.append(DataSourcesSQLite(profile_path, cache_path))
        self.sources.append(DataSourcesJSON(profile_path, cache_path))
        self.sources.append(DataSourcesCache(cache_path, cache_path))

        #

    def get_data(self):
        for source in self.sources:
            for data_list in source.get_data():
                self.data_list.append(data_list)

        return self.data_list

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
