# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:57 2012

@author: Preston
"""
import os
import threading


class RuleHandler(object):
    """Holds rules to be executed from input corresponding to triggers"""
    def __init__(self, rules=None):
        """Rules should be an iterable of rule objects."""
        self.rules = set()  # Set of Rule objects
        if rules:
            for rule in rules:
                self.add_rule(rule)

    @staticmethod
    def execute_rules(rules, server):
        """For each rule in rules, executes the rule's script in a seperate
        thread. Returns a list of the threads"""
        # Generate the threads that will run the rules in parallel
        threads = [threading.Thread(name="Thread for {}".format(rule),
                                    target=rule,
                                    args=server)
                   for rule in rules]
        for thread in threads:
            thread.start()
        # If stoppable threads needs to be implemented,
        # this can allow access to them
        return threads

    def check_rules(self, trigger, check_none=False):
        """Using the trigger as a key, returns a list of the rules
        that have that trigger; if check_None is given and True, triggers that
        are None also get counted"""
        rules = []
        for rule in self.rules:
            if rule.trigger == trigger or not rule.trigger and check_none:
                rules.append(rule)
        return rules

    def add_rule(self, rule):
        """If the rule is not in the rules, adds it to the rules"""
        self.rules.add(rule)

    def remove_rule(self, rule):
        """Removes the rule from the list of rules"""
        self.rules.remove(rule)

if __name__ == "__main__":
    class TestRule():
        def __init__(self, trigger):
            self.trigger = trigger

    # Generator can work, as well as any iterable
    rules = [TestRule('Test Phrase')]
    RH = RuleHandler(rules)
    assert(RH.check_rules("Test Phrase")), (
        '"Test Phrase" is not a trigger for any rule!')
