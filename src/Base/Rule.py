# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:26 2012

@author: Preston
"""

from inspect import getargspec


class Rule(object):
    """Object that holds the information of a Mao game rule. Has a name for
    identification, a trigger to know when to execute, and a function to
    execute. The function requires a single argument which represent a server
    object"""
    def __init__(self, name, trigger, function):
        """Rule that has a name, trigger, and function to execute"""
        self.name = name
        self.trigger = trigger
        # Make sure there is one and only one argument
        assert len(getargspec(function)[0]) == 1, (
            "The function should take one and only one argument!")
        self.function = function

    def __call__(self, *args):
        return self.function(args[0])

    def __repr__(self):
        return ("Rule named {} which executes '{}'").format(
            self.name, self.function.__name__)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    def func_code(x):
        x += 1
        return x
    lambda_code = lambda x: x + 1

    lambda_rule = Rule("Lambda Test Rule", "Test Phrase", lambda_code)
    func_rule = Rule("Function Test Rule", "test phrase ", func_code)

    x = 1
    # Tests calls
    assert(lambda_rule(x) + func_rule(x) == 4), (
        "lambdas and functions should be acceptable callables!")
    assert(x == 1), "ints shouldn't change value!"

    print("Rule Representation: {}".format(lambda_rule))
    print("Rule Debug: {}".format(func_rule.__repr__()))
    warning = '\033[93m'
    end = '\033[0m'
    print(warning + "lambdas show up in debug prompts as {}, "
           "use functions instead\033[0m".format(
            lambda_rule.function.__name__) + end)

