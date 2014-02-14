# -*- coding: utf-8 -*-
"""
Created on 2014/02/12 07:37:00

@author: Preston
"""

import os
import inspect

def import_module(module_name):
    """Searches the Variants directory for module_name and returns it"""
    assert type(module_name) == str
    try:
        module = __import__("Rules." + module_name, 
                            fromlist = ["filler"])
                            #non-empty list imports module_name
    except ImportError, e:
        raise (ImportError, 
               "Could not find {} in {}".format(module_name, 
                os.getcwd() + os.sep + "Rules"))
        
    return module

def get_functions(module):
    """Returns a list of the non-hidden functions in module"""
    return [function for function in module.__dict__.itervalues()
            if (is_function(function))]

def is_function(function):
    """Returns true if function is a function"""
    return inspect.isfunction(function)
