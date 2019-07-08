"""
Random programs that fit nowhere else
"""

import collections as _collections
import copy as _copy
import os as _os
import pickle as _pickle
import shutil as _shutil
import sys as _sys
import tempfile as _tempfile
import threading as _threading
import time as _time
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
        start_time = _time.time()
        timed(*args, **kwargs)
        end_time = _time.time() - start_time
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


class StateMachine:
    """
    Locking machine that can have decorated callbacks
    and controls the flow based on some state, that can be accessed by the callback
    and is lockable.
    """
    def __init__(self, states, paths=None):
        self.lock = _threading.Lock()
        self._states = states[:]  # this should be property based
        self._current = self._states[0]
        self._stack = _collections.deque()  # this should be for holding various data
        self._legal = paths[:] if paths is not None else None
        self._on_illegal = None
        self._on_error = None
        self._on_enter = {}
        self._on_leave = {}
        self._on_path = {}

    @property
    def state(self):
        with self.lock:
            return self._current

    @state.setter
    def state(self, value):
        with self.lock:
            passage = (self._current, value)
            try:
                assert value in self._states
                if self._legal is not None:
                    assert passage in self._legal
            except AssertionError:
                if self._on_illegal is not None:
                    self._on_illegal(passage)
            else:
                try:
                    on_leave = self._on_leave.get(self._current)
                    if on_leave is not None:
                        on_leave(self._stack, value)
                    on_path = self._on_path.get(passage)
                    if on_path is not None:
                        on_path(self._stack)
                    on_enter = self._on_enter.get(value)
                    if on_enter is not None:
                        on_enter(self._stack, self._current)
                    self._current = value
                except Exception as error:
                    self._on_error(self._stack, passage, error)

    def wait_until(self, key):
        while True:
            with self.lock:
                if self._current == key:
                    break
            _time.sleep(0)

    def wait_until_not(self, key):
        while True:
            with self.lock:
                if self._current != key:
                    break
            time.sleep(0)

    def on_enter(self, key):
        def wrapper(f):
            self._on_enter[key] = f
            return f
        return wrapper

    def on_leave(self, key):
        def wrapper(f):
            self._on_leave[key] = f
            return f
        return wrapper

    def on_path(self, vertex):
        def wrapper(f):
            self._on_path[key] = f
            return f
        return wrapper

    @property
    def on_error(self):
        def wrapper(f):
            self._on_error = f
            return f
        return wrapper
                
    @property
    def on_illegal(self):
        def wrapper(f):
            self._on_illegal = f
            return f
        return wrapper



class Invoke:
    def __call__(self, args=None):
        if args is None:
            args = _sys.argv[1:]
        if len(args) == 0:
            return self.help()
        keys = [x for x in dir(self) if not x.startswith("_")]
        for k in keys:
            if k == args[0]:
                return getattr(self, k)(*args[1:])
        else:
            return self.help()

    def help(self):
        """Print this help"""
        print(self._about, end="\n\n")
        keys = [x for x in dir(self) if not x.startswith("_")]
        for k in keys:
            print("{} - {}".format(k, getattr(self, k).__doc__))


class StringBuilder:
    """
    Builder of large amount of text from small pieces
    """
    def __init__(self, *strings, sep=' ', end='\n'):
        self.string = ""
        self.print(*strings, sep=' ', end='\n')

    def print(self, *strings, sep=' ', end='\n'):
        self.string += sep.join(strings) + end
