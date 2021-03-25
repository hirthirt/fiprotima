import os
import struct

from Model.FirefoxModel.Cache.base import BaseCacheClass, BaseCacheHandler


class IndexEntry(BaseCacheClass):
    def __init__(
        self,
        id,
        sha1_hash,
        frecency,
        origin_attr_hash,
        on_start_time,
        on_stop_time,
        content_type,
        flags,
        index_file_size,
    ):
        self.id = id
        self.sha1_hash = sha1_hash
        self.frecency = frecency
        self.origin_attr_hash = origin_attr_hash
        self.on_start_time = on_start_time
        self.on_stop_time = on_stop_time
        self.content_type = content_type
        self.flags = flags
        self.file_size = index_file_size


class IndexHandler(BaseCacheHandler):
    name = "Cache - Indexeintraege"

    index_entries = []

    def __init__(
        self, rootpath: str, filepath: str = "cache2/index",
    ):
        super().__init__(rootpath, filepath)

    def init(self):
        i = 0
        self.open_file()
        file_size = os.path.getsize(self.path)

        self.version = struct.unpack(">I", self.file_handle.read(4))[0]
        self.last_written_timestamp = struct.unpack(">I", self.file_handle.read(4))[0]
        self.dirty = struct.unpack(">I", self.file_handle.read(4))[0]
        while (file_size - self.file_handle.tell()) > 36:
            sha1_hash = self.file_handle.read(20).hex()
            frecency = struct.unpack(">I", self.file_handle.read(4))[0]  # [sic]
            origin_attr_hash = struct.unpack(">Q", self.file_handle.read(8))[0]

            # See https://bugzilla.mozilla.org/show_bug.cgi?id=1325088
            on_start_time = struct.unpack(">H", self.file_handle.read(2))[0]
            on_stop_time = struct.unpack(">H", self.file_handle.read(2))[0]
            content_type = struct.unpack("B", self.file_handle.read(1))[0]
            flags = struct.unpack(">B", self.file_handle.read(1))[0]
            index_file_size = struct.unpack(">I", b"\x00" + self.file_handle.read(3))[0]

            self.index_entries.append(
                IndexEntry(
                    i,
                    sha1_hash,
                    frecency,
                    origin_attr_hash,
                    on_start_time,
                    on_stop_time,
                    content_type,
                    flags,
                    index_file_size,
                )
            )
            i = i + 1
        self.close_file()
