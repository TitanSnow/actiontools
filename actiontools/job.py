# Copyright (c) 2017 TitanSnow; All Rights Reserved


from threading import Thread
from queue import Queue, Empty
from time import sleep
from typing import Collection

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

def do_once(joblist: Collection[Job], maxjobs: int = 1, idle_wait_sleeptime: float = 0.01):
    """
    do `maxjobs` of jobs at once
    if maxjobs <= 0, it will be set to len(joblist)
    """
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
