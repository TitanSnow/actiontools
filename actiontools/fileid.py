from hashlib import sha1
from typing import Tuple
from os import path

def get_fileid(pathname: str) -> Tuple[str, bytes]:
    """get fileid with a given path"""
    with open(pathname, "rb") as f:
        filesize = f.seek(0, 2) # seek to end to get file size
        f.seek(0, 0)            # seek back to start
        # use filesize as prefix. leftpad to 32
        content_prefix = ('%032d' % filesize).encode('ascii')
        content = f.read()
        hashcode = sha1(content_prefix + content).digest()
        return (path.abspath(pathname), hashcode)
