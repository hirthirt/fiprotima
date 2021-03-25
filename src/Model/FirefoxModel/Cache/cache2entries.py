import os
import os.path
import struct

from Model.util import log_message

from Model.FirefoxModel.Cache.base import (
    BaseCacheClass,
    BaseCacheHandler,
    BaseAttribute,
    DT_SEC,
    OTHER,
    Caretaker,
)

# Value from netwerk/cache2/CacheFileChunk.h
CHUNKSIZE = 256 * 1024

ID = "ID"
URL = "URL"
LASTFETCHED = "Zuletzt verwendet"
LASTMODIFIED = "Geändert am"
EXPIRATION = "Läuft ab am"


class CacheEntry(BaseCacheClass):
    def __init__(self, i, file_name, url, last_fetched, last_modified, expiration):
        self.id = i
        self.file_name = file_name
        self.url = url
        self.last_fetched_timestamp = last_fetched
        self.last_modified_timestamp = last_modified
        self.expiration_timestamp = expiration
        self.init()

    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(URL, OTHER, self.url))
        self.attr_list.append(BaseAttribute(LASTFETCHED, DT_SEC, self.last_fetched_timestamp))
        self.attr_list.append(BaseAttribute(LASTMODIFIED, DT_SEC, self.last_modified_timestamp))
        self.attr_list.append(BaseAttribute(EXPIRATION, DT_SEC, self.expiration_timestamp))

    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Cache", "error")
            return
        for attr in self.attr_list:
            if attr.name == LASTMODIFIED:
                attr.change_date(delta)
                attr.date_to_timestamp()
                self.last_modified_timestamp = attr.timestamp
                try:
                    pass
                except:
                    log_message("Fehler bei Update in Cache für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == LASTFETCHED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_fetched_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cache für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == EXPIRATION:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.expiration_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Cache für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class CacheEntryHandler(BaseCacheHandler):
    name = "Cache"

    attr_names = [ID, URL, LASTFETCHED, LASTMODIFIED, EXPIRATION]

    cache_entries = []

    def __init__(
        self, profile_path: str, cache_path: str, file_name=os.path.join("cache2", "entries")
    ):
        super().__init__(cache_path, file_name)

    def init(self):
        i = 0
        file_list = os.listdir(self.path)

        for file_name in file_list:
            file_handle = open(self.path + "/" + file_name, "rb")
            file_size = os.path.getsize(file_handle.name)

            self.seek_metadata(file_handle)

            version = struct.unpack(">I", file_handle.read(4))[0]
            if version != 3:
                continue

            # Skip fetch_count
            # fetch_count = struct.unpack(">I", file_handle.read(4))[0]
            file_handle.seek(4, os.SEEK_CUR)

            last_fetched_timestamp = struct.unpack(">I", file_handle.read(4))[0]
            last_modified_timestamp = struct.unpack(">I", file_handle.read(4))[0]

            # Skip frecency
            # frecency = struct.unpack(">I", file_handle.read(4))[0]
            file_handle.seek(4, os.SEEK_CUR)

            expiration_timestamp = struct.unpack(">I", file_handle.read(4))[0]
            key_size = struct.unpack(">I", file_handle.read(4))[0]

            # Skip flags
            # flags = struct.unpack(">I", file_handle.read(4))[0]
            file_handle.seek(4, os.SEEK_CUR)

            key = file_handle.read(key_size)
            file_handle.close()

            url = str(key, "utf-8").split(":", 1)[-1:][0]

            cache_entry = CacheEntry(
                i,
                file_name,
                url,
                last_fetched_timestamp,
                last_modified_timestamp,
                expiration_timestamp,
            )
            self.caretakers.append(Caretaker(cache_entry))

            self.cache_entries.append(cache_entry)
            i = i + 1

    def get_all_id_ordered(self):
        if not self.cache_entries:
            self.init()
        return self.cache_entries

    def commit(self):
        for cache_entry in self.cache_entries:
            file_name = cache_entry.file_name
            file_handle = open(self.path + "/" + file_name, "r+b")
            self.seek_metadata(file_handle)

            version = struct.unpack(">I", file_handle.read(4))[0]
            if version != 3:
                continue

            # Skip fetch count
            file_handle.seek(4, os.SEEK_CUR)
            file_handle.write(struct.pack(">I", cache_entry.last_fetched_timestamp))
            file_handle.write(struct.pack(">I", cache_entry.last_modified_timestamp))

            # Skip frecency
            file_handle.seek(4, os.SEEK_CUR)
            file_handle.write(struct.pack(">I", cache_entry.expiration_timestamp))

            # Since we do not change other values, skip the rest
            file_handle.close()
        super().commit()

    def seek_metadata(self, file_handle):
        # For this to work the file has to be opened in mode "b"
        file_handle.seek(-4, os.SEEK_END)

        # Find where metadata is saved in file
        metadata_start = struct.unpack(">I", file_handle.read(4))[0]

        number_chunks = int(metadata_start / CHUNKSIZE)
        if metadata_start % CHUNKSIZE:
            number_chunks = number_chunks + 1

        # Go and read metadata
        file_handle.seek(metadata_start + 4 + number_chunks * 2, os.SEEK_SET)

    def close(self):
        # We should not have open files anymore
        pass

    def open_file(self, write: bool = False):
        # Don't open files
        pass
