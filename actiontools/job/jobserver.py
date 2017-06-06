from .jobclient import Jobclient
from threading import Thread, Lock, Event

class Jobserver:
    """
    Jobserver class
    the class to manage jobclients
    """

    def __init__(self, njc = 1):
        """
        init jobserver
        njc: number of jobclients
        """
        self._idleevet = Event()
        self._distevet = Event()
        self._distlock = Lock()
        self._distlist = []
        self._lasterror = None
        self._client = [Thread(target = self._waitclient) for i in range(njc)]
        for c in self._client:
            c.start()

    def _waitclient(self):
        """thread function to wait jobclient"""
        client = Jobclient()
        while True:
            self._idleevet.set()
            self._distevet.wait()
            self._distlock.acquire()
            distlist = self._distlist
            self._distlist = []
            self._distevet.clear()
            self._distlock.release()
            if distlist:
                if None in distlist:
                    client.join()
                    return
                client.do(*distlist)
                client.wait()
                if client.get_lasterror():
                    self._lasterror = client.get_lasterror()

    def do(self, *args):
        """
        do jobs
        returns whether all jobs succeeded
        """
        for job in args:
            self._idleevet.wait()
            if self._lasterror:
                return False
            self._distlist = [job]
            self._idleevet.clear()
            self._distevet.set()
        return True

    def wait(self, timeout = None):
        """wait until idle"""
        return self._idleevet.wait(timeout)

    def get_lasterror(self):
        """returns lasterror"""
        return self._lasterror

    def join(self):
        """join jobclients"""
        self.do(*[None] * len([c for c in self._client if c.is_alive()]))
        for c in self._client:
            c.join()

    def __del__(self):
        self.join()
