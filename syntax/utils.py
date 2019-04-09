import os as _os
import pickle as _pickle
from collections import UserDict as _UserDict


class PersistentState(_UserDict):
    def __init__(self, path):
        self.path = path
        if _os.path.isfile(path):
            with open(path, "rb") as f:
                self.data = _pickle.load(f)
        else:
            self.data = {}

    def copy(self):
        raise ValueError("Cannot create a new instance of PersistentState at the same path")

    def __getitem__(self, k):
        return self.data[k]

    def __setitem__(self, k, v):
        # ensure that v is pickleable
        self.data[k] = v
        with open(self.path, "wb") as f:
            _pickle.dump(self.data, f)

    def __delitem__(self, k):
        del self.data[k]

    def __contains__(self, what):
        return self.data.__contains__(what)

    def __iter__(self):
        return self.data.__iter__()
