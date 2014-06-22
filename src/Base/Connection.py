# -*- coding: utf-8 -*-

import socket
import pickle
import threading
try:
    # For python 2.x
    import Queue as queue
except ImportError:
    # For python 3.x
    import queue


class Connection(socket.socket, object):
    def __init__(self, *args, **kargs):
        super(Connection, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        # Make the connection reusable after this one dies
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.messages = queue.Queue()

    def _send_to(self, data, connection):
        # Pickle the data, so abstract data types can be transferred
        pickled = pickle.dumps(data) + b';'
        # Pickle the length as well, to simplify the receiving end
        length = len(pickled)
        pickled_length = pickle.dumps(length) + b':'
        connection.send(pickled_length)
        total = 0
        while total < len(pickled):
            sent = connection.send(pickled[total:])
            if sent == 0:
                raise socket.error("Connection Broken!")
            else:
                total += sent
        # Wait until they get the message before continuing
        return connection.recv(length)

    def constantly_listen(self, connection):
        """Constantly receives messages from the connection and passes it into
        the messages queue to be handled later"""
        # It is automatically closed when the loop ends
        try:
            # Infinite loop, unless there is an error
            while True:
                data = self.receive(connection, timeout=None)
                for item in data:
                    self.messages.put(item)
        except socket.error as e:
            self.disconnect(connection)
            print(e)

        finally:
            connection.close()

    def receive(self, connection, timeout=10):
        """Get a response from the connection and de-pickles it. If the actual
        message takes too long (longer than 10 seconds or timeout if given)
        then a socket.error is raised"""
        # Common error when listening to sockets
        error = socket.error("Connection Closed!")
        def get_messages(connection, timeout, message=b""):
            # If we have the delimiter, we have the entire message size
            if b':' not in message:
                # If not, read from the socket
                message = connection.recv(2048)
                # When the connection calls the close function
                if not message:
                    # They want to disconnect from the server
                    raise error
            length, data = message.split(b':', 1)
            # Unpickle the length and verify that it is a number
            length = int(pickle.loads(length))
            # Length of the message should never be 0
            if not length:
                raise ValueError("Message length was 0!")
            # Save the old timeout so it can be re-instated afterwards
            old_timeout = connection.gettimeout()
            connection.settimeout(timeout)
            # Get ALL the data
            while len(data) < length:
                some_data = connection.recv(2048)
                # Add to the data we already have
                data += some_data
            # Reset the timeout
            connection.settimeout(old_timeout)
            # Tell them we got the message
            connection.send(pickle.dumps(length))
            # Get the first and second message (if there is a second message)
            first, second = data.rsplit(b';', 1)
            first = pickle.loads(first)
            # An empty string means the other side disconnected
            if first == '':
                raise error
            messages = [first]
            # If we got some of the next message, get the rest of that one
            if second:
                second = get_messages(connection, timeout, message=second)
                messages.extend(second)
            return messages
        return get_messages(connection, timeout)

    def disconnect(self, connection):
        try:
            connection.send(b'')
            connection.shutdown(socket.SHUT_RDWR)
        except socket.error as e:
            pass
        finally:
            connection.close()


class Client(Connection, object):
    def __init__(self, ip, port):
        super(Client, self).__init__()
        self.connect((ip, port))

    def send_to_server(self, data):
        self._send_to(data, self)

    def disconnect(self, *args):
        super(Client, self).disconnect(self)


class Server(Connection, object):
    def __init__(self, ip, port):
        super(Server, self).__init__()
        # listen on this address
        self.bind((ip, port))
        super(Server, self).listen(5)
        self.connections = {}   # {Connection object: IP address}

    def accept_connections(self):
        while True:
            self.settimeout(None)
            connection, address = server.accept()
            if (connection, address) in self.connections:
                connection.send("Same ip as other user! Connnection aborted!")
                connection.close()
                raise socket.error("IP {} already taken!".format(address))
            # Add the connection to the list of connections
            self.connections.update({connection: address})
            # Set up a socket to listen to the data from the connection
            thread_name = "Listening to: {}".format(address)
            listen_thread = threading.Thread(name=thread_name,
                                             target=self.constantly_listen,
                                             args=(connection,))
            listen_thread.setDaemon(True)
            listen_thread.start()

    def disconnect(self, connection):
        super(Server, self).disconnect(connection)
        if connection in self.connections:
            self.connections.pop(connection)

    def shutdown(self):
        self.close()
        # Sometimes the dict size changes while it is running
        # This causes a RunTimeError to happen, stopping it from disconnecting
        # The worst that will happen is disconnect already disconnected client
        connections = self.connections.copy()
        assert connections is not self.connections
        for connection in connections:
            self.disconnect(connection)


if __name__ == "__main__":
    from Card import Card
    import time
    # Set up the echo server
    server = Server(socket.getfqdn(), 9000)
    def echo(server):
        while True:
            # get length, which we don't care about
            try:
                message = server.messages.get(timeout=1)
                print("Message Received: {}".format(message))
            except queue.Empty:
                break
    echo_thread = threading.Thread(name="Echo message-getting thread",
                                   target=echo,
                                   args=(server,))
    echo_thread.start()
    server_thread = threading.Thread(name="Server Thread",
                                     target=server.accept_connections)
    server_thread.setDaemon(True)
    server_thread.start()

    # This represents be the networking part of a client
    client = Client(socket.getfqdn(), 9000)
    send = client.send_to_server
    send("HEY!" * 4)
    send([5] * 90)
    send(Card("Hearts", "5"))
    send("blurg")
    # Client disconnects from server, server still running
    client.disconnect()
    # Need to wait just a mili-second for the server to register the change
    # God I hate multi-threaded programs...
    time.sleep(.1)
    error_message = ("The server did not shut down the connection! Of course,",
                     " this could be an issue of time. Perhaps wait a bit",
                     " longer?")
    # Server is not hosting anyone
    assert not server.connections, error_message
    client = Client(socket.getfqdn(), 9000)
    # This time the server disconnects
    server.disconnect(client)
    time.sleep(.1)
    assert not server.connections, error_message
    # Server no longer takes requests, flags are set so the game can stop
    server.shutdown()
