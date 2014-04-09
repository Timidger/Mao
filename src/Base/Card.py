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

    @property
    def suit(self):
        "String that represents the card's suit"
        return self._suit

    @suit.setter
    def suit(self, value):
        # Assert, value si not none, python 2????
        assert(value in SUITS or value is None), (
        "Suit should be in {}, was {}".format(SUITS, value))
        self._suit = value

    @suit.deleter
    def suit(self):
        self._suit = None

    @property
    def rank(self):
        "String that represents the card's rank"
        return self._rank

    @rank.setter
    def rank(self, value):
        assert(value in RANKS or value is None), (
        "Rank should be in {}, was {}".format(SUITS, value))
        self._rank = value

    @rank.deleter
    def rank(self):
        self._rank = None

    @staticmethod
    def is_similar(card, other_card):
        ranks = (card.rank == other_card.rank
                 if other_card.rank and card.rank else True)
        suits = (card.suit == other_card.suit
                 if other_card.suit and card.suit else True)
        return suits or ranks

    def __bool__(self):
        return any((self.rank, self.suit))

    def __eq__(self, other_card):
        assert(type(other_card) == Card), "Can't compare card and non-card!"
        return (other_card.rank, other_card.suit) == (self.rank, self.suit)

    def __repr__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

if __name__ == "__main__":
    cards = [Card(suit, rank)
            for suit in (SUITS + [None]) for rank in (RANKS + [None])]
#    print(cards)
    for card in cards:
        if not card:
            print(card)
            assert(card.rank == None and card.suit == None), (
                "Both rank and suit must be None!")
        else:
            assert(card), "Both suit and rank must be values!".format(card)
    for rank in RANKS:
        for suit in SUITS:
            try:
                Card(rank.lower(), suit.lower())
            except AssertionError:
                continue
            else:
                raise AssertionError(
                    "Card can only accept proper ranks and suits")
