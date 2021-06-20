from __future__ import absolute_import


import sys

import stbt


MAX_ALLOWED_STATE_CHANGES = 20
class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.iterations = 0

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        global MAX_ALLOWED_STATE_CHANGES
        count = 0
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise InitializationError("at least one state must be an end_state")
        while True:
            stbt.debug(">>> Info >>>STATE CHANGE NUMBER: " + str(self.iterations))
            if self.iterations >= MAX_ALLOWED_STATE_CHANGES:
                stbt.debug(">>> Error >>> Maximum state changes reached!")
                stbt.draw_text("[StateMachine][Error] Maximum state changes reached!", duration_secs=4)
                raise_fail()

            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                stbt.debug(">>> Info >>> Endpoint state reached")
                stbt.draw_text("[StateMachine] Endpoint " + newState + " state reached", duration_secs=4)
                break
            else:
                self.iterations += 1
                stbt.draw_text("[StateMachine] Applying state " + newState, duration_secs=4)
                handler = self.handlers[newState.upper()]


def raise_fail():
    sys.exit(-1)
