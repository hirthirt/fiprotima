import os
import sys
from datetime import datetime
from pubsub import pub
import platform

if platform.system() == "Windows":
    from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
    from win32file import GENERIC_WRITE, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, FILE_SHARE_WRITE

def log_message(message, lvl):
    pub.sendMessage("logging", message=message, lvl=lvl)

def change_file_time(path, delta):
    if not os.path.exists(path):
        log_message("Pfad: " + path + " existiert nicht!", "info")
        return
    if platform.system() == "Windows":
        # modify filetimes on Windows
        fh = CreateFile(path, GENERIC_WRITE, 
                        FILE_SHARE_WRITE, None, 
                        OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, 0)
        cTime, aTime, mTime = GetFileTime(fh)
        cTime = datetime.fromtimestamp(cTime.timestamp() - delta)
        aTime = datetime.fromtimestamp(aTime.timestamp() - delta)
        mTime = datetime.fromtimestamp(mTime.timestamp() - delta)
        SetFileTime(fh, cTime, aTime, mTime)
        CloseHandle(fh)
    else:
        # modify filetimes on Linux/Mac
        a_time = os.path.getatime(path)
        m_time = os.path.getmtime(path)
        a_time = a_time - delta
        m_time = m_time - delta
        os.utime(path, (a_time, m_time))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)