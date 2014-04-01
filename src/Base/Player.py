# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:12 2012

@author: Preston
"""


class Player(object):
    """Player which has a unique name and a hand of cards"""
    def __init__(self, name, hand=None, address=None):
        """Creates a new player for a game which has a hand and name"""
        if hand is None:
            self.hand = []
        else:
            self.hand = list(hand)
        self.name = name

    def get_card(self, index):
        """Returns and removes the card at the index"""
        return self.hand.pop(index)

    def in_hand(self, card):
        """Returns true if the card is in the hand, false other wise"""
        if card in self.hand:
            return True
        else:
            return False

    def add_card(self, card, index=0):
        "Add the card to the player's hand at the index (defaults to 0)"
        self.hand.insert(index, card)

    def __eq__(self, other):
        assert type(other) == Player
        return other.name = self.name

    def __repr__(self):
        return "Player named {} with {} cards".format(self.name,
                                                      len(self.hand))
