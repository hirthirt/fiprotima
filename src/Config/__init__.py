class Config:
    """Saves the current config paths"""

    def __init__(self, profile_path=None, cache_path=None,
                 current_username=None, current_os=None,
                 current_browser=None, startup_history_last_time=None):
        self.profile_path = profile_path
        self.cache_path = cache_path
        self.current_username = current_username
        self.current_os = current_os
        self.current_browser = current_browser
        self.startup_history_last_time = startup_history_last_time



    def set_profile_path(self, path: str):
        self.profile_path = path


    def set_cache_path(self, path: str):
        self.cache_path = path

    def set_current_username(self, username: str):
        self.current_username = username

    def set_current_os(self, current_os: str):
        self.current_os = current_os

    def set_current_browser(self, current_browser: str):
        self.current_browser = current_browser

    def set_startup_history_last_time(self, startup_history_last_time):
        self.startup_history_last_time = startup_history_last_time