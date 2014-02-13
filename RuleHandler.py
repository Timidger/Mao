# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:57 2012

@author: Preston
"""
import os
from Card import Card
import Variants


class RuleHandler(object):
    """Holds rules to be executed from input corresponding to triggers."""
    def __init__(self, rules = None):
        """Rules should be a list or tuple of rule objects."""
        self.rules = {} # {rule object: rule script}
        if rules:
            for rule in tuple(rules):
                self.add_rule(rule)

    def check_rules(self, trigger, check_none = False):
        """Using the trigger as a key, returns a list of the rule scripts
        that pass the check; if check_None is given and True, triggers that
        are None also get counted."""
        rule_scripts = []
        if type(trigger) == Card:
            trigger = trigger.rank, trigger.suit
        for rule in self.rules:
            if not rule.triggers and check_none:
                rule_scripts.append(self.rules.get(rule))
            else:
                for trigger in rule.triggers:
                    if type(trigger) == Card and type(trigger) == Card:
                        if all((trigger.rank == trigger.rank,
                        trigger.suit == trigger.suit)):
                            rule_scripts.append(self.rules.get(rule))
                    elif type(trigger) == str and type(trigger) == str:
                        if trigger == trigger or not trigger and check_none:
                            rule_scripts.append(self.rules.get(rule))
        return rule_scripts

    def add_rule(self, rule):
        """If the rule is not in the rules, adds it to the rules. If the
        rulewas added, returns True. Else, returns False."""
        if rule not in self.rules:
            self.rules.update({rule: rule.script})
            return True
        else:
            return False

    def remove_rule(self, rule):
        """Removes the rule from the list of rules."""
        self.rules.pop(rule)
