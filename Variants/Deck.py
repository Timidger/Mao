def flip_deck(server):
    server.deck.cards = server.deck.cards[::-1]
    server.deck.update_top_card()

def shuffle_deck(server):
    server.deck.shuffle()

def remove_top_card(server):
    server.deck.remove()

def remove_cards_from__deck(server):
    server.deck.remove(cardrange = len(server.deck.cards))
