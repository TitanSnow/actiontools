from typing import Optional
from .fileid import get_fileid, get_abs_fileid, Fileid
from .storage import open_local, open_global

def get_stored_fileid(pathname: str) -> Optional[Fileid]:
    with open_local() as ls:
        return ls.get(pathname)

def set_stored_fileid(fid: Fileid) -> None:
    with open_local() as ls:
        ls[fid[0]] = fid

def peek_is_updated(pathname: str, newfid: Optional[Fileid] = None) -> bool:
    oldfid = get_stored_fileid(pathname)
    if oldfid is None:
        return True
    if newfid is None:
        newfid = get_fileid(pathname)
    return oldfid != newfid

def get_is_updated(pathname: str, newfid: Optional[Fileid] = None) -> bool:
    """
    get is updated of a given path
    this will update stored fileid
    """
    if newfid is None:
        newfid = get_fileid(pathname)
    is_updated = peek_is_updated(pathname, newfid)
    if is_updated:
        # update store
        set_stored_fileid(newfid)
    return is_updated

def get_abs_stored_fileid(pathname: str) -> Optional[Fileid]:
    with open_global() as gs:
        return gs.get(pathname)

def set_abs_stored_fileid(fid: Fileid) -> None:
    with open_global() as gs:
        gs[fid[0]] = fid

def peek_abs_is_updated(pathname: str, newfid: Optional[Fileid] = None) -> bool:
    oldfid = get_abs_stored_fileid(pathname)
    if oldfid is None:
        return True
    if newfid is None:
        newfid = get_abs_fileid(pathname)
    return oldfid != newfid

def get_abs_is_updated(pathname: str, newfid: Optional[Fileid] = None) -> bool:
    """
    get is updated of a given abspath
    this will update stored fileid
    """
    if newfid is None:
        newfid = get_abs_fileid(pathname)
    is_updated = peek_abs_is_updated(pathname, newfid)
    if is_updated:
        # update store
        set_abs_stored_fileid(newfid)
    return is_updated
