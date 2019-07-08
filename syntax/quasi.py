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

def generate_interface(_fun_name, _module_name, arg_dict):
    """
    Produces python code to C calls
    To be integrated to a larger module interface generator
    """
    signature = ", ".join([x for x in arg_dict.keys()])
    sb = StringBuilder()
    sb.print("def {}({}):".format(_fun_name, signature))
    sb.print("    mod = ctypes.CDLL('{}')".format(_module_name))
    sb.print("    fun = mod['{}']".format(_fun_name))
    sb.print("    cargs = []".format(_fun_name))
    for var, typ in arg_dict.items():
        type_func = "ctypes.c_int" # based on typ 
        type_conversion = "{}({})".format(type_func, var)
        sb.print("    cargs.append({})".format(type_conversion))
    sb.print("    return fun(*cargs)")
    print(sb.string)


# tests
if __name__ == "__main__":
    generate_interface("addition", "mymod.dll", {
        "x": "int",
        "y": "int"
    })