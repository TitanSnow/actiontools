import subprocess
from typing import Iterable
from .storage import get_storage, join_storage_path

def vdo_shell(cmd: str) -> None:
    print(cmd)
    subprocess.check_call(cmd, shell = True)

def vdo_shells(cmds: Iterable[str]) -> None:
    for cmd in cmds:
        vdo_shell(cmd)

def qdo_shell(cmd: str) -> None:
    subprocess.check_call(cmd, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

def qdo_shells(cmds: Iterable[str]) -> None:
    for cmd in cmds:
        qdo_shell(cmd)

def do_shell(cmd: str) -> None:
    if get_storage(join_storage_path(['actiontools', 'verbose'])) is True:
        vdo_shell(cmd)
    else:
        qdo_shell(cmd)

def do_shells(cmds: Iterable[str]) -> None:
    for cmd in cmds:
        do_shell(cmd)
