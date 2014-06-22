#!/usr/bin/python

import random
from threading import Event
import time
from ..Base.Player import Player
from ..Base.Pile import Pile
from .PlayerHandler import PlayerHandler


class Game(object):
    def __init__(self, player_handler, deck):
        self.PH = PlayerHandler()
        self.deck = Pile()
        self.pile = Pile()
        # Everytime a player's turn is over, this event activates
        self._turn_over = Event()
        # Event that is set when the game is done running
        self._is_playing = Event()
        # Event set when card added to pile
        self._pile_added_to = Event()
        # Event set when deck taken from
        self._deck_taken_from = Event()
        # New player joined Event
        self._new_player = Event()
        # Player stopped playing Event
        self._player_left = Event()

    def is_game_running(self):
        return not self._is_playing.is_set()

    def add_player(self, player_name, hand_size):
        new_player = Player(player_name)
        self.PH.add_player(new_player)
        self._new_player.set()
        self._new_player.clear()
        # Give the player his starting cards
        for _ in range(hand_size):
            card = self.deck.draw()
            new_player.add_card(card)
        return new_player

    def remove_player(self, player):
        for card in player:
            deck.add(card)
        deck.shuffle()
        self.PH.remove(player)
        self._player_left.set()
        self._player_left.clear()

    def punish(self, player, num_penalty_cards):
        """The player is punished the given number of penalty cards"""
        assert player in self.PH, "Player is not in the player's list!"
        if num_penalty_cards > 0:
            for _ in range(num_penalty_cards):
                card = self.deck.draw()
                player.add_card(card)
        else:
            for _ in range(0, num_penalty_cards, -1):
                card = player.get_card(random.randint(0, len(player) - 1))
                self.deck.add(card, random.randint(0, len(self.deck) - 1))

    def constantly_punish(self, player, penalty_num, punish_time_per_turn):
        """Constantly punishes the player the number of cards in penalty_num
        until the event is set. If no event is given, uses the main_event
        (the one that is set when the current player finally plays a card)"""
        while not self._turn_over.wait(punish_time_per_turn):
            self.punish(player, penalty_num)
        return True

    def main_loop(self, time_per_turn, num_penalty_cards):
        """Main loop that should be called after initialisation"""
        for player in PH:
            if not self.is_game_running():
                break
            if self.PH.current_player:
                print('Current Player: {}'.format(self.PH.current_player))
                # This will loop until the current player plays
                # Or until he is no longer playing
                self.constantly_punish(self.PH.current_player, penalty_num)
                self._turn_over.clear()
            else:
                time.sleep(1)
        self._is_playing.set()

if __name__ == "__main__":
    game = Game()
    error = "{} did not have {} cards (had {})!"
    TIMIDGER = game.add_player("Timidger", 7)
    assert len(TIMIDGER) == 7, error.format("Timidger", 7, len(TIMIDGER))
    HARRY = game.add_player("Harry", 53) # More than there are cards in deck
    assert len(HARRY) == 53, error.format("Harry", 53, len(HARRY)) # Works
    game.punish(TIMIDGER, 2)
    assert len(TIMIDGER) == 9, error.format("Timidger", 9, len(TIMIDGER))
    game.punish(HARRY, 0)
    assert len(HARRY) == 53, error.format("Harry", 53, len(HARRY))
    game.punish(HARRY, -10) # Can remove cards with punish
    assert len(HARRY) == 43, error.format("Harry", 43, len(HARRY))
    game.punish(TIMIDGER, 2**10) # Way more than there are cards in the deck
    assert len(TIMIDGER) == 1033, error.format("Timiger", 1033,
                                                 len(TIMIDGER))
