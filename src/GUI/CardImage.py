import os
from PIL import Image, ImageTk, ImageOps
import Tkinter

# Default card size: 145x205
CARD_SIZE = (145, 205)
image_directory = "Images/Cards/"
IMAGE_EXT = ".gif"

# Default symbol size: 20x20
SYMBOL_SIZE = (20, 20) # Size of the chunk that denotes a card's rank (x, y)

RANK_TOP_CORDS = (7, 8, 27, 28) # Cords for the top rank symbol
RANK_BOTTOM_CORDS = (115, 177, 135, 197) # Cords for the bottom rank symbol

SUIT_TOP_CORDS = (7, 32, 27, 52) # Cords for the top suit symbol
SUIT_BOTTOM_CORDS = (113, 153, 133, 173) # Cords for the bottom suit symbol

class CardImage(Tkinter.Button, object):
    """Image representation of a card"""
    def __init__(self, master, card):
        """master is the root Tk window, card is the card that will be
        displayed  by the program"""
        super(CardImage, self).__init__(master)
        self.card = card
        rank, suit = card.rank, card.suit
        image_file = self.make_card_image(card.rank, card.suit)
        self.image = ImageTk.PhotoImage(image_file)

    def get_suit_symbol(self, suit):
        """Gets the suit symbol from the image directory"""
        # Chop of the last letter, because otherwise the suit is plural
        path = (image_directory + "Suits/{}" + IMAGE_EXT).format(suit[:-1])
        return Image.open(path)

    def get_rank_symbol(self, rank):
        """Gets the rank symbol from the image directory"""
        path = (image_directory + "Ranks/{}" + IMAGE_EXT).format(rank)
        return Image.open(path)

    def get_blank_card(self, card_suit):
        """Depending on the type of the suit, returns a card image with either
        red or black borders"""
        card = image_directory + "blank_card_{}" + IMAGE_EXT
        if card_suit in ("Hearts", "Diamonds"):
            return Image.open(card.format("black"))
        elif card_suit in ("Clubs", "Spades"):
            return Image.open(card.format("red"))
        else:
            raise ValueError, (
                "card_suit must one of these: {}, was {}".format(
                    "Hearts Diamonds Clubs Spades".split(), card_suit))

    def add_symbol(self, image, symbol, cords):
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

    def __repr__(self):
        path = os.path.abspath(self.image.name)
        return path
