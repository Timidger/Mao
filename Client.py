# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:54:20 2013

@author: preston
"""
import socket, pickle, threading, Queue
from Card import Card
from Pile import Pile
from Player import Player


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
        if not message:
            received = self.server.recv(2048).split(':', 1)
        else:
            received = message.split(':', 1)
        length = received[0]
        if not length:
            raise socket.error
        data = received[1]
        self.server.settimeout(timeout)
        while len(data) < int(length):
            message = self.server.recv(2048)
            if not message:
                raise socket.error
            data += message
        self.server.settimeout(None)
        first, second = data.rsplit(';', 1)
        first = pickle.loads(first)
        if first == '':
            raise socket.error('The Server closed the connection!')
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
                    print 'Added {}'.format(data.rank + data.suit)
                    self.pile.add((card,))
                    self.pile.update_top_card()
                    self.pile_queue.put(card)
                elif type(data) == tuple:
                    if all((type(card) == Card for card in data)):
                        print 'Adding this many cards: ' + str(len(data))
                        for card in data:
                            print 'added 1!'
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

if __name__ == '__main__':
    ip = raw_input('ip (nothing for localname) = ')
    port = int(raw_input('port = '))
    name = raw_input('name (nothing for "Timidger") = ') or 'Timidger'
    client = Client(port, ip, name)

    def Client_listen():
        while client.is_running():
            try:
                print client.message_queue.get(timeout = 1)
            except Queue.Empty:
                continue
    threading.Thread(target = Client_listen).start()

    while client.is_running():
        message = raw_input()
        if client.is_running():
            if message.startswith('/'):
                command = message.split('/', 1)[1].split()
                if command[0] == 'pile':
                    if client.pile.top_card.rank and (
                    client.pile.top_card.suit):
                        print client.pile.top_card.rank + ' of ' + (
                        client.pile.top_card.suit)
                    else:
                        print 'No top card!'
                elif command[0] == 'hand':
                    for index, card in enumerate(client.player.hand):
                        print str(index) + ': ' + (
                        card.rank + ' of ' + card.suit)
                elif command[0] == 'send' and command[1]:
                    try:
                        card = (client.player.get_card(int(command[1])))
                        print card.rank + ' of ' + card.suit + ' sent!'
                        client.send(card)
                    except IndexError:
                        print "There are only {} cards!".format(len(
                        client.player.hand) + 1)
                elif command[0] == 'draw':
                    client.send(Card(None, None))
                elif command[0] == 'help':
                    print "Commands:"
                    print "    pile: shows top card"
                    print "    hand: shows hand"
                    print "    send: send the card of the given index"
                    print "    (0 == first, -1 == last)"
                    print "    draw: draw a card....duh"
                else:
                    print "'/{}' is an invalid command!".format(' '.join(
                                                         command))
                print
            else:
                client.send(message)
