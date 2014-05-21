# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:59:49 2013

@author: timidger
"""

import Tkinter
import Queue
import threading
from ..Client.Client import Client
import CardImage


class Stack(Tkinter.Frame, object):
    def __init__(self, master, Client):
        super(Stack, self).__init__(master)
        self.Client = Client
        self.update_top_card()
        self.listener = threading.Thread(name = 'Listening for pile updates',
                                target = self.update_display)
        self.listener.start()

    def update_top_card(self):
        # Clubs has a black border
        if not self.Client.pile.top_card:
            image = CardImage.get_blank_card("Clubs")
            self.top_card_image = CardImage.prepare_for_tkinter(image)
        else:
            rank, suit = (self.Client.pile.top_card.rank,
                         self.Client.pile.top_card.suit)
            self.top_card_image = CardImage.make_card_image(rank, suit)

        self.top_card = Tkinter.Button(self, image=self.top_card_image)
        self.top_card.grid()

    def update_display(self):
        while self.Client.is_running():
            try:
                self.Client.pile_queue.get(timeout = 1)
                self.top_card.destroy()
                self.update_top_card()
            except Queue.Empty:
                continue

    def destroy(self):
        self.Client.disconnect()
        super(Stack, self).destroy()

    def __repr__(self):
        return "GUI representation of {}".format(self.Client.pile)

if __name__ == '__main__':
    root = Tkinter.Tk()
    ip = raw_input('ip (nothing for localname) = ')
    port = int(raw_input('port = '))
    name = raw_input('name (nothing for "Timidger") = ') or 'Timidger'
    Client = Client(port, ip, name)
    pile = Stack(root, Client)
    pile.grid()
    root.mainloop()
