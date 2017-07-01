# Copyright (c) 2017 TitanSnow; All Rights Reserved


from threading import Thread
from queue import Queue, Empty
from time import sleep
from typing import Collection, Optional
from .storage import get_storage, join_storage_path
from .lisp import LispMachine

class Job:
    """class Job"""
    def before(self) -> None:
        pass
    def on(self) -> None:
        pass
    def after(self) -> None:
        pass
    def do(self) -> None:
        """do this job"""
        self.before()
        self.on()
        self.after()

class TemporarilyNotAvailable(RuntimeError):
    """Exception TemporarilyNotAvailable"""
    def __init__(self, err_msg: str = "Temporarily not available. Retry needed") -> None:
        super().__init__(err_msg)

def do_once(joblist: Collection[Job], maxjobs: Optional[int] = None, idle_wait_sleeptime: Optional[float] = None):
    """
    do `maxjobs` of jobs at once
    if maxjobs <= 0, it will be set to len(joblist)
    """
    if maxjobs is None:
        maxjobs = get_storage(join_storage_path([__name__, 'do_once', 'maxjobs']), 1)
    if idle_wait_sleeptime is None:
        idle_wait_sleeptime = get_storage(join_storage_path([__name__, 'do_once', 'idle_wait_sleeptime']), 0.01)
    if maxjobs <= 0:
        maxjobs = len(joblist)
    q = Queue()
    e = None
    def thread_func():
        nonlocal e
        try:
            while e is None:
                job = q.get_nowait()
                try:
                    job.do()
                except TemporarilyNotAvailable:
                    q.put(job)
                    sleep(idle_wait_sleeptime)
                except Exception as err:
                    e = err
        except Empty:
            pass
    for item in joblist:
        q.put(item)
    threads = [Thread(target = thread_func) for i in range(maxjobs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    if e is not None:
        raise e

class LispJob(Job):
    """class LispJob"""
    _lisp_machine = None
    before_ = []
    on_     = []
    after_  = []
    def before(self) -> None:
        """prepare lisp machine and eval `self.before_`"""
        self._lisp_machine = LispMachine()
        self._lisp_machine.eval(self.before_)
    def on(self) -> None:
        """eval `self.on_`"""
        self._lisp_machine.eval(self.on_)
    def after(self) -> None:
        """eval `self.after_`"""
        self._lisp_machine.eval(self.after_)
