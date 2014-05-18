import time
import threading
import atexit
from src.Server.Server import Server
from src.Server.PlayerHandler import PlayerHandler
from src.Server.RuleHandler import RuleHandler
from src.Base.Rule import Rule
from src.Base.OptionsParser import load_configuration

start_time = time.time()

def test_rule(server_object):
    global a
    a = exit
config_parser = load_configuration("server")
rules = [Rule('Test Rule', None, test_rule)]
RH = RuleHandler(rules)
PH = PlayerHandler([])
ip = config_parser.get('Misc.', 'ip')
port = config_parser.getint('Misc.', 'port')
players = PH.players
server = Server(RH, PH, config_parser, port, ip)
clients = server.clients
deck = server.deck
pile = server.pile

print 'Server at {}:{}'.format(ip or 'localhost', port)
MAIN_THREAD = threading.Thread(target = server.main_loop)
print "Type 'MAIN_THREAD.start()' to start the game!"

def uptime():
    print "The server has been running for {} seconds".format(
    int(time.time() - start_time))

def kick(player_name):
    for player in players:
        if player.name == player_name:
            server.disconnect(server.get_client(player))
    else:
        raise KeyError, 'No player named "{}"!'.format(player_name)

atexit.register(server.shutdown)
