def new(*args, **kwargs):
    """
    Create anonymous object with given keyword arguments. Automatically binds all functions
    as bound methods. Non-keyword arguments serve as base classes. Constructors are not run!
    """

    class AnonymousClass(*args):
        def __repr__(self):
            return "<AnonymousClass> {}".format(self.__dict__)

    obj = AnonymousClass()
    for k,v in kwargs.items():
        if type(v) == func_type:
            setattr(obj, k, types.MethodType(v, obj))
        elif type(v) == verbatim:
            setattr(obj, k, v.object)
        else:
            setattr(obj, k, v)
    return obj

