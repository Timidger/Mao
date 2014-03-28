# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:54:20 2013

@author: preston
"""
import socket
import pickle
import threading
import Queue
from ..Base.Card import Card
from ..Base.Pile import Pile
from ..Base.Player import Player


class Client(object):
    def __init__(self, port, ip_address = None, name = 'Player'):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address or socket.getfqdn(), port))
        print self.server.recv(2048)

        self.send(name)
        self.player = self.receive()[0]
        assert type(self.player) == Player
        self.pile = Pile()
        self.send("Give me the pile!")#Server needs to wait for the request
        self.pile.add(self.receive()[0])
        self.listener = threading.Thread(target = self.listen)
        self._connected = threading.Event()
        self.listener.start()
        self.message_queue = Queue.Queue()
        self.card_queue = Queue.Queue()
        self.pile_queue = Queue.Queue()
        self.players = None

    def is_running(self):
        return not self._connected.is_set()

    def send(self, data):
        "Send some data to the server, returns the bytes of the sent string"
        pickled = pickle.dumps(data) + ';'
        self.server.send(str(len(pickled)) + ':')
        total = 0
        while total < len(pickled):
            sent = self.server.send(pickled[total:])
            if sent == 0:
                raise socket.error("Connection Broken")
            else:
                total += sent
        return total

    def receive(self, timeout = 10, message = None):
        """Get a response from the server and de-pickles it. If the actual
        message takes too long (longer than 10 seconds or timeout if given)
        then socket.error is raised"""
        self.server.settimeout(timeout)
        if not message:
            received = self.server.recv(2048).split(':', 1)
        else:
            received = message.split(':', 1)
        length = received[0]
        if not length:
            raise socket.error
        data = received[1]
        while len(data) < int(length):
            message = self.server.recv(2048)
            if not message:
                raise socket.error
            data += message
        self.server.settimeout(None)
        first, second = data.rsplit(';', 1)
        if first == '':
            raise socket.error('The Server closed the connection!')
        first = pickle.loads(first)
        data = []
        data.append(first)
        if second:
            data.extend(self.receive(timeout = 10, message = second))
        return data

    def constantly_receive(self, queue):
        while self.is_running():
            try:
                data = self.receive(timeout = 1)
                for item in data:
                    queue.put(item)
            except socket.timeout:
                continue
            except socket.error:
                if self.is_running():
                    self.disconnect()
                break

    def disconnect(self):
        """Disconnects the client from the server"""
        if self.is_running():
            try:
                print 'Closing connection!'
                self.server.send('')#Closes connection
            finally:
                self._connected.set()
                self.server.close()
                print 'Connection Closed!'

    def listen(self):
        message_queue = Queue.Queue()
        get_message_thread = threading.Thread(name = (
            'Getting messages from server'.format()), target = (
            self.constantly_receive), args = (message_queue,))
        get_message_thread.start()
        try:
            while self.is_running():
                try:
                    data = message_queue.get(timeout = 1)
                except Queue.Empty:
                    continue
                if type(data) == Card:
                    card = data
                    self.pile.add((card,))
                    self.pile.update_top_card()
                    self.pile_queue.put(card)
                elif type(data) == tuple:
                    if all((type(card) == Card for card in data)):
                        for card in data:
                            self.player.add_card(card)
                            self.card_queue.put(card)
                    elif all((type(player) == str for player in data)):
                        self.players = data
                    else:
                        raise KeyError, (
                        '{} was not all Cards or strings'.format(
                        data), ' representing player names!')
                elif type(data) == str:
                    self.message_queue.put(data)
        except (socket.error, socket.timeout):
            self.disconnect()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()
