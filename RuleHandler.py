
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:57 2012

@author: Preston
"""

import RuleGenerator
from Card import Card

class RuleHandler(object):
    """Holds rules to be executed from input corresponding to triggers"""
    def __init__(self, rules = None):
        """Rules should be a list or tuple of rule objects"""
        self.rules = {} # {rule object: codified script}
        if rules:
            for rule in tuple(rules):
                self.add_rule(rule)

    def check_rules(self, trigger, check_none = False):
        """Using the trigger as a key, returns a list of the rule scripts
        that pass the check; if check_None is given and True, triggers that
        are None also get counted"""
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
        rulewas added, returns True. Else, returns False"""
        if rule not in self.rules:
            self.rules.update({rule: RuleGenerator.codify(rule)})
            return True
        else:
            return False

    def remove_rule(self, rule):
        """Removes the rule from the list of rules. If the rule is not
        present, a KeyError is raised"""
        self.rules.pop(rule)

if __name__ == '__main__':
    import Rule
    from Pile import Pile
    RH = RuleHandler({})
    test_pile = Pile()
    RuleGenerator.WHITE_LIST.add(test_pile)
    Cards = tuple(Card(suit, rank) for rank in (
    "Ace 2 3 4 5 6 7 8 9 10 King Queen Jack".split()) for suit in (
    "Hearts", "Spades", "Clubs", "Diamonds") )
    RuleGenerator.WHITE_LIST.add(Cards)
    fill_pile = Rule.Rule('Fill Pile',  None,
                            'Set test_pile.cards to Cards')
    empty = Rule.Rule('Empty deck', ('Correct Phrase',),
                      'Set test_pile.cards to []')
    RH.add_rule(fill_pile)
    RH.add_rule(empty)
    for rule in RH.check_rules('Test'):
        eval(rule or '')
    assert not test_pile.cards
    for rule in RH.check_rules('Test', True):
        eval(rule or '')
    assert len(test_pile.cards) == 52
    for rule in RH.check_rules('This is a test phrase'):
        eval(rule or '')
    assert len(test_pile.cards) == 52
    for rule in RH.check_rules(Card(None, None)):
        eval(rule or '')
    assert len(test_pile.cards) == 52
    for rule in RH.check_rules('Correct Phrase'):
        eval(rule or '')
    assert not test_pile.cards
    print
    print 'Rule, RuleGenerator, and RuleHandler tests complete!'
