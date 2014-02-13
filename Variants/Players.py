def skip_player(server):
    server.player_handler.next_player()

def reverse_order(server):
    server.player_handler.order = - server.player_handler.order
    server.player_handler.next_player()
    server.player_handler.next_player()
