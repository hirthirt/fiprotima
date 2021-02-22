from sqlalchemy import Column, ForeignKey, Integer, String, orm
from sqlalchemy.orm import relationship

from Model.ChromeModel.SQLite.base import *

URL = "Url"
PATH = "Pfad"
LASTUPDATED = "Zuletzt aktualisiert"

# TODO: Check if its better to edit timestamps for Playback if Origin is edited
class Origin(BaseSession, BaseSQLiteClass):
    __tablename__ = "origin"

    id = Column("id", Integer, primary_key=True)
    origin = Column("origin", String)
    last_updated = Column("last_updated_time_s", Integer)
    playback = relationship("Playback")
    playbackSession = relationship("PlaybackSession")

    @orm.reconstructor
    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.origin))
        self.attr_list.append(BaseAttribute(LASTUPDATED, DT_WEBKIT, self.last_updated))


    def update(self, delta):
        for attr in self.attr_list:
            if attr.name == LASTUPDATED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_updated = attr.timestamp
                except:
                    print("Fehler bei Update in Origin/MediaHistory für " + attr.name)
                    continue
                self.is_date_changed = True



class Playback(BaseSession, BaseSQLiteClass):
    __tablename__ = "playback"

    id = Column("id", Integer, primary_key=True)
    origin_id = Column("origin_id", Integer, ForeignKey("origin.id"))
    url = Column("url", String)
    last_updated = Column("last_updated_time_s", Integer)


    @orm.reconstructor
    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.url))
        self.attr_list.append(BaseAttribute(LASTUPDATED, DT_WEBKIT, self.last_updated))


    def update(self, delta):
        for attr in self.attr_list:
            if attr.name == LASTUPDATED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_updated = attr.timestamp
                except:
                    print("Fehler bei Update in Playback/MediaHistory für " + attr.name)
                    continue
                self.is_date_changed = True


class PlaybackSession(BaseSession, BaseSQLiteClass):
    __tablename__ = "playbackSession"

    id = Column("id", Integer, primary_key=True)
    origin_id = Column("origin_id", Integer, ForeignKey("origin.id"))
    url = Column("url", String)
    last_updated = Column("last_updated_time_s", Integer)


    @orm.reconstructor
    def init(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.url))
        self.attr_list.append(BaseAttribute(LASTUPDATED, DT_WEBKIT, self.last_updated))


    def update(self, delta):
        for attr in self.attr_list:
            if attr.name == LASTUPDATED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_updated = attr.timestamp
                except:
                    print("Fehler bei Update in PlaybackSession/MediaHistory für " + attr.name)
                    continue
                self.is_date_changed = True


class OriginHandler(BaseSQliteHandler):
    name = "Login"

    attr_names = [URL]

    def __init__(
        self,
        profile_path: str,
        file_name: str = "Media History",
        logging: bool = False,
    ):
        super().__init__(profile_path, file_name, logging)

    def get_all_id_ordered(self):
        origins = self.session.query(Origin).order_by(Origin.id).all()
        return origins