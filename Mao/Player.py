# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:12 2012

@author: Preston
"""

class Player(object):
    """Creates a player that has a name, a hand of cards, and starts
    playing until he is removed from play either through a rule or when he
    runs out of cards"""
    def __init__(self, name, hand = None, address = None):
        """Creates a new player for a game which has a hand and name"""
        if hand is None:
            self.hand = []
        else:
            self.hand = list(hand)
        self.name = name

    def get_card_index(self, card):
        """Returns the index of the card in the hand. Returns None if the
        card cannot be found"""
        rank_suit = (card.rank, card.suit)
        for index, card in enumerate((card.rank, card.suit) for card in
        self.hand):
            if rank_suit == card:
                return index
        else:
            return None

    def get_card(self, index):
        "Pops the card out of the list and returns it"
        return self.hand.pop(index)

    def add_card(self, card, index = 0):
        "Add the card to the player's hand at the index (defaults to 0)"
        self.hand.insert(index, card)
