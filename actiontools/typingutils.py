from typing import _ForwardRef as ForwardRef

def eval_forward_ref(ref: ForwardRef, globalns, localns):
    return ref._eval_type(globalns, localns)
