import os
from PIL import Image, ImageTk
import Tkinter

# Put this in the config
image_directory = "Images/Cards/"
IMAGE_EXT = ".gif"
RANK_SIZE = (20, 20) # Size of the chunk that denotes a card's rank (x, y)
TOP_CORDS = (3, 8, 23, 28) # Chunk above the top suit symbol
BOTTOM_CORDS = (120, 173, 140, 193) # Chunk below the bottom suit symbol

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

    def make_card_image(self, rank, suit):
        """Using the basic images that make up a card found in the image
        directory, constructs a card from the given rank and suit"""
        # Open a blank card corresponding to the given suit
        blank_card = Image.open(image_directory + "blank_" + suit + IMAGE_EXT)
        rank_chunk = Image.open(image_directory + "Ranks/" + rank + IMAGE_EXT)
        blank_card.paste(rank_chunk, TOP_CORDS, rank_chunk.convert("RGBA"))
        # Flip the rank image
        rank_chunk = rank_chunk.rotate(180)
        blank_card.paste(rank_chunk, BOTTOM_CORDS, rank_chunk.convert("RGBA"))
        return blank_card

    def __repr__(self):
        path = os.path.abspath(self.image.name)
        return path
