# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:14:51 2013

@author: Preston
"""

class PlayerHandler(object):
    """Holds and handles players and order"""
    def __init__(self, players = None, order = 1):
        """The order is how much the list increments (or decrements) every
        time a player finishes his turn, and the players is a list of
        player instances"""
        if players is None:
            self.players = []
        else:
            self.players = list(players)
        self.current_player = None
        self.next_player()
        self.order = order

    def get_current_player(self):
        """Returns the current player's name or None if there is no current
        player"""
        try:
            return self.current_player.name
        except AttributeError:
            return None

    def get_player_distance(self, index):
        """Returns the 'distance' between the current player and the given
        index. Takes either a player instance or an int index as an index
        """
        if type(index) == int:
            return abs(self.players.index(self.current_player) - index)
        else:
            return abs(self.players.index(self.current_player) - (
            self.players.index(index)))

    def update_order(self):
        """If order is configured to be unfair (i.e: not every player will
        play in a given round), then the order reverts to one"""
        if not self.order or (
        len(self.players) % 2 == 0 and self.order % 2 == 0) or (
        len(self.players) % 2 != 0 and self.order % 2 != 0):
            self.order = 1
        else:
            pass

    def add_player(self, player):
        """Adds the player to players and deals him a new hand"""
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player):
        """Removes the player from players, essentially deleting him"""
        if player is self.current_player:
            self.next_player()
        self.players.remove(player)
        if not self.players:
            self.current_player = None

    def get_player(self, interval):
        """Returns the player based on the interval and the current order.
        I.E: with an interval of 1 and an order of 1, it will get the next
        player in the list. An interval of 2 with an order of 1 is the same
        as an interval of 1 with an interval of 2. A negative number goes in
        the reverse direction, so interval as -2 would be the 2nd to last
        player who would have played BASED ON THE CURRENT ORDER"""
        assert type(interval) == int
        if not interval and self.players:
            return self.current_player
        elif self.players:
            step = interval * self.order
            index = self.players.index(self.current_player) + step
            while index >= len(self.players):
                index -= len(self.players)
            while index <= -(len(self.players)):
                index += len(self.players)
            return self.players[index]
        else:
            return None

    def next_player(self):
        """Sets the current player to the next player to play"""
        if not self.current_player:
            if self.players:
                self.current_player = self.players[0]
            else:
                self.current_player = None
        self.current_player = self.get_player(1)
