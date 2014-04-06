# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""
SUITS = "Hearts Clubs Spades Diamonds".split()
RANKS = "Ace 2 3 4 5 6 7 8 9 10 Jack Queen King".split()


class Card(object):
    """A card that has a suit and rank"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def change_suit(self, new_suit):
        """Changes the suit of the card to the new suit"""
        assert new_suit in SUITS
        self.suit = new_suit

    def change_rank(self, new_rank):
        """Changes the rank of the card to the new rank"""
        assert new_rank in RANKS
        self.rank = new_rank

    @staticmethod
    def is_similar(card, other_card):
        ranks = (card.rank == other_card.rank
                if other_card.rank and card.rank else True)
        suits = (card.suit == other_card.suit
                if other_card.suit and card.suit else True)
        return suits or ranks

    def __nonzero__(self):
        return any((self.rank, self.suit))

    def __eq__(self, other_card):
        assert type(other_card) == Card
        return (other_card.rank, other_card.suit) == (self.rank, self.suit)

    def __repr__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)
