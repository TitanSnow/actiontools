# Copyright (c) 2017 TitanSnow; All Rights Reserved


from .job import *
from .callexternal import calls

class ShellJob(Job):
    """class ShellJob"""
    shells_before = []
    shells_on = []
    shells_after = []
    shells_flag_before = ''
    shells_flag_on = ''
    shells_flag_after = ''
    def before(self) -> None:
        """do `self.shells_before` with flag `self.shells_flag_before`"""
        calls(self.shells_before, self.shells_flag_before)
    def on(self) -> None:
        """do `self.shells_on` with flag `self.shells_flag_on`"""
        calls(self.shells_on, self.shells_flag_on)
    def after(self) -> None:
        """do `self.shells_after` with flag `self.shells_flag_after`"""
        calls(self.shells_after, self.shells_flag_after)
