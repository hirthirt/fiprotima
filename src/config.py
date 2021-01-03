class Config:
    """Saves the current config paths"""

    def __init__(self, profile_path=None, cache_path=None):
        self.profile_path = profile_path
        self.cache_path = cache_path


configuration = Config()


def set_profile_path(path: str):
    global configuration
    configuration.profile_path = path


def set_cache_path(path: str):
    global configuration
    configuration.cache_path = path
