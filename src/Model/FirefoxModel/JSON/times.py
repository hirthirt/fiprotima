import json
import random

from Model.util import log_message
from Model.FirefoxModel.JSON.base import (
    BaseJSONHandler,
    BaseJSONClass,
    BaseAttribute,
    Caretaker,
    OTHER,
    DT_SEC_ZEROED_MILLI,
)

NAME = "Hostname"
CREATEDDATE = "Erstellt am"
FIRSTUSE = "Erste Verwendung"


class Times(BaseJSONClass):
    def __init__(self, created, first_use):
        self.created = int(created)
        self.first_use = int(first_use)
        self.init()

    def init(self):
        self.is_date_changed = False
        self.id = random.randint(0, 9999999999999)
        self.attr_list = []
        self.attr_list.append(BaseAttribute(CREATEDDATE, DT_SEC_ZEROED_MILLI, self.created))
        self.attr_list.append(BaseAttribute(FIRSTUSE, DT_SEC_ZEROED_MILLI, self.first_use))

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Times", "error")
            return
        for attr in self.attr_list:
            if attr.name == CREATEDDATE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.created = attr.timestamp
                except:
                    log_message("Fehler bei Update in Times für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == FIRSTUSE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.first_use = attr.timestamp
                except:
                    log_message("Fehler bei Update in Times für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class TimesHandler(BaseJSONHandler):
    name = "Times"

    attr_names = [NAME, CREATEDDATE, FIRSTUSE]

    times = []
    json_all = dict

    def __init__(
        self, profile_path: str, cache_path: str, file_name: str = "times.json",
    ):
        super().__init__(profile_path, file_name)

    def get_all_id_ordered(self):
        if self.times:
            return self.times

        self.times = []
        self.open_file()
        self.json_all = json.loads(self.read_file())
        self.close()

        created = self.json_all["created"]
        first_use = self.json_all["firstUse"]

        time = Times(created, first_use)

        self.caretakers.append(Caretaker(time))
        self.times.append(time)

        return self.times

    def commit(self):
        
        self.json_all["created"] = self.times[0].created
        self.json_all["firstUse"] = self.times[0].first_use

        self.write_file()

        super().commit()
