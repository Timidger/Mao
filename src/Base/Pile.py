# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""
import random
from .Card import Card


class Pile(object):
    """Creates a place for cards to be placed"""
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = list(cards)
            self.shuffle()

    def shuffle(self):  # Modern Fisher-Yates Shuffle Algorithm
        """Shuffles the deck"""
        for first in range(len(self.cards) - 1, 0, -1):
            second = random.randint(0, first)
            self.cards[second], self.cards[first] = (self.cards[first],
                                                     self.cards[second])

    def add(self, cards, index=0):
        """Adds cards to the pile at the appropriate index, which is the
        top card by default. Cards needs to be iterable"""
        for card in cards:
            self.cards.insert(index, card)

    def remove(self, index=0):
        """Removes and returns a card at the appropriate index"""
        card = self.cards.pop(index)
        return card

    def __getitem__(self, index):
        if self.cards:
            return self.cards[index]
        else:
            return Card(None, None)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return "A Pile with {} cards".format(len(self.cards))
