# Copyright (c) 2017 TitanSnow; All Rights Reserved


from typing import Optional, Callable, Tuple, BinaryIO
from hashlib import sha1
from os import fstat
from .storage import *

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

def get_stored_fileid(pathname: str) -> Optional[Fileid]:
    return get_storage(join_storage_path([__name__, 'files', pathname]))

def set_stored_fileid(fid: Fileid) -> None:
    set_local(join_storage_path([__name__, 'files', fid[0]]), fid)

def peek_is_updated(pathname: str, newfid: Optional[Fileid] = None) -> bool:
    oldfid = get_stored_fileid(pathname)
    if oldfid is None:
        return True
    if newfid is None:
        newfid = get_fileid(pathname)
    return oldfid != newfid

def get_is_updated(pathname: str, newfid: Optional[Fileid] = None, storer: Callable[[Fileid], None] = set_stored_fileid) -> bool:
    """
    get is updated of a given path
    this will update stored fileid
    """
    if newfid is None:
        newfid = get_fileid(pathname)
    is_updated = peek_is_updated(pathname, newfid)
    if is_updated:
        # update store
        storer(newfid)
    return is_updated

def set_global_stored_fileid(fid: Fileid) -> None:
    set_global(join_storage_path([__name__, 'files', fid[0]]), fid)
