# Copyright (c) 2017 TitanSnow; All Rights Reserved


from hashlib import sha1
from os import fstat
from typing import Tuple, BinaryIO

Fileid = Tuple[str, bytes]

def fget_file_hashcode(f: BinaryIO, bufsize: int = 1024*1024) -> bytes:
    """get hashcode of a fileobj"""
    filestat = fstat(f.fileno())
    content = ('%032d%032d%032d%032d' % (filestat.st_mode, filestat.st_uid, filestat.st_gid, filestat.st_size)).encode('ascii')
    hashobj = sha1()
    hashobj.update(content)
    while True:
        content = f.read(bufsize)
        if content:
            hashobj.update(content)
        else:
            break
    return hashobj.digest()

def get_file_hashcode(pathname: str) -> bytes:
    """get hashcode of a given path"""
    with open(pathname, "rb") as f:
        return fget_file_hashcode(f)

def get_fileid(pathname: str) -> Fileid:
    """get fileid of a given path"""
    return pathname, get_file_hashcode(pathname)
