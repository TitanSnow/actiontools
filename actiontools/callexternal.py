# Copyright (c) 2017 TitanSnow; All Rights Reserved


import subprocess
from typing import Callable, Union, Iterable, Optional, Any, Sequence, IO
from functools import partial
from io import IOBase
from .storage import get_storage, join_storage_path, open_session

def _call(cmd: Union[str, Iterable[str]], shell: bool, protect: bool) -> Optional[bool]:
    try:
        if get_storage(join_storage_path(['actiontools', 'verbose'])) is True:
            print(cmd)
            subprocess.check_call(cmd, shell = shell)
        else:
            subprocess.check_call(cmd, shell = shell, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    except (subprocess.SubprocessError, OSError) as e:
        if not protect:
            raise e
        else:
            return False
    if protect:
        return True

call  = lambda *cmd: _call(cmd, False, False)
shell = lambda  cmd: _call(cmd, True,  False)
pcall  = lambda *cmd: _call(cmd, False, True)
pshell = lambda  cmd: _call(cmd, True,  True)

def _verbose(verbose: bool, func: Callable, *args) -> Any:
    ph = join_storage_path(['actiontools', 'verbose'])
    with open_session() as db:
        try:
            origin = db[ph]
            db[ph] = verbose
            try:
                rv = func(*args)
            finally:
                db[ph] = origin
        except KeyError:
            db[ph] = verbose
            try:
                rv = func(*args)
            finally:
                del db[ph]
    return rv

verbose = partial(_verbose, True)
quiet   = partial(_verbose, False)

def _pipe(cmds: Sequence[Union[Iterable[str], IO, str]], protect: bool) -> Optional[bool]:
    verbose = get_storage(join_storage_path(['actiontools', 'verbose'])) is True
    if verbose:
        print(cmds)
    if len(cmds):
        ff = isinstance(cmds[0],  IOBase)
        lf = isinstance(cmds[-1], IOBase)
        lastout = cmds[0] if ff else None
        try:
            for cmd in cmds[1 if ff else 0 : -2 if lf else -1]:
                p = subprocess.Popen(cmd, stdin = lastout, stdout = subprocess.PIPE, shell = isinstance(cmd, str))
                if lastout is not None: lastout.close()
                lastout = p.stdout
            if not lf:
                subprocess.check_call(cmds[-1], stdin = lastout, stdout = None if verbose else subprocess.DEVNULL, stderr = None if verbose else subprocess.DEVNULL, shell = isinstance(cmds[-1], str))
            elif len(cmds) >= (3 if ff else 2):
                subprocess.check_call(cmds[-2], stdin = lastout, stdout = cmds[-1], stderr = None if verbose else subprocess.DEVNULL, shell = isinstance(cmds[-2], str))
        except (subprocess.SubprocessError, OSError) as e:
            if not protect:
                raise e
            else:
                return False
    if protect:
        return True

pipe = lambda *cmds: _pipe(cmds, False)
ppipe = lambda *cmds: _pipe(cmds, True)
