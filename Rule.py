# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:26 2012

@author: Preston
"""

from Queue import Queue

class Rule(object):
    """Creates a new rule object which, when passed into the RuleGenerator,
    will generate code based off given commands and parametres"""
    def __init__(self, name, triggers, script):
        """name: a simple name to easily identify a rule
        
        trigger: card or phrase that invokes the rule

        commands is a multi-lined script like the following:

        Logic:
            if True:
                Set dog to 'bark!'
                if dog == None
                    Remove dog
            elif False:
                Replace cat with dog
            else:
                Print 'There is no logic'

        Commands:
            Set word to 'World!'
            Set something to Any-Player say Anything
            New Card to Current-Player where rank = None, suit = 'Joker'
            Replace this with that
            3rd-Player and Last-Player say 'Hello' + word * 2 in 5 seconds
            Next-Player or Previous-Player play King of Hearts //Can we do or?
            Random-Player play Hearts         //Just match suit
            Any-Player play 5                 //Just match rank
            Call awesome_rule                 /Referred to by name attribute
            Set Order to 7
            
            The Say/Play commands are the deepest ones, offering the following
            features:
                *Multiple player listings (Just use 'and' or 'or')
                *Relative player choice (First, Last, Next, Random)
                *Specific player choice (3rd player (Think like 3 next players))
                *Action multipliers (Have to say/phrase something more than once)
                *Timers (How long until punished for not doing the action)
            Please note the player(s) are first, not the command, unlike the
            other commands. This is to allow smooth semantics.

            Things in quotes are strings, lowerscore-only words are 
            User-Variables, and Capitalised words are Commands/Dynamic-Variables
            (Variables dependent on exterior knowlege, like the current player)

            The extra words (to, with, in, etc.) is the delimiter between parametres
        """
        self.name = name
        if triggers:
            self.triggers = tuple(triggers)
        else:
            self.triggers = ()
        self.script = script#Used to be commands/actions
        #So that other if's can be nested as well!
        self.play_queue = Queue()
        self.say_queue = Queue()

if __name__ == '__main__':
    raise NotImplementedError, 'I have yet to rewrite the code generation in RuleGenerator for the sexy scripting language'
