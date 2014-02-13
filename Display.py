# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 08:07:15 2013

@author: timidger
"""

import Tkinter
from threading import Thread
from Client import Client
from Deck import Deck
from Stack import Stack
from Hand import Hand
from Chat import Chat

class Display(Tkinter.Frame, object):
    def __init__(self, master):
        super(Display, self).__init__(master)
        self.start_screen()

    def start_screen(self):
        self.start_frame = Tkinter.Frame(self.master)
        self.ip_box = Tkinter.Entry(self.start_frame, text="hey")
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

    def start_game(self):
        self.client = Client(int(self.port_box.get()), self.ip_box.get(),
                        self.name_box.get())
        Thread(name = "Destroy wait thread",
               target = self.wait_to_destroy).start()
        self.start_frame.destroy()
        self.deck = Deck(self.master, self.client)
        self.pile = Stack(self.master, self.client)
        self.hand = Hand(self.master, self.client)
        self.chat = Chat(self.master, self.client)

        self.deck.grid(column = 0, row = 1)
        self.pile.grid(column = 2, row = 1)
        self.hand.grid(column = 1, row = 0)
        self.chat.grid(column = 1, row = 1)

    def wait_to_destroy(self):
        #Looks kinda weird, but it destroys GUI when client disconnects
        if self.client._connected.wait():
            print "destroying"
            self.destroy()

    def destroy(self):
        try:
            self.client.disconnect()
        #In case the window is closed before joining a server
        except AttributeError:
            pass
        super(Display, self).destroy()

if __name__ == '__main__':
    root = Tkinter.Tk()
    root.wm_title("Mao: Version 1.0")
    main = Display(root)
    root.mainloop()
