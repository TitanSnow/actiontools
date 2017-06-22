import subprocess
from typing import Iterable

def vdo_shell(cmd: str) -> None:
    print(cmd)
    subprocess.check_call(cmd, shell = True)

def vdo_shells(cmds: Iterable[str]) -> None:
    for cmd in cmds:
        vdo_shell(cmd)
