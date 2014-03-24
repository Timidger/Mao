def skip_player(server):
    """Skips the next player"""
    server.player_handler.next_player()

def reverse_order(server):
    """Reverses the order, then goes to the player that should have gone next
    """
    server.player_handler.order = -server.player_handler.order
    server.player_handler.next_player()
    server.player_handler.next_player()

def play_again(server):
    """The same player plays again, preserving the current order"""
    server.player_handler.current_player = (
    server.player_handler.get_player(-server.player_handler.order))
