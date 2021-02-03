from sqlalchemy import Column, Integer, String, orm

from data_source.sqlite.base import *

ID = "ID"
ORIGIN = "Herkunft"
TYPE = "Erlaubnistyp"
EXPIRYAT = "Ungueltig ab"
LASTMODIFIED = "Zuletzt geaendert"


class Permission(BaseSession, BaseSQLiteClass):
    __tablename__ = "moz_perms"

    id = Column("id", Integer, primary_key=True)
    origin = Column("origin", String)
    type = Column("type", String)
    expiry_timestamp = Column("expireTime", Integer)
    modify_timestamp = Column("modificationTime", Integer)

    @orm.reconstructor
    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(ID, OTHER, self.id))
        self.attr_list.append(BaseAttribute(ORIGIN, OTHER, self.origin))
        self.attr_list.append(BaseAttribute(TYPE, OTHER, self.type))
        self.attr_list.append(BaseAttribute(EXPIRYAT, DT_MILLI_OR_ZERO, self.expiry_timestamp))
        self.attr_list.append(BaseAttribute(LASTMODIFIED, DT_MILLI, self.modify_timestamp))

    def update(self):
        for attr in self.attr_list:
            if attr.name == EXPIRYAT:
                if attr.type == DT_ZERO:
                    self.expiry_timestamp = 0
                else:
                    self.expiry_timestamp = attr.timestamp
            elif attr.name == LASTMODIFIED:
                self.modify_timestamp = attr.timestamp
        self.init()


class PermissionHandler(BaseSQliteHandler):
    name = "Seitenerlaubnis"

    attr_names = [ID, ORIGIN, TYPE, EXPIRYAT, LASTMODIFIED]

    def __init__(
        self,
        profile_path: str,
        cache_path: str,
        file_name: str = "permissions.sqlite",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        query = self.session.query(Permission).order_by(Permission.id)
        return query.all()
