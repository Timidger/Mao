# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""
import random
from .Card import Card, SUITS, RANKS

MINIMUM_DECK_LENGTH = 26 # Half of a deck


class Pile(object):
    """Creates a place for cards to be placed"""
    def __init__(self, cards=None):
        if cards is None:
            self._cards = []
        else:
            self._cards = list(cards)
            self.shuffle()

    def shuffle(self):  # Modern Fisher-Yates Shuffle Algorithm
        """Shuffles the deck"""
        for first in range(len(self._cards) - 1, 0, -1):
            second = random.randint(0, first)
            self._cards[second], self._cards[first] = (self._cards[first],
                                                     self._cards[second])

    def draw(self, num_of_cards=1):
        """Draws num_of_cards from the deck. If the deck gets low (<= 26)
        at any point, then a new deck is made, combined with the current deck,
        and then shuffled before drawing continues"""
        cards = []
        for card in range(num_of_cards):
            # Add before the draw, in case there are not any cards left
            if len(self._cards) <= MINIMUM_DECK_LENGTH:
                new_cards = [Card(suit, rank) for rank in RANKS
                                              for suit in SUITS]
                self.add(new_cards)
                self.shuffle()
            card = self.remove()
            cards.append(card)
        return cards

    def add(self, card, index=0):
        """Adds the card to the pile at the appropriate index, which is the
        top card by default"""
        assert(type(card) == Card)
        self._cards.insert(index, card)

    def remove(self, index=0):
        """Removes and returns a card at the appropriate index"""
        card = self._cards.pop(index)
        return card

    def __getitem__(self, index):
        if not self._cards and not index:
            return Card(None, None)
        else:
            return self._cards[index]

    def __len__(self):
        return len(self._cards)

    def __repr__(self):
        return "A Pile with {} cards".format(len(self._cards))
