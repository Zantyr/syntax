## When you import this, tests should run

from . import *

assert (3 | it) == 3
assert (3 | (it + 3)) == 6
assert (3 | (3 + it)) == 6
assert ("Asdf" | ("34" + it)) == "34Asdf"
assert ([1, 2, 3] | it.replace(3, 4)) == [1, 2, 4]
assert (3 | (not it)) == False