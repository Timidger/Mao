# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 09:13:12 2013

@author: timidger
"""

import Tkinter, Queue, threading
from Card import Card
from Client import Client
from OptionsParser import config_parser
from collections import OrderedDict


class Hand(Tkinter.Frame, object):
    def __init__(self, master, Client):
        super(Hand, self).__init__(master)
        self.pack(fill = 'both', expand = True)
        self.grid()
        self.cards = OrderedDict() # {Card: Button}
        self.Client = Client
        self._send_lock = threading.Lock()
        self.create_widgets()
        master.grid_propagate(True)
        master.grid_rowconfigure(0, weight = 1)
        master.grid_columnconfigure(0, weight = 1)
        threading.Thread(name = 'Listening for cards', target = (
        self.listen)).start()

    def create_widgets(self):
        for index, card in enumerate(self.Client.player.hand):
            self.add_to_hand(card)
        self.update_hand()

    def add_to_hand(self, card):
        assert type(card) == Card
        self._send_lock.acquire()
        button = Tkinter.Button(self)
        button.config(relief = 'flat',
                      command = lambda card = card:
                          self.send_card(card),
                      text = card.rank + ' of ' + card.suit)
        self.cards.update({card: button})
        self._send_lock.release()

    def update_hand(self):
        for index, button in enumerate(self.cards.values()):
            row = (index / 7) + 1
            column = index % 7
            button.grid(column = column, row = row)

    def send_card(self, card):
        self.cards.pop(card).destroy()
        self.Client.player.hand.remove(card)
        self.update_hand()
        self._send_lock.acquire()
        self.Client.send(card)
        self._send_lock.release()

    def listen(self):
        while self.Client.is_running():
            try:
                self.add_to_hand(self.Client.card_queue.get(timeout = 1))
                self.Client.card_queue.queue
                self.update_hand()
            except Queue.Empty:#So this thread stops when the client stops
                continue

    def destroy(self):
        self.Client.disconnect()
        super(Hand, self).destroy()

    def __repr__(self):
        return "GUI representation of the hand for {}".format(
        self.Client.player)

if __name__ == '__main__':
    from Pile import Pile
    suits = []
    for suit in (
    config_parser.get('Cards', suit_type).split() for suit_type in (
    option for option in config_parser.options('Cards') \
    if option.endswith('suit'))):
        suits.extend(suit)
    ranks = config_parser.get('Cards', 'ranks').split()
    deck = (Pile([Card(suit, rank) for rank in \
    ranks for suit in suits]))
    ip = raw_input('ip (nothing for localname) = ')
    port = int(raw_input('port = '))
    name = raw_input('name (nothing for "Timidger") = ') or 'Timidger'
    Client = Client(port, ip, name)
    root = Tkinter.Tk()
    hand = Hand(root, Client)

    root.mainloop()
