from argparse import ArgumentParser
import shelve
from pprint import pprint
from . import storage

def storage_main():
    """actiontools-storage"""
    parser = ArgumentParser()
    parser.add_argument('action', help = 'specify action to do', choices = ['list', 'get', 'set'])
    whichdb_group = parser.add_mutually_exclusive_group(required = True)
    whichdb_group.add_argument('--global', help = 'access global db', action = 'store_true')
    whichdb_group.add_argument('--local', help = 'access local db', action = 'store_true')
    whichdb_group.add_argument('--session', help = 'access session db', action = 'store_true')
    whichdb_group.add_argument('--file', help = 'access specified file db', action = 'store')
    whichdb_group.add_argument('--all', help = 'list all db', action = 'store_true')
    parser.add_argument('--delete', help = 'delete specified key in set action', action = 'store_true')
    parser.add_argument('key', help = 'specify key in set/get action', nargs = '?')
    parser.add_argument('value', help = 'specify value in set action', nargs = '?')
    arg = parser.parse_args()
    if getattr(arg, 'global'):
        db = storage.open_global()
    elif arg.local:
        db = storage.open_local()
    elif arg.session:
        db = storage.open_session()
    elif arg.file:
        db = shelve.open(arg.file)
    if arg.action == 'list':
        if arg.all:
            pprint({
                "global": {**storage.open_global()},
                "local": {**storage.open_local()},
                "session": {**storage.open_session()},
            })
        else:
            pprint({**db})
    elif arg.action == 'get':
        if arg.all:
            pprint(storage.get_storage(arg.key))
        else:
            pprint(db[arg.key])
    elif arg.action == 'set':
        if arg.delete:
            del db[arg.key]
        else:
            db[arg.key] = arg.value
    return 0
