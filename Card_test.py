import time
import os
from src.GUI.Card import CardImage
from src.Base.Card import Card as Card

ranks = "Ace 2 3 4 5 6 7 8 9 10 Jack Queen King".split()
suits = "Hearts Spades Diamonds Clubs".split()

deck = [Card(suit, rank) for rank in ranks for suit in suits]
for card in deck:
    CardImage(card)
    time.sleep(.1)

time.sleep(3)
os.system("killall display")
