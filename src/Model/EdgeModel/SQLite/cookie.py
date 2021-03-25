from sqlalchemy import Column, Integer, String, orm
import random

from Model.util import log_message
from Model.EdgeModel.SQLite.base import *

ID = "ID"
HOST = "Host"
NAME = "Name"
PATH = "Pfad"
EXPIRYAT = "Ungueltig ab"
LASTACCESSAT = "Letzter Zugriff"
CREATEDAT = "Erstellt am"


class Cookie(BaseSession, BaseSQLiteClass):
    __tablename__ = "cookies"

    host = Column("host_key", String)
    name = Column("name", String)
    path = Column("path", String)
    expiry_timestamp = Column("expires_utc", Integer)
    last_accessed_timestamp = Column("last_access_utc", Integer)
    creation_timestamp = Column("creation_utc", Integer, primary_key=True)

    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.id = random.randint(0, 9999999999999)
        self.attr_list = []
        self.attr_list.append(BaseAttribute(HOST, OTHER, self.host))
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.name))
        self.attr_list.append(BaseAttribute(PATH, OTHER, self.path))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_WEBKIT, self.creation_timestamp))
        self.attr_list.append(BaseAttribute(EXPIRYAT, DT_WEBKIT, self.expiry_timestamp))
        self.attr_list.append(BaseAttribute(LASTACCESSAT, DT_WEBKIT, self.last_accessed_timestamp))    

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Cookie", "error")
            return
        for attr in self.attr_list:
            if attr.name == EXPIRYAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.expiry_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cookie für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            elif attr.name == LASTACCESSAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_accessed_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cookie für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            elif attr.name == CREATEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.creation_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cookie für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class CookieHandler(BaseSQliteHandler):
    name = "Cookies"

    attr_names = [ID, HOST, PATH, EXPIRYAT, LASTACCESSAT, CREATEDAT]

    def __init__(
        self,
        profile_path: str,
        file_name: str = "Cookies",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        query = self.session.query(Cookie)
        return query.all()
