"""
Library for quasi strings converted to Python modules from other language
"""

import hashlib
from syntax.config_manager import ConfigManager
from syntax.utils import Cache
from syntax.decorators import implicit

def load_so(filename):
    pass

def cpp_compile(program, filename, use):
    pass

def cpp(program_string, use=None):
    """
    Compile the string, make Python module
    """
    cache = implicit(Cache(ConfigManager.get_manager()['cache_path']))
    hash = hashlib.sha256(program_string).digest().hex()
    filename = cache.get_hash(hash)
    if filename is None:
        filename = cache.get_path(hash)
        cpp_compile(program_string, filename, use=use)
    return load_so(filename)
