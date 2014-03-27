import time
import threading
import atexit
from src.Server.Server import Server
from src.Server.PlayerHandler import PlayerHandler
from src.Server.RuleHandler import RuleHandler
from src.Base.Rule import Rule
from src.Base.OptionsParser import config_parser

start_time = time.time()

def test_rule(server_object):
    global a
    a = exit
rules = [Rule('Test Rule', None, test_rule)]
RH = RuleHandler(rules)
PH = PlayerHandler([])
ip = config_parser.get('Misc.', 'ip')
port = config_parser.getint('Misc.', 'port')
players = PH.players
server = Server(RH, PH, port, ip)
clients = server.clients
deck = server.deck
pile = server.pile

print 'Server at {}:{}'.format(ip or 'localhost', port)
MAIN_THREAD = threading.Thread(target = server.main_loop)
print "Type 'MAIN_THREAD.start()' to start the game!"

def uptime():
    print "The server has been running for {} seconds".format(
    int(time.time() - start_time))

atexit.register(server.shutdown)
