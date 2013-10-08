# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:58 2012

@author: Preston
"""
import Player, Pile, socket, threading, pickle
import time, random, Queue
from OptionsParser import config_parser
from Card import Card

class Server(object):
    def __init__(self, rule_handler, player_handler, port = None,
                 ip_address = None):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip_address or socket.getfqdn(), int(port)))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.listen(5)
        self.clients = {}
        self._server_running = threading.Event()
        threading.Thread(name = 'Connection Thread',
                         target = (self.get_connections),
                         args = (self.server,)).start()
        self.player_handler = player_handler
        self.rule_handler = rule_handler
        self.deck = Pile.Pile()
        self.pile = Pile.Pile()
        self.update_deck()
        self._main_event = threading.Event()


    def is_running(self):
        "Returns True if the server is running, or False if it is not"
        return not self._server_running.is_set()

    def get_connections(self, server):
        "Constantly get connections and adds them to clients"
        while self.is_running():
            try:
                server.settimeout(None)
                client, address = server.accept()
                if address in self.clients:
                    client.send('Same ip as other user! Connection aborted')
                    client.close()
                    continue
                client.send('Connection Established')
                print 'Connection Established with {}'.format(
                ':'.join((address[0], str(address[1]))))
                if client not in self.clients and (
                config_parser.getint('Players', 'max_players') > len(
                self.clients)):
                    player = self.authorise_player(client)
                    self.clients.update({client: player})
                    self.player_handler.add_player(player)
                    Server.send(player, client)
                    self.receive(client) #Pile request
                    Server.send(self.pile.cards, client)
                    if not self.player_handler.current_player:
                        self.player_handler.next_player()
                    threading.Thread(name = 'Listening to {0} at {1}'.format(
                        player.name, address), target = self.listen,
                        args = (client, player)).start()
                else:
                    Server.send('', client)
                    client.close()
            except (socket.timeout, socket.error):
                try:
                    client.close()
                    if client in self.clients:
                        self.clients.pop(client)
                except (socket.error, UnboundLocalError):
                    pass

    def authorise_player(self, client):
        """Generates and then authorises the player with the information
        provided by the client (It has to send the name). It then returns
        the player if it succeeds, or raises socket.error"""
        player_name = self.receive(client)[0]
        if any(player.name == player_name for player in (
        self.player_handler.players)):
            print '{} is already taken!'.format(player_name)
            raise socket.error
        print player_name + ' Joined!'
        self.send_all('[{} Joined!]'.format(player_name))
        return Player.Player(player_name, hand = self.deck.remove(0,
                               config_parser.getint('Cards', 'hand_size')))

    @staticmethod
    def send(data, client, timeout = None):
        "Send some data (pickled) to the client"
        pickled = pickle.dumps(data) +  ';'
        client.send(str(len(pickled)) + ':')
        total = 0
        while total < len(pickled):
            sent = client.send(pickled[total:])
            if sent == 0:
                raise socket.error("Connection Broken")
            else:
                total += sent

    def send_all(self, data):
        for client in self.clients:
            Server.send(data, client)

    def receive(self, client, timeout = 10, message = None):
        """Get a response from the server and de-pickles it. If the actual
        message takes too long (longer than 10 seconds or timeout if given)
        then socket.error is raised"""
        if not message:
            received = client.recv(2048).split(':', 1)
        else:
            received = message.split(':', 1)
        length = received[0]
        if not length:
            raise socket.error
        data = received[1]
        client.settimeout(timeout)
        while len(data) < int(length):
            message = client.recv(2048)
            if not message:
                raise socket.error
            data += message
        client.settimeout(None)
        first, second = data.rsplit(';', 1)
        first = pickle.loads(first)
        if first == '':
            raise socket.error('The Client closed the connection!')
        data = []
        data.append(first)
        if second:
            data.extend(self.receive(client, timeout = 10, message = second))
        return data

    def constantly_receive(self, client, queue):
        """Constantly receives messages from the client and passes it into
        the given queue to be handled by the server"""
        while self.is_running() and client in self.clients:
            try:
                data = self.receive(client, timeout = 1)
                for item in data:
                    queue.put(item)
            except socket.timeout:
                continue
            except socket.error:
                if client in self.clients:
                    self.disconnect(client)
                break

    def disconnect(self, client):
        player = self.clients.pop(client)
        try:
            Server.send('', client)
        except (socket.error, socket.timeout):
            pass
        finally:
            client.close()
            self.deck.add(player.hand)
            self.deck.shuffle()
            if player is self.player_handler.current_player:
                self._main_event.set() #Stop the thread
            self.player_handler.remove_player(player)
            self.send_all('{} disconnected'.format(player.name))
            self.send_all(self.player_handler.players)
            #Just added this, hope it works aight
            print '{} disconnected'.format(player.name)

    def shutdown(self):
        "Turns off the server, closing all the connections in clients"
        self._server_running.set()
        clients = []
        clients.extend(self.clients.iterkeys())
        for client in clients:
            self.disconnect(client)
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()

    def get_client(self, player):
        """Returns the client connected to the player instance"""
        reversed_map = {player: client for client, player in (
        self.clients.iteritems())}
        return reversed_map.get(player)

    def punish(self, player, penalty_num = config_parser.getint(
               'Punishment','penalty_num'), reason = None, cards = None):
        """The player is punished by being given penalty_num of cards.
        Raises a KeyError if the player is not in the list of players.
        If cards is given, then it appends that to the cards so that they are
        sent as one batch"""
        if cards is None:
            cards = ()
        if reason is None:
            reason = random.choice(config_parser.get(
                    'Punishment', 'default_phrases').split(';')).format(
                    name = player.name, random_card = (
                    random.choice(player.hand).rank + ' of ' + (
                    random.choice(player.hand).suit)))
        self.send_all('Penalty card for {} '.format(player.name) + reason)
        if player in self.player_handler.players:
            self.update_deck()
            cards = self.deck.remove(0, penalty_num) + cards
            Server.send(cards, self.get_client(player))
            for card in cards:
                player.add_card(card)
        else:
            raise KeyError, player.name + ' is not in players!'

    def constantly_punish(self, player, penalty_num, punish_timer, event):
        """Constantly punishes the player the number of cards in penalty_num
        until the event is set. If no event is given, uses the main_event
        (the one that is set when the current player finally plays a card)"""
        while player in self.player_handler.players:
            punish_thread = threading.Timer(interval = punish_timer,
                                            function = self.punish,
                                            args = [player, penalty_num])
            punish_thread.start()
            if event.wait(punish_timer):
                punish_thread.cancel()
                event.clear()
                return True

    def update_deck(self):
        "Checks if the deck is getting low (<= 26), and adds card if it is"
        if len(self.deck.cards) <= 26:
            suits = []
            for suit in (
            config_parser.get('Cards', suit_type).split() for suit_type in (
            option for option in config_parser.options('Cards') \
            if option.endswith('suit'))):
                suits.extend(suit)
            ranks = config_parser.get('Cards', 'ranks').split()
            new_deck = (Pile.Pile([Card(suit, rank) for rank in \
            ranks for suit in suits]))
            self.deck.add(new_deck.cards)
            self.deck.shuffle()
            self.deck.update_top_card()

    def main_loop(self, timer = config_parser.getint('Punishment', 'timer'),
                  penalty_num = config_parser.getint('Punishment',
                  'penalty_num')):
        """Main loop that should be called after initalisation. timer is the
        amount of time a player has to play before he is punished for taking
        too long and penalty num is the amount he is punished by"""
        while self.is_running():
            if self.player_handler.current_player:
                print 'Current Player: {}'.format(
                    self.player_handler.get_current_player())
                if self.constantly_punish(self.player_handler.current_player,
                                    penalty_num, timer,
                                    self._main_event):
                #Wait for a player to play
                    self.player_handler.next_player()
                    self.player_handler.update_order()
                    self.update_deck()
                    self.deck.update_top_card()
            else:
                time.sleep(1)
        self._main_event.set()

    def listen(self, client, player):
        """Constantly listens for messages from the respective client.
        Depending on the input, the player is either sent a card or nothing
        """
        message_queue = Queue.Queue()
        get_message_thread = threading.Thread(name = (
            'Getting messages from {}'.format(player.name)), target = (
            self.constantly_receive), args = (client, message_queue))
        get_message_thread.start()
        self.send(self.player_handler.players, client)#Added this too
        try:
            while self.is_running():
                try:
                    data = message_queue.get(timeout = 1)
                except Queue.Empty:
                    continue
                if not self.is_running():
                    #else it'd sent to a broken socket
                    break
                for code in self.rule_handler.check_rules(data,
                                                          config_parser.get(
                                                          'Rules',
                                                          'allow_no_trigger'
                                                          )):
                    threading.Thread(name = 'A Rule thread',
                                     target = lambda: code).start()
                if type(data) == str:
                    self.send_all('{player}: {message}'.format(
                    player = player.name, message = data))
                    print '{player}: {message}'.format(
                    player = player.name, message = data)
                    self.rule_handler.said(data, player,
                                 PH.get_player_distance(player))
                elif player == self.player_handler.current_player and (
                type(data) == Card):
                    card_index = player.get_card_index(data)
                    if card_index is not None:#Card index could be 0
                        print '{player} attempted to play {card}'.format(
                                player = player.name,
                                card = data.rank + ' of ' + data.suit)
                        card = player.get_card(card_index)
                        if any((card.suit == self.pile.top_card.suit,
                        card.rank == self.pile.top_card.rank,
                        not self.pile.top_card.suit,
                        not self.pile.top_card.rank)):
                            print ('{card} is now the top card'.format(
                            card = card.rank + ' of ' + card.suit))
                            self._main_event.set()
                            self.pile.add((card,))
                            self.send_all(card)
                            self.rule_handler.played(card, player,
                                           PH.get_player_distance(
                                           player))
                        else:
                            print (
                            '{card} was given back to {player}'.format(
                            player = player.name, card = card.rank + (
                            ' of ' + card.suit)))
                            assert type(data) == Card
                            if not data.rank and not data.suit:
                                data = None
                            else:
                                data = (data,)
                            self.punish(player, cards = data, reason = (
                            "for not playing a valid card"))
                    elif not data.rank and not data.suit:
                        self._main_event.set()
                        self.punish(player)#They draw a card
                    else:
                        self._main_event.set()
                        self.send_all(
                        '{} was caught with a fake card!'.format(
                        player.name))
                        print '{} was caught with a fake card!'.format(
                        player.name)
                        raise socket.error

                else:
                    assert type(data) == Card
                    if not data.rank and not data.suit:
                        data = None
                    else:
                        data = (data,)
                    self.punish(player, cards = data, reason = (
                    'for playing out of turn!'))
        except (socket.error, socket.timeout):
            if self.is_running() and client in self.clients:
                self.disconnect(client)
            return

if __name__ == '__main__':
    from PlayerHandler import PlayerHandler
    from RuleHandler import RuleHandler, RuleGenerator
    from Rule import Rule
    rules = [Rule('Test Rule', None, 'Set a to exit()')]
    RH = RuleHandler(rules)
    PH = PlayerHandler([])
    ip = config_parser.get('Misc.', 'ip')
    port = config_parser.getint('Misc.', 'port')
    players = PH.players
    server = Server(RH, PH, port, ip)

    for variable in ('RH', 'PH', 'server.deck', 'server.pile'):
        RuleGenerator.WHITE_LIST.add(variable)
    print 'Server at {}:{}'.format(ip or 'localhost', port)
    MAIN_THREAD = threading.Thread(target = server.main_loop)
    print "Type 'MAIN_THREAD.start()' to start the game!"

    def shutdown():
        server.shutdown()
        exit()

    print "Type 'shutdown()' to shutdown the server; DON'T exit the prompt"
    print
    print [var for var in vars(server).keys() if not var.startswith('_')]
    print "I don't think we need clients in here....:P"
