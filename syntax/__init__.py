"""
The module of alternative extensions to Python.
`from syntax import *`

Finished features:
- anonymous objects via `new`
- signature typecheck via `@typed`
- dataclass init with normal classes with `@constructor`
- it method getting and mapping via `it` and `|`, `|-`
- github importer

Being done:
- extension methods for common types, i.e. replace for lists

To do:
- return() <- returns with after_return code
- fancy use of & (sending to thread?)
- fancy use of ^
- abbrevation for Pipeline(function)
- parallel (multithread, multiprocessing)
- use the pipe from syntax sugar to make longer pipes... (but do not duplicate)
- add tensor comprehensions
"""

from syntax.anon import new
from syntax.decorators import typed, constructor
from syntax.maps import it, _, Pipeable
from syntax.snip import remote_import
