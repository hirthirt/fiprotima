from importlib import import_module


class DataSourcesCache:
    def __init__(self, profile_path: str, cache_path: str):
        self.sources = {}
        source_names = []

        source_names.append(["Model.EdgeModel.Cache.cache2entries", "Cache2Handler"])

        for source_name in source_names:
            module_name = source_name[0]
            class_name = source_name[1]

            try:
                module = import_module(module_name)
                Class_ = getattr(module, class_name)
                instance = Class_(profile_path=profile_path, cache_path=cache_path)
            except Exception as e:
                print(
                    "Fehler in Datenquelle Cache, Modul %s, Klasse %s: %s. Überspringe"
                    % (module_name, class_name, e)
                )
                continue
            self.sources[class_name] = instance

    def get_data(self):
        data = {}
        for source in self.sources:
            data[source] = self.sources[source].get_all_id_ordered()

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
                self.sources[name].rollback()
            except:
                print("Fehler beim speichern von: " + str(name))
        else:
            for source in self.sources:
                try:
                    self.sources[source].rollback()
                except:
                    print("Fehler beim Speichern von: "  + str(source))


    def commit(self, name):
        """Save changes for only one source or all"""
        if name:
            try:
                self.sources[name].commit()
            except:
                print("Fehler beim speichern von: " + str(name))
        else:
            for source in self.sources:
                try:
                    self.sources[source].commit()
                except:
                    print("Fehler beim Speichern von: "  + str(source))

    def close(self):
        """Close all connections"""
        for source in self.sources:
            self.sources[source].close()
