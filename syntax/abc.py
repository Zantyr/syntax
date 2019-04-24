"""
list | G[:, ...] (getter)   (one capital letter programs...)
"""

from .anon import new as _new
from .maps import Pipeable as _Pipeable

def _getter(x, index):
    try:
        return x[index]
    except Exception:
        map_indices = []
        for i in index:
            if isinstance(i, slice):
                map_indices.append(True)
            else:
                map_indices.append(False)
            num = len([x for x in map_indices if x == True])
            if num:
                fn = ...
                while num:
                    fn = ...
                    num -= 1
                x = fn(x, i)
            else:
                x = x[i]
        return x

def _g_func(_, index):
    return _Pipeable(lambda x: _getter(x, index))

G = _new(__getitem__=_g_func)
