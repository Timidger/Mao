import threading
import Queue
from src.Client.Client import Client
from src.Base.Card import Card
from src.Base.OptionsParser import load_configuration

# Automated login using the server configuration
config = load_configuration("server")

ip = config.get("Misc.", "ip")
port = config.getint("Misc.", "port")
name = 'Timidger'
connection = Client(port, ip, name)


def Client_listen():
    while connection.is_running():
        try:
            print connection.message_queue.get(timeout=1)
        except Queue.Empty:
            continue
listen_thread = threading.Thread(target=Client_listen)
listen_thread.start()

with connection as client:
    try:
        while True:
            message = raw_input()
            # If the user put in a command
            if message.startswith('/'):
                command = message.split('/', 1)[1].split()
                if command[0] == 'pile':
                    if client.pile:
                        print client.pile[0]
                    else:
                        print 'No top card!'
                elif command[0] == 'hand':
                    for index, card in enumerate(client.player.hand):
                        print str(index) + ': ' + str(card)
                elif command[0] == 'send' and len(command) > 1:
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
                    print "'/{}' is an invalid command!".format(command[0])
                print
            else:
                if message:
                    client.send(message)
                else:
                    break
    finally:
        client.disconnect()
