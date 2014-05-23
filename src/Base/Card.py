# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""
SUITS = ("Hearts", "Clubs", "Spades", "Diamonds")
RANKS = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
         "Jack", "Queen", "King")
WILD_CARD = "*"


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
        assert(value in SUITS or value == WILD_CARD), (
            "Suit should be in {}, was {}".format(
                SUITS + (WILD_CARD,), value))
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
        assert(value in RANKS or value == WILD_CARD), (
            "Rank should be in {}, was {}".format(
                RANKS + (WILD_CARD,), value))
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
        ranks = (self.rank, other_card.rank)
        suits = (self.suit, other_card.suit)
        ranks_equal = WILD_CARD in ranks or ranks[0] == ranks[1]
        suits_equal = WILD_CARD in suits or suits[0] == suits[1]
        return ranks_equal and suits_equal

    def __nq__(self, other_card):
        return not self.__eq__(other_card)

    def __repr__(self):
        return "Card with rank {} and suit {}".format(self.rank, self.suit)

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

if __name__ == "__main__":
    cards = [Card(suit, rank)
             for suit in (SUITS + (WILD_CARD,))
             for rank in (RANKS + (WILD_CARD,))]
    for card in cards:
        # Tests not bool-ness
        if not card:
            assert(card.rank == WILD_CARD and card.suit == WILD_CARD), (
                "Both rank and suit must be {}!".format(WILD_CARD))
        # Tests bool-ness
        else:
            assert(card), "Both suit and rank must be values!".format(card)
    for rank in RANKS:
        for suit in SUITS:
            # Test that case matters
            try:
                Card(rank.lower(), suit.lower())
            except AssertionError:
                continue
            else:
                raise AssertionError(
                    "Ranks and Suits must be properly capitalized")
    # Test that equality does not check for "similar" cards
    card1, card2 = Card("Hearts", "5"), Card("Hearts", "6")
    assert(not (card1 == card2) == (card1 != card2)), (
        "Equality checking should work only for cards exactly the same")

    assert (card1 == Card(WILD_CARD, "5")), (
        "{} should act as a wildcard".format(WILD_CARD))

    assert(card2 == Card(WILD_CARD, "6")), (
        "{} should act as a wildcard".format(WILD_CARD))

    # Tests is_similar method for like ranks and suits
    assert(Card.is_similar(card1, card2)), "Must accept same ranks!"
    assert(Card.is_similar(Card("Clubs", "Jack"), Card("Clubs", "Ace"))), (
        "Must accept same suits!")
    assert(Card.is_similar(card1, card1))

    # Shows the different ways cards are represented in the program
    print("Card Representation: {}".format(cards[0]))
    print("Card Debug: {}".format(cards[0].__repr__()))
