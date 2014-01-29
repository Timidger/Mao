# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 08:07:15 2013

@author: timidger
"""

import Tkinter
from Client import Client
from Deck import Deck
from Stack import Stack
from Hand import Hand
from Chat import Chat

class Display(Tkinter.Frame, object):
    def __init__(self, master):
        super(Display, self).__init__(master)
        self.start_screen()

    def start_game(self):
        self.client = Client(int(self.port_box.get()), self.ip_box.get(),
                        self.name_box.get())
        self.start_frame.destroy()
        self.deck = Deck(self.master, self.client)
        self.pile = Stack(self.master, self.client)
        self.hand = Hand(self.master, self.client)
        self.chat = Chat(self.master, self.client)

        self.deck.columnconfigure(1, weight = 1)
        self.pile.rowconfigure(1, weight = 1)
        self.pile.columnconfigure(2, weight = 1)
        self.hand.columnconfigure(1, weight = 1)
        self.chat.columnconfigure(2, weight = 1)

        self.deck.grid()
        self.pile.grid()
        self.hand.grid()
        self.chat.grid()

    def start_screen(self):
        self.start_frame = Tkinter.Frame(self.master)
        self.ip_box = Tkinter.Entry(self.start_frame)
        self.port_box = Tkinter.Entry(self.start_frame)
        self.name_box = Tkinter.Entry(self.start_frame)
        start_button = Tkinter.Button(self.start_frame)
        start_button.config(text = 'Start the game!',
                            command = self.start_game,)
        self.start_frame.grid()
        self.ip_box.grid()
        self.port_box.grid()
        self.name_box.grid()
        start_button.grid()

    def destroy(self):
        self.client.disconnect()
        super(Display, self).destroy()

if __name__ == '__main__':
    root = Tkinter.Tk()
    main = Display(root)
    root.mainloop()
