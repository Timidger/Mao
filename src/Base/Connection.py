# -*- coding: utf-8 -*-

import socket
import threading
import pickle
import sys
import time
import random
import Queue
from ..Base import Player
from ..Base.Card import Card
from ..Base import Pile

class Connection(socket.socket, object):
    def __init__(self, ip, port):
        super(Connection, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((ip_address or socket.getfqdn(), port))

    def send(self, data, connection):
        # Pickle the data, so abstract data types can be transferred
        pickled = pickle.dumps(data.encode()) + b';'
        connection.send(bytes(len(pickled)) + b':')
        connection.sendall(pickled)


    # Lets put a try, finally clause in here, clean up the code a bit so it's more readable (the comments were a great start), and see if we even need to implement that recursion (I have a feeling we don't)
    # Catch the Socket error (not timeout), close the connection, then re throw the same exception (so higher levels can deal with it)

    def receive(self, connection, timeout=10):
            """Get a response from the server and de-pickles it. If the actual
            message takes too long (longer than 10 seconds or timeout if given)
            then a socket.error is raised"""
            error = socket.error("Connection closed!")
            def get_message(connection, timeout, message=None):
                """Recursively get messages from the connection. If part of
                another message is found, that is also returned"""
                # This not part of another message from a recursive call
                if not message:
                    # So get the start of the message in string form
                    message = connection.recv(2048).decode(encoding='utf-8')
                # Split up the message length and the message
                received = message.split(':', 1)
                # Get the decoded message length and message
                length.decode(), data.decode() = received
                # Convert the length to an int and check that it is valid
                length = int(length)
                if not length:
                    raise error
                # Remember the old timeout to be reset later
                old_timeout = connection.gettimeout()
                # For slow connections, this value can be set higher
                connection.settimeout(timeout)
                # While we don't have the whole message
                while len(data) < length:
                    # Read from the socket
                    message = connection.recv(2048)
                    # Connection abrubtly closed
                    if not message:
                        raise error
                    data += message
                # reset the timeout
                connection.settimeout(old_timeout)
                # Split the messages up in case more than one were read
                first, second = data.rsplit(';', 1)
                if first == '':
                    raise error
                # Depickle the data structure
                first = pickle.loads(first)
                data = [first] # I feel like we data should be a different name
                # If we got a bit of a second message
                if second:
                    print "Message was too long!"
                    # Get that one too
                    data.extend(get_message(connection, timeout=10,
                                            message=second))
                return data
            return get_message(connection, timeout)

    def constantly_receive(self, connection, queue):
        """Constantly receives messages from the client and passes it into
        the given queue to be handled by the server"""
        # It is automatically closed when the loop ends
        with connection:
            # Infinite loop, unless there is an error
            while True:
                data = self.receive(connection, timeout=None)
                for item in data:
                    queue.put(item)
