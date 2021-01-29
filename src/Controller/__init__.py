import getpass
import platform

from Config import Config
from View import View
from Model import Model

class Controller:

    def __init__(self):
        self.config = Config()
        self.model = Model()
        self.view = View(self)
        self.config.set_current_username(getpass.getuser())
        self.config.set_current_os(platform.system())

    def main(self):
        self.view.main()

    
    def load_profiles(self):
        profiledict, messages = self.model.search_profiles(current_username=self.config.current_username, current_os=self.config.current_os)
        if messages:
            for message in messages:
                self.view.sidebar.insert_message(message)
        print(profiledict)
        return profiledict