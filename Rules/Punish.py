def punish_many_because(server, *args, **kargs):
    """Provides a special wrapper around the punish method. Args is a list of
    the strings that will be printed as the reason, seperated by a newline. The
    kargs is a dictionary where the players are the keys and the values are how
    much they are being punished.
    """
    for player, amount in kargs.iteritems():
        server.punish(player, penalty_num = amount, 
                      reason = '\n'.join(args) or None)

def punish_random(server, *args):
    """Punishes a random player in args the default amount of cards"""
    from random import choice
    server.punish(choice(args))

def punish_until(server, *args, **kargs):
    """Punishes players (*kargs = {player: amount} until all the events in args 
    are set at the same time"""
    from threading import Event
    while not all(event.is_set() for event in args if type(event) == Event):
        punish_many_because(server, kargs = kargs)
