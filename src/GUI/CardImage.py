import os
from PIL import Image, ImageTk, ImageOps
import Tkinter


IMAGE_DIRECTORY = "Images/Cards/"
IMAGE_EXT = ".gif"

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

def get_suit_cords(card_size, symbol_size):
    """Returns two tuples representing the coordinates for the top and bottom
    suity symbol on the card. This operates exactly like get_rank_cords but
    it is offset based on the y-size of the symbol."""
    # The y_offset is the symbol size + 1/4 of the symbol size
    y_offset = symbol_size[1] // 4 + symbol_size[1]
    rank_cords = get_rank_cords(card_size, symbol_size)
    rank_cords[0][1] += y_offset
    rank_cords[0][3] += y_offset
    # Now we do it again upside down
    rank_cords[1][1] -= y_offset
    rank_cords[1][3] -= y_offset
    return rank_cords

def get_image_path(path):
    """Adds the image directory and file extension to the path"""
    return (IMAGE_DIRECTORY + "{}" + IMAGE_EXT).format(path)

def get_suit_symbol(suit):
    """Gets the suit symbol from the image directory"""
    # Chop of the last letter, because otherwise the suit is plural
    path = get_image_path("Suits/{}".format(suit[:-1]))
    return Image.open(path)

def get_rank_symbol(rank):
    """Gets the rank symbol from the image directory"""
    path = get_image_path("Ranks/{}".format(rank))
    return Image.open(path)

def get_blank_card(card_suit):
    """Depending on the type of the suit, returns a card image with either
    red or black borders"""
    if card_suit in ("Hearts", "Diamonds"):
        color = "red"
    elif card_suit in ("Clubs", "Spades"):
        color = "black"
    else:
        raise ValueError, (
            "card_suit must one of these: {}, was {}".format(
                "Hearts Diamonds Clubs Spades".split(), card_suit))
    path = get_image_path("blank_card_{}".format(color))
    return Image.open(path)

def add_symbol(image, symbol, cords):
    """Adds the symbol to the image at the given cords. The cords is a
    tuple of four numbers representing the top left and bottom right edges
    of the symbol's image"""
    image.paste(symbol, cords, symbol.convert("RGBA"))

def make_card_image(rank, suit):
    """Using the basic images that make up a card found in the image
    directory, constructs a card from the given rank and suit"""
    # Open a blank card corresponding to the given suit
    card = get_blank_card(suit)

    # Get the symbol corresponding to the rank
    rank_symbol = get_rank_symbol(rank)
    # Generate the cords based off the size of the rank symbol and the card
    top_cords, bottom_cords = get_rank_cords(card.size, rank_symbol.size)
    # Add the symbol to the top of the card
    add_symbol(card, rank_symbol, top_cords)
    # Flip the symbol
    rank_symbol = rank_symbol.rotate(180)
    # Add the symbol to the bottom of the card
    add_symbol(card, rank_symbol, bottom_cords)

    # Get the symbol corresponding to the suit
    suit_symbol = get_suit_symbol(suit)
    # Generate the cords based off the size of the suit symbol and the card
    top_cords, bottom_cords = get_suit_cords(card.size, suit_symbol.size)
    # Add the symbol to the top of the card
    add_symbol(card, suit_symbol, top_cords)
    # Flip the symbol
    suit_symbol = suit_symbol.rotate(180)
    # Add the symbol to the bottom of the card
    add_symbol(card, suit_symbol, bottom_cords)
    card = prepare_for_tkinter(card)
    return card

def get_back_image():
    path = get_image_path("card_back")
    image = prepare_for_tkinter(Image.open(path))
    return image

def prepare_for_tkinter(image):
    """Attempts to convert the image to an image tkinter can use to display.
    If a tk instance is not running, simply the image is returned"""
    try:
        return ImageTk.PhotoImage(image)
    except RuntimeError, e:
        print "Error: tk was not running, the image was not converted!"
        return Image
