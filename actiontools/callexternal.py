# Copyright (c) 2017 TitanSnow; All Rights Reserved


import subprocess
from typing import Iterable, Optional, Sequence, Union
from .storage import get_storage, join_storage_path

class ctr(str):
    """cmd control node type"""
    pass

def call(cmd: Union[str, Sequence[str]], flag: str = '') -> Optional[Union[subprocess.SubprocessError, OSError]]:
    """
    do `cmd`
    `flag` is a str, the combination of log-control flag, error-ignore flag and shell flag
    log-control flag can be one of 'v' (verbose), 'q' (quiet)
    when not specified, is controlled by whether storage 'actiontools.verbose' is True
    error-ignore flag is 'i'
    when specified, will return exception object instead of raise it
    when there raising subprocess.SubprocessError or OSError on cmd starts with ctr '-'
    shell flag is 's'
    when specified, cmd will be parsed as a shell string
    """
    ignore = 'i' in flag and len(cmd) and isinstance(cmd[0], ctr) and cmd[0] == '-'
    shell = 's' in flag
    if ignore:
        cmd = cmd[1:]
    try:
        if 'v' in flag or ('q' not in flag and get_storage(join_storage_path(['actiontools', 'verbose'])) is True):
            print(cmd)
            subprocess.check_call(cmd, shell = shell)
        else:
            subprocess.check_call(cmd, shell = shell, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    except (subprocess.SubprocessError, OSError) as e:
        if not ignore:
            raise e
        else:
            return e

def calls(cmds: Iterable[Union[str, Sequence[str]]], flag: str = '') -> Sequence[Optional[Union[subprocess.SubprocessError, OSError]]]:
    """
    do `cmds`.
    returns a list of return value returned by `call`
    `flag` applies to all cmds, has same meaning as `call`
    """
    return [call(cmd, flag) for cmd in cmds]
