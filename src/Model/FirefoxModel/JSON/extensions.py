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

NAME = "Hostname"
INSTALLDDATE = "Installiert am"
UPDATEDATE = "Geupdatet am"
SIGNEDDATE = "Signiert am"
VALIDNOTAFTER = "Nicht valide nach"
VALIDNOTBEFORE = "Nicht valide vor"


class Extension(BaseJSONClass):
    def __init__(self, id, name, install_timestamp,
                update_timestamp, signed_timestamp, 
                validnotafter_timestamp, validnotbefore_timestamp):
        self.id = id
        self.name = name
        self.install_timestamp = int(install_timestamp)
        if update_timestamp:
            self.update_timestamp = int(update_timestamp)
        else:
            self.update_timestamp = None
        if signed_timestamp:
            self.signed_timestamp = int(signed_timestamp)
        else:
            self.signed_timestamp = None
        if validnotafter_timestamp:
            self.validnotafter_timestamp = int(validnotafter_timestamp)
        else:
            self.validnotafter_timestamp = None
        if validnotbefore_timestamp:
            self.validnotbefore_timestamp = int(validnotbefore_timestamp)
        else:
            self.validnotbefore_timestamp = None
        self.init()

    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.name))
        self.attr_list.append(BaseAttribute(INSTALLDDATE, DT_SEC_ZEROED_MILLI, self.install_timestamp))
        if self.update_timestamp:
            self.attr_list.append(BaseAttribute(UPDATEDATE, DT_SEC_ZEROED_MILLI, self.update_timestamp))
        else:
            self.attr_list.append(BaseAttribute(UPDATEDATE, OTHER, "None"))
        if self.signed_timestamp:
            self.attr_list.append(BaseAttribute(SIGNEDDATE, DT_SEC_ZEROED_MILLI, self.signed_timestamp))
        else:
            self.attr_list.append(BaseAttribute(SIGNEDDATE, OTHER, "None"))
        if self.validnotafter_timestamp:
            self.attr_list.append(BaseAttribute(VALIDNOTAFTER, DT_SEC_ZEROED_MILLI, self.validnotafter_timestamp))
        else:
            self.attr_list.append(BaseAttribute(VALIDNOTAFTER, OTHER, "None"))
        if self.validnotbefore_timestamp:
            self.attr_list.append(BaseAttribute(VALIDNOTBEFORE, DT_SEC_ZEROED_MILLI, self.validnotbefore_timestamp))
        else:
            self.attr_list.append(BaseAttribute(VALIDNOTBEFORE, OTHER, "None"))

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Extensions", "error")
            return
        for attr in self.attr_list:
            if attr.name == INSTALLDDATE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.install_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Extensions für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == UPDATEDATE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.update_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Extensions für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == SIGNEDDATE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.signed_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Extensions für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == VALIDNOTAFTER:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.validnotafter_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Extensions für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == VALIDNOTBEFORE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.validnotbefore_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Extensions für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class ExtensionsHandler(BaseJSONHandler):
    name = "Extensions"

    attr_names = [NAME, INSTALLDDATE, UPDATEDATE, SIGNEDDATE, VALIDNOTAFTER, VALIDNOTBEFORE]

    extensions = []
    json_all = dict

    def __init__(
        self, profile_path: str, cache_path: str, file_name: str = "extensions.json",
    ):
        super().__init__(profile_path, file_name)

    def get_all_id_ordered(self):
        if self.extensions:
            return self.extensions

        self.extensions = []
        self.open_file()
        self.json_all = json.loads(self.read_file())
        self.close()

        json_extensions = self.json_all["addons"]
        for id, json_extension in enumerate(json_extensions):
            name = json_extension["defaultLocale"]["name"]
            installdate = json_extension["installDate"]
            try:
                updatedate = json_extension["updateDate"]
            except:
                updatedate = None
            try:
                signeddate = json_extension["signedDate"]
            except:
                signeddate = None
            try:
                validnotafter = json_extension["recommendationState"]["validNotAfter"]
            except:
                validnotafter = None
            try:
                 validnotbefore = json_extension["recommendationState"]["validNotBefore"]
            except:
                validnotbefore = None
            extension = Extension(id, name, installdate, updatedate, signeddate,
                        validnotafter, validnotbefore)
            self.caretakers.append(Caretaker(extension))
            self.extensions.append(extension)

        return self.extensions

    def commit(self):
        json_extensions = self.json_all["addons"]
        for id, json_extension in enumerate(json_extensions):
            json_extension["installDate"] = self.extensions[id].install_timestamp
            if self.extensions[id].update_timestamp:
                json_extension["updateDate"] = self.extensions[id].update_timestamp
            if self.extensions[id].signed_timestamp:
                json_extension["signedDate"] = self.extensions[id].signed_timestamp
            if self.extensions[id].validnotafter_timestamp:
                json_extension["recommendationState"]["validNotAfter"] = self.extensions[id].validnotafter_timestamp
            if self.extensions[id].validnotbefore_timestamp:
                json_extension["recommendationState"]["validNotBefore"] = self.extensions[id].validnotbefore_timestamp


        self.json_all["extensions"] = json_extensions

        self.write_file()

        super().commit()
