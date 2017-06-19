from threading import Thread
from queue import Queue, Empty

class Job:
    """class Job"""
    def before(self):
        pass
    def on(self):
        pass
    def after(self):
        pass
    def do(self):
        """do this job"""
        self.before()
        self.on()
        self.after()

def do_once(joblist, maxjobs = 1):
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
                except Exception as err:
                    e = err
                q.task_done()
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
