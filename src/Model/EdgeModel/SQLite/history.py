from sqlalchemy import Column, Integer, String, orm, ForeignKey
from sqlalchemy.orm import relationship

from Model.EdgeModel.SQLite.base import (
    BaseSession,
    BaseSQLiteClass,
    BaseSQliteHandler,
    BaseAttribute,
    OTHER,
    DT_MICRO,
    DT_MILLI_ZEROED_MICRO,
    DT_WEBKIT
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
    __tablename__ = "urls"

    id = Column("id", Integer, primary_key=True)
    url = Column("url", String)
    title = Column("title", String)
    last_visited_time = Column("last_visit_time", Integer)  # Webkit


class Visits(BaseSession, BaseSQLiteClass):
    __tablename__ = "visits"

    id = Column("id", Integer, primary_key=True)
    url_id = Column("url", Integer, ForeignKey("urls.id"))
    from_visit = Column("from_visit", Integer)
    visit_time = Column("visit_time", Integer)  # WebKit
    place = relationship("Place")

    @orm.reconstructor
    def init(self):
        self.attr_list = []

        self.attr_list.append(BaseAttribute(ID, OTHER, self.id))
        self.attr_list.append(BaseAttribute(URL, OTHER, self.place.url))
        self.attr_list.append(BaseAttribute(TITLE, OTHER, self.place.title))
        self.attr_list.append(
            BaseAttribute(LASTVISITED, DT_WEBKIT, self.place.last_visited_time)
        )
        self.attr_list.append(BaseAttribute(VISITED, DT_WEBKIT, self.visit_time))

    def update(self):
        for attr in self.attr_list:
            if attr.name == LASTVISITED:
                self.url.last_visited_timestamp = attr.timestamp
            elif attr.name == VISITED:
                self.visit_timestamp = attr.timestamp

        self.init()




class PlacesHandler(BaseSQliteHandler):
    def __init__(
        self,
        profile_path: str,
        file_name: str = "History",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)


class VisitsHandler(PlacesHandler):
    name = "Visit"

    attr_names = [ID, URL, TITLE, LASTVISITED, VISITED]

    def get_all_id_ordered(self):
        query = self.session.query(Visits).order_by(Visits.id)
        return query.all()

    def get_history_tree(self):
        histroy_tree = {}
        history = self.get_all_id_ordered()
        for entry in history:
            if entry.from_visit == 0:
                histroy_tree[entry] = []
            else:
                for tree_entry in histroy_tree:
                    if entry.from_visit == tree_entry.id or entry.from_visit in [sube.id for sube in histroy_tree[tree_entry]]:
                        histroy_tree[tree_entry].append(entry)
        return histroy_tree

