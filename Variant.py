# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:15:23 2012

@author: Preston
"""
import Rule

class Variant(object):
    """A collection of Rules to be saved and loaded, into RuleHandler"""
    def __init__(self, name, description, rules):
        self.name = name
        self.description = description
        self.rules = list(rules)

    def change_name(self, name):
        self.name = name

    def change_description(self, description):
        self.description = description

    def add_rule(self, rule):
        if rule not in self.rules and isinstance(rule, Rule):
            self.rules.append(rule)

    def remove_rule(self, rule):
        """Removes the rule from self.rules if it is in there"""
        self.rules.remove(rule)
