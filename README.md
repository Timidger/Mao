#Mao
[Mao](http://en.wikipedia.org/wiki/Mao_%28card_game%29) is a card game, usually played amongst teenagers, where the rules are dynamic. Usually, only one player (known as the chairman) knows the rules and is entrusted to enforce them fairly and consistently. Because this is a demanding job, and the dynamic addition of rules as the game goes on complicates it further, in this adaption of the game the computer, in the form of a central server, handles the rules. This way, all the players can participate as clueless players.

##Rules
Unlike most adaptations of the card game, you create rules by programming them in Python modules. Each rule is a function that takes a single parameter, `server`, which is the entire server object. Though this gives rules a lot of power, this is counteracted by the avaliablity of the source code.

The `trigger` that activate the rule (which is either a phrase or a card) is determined when the rule is imported into the server. It is not part of the rule's code.

Any side effects from a rule's `trigger`, (i.e: placing down a card while it is your turn means it is the next player's turn) happen *before* the rule's code executes. In other words, if a rule whose trigger is a card, the code `server.player_handler.next_player()` will execute after the turn has already switched, meaning it is the same player's turn *again*.

Here some example rules:

```python
def flip_deck(server):
    server.deck.cards = server.deck.cards[::-1]
```
This rule flips the deck.

```python
def skip_player(server):
    server.player_handler.next_player()
```
This rule skips the current player 

```python
def reverse_order(server):
    server.player_handler.order = -server.player_handler.order
    server.player_handler.next_player()
```
This rule flips the order around, and then goes to the next player. Because of the timing of rule execution, the code executes *after* the player's input is handled, so if this was the effect of placing down a card successfully, the player that just went is the current player.

##Server Configuration
The 'options.cfg' file contains options to control server options, such as the default amount of cards that a player receives when they are punished.

The server actually reads this information at runtime, so they can be edited while the server is running, without having to restart it each time.
