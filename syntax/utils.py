import copy as _copy
import os as _os
import pickle as _pickle
import shutil as _shutil
import sys as _sys
import tempfile as _tempfile
import zipfile as _zipfile

from collections import UserDict as _UserDict


class PersistentState(_UserDict):
    """
    Creates a dict that autoserializes to the filesystem
    """
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


class Cache:
    def __init__(self, path):
        self.path = path

    def get_hash(self, hash):
        if _os.path.exists(_os.path.join(self.path, str(hash))):
            return _os.path.exists(_os.path.join(self.path, str(hash)))
        return None
        

def zdict(*args):
    return dict(zip(*args))

def lrange(arg):
    return range(len(arg))

def timer(timed):
    """@timeit but logs instead of printing"""
    def timer_wrapper(*args, **kwargs):
        start_time = time.time()
        timed(*args, **kwargs)
        end_time = time.time() - start_time
        logger.info('%s done in %s seconds', timed.__name__, round(end_time, 2))
    return timer_wrapper


class Frame(_UserDict):
    """
    For interpreter development - frame for function call and so on
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.data = data

    def setv(self, k, v):
        while self.parent is not None:
            self = self.parent
        self.data[k] = v

    def new_frame(self):
        return Frame(self)

    def copy(self):
        return _copy.copy(self)

    def __getitem__(self, k):
        if k in self.data.keys():
            return self.data[k]
        if self.parent is not None:
            return self.parent[k]
        raise KeyError("No such item as {}".format(k))

    def __setitem__(self, k, v):
        self.data[k] = v

    def __delitem__(self, k):
        del self.data[k]

    def __contains__(self, what):
        return self.data.__contains__(what)

    def __iter__(self):
        return self.data.__iter__()


class TempEnv:
    """
    Create a temporary directory. If path is given, the temporary dir is zipped and unzipped
    accordingly.
    """
    def __init__(self, path=None):
        self.path = None

    def __enter__(self):
        tmpdname = _tempfile.mkdtemp()
        if self.path is not None:
            with _zipfile.ZipFile(self.path) as f:
                f.extractall(tmpdname)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path is not None:
            with _zipfile.ZipFile(self.path, 'w') as f:
                for root, folders, files in _os.walk():
                    for file in files:
                        f.write(_os.path.join(root, file))
        _shutil.rmtree(tmpdname)


"""
Requirements for LISP VM
Correctly allocate and deallocate things at enter, exit or rewrite
Since functions are stateless, there is no need to manage external state really - the creator
is responsible for deletion unless the item is returned
Create incremental items -> when Mutated object is returned, the original is also undeallocated

Also, refcount GC...
"""



def yes_no(question):
    """
    Ask a yes/no question
    """
    prompt = " [y/n] "
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    while True:
        _sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            _sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")



class DotDict(dict):
    """
    Convenience collection
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return super().__getattr__(self, key)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            return super().__setattr__(self, key, value)
        self[key] = value
