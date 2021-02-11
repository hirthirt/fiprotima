from sqlalchemy import Table, Column, Integer, String, orm, ForeignKey
from sqlalchemy.orm import relationship

from Model.ChromeModel.SQLite.base import (
    BaseSession,
    BaseSQLiteClass,
    BaseSQliteHandler,
    BaseAttribute,
    OTHER,
    DT_MICRO,
    DT_MILLI_ZEROED_MICRO,
    DT_WEBKIT,
    DT_STRING
)

ID = "id"
LASTREQUESTED = "Zuletzt angefordert"
LASTUPDATED = "Zuletzt geupdated"
URL = "Url"

class Favicon(BaseSession, BaseSQLiteClass):
    __tablename__ = "favicon_bitmaps"

    id = Column("id", Integer, primary_key=True)
    icon_id = Column("icon_id", Integer, ForeignKey("favicons.id"))
    last_updated = Column("last_updated", Integer) #Webkit
    last_requested = Column("last_requested", Integer) #Webkit
    urls = relationship("FaviconUrls")

    @orm.reconstructor
    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.urls.url))
        self.attr_list.append(BaseAttribute(LASTUPDATED, DT_WEBKIT, self.last_updated))
        self.attr_list.append(BaseAttribute(LASTREQUESTED, DT_WEBKIT, self.last_requested))

    def update(self):
        for attr in self.attr_list:
            if attr.name == LASTUPDATED:
                self.expiry_timestamp = attr.timestamp


class FaviconUrls(BaseSession, BaseSQLiteClass):
    __tablename__ = "favicons"
    id = Column("id", Integer, primary_key=True)
    url = Column("url", String)


class FaviconsHandler(BaseSQliteHandler):
    name = "Favicons"

    attr_names = [URL, LASTUPDATED, LASTREQUESTED]

    def __init__(
        self,
        profile_path: str,
        file_name: str = "Favicons",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        query = self.session.query(Favicon).order_by(Favicon.id)
        return query.all()
