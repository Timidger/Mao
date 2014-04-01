# -*- coding: utf-8 -*-
"""
Created on 2014/02/12 07:37:00

@author: Preston
"""

import os
import inspect


def load_rules(module_name):
    """Returns the functions in the module to be used in a Rule's script"""
    get_functions(import_module(module_name))


def import_module(module_name):
    """Searches the Variants directory for module_name and returns it"""
    assert type(module_name) == str
    rules_dir = os.getcwd() + os.sep + "Rules"
    try:
        module = __import__("Rules." + module_name,
                            # non-empty list imports module_name
                            fromlist=["filler"])
    except ImportError, e:
        if os.path.exists(rules_dir):
            raise ImportError("Could not find {} in {}".format(module_name,
                                                               rules_dir))
        else:
            raise ImportError('{} does not exist!'.format(rules_dir))
    return module


def get_functions(module):
    """Returns a list of the non-hidden functions in module"""
    return [function for function in module.__dict__.itervalues()
            if (is_function(function))]


def is_function(function):
    """Returns true if function is a function"""
    return inspect.isfunction(function)
