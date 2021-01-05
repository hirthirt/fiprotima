from . import tk_ui
import getpass
import platform
import controller as control

TKINTER = 0


def main(interface: int):
    control.set_current_username(getpass.getuser())
    control.set_current_os(platform.system())
    if interface == TKINTER:
        tk_ui.main()
