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
import CardImage

class Hand(Tkinter.Canvas, object):
    def __init__(self, master, Client):
        super(Hand, self).__init__(master)
        #self.pack(fill = 'both', expand = True)
        self.frame = Tkinter.Frame(self)
        # Make the scroll bar go across the entire frame
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Horizontal Scroll bar setup
        self.vsb = Tkinter.Scrollbar(self, orient="horizontal",
                                     command=self.xview)
        self.configure(xscrollcommand=self.vsb.set)
        self.frame.grid(row=1, column=1, sticky="nsew")
        self.vsb.grid(row=2, column=1, sticky="ew")
        self.grid(row=1, column=1, sticky="nsew")
        self.create_window((4, -10), window=self.frame, tags="self.frame",
                           anchor="nw")
        # Binds it so it can't scroll beyond the boundaries
        self.frame.bind("<Configure>", self.OnFrameConfigure)


        self.cards = OrderedDict() # {Card: Button}
        self.card_images = set()
        self.Client = Client
        self._send_lock = threading.Lock()
        self.create_widgets()
        threading.Thread(name = 'Listening for cards', target = (
        self.listen)).start()

    def create_widgets(self):
        for card in self.Client.player.hand:
            self.add_to_hand(card)
        self.update_hand()

    def add_to_hand(self, card):
        assert type(card) == Card, (
        "{} (a {}) must be a Card!".format(card, type(card)))
        self._send_lock.acquire()
        card_image = CardImage.make_card_image(card.rank, card.suit)
        # So it is not garbage collected
        self.card_images.add(card_image)
        card_button = Tkinter.Button(self.frame)
        card_button.config(command=lambda card=card: self.send_card(card),
                           image=card_image)
        self.cards.update({card: card_button})
        self._send_lock.release()

    def update_hand(self):
        # So that the new card is added to the beginning.
        # Quick hack that needs to be addressed with a new data structure
        reversed_hand = reversed(self.cards.values())
        for index, button in enumerate(reversed_hand):
            column = index
            button.grid(column=column, row=0)

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

    # Makes sure you can't just keep scrolling
    def OnFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.configure(scrollregion=self.bbox("all"))

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
