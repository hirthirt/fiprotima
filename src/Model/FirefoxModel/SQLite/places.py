from sqlalchemy import Column, Integer, String, orm, ForeignKey
from sqlalchemy.orm import relationship

from Model.FirefoxModel.SQLite.base import (
    BaseSession,
    BaseSQLiteClass,
    BaseSQliteHandler,
    BaseAttribute,
    OTHER,
    DT_MICRO,
    DT_MILLI_ZEROED_MICRO,
)

ID = "ID"
URL = "Url"
TITLE = "Name"
LASTVISITED = "Zuletzt besucht"
LASTVISITEDNONE = "Zuletzt besucht (Null)"
VISITED = "Besucht am"
ADDEDAT = "Hinzugefügt am"
LASTMODIFIED = "Geändert am"


class Place(BaseSession, BaseSQLiteClass):
    __tablename__ = "moz_places"

    id = Column("id", Integer, primary_key=True)
    url = Column("url", String)
    title = Column("title", String)
    last_visited_timestamp = Column("last_visit_date", Integer)  # Micro


class HistoryVisit(BaseSession, BaseSQLiteClass):
    __tablename__ = "moz_historyvisits"

    id = Column("id", Integer, primary_key=True)
    place_id = Column("place_id", Integer, ForeignKey("moz_places.id"))
    place = relationship("Place")
    visit_timestamp = Column("visit_date", Integer)  # Micro

    @orm.reconstructor
    def init(self):
        self.attr_list = []

        self.attr_list.append(BaseAttribute(ID, OTHER, self.id))
        self.attr_list.append(BaseAttribute(URL, OTHER, self.place.url))
        self.attr_list.append(BaseAttribute(TITLE, OTHER, self.place.title))
        self.attr_list.append(
            BaseAttribute(LASTVISITED, DT_MICRO, self.place.last_visited_timestamp)
        )
        self.attr_list.append(BaseAttribute(VISITED, DT_MICRO, self.visit_timestamp))

    def update(self):
        for attr in self.attr_list:
            if attr.name == LASTVISITED:
                self.place.last_visited_timestamp = attr.timestamp
            elif attr.name == VISITED:
                self.visit_timestamp = attr.timestamp

        self.init()


class Bookmark(BaseSession, BaseSQLiteClass):
    __tablename__ = "moz_bookmarks"

    id = Column("id", Integer, primary_key=True)
    type = Column("type", Integer)  # We want only type == 1
    fk_id = Column("fk", Integer, ForeignKey("moz_places.id"))
    place = relationship("Place")
    title = Column("title", String)
    added_timestamp = Column("dateAdded", Integer)  # Micro-zero
    last_modified_timestamp = Column("lastModified", Integer)  # Micro-zero

    @orm.reconstructor
    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(ID, OTHER, self.id))
        self.attr_list.append(BaseAttribute(TITLE, OTHER, self.title))
        self.attr_list.append(BaseAttribute(URL, OTHER, self.place.url))
        if self.place.last_visited_timestamp is not None:
            self.attr_list.append(
                BaseAttribute(LASTVISITED, DT_MICRO, self.place.last_visited_timestamp)
            )
        else:
            self.attr_list.append(BaseAttribute(LASTVISITEDNONE, OTHER, "None"))
        self.attr_list.append(BaseAttribute(ADDEDAT, DT_MILLI_ZEROED_MICRO, self.added_timestamp))
        self.attr_list.append(
            BaseAttribute(LASTMODIFIED, DT_MILLI_ZEROED_MICRO, self.last_modified_timestamp)
        )

    def update(self):
        for attr in self.attr_list:
            if attr.name == LASTVISITED:
                self.place.last_visited_timestamp = attr.timestamp
            elif attr.name == ADDEDAT:
                self.added_timestamp = attr.timestamp
            elif attr.name == LASTMODIFIED:
                self.last_modified_timestamp = attr.timestamp

        self.init()


class PlacesHandler(BaseSQliteHandler):
    def __init__(
        self,
        profile_path: str,
        cache_path: str,
        file_name: str = "places.sqlite",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)


class HistoryVisitHandler(PlacesHandler):
    name = "History"

    attr_names = [ID, URL, TITLE, LASTVISITED, VISITED]

    def get_all_id_ordered(self):
        query = self.session.query(HistoryVisit).order_by(HistoryVisit.id)
        return query.all()


class BookmarkHandler(PlacesHandler):
    name = "Lesezeichen"

    attr_names = [ID, TITLE, URL, LASTVISITED, ADDEDAT, LASTMODIFIED]

    def get_all_id_ordered(self):
        query = self.session.query(Bookmark).filter(Bookmark.type == 1).order_by(Bookmark.id)
        return query.all()
