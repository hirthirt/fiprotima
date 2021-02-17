from sqlalchemy import Column, Integer, String, orm
import random

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
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.origin_url))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_WEBKIT, self.date_created))
        self.attr_list.append(BaseAttribute(LASTUSED, DT_WEBKIT, self.date_last_used))

    def update(self):
        for attr in self.attr_list:
            if attr.name == CREATEDAT:
                self.date_created = attr.timestamp
            elif attr.name == LASTUSED:
                self.date_last_used = attr.timestamp

        self.init()


class CompromisedCredetials(BaseSession, BaseSQLiteClass):
    __tablename__ = "compromised_credentials"

    url = Column("url", String)
    username = Column("username", String)
    date_created = Column("create_time", Integer, primary_key=True)

    @orm.reconstructor
    def init(self):
        self.id = random.randint(0, 9999999999999)
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.url))
        self.attr_list.append(BaseAttribute(USERNAME, OTHER, self.username))
        self.attr_list.append(BaseAttribute(CREATEDAT, DT_WEBKIT, self.date_created))


    def update(self):
        for attr in self.attr_list:
            if attr.name == CREATEDAT:
                self.date_created = attr.timestamp

        self.init()

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

class CompromisedCredentialsHandler(LoginDataHandler):
    name = "CompromisedCredentials"


    def get_all_id_ordered(self):
        logins = self.session.query(CompromisedCredetials).all()
        return logins
