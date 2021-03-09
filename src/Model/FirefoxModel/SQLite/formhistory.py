from sqlalchemy import Column, Integer, String, orm

from Model.log_util import log_message
from Model.FirefoxModel.SQLite.base import *

ID = "ID"
FIELDNAME = "Feldname"
VALUE = "Eingabewert"
FIRSTUSED = "Zum ersten mal verwendet"
LASTUSED = "Zuletzt genutzt"


class FormHistory(BaseSession, BaseSQLiteClass):
    __tablename__ = "moz_formhistory"

    id = Column("id", Integer, primary_key=True)
    field_name = Column("fieldname", String)
    value = Column("value", String)
    first_used_timestamp = Column("firstUsed", Integer)
    last_used_timestamp = Column("lastUsed", Integer)

    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(FIELDNAME, OTHER, self.field_name))
        self.attr_list.append(BaseAttribute(VALUE, OTHER, self.value))
        self.attr_list.append(
            BaseAttribute(FIRSTUSED, DT_MILLI_ZEROED_MICRO, self.first_used_timestamp)
        )
        self.attr_list.append(
            BaseAttribute(LASTUSED, DT_MILLI_ZEROED_MICRO, self.last_used_timestamp)
        )

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in FormHistory", "error")
            return
        for attr in self.attr_list:
            if attr.name == FIRSTUSED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.first_used_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Formhistory für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == LASTUSED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_used_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Formhistory für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class FormHistoryHandler(BaseSQliteHandler):
    name = "Formhistory"

    attr_names = [ID, FIELDNAME, VALUE, FIRSTUSED, LASTUSED]

    def __init__(
        self,
        profile_path: str,
        cache_path: str,
        file_name: str = "formhistory.sqlite",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        query = self.session.query(FormHistory).order_by(FormHistory.id)
        return query.all()
