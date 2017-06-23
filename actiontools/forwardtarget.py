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
    pass

class ForwardUpdate(ForwardTarget, Update):
    pass

class ForwardFile(ForwardTarget, File):
    pass

def dep_eval_type(target: ForwardTarget, globalns, localns, inited_objs: Mapping = dict()) -> None:
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
        else:
            new_deps.add(dep)
    target.deps = new_deps
    for dep in new_deps:
        dep_eval_type(dep, globalns, localns, inited_objs)
