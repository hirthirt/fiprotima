import json
import pickle
from datetime import datetime, timedelta, timezone

import lz4.block
from os.path import exists, isfile, join

EPOCH = datetime(1970, 1, 1)
WEBKITEPOCH = datetime(1601, 1, 1)
OTHER = "other"
DT_SEC = "datetime_second"
DT_SEC_DOT_MILLI = "datetime_second_dot_milli"
DT_SEC_DOT_MICRO = "datetime_second_dot_micro"
DT_MILLI = "datetime_milli"
DT_MICRO = "datetime_microseconds"
DT_MILLI_ZEROED_MICRO = "datetime_milliseconds_zeroed_microseconds"
DT_MILLI_OR_ZERO = "datetime_milliseconds_zero"
DT_ZERO = "datetime_always_zero"
DT_WEBKIT = "datetime_webkit"
DT_WEBKIT_SEC = "datetime_webkit_sec"
DT_STRING = "datetime_string"
DT_SIMPLE_STRING = "datetime_simple_string"

MILLI_FACTOR = 1000
MICRO_FACTOR = 1000000

PERSISTENT = "Dauerhaft"


def microseconds_to_datetime(microseconds):
    """
    Creates datetime from microseconds.
    Workaround to datetime.replace does not handle microseconds well
    """
    datetime_obj = EPOCH + timedelta(microseconds=microseconds)
    return datetime_obj

def webit_to_datetime(microsecond):
    """
    Creates datetime form a webkit timestamp.
    Webkit is microseconds since 1.1.1601
    """
    try:
        date_time = WEBKITEPOCH + timedelta(microseconds=microsecond)
    except:
        date_time = WEBKITEPOCH + timedelta(microseconds=microsecond/10)
    return date_time

def webit_seconds_to_datetime(seconds):
    """
    Creates datetime form a webkit timestamp in seconds.
    Webkit is microseconds since 1.1.1601
    """
    return WEBKITEPOCH + timedelta(seconds==seconds)

class BaseAttribute:
    """
    Helper class to better handle Attributes
    Transforms timestamp into datetime because it makes handling date and time easier
    """

    def __init__(self, name: str, type_: str, value):
        self.name = name
        self.type = type_
        self.value = value
        self.timestamp = None

        if type_ == DT_SEC:
            self.timestamp = int(value)
            try:
                self.value = datetime.fromtimestamp(0) + timedelta(seconds=self.timestamp)
            except:
                self.value = datetime.fromtimestamp(0) + timedelta(seconds=self.timestamp/1000)
        elif type_ in (DT_MICRO, DT_MILLI_ZEROED_MICRO):
            self.timestamp = int(value)
            self.value = microseconds_to_datetime(self.timestamp)
        elif type_ == DT_MILLI:
            self.timestamp = int(value)
            self.value = microseconds_to_datetime(self.timestamp * MILLI_FACTOR)
        elif type_ == DT_MILLI_OR_ZERO:
            if self.value == 0:
                self.timestamp = 0
                self.value = PERSISTENT
                self.type = DT_ZERO
            else:
                self.timestamp = int(self.value)
                self.value = microseconds_to_datetime(self.timestamp * MILLI_FACTOR)
                self.type = DT_MILLI
        elif type_ == DT_SEC_DOT_MILLI:
            second = int(self.value)
            str_value = str(self.value)

            millisecond = int(str_value.split(".")[1])
            self.timestamp = (second * MILLI_FACTOR) + millisecond
            self.value = microseconds_to_datetime(self.timestamp * MILLI_FACTOR)
        elif type_ == DT_SEC_DOT_MICRO:
            second = int(self.value)
            str_value = str(self.value)

            mircroseconds = int(str_value.split(".")[1])
            self.timestamp = (second * MICRO_FACTOR) + mircroseconds
            self.value = microseconds_to_datetime(self.timestamp)
        elif type_ == DT_WEBKIT:
            self.timestamp = int(value)
            self.value = webit_to_datetime(self.timestamp)
        elif type_ == DT_WEBKIT_SEC:
            self.timestamp = int(value)
            self.value = webit_seconds_to_datetime(self.timestamp)
        elif type_ == DT_STRING:
            self.timestamp = value
            self.value = datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z")
        elif type_ == DT_SIMPLE_STRING:
            self.timestamp = value
            self.value = datetime.strptime(value, "%Y-%m-%d")

    def date_to_timestamp(self):
        if self.type == OTHER or self.type == DT_ZERO:
            return

        if self.type == DT_MICRO:
            microseconds = self.value.microsecond
            self.timestamp = int(datetime.timestamp(self.value.replace(tzinfo=timezone.utc)))
            self.timestamp = (self.timestamp * MICRO_FACTOR) + microseconds
        elif self.type == DT_MILLI_ZEROED_MICRO:
            # Zeroing out the last three numbers
            microseconds = self.value.microsecond
            self.timestamp = int(datetime.timestamp(self.value.replace(tzinfo=timezone.utc)))
            microseconds = int(microseconds / MILLI_FACTOR) * MILLI_FACTOR
            self.timestamp = (self.timestamp * MICRO_FACTOR) + microseconds
        elif self.type == DT_MILLI:
            microseconds = self.value.microsecond
            self.timestamp = int(datetime.timestamp(self.value.replace(tzinfo=timezone.utc)))
            milliseconds = int(microseconds / MILLI_FACTOR)
            self.timestamp = (self.timestamp * MILLI_FACTOR) + milliseconds
        elif self.type == DT_SEC_DOT_MILLI:
            microseconds = self.value.microsecond
            self.timestamp = int(datetime.timestamp(self.value.replace(tzinfo=timezone.utc)))
            milliseconds = int(microseconds / MILLI_FACTOR)
            self.timestamp = float(str(self.timestamp) + "." + str(milliseconds))
        elif self.type == DT_SEC_DOT_MICRO:
            microseconds = self.value.microsecond
            self.timestamp = int(datetime.timestamp(self.value.replace(tzinfo=timezone.utc)))
            self.timestamp = float(str(self.timestamp) + "." + str(microseconds))
        elif self.type == DT_WEBKIT:
            diff = self.value - WEBKITEPOCH
            seconds_in_day = 60 * 60 * 24
            self.timestamp = (diff.days * seconds_in_day + diff.seconds) * 1000000  + diff.microseconds
        elif self.type == DT_WEBKIT:
            diff = self.value - WEBKITEPOCH
            seconds_in_day = 60 * 60 * 24
            self.timestamp = diff.days * seconds_in_day + diff.seconds
        elif self.type == DT_STRING:
            self.timestamp = datetime.strftime(self.value, "%a, %d %b %Y %H:%M:%S %Z")
        elif self.type == DT_SIMPLE_STRING:
            self.timestamp = datetime.strftime(self.value, "%Y-%m-%d")

    def change_date(self, delta):
        if self.type == OTHER:
            return
        
        if self.timestamp == 0:
            return

        self.value = datetime.fromtimestamp(self.value.timestamp() - delta)

    def is_other(self):
        return self.type == OTHER or self.type == DT_ZERO

    def extended_timestamp(self):
        if self.type == DT_MICRO:
            return self.timestamp % MICRO_FACTOR
        if self.type == DT_MILLI:
            return self.timestamp % MILLI_FACTOR

        return None


