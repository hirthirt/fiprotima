from config import set_cache_path, set_profile_path, set_current_os, set_current_username, set_current_browser, configuration
from data_source import DataSources

source: DataSources = None


def init():
    global source

    # Close old connections
    if source is not None:
        source = None

    profile_path = configuration.profile_path
    cache_path = configuration.cache_path

    source = DataSources(profile_path=profile_path, cache_path=cache_path)


def get_source_names():
    if source is not None:
        return source.get_names()
    else:
        return None


def get_data_headers():
    if source is not None:
        return source.get_data_header()
    else:
        return None


def get_data_lists():
    if source is not None:
        return source.get_data()
    else:
        return None


def save():
    if source is not None:
        source.commit()


def undo():
    if source is not None:
        source.rollback()


def reinit_list(lists):
    source.init_obj(lists)


def close():
    if source is not None:
        source.close()


def set_paths(profile_path: str, cache_path: str):
    set_profile_path(profile_path)
    set_cache_path(cache_path)

def set_os(os: str):
    set_current_os(os)

def set_username(username: str):
    set_current_username(username)

def set_browser(browser: str):
    set_current_browser(browser)
