import threading
import Queue
from src.Client.Client import Client
from src.Base.Card import Card


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
