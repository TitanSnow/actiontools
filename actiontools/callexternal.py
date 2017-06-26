# Copyright (c) 2017 TitanSnow; All Rights Reserved


import subprocess
from typing import Callable
from .storage import *

def call(*cmd) -> None:
    if get_storage(join_storage_path(['actiontools', 'verbose'])) is True:
        print(cmd)
        subprocess.check_call(cmd)
    else:
        subprocess.check_call(cmd, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

def shell(cmd: str) -> None:
    if get_storage(join_storage_path(['actiontools', 'verbose'])) is True:
        print(cmd)
        subprocess.check_call(cmd, shell = True)
    else:
        subprocess.check_call(cmd, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

def verbose(func: Callable, *args) -> Any:
    ph = join_storage_path(['actiontools', 'verbose'])
    with open_session() as db:
        try:
            origin = db[ph]
            db[ph] = True
            try:
                rv = func(*args)
            finally:
                db[ph] = origin
        except KeyError:
            db[ph] = True
            try:
                rv = func(*args)
            finally:
                del db[ph]
    return rv

def quiet(func: Callable, *args) -> Any:
    ph = join_storage_path(['actiontools', 'verbose'])
    with open_session() as db:
        try:
            origin = db[ph]
            db[ph] = False
            try:
                rv = func(*args)
            finally:
                db[ph] = origin
        except KeyError:
            db[ph] = False
            try:
                rv = func(*args)
            finally:
                del db[ph]
    return rv
