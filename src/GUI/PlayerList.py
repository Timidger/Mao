#!/bin/python2
import Tkinter
import threading
import time

class PlayerList(Tkinter.Frame, object):
    def __init__(self, master, client):
        super(PlayerList, self).__init__(master)
        self.client = client
        self.label_list = [] # Labels containing player the names
        self.make_player_list()
        self.thread = threading.Thread(name="Last player thread",
                                       target=self.constantly_update)
        self.thread.start()

    def make_player_list(self):
        if self.client.players:
            for index, name in enumerate(self.client.players):
                # Make a label
                label = Tkinter.Label(self, text=name, bg="white",
                                      relief="groove")
                # Add it to the list
                self.label_list.append(label)
                # Show it
                label.grid(row=index)

    def highlight_last_player(self):
        """Highlights the name of the last player who played"""
        self.clear_hightlights()
        last_player = self.client.last_player
        if last_player:
            index = self.label_list.index(last_player)
            self.label_list[index].config(bg="yellow")

    def clear_hightlights(self):
        """Clears all the player hightlights on the player list"""
        for label in self.label_list:
            label.config(bg="white")

    def constantly_update(self):
        while self.client.is_running():
            self.clear_hightlights()
            self.highlight_last_player()
            self.make_player_list()
            time.sleep(.5)