class BaseJSONClass:
    attr_list = []

    def get_value_list(self):
        list_ = []
        for attr in self.attr_list:
            list_.append(attr.value)

        return list_

    def get_state(self):
        return pickle.dumps(vars(self))

    def set_state(self, memento):
        previous_state = pickle.loads(memento)
        vars(self).clear()
        vars(self).update(previous_state)


class BaseJSONHandler:
    pre_path = ""
    post_path = ""

    json_all = ""
    caretakers = []

    def __init__(self, root_path: str, file_name: str, compressed=False):
        self.path = join(root_path, file_name)

        if root_path == "":
            raise FileNotFoundError("Kein Pfad angegeben")
        if not exists(self.path) and not isfile(self.path):
            raise FileNotFoundError("Datei nicht gefunden, Pfad %s" % self.path)

        self.path = self.pre_path + self.path + self.post_path

        self.compressed = compressed

    def rollback(self):
        for caretaker in self.caretakers:
            caretaker.undo()

    def commit(self):
        for caretaker in self.caretakers:
            caretaker.save()

    def close_file(self):
        self.file_handle.close()

    def close(self):
        self.close_file()

    def open_file(self, write: bool = False):
        mode = "r"
        if write:
            mode = "w"
        if self.compressed:
            mode = mode + "b"

        self.file_handle = open(self.path, mode)

    def read_file(self):
        if self.compressed:
            if self.file_handle.read(8) != b"mozLz40\0":
                raise Exception("Ungueltiger Datenheader")
            else:
                return lz4.block.decompress(self.file_handle.read())
        return self.file_handle.read()

    def write_file(self):
        json_dump = json.dumps(self.json_all, separators=(",", ":"))
        if self.compressed:
            json_dump = b"mozLz40\0" + lz4.block.compress(json_dump)
        self.open_file(write=True)

        self.file_handle.write(json_dump)
        self.close_file()


class Caretaker:
    originator: BaseJSONClass

    def __init__(self, obj: BaseJSONClass):
        self.originator = obj
        self.save()

    def save(self):
        self.memento = self.originator.get_state()

    def undo(self):
        self.originator.set_state(self.memento)
