import shelve
from getpass import getuser
from os import getpid, path

Shelf = shelve.Shelf

def open_local() -> Shelf:
    return shelve.open(".actiontools_local_storage_" + getuser())

def open_session() -> Shelf:
    return shelve.open(".actiontools_session_storage_" + str(getpid()))

def open_global() -> Shelf:
    return shelve.open(path.join(path.expanduser("~"), ".actiontools_global_storage"))
