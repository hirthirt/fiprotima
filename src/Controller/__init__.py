import getpass
import platform

from Config import Config
from View import View
from Model import Model

class Controller:

    def __init__(self):
        self.config = Config()
        self.config.set_current_username(getpass.getuser())
        self.config.set_current_os(platform.system())

        self.model = Model()
        self.view = View(self)


    def main(self):
        self.view.main()

    
    def load_profiles(self):
        profiledict, messages = self.model.search_profiles(current_username=self.config.current_username, current_os=self.config.current_os)
        if messages:
            for message in messages:
                self.view.sidebar.insert_message(message)
        return profiledict

    def load_profile(self, browser, name):
        data, messages = self.model.load_profile(browser,name)
        if messages:
            for message in messages:
                self.view.sidebar.insert_message(message)
        return data


# TODO: Implement LoggerClass to log events directly to text console