import shelve
from getpass import getuser
from os import getpid, path

def open_local():
    return shelve.open(".actiontools_local_storage_" + getuser())

def open_session():
    return shelve.open(".actiontools_session_storage_" + str(getpid()))

def open_global():
    return shelve.open(path.join(path.expanduser("~"), ".actiontools_global_storage"))
