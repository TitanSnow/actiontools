from threading import Thread, Lock, Event
from collections import deque

class Jobclient:
    def __init__(self):
        self._distlock = Lock()
        self._distevet = Event()
        self._jobqueue = deque()
        self._lasterror = None
        self._jobthread = Thread(target = self._threadwork)
        self._jobthread.start()

    def _threadwork(self):
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
        if not self._distlock.acquire(blocking, timeout):
            return False
        self._jobqueue += args
        self._distevet.set()
        self._distlock.release()
        return True

    def get_lasterror(self):
        return self._lasterror

    def wait(self, blocking = True, timeout = -1):
        if not self._distlock.acquire(blocking, timeout):
            return False
        self._distlock.release()
        return True

    def join(self, blocking = True, timeout = -1):
        if not self.do(None, blocking = blocking, timeout = timeout):
            return False
        self._jobthread.join()
        return True

    def is_alive(self):
        return self._jobthread.is_alive()
