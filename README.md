#Mao
[Mao](http://en.wikipedia.org/wiki/Mao_%28card_game%29) is a card game, usually played amongst teenagers, where the rules are dynamic. Usually, only one player (known as the chairman) knows the rules and is entrusted to enforce them fairly and consistently. Because this is a demanding job, and the dynamic addition of rules as the game goes on complicates it further, in this adaption of the game the computer, in the form of a central server, handles the rules. This way, all the players can participate as clueless players.

##Rules
Unlike most adaptations of the card game, you create rules by programming them in Python modules. Each rule is a function that takes a single parameter, `server`, which is the entire server object. Though this gives rules a lot of power, this is counteracted by the avaliablity of the source code.
Here is an example rule:

```python
def flip_deck(server):
    server.deck.cards = server.deck.cards[::-1]
    server.deck.update_top_card()
```
This function simply flips the deck.

The `update_top_card` call is required to update the top card, which holds a reference to the top card. This will probably be incorporated into its own check eventually, because this could cause display problems if it is forgotten.

##Server Configuration
The 'options.cfg' file contains options to control server options, such as the default amount of cards that a player receives when they are punished.

The server actually reads this information at runtime, so they can be edited while the server is running, without having to restart it each time.
