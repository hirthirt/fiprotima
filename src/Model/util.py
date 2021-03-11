import os
from pubsub import pub
import platform

if platform.system() == "Windows":
    from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
    from win32file import GENERIC_WRITE, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, FILE_SHARE_WRITE

def log_message(message, lvl):
    pub.sendMessage("logging", message=message, lvl=lvl)

def change_file_time(path, delta):
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