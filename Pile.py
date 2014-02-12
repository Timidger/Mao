# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""
import random
from Card import Card

class Pile(object):
    """Creates a place for cards to be placed"""
    def __init__(self, cards = None):
        if cards is None:
            self.cards = []
        else:
            self.cards = list(cards)
            self.shuffle()
        self.update_top_card()

    def update_top_card(self):
        if self.cards:
            self.top_card = self.cards[0]
        else:
            self.top_card = Card(None, None)

    def shuffle(self): #Modern Fisher-Yates Shuffle Algorithm
        """Shuffles the deck"""
        for first in range(len(self.cards) - 1, 0, -1):
            second = random.randint(0, first)
            self.cards[second], self.cards[first] = (
            self.cards[first], self.cards[second])

    def add(self, cards, index = 0):
        """Adds cards to the pile at the appropriate index, which is the
        top card by default. Cards needs to be iterable"""
        for card in cards:
            self.cards.insert(index, card)
        if not index:
            self.update_top_card()

    def remove(self, index = 0, cardrange = 1):
        """Removes n number of cards from the pile at the appropriate index"""
        cards = tuple(self.cards.pop(index) for card in xrange(cardrange))
        if not index:
            self.update_top_card()
        return cards

    def __repr__(self):
        return "A Pile with these three cards on top: {}".format(
        self.cards[0:3])
