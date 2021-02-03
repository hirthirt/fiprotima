from sqlalchemy import Table, Column, Integer, String, orm, ForeignKey
from sqlalchemy.orm import relationship

from Model.FirefoxModel.SQLite.base import *

ID = "id"
EXPIRYAT = "Ungueltig ab"
URL = "Url"

favicons_to_pages = Table(
    "moz_icons_to_pages",
    BaseSession.metadata,
    Column("page_id", Integer, ForeignKey("moz_pages_w_icons.id")),
    Column("icon_id", Integer, ForeignKey("moz_icons.id")),
)


class Favicon(BaseSession, BaseSQLiteClass):
    __tablename__ = "moz_icons"

    id = Column("id", Integer, primary_key=True)
    expiry_timestamp = Column("expire_ms", Integer)
    icon_url = Column("icon_url", String)
    urls = relationship("FaviconPage", secondary=favicons_to_pages)

    @orm.reconstructor
    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(ID, OTHER, self.id))

        if len(self.urls) == 0:
            self.attr_list.append(BaseAttribute(URL, OTHER, self.icon_url))
        else:
            self.attr_list.append(BaseAttribute(URL, OTHER, self.urls[0].page_url))
        self.attr_list.append(BaseAttribute(EXPIRYAT, DT_MILLI, self.expiry_timestamp))

    def update(self):
        for attr in self.attr_list:
            if attr.name == EXPIRYAT:
                self.expiry_timestamp = attr.timestamp


class FaviconPage(BaseSession, BaseSQLiteClass):
    __tablename__ = "moz_pages_w_icons"
    id = Column("id", Integer, primary_key=True)
    page_url = Column("page_url", String)


class FaviconsHandler(BaseSQliteHandler):
    name = "Favicons"

    attr_names = [ID, URL, EXPIRYAT]

    def __init__(
        self,
        profile_path: str,
        cache_path: str,
        file_name: str = "favicons.sqlite",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        query = self.session.query(Favicon).order_by(Favicon.id)
        return query.all()
