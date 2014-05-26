# -*- coding: utf-8 -*-

import socket
import pickle

class Connection(socket.socket, object):
    def __init__(self, ip, port):
        super(Connection, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((ip, port))

def send(data, connection):
    # Pickle the data, so abstract data types can be transferred
    pickled = pickle.dumps(data) + b';'
    # Pickle the length as well, to simplify the receiving end
    length = pickle.dumps(len(pickled)) + b':'
    connection.send(length)
    connection.sendall(pickled)

def receive(connection, timeout=10):
        """Get a response from the server and de-pickles it. If the actual
        message takes too long (longer than 10 seconds or timeout if given)
        then a socket.error is raised"""
        # Common error when listening to sockets
        error = socket.error("Connection closed!")
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

def listen(connection, queue):
    """Constantly receives messages from the client and passes it into
    the given queue to be handled by the server"""
    # It is automatically closed when the loop ends
    with connection:
        # Infinite loop, unless there is an error
        while True:
            data = receive(connection, timeout=None)
            for item in data:
                queue.put(item)

if __name__ == "__main__":
    from Card import Card
    try:
        import Queue as queue
    except ImportError:
        import queue
    import threading
    import time
    # Set up the echo server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.getfqdn(), 9000))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen(5)
    queue = queue.Queue()
    def echo(server, queue):
        connection, address = server.accept()
        listen_thread = threading.Thread(name="Listening thread",
                                         target=listen,
                                         args=(connection, queue))
        listen_thread.start()
        while True:
            # get length, which we don't care about
            message = queue.get()
            if not message:
                break
            print("Message Received: {}".format(message))
    server_thread = threading.Thread(name="Echo Server Thread",
                                     target=echo,
                                     args=(server, queue),
                                     daemon=True)
    server_thread.start()

    # This represents be the networking part of a client
    server_connection = Connection(socket.getfqdn(), 9000)
    with server_connection:
        send("HEY!" * 4, server_connection)
        send([5] * 90, server_connection)
        send(Card("Hearts", "5"), server_connection)
