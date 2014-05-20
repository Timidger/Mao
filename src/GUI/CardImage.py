import os
from PIL import Image, ImageTk, ImageOps
import Tkinter

# Default card size: 145x205
CARD_SIZE = (145, 205)
image_directory = "Images/Cards/"
IMAGE_EXT = ".gif"

# Default symbol size: 20x20
SYMBOL_SIZE = (20, 20) # Size of the chunk that denotes a card's rank (x, y)

def get_rank_cords(card_size, symbol_size):
    """Returns two lists representing the coordinates for the top and bottom
    rank symbol on the card. This location is determined by taking a fraction
    of the card_size using the symbol_size."""
    # Get the top cords
    x = card_size[0] // symbol_size[0]
    y = card_size[1] // symbol_size[1]
    top_cords = [x, y, symbol_size[0] + x, symbol_size[1] + y]

    # Get the bottom cords, which is just a mirror of the top cords
    x = card_size[0] - x
    y = card_size[1] - y
    # Since we start from the bottom, the first corrdinates have to be added
    bottom_cords = [x - symbol_size[0], y - symbol_size[1], x, y]
    return (top_cords, bottom_cords)

def get_suit_cords(card_size, symbol_size, y_offset):
    """Returns two tuples representing the coordinates for the top and bottom
    suity symbol on the card. This operates exactly like get_rank_cords but the
    offset is provided here so that the suit symbol can be below the rank
    symbol"""
    # The y_offset is based off the symbol's y-size
    y_offset += symbol_size[1]
    rank_cords = get_rank_cords(card_size, symbol_size)
    rank_cords[0][1] += y_offset
    rank_cords[0][3] += y_offset
    # Now we do it again upside down
    rank_cords[1][1] -= y_offset
    rank_cords[1][3] -= y_offset
    return rank_cords

print(get_rank_cords(CARD_SIZE, SYMBOL_SIZE))
print(get_suit_cords(CARD_SIZE, SYMBOL_SIZE, 5))

RANK_TOP_CORDS = (7, 10, 27, 30) # Cords for the top rank symbol
RANK_BOTTOM_CORDS = (118, 175, 138, 195) # Cords for the bottom rank symbol

SUIT_TOP_CORDS = (7, 35, 27, 55) # Cords for the top suit symbol
SUIT_BOTTOM_CORDS = (118, 150, 138, 170) # Cords for the bottom suit symbol

class CardImage(Tkinter.Button, object):
    """Image representation of a card"""
    def __init__(self, master, card):
        """master is the root Tk window, card is the card that will be
        displayed  by the program"""
        super(CardImage, self).__init__(master)
        self.card = card
        rank, suit = card.rank, card.suit
        if rank and suit:
            # Generate a card image
            image_file = self.make_card_image(card.rank, card.suit)
        else:
            # Generate a blank card(Clubs has a black border)
            image_file = self.get_blank_card("Clubs")
        self.image = ImageTk.PhotoImage(image_file)
        back_image = self.get_back_image()
        self.back_image = ImageTk.PhotoImage(back_image)
        self.config(relief='flat', image=self.image)

    @staticmethod
    def get_suit_symbol(suit):
        """Gets the suit symbol from the image directory"""
        # Chop of the last letter, because otherwise the suit is plural
        path = (image_directory + "Suits/{}" + IMAGE_EXT).format(suit[:-1])
        return Image.open(path)

    @staticmethod
    def get_rank_symbol(rank):
        """Gets the rank symbol from the image directory"""
        path = (image_directory + "Ranks/{}" + IMAGE_EXT).format(rank)
        return Image.open(path)

    @staticmethod
    def get_blank_card(card_suit):
        """Depending on the type of the suit, returns a card image with either
        red or black borders"""
        card = image_directory + "blank_card_{}" + IMAGE_EXT
        if card_suit in ("Hearts", "Diamonds"):
            return Image.open(card.format("red"))
        elif card_suit in ("Clubs", "Spades"):
            return Image.open(card.format("black"))
        else:
            raise ValueError, (
                "card_suit must one of these: {}, was {}".format(
                    "Hearts Diamonds Clubs Spades".split(), card_suit))

    @staticmethod
    def add_symbol(image, symbol, cords):
        """Adds the symbol to the image at the given cords. The cords is a
        tuple of four numbers representing the top left and bottom right edges
        of the symbol's image"""
        image.paste(symbol, cords, symbol.convert("RGBA"))

    def make_card_image(self, rank, suit):
        """Using the basic images that make up a card found in the image
        directory, constructs a card from the given rank and suit"""
        # Open a blank card corresponding to the given suit
        card = self.get_blank_card(suit)

        # Get the symbol corresponding to the rank
        rank_symbol = self.get_rank_symbol(rank)
        # Add the symbol to the top of the card
        self.add_symbol(card, rank_symbol, RANK_TOP_CORDS)
        # Flip the symbol
        rank_symbol = rank_symbol.rotate(180)
        # Add the symbol to the bottom of the card
        self.add_symbol(card, rank_symbol, RANK_BOTTOM_CORDS)

        # Get the symbol corresponding to the suit
        suit_symbol = self.get_suit_symbol(suit)
        # Add the symbol to the top of the card
        self.add_symbol(card, suit_symbol, SUIT_TOP_CORDS)
        # Flip the symbol
        suit_symbol = suit_symbol.rotate(180)
        # Add the symbol to the bottom of the card
        self.add_symbol(card, suit_symbol, SUIT_BOTTOM_CORDS)
        return card

    @staticmethod
    def get_back_image():
        path = image_directory + "back" + IMAGE_EXT
        return Image.open(path)

    def __repr__(self):
        path = os.path.abspath(self.image.name)
        return path
