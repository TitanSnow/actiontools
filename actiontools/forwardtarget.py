# Copyright (c) 2017 TitanSnow; All Rights Reserved


from typing import Union, Mapping
from .typingutils import ForwardRef, type_check
from .target import *

ForwardTargetType = Union['ForwardTarget', ForwardRef, str, type]

class ForwardTarget(Target):
    """class ForwardTarget"""
    def __init__(self, deps: AbstractSet[ForwardTargetType] = frozenset()) -> None:
        """init target with deps"""
        super().__init__()
        self.deps.update(deps)

class ForwardPhony(ForwardTarget, Phony):
    """class ForwardPhony"""
    pass

class ForwardUpdate(ForwardTarget, Update):
    """class ForwardUpdate"""
    pass

class ForwardFile(ForwardTarget, File):
    """class ForwardFile"""
    pass

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
