# Copyright (c) 2017 TitanSnow; All Rights Reserved


import subprocess
from typing import Iterable, Optional, Sequence
from .storage import get_storage, join_storage_path

def do_shell(cmd: str, flag: str = '') -> Optional[subprocess.CalledProcessError]:
    """
    do `cmd`
    `flag` is a str, the combination of log-control flag and error-ignore flag
    log-control flag can be one of 'v' (verbose), 'q' (quiet)
    when not specified, is controlled by whether storage 'actiontools.verbose' is True
    error-ignore flag is 'i'
    when specified, will return exception object instead of raise it
    when there raising subprocess.CalledProcessError on cmd starts with '-'
    """
    ignore = 'i' in flag and cmd.startswith('-')
    if ignore:
        cmd = cmd[1:]
    try:
        if 'v' in flag or ('q' not in flag and get_storage(join_storage_path(['actiontools', 'verbose'])) is True):
            print(cmd)
            subprocess.check_call(cmd, shell=True)
        else:
            subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        if not ignore:
            raise e
        else:
            return e

def do_shells(cmds: Iterable[str], flag: str = '') -> Sequence[Optional[subprocess.CalledProcessError]]:
    """
    do `cmds`.
    returns a list of return value returned by `do_shell`
    `flag` applies to all cmds, has same meaning as `do_shell`
    """
    return [do_shell(cmd, flag) for cmd in cmds]
