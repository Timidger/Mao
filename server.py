import time
import threading
import atexit
from os import listdir
from os.path import isfile, join
from src.Server.Server import Server
from src.Server.PlayerHandler import PlayerHandler
from src.Server.RuleHandler import RuleHandler
from src.Base.Rule import Rule
from src.Base.OptionsParser import load_configuration

from lupa import LuaRuntime

start_time = time.time()
lua = LuaRuntime()
rule_path = "./Rules/"
rule_files = [join(rule_path,f) for f in listdir(rule_path)
              if isfile(join(rule_path, f))]
rules = []
for f_ in rule_files:
    with open(f_, "r") as f:
        lines = "".join(f.readlines())
        lua_func = lua.eval(lines)
        rule = Rule(f_, None, lua_func)
        rules.append(rule)
config_parser = load_configuration("server")

#rules = []#[Rule('Test Rule', None, test_rule)]
RH = RuleHandler(lua, rules)
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
MAIN_THREAD.start()

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

while True:
    time.sleep(1)
