from sqlalchemy import Column, Integer, String, Float, orm, ForeignKey
from sqlalchemy.orm import relationship

from Model.util import log_message
from Model.FirefoxModel.SQLite.base import (
    BaseSession,
    BaseSQLiteClass,
    BaseAttribute,
    BaseSQliteHandler,
    OTHER,
    DT_SEC_DOT_MILLI,
)

ID = "ID"
HOST = "Host"
SETTING = "Einstellungtype"
VALUE = "Wert"
CREATEDAT = "Erstellt am"


class ContentPref(BaseSession, BaseSQLiteClass):
    __tablename__ = "prefs"

    id = Column("id", Integer, primary_key=True)
    group_id = Column("groupID", Integer, ForeignKey("groups.id"))
    group = relationship("ContentPrefGroup")
    setting_id = Column("settingID", Integer, ForeignKey("settings.id"))
    setting = relationship("ContentPrefSetting")
    value = Column("value", String)
    created_at_timestamp = Column("timestamp", Float)

    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(HOST, OTHER, self.group.name))
        self.attr_list.append(BaseAttribute(SETTING, OTHER, self.setting.name))
        self.attr_list.append(BaseAttribute(VALUE, OTHER, self.value))
        self.attr_list.append(
            (BaseAttribute(CREATEDAT, DT_SEC_DOT_MILLI, self.created_at_timestamp))
        )

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in ContentPref", "error")
            return
        for attr in self.attr_list:
            if attr.name == CREATEDAT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.created_at_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Extensions für " + attr.name, "error")
                    continue
                self.is_date_changed = True



class ContentPrefGroup(BaseSession, BaseSQLiteClass):
    __tablename__ = "groups"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)


class ContentPrefSetting(BaseSession, BaseSQLiteClass):
    __tablename__ = "settings"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)


class ContentPrefHandler(BaseSQliteHandler):
    name = "Inhaltseinstellungen"

    attr_names = [ID, HOST, SETTING, VALUE, CREATEDAT]

    def __init__(
        self,
        profile_path: str,
        cache_path: str,
        file_name: str = "content-prefs.sqlite",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        query = self.session.query(ContentPref).order_by(ContentPref.id)
        return query.all()
