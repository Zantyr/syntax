## When you import this, tests should run
## extended_tests.py

import unittest

from syntax import it, constructor
from syntax import typed
from syntax import StateMachine


class MethodPipeTests(unittest.TestCase):
    def test_methodpipes_1(self):
        assert (3 | it) == 3

    def test_methodpipes_2(self):
        assert (3 | (it + 3)) == 6

    def test_methodpipes_3(self):
        assert (3 | (3 + it)) == 6
                                                                
    def test_methodpipes_4(self):
        assert ("Asdf" | ("34" + it)) == "34Asdf"

    def test_methodpipes_5(self):
        assert ([1, 2, 3] | it.replace(3, 4)) == [1, 2, 4]

    def test_methodpipes_6(self):
        assert (3 | (not it)) == False


class Constructor(unittest.TestCase):
    def test_1(self):
        class X:
            @constructor
            def __init__(a):
                pass

        instance = X(3)
        assert instance.a == 3


class TypedTests(unittest.TestCase):
    def test_typed_1(self):
        try:
            @typed(str)
            def x(y):
                return y

            x(3)
        except:
            return True
        else:
            raise AssertionError

    def test_typed_2(self):
        try:
            @typed(str)
            def x(y):
                return y

            x("")
        except:
            raise AssertionError
        else:
            return True


class UtilsTests(unittest.TestCase):
    def test_on_enter_A(self):    
        s = StateMachine(["A", "B", "C"])
        s.state = "B"
        flag = [False]
        @s.on_enter("A")
        def state_entering_A(_, to_whom):
            flag[0] = True        
        s.state = "A"
        assert flag[0]

    def test_on_leave_A(self):
        s = StateMachine(["A", "B", "C"])
        flag = [False]
        @s.on_leave("A")
        def state_leaving_A(_, to_where):
            flag[0] = True        
        s.state = "B"
        assert flag[0]

    def test_on_illegal(self):
        s = StateMachine(["A", "B", "C"], [("A", "C")])
        flag = [False]
        @s.on_illegal
        def error_happened(_):
            flag[0] = True        
        s.state = "B"
        assert flag[0]


if __name__ == '__main__':
    unittest.main()
