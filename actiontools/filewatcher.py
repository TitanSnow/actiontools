from typing import Optional, Callable
from .fileid import get_fileid, Fileid
from .storage import *

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
