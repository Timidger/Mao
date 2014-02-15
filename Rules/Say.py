def whisper(server, **kargs):
    """Whisper to the players in kargs the messages {player: message}"""
    for player, message in kargs.iteritems():
        server.send("From your supreme leader: " + 
                    message, server.get_client(player))

def inform(server, *args):
    """Sends the string in args (seperated by newlines) to all players"""
    server.send_all('\n'.join(args) or "*Cough*") #If send nothing, disconnects
