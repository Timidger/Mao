# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 19:00:23 2013

@author: preston
"""

import os
from Card import Card
from Rule import Rule
from Player import Player
from Pile import Pile
from Variant import Variant
from VariantHandler import VariantHandler
from PlayerHandler import PlayerHandler
from RuleHandler import RuleHandler
PH, VH, RH = PlayerHandler(), VariantHandler(), RuleHandler(None)


def server_test():
    print "Sorry! I'm too lazy to open the server and client in seperate",
    print " proccesses, so just go run the seperate modules!"
    print "Sorry, once again"
    print

def player_test():
    deck = Pile(list(Card(suit, rank) for rank in (
    "Ace 2 3 4 5 6 7 8 9 10 Jack Queen King".split()) for suit in (
    ' Hearts, Spades, Clubs, Diamonds'.split(','))))
    for name in 'Timidger Brendyn Grey Harry'.split():
        PH.add_player(Player(name))
    for player in PH.players:
        player.add_cards(deck.remove(0, 7))
    assert len(PH.players) == 4
    assert not PH.get_current_player()
    PH.next_player()
    assert PH.current_player == PH.players[0]
    assert PH.order == 1
    PH.next_player()
    PH.remove_player(PH.current_player)
    assert len(PH.players) == 3
    assert PH.get_current_player() == PH.players[1].name
    assert PH.get_current_player() == 'Grey'
    PH.current_player = PH.players[0]

def pile_test(): #Also tests card
    deck = Pile(list(Card(suit, rank) for rank in (
    "Ace 2 3 4 5 6 7 8 9 10 Jack Queen King".split()) for suit in(
    ' Hearts, Spades, Clubs, Diamonds'.split(','))))
    assert len(deck.cards) == 52
    assert deck.top_card == deck.cards[0]
    pile = Pile()
    assert len(pile.cards) == 0
    assert not pile.top_card
    PH.current_player.hand = []
    PH.current_player.add_cards(deck.remove(cardrange = 7))
    assert len(deck.cards) == 45
    assert len(PH.current_player.hand) == 7
    assert deck.top_card == deck.cards[0]
    card = PH.current_player.hand[0]
    pile.add(PH.current_player.get_card(0))
    assert len(pile.cards) == 1
    assert len(PH.current_player.hand) == 6
    assert card in pile.cards


def rule_test():
    """Tests the entire Rule.py module"""
    Deck = Pile()
    assert len(Deck.cards) == 0

    #Remove... Test
    hearts_remove = Rule('Card', 'Hearts', {'Remove': {'instance':
        'PH.current_player.hand[0]'}})

    #New... Test
    new_card = Rule('Player_Action', 'Knock', {'New': {'instance':
        'Card', 'instances': 'Deck.cards', 'parametres': ['Hearts', '5',
            'dj'], 'if': 'len(Decks.cards) <= 1'}})

    #Set... Test
    reverse_order = Rule('Card', 'Ace', {'Set': {'instance':
        'PH.order', 'value': '-PH.order'}})

    #Replace... Test
    switch_hands = Rule('Player_Action', 'Wink', {'Replace': {
        'instance': 'PH.current_player.hand', 'other_instance':
            'PH.players[0].hand', 'if':
                "len(PH.current_player.hand) == len(PH.players[0].hand)"}})

    #Say... Test
    say_shit = Rule('Start', 'SHIT', {'Say': {'extra_phrase': 'shit',
        'modifier': '5'}})

    rules = [hearts_remove, new_card, reverse_order, switch_hands,
             say_shit]

    RH = RuleHandler(rules)
    for rule in RH.rules.values():
        eval(rule)#Just asserts the code can run, not if it works

    test_variant = Variant('Test_Run', 'This is for testing purposes only',
                           rules)
    VH.add_variant(test_variant)
    VH.save_variant(test_variant)
    assert len(VH.variants) == 1
    VH.remove_variant(test_variant)
    assert not VH.variants
    VH.load_variant('Test_Run')
    assert len(VH.variants) == 1
    for rule in VH.variants[0].rules:
        RH.build_rule(rule)
    for rule in RH.rules.values():
        eval(rule)
    assert len(os.listdir(VH.directory)) == 1
    VH.delete_variant('Test_Run')
    assert len(os.listdir(VH.directory)) == 0

#End single tests!




if __name__ == '__main__':
    player_test()
    pile_test()
#    rule_test() Still gotta rewrite since we split that class up
    print 'All Tests Passed!'
