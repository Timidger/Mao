# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 23:01:34 2013

@author: timidger
"""
import Tkinter
from Card import Card

class Deck(Tkinter.Frame, object):
    def __init__(self, master, Client):
        super(Deck, self).__init__(master)
        self.Client = Client
        self.pack(fill = 'both', expand = True)
        self.grid()
        self.deck = Tkinter.Button(self)
        self.deck.config(relief = 'flat',
                         command = lambda: self.Client.send(Card(None, None
                         )),
                         text = '<Insert Fancy Design Here>')
        self.deck.grid()

    def destroy(self):
        self.Client.disconnect()
        super(Deck, self).destroy()

if __name__ == '__main__':
    from Client import Client
    ip = raw_input('ip (nothing for localname) = ')
    port = int(raw_input('port = '))
    name = raw_input('name (nothing for "Timidger") = ') or 'Timidger'
    client = Client(port, ip, name)
    root = Tkinter.Tk()
    deck = Deck(root, client)
    root.mainloop()