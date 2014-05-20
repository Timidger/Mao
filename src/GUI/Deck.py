# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 23:01:34 2013

@author: timidger
"""
import Tkinter
from ..Base.Card import Card
from CardImage import CardImage


class Deck(Tkinter.Frame, object):
    def __init__(self, master, Client):
        super(Deck, self).__init__(master)
        self.Client = Client
        self.grid()
        self.deck = Tkinter.Button(self)
        blank_card = Card(None, None)
        self.image = CardImage(self, blank_card).back_image
        self.deck.config(relief = 'flat',
                         command = lambda: self.Client.send(Card(None, None
                         )),
                         image=self.image)
        self.deck.grid()

    def destroy(self):
        self.Client.disconnect()
        super(Deck, self).destroy()

    def __repr__(self):
        return "GUI representation of {}".format(self.Client.deck)

if __name__ == '__main__':
    from Client import Client
    ip = raw_input('ip (nothing for localname) = ')
    port = int(raw_input('port = '))
    name = raw_input('name (nothing for "Timidger") = ') or 'Timidger'
    client = Client(port, ip, name)
    root = Tkinter.Tk()
    deck = Deck(root, client)
    root.mainloop()
