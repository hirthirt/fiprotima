from sqlalchemy import Column, Integer, String, orm, ForeignKey
from sqlalchemy.orm import relationship
import random

from Model.util import log_message
from Model.ChromeModel.SQLite.base import *

URL = "Url"
PATH = "Pfad"
CREATEDAT = "Erstellt am"
LASTUSED = "Zuletzt genutzt"
USERNAME = "Nutzername"

class Login(BaseSession, BaseSQLiteClass):
    __tablename__ = "logins"

    id = Column("id", Integer, primary_key=True)
    origin_url = Column("origin_url", String)
    date_created = Column("date_created", Integer)
    date_last_used = Column("date_last_used", Integer)

    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.origin_url))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_WEBKIT, self.date_created))
        self.attr_list.append(BaseAttribute(LASTUSED, DT_WEBKIT, self.date_last_used))

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Login", "error")
            return
        for attr in self.attr_list:
            if attr.name == CREATEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.date_created = attr.timestamp
                except:
                    log_message("Fehler bei Update in  Login für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            elif attr.name == LASTUSED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.date_last_used = attr.timestamp
                except:
                    log_message("Fehler bei Update in  Login für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class CompromisedCredetial(BaseSession, BaseSQLiteClass):
    __tablename__ = "insecure_credentials"

    login_id = Column("parent_id", Integer, ForeignKey("logins.id"))
    date_created = Column("create_time", Integer, primary_key=True)
    login = relationship("Login")

    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.id = random.randint(0, 9999999999999)
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.login.origin_url))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_WEBKIT, self.date_created))


    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in CompromisedCredentials", "error")
            return
        for attr in self.attr_list:
            if attr.name == CREATEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.date_created = attr.timestamp
                except:
                    log_message("Fehler bei Update in  CompromisedCredentials für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class LoginDataHandler(BaseSQliteHandler):
    name = "Login"

    attr_names = [URL, CREATEDAT, LASTUSED]

    def __init__(
        self,
        profile_path: str,
        file_name: str = "Login Data",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)


class LoginHandler(LoginDataHandler):
    name = "Logins"


    def get_all_id_ordered(self):
        logins = self.session.query(Login).order_by(Login.id).all()
        return logins

class CompromisedCredentialHandler(LoginDataHandler):
    name = "CompromisedCredentials"


    def get_all_id_ordered(self):
        logins = self.session.query(CompromisedCredetial).all()
        return logins
