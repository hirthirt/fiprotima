class Config:
    """Saves the current config paths"""

    def __init__(self, profile_path=None, cache_path=None,
                 current_username=None, current_os=None,
                 current_browser=None):
        self.profile_path = profile_path
        self.cache_path = cache_path
        self.current_username = current_username
        self.current_os = current_os
        self.current_browser = current_browser


configuration = Config()


def set_profile_path(path: str):
    global configuration
    configuration.profile_path = path


def set_cache_path(path: str):
    global configuration
    configuration.cache_path = path

def set_current_username(username: str):
    global configuration
    configuration.current_username = username

def set_current_os(current_os: str):
    global configuration
    configuration.current_os = current_os

def set_current_browser(current_browser: str):
    global configuration
    configuration.current_browser = current_browser
