from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from os.path import exists, isfile, join

# Base needed for sqlalchemy
BaseSession = declarative_base()
BaseSessionTwo = declarative_base()

EPOCH = datetime(1970, 1, 1)
WEBKITEPOCH = datetime(1601, 1, 1)
OTHER = "other"
DT_SEC = "datetime_second"
DT_SEC_DOT_MILLI = "datetime_second_dot_milli"
DT_MILLI = "datetime_milli"
DT_MICRO = "datetime_microseconds"
DT_MILLI_ZEROED_MICRO = "datetime_milliseconds_zeroed_microseconds"
DT_MILLI_OR_ZERO = "datetime_milliseconds_zero"
DT_ZERO = "datetime_always_zero"
DT_WEBKIT = "datetime_webkit"
DT_STRING = "datetime_string"

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
        elif type_ == DT_WEBKIT:
            self.timestamp = int(value)
            self.value = webit_to_datetime(self.timestamp)
        elif type_ == DT_STRING:
            self.timestamp = value
            self.value = datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z")

    def date_to_timestamp(self):
        """Transforms datetime to timestamps"""
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
        elif self.type == DT_WEBKIT:
            diff = self.value - WEBKITEPOCH
            seconds_in_day = 60 * 60 * 24
            self.timestamp = (diff.days * seconds_in_day + diff.seconds) * 1000000  + diff.microseconds
        elif self.type == DT_STRING:
            self.timestamp = datetime.strftime(self.value, "%a, %d %b %Y %H:%M:%S %Z")

    def change_date(self, delta):
        """Override value with datetime"""
        if self.type == OTHER:
            return
        
        if self.timestamp == 0:
            return

        self.value = datetime.fromtimestamp(self.value.timestamp() - delta)

    def is_other(self):
        """Check if attribute is datetime or other type like string"""
        return self.type == OTHER or self.type == DT_ZERO

    def extended_timestamp(self):
        """Returns microseconds or milliseconds from timestamp"""
        if self.type == DT_MICRO:
            return self.timestamp % MICRO_FACTOR
        if self.type == DT_MILLI:
            return self.timestamp % MILLI_FACTOR

        return None

    def check_new_bigger(self, timestamp, delta):
        value = None
        try:
            value = datetime.fromtimestamp(timestamp.timestamp() - delta)
        except:
            return False, None
        if value and value > self.value:
            return True, self.value.timestamp() - value.timestamp()
        else:
             return False, None


class BaseSQLiteClass:
    attr_list = []

    def get_value_list(self):
        list_ = []
        for attr in self.attr_list:
            list_.append(attr.value)

        return list_


class BaseSQliteHandler:
    pre_path = "sqlite:///"
    post_path = ""

    def __init__(self, root_path: str, file_name: str, logging: bool = False):
        path = join(root_path, file_name)
        if root_path == "":
            raise FileNotFoundError("Kein Pfad angegeben")

        if not exists(path) and not isfile(path):
            raise FileNotFoundError("Datei nicht gefunden, Pfad %s" % path)

        path = self.pre_path + path + self.post_path

        engine = create_engine(path, echo=logging)
        SessionClass = sessionmaker(bind=engine)
        self.session = SessionClass()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        if len(self.session.dirty) != 0 or len(self.session.new) != 0:
            self.session.commit()

    def close(self):
        self.session.close()

    
