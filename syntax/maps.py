class Pipeable:
    """
    Any callback that can be evaluated via piping.
    Can be negated to become a map
    Can be unchained with unary + (changes it into lambda)
    """
    def __init__(self, callback):
        self._eval = callback
    
    def __ror__(self, other):
        return self._eval(other)

    def __neg__(self):
        return Pipeable(lambda x: [self._eval(x) for x in x])


class DelayedAccessor(Pipeable):
    """
    Creates delayed accessor
    """

    def __getattribute__(self, v):
        if v not in ["__ror__", "_eval", "__neg__", "__pos__", "__init__", "__add__"]:
            return DelayedAccessor(lambda x: self._eval(x).__getattribute__(v))
        else:
            return super().__getattribute__(v)

    def __str__(self):
        return DelayedAccessor(lambda x: self._eval(x).__str__())

    def __pos__(self):
        return lambda x: x | self

    def __call__(self, *args):
        return DelayedAccessor(lambda x: self._eval(x)(*args))

    def __add__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) + other)

    def __sub__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) - other)

    def __mul__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) * other)

    def __truediv__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) / other)

    def __floordiv__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) // other)

    def __pow__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) ** other)

    def __lshift__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) << other)

    def __rshift__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) >> other)

    def __lt__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) < other)

    def __le__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) <= other)

    def __eq__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) == other)

    def __ne__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) != other)

    def __gt__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) > other)

    def __ge__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) >= other)


it = DelayedAccessor(lambda x: x)
_ = it

