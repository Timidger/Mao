# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:57 2012

@author: Preston
"""
import os
import threading
from ..Base import Card


class RuleHandler(object):
    """Holds rules to be executed from input corresponding to triggers."""
    def __init__(self, rules=None):
        """Rules should be a list or tuple of rule objects."""
        self.rules = {}  # {rule object: rule script}
        if rules:
            for rule in tuple(rules):
                self.add_rule(rule)

    def check_rules(self, trigger, check_none=False):
        """Using the trigger as a key, returns a list of the rules
        that pass the check; if check_None is given and True, triggers that
        are None also get counted."""
        rules = []
        for rule in self.rules:
            if not rule.trigger:
                if check_none:
                    rules.append(rule)
            elif rule.trigger == trigger or not rule.trigger and check_none:
                rules.append(rule)
        return rules

    def execute_rules(self, rules, server):
        """For each rule in rules, executes the rule's script in a seperate
        thread. Returns the list of the threads"""
        # Generate the threads that will run the rules in parallel
        threads = [threading.Thread(name="Thread for {}".format(rule.name,
                                    target=rule.function,
                                    args=server))
                   for rule in rules]
        for thread in threads:
            thread.start()
        # If stoppable threads needs to be implemented,
        # this can allow access to them
        return threads

    def add_rule(self, rule):
        """If the rule is not in the rules, adds it to the rules. If the
        rulewas added, returns True. Else, returns False."""
        if rule not in self.rules:
            self.rules.update({rule: rule.function})
            return True
        else:
            return False

    def remove_rule(self, rule):
        """Removes the rule from the list of rules."""
        self.rules.pop(rule)
