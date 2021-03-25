from sqlalchemy import Column, Integer, String, orm

from Model.util import log_message
from Model.FirefoxModel.SQLite.base import *

ID = "ID"
HOST = "Host"
PATH = "Pfad"
EXPIRYAT = "Ungueltig ab"
LASTACCESSAT = "Letzter Zugriff"
CREATEDAT = "Erstellt am"


class Cookie(BaseSession, BaseSQLiteClass):
    __tablename__ = "moz_cookies"

    id = Column("id", Integer, primary_key=True)
    host = Column("host", String)
    path = Column("path", String)
    expiry_timestamp = Column("expiry", Integer)
    last_accessed_timestamp = Column("lastAccessed", Integer)
    creation_timestamp = Column("creationTime", Integer)

    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(HOST, OTHER, self.host))
        self.attr_list.append(BaseAttribute(PATH, OTHER, self.path))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_MICRO, self.creation_timestamp))
        self.attr_list.append(BaseAttribute(EXPIRYAT, DT_SEC, self.expiry_timestamp))
        self.attr_list.append(BaseAttribute(LASTACCESSAT, DT_MICRO, self.last_accessed_timestamp))
        
    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Cookies", "error")
            return
        for attr in self.attr_list:
            if attr.name == EXPIRYAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.expiry_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cookies für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            elif attr.name == LASTACCESSAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_accessed_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cookies für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            elif attr.name == CREATEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.creation_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cookies für " + attr.name, "error")
                    continue
                self.is_date_changed = True



class CookieHandler(BaseSQliteHandler):
    name = "Cookies"

    attr_names = [ID, HOST, PATH, EXPIRYAT, LASTACCESSAT, CREATEDAT]

    def __init__(
        self,
        profile_path: str,
        cache_path: str,
        file_name: str = "cookies.sqlite",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        query = self.session.query(Cookie).order_by(Cookie.id)
        return query.all()
