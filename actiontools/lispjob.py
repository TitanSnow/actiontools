# Copyright (c) 2017 TitanSnow; All Rights Reserved


from .lisp import LispMachine
from .job import Job

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
