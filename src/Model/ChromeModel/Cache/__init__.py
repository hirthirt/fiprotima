from importlib import import_module
from Model.util import log_message

class DataSourcesCache:
    def __init__(self, profile_path: str):
        self.sources = {}
        source_names = []

        source_names.append(["Model.ChromeModel.Cache.cacheHandler", "CacheEntryHandler"])

        for source_name in source_names:
            module_name = source_name[0]
            class_name = source_name[1]

            try:
                module = import_module(module_name)
                Class_ = getattr(module, class_name)
                instance = Class_(profile_path=profile_path)
            except Exception as e:
                log_message(
                    "Fehler in Datenquelle Cache, Modul %s, Klasse %s: %s. Überspringe"
                    % (module_name, class_name, e), "info"
                )
                continue
            self.sources[class_name] = instance

    def get_data(self):
        data = {}
        for source in self.sources:
            try:
                data[source] = self.sources[source].get_all_id_ordered()
            except Exception as e:
                log_message("Fehler in " + source + ": " + str(e), "info")

        return data

    def get_data_header(self):
        data_header = []
        for source in self.sources:
            data_header.append(source.attr_names)
        return data_header

    def get_names(self):
        name_list = []
        for source in self.sources:
            name_list.append(source.name)
        return name_list

    def rollback(self, name):
        """Undo changes for only one source or all"""
        if name:
            try:
                if name in self.sources:
                    self.sources[name].rollback()
                else:
                    pass
            except:
                log_message("Fehler beim Rollback von: " + str(name), "error")
        else:
            for source in self.sources:
                try:
                    self.sources[source].rollback()
                except:
                    log_message("Fehler beim Rollback von: "  + str(source), "error")


    def commit(self, name):
        """Save changes for only one source or all"""
        if name:
            try:
                if name in self.sources:
                    self.sources[name].commit()
                else:
                    pass
            except:
                log_message("Fehler beim speichern von: " + str(name), "error")
        else:
            for source in self.sources:
                try:
                    self.sources[source].commit()
                except:
                    log_message("Fehler beim Speichern von: "  + str(source), "error")

    def close(self):
        """Close all connections"""
        for source in self.sources:
            self.sources[source].close()
