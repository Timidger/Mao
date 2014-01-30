# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""
from Client import Client
import Tkinter, threading, Queue
from idlelib.WidgetRedirector import WidgetRedirector

#This class is totally not mine, and is from the unpythonic tkinter wiki
class ReadOnlyText(Tkinter.Text):
    """Sets up a read-only chat box that can be added to with the
    Text.insert method, but cannot be modified by the user because
    all the input is rerouted"""
    def __init__(self, *args, **kwargs):
        Tkinter.Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = self.redirector.register(
                                  "insert", lambda *args, **kw: "break")
        self.delete = self.redirector.register(
                                  "delete", lambda *args, **kw: "break")

class Chat(Tkinter.Frame, object):
    """Sets up a non-editable window where received text is displayed
    and a smaller chat panel where one can type and send messages
    by hitting the enter key"""
    def __init__(self, master, Client):
        """Master needs to be a Tk instance, and client needs to be an
        Client instance"""
        super(Chat, self).__init__(master)
        self.pack(fill = 'both', expand = True)
        self.grid()
        self.create_widgets()
        master.grid_propagate(True)
        master.grid_rowconfigure(0, weight = 1)
        master.grid_columnconfigure(0, weight = 1)
        self.Client = Client
        threading.Thread(target = self.listen).start()

    def destroy(self):
        self.Client.disconnect()
        super(Chat, self).destroy()

    def create_widgets(self):
        self.chat_box = ReadOnlyText(self, borderwidth=3)
        self.chat_box.grid()
        scrollb = Tkinter.Scrollbar(self, command=self.chat_box.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.chat_box['yscrollcommand'] = scrollb.set

        self.message_box = Tkinter.Entry(self)
        self.grid_rowconfigure(2, weight = 1)
        self.message_box.grid({'row': 2,
                               'rowspan': 2,
                               'sticky': 'WNSE'})
        self.message_box.bind('<Return>', self.send)

    def send(self, *args):
        if self.message_box.get():
            self.Client.send(self.message_box.get())
            self.message_box.delete(0, len(self.message_box.get()) + 1)

    def listen(self):
        while self.Client.is_running():
            try:
                self.chat_box.insert(
                Tkinter.END, self.Client.message_queue.get(timeout = 1) + (
                '\n'))
                self.chat_box.see(Tkinter.END)
            except Queue.Empty:
                continue

    def __repr__(self):
        return "GUI representation of chat, with {} in the chat buffer".format(
        self.message_box.get())

if __name__ == '__main__':
    ip = raw_input('ip (Nothing for localhost): ')
    port = int(raw_input('port: '))
    name = raw_input('Name (Nothing for Timidger): ') or 'Timidger'
    Client = Client(port, ip, name)
    root = Tkinter.Tk()
    chat = Chat(root, Client)
    root.mainloop()
