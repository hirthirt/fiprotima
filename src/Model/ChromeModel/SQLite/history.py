from sqlalchemy import Column, Integer, String, orm, ForeignKey
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

ID = "ID"
URL = "Url"
TITLE = "Name"
LASTVISITED = "Zuletzt besucht"
LASTVISITEDNONE = "Zuletzt besucht (Null)"
VISITED = "Besucht am"
ADDEDAT = "Hinzugefügt am"
LASTMODIFIED = "Geändert am"
CONTENT = "Inhalt"
FILE = "Datei"
STARTTIME = "Startzeit"
ENDTIME = "Endzeit"


class Urls(BaseSession, BaseSQLiteClass):
    __tablename__ = "urls"

    id = Column("id", Integer, primary_key=True)
    url = Column("url", String)
    title = Column("title", String)
    last_visited_timestamp = Column("last_visit_time", Integer)  # Webkit


class Visits(BaseSession, BaseSQLiteClass):
    __tablename__ = "visits"

    id = Column("id", Integer, primary_key=True)
    url_id = Column("url", Integer, ForeignKey("urls.id"))
    from_visit = Column("from_visit", Integer)
    visit_timestamp = Column("visit_time", Integer)  # Webkit
    place = relationship("Urls")

    @orm.reconstructor
    def init(self):
        self.attr_list = []

        self.attr_list.append(BaseAttribute(URL, OTHER, self.place.url))
        self.attr_list.append(BaseAttribute(TITLE, OTHER, self.place.title))
        self.attr_list.append(
            BaseAttribute(LASTVISITED, DT_MICRO, self.place.last_visited_timestamp)
        )
        self.attr_list.append(BaseAttribute(VISITED, DT_MICRO, self.visit_timestamp))

    def update(self):
        for attr in self.attr_list:
            if attr.name == LASTVISITED:
                self.url.last_visited_timestamp = attr.timestamp
            elif attr.name == VISITED:
                self.visit_timestamp = attr.timestamp

        self.init()


class Download(BaseSession, BaseSQLiteClass):
    __tablename__ = "downloads"

    id = Column("id", Integer, primary_key=True)
    target_path = Column("target_path", String)
    start_time = Column("start_time", Integer) #Webkit
    end_time = Column("end_time", Integer) #Webit
    last_modified = Column("last_modified", String) #Tue, 26 Jan 2021 13:11:34 GMT
    referrer = Column("referrer", String)

    @orm.reconstructor
    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(FILE, OTHER, self.target_path))
        self.attr_list.append(BaseAttribute(URL, OTHER, self.referrer))
        self.attr_list.append(BaseAttribute(STARTTIME, DT_WEBKIT, self.start_time))
        self.attr_list.append(BaseAttribute(ENDTIME, DT_WEBKIT, self.end_time))
        self.attr_list.append(BaseAttribute(LASTMODIFIED, DT_STRING, self.last_modified))

    def update(self):
        for attr in self.attr_list:
            if attr.name == ADDEDAT:
                self.added_timestamp = attr.timestamp
            elif attr.name == LASTMODIFIED:
                self.last_modified_timestamp = attr.timestamp

        self.init()



class HistoryHandler(BaseSQliteHandler):
    def __init__(
        self,
        profile_path: str,
        file_name: str = "History",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)


class VisitsHandler(HistoryHandler):
    name = "Visits"

    attr_names = [ID, URL, TITLE, LASTVISITED, VISITED]

    def get_all_id_ordered(self):
        history = self.session.query(Visits).order_by(Visits.id).all()
        return history
        


class DownloadHandler(HistoryHandler):
    name = "Downloads"

    attr_names = [FILE, URL, STARTTIME, ENDTIME, LASTMODIFIED]

    def get_all_id_ordered(self):
        query = self.session.query(Download).order_by(Download.id)
        return query.all()
