import json

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
LASTUSE = "Zuletzt verwendet am"
LASTPASSCHANGED = "Passwort geändert am"


class Login(BaseJSONClass):
    def __init__(self, id: str, hostname: str, created_timestamp: str,
                lastused_timestamp: str, lastpasschange_timestamp: str):
        self.id = id
        self.hostname = hostname
        self.created_timestamp = int(created_timestamp)
        self.lastused_timestamp = int(lastused_timestamp)
        self.lastpasschange_timestamp = int(lastpasschange_timestamp)
        self.init()

    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.hostname))
        self.attr_list.append(BaseAttribute(CREATEDDATE, DT_SEC_ZEROED_MILLI, self.created_timestamp))
        self.attr_list.append(BaseAttribute(LASTUSE, DT_SEC_ZEROED_MILLI, self.lastused_timestamp))
        self.attr_list.append(BaseAttribute(LASTPASSCHANGED, DT_SEC_ZEROED_MILLI, self.lastpasschange_timestamp))

    def update(self, delta):
        for attr in self.attr_list:
            if attr.name == CREATEDDATE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.created_timestamp = attr.timestamp
                except:
                    print("Fehler bei Update in Login für " + attr.name)
                    continue
                self.is_date_changed = True
            if attr.name == LASTUSE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.lastused_timestamp = attr.timestamp
                except:
                    print("Fehler bei Update in Login für " + attr.name)
                    continue
                self.is_date_changed = True
            if attr.name == LASTPASSCHANGED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.lastpasschange_timestamp = attr.timestamp
                except:
                    print("Fehler bei Update in Login für " + attr.name)
                    continue
                self.is_date_changed = True


class LoginsHandler(BaseJSONHandler):
    name = "Logins"

    attr_names = [NAME, CREATEDDATE, LASTUSE, LASTPASSCHANGED]

    logins = []
    json_all = dict

    def __init__(
        self, profile_path: str, cache_path: str, file_name: str = "logins.json",
    ):
        super().__init__(profile_path, file_name)

    def get_all_id_ordered(self):
        if self.logins:
            return self.logins

        self.logins = []
        self.open_file()
        self.json_all = json.loads(self.read_file())
        self.close()

        json_logins = self.json_all["logins"]
        for id, json_login in enumerate(json_logins):
            hostname = json_login["hostname"]
            createddate = json_login["timeCreated"]
            lastuseddate = json_login["timeLastUsed"]
            lastpasschangeddate = json_login["timePasswordChanged"]
            login = Login(id, hostname, createddate, lastuseddate, lastpasschangeddate)
            self.caretakers.append(Caretaker(login))
            self.logins.append(login)

        return self.logins

    def commit(self):
        json_logins = self.json_all["logins"]
        for id, json_login in enumerate(json_logins):
            json_login["timeCreated"] = self.logins[id].created_timestamp
            json_login["timeLastUsed"] = self.logins[id].lastused_timestamp
            json_login["timePaswordChanged"] = self.logins[id].lastpasschange_timestamp

        self.json_all["logins"] = json_logins

        self.write_file()

        super().commit()