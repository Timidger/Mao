def flip_deck(server):
    """Flips the deck over, so the bottom card is top and vice versa"""
    server.deck.cards = server.deck.cards[::-1]

def shuffle_deck(server):
    """Shuffles the deck using the Modern Fisher-Yates Shuffle Algorithm
    (the default in Mao)"""
    server.deck.shuffle()

def remove_top_card(server):
    """Take the top card of the deck and throw it into the void where it is
    never seen nor heard from again"""
    server.deck.remove()

def new_deck(server):
    """Replaces the current deck with a new one"""
    server.deck.remove(cardrange = len(server.deck.cards))
    server.update_deck()
