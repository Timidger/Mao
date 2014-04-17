# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:14:51 2013

@author: Preston
"""


class PlayerHandler(object):
    """Holds and handles players and order"""
    def __init__(self, players=None, order=1):
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

    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, value):
        assert(value in self.players or value is None), (
            "{} not in players!".format(value))
        self._current_player = value

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        value = int(value)
        assert(value > 0), "order must be a positive number!"
        # If players % value == 0, then not everybody will play once per round
        if not self.players:
            self._order = 1
        if value % len(self.players) != 0:
            self._order = value
        else:
            self._order = 1

    def add_player(self, player):
        """Adds the player to players and deals him a new hand"""
        if player not in self.players:
            self.players.append(player)
        else:
            raise PlayerError("{} already in players!".format(player))

    def remove_player(self, player):
        """Removes the player from players, essentially deleting him"""
        if player in self.players:
            self.players.remove(player)
        else:
            raise PlayerError("{} not in players!".format(player))

    def get_player(self, interval):
        """Returns the player based on the interval and the current order.
        I.E: with an interval of 1 and an order of 1, it will get the next
        player in the list. An interval of 2 with an order of 1 is the same
        as an interval of 1 with an interval of 2. A negative number goes in
        the reverse direction, so interval as -2 would be the 2nd to last
        player who would have played BASED ON THE CURRENT ORDER"""
        assert type(interval) == int, "Key must be an integer!"
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
            raise KeyError("No players in the list!")

    def next_player(self):
        """Sets the current player to the next player to play"""
        if not self.current_player:
            if self.players:
                self.current_player = self.players[0]
            else:
                self.current_player = None
        else:
            self.current_player = self.get_player(1)

    def __getitem__(self, key):
        """Instead of directly accessing the player list, this uses the
        get_player function, which takes into account order and the current
        player"""
        return self.get_player(key)

    def __iter__(self):
        return self

    def __next__(self):
        self.next_player()
        return self.current_player

    def __repr__(self):
        return "Playerhandler with {} players and an order of {}".format(
            len(self.players), self.order)


class PlayerError(Exception):
    pass

if __name__ == "__main__":
    from random import choice

    def play(stop, orders=None):
        for turn, player in enumerate(PH):
            print("{}: {}\t{}".format(turn, player, PH.order))
            if turn == stop:
                break
            # Can change orders halfway through
            if orders:
                PH.order = choice(orders)

    PH = PlayerHandler()
    try:
        PH.order = 0
        raise AssertionError("Order can't be set to 0!")
    except AssertionError:
        pass
    assert not PH.players, "There shouldn't be any players!"
    assert not PH.current_player, "No players == current_player == None!"

    players = ["Preston", "Harry", "Gerald", "Aristotle"]
    for player in players:
        PH.add_player(player)
    assert PH.players, "There should be players now!"
    assert len(PH.players) == 4, "There should be 4 players now!"
    play(4)
    print("-"*69)
    PH.order = 3
    assert(PH.order == 3), (
        "Order should be 3, order of 3 is good for an even number of players!")
    play(4)
    print(PH)
    play(4, [order for order in range(1, 100)])
