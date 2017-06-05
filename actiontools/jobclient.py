from threading import Thread, Lock, Event
from collections import deque

class Jobclient:
    """
    Jobclient class
    a jobclient is a thread to run jobs
    """
    def __init__(self):
        self._distlock = Lock()
        self._distevet = Event()
        self._jobqueue = deque()
        self._lasterror = None
        self._jobthread = Thread(target = self._threadwork)
        self._jobthread.start()

    def _threadwork(self):
        """the function for thread to run jobs"""
        while True:
            self._distevet.wait()
            self._distlock.acquire()
            self._distevet.clear()
            while self._jobqueue:
                job = self._jobqueue.popleft()
                if job is None:
                    self._distlock.release()
                    return
                try:
                    job.do()
                except Exception as e:
                    self._lasterror = e
                    break
            self._distlock.release()

    def do(self, *args, blocking = True, timeout = -1):
        """
        dist jobs
        if thread is doing jobs, wait to dist
        blocking: a bool to set whether wait blockly
        timeout: the wait timeout
        returns whether jobs are disted
        """
        if not self._distlock.acquire(blocking, timeout):
            return False
        self._jobqueue += args
        self._distevet.set()
        self._distlock.release()
        return True

    def get_lasterror(self):
        """returns last error in jobthread"""
        return self._lasterror

    def wait(self, blocking = True, timeout = -1):
        """wait jobthread to be distable"""
        if not self._distlock.acquire(blocking, timeout):
            return False
        self._distlock.release()
        return True

    def join(self, blocking = True, timeout = -1):
        """join jobthread"""
        if not self.is_alive() or not self.do(None, blocking = blocking, timeout = timeout):
            return False
        self._jobthread.join()
        return True

    def is_alive(self):
        """returns whether jobthread is alive"""
        return self._jobthread.is_alive()

    def __del__(self):
        self.join()
