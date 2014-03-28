# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:26 2012

@author: Preston
"""

from inspect import getargspec
from Queue import Queue


class Rule(object):
    """Creates a new rule object which, has a name (for identification),
    a trigger, and a script,which is some executable python code, whether it is
    a function, lambda, compiled code object, or even an entire object
    (assuming it implements __call__). The only requriement for the code is
    that there is exactly one parameter that will represent the
    entire Server object"""
    def __init__(self, name, trigger, function):
        """name -- a simple name to easily identify a rule
        trigger -- card or phrase that invokes the rule

        script -- executable python code. Either a lambda, function, compiled
        code object, or class. The only requriement is that it takes one
        parametre, which will represnt the Server. A lambda is discouraged,
        as that is hard to identify (function name just gives "lambda" """
        assert type(name) == str
        self.name = name
        self.trigger = trigger
        # Make sure there is one and only one argument
        assert len(getargspec(script)[0]) == 1
        self.script = script

    def __repr__(self):
        return ("Rule named {} which executes '{}'").format(
            self.name, self.script.__name__)

if __name__ == '__main__':
    pass
