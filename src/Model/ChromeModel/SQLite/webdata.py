from sqlalchemy import Column, Integer, String, orm
import random

from Model.util import log_message
from Model.ChromeModel.SQLite.base import *

NAME = "Name"
VALUE = "Wert"
KEYWORD = "Schlüsselwort"
CREATEDAT = "Erstellt am"
LASTMODIFIED = "Zuletzt geändert"
LASTVISITED = "Zuletzt besucht"
LASTUSED = "Zuletzt benutzt"

class Autofill(BaseSession, BaseSQLiteClass):
    __tablename__ = "autofill"

    name = Column("name", String, primary_key=True)
    value = Column("value", String, primary_key=True)
    date_created = Column("date_created", Integer)
    date_last_used = Column("date_last_used", Integer)

    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.id = random.randint(0, 9999999999999)
        self.attr_list = []
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.name))
        self.attr_list.append(BaseAttribute(VALUE, OTHER, self.value))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_SEC, self.date_created))
        self.attr_list.append(BaseAttribute(LASTUSED, DT_SEC, self.date_last_used))

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Autofill", "error")
            return
        for attr in self.attr_list:
            if attr.name == CREATEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.date_created = attr.timestamp
                except:
                    log_message("Fehler bei Update in Autofill für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            elif attr.name == LASTUSED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.date_last_used = attr.timestamp
                except:
                    log_message("Fehler bei Update in Autofill für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class Keyword(BaseSession, BaseSQLiteClass):
    __tablename__ = "keywords"

    id = Column("id", Integer, primary_key=True)
    keyword = Column("keyword", String)
    date_created = Column("date_created", Integer)
    last_modified = Column("last_modified", Integer)
    last_visited = Column("last_visited", Integer)


    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(KEYWORD, OTHER, self.keyword))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_WEBKIT, self.date_created))
        self.attr_list.append(BaseAttribute(LASTMODIFIED, DT_WEBKIT, self.last_modified))
        self.attr_list.append(BaseAttribute(LASTVISITED, DT_WEBKIT, self.last_visited))


    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Keywords", "error")
            return
        for attr in self.attr_list:
            if attr.name == CREATEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.date_created = attr.timestamp
                except:
                    log_message("Fehler bei Update in KeyWord für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == LASTMODIFIED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_modified = attr.timestamp
                except:
                    log_message("Fehler bei Update in KeyWord für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == LASTVISITED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_visited = attr.timestamp
                except:
                    log_message("Fehler bei Update in KeyWord für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class WebDataHandler(BaseSQliteHandler):
    name = "WebData"

    def __init__(
        self,
        profile_path: str,
        file_name: str = "Web Data",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)


class AutofillHandler(WebDataHandler):
    name = "Autofills"


    def get_all_id_ordered(self):
        autofills = self.session.query(Autofill).all()
        return autofills

class KeywordHandler(WebDataHandler):
    name = "Keywords"


    def get_all_id_ordered(self):
        keywords = self.session.query(Keyword).all()
        return keywords
