# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:26 2012

@author: Preston
"""

from inspect import getargspec
from Queue import Queue


class Rule(object):
    """Object that holds the information of a Mao game rule. Has a name for
    identification, a trigger to know when to execute, and a function to
    execute. The function requires a single argument which represent a server
    object"""
    def __init__(self, name, trigger, function):
        """
        Args:
            name(str): A simple name to easily identify a rule
            trigger(card or str): card or phrase that invokes the rule
        """
        self.name = named
        self.trigger = trigger
        # Make sure there is one and only one argument
        assert len(getargspec(function)[0]) == 1
        self.function = function

    def __repr__(self):
        return ("Rule named {} which executes '{}'").format(
            self.name, self.function.__name__)

if __name__ == '__main__':
    pass
