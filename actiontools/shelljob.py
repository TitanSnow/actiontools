from .job import *
from .callexternal import do_shells

class ShellJob(Job):
    shells_before = []
    shells_on = []
    shells_after = []
    shells_flag_before = ''
    shells_flag_on = ''
    shells_flag_after = ''
    def before(self) -> None:
        do_shells(self.shells_before, self.shells_flag_before)
    def on(self) -> None:
        do_shells(self.shells_on, self.shells_flag_on)
    def after(self) -> None:
        do_shells(self.shells_after, self.shells_flag_after)
