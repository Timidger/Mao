def wild_card(server):
    """Turns the suit and rank of the top card of the pile into a wildcard by 
    setting them equal to '*'"""
    server.pile.top_card.rank = "*"
    server.pile.top_card.suit = "*"

def random_card(server):
    """Makes the top card of the pile a random card. This doesn't actually
    change the object, just the rank and suit associated with it"""
    from random import choice
    server.pile.top_card.rank = choice(
    "Ace 2 3 4 5 6 7 8 9 10 Jack Queen King".split())
    server.pile.top_card.suit = choice("Hearts Clubs Spades Diamonds".split())

def switch_suit_colour(server):
    """Switches the top card of the pile's suit over according to the following
    rules:
    
         Hearts
        \/    /\
    Spades   Clubs
        \/    /\
        Diamonds

    (Hearts ==> Spades ==> Diamonds ==> Clubs ==> Hearts ==> Spades . . .)
    """
    suits = "Hearts Clubs Diamonds Spades".split()
    server.pile.top_card.suit = suit[suits.index(server.pile.top_card.suit) - 1]

def switch_suit_type(server):
    """Switches the top card of the pile's suit between the symbols of the
    current colours.

    Hearts <==> Diamonds
    Spades <==> Clubs
    """
    red_suits = "Hearts Diamonds".split()
    black_suits = "Spades Clubs".split()
    if server.pile.top_card.suit in red_suits:
        server.pile.top_card.suit = red_suits[red_suits.index(
        server.pile.top_card.suit - 1)]

    elif server.pile.top_card.suit in black_suits:
        server.pile.top_card.suit = black_suits[black_suits.index(
        server.pile.top_card.suit - 1)]
