# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 09:13:12 2013

@author: timidger
"""

import Tkinter
import Queue
import threading
from collections import OrderedDict
from ..Base.Card import Card
from ..Client.Client import Client
from ..Base import OptionsParser


class Hand(Tkinter.Canvas, object):
    def __init__(self, master, Client):
        super(Hand, self).__init__(master)
        #self.pack(fill = 'both', expand = True)
        self.frame = Tkinter.Frame(self)
        # Vertical Scroll bar setup
        self.vsb = Tkinter.Scrollbar(self, orient="horizontal",
                                     command=self.xview)
        self.configure(xscrollcommand=self.vsb.set)
        self.vsb.grid(row=1)
        self.grid(sticky="WE")
        self._frame_id = self.create_window((4,4), window=self.frame,
                                            anchor="sw", tags="self.frame")
        self.frame.bind("<Configure>", self.OnFrameConfigure)
        self.frame.grid(sticky="WE", row=0, in_=self)
        #self.grid_propagate(False)
        self.frame.grid_propagate(False)


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
        assert type(card) == Card, (
        "{} (a {}) must be a Card!".format(card, type(card)))
        self._send_lock.acquire()
        button = Tkinter.Button(self.frame)
        button.config(relief = 'flat',
                      command = lambda card=card: self.send_card(card),
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
                card = self.Client.card_queue.get(timeout=1)
                self.add_to_hand(card)
                self.update_hand()
            except Queue.Empty:
                continue

    def destroy(self):
        self.Client.disconnect()
        super(Hand, self).destroy()

    def __repr__(self):
        return "GUI representation of the hand for {}".format(
        self.Client.player)

    #No Idea if I need this
    def OnFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.itemconfig(self._frame_id, height=event.height, width=event.width)
        #self.configure(scrollregion=self.bbox("all"))

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
