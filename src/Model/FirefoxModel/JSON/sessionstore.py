import json
import random

from Model.FirefoxModel.JSON.base import (
    BaseJSONHandler,
    BaseJSONClass,
    BaseAttribute,
    Caretaker,
    OTHER,
    DT_SEC_ZEROED_MILLI,
)

NAME = "Titel"
WINDOWTYPE = "Fenstertyp"
CLOSEDAT = "Geschlossen am"
LASTACCESSED = "Zuletzt ausgewählt"
LASTUPDATED = "Zuletzt geupdatet"
STARTTIME = "Startzeit"


class Window(BaseJSONClass):
    def __init__(self, id: str, title, closed_at, tabs, session, window_type):
        self.id = id
        self.title = title
        self.closed_at = closed_at
        self.tabs = tabs
        self.session = session
        self.window_type = window_type
        self.init()

    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.title))
        self.attr_list.append(BaseAttribute(WINDOWTYPE, OTHER, self.window_type))
        self.attr_list.append(BaseAttribute(CLOSEDAT, DT_SEC_ZEROED_MILLI, self.closed_at))

    def update(self, delta):
        for attr in self.attr_list:
            if attr.name == CLOSEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.closed_at = attr.timestamp
                except:
                    print("Fehler bei Update in Window für " + attr.name)
                    continue
                self.is_date_changed = True
        for tab in self.tabs:
            tab.update(delta)
        self.session.update(delta)


class Tab(BaseJSONClass):
    def __init__(self, id, title, last_accessed):
        self.id = id
        self.title = title
        self.last_accessed = last_accessed
        self.init()
    
    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.title))
        self.attr_list.append(BaseAttribute(LASTACCESSED, DT_SEC_ZEROED_MILLI, self.last_accessed))

    def update(self, delta):
        for attr in self.attr_list:
            if attr.name == LASTACCESSED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_accessed = attr.timestamp
                except:
                    print("Fehler bei Update in Tab für " + attr.name)
                    continue
                self.is_date_changed = True

class Session(BaseJSONClass):
    def __init__(self, last_update, start_time):
        self.last_update = last_update
        self.start_time = start_time
        self.init()

    def init(self):
        self.id = random.randint(0, 9999999999999)
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(LASTUPDATED, DT_SEC_ZEROED_MILLI, self.last_update))
        self.attr_list.append(BaseAttribute(STARTTIME, DT_SEC_ZEROED_MILLI, self.start_time))
    
    def update(self, delta):
        for attr in self.attr_list:
            if attr.name == LASTUPDATED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_update = attr.timestamp
                except:
                    print("Fehler bei Update in Session für " + attr.name)
                    continue
                self.is_date_changed = True
            if attr.name == STARTTIME:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.start_time = attr.timestamp
                except:
                    print("Fehler bei Update in Session für " + attr.name)
                    continue
                self.is_date_changed = True

class WindowsHandler(BaseJSONHandler):
    name = "Windows"

    attr_names = [NAME, CLOSEDAT]

    windows = []
    json_all = dict

    def __init__(
        self, profile_path: str, cache_path: str, file_name: str = "sessionstore.jsonlz4",
    ):
        super().__init__(profile_path, file_name, compressed=True)

    def get_all_id_ordered(self):
        if self.windows:
            return self.windows

        self.windows = []
        self.open_file()
        self.json_all = json.loads(self.read_file())
        self.close()

        session = Session(self.json_all["session"]["lastUpdate"], self.json_all["session"]["startTime"])
        json_windows = self.json_all["windows"]
        for id, json_window in enumerate(json_windows):
            title = json_window["title"]
            closed_at = json_window["closedAt"]
            window_type = "Geöffnet"
            tabs = []
            for t_id, json_tab in enumerate(json_window["tabs"]):
                t_title = json_tab["entries"][-1]["title"]
                last_accessed = json_tab["lastAccessed"]
                tabs.append(Tab(t_id, t_title, last_accessed))
            window = Window(id, title, closed_at, tabs, session, window_type)
            self.caretakers.append(Caretaker(window))
            self.windows.append(window)

        json_windows = self.json_all["_closedWindows"]
        for id, json_window in enumerate(json_windows):
            title = json_window["title"]
            closed_at = json_window["closedAt"]
            window_type = "Geschossen"
            tabs = []
            for t_id, json_tab in enumerate(json_window["tabs"]):
                t_title = json_tab["entries"][-1]["title"]
                last_accessed = json_tab["lastAccessed"]
                tabs.append(Tab(t_id, t_title, last_accessed))
            window = Window(id, title, closed_at, tabs, session, window_type)
            self.caretakers.append(Caretaker(window))
            self.windows.append(window)

        return self.windows

    def commit(self):
        json_windows = self.json_all["windows"]
        for id, json_login in enumerate(json_windows):
            json_login["timeCreated"] = self.windows[id].created_timestamp
            json_login["timeLastUsed"] = self.windows[id].lastused_timestamp
            json_login["timePaswordChanged"] = self.windows[id].lastpasschange_timestamp

        self.json_all["windows"] = json_windows

        self.write_file()

        super().commit()
