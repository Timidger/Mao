# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""
import random
from .Card import Card, SUITS, RANKS

MINIMUM_DECK_LENGTH = (len(SUITS) * len(RANKS)) // 2  # Half of a deck


class Pile(list, object):

    """Creates a place for cards to be placed"""

    def __init__(self, *cards):
        """Creates a new list with using cards"""
        super(Pile, self).__init__(cards)
        self.shuffle()

    def shuffle(self):  # Modern Fisher-Yates Shuffle Algorithm
        """Shuffles the deck"""
        for first in range(len(self) - 1, 0, -1):
            second = random.randint(0, first)
            self[second], self[first] = (self[first], self[second])

    def draw(self):
        """Draws num_of_cards from the deck. If the deck gets low (<= 26)
        at any point, then a new deck is made, combined with the current deck,
        and then shuffled before drawing continues"""
        # Add before the draw, in case there are not any cards left
        if len(self) <= MINIMUM_DECK_LENGTH:
            new_cards = [Card(suit, rank) for rank in RANKS
                         for suit in SUITS]
            self.add(new_cards)
            self.shuffle()
        card = self.remove()
        return card

    def add(self, card, index=0):
        """Adds the card to the pile at the appropriate index, which is the
        top card by default"""
        assert(isinstance(card, Card)), "Tried to add a non-card!"
        self.insert(index, card)

    def __getitem__(self, index):
        if not self and not index:
            return None
        else:
            return super(Pile, self).__getitem__(index)

    def __repr__(self):
        return "A Pile with {} cards".format(len(self))
