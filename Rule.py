# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:26 2012

@author: Preston
"""

from Queue import Queue

class Rule(object):
    """Creates a new rule object which, has a name (for identification),
    triggers (to indicate when the script will execute), and a script,
    which is some executable python code, whether it is a function, lambda,
    compiled code object, or even an entire object (with enough hacking).
    The only requriement for the script is that there is only one parametre
    that will represent the entire Server object"""
    def __init__(self, name, triggers, script):
        """
        name -- a simple name to easily identify a rule
        
        trigger -- card or phrase that invokes the rule

        commands -- executable python code. Either a lambda, function, compiled
        code object, or class. The only requriement is that it takes one
        parametre, which will represnt the Server

        """
        assert type(name) == str
        self.name = name
        if triggers:
            self.triggers = tuple(triggers)
        else:
            self.triggers = ()
        self.script = script
        self.play_queue = Queue()
        self.say_queue = Queue()

if __name__ == '__main__':
    
