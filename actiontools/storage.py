import shelve
from getpass import getuser
from os import getpid, path, remove
from typing import Any, Iterable
import re
import atexit

Shelf = shelve.Shelf

def del_session() -> None:
    try:
        remove(".actiontools_session_storage_" + str(getpid()))
    except FileNotFoundError:
        pass

atexit.register(del_session)

def open_session() -> Shelf:
    return shelve.open(".actiontools_session_storage_" + str(getpid()))

def open_local() -> Shelf:
    return shelve.open(".actiontools_local_storage_" + getuser())

def open_global() -> Shelf:
    return shelve.open(path.join(path.expanduser("~"), ".actiontools_global_storage"))

def get_storage(key: str) -> Any:
    with open_session() as db:
        if key in db:
            return db[key]
    with open_local() as db:
        if key in db:
            return db[key]
    with open_global() as db:
        if key in db:
            return db[key]

def set_session(key: str, value: Any) -> None:
    with open_session() as db:
        db[key] = value

def set_local(key: str, value: Any) -> None:
    with open_local() as db:
        db[key] = value

def set_global(key: str, value: Any) -> None:
    with open_global() as db:
        db[key] = value

def join_storage_path(path: Iterable[str]) -> str:
    return '.'.join((re.sub(r'\.', r'\.', re.sub(r'\\', r'\\\\', part)) for part in path))

def split_storage_path(path: str) -> Iterable[str]:
    arr = []
    is_escaping = False
    for ch in path:
        if is_escaping:
            is_escaping = False
            arr.append(ch)
        else:
            if ch == '\\':
                is_escaping = True
            elif ch == '.':
                yield ''.join(arr)
                arr = []
            else:
                arr.append(ch)
    yield ''.join(arr)
    return
