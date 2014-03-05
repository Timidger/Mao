# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""

class Card(object):
    """A card is made up of a suit, rank, and is represented in the game by a
    texture."""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def change_suit(self, new_suit):
        self.suit = new_suit

    def change_rank(self, new_rank):
        self.rank = new_rank

    def __repr__(self):
        return "A Card with suit = {} and rank = {}".format(
        self.suit, self.rank)
    
    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)
