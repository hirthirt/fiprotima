import json

from Model.util import log_message
from Model.FirefoxModel.JSON.base import (
    BaseJSONHandler,
    BaseJSONClass,
    BaseAttribute,
    Caretaker,
    OTHER,
    DT_SEC_ZEROED_MILLI,
)

ID = "ID"
NAME = "Addonsname"
UPDATEDATE = "Aktualisiert am"


class Addon(BaseJSONClass):
    def __init__(self, id: int, name: str, update_timestamp: str):
        self.id = id
        self.name = name
        self.update_timestamp = int(update_timestamp)
        self.init()

    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.name))
        self.attr_list.append(BaseAttribute(UPDATEDATE, DT_SEC_ZEROED_MILLI, self.update_timestamp))

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Addons", "error")
            return
        for attr in self.attr_list:
            if attr.name == UPDATEDATE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.update_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Addons für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class AddonsHandler(BaseJSONHandler):
    name = "Addons"

    attr_names = [ID, NAME, UPDATEDATE]

    addons = []
    json_all = dict

    def __init__(
        self, profile_path: str, cache_path: str, file_name: str = "addons.json",
    ):
        super().__init__(profile_path, file_name)

    def get_all_id_ordered(self):
        if self.addons:
            return self.addons

        self.addons = []
        self.open_file()
        self.json_all = json.loads(self.read_file())
        self.close()

        json_addons = self.json_all["addons"]
        for id, json_addon in enumerate(json_addons):
            name = json_addon["name"]
            update_date = json_addon["updateDate"]
            addon = Addon(id, name, update_date)
            self.caretakers.append(Caretaker(addon))
            self.addons.append(addon)

        return self.addons

    def commit(self):
        json_addons = self.json_all["addons"]
        for id, json_addon in enumerate(json_addons):
            json_addon["updateDate"] = self.addons[id].update_timestamp

        self.json_all["addons"] = json_addons

        self.write_file()

        super().commit()
