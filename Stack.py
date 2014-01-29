# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:59:49 2013

@author: timidger
"""


#Good enought, still need to add multiple cards for the pile

import Tkinter, Queue, threading
from Client import Client

class Stack(Tkinter.Frame, object):
    def __init__(self, master, Client):
        super(Stack, self).__init__(master)
        self.Client = Client
        self.create_widgets()
        self.listener = threading.Thread(name = 'Listening for pile updates',
                                target = self.update_display)
        self.listener.start()

    def create_widgets(self):
        print Client
        self.top_card = Tkinter.Button(self,
                                       relief = 'flat',
                                       text = (
                                       (self.Client.pile.top_card.rank or (
                                       'Essence')) + ' of ' + (
                                       self.Client.pile.top_card.suit or(
                                       'Nothing!'))))
        self.top_card.grid()

    def update_display(self):
        while self.Client.is_running():
            try:
                self.Client.pile_queue.get(timeout = 1)
                self.top_card.config(
                text = (self.Client.pile.top_card.rank or 'Essense') + (
                ' of ' + self.Client.pile.top_card.suit or 'Nothing'))
                self.top_card.grid()
            except Queue.Empty:
                continue

    def destroy(self):
        self.Client.disconnect()
        super(Stack, self).destroy()

if __name__ == '__main__':
    root = Tkinter.Tk()
    ip = raw_input('ip (nothing for localname) = ')
    port = int(raw_input('port = '))
    name = raw_input('name (nothing for "Timidger") = ') or 'Timidger'
    Client = Client(port, ip, name)
    pile = Stack(root, Client)
    pile.grid()
    root.mainloop()
