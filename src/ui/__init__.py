from . import tk_ui

TKINTER = 0


def main(interface: int):
    if interface == TKINTER:
        tk_ui.main()
