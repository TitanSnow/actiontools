from .job import Job, TemporarilyNotAvailable

class Target(Job):
    """class Target"""
    def __init__(self, deps = []):
        """init target with deps"""
        self.deps = deps

    def dep_satisfied(self):
        """check whether deps have satisfied"""
        raise NotImplementedError()

    def is_satisfied(self):
        """check whether self has satisfied"""
        raise NotImplementedError()

class DepNotSatisfied(TemporarilyNotAvailable):
    def __init__(self, err_msg = "Dep not satisfied"):
        super().__init__(err_msg)

class Phony(Target):
    """class Phony"""
    def dep_satisfied(self):
        """check whether deps have satisfied"""
        for dep in self.deps:
            if not dep.is_satisfied():
                return False
        return True

    _satisfied = False

    def is_satisfied(self):
        """check whether self has satisfied"""
        return self._satisfied

    def _set_satisfied(self):
        """set state to satisfied"""
        self._satisfied = True

    def _clear_satisfied(self):
        """clear state to satisfied"""
        self._satisfied = False

    def do(self):
        """
        do this phony
        raise `DepNotSatisfied` if dep not satisfied
        do nothing if self is satisfied
        after job done, set state to satisfied
        """
        if not self.is_satisfied():
            if self.dep_satisfied():
                super().do()
                self._set_satisfied()
            else:
                raise DepNotSatisfied()

class CannotSatisfy(RuntimeError):
    def __init__(self, err_msg = "Deps cannot satisfiy"):
        super().__init__(err_msg)

def dep_walk(target, visited = set()):
    """
    walk deps for a target
    raise `CannotSatisfy` if there is recursion ref
    return a set of targets walked
    """
    if target.is_satisfied():
        return set()
    else:
        rst = set([target])
        for dep in [dep for dep in target.deps if not dep.is_satisfied()]:
            if dep in visited or dep is target:
                raise CannotSatisfy()
            else:
                rst |= dep_walk(dep, visited | set([target]))
        return rst
