# Copyright (c) 2017 TitanSnow; All Rights Reserved


from .job import *
from .callexternal import calls

class ExternalJob(Job):
    """class ExternalJob"""
    calls_before = []
    calls_on = []
    calls_after = []
    flag_before = ''
    flag_on = ''
    flag_after = ''
    def before(self) -> None:
        """do `self.calls_before` with flag `self.flag_before`"""
        calls(self.calls_before, self.flag_before)
    def on(self) -> None:
        """do `self.calls_on` with flag `self.flag_on`"""
        calls(self.calls_on, self.flag_on)
    def after(self) -> None:
        """do `self.calls_after` with flag `self.flag_after`"""
        calls(self.calls_after, self.flag_after)
