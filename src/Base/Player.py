# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:14:12 2012

@author: Preston
"""


class Player(object):
    """Player which has a unique name and a hand of cards"""
    def __init__(self, name, hand=None):
        """Creates a new player for a game which has a hand and name"""
        if hand is None:
            self.hand = []
        else:
            self.hand = list(hand)
        assert(type(name) is str), "{} must be a string!".format(name)
        self.name = name

    def get_card(self, index):
        """Returns and removes the card at the index"""
        return self.hand.pop(index)

    def add_card(self, card, index=-1):
        "Add the card to the player's hand at the index (defaults to -1)"
        self.hand.insert(index, card)

    def __contains__(self, card):
        return card in self.hand

    def __getitem__(self, key):
        return self.hand[key]

    def __len__(self):
        return len(self.hand)

    def __eq__(self, other):
        assert(type(other) == Player), "{} must be a player!".format(other)
        return other.name == self.name

    def __repr__(self):
        return "Player named {} with {} cards".format(self.name,
                                                      len(self.hand))

    def __str__(self):
        return self.name

if __name__ == "__main__":
    from Card import Card
    card1, card2 = Card("Hearts", "5"), Card("Spades", "King")
    cards = [card1, card2]
    player = Player("Timidger", cards)

    assert(len(player) == 2), (
        "{} must have 2 cards! (had {})".format(player, len(player)))
    player.add_card(Card("Clubs", "5"))
    assert(len(player) == 3), (
        "{} must have 3 cards! Failed 'add_card' test".format(player))

    # "in" check works for both list and player objects
    assert(card1 in player.hand)
    assert(card1 in player)

    # Slice test
    assert(player[0] == card1)
    assert(player.get_card(0) == card1)

    assert(len(player.hand) == 2), "get_card needs to remove the card!"

    print("Player Representation: {}".format(player))
    print("Player Debug: {}".format(player.__repr__()))
