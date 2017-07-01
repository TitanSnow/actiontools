# Copyright (c) 2017 TitanSnow; All Rights Reserved


from typing import AbstractSet, FrozenSet, Optional, Union, Mapping
from os import path
from .job import Job, TemporarilyNotAvailable
from .typingutils import ForwardRef, type_check
from . import filewatcher

class Target(Job):
    """class Target"""
    def __init__(self, deps: AbstractSet['Target'] = frozenset()) -> None:
        """init target with deps"""
        try:
            self.deps
        except AttributeError:
            self.deps = set(deps)
        else:
            try:
                self.deps.update(deps)
            except AttributeError:
                self.deps = set(self.deps) | deps

    def dep_satisfied(self) -> bool:
        """check whether deps have satisfied"""
        raise NotImplementedError()

    def is_satisfied(self) -> bool:
        """check whether self has satisfied"""
        raise NotImplementedError()

class DepNotSatisfied(TemporarilyNotAvailable):
    """Exception DepNotSatisfied"""
    def __init__(self, err_msg: str = "Dep not satisfied") -> None:
        super().__init__(err_msg)

class Phony(Target):
    """class Phony"""
    def dep_satisfied(self) -> bool:
        """check whether deps have satisfied"""
        for dep in self.deps:
            if not dep.is_satisfied():
                return False
        return True

    _satisfied = False

    def is_satisfied(self) -> bool:
        """check whether self has satisfied"""
        return self._satisfied

    def _set_satisfied(self) -> None:
        """set state to satisfied"""
        self._satisfied = True

    def _clear_satisfied(self) -> None:
        """clear state to satisfied"""
        self._satisfied = False

    def do(self) -> None:
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

class Update(Phony):
    """class Update"""
    def is_updated(self) -> bool:
        """check whether self is updated"""
        raise NotImplementedError()

    def need_update(self) -> bool:
        """check whether self needs update"""
        returnval = False
        for dep in [dep for dep in self.deps if isinstance(dep, Update)]:
            if dep.is_updated():
                returnval = True
        return returnval

    def do(self) -> None:
        """
        do this update
        raise `DepNotSatisfied` if dep not satisfied
        do nothing if self is satisfied or no update needed
        after job done, set state to satisfied
        """
        if not self.need_update():
            self._set_satisfied()
        else:
            super().do()

class File(Update):
    """class File"""
    def is_updated(self) -> bool:
        """check whether self is updated by checking file"""
        try:
            return self._updated
        except AttributeError:
            self._updated = filewatcher.get_is_updated(self.file)
            return self._updated

    def need_update(self) -> bool:
        """check whether self needs update"""
        return not path.exists(self.file) or super().need_update()

    def __init__(self, file: Optional[str] = None, deps: AbstractSet[Target] = frozenset()) -> None:
        """init file with file and deps"""
        super().__init__(deps)
        if file is not None:
            self.file = file

class DepCannotSatisfy(RuntimeError):
    """Exception DepCannotSatisfy"""
    def __init__(self, err_msg: str = "Deps cannot satisfiy") -> None:
        super().__init__(err_msg)

def dep_walk(target: Target, visited: AbstractSet[Target] = frozenset()) -> FrozenSet[Target]:
    """
    walk deps for a target
    raise `DepCannotSatisfy` if there is recursion ref
    return a set of targets walked
    """
    if target.is_satisfied():
        return frozenset()
    else:
        rst = frozenset([target])
        for dep in [dep for dep in target.deps if not dep.is_satisfied()]:
            if dep in visited or dep is target:
                raise DepCannotSatisfy()
            else:
                rst |= dep_walk(dep, visited | frozenset([target]))
        return rst


ForwardTargetType = Union['ForwardTarget', ForwardRef, str, type]

class ForwardTarget(Target):
    """class ForwardTarget"""
    def __init__(self, deps: AbstractSet[ForwardTargetType] = frozenset()) -> None:
        """init target with deps"""
        super().__init__()
        self.deps.update(deps)

def dep_eval_type(target: ForwardTarget, globalns, localns, inited_objs: Mapping = dict()) -> ForwardTarget:
    """
    eval the types in dep tree of given target
    returns the same target passed in. will modify origin target
    """
    inited_objs = {**inited_objs}
    new_deps = set()
    old_deps = target.deps
    for dep in old_deps:
        dep_type = type_check(dep)
        if isinstance(dep_type, ForwardRef):
            if dep_type not in inited_objs:
                inited_objs[dep_type] = dep_type.eval_type(globalns, localns)()
            dep_instance = inited_objs[dep_type]
            new_deps.add(dep_instance)
        elif isinstance(dep, type):
            if dep not in inited_objs:
                inited_objs[dep] = dep()
            dep_instance = inited_objs[dep]
            new_deps.add(dep_instance)
        else:
            new_deps.add(dep)
    target.deps = new_deps
    for dep in new_deps:
        dep_eval_type(dep, globalns, localns, inited_objs)
    return target
