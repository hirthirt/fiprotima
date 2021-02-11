from importlib import import_module


class DataSourcesJSON:
    pre_path = ""
    post_path = ""

    def __init__(self, profile_path: str):
        path = self.pre_path + profile_path + self.post_path
        self.sources = {}

        source_names = []

        source_names.append(["Model.EdgeModel.JSON.addons", "AddonsHandler"])

        for source_name in source_names:
            module_name = source_name[0]
            class_name = source_name[1]

            try:
                module = import_module(module_name)
                Class_ = getattr(module, class_name)
                instance = Class_(profile_path=profile_path)
            except Exception as e:
                print(
                    "Fehler in Datenquelle JSON, Modul %s, Klasse %s: %s. Überspringe"
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
        if name is None:
            for source in self.sources:
                source.rollback()
        else:
            for source in self.sources:
                if source.name == name:
                    source.rollback()

    def commit(self, name):
        if name is None:
            for source in self.sources:
                source.commit()
        else:
            for source in self.sources:
                if source.name == name:
                    source.commit()

    def close(self):
        for source in self.sources:
            source.close()
