"""
Random programs that fit nowhere else
"""

import threading

class StateMachine:
    """
    Locking machine that can have decorated callbacks
    and controls the flow based on some state, that can be accessed by the callback
    and is lockable.
    """
    def __init__(self, states, paths):
        self.lock = threading.Lock()
        self.current = ...
        self._states = ...  # this should be property based
        self._stack = deque()  # this should be for holding various data

    def _perform(self, name, source, target):
        """
        perform on_leave[source]
        perform on_path[name]
        perform on_enter[target]
        actually change the state
        exception will cancel the operation and enter on_error
        """

    def reset(self):
        pass

    def when(self, key):
        pass

    def when_not(self, key):
        pass

    def wait_until(self, key):
        pass

    def wait_until_not(self, key):
        pass

    def on_enter(self, key):
        pass

    def on_leave(self, key):
        pass

    @property
    def on_error(self):
        pass

    def on_path(self, vertex):
        pass


def state_machine_tests():
    s = StateMachine(["A", "B", "C"])
    @s.when("A")
    def state_that_A(_, to_whom):
        print("{}! I'm in state A!".format(to_whom))
    
    @s.when_not("A")
    def state_that_not_A(_, to_whom):
        print("{}! I'm allowed to be called, because I left state A!".format(to_whom))
    
    @s.on_enter("A")
    def state_entering_A(_, to_whom):
        print("{}! I'm allowed to be called, because I left state A!".format(to_whom))
    
    @s.on_leave("A")
    def state_leaving_A(_, to_whom):
        print("{}! I'm allowed to be called, because I left state A!".format(to_whom))

    @s.on_error
    def error_happened(_, err):
        pass
