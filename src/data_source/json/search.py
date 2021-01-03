import json

from data_source.json.base import (
    BaseJSONHandler,
    BaseJSONClass,
    BaseAttribute,
    Caretaker,
    OTHER,
    DT_MILLI,
)

ID = "ID"
SEARCHENGINE = "Standard-Suchmaschine"
EXPIRY = "Ablaufdatum Standardsuchmaschine"


class Search(BaseJSONClass):
    def __init__(self, id: int, search_engine: str, expiry: str):
        self.id = id
        self.name = search_engine
        self.expiry_timestamp = int(expiry)
        self.init()

    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(ID, OTHER, self.id))
        self.attr_list.append(BaseAttribute(SEARCHENGINE, OTHER, self.name))
        self.attr_list.append(BaseAttribute(EXPIRY, DT_MILLI, self.expiry_timestamp))

    def update(self):
        for attr in self.attr_list:
            if attr.name == EXPIRY:
                self.expiry_timestamp = attr.timestamp


class SearchHandler(BaseJSONHandler):
    name = "Suche-Engines"

    attr_names = [ID, SEARCHENGINE, EXPIRY]

    compressed = True

    search_engines = []
    json_all = dict

    def __init__(
        self, profile_path: str, cache_path: str, file_name: str = "search.json.mozlz4",
    ):
        super().__init__(profile_path, file_name, compressed=True)

    def get_all_id_ordered(self):
        if self.search_engines:
            return self.search_engines

        self.search_engines = []

        self.open_file()
        self.json_all = json.loads(self.read_file())
        self.close()

        search_metadata = self.json_all["metaData"]
        search_default = search_metadata["searchDefault"]
        search_default_expiry = search_metadata["searchDefaultExpir"]

        search = Search(0, search_default, search_default_expiry)
        self.caretakers.append(Caretaker(search))
        self.search_engines.append(search)

        return self.search_engines
