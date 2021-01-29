from . import tk_ui
import getpass
import platform
import controller as control

TKINTER = 0


def main(interface: int):
    # TODO Probably implement finding all users on system
    control.set_current_username(getpass.getuser())
    control.set_current_os(platform.system())
    if interface == TKINTER:
        tk_ui.main()
